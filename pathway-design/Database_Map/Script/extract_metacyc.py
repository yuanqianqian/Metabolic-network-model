def extract_info(inputfile, outputfile):  # 输入下载的MetaCyc.xml文件,输出MetaCyc.xlsx文件
    from bs4 import BeautifulSoup
    import pandas as pd
    import re
    soup = BeautifulSoup(open(inputfile), 'xml')  # 解析 xml 文件
    # 提取MetaCyc中反应信息
    rxns_info = soup.find_all('reaction')  # 获取标签为<reaction>的全部信息
    rxnformat2str = str(rxns_info).replace('\n', '').replace(' ', '')  # 将信息存贮的方式转为连续的字符串，去除换行符和空格
    single_rxn = re.findall(r'<reaction([\s\S]+?)</reaction>', rxnformat2str)  # 将全部反应信息中拆分成单个反应的全部信息
    rxn_tiqu = []
    for rxninfo in single_rxn:  # 单个反应的全部信息
        rxn_id = re.findall(r'id="([\s\S]+?)"metaid', rxninfo)  # 反应id
        rxn_metaid = re.findall(r'metaid="([\s\S]+?)"name', rxninfo)  # 反应metacyc id
        rxn_name = re.findall(r'name="([\s\S]+?)"reversible', rxninfo)  # 反应name
        rxn_reversible = re.findall(r'reversible="([\s\S]+?)">', rxninfo)  # 反应可逆性
        rxn_gene = re.findall(r'geneProduct="([\s\S]+?)"/>', rxninfo)  # 反应基因
        rxn_link = re.findall(r'rdf:resource="([\s\S]+?)"/>', rxninfo)  # 反应在其他数据库中的链接
        reactants_info = re.findall(r'<listOfReactants>([\s\S]+?)</listOfReactants>', rxninfo)  # 反应的反应物信息
        reactants_id = re.findall(r'species="([\s\S]+?)"stoichiometry', str(reactants_info))  # 反应物id
        reactants_stoi = re.findall(r'stoichiometry="([\s\S]+?)"/>', str(reactants_info))  # 反应物系数
        reactants = zip(reactants_id, reactants_stoi)  # 以元组形式将代谢物和其系数存储到列表中
        products_info = re.findall(r'<listOfProducts>([\s\S]+?)</listOfProducts>', rxninfo)  # 反应的生成物信息
        products_id = re.findall(r'species="([\s\S]+?)"stoichiometry', str(products_info))  # 生成物id
        products_stoi = re.findall(r'stoichiometry="([\s\S]+?)"/>', str(products_info))  # 生成物系数
        products = zip(products_id, products_stoi)  # 以元组形式将代谢物和其系数存储到列表中
        rea = list(reactants)
        pro = list(products)
        left = []  # 反应方程式左边
        right = []  # 反应方程式右边
        for i in range(len(rea)):
            a = rea[i]
            left.append(str(float(a[1])) + ' ' + a[0])
        for j in range(len(pro)):
            b = pro[j]
            right.append(str(float(b[1])) + ' ' + b[0])
        str_link = ' + '
        eq_left = str_link.join(left)  # 拼接反应式左边
        eq_right = str_link.join(right)  # 拼接反应式右边
        reaction_eq = eq_left + ' --> ' + eq_right  # 反应方程式
        rxntemp = []
        rxntemp.append(", ".join(rxn_id))
        rxntemp.append(", ".join(rxn_metaid))
        rxntemp.append(", ".join(rxn_name))
        rxntemp.append(", ".join(rxn_reversible))
        rxntemp.append(", ".join(rxn_gene))
        rxntemp.append(", ".join(rxn_link))
        rxntemp.append(reaction_eq)
        rxn_tiqu.append(rxntemp)

    # 提取MetaCyc中代谢物信息
    mets_info = soup.find_all('species')
    metinfo2str = str(mets_info).replace('\n', '').replace(' ', '')
    single_met = re.findall(r'<species([\s\S]+?)</species>', metinfo2str)
    met_tiqu = []
    for metinfo in single_met:
        met_compartment = re.findall(r'compartment="([\s\S]+?)"constant', metinfo)
        met_charge = re.findall(r'charge="([\s\S]+?)"fbc:chemicalFormula', metinfo)
        met_formula = re.findall(r'chemicalFormula="([\s\S]+?)"hasOnlySubstanceUnits', metinfo)
        met_id = re.findall(r'id="([\s\S]+?)"metaid', metinfo)
        met_metaid = re.findall(r'metaid="([\s\S]+?)"name', metinfo)
        met_name = re.findall(r'name="([\s\S]+?)">', metinfo)
        met_link = re.findall(r'rdf:resource="([\s\S]+?)"/>', metinfo)
        mettemp = []
        mettemp.append(", ".join(met_id))
        mettemp.append(", ".join(met_metaid))
        mettemp.append(", ".join(met_name))
        mettemp.append(", ".join(met_compartment))
        mettemp.append(", ".join(met_charge))
        mettemp.append(", ".join(met_formula))
        mettemp.append(", ".join(met_link))
        met_tiqu.append(mettemp)

    # 提取MetaCyc中基因信息
    genes_info = soup.find_all('fbc:geneProduct')
    geneinfo2str = str(genes_info).replace('\n', '').replace(' ', '')
    single_gene = re.findall(r'<fbc:geneProduct([\s\S]+?)</fbc:geneProduct>', geneinfo2str)
    gene_tiqu = []
    for geneinfo in single_gene:
        gene_id = re.findall(r'id="([\s\S]+?)"fbc:label', geneinfo)
        gene_label = re.findall(r'label="([\s\S]+?)"fbc:name', geneinfo)
        gene_name = re.findall(r'name="([\s\S]+?)"metaid', geneinfo)
        gene_metaid = re.findall(r'metaid="([\s\S]+?)">', geneinfo)
        gene_link = re.findall(r'rdf:resource="([\s\S]+?)"/>', geneinfo)
        genetemp = []
        genetemp.append(", ".join(gene_id))
        genetemp.append(", ".join(gene_metaid))
        genetemp.append(", ".join(gene_name))
        genetemp.append(", ".join(gene_label))
        genetemp.append(", ".join(gene_link))
        gene_tiqu.append(genetemp)

    # 将这些信息放进excel中
    writer = pd.ExcelWriter(outputfile)
    pd.DataFrame(rxn_tiqu).to_excel(writer, 'reactions',
                                    header=['id', 'metaid', 'name', 'reversible', 'gene', 'datalink', 'reaction_eq'],
                                    index=False)
    pd.DataFrame(met_tiqu).to_excel(writer, 'metabolites',
                                    header=['id', 'metaid', 'name', 'compartment', 'charge', 'formula', 'datalink'],
                                    index=False)
    pd.DataFrame(gene_tiqu).to_excel(writer, 'genes', header=['id', 'metaid', 'name', 'label', 'datalink'], index=False)
    writer.save()