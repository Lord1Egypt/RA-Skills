#!/usr/bin/env python3
"""航班延误赔偿助手 - Flight Delay Compensation Helper
基于飞常准API查询航班延误状态，根据各国法规计算赔偿金额，提供索赔指引
走SCF代理，用户零配置
"""
import os
import json
import sys
import urllib.request
import urllib.error
import ssl
from datetime import datetime

# ========== 配置 ==========
SCF_PROXY_URL = "https://1439498936-eqcpuaevzz.ap-guangzhou.tencentscf.com"
PROXY_TOKEN = os.environ.get("PROXY_TOKEN", "")

# 代理域名白名单
_ALLOWED_PROXY_HOSTS = ["ap-guangzhou.tencentscf.com"]

# ========== 延误赔偿法规数据库 ==========

# EU261/2004 赔偿标准
EU261_COMPENSATION = {
    "name": "欧盟EU261/2004",
    "applies": "从欧盟机场出发的航班，或欧盟航司抵达欧盟的航班",
    "thresholds": [
        {"distance": 1500, "short_delay": 3, "comp_short": 250, "comp_long": 250},
        {"distance": 3500, "short_delay": 3, "comp_short": 400, "comp_long": 400},
        {"distance": float("inf"), "short_delay": 3, "comp_short": 300, "comp_long": 600},
    ],
    "notes": "航班取消也适用；因不可抗力(天气/罢工/安全风险)可免责；2小时内可拒赔"
}

# 英国UK261
UK261_COMPENSATION = {
    "name": "英国UK261",
    "applies": "从英国机场出发的航班，或英国航司抵达英国的航班",
    "thresholds": [
        {"distance": 1500, "short_delay": 3, "comp_short": 220, "comp_long": 220},
        {"distance": 3500, "short_delay": 3, "comp_short": 350, "comp_long": 350},
        {"distance": float("inf"), "short_delay": 3, "comp_short": 260, "comp_long": 520},
    ],
    "notes": "脱欧后与EU261基本一致，金额为英镑"
}

# 中国民航规定（无强制赔偿，但航司有自愿标准）
CHINA_COMPENSATION = {
    "name": "中国民航局规定",
    "applies": "中国国内航班及中国航司航班",
    "rules": [
        {"delay_min": 120, "type": "餐饮", "desc": "延误2小时以上提供餐饮服务"},
        {"delay_min": 240, "type": "住宿", "desc": "延误4小时以上安排住宿(非旅客原因)"},
        {"delay_min": 480, "type": "补偿", "desc": "延误8小时以上可能获得补偿(非旅客原因)"},
    ],
    "airline_policies": {
        "CA": {"name": "国航", "4-8h": "200元", "8h+": "400元"},
        "MU": {"name": "东航", "4-8h": "200元", "8h+": "400元"},
        "CZ": {"name": "南航", "4-8h": "200元", "8h+": "400元"},
        "HU": {"name": "海航", "4-8h": "200元", "8h+": "400元"},
        "3U": {"name": "川航", "4-8h": "200元", "8h+": "400元"},
        "MF": {"name": "厦航", "4-8h": "200元", "8h+": "400元"},
        "9C": {"name": "春秋", "4-8h": "100元", "8h+": "200元"},
        "HO": {"name": "吉祥", "4-8h": "200元", "8h+": "400元"},
    },
    "notes": "中国暂无法定义务赔偿标准，以上为各航司自愿承诺；天气/空管/安检原因通常不赔"
}

# 加拿大APPR
CANADA_APPR = {
    "name": "加拿大APPR",
    "applies": "从加拿大出发的航班，或抵达加拿大的航班(含中转)",
    "thresholds": [
        {"delay_h": 3, "small_carrier_100m": 0, "large_carrier_100m": 400},
        {"delay_h": 6, "small_carrier_100m": 125, "large_carrier_100m": 700},
        {"delay_h": 9, "small_carrier_100m": 250, "large_carrier_100m": 1000},
    ],
    "notes": "CAD加元；大型航司=年运量>200万乘客；安全相关延误可免责"
}

# 美国DOT
US_DOT = {
    "name": "美国DOT规定",
    "applies": "美国国内航班和国际航班(美国出发)",
    "rules": [
        {"type": "超售拒载", "domestic_comp": "200-775美元", "international_comp": "650-1550美元"},
        {"type": "停机坪延误", "desc": "国内3小时/国际4小时必须让旅客下机"},
    ],
    "notes": "美国无法定义务赔偿航班延误；各航司有自愿政策；超售拒载有赔偿"
}

# 土耳其SHY-YOLCU
TURKEY_SHY = {
    "name": "土耳其SHY-YOLCU",
    "applies": "从土耳其机场出发的航班",
    "thresholds": [
        {"distance": 1500, "comp_3h": 100, "comp_5h": 100},
        {"distance": 3500, "comp_3h": 200, "comp_5h": 200},
        {"distance": float("inf"), "comp_3h": 300, "comp_5h": 300},
    ],
    "notes": "欧元；与EU261类似但金额较低"
}

# 常用机场代码
AIRPORT_CODES = {
    "北京": "PEK", "北京首都": "PEK", "北京大兴": "PKX",
    "上海": "SHA", "上海虹桥": "SHA", "上海浦东": "PVG",
    "广州": "CAN", "深圳": "SZX", "成都": "CTU",
    "杭州": "HGH", "重庆": "CKG", "西安": "XIY",
    "武汉": "WUH", "长沙": "CSX", "南京": "NKG",
    "厦门": "XMN", "昆明": "KMG", "青岛": "TAO",
    "大连": "DLC", "天津": "TSN", "郑州": "CGO",
    "海口": "HAK", "三亚": "SYX", "贵阳": "KWE",
    "哈尔滨": "HRB", "沈阳": "SHE", "长春": "CGQ",
    "福州": "FOC", "济南": "TNA", "太原": "TYN",
    "南宁": "NNG", "兰州": "LHW", "乌鲁木齐": "URC",
    "拉萨": "LXA", "呼和浩特": "HET", "银川": "INC",
    "西宁": "XNN", "石家庄": "SJW", "合肥": "HFE",
    "南昌": "KHN", "温州": "WNZ", "宁波": "NGB",
    "烟台": "YNT", "珠海": "ZUH", "揭阳": "SWA",
    "桂林": "KWL", "丽江": "LJG", "大理": "DLU",
    # 国际
    "东京": "NRT", "东京成田": "NRT", "东京羽田": "HND",
    "大阪": "KIX", "首尔": "ICN", "釜山": "PUS",
    "曼谷": "BKK", "新加坡": "SIN", "吉隆坡": "KUL",
    "河内": "HAN", "胡志明": "SGN", "雅加达": "CGK",
    "马尼拉": "MNL", "金边": "PNH", "暹粒": "REP",
    "巴厘岛": "DPS", "清迈": "CNX", "普吉岛": "HKT",
    "悉尼": "SYD", "墨尔本": "MEL", "奥克兰": "AKL",
    "伦敦": "LHR", "巴黎": "CDG", "法兰克福": "FRA",
    "阿姆斯特丹": "AMS", "莫斯科": "SVO", "罗马": "FCO",
    "纽约": "JFK", "洛杉矶": "LAX", "旧金山": "SFO",
    "芝加哥": "ORD", "迪拜": "DXB", "多伦多": "YYZ",
    "温哥华": "YVR", "伊斯坦布尔": "IST",
}

# 欧盟国家代码
EU_COUNTRIES = {
    "AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR",
    "DE", "GR", "HU", "IE", "IT", "LV", "LT", "LU", "MT", "NL",
    "PL", "PT", "RO", "SK", "SI", "ES", "SE"
}

# 机场所在国家/区域映射（主要国际机场）
AIRPORT_REGION = {
    # 欧盟
    "CDG": "EU", "ORY": "EU", "AMS": "EU", "FRA": "EU", "MUC": "EU",
    "FCO": "EU", "MAD": "EU", "BCN": "EU", "ATH": "EU", "VIE": "EU",
    "BRU": "EU", "CPH": "EU", "DUB": "EU", "LIS": "EU", "PRG": "EU",
    "ARN": "EU", "HEL": "EU", "WAW": "EU", "BUD": "EU", "ZRH": "EU",
    # 英国
    "LHR": "UK", "LGW": "UK", "MAN": "UK", "EDI": "UK", "STN": "UK",
    # 美国
    "JFK": "US", "LAX": "US", "SFO": "US", "ORD": "US", "ATL": "US",
    "DFW": "US", "DEN": "US", "SEA": "US", "MIA": "US", "BOS": "US",
    # 加拿大
    "YYZ": "CA", "YVR": "CA", "YUL": "CA", "YYC": "CA",
    # 土耳其
    "IST": "TR", "AYT": "TR",
    # 中国
    "PEK": "CN", "PKX": "CN", "PVG": "CN", "SHA": "CN", "CAN": "CN",
    "SZX": "CN", "CTU": "CN", "HGH": "CN", "CKG": "CN", "XIY": "CN",
    "WUH": "CN", "CSX": "CN", "NKG": "CN", "XMN": "CN", "KMG": "CN",
    "TAO": "CN", "DLC": "CN", "TSN": "CN", "CGO": "CN", "HAK": "CN",
    "SYX": "CN", "HRB": "CN", "SHE": "CN",
    # 日韩
    "NRT": "JP", "HND": "JP", "KIX": "JP", "ICN": "KR",
    # 东南亚
    "BKK": "TH", "SIN": "SG", "KUL": "MY", "CGK": "ID", "MNL": "PH",
    # 其他
    "DXB": "AE", "SYD": "AU", "MEL": "AU", "SVO": "RU",
}

# 欧盟航司IATA代码前缀
EU_AIRLINE_PREFIXES = {
    "LH": "DE", "DE": "DE",  # 汉莎
    "AF": "FR",  # 法航
    "KL": "NL",  # 荷航
    "BA": "UK",  # 英航
    "IB": "ES",  # 伊比利亚
    "AZ": "IT",  # 意航
    "SK": "DK",  # 北欧
    "OS": "AT",  # 奥航
    "SN": "BE",  # 布鲁塞尔
    "TP": "PT",  # 葡航
    "LO": "PL",  # 波兰航
    "A3": "GR",  # 爱琴海
    "EI": "IE",  # 爱尔兰航
    "FR": "IE",  # 瑞安
    "U2": "UK",  # 易捷
    "VY": "ES",  # 伏林
    "W6": "HU",  # 维兹
    "TK": "TR",  # 土航
}


def _validate_proxy_url(url):
    """校验代理URL是否在白名单域名内"""
    from urllib.parse import urlparse
    parsed = urlparse(url)
    host = parsed.hostname or ""
    return any(host.endswith(allowed) for allowed in _ALLOWED_PROXY_HOSTS)


def _api_request(endpoint, params):
    """通过SCF代理调用飞常准API"""
    if not _validate_proxy_url(SCF_PROXY_URL):
        return {"code": -1, "message": "代理URL校验失败：域名不在白名单中"}

    if not PROXY_TOKEN:
        return {"code": -1, "message": "PROXY_TOKEN未配置"}

    body = json.dumps({
        "type": endpoint,
        "params": params
    }).encode('utf-8')

    req = urllib.request.Request(
        SCF_PROXY_URL,
        data=body,
        headers={
            'X-Proxy-Token': PROXY_TOKEN,
            'Content-Type': 'application/json'
        },
        method='POST'
    )

    ctx = ssl.create_default_context()
    ctx.check_hostname = True
    ctx.verify_mode = ssl.CERT_REQUIRED

    try:
        with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
            result = json.loads(resp.read().decode('utf-8'))
            if result.get("code") == 0:
                return result.get("data", {})
            else:
                return {"code": -1, "message": result.get("error", "代理请求失败")}
    except urllib.error.HTTPError as e:
        return {"code": e.code, "message": f"HTTP {e.code}: {e.reason}"}
    except Exception as e:
        return {"code": -1, "message": str(e)}


def _resolve_airport(code_or_name):
    """解析机场代码"""
    if not code_or_name:
        return None
    code = code_or_name.upper().strip()
    if code in AIRPORT_CODES.values():
        return code
    for name, airport_code in AIRPORT_CODES.items():
        if code_or_name == name:
            return airport_code
    if len(code) == 3 and code.isalpha():
        return code
    return None


def _get_airline_prefix(flight_no):
    """从航班号提取航司前缀"""
    if not flight_no or len(flight_no) < 2:
        return None
    prefix = flight_no[:2].upper()
    if flight_no[0].isdigit():
        prefix = flight_no[:2]
    return prefix


def _calc_delay_minutes(plan_str, actual_str):
    """计算延误分钟数"""
    if not plan_str or not actual_str:
        return None
    try:
        plan = datetime.strptime(plan_str, "%Y-%m-%d %H:%M:%S")
        actual = datetime.strptime(actual_str, "%Y-%m-%d %H:%M:%S")
        delta = (actual - plan).total_seconds() / 60
        return int(delta)
    except (ValueError, TypeError):
        return None


def _determine_jurisdiction(dep_code, arr_code, airline_prefix):
    """判断适用哪个法域的赔偿规则"""
    dep_region = AIRPORT_REGION.get(dep_code, "")
    arr_region = AIRPORT_REGION.get(arr_code, "")
    airline_country = EU_AIRLINE_PREFIXES.get(airline_prefix, "")

    jurisdictions = []

    # EU261: 从欧盟出发，或欧盟航司抵达欧盟
    if dep_region == "EU":
        jurisdictions.append("EU261")
    elif arr_region == "EU" and airline_country in EU_COUNTRIES:
        jurisdictions.append("EU261")

    # UK261: 从英国出发，或英国航司抵达英国
    if dep_region == "UK":
        jurisdictions.append("UK261")
    elif arr_region == "UK" and airline_country == "UK":
        jurisdictions.append("UK261")

    # 加拿大APPR: 从加拿大出发
    if dep_region == "CA":
        jurisdictions.append("CANADA_APPR")

    # 土耳其SHY: 从土耳其出发
    if dep_region == "TR":
        jurisdictions.append("TURKEY_SHY")

    # 中国: 中国国内或中国航司
    if dep_region == "CN" or (arr_region == "CN" and dep_region == ""):
        jurisdictions.append("CHINA")

    # 美国: 从美国出发
    if dep_region == "US":
        jurisdictions.append("US_DOT")

    # 默认
    if not jurisdictions:
        jurisdictions.append("CHINA")  # 默认中国规则

    return jurisdictions


def _estimate_flight_distance_km(dep_code, arr_code):
    """粗略估算飞行距离（基于区域间典型距离）"""
    # 简化版：基于区域对判断大致距离范围
    dep_region = AIRPORT_REGION.get(dep_code, "")
    arr_region = AIRPORT_REGION.get(arr_code, "")

    # 同区域内部
    if dep_region == arr_region:
        if dep_region == "CN":
            return 1200  # 中国国内平均
        elif dep_region == "EU":
            return 1000
        elif dep_region == "US":
            return 1500
        return 800

    # 中日韩
    cn_jp_kr = {"CN", "JP", "KR"}
    if dep_region in cn_jp_kr and arr_region in cn_jp_kr:
        return 1500

    # 中/日韩 ↔ 东南亚
    sea = {"TH", "SG", "MY", "ID", "PH", "VN"}
    if (dep_region in cn_jp_kr and arr_region in sea) or (dep_region in sea and arr_region in cn_jp_kr):
        return 3500

    # 亚洲 ↔ 欧洲
    if (dep_region in cn_jp_kr | sea and arr_region == "EU") or \
       (dep_region == "EU" and arr_region in cn_jp_kr | sea):
        return 8500

    # 亚洲 ↔ 北美
    na = {"US", "CA"}
    if (dep_region in cn_jp_kr | sea and arr_region in na) or \
       (dep_region in na and arr_region in cn_jp_kr | sea):
        return 10000

    # 欧洲 ↔ 北美
    if (dep_region == "EU" and arr_region in na) or (dep_region in na and arr_region == "EU"):
        return 6000

    # 澳洲
    if dep_region == "AU" or arr_region == "AU":
        return 7000

    # 中东
    if dep_region == "AE" or arr_region == "AE":
        return 5500

    return 3000  # 默认中等距离


def _calc_eu261_compensation(distance_km, delay_hours):
    """计算EU261赔偿金额"""
    if delay_hours < 3:
        return 0, "延误不足3小时，不满足EU261赔偿条件"
    
    for threshold in EU261_COMPENSATION["thresholds"]:
        if distance_km <= threshold["distance"]:
            if delay_hours >= 4 or distance_km > 3500:
                return threshold["comp_long"], f"EU261: {distance_km:.0f}km航线，延误{delay_hours}小时"
            else:
                return threshold["comp_short"], f"EU261: {distance_km:.0f}km航线，延误{delay_hours}小时(3-4小时)"
    return 0, ""


def _calc_uk261_compensation(distance_km, delay_hours):
    """计算UK261赔偿金额"""
    if delay_hours < 3:
        return 0, "延误不足3小时，不满足UK261赔偿条件"
    
    for threshold in UK261_COMPENSATION["thresholds"]:
        if distance_km <= threshold["distance"]:
            if delay_hours >= 4 or distance_km > 3500:
                return threshold["comp_long"], f"UK261: {distance_km:.0f}km航线，延误{delay_hours}小时"
            else:
                return threshold["comp_short"], f"UK261: {distance_km:.0f}km航线，延误{delay_hours}小时(3-4小时)"
    return 0, ""


def _calc_china_compensation(airline_prefix, delay_minutes):
    """计算中国航班延误补偿"""
    delay_hours = delay_minutes / 60
    result = []

    # 民航局规定
    for rule in CHINA_COMPENSATION["rules"]:
        if delay_minutes >= rule["delay_min"]:
            result.append(rule)

    # 航司自愿标准
    policy = CHINA_COMPENSATION["airline_policies"].get(airline_prefix)
    if policy:
        if delay_hours >= 4 and delay_hours < 8:
            result.append({"type": "航司补偿", "desc": f"{policy['name']}: {policy.get('4-8h', '未公布')}"})
        elif delay_hours >= 8:
            result.append({"type": "航司补偿", "desc": f"{policy['name']}: {policy.get('8h+', '未公布')}"})

    return result


def _calc_canada_compensation(delay_hours, is_large_carrier=True):
    """计算加拿大APPR赔偿"""
    for threshold in CANADA_APPR["thresholds"]:
        if delay_hours >= threshold["delay_h"]:
            amount = threshold["large_carrier_100m"] if is_large_carrier else threshold["small_carrier_100m"]
            if amount > 0:
                return amount, f"APPR: 延误{delay_hours}小时，{'大型' if is_large_carrier else '小型'}航司"
    return 0, "延误时间不足，不满足APPR赔偿条件"


# ========== 工具1: 延误检查与赔偿评估 ==========
def cmd_check(flight_no, date=None):
    """检查航班延误状态并评估赔偿资格"""
    if not flight_no:
        return json.dumps({"status": "error", "message": "请提供航班号"}, ensure_ascii=False)

    flight_no = flight_no.upper().strip()
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    # 查询航班动态
    result = _api_request("flight", {"fnum": flight_no, "date": date})

    if result.get("code") != 200:
        return json.dumps({
            "status": "error",
            "message": f"查询失败：{result.get('message', '未知错误')}"
        }, ensure_ascii=False)

    flights = result.get("data", [])
    if not flights:
        return json.dumps({
            "status": "empty",
            "message": f"未找到航班 {flight_no}（{date}）的动态"
        }, ensure_ascii=False)

    f = flights[0]
    state = f.get("FlightState", "")
    dep_code = f.get("FlightDepcode", "")
    arr_code = f.get("FlightArrcode", "")
    dep_name = f.get("FlightDep", "")
    arr_name = f.get("FlightArr", "")
    airline_prefix = _get_airline_prefix(flight_no)

    plan_dep = f.get("FlightDeptimePlanDate", "")
    actual_dep = f.get("FlightDeptimeDate", "")
    plan_arr = f.get("FlightArrtimePlanDate", "")
    actual_arr = f.get("FlightArrtimeDate", "")

    dep_delay = _calc_delay_minutes(plan_dep, actual_dep)
    arr_delay = _calc_delay_minutes(plan_arr, actual_arr)

    # 构建输出
    output = f"✈️ **航班延误赔偿评估：{flight_no}**（{date}）\n\n"
    output += f"**航线**：{dep_name}({dep_code}) → {arr_name}({arr_code})\n"

    # 判断延误状态
    is_delayed = state == "延误" or (dep_delay is not None and dep_delay > 30) or (arr_delay is not None and arr_delay > 30)
    is_cancelled = state == "取消"

    if is_cancelled:
        output += f"**状态**：❌ 航班取消\n\n"
        effective_delay = 180  # 取消视为长时间延误
        output += "⚠️ 航班取消也属于赔偿范围！\n\n"
    elif is_delayed:
        max_delay = max(dep_delay or 0, arr_delay or 0)
        output += f"**状态**：⏰ 延误\n"
        if dep_delay and dep_delay > 0:
            output += f"- 出发延误：**{dep_delay}分钟**\n"
        if arr_delay and arr_delay > 0:
            output += f"- 到达延误：**{arr_delay}分钟**\n"
        effective_delay = arr_delay if arr_delay else dep_delay
        output += "\n"
    else:
        output += f"**状态**：✅ 正常/未延误\n\n"
        if state not in ["延误", "取消"] and (dep_delay is None or dep_delay <= 30):
            output += "📋 当前航班状态正常，暂无赔偿资格。如果后续发生延误，可以再次查询。\n"
            return output

    # 判断法域
    jurisdictions = _determine_jurisdiction(dep_code, arr_code, airline_prefix)
    distance_km = _estimate_flight_distance_km(dep_code, arr_code)
    delay_hours = (effective_delay or 0) / 60

    output += "---\n\n## 💰 赔偿评估\n\n"

    for jur in jurisdictions:
        if jur == "EU261":
            amount, detail = _calc_eu261_compensation(distance_km, delay_hours)
            output += f"### 🇪🇺 {EU261_COMPENSATION['name']}\n"
            output += f"**适用**：{EU261_COMPENSATION['applies']}\n\n"
            if amount > 0:
                output += f"✅ **可获赔偿：€{amount}**\n"
                output += f"依据：{detail}\n\n"
            else:
                output += f"❌ {detail}\n\n"
            output += f"📌 {EU261_COMPENSATION['notes']}\n\n"

        elif jur == "UK261":
            amount, detail = _calc_uk261_compensation(distance_km, delay_hours)
            output += f"### 🇬🇧 {UK261_COMPENSATION['name']}\n"
            output += f"**适用**：{UK261_COMPENSATION['applies']}\n\n"
            if amount > 0:
                output += f"✅ **可获赔偿：£{amount}**\n"
                output += f"依据：{detail}\n\n"
            else:
                output += f"❌ {detail}\n\n"
            output += f"📌 {UK261_COMPENSATION['notes']}\n\n"

        elif jur == "CHINA":
            comp_items = _calc_china_compensation(airline_prefix, effective_delay or 0)
            output += f"### 🇨🇳 {CHINA_COMPENSATION['name']}\n"
            output += f"**适用**：{CHINA_COMPENSATION['applies']}\n\n"
            if comp_items:
                output += "**可获得：**\n"
                for item in comp_items:
                    output += f"- **{item['type']}**：{item['desc']}\n"
                output += "\n"
            else:
                output += "❌ 延误时间不足，暂无赔偿资格\n\n"
            output += f"📌 {CHINA_COMPENSATION['notes']}\n\n"

        elif jur == "CANADA_APPR":
            amount, detail = _calc_canada_compensation(delay_hours, is_large_carrier=True)
            output += f"### 🇨🇦 {CANADA_APPR['name']}\n"
            output += f"**适用**：{CANADA_APPR['applies']}\n\n"
            if amount > 0:
                output += f"✅ **可获赔偿：C${amount}**\n"
                output += f"依据：{detail}\n\n"
            else:
                output += f"❌ {detail}\n\n"

        elif jur == "TURKEY_SHY":
            output += f"### 🇹🇷 {TURKEY_SHY['name']}\n"
            output += f"**适用**：{TURKEY_SHY['applies']}\n\n"
            for threshold in TURKEY_SHY["thresholds"]:
                if distance_km <= threshold["distance"]:
                    if delay_hours >= 5:
                        output += f"✅ **可获赔偿：€{threshold['comp_5h']}**（延误5h+）\n"
                    elif delay_hours >= 3:
                        output += f"✅ **可获赔偿：€{threshold['comp_3h']}**（延误3-5h）\n"
                    else:
                        output += "❌ 延误不足3小时\n"
                    break
            output += f"\n📌 {TURKEY_SHY['notes']}\n\n"

        elif jur == "US_DOT":
            output += f"### 🇺🇸 {US_DOT['name']}\n"
            output += f"**适用**：{US_DOT['applies']}\n\n"
            output += "⚠️ 美国没有法定延误赔偿，但以下情况有赔偿：\n"
            for rule in US_DOT["rules"]:
                output += f"- **{rule['type']}**：{rule.get('desc', rule.get('domestic_comp', ''))}\n"
            output += f"\n📌 {US_DOT['notes']}\n\n"

    # 索赔指引
    output += "---\n\n## 📝 索赔指引\n\n"
    output += "1. **保留证据**：保存登机牌、行程单、延误/取消通知截图\n"
    output += "2. **现场索取**：在机场向航司柜台索取延误/取消证明\n"
    output += "3. **在线索赔**：大多数航司官网有在线索赔入口\n"
    output += "4. **第三方索赔**：可使用 ClaimAir / AirHelp / refund.me 等服务（抽成15-30%）\n"
    output += "5. **投诉渠道**：\n"
    if "EU261" in jurisdictions:
        output += "   - 欧盟：向航班出发国的国家执法机构(NEB)投诉\n"
    if "UK261" in jurisdictions:
        output += "   - 英国：向民航局(CAA)投诉\n"
    if "CHINA" in jurisdictions:
        output += "   - 中国：拨打12326民航服务质量监督电话\n"
    if "CANADA_APPR" in jurisdictions:
        output += "   - 加拿大：向加拿大交通局(CTA)投诉\n"
    output += "\n💡 **提示**：直接向航司索赔最划算，无需给第三方抽成！\n"

    return output


# ========== 工具2: 赔偿规则查询 ==========
def cmd_rules(region=None):
    """查询各国/地区航班延误赔偿规则"""
    regions = {
        "eu": ("🇪🇺 欧盟EU261/2004", EU261_COMPENSATION),
        "uk": ("🇬🇧 英国UK261", UK261_COMPENSATION),
        "china": ("🇨🇳 中国民航规定", CHINA_COMPENSATION),
        "canada": ("🇨🇦 加拿大APPR", CANADA_APPR),
        "us": ("🇺🇸 美国DOT规定", US_DOT),
        "turkey": ("🇹🇷 土耳其SHY-YOLCU", TURKEY_SHY),
    }

    if region:
        region = region.lower().strip()
        if region not in regions:
            return json.dumps({
                "status": "error",
                "message": f"未知地区: {region}。支持: eu, uk, china, canada, us, turkey"
            }, ensure_ascii=False)
        display_regions = {region: regions[region]}
    else:
        display_regions = regions

    output = "📋 **航班延误赔偿规则大全**\n\n"

    for key, (title, data) in display_regions.items():
        output += f"## {title}\n\n"
        output += f"**适用范围**：{data['applies']}\n\n"

        if key == "eu":
            output += "| 航线距离 | 延误≥3小时 | 延误≥4小时(长途) |\n|----------|-----------|----------------|\n"
            output += f"| ≤1500km | €250 | €250 |\n"
            output += f"| 1500-3500km | €400 | €400 |\n"
            output += f"| >3500km | €300 | €600 |\n\n"

        elif key == "uk":
            output += "| 航线距离 | 延误≥3小时 | 延误≥4小时(长途) |\n|----------|-----------|----------------|\n"
            output += f"| ≤1500km | £220 | £220 |\n"
            output += f"| 1500-3500km | £350 | £350 |\n"
            output += f"| >3500km | £260 | £520 |\n\n"

        elif key == "china":
            output += "**民航局规定：**\n\n"
            for rule in data["rules"]:
                output += f"- 延误≥{rule['delay_min']//60}小时：{rule['type']} - {rule['desc']}\n"
            output += "\n**主要航司自愿补偿标准：**\n\n"
            output += "| 航司 | 延误4-8小时 | 延误8小时以上 |\n|------|------------|-------------|\n"
            for prefix, policy in data["airline_policies"].items():
                output += f"| {policy['name']} | {policy.get('4-8h', '未公布')} | {policy.get('8h+', '未公布')} |\n"
            output += "\n"

        elif key == "canada":
            output += "| 延误时长 | 小型航司 | 大型航司 |\n|---------|---------|--------|\n"
            for t in data["thresholds"]:
                output += f"| ≥{t['delay_h']}小时 | C${t['small_carrier_100m']} | C${t['large_carrier_100m']} |\n"
            output += "\n"

        elif key == "us":
            for rule in data["rules"]:
                output += f"- **{rule['type']}**：{rule.get('desc', rule.get('domestic_comp', ''))}\n"
            output += "\n"

        elif key == "turkey":
            output += "| 航线距离 | 延误3-5小时 | 延误≥5小时 |\n|----------|-----------|------------|\n"
            for t in data["thresholds"]:
                d = f"≤{t['distance']}" if t['distance'] != float('inf') else ">3500km"
                output += f"| {d} | €{t['comp_3h']} | €{t['comp_5h']} |\n"
            output += "\n"

        output += f"📌 {data['notes']}\n\n"
        output += "---\n\n"

    return output


# ========== 工具3: 索赔信生成 ==========
def cmd_claim(flight_no, date=None, passenger_name="旅客"):
    """生成索赔信模板"""
    if not flight_no:
        return json.dumps({"status": "error", "message": "请提供航班号"}, ensure_ascii=False)

    flight_no = flight_no.upper().strip()
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    # 查询航班信息
    result = _api_request("flight", {"fnum": flight_no, "date": date})
    
    dep_name = "出发地"
    arr_name = "目的地"
    airline_name = "航空公司"
    plan_dep = "计划时间"
    actual_dep = "实际时间"
    delay_min = 0
    jurisdictions = []
    
    if result.get("code") == 200:
        flights = result.get("data", [])
        if flights:
            f = flights[0]
            dep_name = f.get("FlightDep", dep_name)
            arr_name = f.get("FlightArr", arr_name)
            plan_dep = f.get("FlightDeptimePlanDate", plan_dep)
            actual_dep = f.get("FlightDeptimeDate", actual_dep)
            dep_code = f.get("FlightDepcode", "")
            arr_code = f.get("FlightArrcode", "")
            airline_prefix = _get_airline_prefix(flight_no)
            jurisdictions = _determine_jurisdiction(dep_code, arr_code, airline_prefix)
            delay_min = _calc_delay_minutes(plan_dep, actual_dep) or 0

    delay_hours = delay_min / 60

    # 根据法域选择索赔法规引用
    if "EU261" in jurisdictions:
        law_ref = "EU Regulation 261/2004"
        currency = "EUR"
        distance_km = _estimate_flight_distance_km(
            flights[0].get("FlightDepcode", "") if result.get("code") == 200 and flights else "",
            flights[0].get("FlightArrcode", "") if result.get("code") == 200 and flights else ""
        ) if result.get("code") == 200 and flights else 0
        amount, _ = _calc_eu261_compensation(distance_km, delay_hours)
        claim_amount = f"€{amount}"
    elif "UK261" in jurisdictions:
        law_ref = "UK261 (The Civil Aviation (Denied Boarding, Compensation and Assistance) Regulations 2005)"
        currency = "GBP"
        claim_amount = "£[根据距离计算]"
    elif "CANADA_APPR" in jurisdictions:
        law_ref = "Canada APPR (Air Passenger Protection Regulations)"
        currency = "CAD"
        claim_amount = "C$[根据延误时长计算]"
    elif "CHINA" in jurisdictions:
        law_ref = "《航班延误经济补偿指导意见》及贵司运输总条件"
        currency = "CNY"
        claim_amount = "[根据贵司标准]"
    else:
        law_ref = "相关航空法规"
        currency = "CNY"
        claim_amount = "[根据适用法规]"

    today = datetime.now().strftime("%Y年%m月%d日")

    output = f"""✉️ **索赔信模板**

---

**致：{airline_name} 客户服务部**

**日期**：{today}

**主题**：航班 {flight_no} 延误赔偿索赔

尊敬的 {airline_name}：

我是 {flight_no} 航班的乘客 {passenger_name}，该航班于 {date} 从 {dep_name} 飞往 {arr_name}。

**航班详情：**
- 航班号：{flight_no}
- 日期：{date}
- 航线：{dep_name} → {arr_name}
- 计划出发时间：{plan_dep}
- 实际出发时间：{actual_dep}
- 延误时长：{delay_min}分钟（{delay_hours:.1f}小时）

根据 {law_ref}，我有权获得延误赔偿。

**索赔金额：{claim_amount}**

**附件：**
1. 登机牌复印件
2. 航班延误证明
3. 身份证明复印件

请在收到本信后 **30天内** 予以回复。如未能满意解决，我将向相关航空监管机构提出投诉。

此致，

{passenger_name}
[联系电话]
[电子邮箱]
[通讯地址]

---

💡 **使用建议**：
1. 替换方括号中的信息
2. 附上登机牌和延误证明
3. 通过航司官网索赔入口或邮寄提交
4. 保留提交记录和回执
"""
    return output


# ========== 主入口 ==========
def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "status": "error",
            "message": "用法: flight_delay_compensation.py <command> [args]\n命令: check <航班号> [日期] | rules [地区] | claim <航班号> [日期]"
        }, ensure_ascii=False))
        return

    command = sys.argv[1]

    if command == "check":
        if len(sys.argv) < 3:
            print(json.dumps({"status": "error", "message": "请提供航班号，如 CA1507"}, ensure_ascii=False))
            return
        flight_no = sys.argv[2]
        date = sys.argv[3] if len(sys.argv) > 3 else None
        print(cmd_check(flight_no, date))

    elif command == "rules":
        region = sys.argv[2] if len(sys.argv) > 2 else None
        print(cmd_rules(region))

    elif command == "claim":
        if len(sys.argv) < 3:
            print(json.dumps({"status": "error", "message": "请提供航班号"}, ensure_ascii=False))
            return
        flight_no = sys.argv[2]
        date = sys.argv[3] if len(sys.argv) > 3 else None
        name = sys.argv[4] if len(sys.argv) > 4 else "旅客"
        print(cmd_claim(flight_no, date, name))

    else:
        print(json.dumps({
            "status": "error",
            "message": f"未知命令: {command}\n支持: check | rules | claim"
        }, ensure_ascii=False))


if __name__ == "__main__":
    main()
