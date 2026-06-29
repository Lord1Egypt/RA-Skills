#!/usr/bin/env python3
"""机场贵宾厅查询 - Airport Lounge Finder
查询全球主要机场贵宾厅信息，包括准入条件、信用卡权益、航司会员等级等
纯本地数据，无需外部API
"""
import json
import sys

# ========== 机场贵宾厅数据库 ==========

# 主要机场贵宾厅数据
LOUNGES = [
    # ===== 中国 =====
    {"airport": "PEK", "airport_name": "北京首都", "lounge": "国航头等舱休息室", "terminal": "T3", "location": "T3-E 三层", "type": "航司自营", "access": ["国航头等舱", "国航白金卡", "星空联盟金卡"], "features": ["餐食", "淋浴", "休息区", "办公区"], "rating": 4.5},
    {"airport": "PEK", "airport_name": "北京首都", "lounge": "国航贵宾休息室", "terminal": "T3", "location": "T3-C 二层", "type": "航司自营", "access": ["国航商务舱", "国航金卡", "星空联盟金卡"], "features": ["餐食", "休息区", "办公区"], "rating": 4.0},
    {"airport": "PEK", "airport_name": "北京首都", "lounge": "首都机场贵宾厅", "terminal": "T3", "location": "T3-E 安检后", "type": "机场自营", "access": ["招商银行百夫长", "浦发美国运通超白金", "龙腾出行", "PP卡"], "features": ["餐食", "淋浴", "休息区", "按摩椅"], "rating": 3.8},
    {"airport": "PKX", "airport_name": "北京大兴", "lounge": "南航明珠休息室", "terminal": "主楼", "location": "四层安检后", "type": "航司自营", "access": ["南航头等舱", "南航金卡", "天合联盟超级精英"], "features": ["餐食", "淋浴", "休息区"], "rating": 4.2},
    
    {"airport": "PVG", "airport_name": "上海浦东", "lounge": "东航贵宾室", "terminal": "T1", "location": "T1 国际/地区安检后", "type": "航司自营", "access": ["东航头等舱", "东航白金卡", "天合联盟超级精英"], "features": ["餐食", "淋浴", "休息区", "面档"], "rating": 4.3},
    {"airport": "PVG", "airport_name": "上海浦东", "lounge": "浦东机场V8贵宾厅", "terminal": "T2", "location": "T2 安检后", "type": "机场自营", "access": ["龙腾出行", "PP卡", "招行百夫长", "工行白金"], "features": ["餐食", "淋浴", "休息区"], "rating": 3.5},
    {"airport": "SHA", "airport_name": "上海虹桥", "lounge": "东航贵宾室", "terminal": "T2", "location": "T2 安检后", "type": "航司自营", "access": ["东航头等舱", "东航金卡", "天合联盟超级精英"], "features": ["餐食", "休息区"], "rating": 4.0},
    
    {"airport": "CAN", "airport_name": "广州白云", "lounge": "南航明珠休息室", "terminal": "T2", "location": "T2 安检后三层", "type": "航司自营", "access": ["南航头等舱", "南航金卡", "天合联盟超级精英"], "features": ["餐食", "淋浴", "休息区", "面档"], "rating": 4.4},
    {"airport": "CAN", "airport_name": "广州白云", "lounge": "白云机场贵宾厅", "terminal": "T1", "location": "T1 安检后", "type": "机场自营", "access": ["龙腾出行", "PP卡", "广发白金"], "features": ["餐食", "休息区"], "rating": 3.5},
    
    {"airport": "SZX", "airport_name": "深圳宝安", "lounge": "深圳机场贵宾厅", "terminal": "T3", "location": "T3 安检后", "type": "机场自营", "access": ["龙腾出行", "PP卡", "招行白金", "平安白金"], "features": ["餐食", "淋浴", "休息区"], "rating": 3.8},
    
    {"airport": "CTU", "airport_name": "成都天府", "lounge": "川航贵宾室", "terminal": "T1", "location": "T1 安检后", "type": "航司自营", "access": ["川航头等舱", "川航金卡"], "features": ["餐食", "休息区", "川味小吃"], "rating": 4.0},
    {"airport": "CKG", "airport_name": "重庆江北", "lounge": "重庆机场贵宾厅", "terminal": "T3", "location": "T3 安检后", "type": "机场自营", "access": ["龙腾出行", "PP卡"], "features": ["餐食", "休息区"], "rating": 3.5},

    # ===== 日本 =====
    {"airport": "NRT", "airport_name": "东京成田", "lounge": "ANA Lounge", "terminal": "T1", "location": "T1 4F 南翼", "type": "航司自营", "access": ["ANA头等舱", "ANA白金/金卡", "星空联盟金卡"], "features": ["餐食", "淋浴", "休息区", "面条吧"], "rating": 4.3},
    {"airport": "NRT", "airport_name": "东京成田", "lounge": "JAL Sakura Lounge", "terminal": "T2", "location": "T2 3F 本馆", "type": "航司自营", "access": ["JAL头等舱", "JAL钻石/蓝宝石", "寰宇一家蓝宝石/绿宝石"], "features": ["餐食", "淋浴", "休息区", "咖喱饭"], "rating": 4.2},
    {"airport": "NRT", "airport_name": "东京成田", "lounge": "IASS Executive Lounge", "terminal": "T1", "location": "T1 4F", "type": "独立休息室", "access": ["PP卡", "龙腾出行", "Diners Club", "JCB金卡+"], "features": ["饮品", "小吃", "休息区"], "rating": 3.2},
    {"airport": "HND", "airport_name": "东京羽田", "lounge": "ANA SUITE LOUNGE", "terminal": "国际", "location": "国际线4F", "type": "航司自营", "access": ["ANA头等舱", "ANA白金卡"], "features": ["顶级餐食", "淋浴", "独立休息区"], "rating": 4.7},
    
    # ===== 韩国 =====
    {"airport": "ICN", "airport_name": "首尔仁川", "lounge": "KAL Business Lounge", "terminal": "T1", "location": "T1 4F", "type": "航司自营", "access": ["大韩头等/商务舱", "天合联盟超级精英"], "features": ["餐食", "淋浴", "休息区", "泡面吧"], "rating": 4.1},
    {"airport": "ICN", "airport_name": "首尔仁川", "lounge": "Asiana Business Lounge", "terminal": "T1", "location": "T1 东侧4F", "type": "航司自营", "access": ["韩亚商务舱", "星空联盟金卡"], "features": ["餐食", "淋浴", "休息区"], "rating": 4.0},
    {"airport": "ICN", "airport_name": "首尔仁川", "lounge": "Sky Hub Lounge", "terminal": "T1", "location": "T1 4F 中央", "type": "独立休息室", "access": ["PP卡", "龙腾出行", "Priority Pass"], "features": ["餐食", "休息区"], "rating": 3.5},
    
    # ===== 东南亚 =====
    {"airport": "SIN", "airport_name": "新加坡樟宜", "lounge": "SATS Lounge", "terminal": "T1", "location": "T1 3F 过境区", "type": "独立休息室", "access": ["PP卡", "龙腾出行"], "features": ["餐食", "淋浴", "休息区"], "rating": 3.8},
    {"airport": "SIN", "airport_name": "新加坡樟宜", "lounge": "银刃贵宾室(KrisFlyer Gold)", "terminal": "T2", "location": "T2 3F 过境区", "type": "航司自营", "access": ["新航金卡", "星空联盟金卡"], "features": ["餐食", "淋浴", "休息区"], "rating": 4.2},
    {"airport": "BKK", "airport_name": "曼谷素万那普", "lounge": "泰航Royal Silk Lounge", "terminal": "T1", "location": "Concourse D 3F", "type": "航司自营", "access": ["泰航头等/商务舱", "泰航金卡", "星空联盟金卡"], "features": ["餐食", "淋浴", "休息区", "按摩"], "rating": 4.3},
    {"airport": "BKK", "airport_name": "曼谷素万那普", "lounge": "Louis Tavern Lounge", "terminal": "T1", "location": "Concourse G 3F", "type": "独立休息室", "access": ["PP卡", "龙腾出行"], "features": ["餐食", "休息区"], "rating": 3.3},
    {"airport": "KUL", "airport_name": "吉隆坡", "lounge": "Malaysia Airlines Golden Lounge", "terminal": "T1", "location": "卫星楼 Level 2", "type": "航司自营", "access": ["马航商务舱", "马航金卡", "寰宇一家蓝宝石"], "features": ["餐食", "淋浴", "休息区"], "rating": 4.0},
    
    # ===== 欧洲 =====
    {"airport": "LHR", "airport_name": "伦敦希思罗", "lounge": "British Airways Galleries Lounge", "terminal": "T5", "location": "T5 南翼", "type": "航司自营", "access": ["英航商务舱", "英航金/银卡", "寰宇一家蓝宝石/绿宝石"], "features": ["餐食", "淋浴", "酒水吧", "spa"], "rating": 4.4},
    {"airport": "LHR", "airport_name": "伦敦希思罗", "lounge": "SkyTeam Lounge", "terminal": "T4", "location": "T4 安检后", "type": "联盟自营", "access": ["天合联盟超级精英", "天合联盟商务舱"], "features": ["餐食", "淋浴", "休息区"], "rating": 4.0},
    {"airport": "CDG", "airport_name": "巴黎戴高乐", "lounge": "Air France La Première Lounge", "terminal": "T2E", "location": "T2E Hall L", "type": "航司自营", "access": ["法航La Première头等舱"], "features": ["米其林餐食", "spa", "私人套间"], "rating": 4.9},
    {"airport": "CDG", "airport_name": "巴黎戴高乐", "lounge": "Air France Business Lounge", "terminal": "T2E", "location": "T2E Hall K/L", "type": "航司自营", "access": ["法航商务舱", "天合联盟超级精英"], "features": ["餐食", "淋浴", "休息区", "酒水吧"], "rating": 4.1},
    {"airport": "FRA", "airport_name": "法兰克福", "lounge": "Lufthansa First Class Lounge", "terminal": "T1", "location": "T1 出港层", "type": "航司自营", "access": ["汉莎头等舱", "HON Circle会员"], "features": ["顶级餐食", "独立浴室", "雪茄吧"], "rating": 4.8},
    {"airport": "FRA", "airport_name": "法兰克福", "lounge": "Lufthansa Senator Lounge", "terminal": "T1", "location": "T1 出港层", "type": "航司自营", "access": ["汉莎金卡", "星空联盟金卡"], "features": ["餐食", "淋浴", "休息区", "酒吧"], "rating": 4.3},
    {"airport": "AMS", "airport_name": "阿姆斯特丹", "lounge": "KLM Crown Lounge", "terminal": "T2", "location": "T2 安检后", "type": "航司自营", "access": ["荷航商务舱", "天合联盟超级精英"], "features": ["餐食", "淋浴", "休息区"], "rating": 4.2},
    
    # ===== 中东 =====
    {"airport": "DXB", "airport_name": "迪拜", "lounge": "Emirates First Class Lounge", "terminal": "T3", "location": "T3 Concourse A", "type": "航司自营", "access": ["阿联酋头等舱"], "features": ["自助餐", "spa", "淋浴", "商务中心", "酒吧"], "rating": 4.8},
    {"airport": "DXB", "airport_name": "迪拜", "lounge": "Emirates Business Class Lounge", "terminal": "T3", "location": "T3 Concourse B", "type": "航司自营", "access": ["阿联酋商务舱", "Skywards金/银卡"], "features": ["自助餐", "淋浴", "休息区"], "rating": 4.4},
    {"airport": "IST", "airport_name": "伊斯坦布尔", "lounge": "Turkish Airlines Lounge Business", "terminal": "国际", "location": "国际出发层", "type": "航司自营", "access": ["土航商务舱", "Miles&Smiles金卡", "星空联盟金卡"], "features": ["土耳其特色餐", "淋浴", "休息区", "台球"], "rating": 4.5},
    
    # ===== 北美 =====
    {"airport": "JFK", "airport_name": "纽约肯尼迪", "lounge": "Delta Sky Club", "terminal": "T4", "location": "T4 安检后", "type": "航司自营", "access": ["达美商务舱", "Delta 360/钻石/白金卡", "Amex Delta Reserve卡"], "features": ["餐食", "酒吧", "淋浴", "休息区"], "rating": 4.2},
    {"airport": "JFK", "airport_name": "纽约肯尼迪", "lounge": "AA Flagship Lounge", "terminal": "T8", "location": "T8 安检后", "type": "航司自营", "access": ["美航头等/商务舱", "寰宇一方蓝宝石/绿宝石"], "features": ["餐食", "酒水", "休息区"], "rating": 4.0},
    {"airport": "LAX", "airport_name": "洛杉矶", "lounge": "Star Alliance Lounge", "terminal": "TBIT", "location": "TBIT 安检后", "type": "联盟自营", "access": ["星空联盟金卡", "星空联盟商务舱"], "features": ["餐食", "淋浴", "露天露台", "酒吧"], "rating": 4.3},
    {"airport": "SFO", "airport_name": "旧金山", "lounge": "United Polaris Lounge", "terminal": "T3", "location": "T3 安检后", "type": "航司自营", "access": ["联合商务舱", "联合1K/白金卡"], "features": ["餐食", "淋浴", "休息舱", "酒吧"], "rating": 4.5},
    {"airport": "YYZ", "airport_name": "多伦多", "lounge": "Air Canada Maple Leaf Lounge", "terminal": "T1", "location": "T1 国际出发", "type": "航司自营", "access": ["加航商务舱", "星空联盟金卡", "Aeroplan超级精英"], "features": ["餐食", "淋浴", "休息区"], "rating": 4.0},
    
    # ===== 澳洲 =====
    {"airport": "SYD", "airport_name": "悉尼", "lounge": "Qantas First Lounge", "terminal": "国际", "location": "国际出发层", "type": "航司自营", "access": ["澳航头等舱", "澳航白金卡", "寰宇一方绿宝石"], "features": ["Neil Perry餐厅", "spa", "淋浴"], "rating": 4.7},
    {"airport": "SYD", "airport_name": "悉尼", "lounge": "Qantas Business Lounge", "terminal": "国际", "location": "国际出发层", "type": "航司自营", "access": ["澳航商务舱", "澳航金卡", "寰宇一方蓝宝石"], "features": ["自助餐", "淋浴", "酒吧"], "rating": 4.2},
]

# 信用卡权益数据
CREDIT_CARDS = [
    {"name": "招商银行百夫长白金卡", "access": ["PP卡", "龙腾出行"], "annual_pp": 10, "annual_lt": 6, "note": "PP每年10次+龙腾6次，附属卡各一半"},
    {"name": "浦发美国运通超白金卡", "access": ["PP卡", "龙腾出行"], "annual_pp": 99, "annual_lt": 0, "note": "无限PP卡（每年99次封顶）"},
    {"name": "工商银行白金卡", "access": ["龙腾出行"], "annual_lt": 6, "note": "龙腾每年6次"},
    {"name": "建设银行白金卡", "access": ["龙腾出行"], "annual_lt": 6, "note": "龙腾每年6次"},
    {"name": "广发银行白金卡", "access": ["PP卡", "龙腾出行"], "annual_pp": 2, "annual_lt": 4, "note": "PP2次+龙腾4次"},
    {"name": "交通银行白金卡", "access": ["龙腾出行"], "annual_lt": 6, "note": "龙腾每年6次"},
    {"name": "平安银行白金卡", "access": ["龙腾出行"], "annual_lt": 6, "note": "龙腾每年6次"},
    {"name": "中信银行美国运通白金卡", "access": ["PP卡", "龙腾出行"], "annual_pp": 8, "annual_lt": 0, "note": "PP每年8次"},
    {"name": "Amex Platinum (美国)", "access": ["PP卡", "Centurion Lounge", "Delta Sky Club"], "annual_pp": 99, "note": "Centurion Lounge无限+PP每年99次+Delta Sky Club"},
    {"name": "Chase Sapphire Reserve", "access": ["PP卡"], "annual_pp": 99, "note": "PP每年99次"},
    {"name": "Citi Prestige", "access": ["PP卡"], "annual_pp": 99, "note": "PP每年99次"},
]

# 机场代码映射（复用）
AIRPORT_NAMES = {
    "PEK": "北京首都", "PKX": "北京大兴", "PVG": "上海浦东", "SHA": "上海虹桥",
    "CAN": "广州白云", "SZX": "深圳宝安", "CTU": "成都天府", "HGH": "杭州萧山",
    "CKG": "重庆江北", "XIY": "西安咸阳", "WUH": "武汉天河", "CSX": "长沙黄花",
    "NKG": "南京禄口", "XMN": "厦门高崎", "KMG": "昆明长水", "TAO": "青岛胶东",
    "DLC": "大连周水子", "TSN": "天津滨海", "CGO": "郑州新郑",
    "HAK": "海口美兰", "SYX": "三亚凤凰",
    "HRB": "哈尔滨太平", "SHE": "沈阳桃仙",
    # 国际
    "NRT": "东京成田", "HND": "东京羽田", "KIX": "大阪关西",
    "ICN": "首尔仁川", "GMP": "首尔金浦",
    "BKK": "曼谷素万那普", "SIN": "新加坡樟宜", "KUL": "吉隆坡",
    "LHR": "伦敦希思罗", "CDG": "巴黎戴高乐", "FRA": "法兰克福",
    "AMS": "阿姆斯特丹", "IST": "伊斯坦布尔",
    "DXB": "迪拜", "JFK": "纽约肯尼迪", "LAX": "洛杉矶",
    "SFO": "旧金山", "ORD": "芝加哥奥黑尔", "YYZ": "多伦多皮尔逊",
    "SYD": "悉尼", "MEL": "墨尔本",
}


def _resolve_airport(query):
    """解析机场代码或名称"""
    if not query:
        return None
    q = query.strip().upper()
    # 直接是机场代码
    if q in AIRPORT_NAMES:
        return q
    # 中文名查找
    for code, name in AIRPORT_NAMES.items():
        if query.strip() == name:
            return code
    # 模糊匹配
    for code, name in AIRPORT_NAMES.items():
        if query.strip() in name:
            return code
    return None


def cmd_search(airport):
    """查询指定机场的贵宾厅列表"""
    code = _resolve_airport(airport)
    if not code:
        return json.dumps({
            "status": "error",
            "message": f"无法识别机场：{airport}。请使用机场代码(如PEK、PVG)或中文机场名"
        }, ensure_ascii=False)

    airport_lounges = [l for l in LOUNGES if l["airport"] == code]
    if not airport_lounges:
        return json.dumps({
            "status": "empty",
            "message": f"暂无{airport}机场的贵宾厅数据，持续更新中"
        }, ensure_ascii=False)

    airport_name = AIRPORT_NAMES.get(code, code)
    output = f"🏢 **{airport_name}机场贵宾厅**（共{len(airport_lounges)}个）\n\n"

    for i, l in enumerate(airport_lounges):
        rating_stars = "⭐" * int(l["rating"]) + ("½" if l["rating"] % 1 >= 0.5 else "")
        output += f"### {i+1}. {l['lounge']}\n"
        output += f"**位置**：{l['terminal']} · {l['location']}\n\n"
        output += f"**类型**：{l['type']} | **评分**：{rating_stars} {l['rating']}\n\n"
        output += f"**准入条件**：\n"
        for a in l["access"]:
            output += f"  - {a}\n"
        output += f"\n**设施**：{' · '.join(l['features'])}\n\n"
        output += "---\n\n"

    return output


def cmd_card(card_name=None):
    """查询信用卡贵宾厅权益"""
    if card_name:
        # 搜索匹配的卡
        matched = [c for c in CREDIT_CARDS if card_name in c["name"]]
        if not matched:
            # 模糊搜索
            matched = [c for c in CREDIT_CARDS if any(word in c["name"] for word in card_name.split())]
    else:
        matched = CREDIT_CARDS

    if not matched:
        return json.dumps({
            "status": "empty",
            "message": f"未找到'{card_name}'的权益信息"
        }, ensure_ascii=False)

    output = "💳 **信用卡贵宾厅权益**\n\n"

    for c in matched:
        output += f"### {c['name']}\n\n"
        output += f"**权益**：{'、'.join(c['access'])}\n\n"
        if c.get("annual_pp"):
            output += f"- PP卡：每年{c['annual_pp']}次\n"
        if c.get("annual_lt"):
            output += f"- 龙腾出行：每年{c['annual_lt']}次\n"
        output += f"\n📌 {c.get('note', '')}\n\n"
        output += "---\n\n"

    return output


def cmd_access(method):
    """按准入方式查询可用贵宾厅"""
    if not method:
        return json.dumps({
            "status": "error",
            "message": "请提供准入方式，如 PP卡、龙腾出行、星空联盟金卡、天合联盟超级精英 等"
        }, ensure_ascii=False)

    matched = [l for l in LOUNGES if any(method in a for a in l["access"])]

    if not matched:
        return json.dumps({
            "status": "empty",
            "message": f"未找到支持'{method}'准入方式的贵宾厅"
        }, ensure_ascii=False)

    # 按机场分组
    by_airport = {}
    for l in matched:
        code = l["airport"]
        if code not in by_airport:
            by_airport[code] = []
        by_airport[code].append(l)

    output = f"🔑 **支持「{method}」的贵宾厅**（共{len(matched)}个）\n\n"

    for code, lounges in sorted(by_airport.items()):
        airport_name = AIRPORT_NAMES.get(code, code)
        output += f"### {airport_name}（{code}）— {len(lounges)}个\n\n"
        for l in lounges:
            output += f"- **{l['lounge']}** {l['terminal']} | {l['type']} | ⭐{l['rating']}\n"
        output += "\n"

    return output


# ========== 主入口 ==========
def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "status": "error",
            "message": "用法: airport_lounge_finder.py <command> [args]\n命令: search <机场代码/名称> | card [信用卡名] | access <准入方式>"
        }, ensure_ascii=False))
        return

    command = sys.argv[1]

    if command == "search":
        if len(sys.argv) < 3:
            print(json.dumps({"status": "error", "message": "请提供机场代码或名称，如 PEK、上海浦东"}, ensure_ascii=False))
            return
        print(cmd_search(sys.argv[2]))

    elif command == "card":
        card = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else None
        print(cmd_card(card))

    elif command == "access":
        if len(sys.argv) < 3:
            print(json.dumps({"status": "error", "message": "请提供准入方式，如 PP卡、龙腾出行"}, ensure_ascii=False))
            return
        method = " ".join(sys.argv[2:])
        print(cmd_access(method))

    else:
        print(json.dumps({
            "status": "error",
            "message": f"未知命令: {command}\n支持: search | card | access"
        }, ensure_ascii=False))


if __name__ == "__main__":
    main()
