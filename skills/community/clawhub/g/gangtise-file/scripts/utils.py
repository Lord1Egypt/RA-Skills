import os
import re
from typing import Dict, List, Any, Optional
# import logging
# from logging.handlers import TimedRotatingFileHandler
import pandas as pd
import datetime
import requests
import json

# 推荐使用环境变量配置 ak/sk，而不是使用文件配置（文件配置仅作为部分框架兼容性的备用方案）
# 如果同时存在，则以环境变量配置为准

GTS_ACCESS_KEY = os.getenv("GTS_ACCESS_KEY", None)
GTS_SECRET_KEY = os.getenv("GTS_SECRET_KEY", None)
GTS_AUTHORIZATION_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), ".authorization")

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

GANGTISE_DATA_DOMAIN = "https://open.gangtise.com/application/open-data"
GANGTISE_INSIGHT_DOMAIN = "https://open.gangtise.com/application/open-insight"

REPORT_URL = f"{GANGTISE_INSIGHT_DOMAIN}/broker-report/getList"
REPORT_DOWNLOAD_URL = f"{GANGTISE_INSIGHT_DOMAIN}/broker-report/download/file"

FOREIGN_REPORT_URL = f"{GANGTISE_INSIGHT_DOMAIN}/foreign-report/getList"
FOREIGN_REPORT_DOWNLOAD_URL = f"{GANGTISE_INSIGHT_DOMAIN}/foreign-report/download/file"

COMPANY_ANNOUNCEMENT_URL = f"{GANGTISE_INSIGHT_DOMAIN}/announcement/getList"
COMPANY_ANNOUNCEMENT_DOWNLOAD_URL = f"{GANGTISE_INSIGHT_DOMAIN}/announcement/download/file"

SUMMARY_URL = f"{GANGTISE_INSIGHT_DOMAIN}/summary/v2/getList"
SUMMARY_DOWNLOAD_URL = f"{GANGTISE_INSIGHT_DOMAIN}/summary/v2/download/file"

OPINION_URL = f"{GANGTISE_INSIGHT_DOMAIN}/chief-opinion/getList"

ROADSHOW_LIST_URL = f"{GANGTISE_INSIGHT_DOMAIN}/schedule/roadshow/getList"
SITE_VISIT_LIST_URL = f"{GANGTISE_INSIGHT_DOMAIN}/schedule/site-visit/getList"
STRATEGY_MEETING_LIST_URL = f"{GANGTISE_INSIGHT_DOMAIN}/schedule/strategy-meeting/getList"
FORUM_LIST_URL = f"{GANGTISE_INSIGHT_DOMAIN}/schedule/forum/getList"

FILE_URL = f"{GANGTISE_DATA_DOMAIN}/ai/resource/download"

GANGTISE_VAULT_DOMAIN = "https://open.gangtise.com/application/open-vault"

FILE_DEFAULT_LIMIT = {
    "announcement": 20,
    "calendar": 500,
    "internal_report": 100,
    "opinion": 800,
    "report": 100,
    "foreign_report": 100,
    "summary": 100,
    "wechat_message": 1000,
}

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

FILE_TYPE_MAP = {
    "研究报告": 10,
    "外资研报": 11,
    "内部报告": 20,
    "AI云盘": 30,
    "首席观点": 40,
    "公司公告": 50,
    "港股公告": 51,
    "会议纪要": 60,
    "调研纪要": 70,
    "网络纪要": 80,
    "产业公众号": 90,
}

FILE_TYPE_MAP_REVERSE = {
    v: k for k, v in FILE_TYPE_MAP.items()
}

INDUSTRIES_MAP = {
    "中信行业分类":{
        "石油石化": 100800101,
        "煤炭": 100800102,
        "有色金属": 100800103,
        "电公": 100800104,
        "钢铁": 100800105,
        "基础化工": 100800106,
        "建筑": 100800107,
        "建材": 100800108,
        "轻工制造": 100800109,
        "机械": 100800110,
        "电新": 100800111,
        "国防军工": 100800112,
        "汽车": 100800113,
        "商贸零售": 100800114,
        "消服": 100800115,
        "家电": 100800116,
        "纺织服装": 100800117,
        "医药": 100800118,
        "食品饮料": 100800119,
        "农林牧渔": 100800120,
        "银行": 100800121,
        "非银": 100800122,
        "房地产": 100800123,
        "综合金融": 100800124,
        "交通运输": 100800125,
        "电子": 100800126,
        "通信": 100800127,
        "计算机": 100800128,
        "传媒": 100800129,
        "综合": 100800130,
    },
    # 申万行业分类
    "申万行业分类": {
        "公用事业": 104410000,
        "机械设备": 104640000,
        "电力设备": 104630000,
        "美容护理": 104770000,
        "商贸零售": 104450000,
        "通信": 104730000,
        "房地产": 104430000,
        "交通运输": 104420000,
        "国防军工": 104650000,
        "轻工制造": 104360000,
        "汽车": 104280000,
        "煤炭": 104740000,
        "环保": 104760000,
        "食品饮料": 104340000,
        "计算机": 104710000,
        "有色金属": 104240000,
        "非银金融": 104490000,
        "综合": 104510000,
        "建筑装饰": 104620000,
        "纺织服饰": 104350000,
        "家用电器": 104330000,
        "医药生物": 104370000,
        "钢铁": 104230000,
        "社会服务": 104460000,
        "农林牧渔": 104110000,
        "银行": 104480000,
        "传媒": 104720000,
        "基础化工": 104220000,
        "建筑材料": 104610000,
        "石油石化": 104750000,
        "电子": 104270000,
    }
}

RESEARCH_AREA_MAP = {
    "宏观": 122000001,
    "策略": 122000002,
    "固收": 122000003,
    "金工": 122000004,
    "海外": 122000005,
}

# 外资研报等区域：中文名 -> 区域 ID（见开放平台区域分类）
REGIONS_MAP = {
    "中国": "cn",
    "中国香港": "cnHk",
    "中国台湾": "cnTw",
    "美国": "us",
    "日本": "jp",
    "东南亚": "sea",
    "全球": "gl",
    "英国": "uk",
    "法国": "fr",
    "德国": "de",
    "韩国": "kr",
    "印度": "in",
    "加拿大": "ca",
    "中东": "me",
    "亚洲其他": "othAs",
    "欧洲其他": "othEur",
    "拉丁美洲": "latAm",
    "大洋洲": "oce",
    "非洲": "af",
}

INSTITUTIONS_MAP = {
    "野村证券": "C800150015",
    "星展银行": "C800150624",
    "渤海证券": "C100000001",
    "山西证券": "C100000007",
    "西南证券": "C100000009",
    "南京证券": "C100000010",
    "世纪证券": "C100000011",
    "中天证券": "C100000012",
    "大通证券": "C100000013",
    "华泰证券": "C100000014",
    "东吴证券": "C100000016",
    "东海证券": "C100000017",
    "中山证券": "C100000018",
    "国海证券": "C100000019",
    "招商证券": "C100000020",
    "开源证券": "C100000022",
    "国信证券": "C100000023",
    "方正证券": "C100000024",
    "英大证券": "C100000028",
    "光大证券": "C100000029",
    "长城证券": "C100000030",
    "平安证券": "C100000031",
    "湘财证券": "C100000032",
    "民生证券": "C100000034",
    "长城国瑞证券": "C100000035",
    "国元证券": "C100000036",
    "东莞证券": "C100000037",
    "华林证券": "C100000038",
    "川财证券": "C100000041",
    "东方证券": "C100000042",
    "第一创业": "C100000043",
    "大同证券": "C100000044",
    "金融街证券": "C100000045",
    "国联民生": "C100000046",
    "首创证券": "C100000048",
    "东方财富证券": "C100000049",
    "兴业证券": "C100000051",
    "华西证券": "C100000052",
    "五矿证券": "C100000053",
    "华金证券": "C100000054",
    "华安证券": "C100000055",
    "西部证券": "C100000056",
    "联储证券": "C100000057",
    "华鑫证券": "C100000058",
    "华龙证券": "C100000061",
    "中泰证券": "C100000062",
    "天府证券": "C100000063",
    "万联证券": "C100000064",
    "国都证券": "C100000065",
    "万和证券": "C100000067",
    "华创证券": "C100000068",
    "红塔证券": "C100000069",
    "中银证券": "C100000070",
    "华宝证券": "C100000071",
    "国融证券": "C100000072",
    "财达证券": "C100000073",
    "浙商证券": "C100000075",
    "金元证券": "C100000076",
    "财信证券": "C100000077",
    "爱建证券": "C100000078",
    "中邮证券": "C100000079",
    "中航证券": "C100000080",
    "中原证券": "C100000081",
    "华源证券": "C100000082",
    "国盛证券": "C100000083",
    "德邦证券": "C100000084",
    "财通证券": "C100000085",
    "诚通证券": "C100000086",
    "江海证券": "C100000088",
    "国开证券": "C100000089",
    "太平洋": "C100000090",
    "高盛中国证券": "C100000093",
    "中信建投": "C100000095",
    "国投证券": "C100000096",
    "银泰证券": "C100000097",
    "中国银河": "C100000099",
    "信达证券": "C100000100",
    "国新证券": "C100000101",
    "东兴证券": "C100000102",
    "北京证券": "C100000103",
    "申港证券": "C100000126",
    "华兴证券": "C100000128",
    "东亚前海证券": "C100000129",
    "汇丰前海证券": "C100000130",
    "野村东方国际证券": "C100000132",
    "摩根大通证券中国": "C100000133",
    "甬兴证券": "C100000135",
    "金圆统一证券": "C100000137",
    "星展证券中国": "C100000140",
    "华福证券": "C100000004",
    "粤开证券": "C100000005",
    "东北证券": "C100000015",
    "麦高证券": "C100000025",
    "上海证券": "C100000060",
    "国金证券": "C100000006",
    "海通证券": "C100000008",
    "广发证券": "C100000021",
    "中金公司": "C100000026",
    "中信证券": "C100000027",
    "长江证券": "C100000039",
    "国泰海通": "C100000047",
    "天风证券": "C100000050",
    "瑞银证券": "C100000098",
    "申万宏源证券": "C100000119",
    "摩根士丹利": "C800040335",
    "巴克莱": "C800065266",
    "德意志银行": "C800070012",
    "汇丰控股": "C800105979",
    "高盛": "C800110443",
    "美国银行": "C800110523",
    "摩根大通": "C800114009",
    "坎特菲茨杰拉德公司": "C800014962",
    "巴西投资银行": "C800015193",
    "BMO Harris Bank": "C800015458",
    "奥尔巴赫格雷森投资": "C800018355",
    "Btic America Corporation": "C800019294",
    "联昌证券": "C800020171",
    "奥地利第一储蓄银行": "C800020225",
    "瑞士信贷集团": "C800020841",
    "Evercore": "C800021184",
    "里昂证券": "C800022831",
    "道明证券": "C800024532",
    "麦格理": "C800033691",
    "古根海姆证券": "C800038847",
    "加拿大皇家银行": "C800044779",
    "美国投资银行派杰公司": "C800045141",
    "法国兴业银行": "C800050267",
    "威廉博莱公司": "C800054695",
    "Truist证券": "C800055019",
    "韦德布什证券": "C800055550",
    "Barclays Bank": "C801298117",
    "北欧联合银行": "C801316708",
    "BNP Paribas SA": "C801317677",
    "杰富瑞集团": "C801303042",
    "加拿大丰业银行": "C801304832",
    "加拿大帝国商业银行": "C801196501",
    "贝伦伯格资管": "C801196577",
    "挪威DNB投资银行": "C801196841",
    "富国证券": "C801198303",
    "开普勒盛富证券": "C900006685",
    "帕累托证券": "C900006686",
    "TD Securities": "C900006687",
    "国民银行": "C900006694",
    "蒙特利尔银行": "C801342605",
    "BTIG": "C900006697",
    "高华证券": "C100000092",
    "恒泰长财": "C100000066",
    "中天国富": "C100000091",
    "国联民生证券承销保荐": "C100000107",
    "中德证券": "C100000104",
    "金通证券": "C100000117",
    "伯恩斯坦研究": "C800016741",
    "高盛集团": "C800080335",
    "花旗银行": "C800090764",
    "瑞银集团": "C800127057",
    "高盛": "C800082057",
    "法巴证券中国": "C801352341",
    "上海申银万国证券研究所": "C500000318",
    "大和证券": "C800070011",
    "法国兴业银行": "C801318100",
    "摩根大通": "C900005224",
    "银河海外": "C800025530",
    "加拿大皇家银行": "C800041439",
    "瑞银": "C800051885",
    "瑞士信贷": "C801342334",
    "杰富瑞金融": "C800031261",
    "中信里昂证券": "C800160866",
    "挪威银行": "C801322814",
    "德意志银行": "C801165257",
    "加拿大帝国商业银行": "C800013239",
    "贝伦伯格银行": "C800035749",
    "蒙特利尔银行": "C800103054",
    "加拿大丰业银行": "C800100302",
    "National Bank of Canada": "C800103710",
    "Piper Sandler": "C800041170",
    "花旗": "C800090327",
    "威廉博莱": "C800142261",
    "海通国际": "C800096075",
    "国盛证券": "C900001246",
    "国金证券公司": "C801361610",
}

ANNOUNCEMENT_CATEGORY_MAP = {
    "招股说明书": "103970511",
    "招股说明书(聆讯后版)": "103970510",
    "招股说明书(申报版)": "103970509",
    "港股公告": "103970000",
    "杠杆及反向产品": "103970802",
    "交易所买卖基金": "103970801",
    "其他证券产品": "103970800",
    "结构性产品发行人": "103970706",
    "股票挂钩票据": "103970705",
    "衍生权证": "103970704",
    "债务证券": "103970703",
    "债务证券发行计划": "103970702",
    "牛熊证": "103970701",
    "债券及结构性产品": "103970700",
    "监管者公告": "103970605",
    "展示文件": "103970603",
    "宪章文件": "103970602",
    "委任代表表格": "103970601",
    "一般公告": "103970600",
    "其他上市文件": "103970508",
    "资本化发行": "103970507",
    "发售现有证券": "103970506",
    "发售以供认购": "103970505",
    "供股": "103970504",
    "聆讯资料": "103970503",
    "公开招股": "103970502",
    "介绍": "103970501",
    "上市文件": "103970500",
    "杂项": "103970408",
    "新上市": "103970407",
    "财务资料": "103970406",
    "重大事项": "103970405",
    "须予公布的交易": "103970404",
    "会议/表决": "103970403",
    "公司变动": "103970402",
    "关联交易": "103970401",
    "公告通函": "103970400",
    "月报表": "103970304",
    "翌日报表": "103970303",
    "交易披露": "103970302",
    "证券/股本": "103970301",
    "股权股本": "103970300",
    "季度业绩": "103970204",
    "中期业绩": "103970203",
    "末期业绩": "103970202",
    "业绩预告": "103970201",
    "业绩快报": "103970200",
    "季度报告": "103970104",
    "中期报告": "103970103",
    "ESG报告": "103970102",
    "年度报告": "103970101",
    "财务报告": "103970100",
    "公司资料报表": "103970604",
    "其他公告": "103980707",
    "文件审查通信": "103980706",
    "SEC通知": "103980705",
    "权证出售": "103980704",
    "中介公告": "103980703",
    "财务信息": "103980702",
    "公司治理": "103980701",
    "一般公告": "103980700",
    "股东倡议及通告": "103980603",
    "最终委托书": "103980602",
    "初步委托书": "103980601",
    "股东大会": "103980600",
    "其他权益": "103980505",
    "重要股东减持": "103980504",
    "内部交易": "103980503",
    "机构持仓": "103980502",
    "大股东持股": "103980501",
    "股本股东": "103980500",
    "转板/退市": "103980402",
    "私有化交易": "103980401",
    "交易提示": "103980400",
    "其他重大事项": "103980305",
    "保密信息": "103980304",
    "收购兼并": "103980303",
    "破产清算": "103980302",
    "重大协议": "103980301",
    "重大事项": "103980300",
    "补充修订": "103980208",
    "撤销上市申请": "103980207",
    "发行获准": "103980206",
    "发行说明书": "103980205",
    "发行预案": "103980204",
    "上市获准": "103980203",
    "首发说明书": "103980202",
    "首发预案": "103980201",
    "证券发行": "103980200",
    "财报修订": "103980105",
    "延迟/过渡": "103980104",
    "年度报告": "103980103",
    "季度报告": "103980102",
    "业绩快报": "103980101",
    "财务报告": "103980100",
    "美股公告": "103980000",
    "基金净值公告": "103960101",
    "基金发售": "103960111",
    "临时公告": "103960110",
    "产品资料概要": "103960109",
    "基金销售": "103960105",
    "清算公告": "103960104",
    "招募说明书": "103960108",
    "定期报告": "103960107",
    "基金月报": "103960106",
    "财报摘要": "103910214",
    "其他财务报告": "103910210",
    "申购赎回": "103960103",
    "收益分配": "103960102",
    "互认基金": "103960100",
    "香港基金公告": "103960000",
    "估值调整": "103920403",
    "基金销售": "103920402",
    "基金其它公告": "103920419",
    "交易提示": "103920420",
    "基金其它情况": "103920700",
    "募集期调整": "103920412",
    "持有人大会": "103920409",
    "清算报告": "103920417",
    "参与增发": "103920416",
    "管理公司信息": "103920421",
    "基金经理变更": "103920414",
    "申购赎回": "103920401",
    "收益分配": "103920501",
    "重要事项": "103920400",
    "托管协议": "103920105",
    "产品资料概要": "103920107",
    "基金合同": "103920111",
    "发行上市": "103920102",
    "成立公告": "103920108",
    "招募说明书": "103920101",
    "基金招募": "103920100",
    "基金年报": "103920312",
    "基金半年报": "103920309",
    "基金季报": "103920106",
    "基金定期报告": "103920300",
    "公募基金公告": "103920000",
    "发行定价": "103910104",
    "增发获准": "103910603",
    "关联H股": "103910833",
    "经营快报": "103910817",
    "权证公告": "103910805",
    "独立董事声明": "103910827",
    "公司制度文件": "103910819",
    "公司资料变更": "103910810",
    "专项意见": "103910903",
    "内部控制与自查": "103910902",
    "董监高工作报告": "103910901",
    "一般公告": "103910800",
    "股权股本": "103910700",
    "公司治理": "103910900",
    "监事会公告": "103910822",
    "员工持股": "103910802",
    "股东大会公告": "103910302",
    "董事会公告": "103910301",
    "澄清致歉": "103910403",
    "一般补充更正": "103910812",
    "问询函及回复": "103910823",
    "ESG报告": "103910820",
    "投资者关系": "103910809",
    "融资融券": "103910808",
    "法律纠纷": "103910807",
    "中介公告": "103910806",
    "股权分置改革": "103910707",
    "约定购回": "103910706",
    "质押式回购": "103910704",
    "股权回购": "103910705",
    "质押冻结": "103910703",
    "股本变动": "103910702",
    "股权变动": "103910701",
    "其他增发公告": "103910607",
    "增发上市": "103910605",
    "增发结果": "103910608",
    "增发发行": "103910604",
    "增发说明书": "103910602",
    "增发预案": "103910601",
    "其他配股公告": "103910507",
    "配股结果": "103910506",
    "配股上市": "103910505",
    "配股发行": "103910504",
    "配股获准": "103910503",
    "配股说明书": "103910502",
    "配股预案": "103910501",
    "暂停上市": "103910408",
    "恢复上市": "103910407",
    "终止上市": "103910406",
    "特别处理": "103910405",
    "风险提示": "103910404",
    "交易异动": "103910402",
    "停复牌提示": "103910401",
    "合同及协议": "103910308",
    "政策影响": "103910804",
    "违纪违规": "103910311",
    "资金占用": "103910319",
    "资金投向": "103910310",
    "人事变动": "103910309",
    "股权激励": "103910803",
    "投资理财": "103910801",
    "借贷担保": "103910307",
    "关联交易": "103910306",
    "收购兼并": "103910305",
    "资产重组": "103910304",
    "股份增减持": "103910818",
    "利润分配": "103910303",
    "补充更正": "103910209",
    "年度报告": "103910208",
    "半年度报告": "103910207",
    "三季度报告": "103910205",
    "一季度报告": "103910203",
    "业绩快报": "103910202",
    "其他首发公告": "103910108",
    "业绩预告": "103910201",
    "上市公告书": "103910106",
    "发行结果": "103910105",
    "招股说明书": "103910103",
    "申报反馈": "103910102",
    "招股说明书(申报稿)": "103910101",
    "发明专利证书": "103910832",
    "可转债": "103910708",
    "披露提示": "103910409",
    "其他公告": "103910813",
    "增发": "103910600",
    "配股": "103910500",
    "交易提示": "103910400",
    "重大事项": "103910300",
    "财务报告": "103910200",
    "IPO": "103910100",
    "股票公告": "103910000",
}
ANNOUNCEMENT_CATEGORYS = [
    {
        "tree_name": "港股公告(103970000)",
        "categoryId": "103970000",
        "children": [
            {
                "tree_name": "财务报告(103970100)",
                "categoryId": "103970100",
                "children": [
                    {"tree_name": "年度报告(103970101)", "categoryId": "103970101", "children": []},
                    {"tree_name": "ESG报告(103970102)", "categoryId": "103970102", "children": []},
                    {"tree_name": "中期报告(103970103)", "categoryId": "103970103", "children": []},
                    {"tree_name": "季度报告(103970104)", "categoryId": "103970104", "children": []},
                ],
            },
            {
                "tree_name": "业绩快报(103970200)",
                "categoryId": "103970200",
                "children": [
                    {"tree_name": "业绩预告(103970201)", "categoryId": "103970201", "children": []},
                    {"tree_name": "末期业绩(103970202)", "categoryId": "103970202", "children": []},
                    {"tree_name": "中期业绩(103970203)", "categoryId": "103970203", "children": []},
                    {"tree_name": "季度业绩(103970204)", "categoryId": "103970204", "children": []},
                ],
            },
            {
                "tree_name": "股权股本(103970300)",
                "categoryId": "103970300",
                "children": [
                    {"tree_name": "证券/股本(103970301)", "categoryId": "103970301", "children": []},
                    {"tree_name": "交易披露(103970302)", "categoryId": "103970302", "children": []},
                    {"tree_name": "翌日报表(103970303)", "categoryId": "103970303", "children": []},
                    {"tree_name": "月报表(103970304)", "categoryId": "103970304", "children": []},
                ],
            },
            {
                "tree_name": "公告通函(103970400)",
                "categoryId": "103970400",
                "children": [
                    {"tree_name": "关联交易(103970401)", "categoryId": "103970401", "children": []},
                    {"tree_name": "公司变动(103970402)", "categoryId": "103970402", "children": []},
                    {"tree_name": "会议/表决(103970403)", "categoryId": "103970403", "children": []},
                    {"tree_name": "须予公布的交易(103970404)", "categoryId": "103970404", "children": []},
                    {"tree_name": "重大事项(103970405)", "categoryId": "103970405", "children": []},
                    {"tree_name": "财务资料(103970406)", "categoryId": "103970406", "children": []},
                    {"tree_name": "新上市(103970407)", "categoryId": "103970407", "children": []},
                    {"tree_name": "杂项(103970408)", "categoryId": "103970408", "children": []},
                ],
            },
            {
                "tree_name": "上市文件(103970500)",
                "categoryId": "103970500",
                "children": [
                    {"tree_name": "介绍(103970501)", "categoryId": "103970501", "children": []},
                    {"tree_name": "公开招股(103970502)", "categoryId": "103970502", "children": []},
                    {"tree_name": "聆讯资料(103970503)", "categoryId": "103970503", "children": []},
                    {"tree_name": "供股(103970504)", "categoryId": "103970504", "children": []},
                    {"tree_name": "发售以供认购(103970505)", "categoryId": "103970505", "children": []},
                    {"tree_name": "发售现有证券(103970506)", "categoryId": "103970506", "children": []},
                    {"tree_name": "资本化发行(103970507)", "categoryId": "103970507", "children": []},
                    {"tree_name": "其他上市文件(103970508)", "categoryId": "103970508", "children": []},
                    {"tree_name": "招股说明书(申报版)(103970509)", "categoryId": "103970509", "children": []},
                    {"tree_name": "招股说明书(聆讯后版)(103970510)", "categoryId": "103970510", "children": []},
                    {"tree_name": "招股说明书(103970511)", "categoryId": "103970511", "children": []},
                ],
            },
            {
                "tree_name": "一般公告(103970600)",
                "categoryId": "103970600",
                "children": [
                    {"tree_name": "委任代表表格(103970601)", "categoryId": "103970601", "children": []},
                    {"tree_name": "宪章文件(103970602)", "categoryId": "103970602", "children": []},
                    {"tree_name": "展示文件(103970603)", "categoryId": "103970603", "children": []},
                    {"tree_name": "公司资料报表(103970604)", "categoryId": "103970604", "children": []},
                    {"tree_name": "监管者公告(103970605)", "categoryId": "103970605", "children": []},
                ],
            },
            {
                "tree_name": "债券及结构性产品(103970700)",
                "categoryId": "103970700",
                "children": [
                    {"tree_name": "牛熊证(103970701)", "categoryId": "103970701", "children": []},
                    {"tree_name": "债务证券发行计划(103970702)", "categoryId": "103970702", "children": []},
                    {"tree_name": "债务证券(103970703)", "categoryId": "103970703", "children": []},
                    {"tree_name": "衍生权证(103970704)", "categoryId": "103970704", "children": []},
                    {"tree_name": "股票挂钩票据(103970705)", "categoryId": "103970705", "children": []},
                    {"tree_name": "结构性产品发行人(103970706)", "categoryId": "103970706", "children": []},
                ],
            },
            {
                "tree_name": "其他证券产品(103970800)",
                "categoryId": "103970800",
                "children": [
                    {"tree_name": "交易所买卖基金(103970801)", "categoryId": "103970801", "children": []},
                    {"tree_name": "杠杆及反向产品(103970802)", "categoryId": "103970802", "children": []},
                ],
            },
        ],
    },
    {
        "tree_name": "美股公告(103980000)",
        "categoryId": "103980000",
        "children": [
            {
                "tree_name": "财务报告(103980100)",
                "categoryId": "103980100",
                "children": [
                    {"tree_name": "业绩快报(103980101)", "categoryId": "103980101", "children": []},
                    {"tree_name": "季度报告(103980102)", "categoryId": "103980102", "children": []},
                    {"tree_name": "年度报告(103980103)", "categoryId": "103980103", "children": []},
                    {"tree_name": "延迟/过渡(103980104)", "categoryId": "103980104", "children": []},
                    {"tree_name": "财报修订(103980105)", "categoryId": "103980105", "children": []},
                ],
            },
            {
                "tree_name": "证券发行(103980200)",
                "categoryId": "103980200",
                "children": [
                    {"tree_name": "首发预案(103980201)", "categoryId": "103980201", "children": []},
                    {"tree_name": "首发说明书(103980202)", "categoryId": "103980202", "children": []},
                    {"tree_name": "上市获准(103980203)", "categoryId": "103980203", "children": []},
                    {"tree_name": "发行预案(103980204)", "categoryId": "103980204", "children": []},
                    {"tree_name": "发行说明书(103980205)", "categoryId": "103980205", "children": []},
                    {"tree_name": "发行获准(103980206)", "categoryId": "103980206", "children": []},
                    {"tree_name": "撤销上市申请(103980207)", "categoryId": "103980207", "children": []},
                    {"tree_name": "补充修订(103980208)", "categoryId": "103980208", "children": []},
                ],
            },
            {
                "tree_name": "重大事项(103980300)",
                "categoryId": "103980300",
                "children": [
                    {"tree_name": "重大协议(103980301)", "categoryId": "103980301", "children": []},
                    {"tree_name": "破产清算(103980302)", "categoryId": "103980302", "children": []},
                    {"tree_name": "收购兼并(103980303)", "categoryId": "103980303", "children": []},
                    {"tree_name": "保密信息(103980304)", "categoryId": "103980304", "children": []},
                    {"tree_name": "其他重大事项(103980305)", "categoryId": "103980305", "children": []},
                ],
            },
            {
                "tree_name": "交易提示(103980400)",
                "categoryId": "103980400",
                "children": [
                    {"tree_name": "私有化交易(103980401)", "categoryId": "103980401", "children": []},
                    {"tree_name": "转板/退市(103980402)", "categoryId": "103980402", "children": []},
                ],
            },
            {
                "tree_name": "股本股东(103980500)",
                "categoryId": "103980500",
                "children": [
                    {"tree_name": "大股东持股(103980501)", "categoryId": "103980501", "children": []},
                    {"tree_name": "机构持仓(103980502)", "categoryId": "103980502", "children": []},
                    {"tree_name": "内部交易(103980503)", "categoryId": "103980503", "children": []},
                    {"tree_name": "重要股东减持(103980504)", "categoryId": "103980504", "children": []},
                    {"tree_name": "其他权益(103980505)", "categoryId": "103980505", "children": []},
                ],
            },
            {
                "tree_name": "股东大会(103980600)",
                "categoryId": "103980600",
                "children": [
                    {"tree_name": "初步委托书(103980601)", "categoryId": "103980601", "children": []},
                    {"tree_name": "最终委托书(103980602)", "categoryId": "103980602", "children": []},
                    {"tree_name": "股东倡议及通告(103980603)", "categoryId": "103980603", "children": []},
                ],
            },
            {
                "tree_name": "一般公告(103980700)",
                "categoryId": "103980700",
                "children": [
                    {"tree_name": "公司治理(103980701)", "categoryId": "103980701", "children": []},
                    {"tree_name": "财务信息(103980702)", "categoryId": "103980702", "children": []},
                    {"tree_name": "中介公告(103980703)", "categoryId": "103980703", "children": []},
                    {"tree_name": "权证出售(103980704)", "categoryId": "103980704", "children": []},
                    {"tree_name": "SEC通知(103980705)", "categoryId": "103980705", "children": []},
                    {"tree_name": "文件审查通信(103980706)", "categoryId": "103980706", "children": []},
                    {"tree_name": "其他公告(103980707)", "categoryId": "103980707", "children": []},
                ],
            },
        ],
    },
    {
        "tree_name": "香港基金公告(103960000)",
        "categoryId": "103960000",
        "children": [
            {
                "tree_name": "互认基金(103960100)",
                "categoryId": "103960100",
                "children": [
                    {"tree_name": "基金净值公告(103960101)", "categoryId": "103960101", "children": []},
                    {"tree_name": "收益分配(103960102)", "categoryId": "103960102", "children": []},
                    {"tree_name": "申购赎回(103960103)", "categoryId": "103960103", "children": []},
                    {"tree_name": "清算公告(103960104)", "categoryId": "103960104", "children": []},
                    {"tree_name": "基金销售(103960105)", "categoryId": "103960105", "children": []},
                    {"tree_name": "基金月报(103960106)", "categoryId": "103960106", "children": []},
                    {"tree_name": "定期报告(103960107)", "categoryId": "103960107", "children": []},
                    {"tree_name": "招募说明书(103960108)", "categoryId": "103960108", "children": []},
                    {"tree_name": "产品资料概要(103960109)", "categoryId": "103960109", "children": []},
                    {"tree_name": "临时公告(103960110)", "categoryId": "103960110", "children": []},
                    {"tree_name": "基金发售(103960111)", "categoryId": "103960111", "children": []},
                ],
            }
        ],
    },
    {
        "tree_name": "公募基金公告(103920000)",
        "categoryId": "103920000",
        "children": [
            {
                "tree_name": "基金招募(103920100)",
                "categoryId": "103920100",
                "children": [
                    {"tree_name": "招募说明书(103920101)", "categoryId": "103920101", "children": []},
                    {"tree_name": "发行上市(103920102)", "categoryId": "103920102", "children": []},
                    {"tree_name": "托管协议(103920105)", "categoryId": "103920105", "children": []},
                    {"tree_name": "基金季报(103920106)", "categoryId": "103920106", "children": []},
                    {"tree_name": "产品资料概要(103920107)", "categoryId": "103920107", "children": []},
                    {"tree_name": "成立公告(103920108)", "categoryId": "103920108", "children": []},
                    {"tree_name": "基金合同(103920111)", "categoryId": "103920111", "children": []},
                ],
            },
            {
                "tree_name": "基金定期报告(103920300)",
                "categoryId": "103920300",
                "children": [
                    {"tree_name": "基金季报(103920106)", "categoryId": "103920106", "children": []},
                    {"tree_name": "基金半年报(103920309)", "categoryId": "103920309", "children": []},
                    {"tree_name": "基金年报(103920312)", "categoryId": "103920312", "children": []},
                ],
            },
            {
                "tree_name": "重要事项(103920400)",
                "categoryId": "103920400",
                "children": [
                    {"tree_name": "申购赎回(103920401)", "categoryId": "103920401", "children": []},
                    {"tree_name": "基金经理变更(103920414)", "categoryId": "103920414", "children": []},
                    {"tree_name": "管理公司信息(103920421)", "categoryId": "103920421", "children": []},
                    {"tree_name": "参与增发(103920416)", "categoryId": "103920416", "children": []},
                    {"tree_name": "清算报告(103920417)", "categoryId": "103920417", "children": []},
                    {"tree_name": "持有人大会(103920409)", "categoryId": "103920409", "children": []},
                    {"tree_name": "募集期调整(103920412)", "categoryId": "103920412", "children": []},
                ],
            },
            {
                "tree_name": "基金其它情况(103920700)",
                "categoryId": "103920700",
                "children": [
                    {"tree_name": "估值调整(103920403)", "categoryId": "103920403", "children": []},
                    {"tree_name": "基金销售(103920402)", "categoryId": "103920402", "children": []},
                    {"tree_name": "基金其它公告(103920419)", "categoryId": "103920419", "children": []},
                    {"tree_name": "交易提示(103920420)", "categoryId": "103920420", "children": []},
                ],
            },
            {
                "tree_name": "收益分配(103920501)",
                "categoryId": "103920501",
                "children": [],
            },
        ],
    },
    {
        "tree_name": "股票公告(103910000)",
        "categoryId": "103910000",
        "children": [
            {"tree_name": "IPO(103910100)", "categoryId": "103910100", "children": [
                {"tree_name": "招股说明书(申报稿)(103910101)", "categoryId": "103910101", "children": []},
                {"tree_name": "申报反馈(103910102)", "categoryId": "103910102", "children": []},
                {"tree_name": "招股说明书(103910103)", "categoryId": "103910103", "children": []},
                {"tree_name": "发行定价(103910104)", "categoryId": "103910104", "children": []},
                {"tree_name": "发行结果(103910105)", "categoryId": "103910105", "children": []},
                {"tree_name": "上市公告书(103910106)", "categoryId": "103910106", "children": []},
                {"tree_name": "其他首发公告(103910108)", "categoryId": "103910108", "children": []},
            ]},
            {"tree_name": "财务报告(103910200)", "categoryId": "103910200", "children": [
                {"tree_name": "业绩快报(103910202)", "categoryId": "103910202", "children": []},
                {"tree_name": "一季度报告(103910203)", "categoryId": "103910203", "children": []},
                {"tree_name": "三季度报告(103910205)", "categoryId": "103910205", "children": []},
                {"tree_name": "半年度报告(103910207)", "categoryId": "103910207", "children": []},
                {"tree_name": "年度报告(103910208)", "categoryId": "103910208", "children": []},
                {"tree_name": "补充更正(103910209)", "categoryId": "103910209", "children": []},
                {"tree_name": "其他财务报告(103910210)", "categoryId": "103910210", "children": []},
                {"tree_name": "财报摘要(103910214)", "categoryId": "103910214", "children": []},
                {"tree_name": "业绩预告(103910201)", "categoryId": "103910201", "children": []},
            ]},
            {"tree_name": "重大事项(103910300)", "categoryId": "103910300", "children": [
                {"tree_name": "董事会公告(103910301)", "categoryId": "103910301", "children": []},
                {"tree_name": "股东大会公告(103910302)", "categoryId": "103910302", "children": []},
                {"tree_name": "利润分配(103910303)", "categoryId": "103910303", "children": []},
                {"tree_name": "资产重组(103910304)", "categoryId": "103910304", "children": []},
                {"tree_name": "收购兼并(103910305)", "categoryId": "103910305", "children": []},
                {"tree_name": "关联交易(103910306)", "categoryId": "103910306", "children": []},
                {"tree_name": "借贷担保(103910307)", "categoryId": "103910307", "children": []},
                {"tree_name": "合同及协议(103910308)", "categoryId": "103910308", "children": []},
                {"tree_name": "人事变动(103910309)", "categoryId": "103910309", "children": []},
                {"tree_name": "资金投向(103910310)", "categoryId": "103910310", "children": []},
                {"tree_name": "违纪违规(103910311)", "categoryId": "103910311", "children": []},
                {"tree_name": "资金占用(103910319)", "categoryId": "103910319", "children": []},
                {"tree_name": "投资理财(103910801)", "categoryId": "103910801", "children": []},
                {"tree_name": "股份增减持(103910818)", "categoryId": "103910818", "children": []},
                {"tree_name": "股权激励(103910803)", "categoryId": "103910803", "children": []},
                {"tree_name": "政策影响(103910804)", "categoryId": "103910804", "children": []},
                {"tree_name": "可转债(103910708)", "categoryId": "103910708", "children": []},
            ]},
            {"tree_name": "交易提示(103910400)", "categoryId": "103910400", "children": [
                {"tree_name": "停复牌提示(103910401)", "categoryId": "103910401", "children": []},
                {"tree_name": "交易异动(103910402)", "categoryId": "103910402", "children": []},
                {"tree_name": "风险提示(103910404)", "categoryId": "103910404", "children": []},
                {"tree_name": "特别处理(103910405)", "categoryId": "103910405", "children": []},
                {"tree_name": "终止上市(103910406)", "categoryId": "103910406", "children": []},
                {"tree_name": "恢复上市(103910407)", "categoryId": "103910407", "children": []},
                {"tree_name": "暂停上市(103910408)", "categoryId": "103910408", "children": []},
                {"tree_name": "披露提示(103910409)", "categoryId": "103910409", "children": []},
            ]},
            {"tree_name": "配股(103910500)", "categoryId": "103910500", "children": [
                {"tree_name": "配股预案(103910501)", "categoryId": "103910501", "children": []},
                {"tree_name": "配股说明书(103910502)", "categoryId": "103910502", "children": []},
                {"tree_name": "配股获准(103910503)", "categoryId": "103910503", "children": []},
                {"tree_name": "配股发行(103910504)", "categoryId": "103910504", "children": []},
                {"tree_name": "配股上市(103910505)", "categoryId": "103910505", "children": []},
                {"tree_name": "配股结果(103910506)", "categoryId": "103910506", "children": []},
                {"tree_name": "其他配股公告(103910507)", "categoryId": "103910507", "children": []},
            ]},
            {"tree_name": "增发(103910600)", "categoryId": "103910600", "children": [
                {"tree_name": "增发预案(103910601)", "categoryId": "103910601", "children": []},
                {"tree_name": "增发说明书(103910602)", "categoryId": "103910602", "children": []},
                {"tree_name": "增发获准(103910603)", "categoryId": "103910603", "children": []},
                {"tree_name": "增发发行(103910604)", "categoryId": "103910604", "children": []},
                {"tree_name": "增发上市(103910605)", "categoryId": "103910605", "children": []},
                {"tree_name": "其他增发公告(103910607)", "categoryId": "103910607", "children": []},
                {"tree_name": "增发结果(103910608)", "categoryId": "103910608", "children": []},
            ]},
            {"tree_name": "股权股本(103910700)", "categoryId": "103910700", "children": [
                {"tree_name": "股权变动(103910701)", "categoryId": "103910701", "children": []},
                {"tree_name": "股本变动(103910702)", "categoryId": "103910702", "children": []},
                {"tree_name": "质押冻结(103910703)", "categoryId": "103910703", "children": []},
                {"tree_name": "质押式回购(103910704)", "categoryId": "103910704", "children": []},
                {"tree_name": "股权回购(103910705)", "categoryId": "103910705", "children": []},
                {"tree_name": "约定购回(103910706)", "categoryId": "103910706", "children": []},
                {"tree_name": "股权分置改革(103910707)", "categoryId": "103910707", "children": []},
            ]},
            {"tree_name": "一般公告(103910800)", "categoryId": "103910800", "children": [
                {"tree_name": "员工持股(103910802)", "categoryId": "103910802", "children": []},
                {"tree_name": "法律纠纷(103910807)", "categoryId": "103910807", "children": []},
                {"tree_name": "融资融券(103910808)", "categoryId": "103910808", "children": []},
                {"tree_name": "投资者关系(103910809)", "categoryId": "103910809", "children": []},
                {"tree_name": "公司资料变更(103910810)", "categoryId": "103910810", "children": []},
                {"tree_name": "一般补充更正(103910812)", "categoryId": "103910812", "children": []},
                {"tree_name": "其他公告(103910813)", "categoryId": "103910813", "children": []},
                {"tree_name": "经营快报(103910817)", "categoryId": "103910817", "children": []},
                {"tree_name": "ESG报告(103910820)", "categoryId": "103910820", "children": []},
                {"tree_name": "问询函及回复(103910823)", "categoryId": "103910823", "children": []},
                {"tree_name": "监事会公告(103910822)", "categoryId": "103910822", "children": []},
                {"tree_name": "违纪违规(103910311)", "categoryId": "103910311", "children": []},
                {"tree_name": "中介公告(103910806)", "categoryId": "103910806", "children": []},
                {"tree_name": "澄清致歉(103910403)", "categoryId": "103910403", "children": []},
                {"tree_name": "发明专利证书(103910832)", "categoryId": "103910832", "children": []},
                {"tree_name": "关联H股(103910833)", "categoryId": "103910833", "children": []},
                {"tree_name": "权证公告(103910805)", "categoryId": "103910805", "children": []},
            ]},
            {"tree_name": "公司治理(103910900)", "categoryId": "103910900", "children": [
                {"tree_name": "董监高工作报告(103910901)", "categoryId": "103910901", "children": []},
                {"tree_name": "内部控制与自查(103910902)", "categoryId": "103910902", "children": []},
                {"tree_name": "专项意见(103910903)", "categoryId": "103910903", "children": []},
                {"tree_name": "独立董事声明(103910827)", "categoryId": "103910827", "children": []},
                {"tree_name": "公司制度文件(103910819)", "categoryId": "103910819", "children": []},
            ]},
        ],
    },
]

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

def format_response(response: dict, method_name: str, output: Optional[str] = None, additional_message: str = ""):
    
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
    return_message = response.get("message", "") + "\n\n"
    method_name_map = {
        "report": "研究报告",
        "inner_report": "内部报告",
        "opinion": "首席观点",
        "announcement": "公司公告",
        "summary": "会议纪要",
        "calendar": "投研日程",
        "foreign_report": "外资研报",
    }
    if response["state"] == "success":
        for item in response["data"]:
            module_name = item["module"]
            data = item["data"]
            if GTS_SAVE_FILE:
                if output:
                    process_path = output
                    if os.path.exists(process_path):
                        return_message = "错误信息：文件已存在"
                        return return_message
                else:
                    extension = GTS_SAVE_EXTENSION
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
                if GTS_SAVE_EXTENSION == "md":
                    with open(process_path, "w", encoding="utf-8") as f:
                        for i, file in enumerate(data):
                            f.write(f"标题：{file['标题']}\n")
                            if file.get("中文标题", None):
                                f.write(f"中文标题：{file['中文标题']}\n")
                            f.write(f"文件时间：{file['文件时间']}\n")
                            for key, value in file.items():
                                if key not in ["标题", "文件时间", "类型", "类型中ID"] and value:
                                    if key == "摘要":
                                        f.write(f"摘要：\"\"\"\n{value}\n\"\"\"\n")
                                    elif key == "中文摘要":
                                        f.write(f"中文摘要：\"\"\"\n{value}\n\"\"\"\n")
                                    elif key == "正文":
                                        f.write(f"正文：\"\"\"\n{value}\n\"\"\"\n")
                                    else:
                                        f.write(f"{key}：{value}\n")
                            f.write(f"file-type：{file['类型']}\n")
                            f.write(f"file-id：{file['类型中ID']}")
                            if i < len(data) - 1:
                                f.write("\n\n---\n\n")
                elif GTS_SAVE_EXTENSION == "json":
                    with open(process_path, "w", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False)
                sample_data = ""
                for file in data:
                    sample_data += f"标题：{file['标题']}\n"
                    if file.get("中文标题", None):
                        sample_data += f"中文标题：{file['中文标题']}\n"
                    sample_data += f"文件时间：{file['文件时间']}\n"
                    for key, value in file.items():
                        if key not in ["标题", "文件时间", "类型", "类型中ID"] and value:
                            if key == "摘要":
                                sample_data += f"摘要：\"\"\"\n{value}\n\"\"\"\n"
                            elif key == "中文摘要":
                                sample_data += f"中文摘要：\"\"\"\n{value}\n\"\"\"\n"
                            elif key == "正文":
                                sample_data += f"正文：\"\"\"\n{value}\n\"\"\"\n"
                            else:
                                sample_data += f"{key}：{value}\n"
                    sample_data += f"file-type：{file['类型']}\n"
                    sample_data += f"file-id：{file['类型中ID']}"
                    sample_data += "\n\n---\n\n"
                return_message += "### " + method_name_map[method_name] + " 查询结果:\n\n---\n\n" + sample_data + f"所有查询结果已保存到{GTS_SAVE_EXTENSION}：\"" + os.path.abspath(process_path) + "\""
                return_message += f"\n查询结果共计{len(data)}条"
            else:
                sample_data = ""
                for i, file in enumerate(data):
                    sample_data += f"标题：{file['标题']}\n"
                    if file.get("中文标题", None):
                        sample_data += f"中文标题：{file['中文标题']}\n"
                    sample_data += f"文件时间：{file['文件时间']}\n"
                    for key, value in file.items():
                        if key not in ["标题", "文件时间", "类型", "类型中ID"] and value:
                            if key == "摘要":
                                sample_data += f"摘要：\"\"\"\n{value}\n\"\"\"\n"
                            elif key == "中文摘要":
                                sample_data += f"中文摘要：\"\"\"\n{value}\n\"\"\"\n"
                            elif key == "正文":
                                sample_data += f"正文：\"\"\"\n{value}\n\"\"\"\n"
                            else:
                                sample_data += f"{key}：{value}\n"
                    sample_data += f"file-type：{file['类型']}\n"
                    sample_data += f"file-id：{file['类型中ID']}"
                    sample_data += "\n\n---\n\n"
                return_message += "### " + method_name_map[method_name] + "查询结果:\n\n---\n\n" + sample_data
                return_message += f"查询结果共计{len(data)}条"
    else:
        return_message = "调用gangtise服务端失败，错误信息：" + response["message"]
    if additional_message:
        return_message += "\n" + additional_message
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
    raise ValueError("证券文件必须包含 security_code 或 security_abbr 列")

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

OPENAPI_SKILL_VERSION = "1.4.7"
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