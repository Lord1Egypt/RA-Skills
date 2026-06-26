import os
import re
from typing import Dict, List, Any, Optional
# import logging
# from logging.handlers import TimedRotatingFileHandler
import pandas as pd
import datetime
import requests
import json

GTS_AUTHORIZATION_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), ".authorization")
GTS_ACCESS_KEY = os.getenv("GTS_ACCESS_KEY", None)
GTS_SECRET_KEY = os.getenv("GTS_SECRET_KEY", None)

# 通过 ak/sk 获取 临时 authorization

AUTHORIZATION_URL = f"https://open.gangtise.com/application/auth/oauth/open/loginV2"

def get_authorization(ak: str, sk: str):
    payload = {
        "accessKey": ak,
        "secretAccessKey": sk
    }
    response = requests.post(AUTHORIZATION_URL, json=payload)
    if response.status_code != 200:
        return None
    try:
        return response.json()["data"]["accessToken"]
    except Exception as e:
        return None

GTS_AUTHORIZATION = None
if GTS_ACCESS_KEY and GTS_SECRET_KEY:
    GTS_AUTHORIZATION = get_authorization(GTS_ACCESS_KEY, GTS_SECRET_KEY)
elif os.path.exists(GTS_AUTHORIZATION_PATH):
    with open(GTS_AUTHORIZATION_PATH, "r", encoding="utf-8") as f:
        content = json.load(f)
        if content.get("accessKey", None) and content.get("secretAccessKey", None):
            GTS_AUTHORIZATION = get_authorization(content["accessKey"], content["secretAccessKey"])
        else:
            GTS_AUTHORIZATION = None

GTS_SAVE_FILE = os.getenv("GTS_SAVE_FILE", False)
GTS_SAVE_EXTENSION = os.getenv("GTS_SAVE_EXTENSION", "md")

GANGTISE_QUOTE_DOMAIN = "https://open.gangtise.com/application/open-quote"
GANGTISE_FUNDAMENTAL_DOMAIN = "https://open.gangtise.com/application/open-fundamental"
QUOTE_URL = f"{GANGTISE_QUOTE_DOMAIN}/kline/daily"
QUOTE_HK_URL = f"{GANGTISE_QUOTE_DOMAIN}/kline-hk/daily"
QUOTE_MINUTE_URL = f"{GANGTISE_QUOTE_DOMAIN}/kline/minute"
QUOTE_ADJUST_FACTOR_URL = f"{GANGTISE_QUOTE_DOMAIN}/adjustFactor"
FINANCIAL_REPORT_INCOME_URL = f"{GANGTISE_FUNDAMENTAL_DOMAIN}/financial-report/income-statement/accumulated"
FINANCIAL_REPORT_INCOME_QUARTERLY_URL = f"{GANGTISE_FUNDAMENTAL_DOMAIN}/financial-report/income-statement/quarterly"
FINANCIAL_REPORT_BALANCE_URL = f"{GANGTISE_FUNDAMENTAL_DOMAIN}/financial-report/balance-sheet/accumulated"
FINANCIAL_REPORT_CASH_FLOW_URL = f"{GANGTISE_FUNDAMENTAL_DOMAIN}/financial-report/cash-flow-statement/accumulated"
FINANCIAL_REPORT_CASH_FLOW_QUARTERLY_URL = f"{GANGTISE_FUNDAMENTAL_DOMAIN}/financial-report/cash-flow-statement/quarterly"
FINANCIAL_REPORT_URL = FINANCIAL_REPORT_INCOME_URL
MAIN_BUSINESS_URL = f"{GANGTISE_FUNDAMENTAL_DOMAIN}/main-business"
VALUATION_URL = f"{GANGTISE_FUNDAMENTAL_DOMAIN}/valuation-analysis"

def _find_openclaw_root():
    """向上遍历目录直到找到 .openclaw，返回其上级目录作为执行目录"""
    path = os.path.abspath(os.path.dirname(__file__))
    openclaw_dir_got = False
    while path != os.path.dirname(path):
        dir_name = os.path.basename(path)
        if dir_name in (".openclaw"):
            openclaw_dir_got = True
            return os.path.abspath(path)
        path = os.path.dirname(path)
    path = os.path.abspath(os.path.dirname(__file__))
    if not openclaw_dir_got:
        openclaw_dir_got = False
        while path != os.path.dirname(path):
            dir_name = os.path.basename(path)
            if dir_name in (".agent"):
                openclaw_dir_got = True
                return os.path.abspath(path)
            path = os.path.dirname(path)
    path = os.path.abspath(os.path.dirname(__file__))
    if not openclaw_dir_got:
        openclaw_dir_got = False
        while path != os.path.dirname(path):
            dir_name = os.path.basename(path)
            if dir_name in ("workspace"):
                openclaw_dir_got = True
                return os.path.abspath(path)
            path = os.path.dirname(path)
    path = os.path.abspath(os.path.dirname(__file__))
    if not openclaw_dir_got:
        openclaw_dir_got = False
        while path != os.path.dirname(path):
            dir_name = os.path.basename(path)
            if dir_name in ("skills"):
                openclaw_dir_got = True
                return os.path.abspath(os.path.dirname(path))
            path = os.path.dirname(path)
    return os.path.abspath(os.getcwd())

openclaw_root = _find_openclaw_root()
if openclaw_root.endswith("workspace"):
    gangtise_workspace_path = os.path.join(openclaw_root, "gangtise")
else:
    gangtise_workspace_path = os.path.join(openclaw_root, "workspace", "gangtise")
if not os.path.exists(gangtise_workspace_path):
    os.makedirs(gangtise_workspace_path, exist_ok=True)

usage_dir = os.path.join(gangtise_workspace_path, ".usage")
if not os.path.exists(usage_dir):
    os.makedirs(usage_dir, exist_ok=True)

file_dir = os.path.join(gangtise_workspace_path, "files")
if not os.path.exists(file_dir):
    os.makedirs(file_dir, exist_ok=True)

def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def data_to_md(data: pd.DataFrame, range: List[int]=None, max_cell_length: int=None):
    data_copy = data.copy()
    if "metadata" in data_copy.columns:
        data_copy = data_copy.drop(columns=["metadata"])
    content = "| " + " | ".join(data_copy.columns) + " |\n"
    content += "| " + " | ".join(["-" for _ in data_copy.columns]) + " |\n"
    omitted = False
    for i, row in enumerate(data_copy.to_dict(orient="records")):
        if range:
            if i in range:
                if max_cell_length:
                    content += "| " + " | ".join([re.sub(r"\s+", " ", str(row[key]).replace("\n"," ")).replace("|", "")[:max_cell_length]+"..." if len(re.sub(r"\s+", " ", str(row[key])).replace("|", "")) > max_cell_length else re.sub(r"\s+", " ", str(row[key])).replace("|", "") for key in row.keys()]) + " |\n"
                else:
                    content += "| " + " | ".join([re.sub(r"\s+", " ", str(row[key]).replace("\n"," ")).replace("|", "") for key in row.keys()]) + " |\n"
            elif not omitted:
                content += "| ... |\n"
                omitted = True
        else:
            if max_cell_length:
                content += "| " + " | ".join([re.sub(r"\s+", " ", str(row[key]).replace("\n"," ")).replace("|", "")[:max_cell_length]+"..." if len(re.sub(r"\s+", " ", str(row[key])).replace("|", "")) > max_cell_length else re.sub(r"\s+", " ", str(row[key])).replace("|", "") for key in row.keys()]) + " |\n"
            else:
                content += "| " + " | ".join([re.sub(r"\s+", " ", str(row[key]).replace("\n"," ")).replace("|", "") for key in row.keys()]) + " |\n"
    content = content[:-1]
    return content.strip()

def add_usages(usages_list: List[Dict[str, Any]]):
    usages = {}
    for usages_item in usages_list:
        if len(usages_item) == 0:
            continue
        for k,v in usages_item.items():
            if k not in usages:
                usages[k] = v
            else:
                usages[k] = usages[k] + v
    return usages

def format_response(response: dict, method_name: str):
    
    # 保存usage
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    now = datetime.datetime.now().strftime("%H%M%S")
    usage_path = os.path.join(usage_dir, f"{today}.json")
    if response.get("usage", None):
        if os.path.exists(usage_path):
            with open(usage_path, "r", encoding="utf-8") as f:
                usage = json.load(f)
            if now in usage:
                now_usage = add_usages([response["usage"], usage[now]])
            else:
                now_usage = response["usage"]
            usage.update({now: now_usage})
        else:
            usage = {now: response["usage"]}
        with open(usage_path, "w", encoding="utf-8") as f:
            json.dump(usage, f, ensure_ascii=False)

    # 保存结果
    return_message = response.get("message", "") + "\n\n" if response.get("message", "") else ""
    method_name_map = {
        "block_component": "板块成分信息",
        "index": "指数信息",
        "financial": "财务数据",
        "earning_forecast": "盈利预测数据",
        "industry_indicator": "行业指标数据",
        "main_business": "主营业务数据",
        "quote": "行情数据",
        "security": "证券信息",
        "shareholder": "股东数据",
        "valuation": "估值数据",
        "rag": "知识库检索",
    }
    if response["state"] == "success":
        for item in response["data"]:
            module_name = item["module"]
            data = item["data"]
            extension = "csv" if item["type"] == "data" else "md"
            process_dir = os.path.join(gangtise_workspace_path, method_name)
            if not os.path.exists(process_dir):
                os.makedirs(process_dir, exist_ok=True)
            # now = datetime.datetime.now().strftime("%H%M%S")
            now = 1
            process_path = os.path.join(process_dir, f"{module_name}_{now}.{extension}")
            max_retries = 10
            for file in os.listdir(process_dir):
                if file.startswith(f"{module_name}_") and file.endswith(f".{extension}"):
                    max_retries = max(max_retries, int(file.split("_")[-1].split(".")[0])+10)
            while os.path.exists(process_path) and max_retries > 0:
                # now = datetime.datetime.now().strftime("%H%M%S")
                now += 1
                process_path = os.path.join(process_dir, f"{module_name}_{now}.{extension}")
                max_retries -= 1
                # sleep(1)
            if max_retries == 0:
                return_message = "错误信息：文件存储系统繁忙，请稍后再试"
                return return_message
            if item["type"] == "data":
                data = pd.DataFrame(data)
                data.to_csv(process_path, index=False)
                sample_data = data_to_md(data, range=[0, 1, 2, len(data)-3, len(data)-2, len(data)-1])
                return_message += "### " + method_name_map[method_name] + " " + module_name + " 数据已保存到csv：\n`" + os.path.abspath(process_path) + "`\n\n#### 样例数据:\n" + sample_data + "\n\n---\n\n"
            elif item["type"] == "files":
                with open(process_path, "w", encoding="utf-8") as f:
                    for i, file in enumerate(data):
                        f.write(f"### 查询结果 {i+1}\n")
                        f.write(f"标题：{file['标题']}\n")
                        f.write(f"文件时间：{file['文件时间']}\n")
                        f.write(f"类型：{file['类型']}\n")
                        f.write(f"类型中ID：{file['类型中ID']}\n")
                        f.write(f"内容：\"\"\"\n{file['摘要']}\n\"\"\"")
                        if i < len(data) - 1:
                            f.write("\n\n---\n\n")
                _sample_data = [file["标题"] for file in data]
                sample_data = []
                for _sample_data_item in _sample_data:
                    if _sample_data_item not in sample_data:
                        sample_data.append(_sample_data_item)
                sample_data = [f'"{x}"' for x in sample_data]
                sample_data = ", ".join(sample_data)
                return_message += "### " + method_name_map[method_name] + "查询结果具体内容已保存到md：\n`" + os.path.abspath(process_path) + "`\n\n#### 查询结果的文件标题:\n" + sample_data
    else:
        return_message = "调用gangtise服务端失败，错误信息：" + response["message"]
    if return_message.endswith("---\n\n"):
        return_message = return_message[:-6].strip()
    return return_message

def load_securities_from_file(path: str) -> List[str]:
    full_path = path
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"证券文件不存在: {path}")
    df = pd.read_csv(full_path)
    if "security_abbr" in df.columns:
        return [str(x) for x in df["security_abbr"].dropna().tolist()]
    if "security_code" in df.columns:
        return [str(x) for x in df["security_code"].dropna().tolist()]
    raise ValueError("证券文件必须包含 security_abbr 或 security_code 列")

def match_best(item: str, candidates, threshold: float = 0.6):
    """
    candidates: List[str] 时返回匹配的字符串，Dict[str, Any] 时返回匹配 key 的 {k: v}。
    无匹配返回 None。
    """
    from difflib import SequenceMatcher

    if not item or not candidates:
        return None
    if item in candidates:
        return item

    is_dict = isinstance(candidates, dict)
    keys = list(candidates.keys()) if is_dict else candidates

    if item in keys:
        return {item: candidates[item]} if is_dict else item

    best_score = 0.0
    best_key = None

    for key in keys:
        if item in key or key in item:
            overlap = min(len(item), len(key))
            score = overlap / max(len(item), len(key))
            score = max(score, 0.8)
        else:
            score = SequenceMatcher(None, item, key).ratio()

        if score > best_score:
            best_score = score
            best_key = key

    if best_score >= threshold and best_key is not None:
        return {best_key: candidates[best_key]} if is_dict else best_key
    return None

INCOME_FIELD_CN = {
    "securityCode": "证券代码",
    "companyName": "证券简称",
    "endDate": "财报截止日期",
    "fiscalYear": "财报年",
    "period": "报告期",
    "reportType": "报表类型",
    "companyType": "企业报表格式",
    "currency": "币种",
    "unit": "单位",
    "totalOperatingRevenue": "一、营业总收入",
    "operatingRevenue": "营业收入",
    "ofWhichSalesRevenue": "其中:主营业务收入",
    "ofWhichOtherOperatingIncome": "其中:其他业务收入",
    "netInterestIncome": "利息净收入",
    "ofWhichInterestIncome": "其中:利息收入",
    "ofWhichInterestExpense": "其中:利息支出",
    "premiumsEarned": "已赚保费",
    "ofWhichPremiumsIncome": "其中:保险业务收入",
    "ofWhichReinsuranceIncome": "其中:分保费收入",
    "ofWhichLessReinsurance": "其中:减:分出保费",
    "ofWhichLessUnearnedPremiumReserve": "其中:减:提取未到期责任准备金",
    "guaranteeIncome": "担保业务收入",
    "netCommissionIncome": "手续费及佣金净收入",
    "ofWhichCommissionIncome": "其中:手续费及佣金收入",
    "ofWhichBrokerageIncome": "其中:经纪业务手续费收入",
    "ofWhichInvestBankIncome": "其中:投资银行业务手续费收入",
    "ofWhichAssetManageIncome": "其中:资产管理业务手续费收入",
    "ofWhichfundManageIncome": "其中:基金管理业务手续费收入",
    "ofWhichInvestConsultIncome": "其中:投资咨询业务收入",
    "ofWhichRiskManageIncome": "其中:风险管理业务收入",
    "ofWhichInvestManageIncome": "其中:投资管理业务收入",
    "ofWhichOtherAgencyIncome": "其中:其他代理业务收入",
    "ofWhichCommissionExpense": "其中:手续费及佣金支出",
    "ofWhichBrokerageExpense": "其中:经纪业务手续费支出",
    "ofWhichInvestBankExpense": "其中:投资银行业务手续费支出",
    "ofWhichAssetManageExpense": "其中:资产管理业务手续费支出",
    "ofWhichfundManageExpense": "其中:基金管理业务手续费支出",
    "ofWhichInvestConsultExpense": "其中:投资咨询业务支出",
    "ofWhichRiskManageExpense": "其中:风险管理业务支出",
    "ofWhichInvestManageExpense": "其中:投资管理业务支出",
    "ofWhichOtherAgencyExpense": "其中:其他代理业务支出",
    "ofWhichNetProxySecuritiesIncome": "其中:代理买卖证券业务净收入",
    "ofWhichNetUnderwritingSecuritiesIncome": "其中:证券承销业务净收入",
    "ofWhichNetTrustIncome": "其中:受托客户资产管理业务净收入",
    "ofWhichNetfundManagementIncome": "其中:基金管理业务手续费净收入",
    "otherOperatingRevenue": "其他收入",
    "specialItemsEffectingOperatingIncome": "营业收入特殊项目",
    "adjustmentItemsEffectingOperatingIncome": "营业收入调整项目",
    "totalOperatingCost": "二、营业总成本",
    "operatingPayout": "营业支出",
    "insuranceCommissionExpense": "保险手续费及佣金支出",
    "refundedPremiums": "退保金",
    "provisionForInsuranceReserve": "提取保费准备金",
    "provisionForFuturesRiskReserve": "提取期货风险准备金",
    "provisionForGuaranteeBusinessReserve": "提取担保业务准备金",
    "provisionForGuaranteeCompensationReserve": "提取担保赔偿准备金",
    "netClaimIncurred": "赔付支出净额",
    "ofWhichGrossClaimsPaid": "其中:赔付支出",
    "ofWhichLessReinsuranceRecoveriesOnClaims": "其中:减:摊回赔付支出",
    "netProvisionForInsuranceLiabilities": "提取保险责任准备金净额",
    "ofWhichProvisionForInsuranceLiabilities": "其中:提取保险责任准备金",
    "ofWhichLessReinsuranceRecoveriesOnReserves": "其中:减:摊回保险责任准备金",
    "policyDividendPayout": "保单红利支出",
    "insuranceServiceExpense": "保险服务费用",
    "reinsuranceCostAllocation": "分出保费的分摊",
    "lessReinsuranceRecoveriesOnServiceExpense": "减:摊回保险服务费用",
    "underwritingFinancialLoss": "承保财务损失",
    "lessCededReinsuranceFinancialIncome": "减:分出再保险财务收益",
    "reinsuranceCommissionExpense": "分保费用",
    "otherOperatingCost": "其他成本",
    "operatingCost": "营业成本",
    "ofWhichSalesCost": "其中:主营业务成本",
    "ofWhichOtherOperationalCost": "其中:其他业务成本",
    "operatingTaxAndSurcharges": "营业税金及附加",
    "salesExpense": "销售费用",
    "totalAdministrativeExpense": "管理费用合计",
    "ofWhichAdministrativeExpense": "其中:管理费用",
    "ofWhichOperatingAndAdminExpense": "其中:业务及管理费",
    "ofWhichLessAmortizedReinsuranceCost": "其中:减:摊回分保费用",
    "researchAndDevelopmentExpense": "研发费用",
    "financialExpense": "财务费用",
    "ofWhichFinancialInterestExpense": "其中:利息费用(财务费用)",
    "ofWhichFinancialInterestIncome": "其中:利息收入(财务费用)",
    "explorationCost": "勘探费用",
    "creditImpairmentLossCost": "信用减值损失(成本)",
    "assetImpairmentLossCost": "资产减值损失(成本)",
    "specialItemsEffectingOperatingCost": "营业成本特殊项目",
    "adjustmentItemsEffectingOperatingCost": "营业成本调整项目",
    "nonOperatingNetIncome": "三、非经营性净收益",
    "otherNonOperatingIncome": "其他收益",
    "investmentIncome": "投资净收益",
    "ofWhichInvestmentIncomeAssociates": "其中:对联营合营企业的投资收益",
    "ofWhichGainOnDerecognitionOfAmortizedCostAssets": "其中:以摊余成本计量的金融资产终止确认收益",
    "exchangeGain": "汇兑收益",
    "netOpenHedgeGain": "净敞口套期收益",
    "fairValueChangeGain": "公允价值变动净收益",
    "creditImpairmentLossProfit": "信用减值损失(利润)",
    "assetImpairmentLossProfit": "资产减值损失(利润)",
    "gainOnAssetDisposal": "资产处置收益",
    "specialItemsEffectingOperatingProfit": "营业利润特殊项目",
    "adjustedItemsEffectingOperatingProfit": "营业利润调整项目",
    "operatingProfit": "四、营业利润",
    "addNonoperatingIncome": "加:营业外收入",
    "lessNonoperatingExpense": "减:营业外支出",
    "ofWhichNetLossOnDisposalOfNonCurrentAssets": "其中:非流动资产处置净损失",
    "specialItemsEffectingTotalProfit": "利润总额特殊项目",
    "adjustedItemsEffectingTotalProfit": "利润总额调整项目",
    "totalProfit": "五、利润总额",
    "lessIncomeTaxExpense": "减:所得税费用",
    "addUnrecognizedInvestmentLoss": "加:未确认的投资损失",
    "specialItemsEffectingNetProfit": "净利润特殊项目",
    "adjustedItemsEffectingNetProfit": "净利润调整项目",
    "netProfit": "六、净利润",
    "byContinuingOperations": "(一)按经营持续性分类",
    "profitFromContinuingOperations": "持续经营净利润",
    "profitFromDiscontinuedOperations": "终止经营净利润",
    "byOwnership": "(二)按所有权归属分类",
    "netProfitAttributableToOwnersOfParent": "归属于母公司所有者的净利润",
    "ofWhichNetProfitAttributableToOrdinaryShareholders": "其中:归属于母公司普通股股东的净利润",
    "ofWhichNetProfitAttributableToOtherEquityInstrumentHolders": "其中:归属于母公司其他权益工具持有者的净利润",
    "netProfitAttributableToNoncontrollingInterests": "少数股东损益",
    "specialItemsEffectingNetProfitParent": "母公司净利润特殊项目",
    "adjustedItemsEffectingNetProfitParent": "母公司净利润调整项目",
    "otherComprehensiveIncome": "七、其他综合收益的税后净额",
    "ociParentCompanyOwners": "归属于母公司所有者的其他综合收益的税后净额",
    "ociNotReclassifiableToProfitOrLoss": "(一)以后不能重分类进损益的其他综合收益",
    "remeasurementOfDefinedBenefitPlans": "1.1重新计量设定受益计划净负债或净资产的变动",
    "shareOfOCIOfInvesteesNotReclassifiable": "1.2权益法下在被投资单位不能重分类进损益的其他综合收益",
    "fairValueChangeOfOtherEquityInstruments": "1.3其他权益工具投资公允价值变动",
    "ownCreditRiskFairValueChange": "1.4企业自身信用风险公允价值变动",
    "financialVariableInInsuranceContractNotReclassifiable": "1.5不能转损益的保险合同金融变动",
    "ociReclassifiableToProfitOrLoss": "(二)以后将重分类进损益的其他综合收益",
    "shareOfOCIOfInvesteesReclassifiable": "2.1权益法下在被投资单位以后将重分类进损益的其他综合收益",
    "fairValueChangeOfOtherDebtInvestments": "2.2其他债权投资公允价值变动",
    "reclassificationOfFinancialAssetsToOCI": "2.3金融资产重分类计入其他综合收益的金额",
    "creditImpairmentOnOtherDebtInvestments": "2.4其他债权投资信用减值准备",
    "effectivePortionOfCashFlowHedges": "2.5现金流量套期损益的有效部分",
    "foreignCurrencyTranslationDifference": "2.6外币财务报表折算差额",
    "fairValueGainLossOnAvailableForSaleFinancialAssets": "2.7可供出售金融资产公允价值变动损益",
    "reclassificationOfHeldToMaturityToAFS": "2.8持有至到期投资重分类为可供出售金融资产损益",
    "financialVariableInInsuranceContractReclassifiable": "2.9可转损益的保险合同金融变动",
    "financialVariableInReinsuranceContractReclassifiable": "3.0可转损益的分出再保险合同金融变动",
    "otherReclassifiableOCI": "3.1其他(以后能重分类进损益表的其他综合收益)",
    "ociAttributableToNoncontrollingInterests": "归属于少数股东的其他综合收益的税后净额",
    "adjustedItemsEffectingOtherComprehensiveIncome": "综合收益总额调整项目",
    "specialItemsEffectingOtherComprehensiveIncome": "综合收益总额特殊项目",
    "totalComprehensiveIncome": "八、综合收益总额",
    "comprehensiveIncomeAttributableToOwnersOfParent": "归属于母公司所有者的综合收益总额",
    "ofWhichComprehensiveIncomeAttributableToOrdinaryShareholders": "其中:归属于母公司普通股股东的综合收益",
    "ofWhichComprehensiveIncomeAttributableToOtherEquityInstrumentHolders": "其中:归属于母公司其他权益工具持有者的综合收益",
    "comprehensiveIncomeAttributableToNoncontrollingInterests": "归属于少数股东的综合收益总额",
    "adjustedItemsEffectingComprehensiveIncomeParent": "母公司综合收益总额调整项目",
    "basicEarningsPerShare": "基本每股收益",
    "dilutedEarningsPerShare": "稀释每股收益",
    "totalOpRev": "一、营业总收入",
    "opRev": "营业收入",
    "salesRev": "其中：主营业务收入",
    "otherOpRev": "其中：其他业务收入",
    "netIntIncome": "利息净收入",
    "intIncome": "其中：利息收入",
    "intExp": "其中：利息支出",
    "premEarned": "已赚保费",
    "premIncome": "其中：保险业务收入",
    "reinsIncome": "其中：保险业务收入：分保费收入",
    "lessReins": "其中：减：分出保费",
    "lessUnearnedPremRes": "其中：减：提取未到期责任准备金",
    "guaranteeIncome": "担保业务收入",
    "netCommIncome": "手续费及佣金净收入",
    "commIncome": "其中：手续费及佣金收入",
    "brokerageIncome": "其中：经纪业务手续费收入",
    "invBankIncome": "其中：投资银行业务手续费收入",
    "assetMgmtIncome": "其中：资产管理业务手续费收入",
    "fundMgmtIncome": "其中：基金管理业务手续费收入",
    "invConsultIncome": "其中：投资咨询业务收入",
    "riskMgmtIncome": "其中：风险管理业务收入",
    "invMgmtIncome": "其中：投资管理业务收入",
    "otherAgencyIncome": "其中：其他代理业务收入",
    "commExp": "其中：手续费及佣金支出",
    "brokerageExp": "其中：经纪业务手续费支出",
    "invBankExp": "其中：投资银行业务手续费支出",
    "assetMgmtExp": "其中：资产管理业务手续费支出",
    "fundMgmtExp": "其中：基金管理业务手续费支出",
    "invConsultExp": "其中：投资咨询业务支出",
    "riskMgmtExp": "其中：风险管理业务支出",
    "invMgmtExp": "其中：投资管理业务支出",
    "otherAgencyExp": "其中：其他代理业务支出",
    "netProxySecIncome": "其中：代理买卖证券业务净收入",
    "netUnderSecIncome": "其中：证券承销业务净收入",
    "netTrustIncome": "其中：受托客户资产管理业务净收入",
    "netFundMgmtIncome": "其中：基金管理业务手续费净收入",
    "otherOpRev2": "其他收入",
    "specialItemsOpRev": "营业收入特殊项目",
    "adjItemsOpRev": "营业收入调整项目",
    "totalOpCost": "二、营业总成本",
    "opPayout": "营业支出",
    "insCommExp": "保险手续费及佣金支出",
    "refundPrem": "退保金",
    "provInsRes": "提取保费准备金",
    "provFutRiskRes": "提取期货风险准备金",
    "provGuaranteeBizRes": "提取担保业务准备金",
    "provGuaranteeCompRes": "提取担保赔偿准备金",
    "netClaims": "赔付支出净额",
    "grossClaimsPaid": "其中：赔付支出",
    "lessReinsRecovClaims": "其中：减：摊回赔付支出",
    "netProvInsLiab": "提取保险责任准备金净额",
    "provInsLiab": "其中：提取保险责任准备金",
    "lessReinsRecovRes": "其中：减：摊回保险责任准备金",
    "policyDivPayout": "保单红利支出",
    "insServiceExp": "保险服务费用",
    "reinsCostAlloc": "分出保费的分摊",
    "lessReinsRecovServiceExp": "减：摊回保险服务费用",
    "underwritingFinLoss": "承保财务损失",
    "lessCededReinsFinInc": "减：分出再保险财务收益",
    "reinsCommExp": "分保费用",
    "otherOpCost": "其他成本",
    "opCost": "营业成本",
    "salesCost": "其中：主营业务成本",
    "otherOpCost2": "其中：其他业务成本",
    "opTaxSurcharges": "营业税金及附加",
    "salesExp": "销售费用",
    "totalAdminExp": "管理费用合计",
    "adminExp": "其中：管理费用",
    "opAdminExp": "其中：业务及管理费",
    "lessAmortReinsCost": "其中：减：摊回分保费用",
    "rdExp": "研发费用",
    "finExp": "财务费用",
    "finIntExp": "其中：利息费用（财务费用）",
    "finIntIncome": "其中：利息收入（财务费用）",
    "explorationCost": "勘探费用",
    "creditImpairLossCost": "信用减值损失（成本）",
    "assetImpairLossCost": "资产减值损失（成本）",
    "specialItemsOpCost": "营业成本特殊项目",
    "adjItemsOpCost": "营业成本调整项目",
    "nonOpNetIncome": "三、非经营性净收益",
    "otherNonOpIncome": "其他收益",
    "invIncome": "投资净收益",
    "invIncomeAssoc": "其中：对联营合营企业的投资收益",
    "gainDerecogAmortCost": "其中：以摊余成本计量的金融资产终止确认收益",
    "fxGain": "汇兑收益",
    "netOpenHedgeGain": "净敞口套期收益",
    "fvChangeGain": "公允价值变动净收益",
    "creditImpairLossProfit": "信用减值损失（利润）",
    "assetImpairLossProfit": "资产减值损失（利润）",
    "gainAssetDisposal": "资产处置收益",
    "specialItemsOpProfit": "营业利润特殊项目",
    "adjItemsOpProfit": "营业利润调整项目",
    "opProfit": "四、营业利润",
    "addNonopIncome": "加：营业外收入",
    "lessNonopExp": "减：营业外支出",
    "netLossDispNonCurrAssets": "其中：非流动资产处置净损失",
    "specialItemsTotalProfit": "利润总额特殊项目",
    "adjItemsTotalProfit": "利润总额调整项目",
    "totalProfit": "五、利润总额",
    "lessIncTaxExp": "减：所得税费用",
    "addUnrecogInvLoss": "加：未确认的投资损失",
    "specialItemsNetProfit": "净利润特殊项目",
    "adjItemsNP": "净利润调整项目",
    "netProfit": "六、净利润",
    "byContOps": "（一）按经营持续性分类",
    "profitContOps": "持续经营净利润",
    "profitDiscOps": "终止经营净利润",
    "byOwnership": "（二）按所有权归属分类",
    "netProfitAttrParent": "归属于母公司所有者的净利润",
    "netProfitAttrOrdShare": "其中：归属于母公司普通股股东的净利润",
    "netProfitAttrOtherEq": "其中：归属于母公司其他权益工具持有者的净利润",
    "netProfitAttrNoncontrol": "少数股东损益",
    "specialItemsNetProfitParent": "母公司净利润特殊项目",
    "adjItemsNetProfitParent": "母公司净利润调整项目",
    "otherCompIncome": "七、其他综合收益的税后净额",
    "OCIParentOwners": "归属于母公司所有者的其他综合收益的税后净额",
    "OCINotReclassToPL": "（一）以后不能重分类进损益的其他综合收益",
    "remeasureDefBenefit": "1.1 重新计量设定受益计划净负债或净资产的变动",
    "shareOCINotReclass": "1.2 权益法下在被投资单位不能重分类进损益的其他综合收益",
    "fvChangeOtherEqInstr": "1.3 其他权益工具投资公允价值变动",
    "ownCreditRiskFvChange": "1.4 企业自身信用风险公允价值变动",
    "finVarInsContrNotReclass": "1.5 不能转损益的保险合同金融变动",
    "OCIReclassToPL": "（二）以后将重分类进损益的其他综合收益",
    "shareOCIReclass": "2.1 权益法下在被投资单位以后将重分类进损益的其他综合收益",
    "fvChangeOtherDebtInv": "2.2 其他债权投资公允价值变动",
    "reclassFinAssetsToOCI": "2.3 金融资产重分类计入其他综合收益的金额",
    "creditImpairOtherDebtInv": "2.4 其他债权投资信用减值准备",
    "effectivePartCashFlowHedge": "2.5 现金流量套期损益的有效部分",
    "fxTransDiff": "2.6 外币财务报表折算差额",
    "fvGainLossAFS": "2.7 可供出售金融资产公允价值变动损益",
    "reclassHTMtoAFS": "2.8 持有至到期投资重分类为可供出售金融资产损益",
    "finVarInsContrReclass": "2.9 可转损益的保险合同金融变动",
    "finVarReinsContrReclass": "3.0 可转损益的分出再保险合同金融变动",
    "otherReclassOCI": "3.1 其他（以后能重分类进损益表的其他综合收益）",
    "OCIAttrNoncontrol": "归属于少数股东的其他综合收益的税后净额",
    "adjItemsOtherCompIncome": "综合收益总额调整项目",
    "specialItemsOtherCompIncome": "综合收益总额特殊项目",
    "totalCompIncome": "八、综合收益总额",
    "compIncomeAttrParent": "归属于母公司所有者的综合收益总额",
    "compIncomeAttrOrdShare": "其中：归属于母公司普通股股东的综合收益",
    "compIncomeAttrOtherEq": "其中：归属于母公司其他权益工具持有者的综合收益",
    "compIncomeAttrNoncontrol": "归属于少数股东的综合收益总额",
    "adjItemsCompIncParent": "母公司综合收益总额调整项目",
    "basicEPS": "基本每股收益",
    "dilutedEPS": "稀释每股收益",
}

BALANCE_FIELD_CN = {
    "securityCode": "证券代码",
    "companyName": "证券简称",
    "endDate": "财报截止日期",
    "fiscalYear": "财报年",
    "period": "报告期",
    "reportType": "报表类型",
    "companyType": "企业报表格式",
    "currency": "币种",
    "unit": "单位",
    "currAssets": "流动资产",
    "monetaryAssets": "货币资金/现金及存放中央银行款项",
    "cash": "其中：货币资金",
    "clientDeposit": "其中：客户资金存款",
    "depositCentralBank": "其中：现金及存放中央银行款项",
    "settleReserve": "结算备付金",
    "clientFundReserve": "其中：客户备付金",
    "fundsLent": "拆出资金",
    "fundsForFinancing": "融出资金",
    "depositInterbank": "存放同业款项",
    "depositAssoc": "存放联行款项",
    "preciousMetals": "贵金属",
    "tradingAssets": "交易性金融资产合计",
    "tradingFinAssets": "其中：交易性金融资产",
    "finAssetsFVTPL": "其中：以公允价值计量且其变动计入当期损益的金融资产",
    "derivAssets": "衍生金融资产",
    "marginDeposited": "存出保证金",
    "notesAcctsRecv": "应收票据及应收账款",
    "notesReceivable": "其中：应收票据",
    "acctsReceivable": "其中：应收账款",
    "recvFinancing": "应收款项融资",
    "advPay": "预付款项",
    "insReceivables": "应收保费",
    "recvSubrogation": "应收代位追偿款",
    "reinsReceivables": "应收分保账款",
    "recvReinsReserves": "应收分保合同准备金",
    "recvReinsUnearnedRes": "其中：应收分保未到期责任准备金",
    "recvReinsClaimsRes": "其中：应收分保未决赔款准备金",
    "recvReinsLifeRes": "其中：应收分保寿险责任准备金",
    "recvReinsHealthRes": "其中：应收分保长期健康险责任准备金",
    "otherRecvIncIntDiv": "其他应收款（含利息和股利）",
    "otherReceivable": "其中：其他应收款",
    "dividendReceivable": "其中：应收股利",
    "interestReceivable": "其中：应收利息",
    "finLeaseRecv": "应收融资租赁款",
    "receivables": "应收款项",
    "cashMarginRecv": "应收货币保证金",
    "pledgeMarginRecv": "应收质押保证金",
    "settleGuaranteeRecv": "应收结算担保金",
    "riskLossRecv": "应收风险损失款",
    "feesCommRecv": "应收手续费及佣金",
    "reverseRepoAssets": "买入返售金融资产",
    "inventory": "存货",
    "consumableBioAssets": "其中：消耗性生物资产",
    "dataResourceInv": "其中：数据资源（存货）",
    "contractAssets": "合同资产",
    "insContractAssets": "保险合同资产",
    "reinsContractAssets": "分出再保险合同资产",
    "assetsHeldForSale": "持有待售资产",
    "agencyAssets": "代理业务资产",
    "prepayDeferredExp": "待摊费用",
    "policyholderPledgeLoan": "保户质押贷款",
    "nonCurrAssetsDue1Yr": "一年内到期的非流动资产",
    "otherCurrAssets": "其他流动资产",
    "specItemsCurrAssets": "流动资产特殊项目",
    "adjItemsCurrAssets": "流动资产调整项目",
    "totalCurrAssets": "流动资产合计",
    "nonCurrAssets": "非流动资产",
    "loansAdvances": "发放贷款和垫款",
    "totalDebtInv": "债权投资合计",
    "debtInvestments": "其中：债权投资",
    "finAssetsAmortCost": "其中：以摊余成本计量的金融资产",
    "totalOtherDebtInv": "其他债权投资合计",
    "otherDebtInvestments": "其中：其他债权投资",
    "finInvFVOCI": "其中：以公允价值计量且其变动计入其他综合收益的金融投资",
    "invLoansRecv": "投资-贷款及应收款项（应收款项类投资）",
    "timeDep": "定期存款",
    "totalOtherEquityInv": "其他权益工具投资合计",
    "otherEquityInv": "其中：其他权益工具投资",
    "nonTradeEquityFVOCI": "其中：以公允价值计量且其变动计入其他综合收益的非交易性权益工具投资",
    "finAssetsFVOCI": "以公允价值计量且其变动计入其他综合收益的金融资产",
    "htmInvestments": "持有至到期投资",
    "afsFinAssets": "可供出售金融资产",
    "otherNonCurrFinAssets": "其他非流动金融资产",
    "entrustedLoans": "委托贷款",
    "ltReceivables": "长期应收款",
    "ltEquityInvest": "长期股权投资",
    "capitalMarginDep": "存出资本保证金",
    "investmentProp": "投资性房地产",
    "totalPPE": "固定资产合计",
    "ppe": "其中：固定资产",
    "ppeDisposal": "其中：固定资产清理",
    "totalCIP": "在建工程合计",
    "cip": "其中：在建工程",
    "constrMaterials": "其中：工程物资",
    "prodBioAssets": "生产性生物资产",
    "pubWelfareBioAssets": "公益性生物资产",
    "oilGasAssets": "油气资产",
    "rouAssets": "使用权资产",
    "intangAssets": "无形资产",
    "tradingSeatFee": "其中：交易席位费",
    "dataResourceIntang": "其中：数据资源（无形资产）",
    "devExp": "开发支出",
    "dataResourceDevExp": "其中：数据资源（开发支出）",
    "goodwill": "商誉",
    "ltDeferredExp": "长期待摊费用",
    "sepAcctAssets": "独立账户资产",
    "deferredTaxAssets": "递延所得税资产",
    "assetsInLieu": "抵债资产",
    "futuresMembershipInv": "期货会员资格投资",
    "otherNonCurrAssets": "其他非流动资产",
    "specItemsNonCurrAssets": "非流动资产特殊项目",
    "adjItemsNonCurrAssets": "非流动资产调整项目",
    "totalNonCurrAssets": "非流动资产合计",
    "otherAssets": "其他资产",
    "finInvestments": "金融投资",
    "otherAssetsMisc": "其他资产",
    "specItemsAssets": "资产特殊项目",
    "adjItemsAssets": "资产调整项目",
    "totalAssets": "资产总计",
    "currLiab": "流动负债",
    "stBorrowings": "短期借款",
    "pledgedBorrowings": "其中：质押借款",
    "stFinancingPay": "应付短期融资款",
    "stBondsPay": "应付短期债券",
    "borrowCentralBank": "向中央银行借款",
    "fundsBorrowed": "拆入资金",
    "totalTradingFinLiab": "交易性金融负债合计",
    "tradingFinLiab": "其中：交易性金融负债",
    "finLiabFVTPL": "其中：以公允价值计量且其变动计入当期损益的金融负债",
    "derivFinLiab": "衍生金融负债",
    "notesAcctsPay": "应付票据及应付账款",
    "notesPayable": "其中：应付票据",
    "acctsPayable": "其中：应付账款",
    "advFromCust": "预收款项",
    "unearnedPremRes": "预收保费",
    "contractLiab": "合同负债",
    "insContractLiab": "保险合同负债",
    "reinsCededLiab": "分出再保险合同负债",
    "repoLiab": "卖出回购金融资产款",
    "depInterbankDep": "吸收存款及同业存款",
    "custDeposits": "其中：吸收存款",
    "interbankDep": "其中：同业及其他金融机构存放款项",
    "dueToAffiliates": "联行存放款项",
    "clientBrokeragePay": "代理买卖证券款",
    "underwritingSecPay": "代理承销证券款",
    "empBenefitsPay": "应付职工薪酬",
    "taxPayable": "应交税费",
    "otherPayIncIntDiv": "其他应付款（含利息和股利）",
    "otherPayable": "其中：其他应付款",
    "dividendPayable": "其中：应付股利",
    "interestPayable": "其中：应付利息",
    "payables": "应付款项",
    "feesCommPay": "应付手续费及佣金",
    "cashMarginPay": "应付货币保证金",
    "pledgeMarginPay": "应付质押保证金",
    "futuresInvestorFundPay": "应付期货投资者保障基金",
    "reinsPayable": "应付分保账款",
    "agencyLiab": "代理业务负债",
    "liabHeldForSale": "持有待售负债",
    "claimsPay": "应付赔付款",
    "policyholderDivPay": "应付保单红利",
    "policyholderDepInvFund": "保户储金及投资款",
    "insContractReserves": "保险合同准备金",
    "marginReceived": "存入保证金",
    "accruedExp": "预提费用",
    "deferredIncome": "递延收益",
    "guarCompensReserve": "担保赔偿准备金",
    "guarBusinessReserve": "担保业务准备金",
    "futuresRiskReserve": "期货风险准备金",
    "nonCurrLiabDue1Yr": "一年内到期的非流动负债",
    "otherCurrLiab": "其他流动负债",
    "specItemsCurrLiab": "流动负债特殊项目",
    "adjItemsCurrLiab": "流动负债调整项目",
    "totalCurrLiab": "流动负债合计",
    "nonCurrLiab": "非流动负债",
    "ltInsContractReserves": "长期保险合同准备金",
    "unearnedPremResLt": "其中：未到期责任准备金",
    "outstandingClaimsRes": "其中：未决赔款准备金",
    "lifeInsLiabRes": "其中：寿险责任准备金",
    "ltHealthRes": "其中：长期健康险责任准备金",
    "ltBorrowings": "长期借款",
    "bondsPay": "应付债券",
    "prefSharesBonds": "其中：优先股（应付债券）",
    "perpetualBonds": "其中：永续债（应付债券）",
    "leaseLiab": "租赁负债",
    "totalLtPayables": "长期应付款合计",
    "ltPayables": "其中：长期应付款",
    "specificPayables": "其中：专项应付款",
    "finLeasePay": "应付融资租赁款",
    "ltEmpBenefitsPay": "长期应付职工薪酬",
    "provisions": "预计负债",
    "ltDeferredIncome": "长期递延收益",
    "sepAcctLiab": "独立账户负债",
    "deferredTaxLiab": "递延所得税负债",
    "otherNonCurrLiab": "其他非流动负债",
    "specItemsNonCurrLiab": "非流动负债特殊项目",
    "adjItemsNonCurrLiab": "非流动负债调整项目",
    "totalNonCurrLiab": "非流动负债合计",
    "otherLiab": "其他负债",
    "otherLiabMisc": "其他负债",
    "specItemsLiab": "负债特殊项目",
    "adjItemsLiab": "负债调整项目",
    "totalLiab": "负债合计",
    "equity": "所有者权益（或股东权益）",
    "shareCapital": "实收资本（或股本）",
    "otherEquityInstr": "其他权益工具",
    "prefSharesEquity": "其中：优先股（其他权益工具）",
    "perpetualBondsEquity": "其中：永续债（其他权益工具）",
    "capReserve": "资本公积",
    "lessTreasuryShares": "减：库存股",
    "specReserve": "专项储备",
    "oci": "其他综合收益",
    "surplusReserve": "盈余公积",
    "genRiskProv": "一般风险准备",
    "tradingRiskProv": "交易风险准备",
    "otherReserves": "其他储备（公允价值变动储备）",
    "retainedEarn": "未分配利润",
    "fxTransDiff": "外币报表折算差额",
    "unrecogInvLoss": "未确认投资损失",
    "specItemsParentEq": "归属母公司所有者权益特殊项目",
    "adjItemsParentEq": "归属母公司所有者权益调整项目",
    "totalParentEq": "归属母公司所有者权益合计",
    "parentOrdinaryEq": "其中：归属于母公司普通股股东权益",
    "nonControllingInterests": "少数股东权益",
    "specItemsTotalEq": "所有者权益特殊项目",
    "adjItemsTotalEq": "所有者权益调整项目",
    "totalEquity": "所有者权益（或股东权益）合计",
    "liabAndEquity": "负债和所有者权益",
    "specItemsLAndE": "负债和权益特殊项目",
    "adjItemsLAndE": "负债和权益调整项目",
    "totalLAndE": "负债和所有者权益（或股东权益）总计",
}

CASH_FLOW_FIELD_CN = {
    "securityCode": "证券代码",
    "companyName": "证券简称",
    "endDate": "财报截止日期",
    "fiscalYear": "财报年",
    "period": "报告期",
    "reportType": "报表类型",
    "companyType": "企业报表格式",
    "currency": "币种",
    "unit": "单位",
    "cashFromSales": "销售商品、提供劳务收到的现金",
    "netIncCustDeposits": "客户存款和同业存放款项净增加额",
    "netIncBorrowFromCentralBank": "向中央银行借款净增加额",
    "netIncBorrowFromOtherFinInst": "向其他金融机构拆入资金净增加额",
    "netDecCustomerLoans": "客户贷款及垫款净减少额",
    "netDecDepositsCentralBank": "存放中央银行和同业款项净减少额",
    "cashFromInsurancePremiums": "收到原保险合同保费取得的现金",
    "netCashFromReinsurance": "收到再保业务现金净额",
    "netIncPolicyholderDeposits": "保户储金及投资款净增加额",
    "netIncBorrowedFunds": "拆入资金净增加额",
    "netDecLoanedFunds": "拆出资金净减少额",
    "netDecReverseRepoFundsOp": "返售业务资金净减少额（经营）",
    "netIncRepoFunds": "回购业务资金净增加额",
    "netCashFromAgencyTrading": "代理买卖证券收到的现金净额",
    "netCashFromAgencyUnderwriting": "代理承销证券收到的现金净额",
    "netIncDisposalFVTOCI": "处置交易性金融资产净增加额",
    "netDecTradingFinancialAssets": "为交易目的而持有的金融资产净减少额",
    "netIncTradingFinancialLiabs": "为交易目的而持有的金融负债净增加额",
    "cashFromInterestFeesComms": "收取利息、手续费及佣金的现金",
    "refundOfTaxes": "收到的税费返还",
    "recoveryOfWrittenOffLoans": "收回已核销贷款",
    "netDecLentFunds": "融出资金净减少额",
    "cashFromOtherOps": "收到其他与经营活动有关的现金",
    "specItemsOpInflows": "经营活动现金流入特殊项目",
    "adjItemsOpInflows": "经营活动现金流入调整项目",
    "subtotalOpInflows": "经营活动现金流入小计",
    "cashPaidForGoodsServices": "购买商品、接受劳务支付的现金",
    "netDecCustDeposits": "客户存款和同业存放款项净减少额",
    "netDecBorrowFromCentralBank": "向中央银行借款净减少额",
    "netDecBorrowFromOtherFinInst": "向其他金融机构拆入资金净减少额",
    "netIncCustomerLoans": "客户贷款及垫款净增加额",
    "netIncDepositsCentralBank": "存放中央银行和同业款项净增加额",
    "cashPaidInsuranceClaims": "支付原保险合同赔付款项的现金",
    "cashPaidPolicyDividends": "支付保单红利的现金",
    "netCashPaidReinsurance": "支付再保业务现金净额",
    "netIncPolicyLoans": "保单质押贷款净增加额",
    "netDecPolicyholderDeposits": "保户储金及投资款净减少额",
    "netDecBorrowedFunds": "拆入资金净减少额",
    "netIncLoanedFunds": "拆出资金净增加额",
    "netIncReverseRepoFundsOp": "返售业务资金净增加额（经营）",
    "netDecRepoFunds": "回购业务资金净减少额",
    "netCashPaidAgencyTrading": "代理买卖证券支付的现金净额",
    "netCashPaidAgencyUnderwriting": "代理承销证券支付的现金净额",
    "netDecDisposalFVTOCI": "处置交易性金融资产净减少额",
    "netIncTradingFinancialAssets": "为交易目的而持有的金融资产净增加额",
    "netDecTradingFinancialLiabs": "为交易目的而持有的金融负债净减少额",
    "cashPaidInterestFeesComms": "支付利息、手续费及佣金的现金",
    "cashPaidEmployees": "支付给职工以及为职工支付的现金",
    "cashPaidTaxes": "支付的各项税费",
    "businessAdminExpensesPaid": "以现金支付的业务及管理费",
    "netIncLentFunds": "融出资金净增加额",
    "cashPaidOtherOps": "支付其他与经营活动有关的现金",
    "specItemsOpOutflows": "经营活动现金流出特殊项目",
    "adjItemsOpOutflows": "经营活动现金流出调整项目",
    "subtotalOpOutflows": "经营活动现金流出小计",
    "adjItemsNetOpCashFlows": "经营活动现金流量净额调整项目",
    "netOpCashFlows": "经营活动产生的现金流量净额",
    "opCashFlows": "一、经营活动产生的现金流量",
    "invCashFlows": "二、投资活动产生的现金流量",
    "cashRecoveredInvestments": "收回投资收到的现金",
    "cashFromReturnsInvestments": "取得投资收益收到的现金",
    "netCashDisposalAssets": "处置固定资产、无形资产和其他长期资产收回的现金净额",
    "netCashDisposalSubsidiaries": "处置子公司及其他营业单位收到的现金净额",
    "cashFromOtherInv": "收到其他与投资活动有关的现金",
    "specItemsInvInflows": "投资活动现金流入特殊项目",
    "adjItemsInvInflows": "投资活动现金流入调整项目",
    "subtotalInvInflows": "投资活动现金流入小计",
    "cashPaidAcqConstructAssets": "购建固定资产、无形资产和其他长期资产支付的现金",
    "cashPaidInvestments": "投资支付的现金",
    "netIncSecuredLoans": "质押贷款净增加额",
    "netCashPaidAcqSubsidiaries": "取得子公司及其他营业单位支付的现金净额",
    "netIncReverseRepoFundsInv": "返售业务资金净增加额（投资）",
    "cashPaidOtherInv": "支付其他与投资活动有关的现金",
    "specItemsInvOutflows": "投资活动现金流出特殊项目",
    "adjItemsInvOutflows": "投资活动现金流出调整项目",
    "subtotalInvOutflows": "投资活动现金流出小计",
    "adjItemsNetInvCashFlows": "投资活动现金流量净额调整项目",
    "netInvCashFlows": "投资活动产生的现金流量净额",
    "finCashFlows": "三、筹资活动产生的现金流量",
    "cashFromCapitalContributions": "吸收投资收到的现金",
    "cashFromMinorityShareholders": "其中：子公司吸收少数股东投资收到的现金",
    "cashFromBorrowings": "取得借款收到的现金",
    "cashFromBondsIssuance": "发行债券收到的现金",
    "cashFromOtherEquityInstruments": "发行其他权益工具收到的现金",
    "netIncRepoFundsFin": "回购业务资金净增加额（筹资）",
    "cashFromOtherFin": "收到其他与筹资活动有关的现金",
    "specItemsFinInflows": "筹资活动现金流入特殊项目",
    "adjItemsFinInflows": "筹资活动现金流入调整项目",
    "subtotalFinInflows": "筹资活动现金流入小计",
    "cashPaidDebtRepayment": "偿还债务支付的现金",
    "cashPaidDividendsInterest": "分配股利、利润或偿付利息支付的现金",
    "cashPaidToMinorityShareholders": "其中：子公司支付给少数股东的股利、利润或偿付的利息",
    "netDecRepoFundsFin": "回购业务资金净减少额（筹资）",
    "cashPaidOtherFin": "支付其他与筹资活动有关的现金",
    "specItemsFinOutflows": "筹资活动现金流出特殊项目",
    "adjItemsFinOutflows": "筹资活动现金流出调整项目",
    "subtotalFinOutflows": "筹资活动现金流出小计",
    "adjItemsNetFinCashFlows": "筹资活动现金流量净额调整项目",
    "netFinCashFlows": "筹资活动产生的现金流量净额",
    "cashEquivalents": "四、现金及现金等价物",
    "fxEffectOnCash": "汇率变动对现金及现金等价物的影响",
    "otherAccEffectCash": "影响现金及现金等价物的其他科目",
    "adjItemsEffectCash": "影响现金及现金等价物的调整项目",
    "cashEquivalentsIncrease": "五、现金及现金等价物净增加额",
    "netIncCashEquivalents": "现金及现金等价物净增加额",
    "addOpeningCashBalance": "加：期初现金及现金等价物余额",
    "specItemsNetIncCash": "现金及现金等价物净增加额的特殊项目",
    "adjItemsNetIncCash": "现金及现金等价物净增加额的调整项目",
    "closingCashBalance": "期末现金及现金等价物余额",
    "reconciliationToOpCashFlows": "1. 将净利润调节为经营活动现金流量",
    "netProfit": "净利润",
    "netProfitToParent": "其中：归属于母公司所有者的净利润",
    "profitLossToMinority": "其中：少数股东损益",
    "addAssetImpairmentLoss": "加：资产减值准备",
    "depAmortFixedAssets": "固定资产折旧、油气资产折耗、生产性生物资产等资产折旧/摊销",
    "depProductBioAssets": "其中：生产性生物资产折旧",
    "depAmortInvProperties": "投资性房地产折旧/摊销",
    "amortDepRightOfUseAssets": "使用权资产摊销/折旧",
    "amortIntangibleAssets": "无形资产摊销",
    "amortLongTermDeferredExp": "长期待摊费用摊销",
    "decreasePrepaidExp": "待摊费用减少（减：增加）",
    "increaseAccruedExp": "预提费用增加（减：减少）",
    "lossOnDisposalAssets": "处置固定资产、无形资产和其他长期资产的损失",
    "lossOnRetirementFixedAssets": "固定资产报废损失",
    "lossOnFVChanges": "公允价值变动损失",
    "financeExpenses": "财务费用",
    "interestIncome": "利息收入",
    "interestExpLeaseLiabs": "其中：租赁负债利息支出",
    "interestExpBondsIssued": "其中：发行债券利息支出",
    "exchangeGainLoss": "汇兑损失（收益以 \"-\" 号填列）",
    "interestExpense": "利息支出",
    "investmentLoss": "投资损失",
    "increaseRestrictedCash": "受限资金的增加",
    "increaseSpecialReserve": "专项储备增加",
    "creditImpairmentLoss": "信用减值损失",
    "amortDeferredIncome": "递延收益摊销",
    "increaseProvisions": "预计负债的增加（减：减少）",
    "deferredRevenueCredits": "递延税款贷项（减：借项）",
    "decreaseDeferredTaxAssets": "递延所得税资产减少",
    "increaseDeferredTaxLiabs": "递延所得税负债增加",
    "decreaseInventories": "存货的减少",
    "shareBasedPaymentExp": "股份支付费用",
    "decreaseFVTPLAssets": "交易性金融资产的减少",
    "decreaseAFSAssets": "可供出售金融资产的减少",
    "decreaseLoans": "贷款的减少",
    "decreaseOpReceivables": "经营性应收项目的减少",
    "increaseOpPayables": "经营性应付项目的增加",
    "other": "其他",
    "noteSpecItemsNetOpCashFlows": "（附注）经营活动现金流量净额特殊项目",
    "noteAdjItemsNetOpCashFlows": "（附注）经营活动现金流量净额调整项目",
    "noteNetOpCashFlows": "（附注）经营活动产生的现金流量净额",
    "addAdjItemsComparisonOpCashFlows": "加：经营流量净额前后对比调整项目",
    "nonCashInvFinActivities": "2. 不涉及现金收支的投资和筹资活动",
    "conversionDebtToCapital": "债务转为资本",
    "convBondsDueWithinOneYear": "一年内到期的可转换公司债券",
    "financeLeaseFixedAssets": "融资租入固定资产",
    "netChangeCashEquivalents": "3. 现金及现金等价物净变动情况",
    "closingBalanceCash": "现金的期末余额",
    "lessOpeningBalanceCash": "减：现金的期初余额",
    "addClosingBalanceEquivalents": "加：现金等价物的期末余额",
    "lessOpeningBalanceEquivalents": "减：现金等价物的期初余额",
    "noteSpecItemsCash": "（附注）现金特殊项目",
    "noteAdjItemsCash": "（附注）现金调整项目",
    "noteNetIncCashEquivalents": "（附注）现金及现金等价物净增加额",
    "addAdjItemsComparisonNetCash": "加：现金净额前后对比调整项目",
}

OPENAPI_SKILL_VERSION = "1.4.3"
SKILL_CHECK_URL = "https://open.gangtise.com/application/skills-backend/version?skill=openapi"

def check_version(large_version: bool = True):
    response = requests.get(SKILL_CHECK_URL)
    if response.status_code == 200 and large_version:
        return response.json()["state"] == "success" and response.json()["version"].split(".")[0] == OPENAPI_SKILL_VERSION.split(".")[0] and response.json()["version"].split(".")[1] == OPENAPI_SKILL_VERSION.split(".")[1]
    elif response.status_code == 200 and not large_version:
        return response.json()["state"] == "success" and response.json()["version"] == OPENAPI_SKILL_VERSION
    else:
        return False

if __name__ == "__main__":
    print("检查 gangtise-file 相关配置")
    if not os.path.exists(GTS_AUTHORIZATION_PATH):
        print("  无法检测到gangtise授权文件, gangtise-file 无法正常工作")
    elif GTS_AUTHORIZATION is None:
        print("  授权文件存在, 但无法获取gangtise授权, 请检查授权文件内容中是否含有 long-term-token 或者 accessKey 和 secretAccessKey, gangtise-file 无法正常工作")
    else:
        print("  检测到gangtise授权文件, gangtise-file 可以正常工作")
    if GTS_SAVE_FILE is None:
        print("  环境变量 GTS_SAVE_FILE 未配置, 默认值为 False, gangtise服务端 将不保存查询结果到文件中")
    elif GTS_SAVE_FILE == "True":
        print("  环境变量 GTS_SAVE_FILE 为 True, gangtise服务端 将保存查询结果到文件中")
    else:
        print("  环境变量 GTS_SAVE_FILE 为 False, gangtise服务端 将不保存查询结果到文件中")
    if check_version(large_version=False):
        print("  gangtise-file 版本为最新")
    else:
        print("  gangtise-file 版本不是最新, 建议进行更新")
    print(f"  gangtise-file 工作文件目录: {gangtise_workspace_path}")