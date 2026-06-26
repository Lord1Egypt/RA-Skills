# -*- coding: utf-8 -*-
# 字段映射库 - 中文字段名到英文字段名

# ============================================================
# 财务报表通用字段
# ============================================================
COMMON_MAPPING = {
    '财务快报主题': 'financialReportTheme',
    '编制单位': 'reportingUnit',
    '报表类型': 'reportType',
    '归属年月': 'reportingPeriod',
    '填报人': 'reporter',
    '填报日期': 'reportDate',
}

# ============================================================
# 资产负债表字段
# ============================================================
BALANCE_SHEET_MAPPING = {
    '货币资金': 'monetaryFunds',
    '短期借款': 'shortTermBorrowings',
    '结算备付金': 'settlementProvisions',
    '向中央银行借款': 'borrowingsFromCentralBank',
    '拆出资金': 'fundsLent',
    '拆入资金': 'fundsBorrowed',
    '交易性金融资产': 'tradingFinancialAssets',
    '交易性金融负债': 'tradingFinancialLiabilities',
    '衍生金融资产': 'derivativeFinancialAssets',
    '衍生金融负债': 'derivativeFinancialLiabilities',
    '应收票据': 'notesReceivable',
    '应付票据': 'notesPayable',
    '应收账款': 'accountsReceivable',
    '应付账款': 'accountsPayable',
    '应收款项融资': 'receivablesFinancing',
    '预收款项': 'advancesFromCustomers',
    '预付款项': 'prepayments',
    '卖出回购金融资产款': 'proceedsFromSaleRepurchase',
    '应收保费': 'premiumReceivable',
    '吸收存款及同业存放': 'depositsAndInterbankPlacements',
    '应收分保账款': 'reinsuranceReceivables',
    '代理买卖证券款': 'customerSecuritiesTradingFunds',
    '应收分保合同准备金': 'reinsuranceContractReserves',
    '代理承销证券款': 'securitiesUnderwritingFunds',
    '其他应收款': 'otherReceivables',
    '合同负债': 'contractLiabilities',
    '其中：应收利息': 'interestReceivable',
    '应付职工薪酬': 'employeeBenefitsPayable',
    '应收股利': 'dividendsReceivable',
    '应交税费': 'taxesPayable',
    '买入返售金融资产': 'reverseRepurchaseAssets',
    '其他应付款': 'otherPayables',
    '存货': 'inventories',
    '其中：应付利息': 'interestPayable',
    '合同资产': 'contractAssets',
    '应付股利': 'dividendsPayable',
    '持有待售资产': 'assetsHeldForSale',
    '应付手续费及佣金': 'feesAndCommissionsPayable',
    '一年内到期的非流动资产': 'nonCurrentAssetsDueWithinOneYear',
    '应付分保账款': 'reinsurancePayables',
    '其他流动资产': 'otherCurrentAssets',
    '持有待售负债': 'liabilitiesHeldForSale',
    '流动资产合计': 'totalCurrentAssets',
    '一年内到期的非流动负债': 'nonCurrentLiabilitiesDueWithinOneYear',
    '其他流动负债': 'otherCurrentLiabilities',
    '发放委托贷款及垫款': 'loansAndAdvances',
    '流动负债合计': 'totalCurrentLiabilities',
    '债权投资': 'debtInvestments',
    '其他债权投资': 'otherDebtInvestments',
    '保险合同准备金': 'insuranceContractReserves',
    '长期应收款': 'longTermReceivables',
    '长期借款': 'longTermBorrowings',
    '长期股权投资': 'longTermEquityInvestments',
    '应付债券': 'bondsPayable',
    '其他权益工具投资': 'otherEquityInvestments',
    '其中：优先股': 'preferredShares',
    '其他非流动金融资产': 'otherNonCurrentFinancialAssets',
    '永续债': 'perpetualBonds',
    '投资性房地产': 'investmentProperties',
    '租赁负债': 'leaseLiabilities',
    '固定资产': 'fixedAssets',
    '长期应付款': 'longTermPayables',
    '在建工程': 'constructionInProgress',
    '长期应付职工薪酬': 'longTermEmployeeBenefitsPayable',
    '生产性生物资产': 'productiveBiologicalAssets',
    '预计负债': 'provisions',
    '油气资产': 'oilAndGasAssets',
    '递延收益': 'deferredIncome',
    '使用权资产': 'rightOfUseAssets',
    '递延所得税负债': 'deferredTaxLiabilities',
    '无形资产': 'intangibleAssets',
    '其他非流动负债': 'otherNonCurrentLiabilities',
    '开发支出': 'developmentExpenditure',
    '非流动负债合计': 'totalNonCurrentLiabilities',
    '商誉': 'goodwill',
    '负债合计': 'totalLiabilities',
    '长期待摊费用': 'longTermPrepaidExpenses',
    '递延所得税资产': 'deferredTaxAssets',
    '实收资本（或股本）': 'paidInCapital',
    '其他非流动资产': 'otherNonCurrentAssets',
    '其他权益工具': 'otherEquityInstruments',
    '非流动资产合计': 'totalNonCurrentAssets',
    '资本公积': 'capitalReserve',
    '减：库存股': 'treasuryStock',
    '其他综合收益': 'otherComprehensiveIncome',
    '专项储备': 'specialReserves',
    '盈余公积': 'surplusReserve',
    '一般风险准备': 'generalRiskProvisions',
    '未分配利润': 'retainedEarnings',
    '归属于母公司所有者权益（或股东权益）合计': 'totalEquityAttributableToParent',
    '少数股东权益': 'minorityInterest',
    '所有者权益（或股东权益）合计': 'totalOwnersEquity',
    '资产总计': 'totalAssets',
    '负债和所有者权益（或股东权益）总计': 'totalLiabilitiesAndEquity',
}

# ============================================================
# 现金流量表字段
# ============================================================
CASHFLOW_MAPPING = {
    '销售商品、提供劳务收到的现金': 'cashFromSalesAndServices',
    '收到的税费返还': 'taxRefundsReceived',
    '收到其他与经营活动有关的现金': 'otherCashFromOperating',
    '其中：财政补贴/政府项目回款': 'governmentSubsidiesReceived',
    '经营活动现金流入小计': 'totalOperatingCashInflows',
    '购买商品、接受劳务支付的现金': 'cashPaidForGoodsAndServices',
    '支付给职工以及为职工支付的现金': 'cashPaidToEmployees',
    '支付的各项税费': 'taxesPaid',
    '支付其他与经营活动有关的现金': 'otherCashPaidForOperating',
    '经营活动现金流出小计': 'totalOperatingCashOutflows',
    '经营活动产生的现金流量净额': 'netCashFromOperatingActivities',
}

# ============================================================
# 利润表字段
# ============================================================
PROFIT_MAPPING = {
    '营业收入': 'operatingRevenue',
    '减：营业成本': 'operatingCosts',
    '税金及附加': 'taxesAndSurcharges',
    '销售费用': 'sellingExpenses',
    '管理费用': 'administrativeExpenses',
    '研发费用': 'rdExpenses',
    '财务费用': 'financialExpenses',
    '其中：利息费用': 'interestExpense',
    '利息收入': 'interestIncome',
    '加：其他收益': 'otherIncome',
    '投资收益': 'investmentIncome',
    '信用减值损失': 'creditImpairmentLoss',
    '公允价值变动收益': 'fairValueChangeIncome',
    '资产处置收益': 'assetDisposalIncome',
    '资产减值损失': 'assetImpairmentLoss',
    '其中：政府补助': 'governmentSubsidies',
    '营业利润': 'operatingProfit',
    '加：营业外收入': 'nonOperatingIncome',
    '减：营业外支出': 'nonOperatingExpenses',
    '利润总额': 'totalProfit',
    '减：所得税费用': 'incomeTaxExpense',
    '净利润': 'netProfit',
    '其他综合收益的税后净额': 'otherComprehensiveIncome',
    '综合收益总额': 'totalComprehensiveIncome',
}

# ============================================================
# 银行账号字段
# ============================================================
BANK_ACCOUNT_MAPPING = {
    '账号名称': 'accountName',
    '归属公司': 'affiliatedCompany',
    '统一社会信用代码': 'unifiedSocialCreditCode',
    '账户类型': 'accountType',
    '信用代码': 'creditCode',
    '账户状态': 'accountStatus',
    '银行名称': 'bankName',
    '开户行': 'openingBank',
    '开户行地址': 'bankAddress',
    '银行账户': 'bankAccount',
    '币种': 'currency',
    '开户日期': 'openingDate',
    '账号用途': 'accountUsage',
}

# ============================================================
# 合并所有映射
# ============================================================
ALL_MAPPINGS = {}
ALL_MAPPINGS.update(COMMON_MAPPING)
ALL_MAPPINGS.update(BALANCE_SHEET_MAPPING)
ALL_MAPPINGS.update(CASHFLOW_MAPPING)
ALL_MAPPINGS.update(PROFIT_MAPPING)
ALL_MAPPINGS.update(BANK_ACCOUNT_MAPPING)


def get_english_name(chinese_name, index=0):
    """获取英文字段名，未知字段返回 field{N} 格式"""
    return ALL_MAPPINGS.get(chinese_name, f'field{index+1}')
