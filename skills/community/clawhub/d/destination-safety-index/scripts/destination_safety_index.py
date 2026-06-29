#!/usr/bin/env python3
"""目的地安全指数 - Destination Safety Index
查询旅行目的地安全评级，包括犯罪率、恐怖袭击风险、自然灾害、健康风险、交通安全等
纯本地数据，综合多源公开信息整理
"""
import json
import sys

# ========== 安全指数数据库 ==========
# 评分 1-10，10最安全，参考：Global Peace Index、US DOS、FCDO、Numbeo等

DESTINATIONS = {
    # ===== 东亚 =====
    "日本": {
        "overall": 9.2, "crime": 9.5, "terror": 9.0, "natural": 7.0, "health": 9.0, "traffic": 8.5,
        "level": "🟢 极安全",
        "risks": ["地震风险（东京/大阪位于地震带）", "台风季6-10月", "夏季高温中暑"],
        "tips": ["日本是全球最安全国家之一", "夜间独行安全", "紧急电话110(警察)/119(急救)", "公共场所免费WiFi"],
        "advisory": "无需特别注意，正常旅行即可",
    },
    "韩国": {
        "overall": 8.8, "crime": 8.5, "terror": 8.0, "natural": 8.5, "health": 9.0, "traffic": 8.5,
        "level": "🟢 极安全",
        "risks": ["朝韩边境局势偶有紧张", "台风季7-9月", "冬季严寒"],
        "tips": ["韩国治安良好", "首尔地铁深夜运营", "紧急电话112(警察)/119(急救)"],
        "advisory": "无需特别注意，避开DMZ附近区域即可",
    },
    "中国": {
        "overall": 8.0, "crime": 8.5, "terror": 8.5, "natural": 7.0, "health": 7.5, "traffic": 6.5,
        "level": "🟢 安全",
        "risks": ["交通事故率较高", "夏季洪涝/台风", "空气质量（北方冬季）"],
        "tips": ["大城市治安良好", "夜间出行注意偏僻区域", "紧急电话110(警察)/120(急救)", "支付宝/微信支付全覆盖"],
        "advisory": "整体安全，注意交通出行安全",
    },

    # ===== 东南亚 =====
    "泰国": {
        "overall": 6.8, "crime": 6.5, "terror": 6.0, "natural": 7.0, "health": 6.5, "traffic": 5.5,
        "level": "🟡 较安全",
        "risks": ["南部三府(也拉/北大年/那拉提瓦)恐怖袭击", "交通事故率高", "旅游景点扒窃", "登革热"],
        "tips": ["主要旅游区(曼谷/清迈/普吉)安全", "远离南部边境三府", "租摩托车务必戴头盔", "紧急电话191(警察)/1669(急救)"],
        "advisory": "旅游区安全，避开南部边境地区，注意交通安全",
    },
    "新加坡": {
        "overall": 9.5, "crime": 9.5, "terror": 8.5, "natural": 9.0, "health": 9.5, "traffic": 9.5,
        "level": "🟢 极安全",
        "risks": ["极低风险", "偶有暴雨", "高温高湿"],
        "tips": ["全球最安全城市之一", "法律严格(禁止口香糖/乱扔垃圾)", "紧急电话999(警察)/995(急救)"],
        "advisory": "极度安全，正常旅行",
    },
    "越南": {
        "overall": 6.5, "crime": 6.0, "terror": 7.5, "natural": 6.5, "health": 6.0, "traffic": 5.0,
        "level": "🟡 较安全",
        "risks": ["飞车抢夺(胡志明)", "交通事故率高", "食品安全", "台风季"],
        "tips": ["背包前背/手机握紧", "过马路需果断匀速", "喝瓶装水", "紧急电话113(警察)/115(急救)"],
        "advisory": "旅游区较安全，注意随身物品和交通安全",
    },
    "马来西亚": {
        "overall": 7.0, "crime": 6.5, "terror": 6.5, "natural": 7.5, "health": 7.0, "traffic": 6.0,
        "level": "🟡 较安全",
        "risks": ["东马沙巴沿海绑架风险", "吉隆坡扒窃", "交通事故"],
        "tips": ["西马(吉隆坡/槟城/兰卡威)安全", "东马海边度假村注意", "紧急电话999"],
        "advisory": "西马安全，东马沿海地区注意安全",
    },
    "印度尼西亚": {
        "overall": 6.0, "crime": 6.0, "terror": 5.5, "natural": 5.5, "health": 5.5, "traffic": 5.0,
        "level": "🟡 较安全",
        "risks": ["地震/火山活动", "巴厘岛偶有恐怖袭击历史", "交通事故", "登革热/疟疾"],
        "tips": ["巴厘岛主旅游区安全", "注意火山预警", "远离政治集会", "紧急电话110(警察)/118(急救)"],
        "advisory": "巴厘岛等旅游区安全，注意自然灾害预警",
    },
    "菲律宾": {
        "overall": 5.5, "crime": 5.0, "terror": 5.0, "natural": 5.5, "health": 5.5, "traffic": 4.5,
        "level": "🟠 注意安全",
        "risks": ["南部棉兰老岛恐怖袭击/绑架", "台风频发", "马尼拉扒窃/抢劫", "登革热"],
        "tips": ["长滩/巴拉望/宿务等旅游区安全", "避开棉兰老岛西部和苏禄群岛", "台风季6-11月关注预警", "紧急电话911"],
        "advisory": "主要旅游区安全，避开南部高风险地区",
    },
    "柬埔寨": {
        "overall": 6.0, "crime": 5.5, "terror": 7.0, "natural": 7.0, "health": 5.0, "traffic": 4.5,
        "level": "🟡 较安全",
        "risks": ["飞车抢夺", "地雷区(偏远地区)", "交通事故", "医疗条件有限"],
        "tips": ["暹粒/金边主城区安全", "偏远地区可能有未排雷区", "随身带常用药品", "紧急电话117(警察)/119(急救)"],
        "advisory": "主要旅游区安全，偏远地区注意地雷和医疗条件",
    },

    # ===== 南亚 =====
    "印度": {
        "overall": 5.0, "crime": 4.5, "terror": 5.0, "natural": 6.0, "health": 4.5, "traffic": 3.5,
        "level": "🟠 注意安全",
        "risks": ["女性安全风险", "恐怖袭击(克什米尔/东北部)", "交通安全极差", "食物/水污染", "登革热/疟疾"],
        "tips": ["女性避免夜间独行", "只喝瓶装水", "交通建议火车>飞机>公路", "紧急电话100(警察)/102(急救)"],
        "advisory": "需高度注意安全，女性旅行者尤其需要防范",
    },

    # ===== 中东 =====
    "阿联酋": {
        "overall": 8.5, "crime": 9.0, "terror": 7.5, "natural": 9.0, "health": 8.5, "traffic": 7.0,
        "level": "🟢 安全",
        "risks": ["高温(夏季50°C+)", "交通事故", "严格的法律法规"],
        "tips": ["迪拜/阿布扎比极度安全", "注意法律差异(酒精/着装/同性恋)", "夏季避免户外活动", "紧急电话999"],
        "advisory": "非常安全，注意遵守当地法律",
    },
    "土耳其": {
        "overall": 6.0, "crime": 6.0, "terror": 5.0, "natural": 6.5, "health": 7.0, "traffic": 5.0,
        "level": "🟡 较安全",
        "risks": ["恐怖袭击风险(伊斯坦布尔/安卡拉)", "叙利亚边境局势", "交通事故", "地震带"],
        "tips": ["旅游区(伊斯坦布尔老城/卡帕多奇亚/海岸)安全", "远离叙利亚边境", "紧急电话155(警察)/112(急救)"],
        "advisory": "旅游区安全，注意恐怖袭击风险和边境地区",
    },

    # ===== 欧洲 =====
    "法国": {
        "overall": 7.0, "crime": 6.0, "terror": 5.5, "natural": 8.5, "health": 8.5, "traffic": 7.5,
        "level": "🟡 较安全",
        "risks": ["巴黎扒窃/抢劫(地铁/景点)", "恐怖袭击风险", "罢工频繁影响交通"],
        "tips": ["地铁注意随身物品", "远离大规模集会", "紧急电话17(警察)/15(急救)/112(通用)"],
        "advisory": "整体安全，巴黎需注意扒窃，关注恐袭预警",
    },
    "英国": {
        "overall": 7.5, "crime": 6.5, "terror": 6.0, "natural": 8.5, "health": 8.5, "traffic": 8.0,
        "level": "🟡 较安全",
        "risks": ["伦敦扒窃", "恐怖袭击风险", "偶有骚乱/抗议"],
        "tips": ["伦敦注意随身物品", "紧急电话999/112"],
        "advisory": "整体安全，大城市注意防盗",
    },
    "意大利": {
        "overall": 7.0, "crime": 5.5, "terror": 7.0, "natural": 7.5, "health": 8.5, "traffic": 5.5,
        "level": "🟡 较安全",
        "risks": ["罗马/米兰/那不勒斯扒窃严重", "交通事故", "那不勒斯黑手党(游客不涉及)", "地震(中部)"],
        "tips": ["景点周围注意吉普赛人团伙", "贵重物品贴身携带", "紧急电话112/113(警察)/118(急救)"],
        "advisory": "整体安全，但扒窃非常普遍需高度警惕",
    },
    "德国": {
        "overall": 7.8, "crime": 7.0, "terror": 6.5, "natural": 9.0, "health": 9.0, "traffic": 8.0,
        "level": "🟢 安全",
        "risks": ["恐怖袭击风险", "大型车站扒窃", "极右翼集会(偶发)"],
        "tips": ["德国整体很安全", "火车站注意随身物品", "紧急电话110(警察)/112(急救)"],
        "advisory": "很安全，注意火车站防盗",
    },
    "西班牙": {
        "overall": 7.0, "crime": 6.0, "terror": 6.5, "natural": 8.0, "health": 8.5, "traffic": 7.0,
        "level": "🟡 较安全",
        "risks": ["巴塞罗那/马德里扒窃严重", "恐怖袭击风险", "夏季高温"],
        "tips": ["兰布拉大道特别小心", "海滩注意随身物品", "紧急电话112"],
        "advisory": "整体安全，扒窃严重需注意",
    },
    "瑞士": {
        "overall": 9.0, "crime": 8.5, "terror": 8.0, "natural": 8.0, "health": 9.5, "traffic": 9.0,
        "level": "🟢 极安全",
        "risks": ["极低风险", "雪崩(滑雪区)", "高山反应"],
        "tips": ["全球最安全国家之一", "紧急电话117(警察)/144(急救)/112(通用)"],
        "advisory": "极度安全，正常旅行",
    },

    # ===== 北美 =====
    "美国": {
        "overall": 6.5, "crime": 5.5, "terror": 6.0, "natural": 7.0, "health": 7.5, "traffic": 6.5,
        "level": "🟡 较安全",
        "risks": ["枪击事件(偶发)", "大城市特定区域犯罪率高", "自然灾害(飓风/山火)", "医疗费用极高"],
        "tips": ["避开高犯罪率区域(可查crime map)", "务必购买旅行保险", "紧急电话911", "夜间避免偏僻区域"],
        "advisory": "旅游区安全，需注意特定区域和枪支安全",
    },
    "加拿大": {
        "overall": 8.0, "crime": 8.0, "terror": 8.0, "natural": 7.5, "health": 8.5, "traffic": 8.0,
        "level": "🟢 安全",
        "risks": ["冬季极端严寒", "大型城市偶发犯罪", "野生动物(郊区)"],
        "tips": ["加拿大整体很安全", "冬季注意防寒", "紧急电话911"],
        "advisory": "很安全，注意冬季极端天气",
    },

    # ===== 大洋洲 =====
    "澳大利亚": {
        "overall": 8.0, "crime": 7.5, "terror": 8.0, "natural": 7.5, "health": 8.5, "traffic": 7.5,
        "level": "🟢 安全",
        "risks": ["海洋生物(鲨鱼/水母)", "紫外线极强", "山火(夏季)", "野生动物"],
        "tips": ["海滩只在红旗/黄旗之间游泳", "涂防晒SPF50+", "夏季关注山火预警", "紧急电话000"],
        "advisory": "很安全，注意海洋安全和防晒",
    },
    "新西兰": {
        "overall": 8.5, "crime": 8.5, "terror": 9.0, "natural": 7.0, "health": 8.5, "traffic": 7.5,
        "level": "🟢 极安全",
        "risks": ["地震", "山路交通", "紫外线强"],
        "tips": ["全球最安全国家之一", "山路驾驶注意", "紧急电话111"],
        "advisory": "极度安全，注意地震和山路驾驶",
    },

    # ===== 非洲 =====
    "埃及": {
        "overall": 5.0, "crime": 5.5, "terror": 4.5, "natural": 7.0, "health": 5.0, "traffic": 4.0,
        "level": "🟠 注意安全",
        "risks": ["恐怖袭击(西奈半岛)", "性骚扰(女性)", "交通事故", "食品安全"],
        "tips": ["开罗/卢克索/红海度假村旅游区安全", "避开西奈半岛北部", "女性注意着装和独行", "紧急电话122(警察)/123(急救)"],
        "advisory": "旅游区有安全保障，需注意性骚扰和交通安全",
    },
    "摩洛哥": {
        "overall": 6.0, "crime": 5.5, "terror": 6.0, "natural": 7.5, "health": 6.0, "traffic": 5.0,
        "level": "🟡 较安全",
        "risks": ["老城区骚扰/诈骗", "交通事故", "偶有恐袭"],
        "tips": ["主要旅游城市安全", "老城避免夜间独行", "紧急电话19(警察)/15(急救)"],
        "advisory": "旅游区安全，注意老城区骚扰",
    },

    # ===== 南美 =====
    "巴西": {
        "overall": 5.0, "crime": 4.0, "terror": 7.0, "natural": 7.0, "health": 5.5, "traffic": 5.0,
        "level": "🟠 注意安全",
        "risks": ["暴力犯罪率高(里约/圣保罗)", "贫民窟(favela)危险", "登革热/寨卡", "交通事故"],
        "tips": ["旅游区白天安全", "绝不进入贫民窟(除非有导游)", "不佩戴贵重首饰", "紧急电话190(警察)/192(急救)"],
        "advisory": "需高度注意安全，避免进入危险区域",
    },
}

# 安全等级颜色映射
LEVEL_COLORS = {
    "🟢": "绿色-安全",
    "🟡": "黄色-较安全",
    "🟠": "橙色-注意安全",
    "🔴": "红色-不建议前往",
}


def cmd_check(destination):
    """查询目的地安全指数"""
    if destination not in DESTINATIONS:
        # 模糊匹配
        matched = [d for d in DESTINATIONS if destination in d]
        if not matched:
            available = "、".join(sorted(DESTINATIONS.keys()))
            return json.dumps({
                "status": "error",
                "message": f"暂不支持「{destination}」，目前支持：{available}"
            }, ensure_ascii=False)
        destination = matched[0]

    d = DESTINATIONS[destination]

    output = f"🛡️ **{destination}安全指数**\n\n"
    output += f"**综合评分**：{d['overall']}/10 {d['level']}\n\n"
    output += "---\n\n"

    # 分项评分
    output += "## 📊 分项评分\n\n"
    output += "| 维度 | 评分 | 安全等级 |\n|------|------|----------|\n"
    dimensions = [
        ("🔪 犯罪安全", "crime"),
        ("💣 恐怖袭击", "terror"),
        ("🌊 自然灾害", "natural"),
        ("🏥 健康卫生", "health"),
        ("🚗 交通安全", "traffic"),
    ]
    for label, key in dimensions:
        score = d[key]
        if score >= 8:
            level = "🟢 安全"
        elif score >= 6:
            level = "🟡 较安全"
        elif score >= 4:
            level = "🟠 注意"
        else:
            level = "🔴 危险"
        bar = "█" * int(score) + "░" * (10 - int(score))
        output += f"| {label} | {bar} {score} | {level} |\n"
    output += "\n"

    # 主要风险
    output += "## ⚠️ 主要风险\n\n"
    for risk in d["risks"]:
        output += f"- {risk}\n"
    output += "\n"

    # 安全建议
    output += "## ✅ 安全建议\n\n"
    for tip in d["tips"]:
        output += f"- {tip}\n"
    output += "\n"

    # 官方建议
    output += "## 📋 官方建议\n\n"
    output += f"**{d['advisory']}**\n\n"

    # 紧急电话汇总
    output += "---\n📌 *安全指数基于公开数据综合评估，仅供参考。出行前请查阅最新外交部/使领馆旅行提醒。*\n"

    return output


def cmd_rank(min_score=0, max_score=10, region=None):
    """安全指数排名"""
    results = []
    for name, d in DESTINATIONS.items():
        if d["overall"] < min_score or d["overall"] > max_score:
            continue
        if region:
            # 简单区域过滤
            region_map = {
                "东亚": ["日本", "韩国", "中国"],
                "东南亚": ["泰国", "新加坡", "越南", "马来西亚", "印度尼西亚", "菲律宾", "柬埔寨"],
                "南亚": ["印度"],
                "中东": ["阿联酋", "土耳其"],
                "欧洲": ["法国", "英国", "意大利", "德国", "西班牙", "瑞士"],
                "北美": ["美国", "加拿大"],
                "大洋洲": ["澳大利亚", "新西兰"],
                "非洲": ["埃及", "摩洛哥"],
                "南美": ["巴西"],
            }
            region_dests = region_map.get(region, [])
            if name not in region_dests:
                continue
        results.append((name, d["overall"], d["level"]))

    results.sort(key=lambda x: x[1], reverse=True)

    output = "🏆 **旅行安全指数排名**\n\n"
    output += "| 排名 | 目的地 | 评分 | 安全等级 |\n|------|--------|------|----------|\n"
    for i, (name, score, level) in enumerate(results):
        output += f"| {i+1} | {name} | {score} | {level} |\n"
    output += "\n"

    return output


def cmd_compare(destinations_str):
    """对比多个目的地安全指数"""
    destinations = [d.strip() for d in destinations_str.split(",") if d.strip()]

    valid = []
    for d in destinations:
        if d in DESTINATIONS:
            valid.append(d)
        else:
            matched = [x for x in DESTINATIONS if d in x]
            if matched:
                valid.append(matched[0])

    if not valid:
        return json.dumps({"status": "error", "message": "没有匹配的目的地"}, ensure_ascii=False)

    output = f"📊 **安全指数对比**\n\n"
    output += "| 目的地 | 综合 | 犯罪 | 恐怖 | 自然 | 健康 | 交通 | 等级 |\n|--------|------|------|------|------|------|------|------|\n"

    for d in valid:
        data = DESTINATIONS[d]
        output += f"| {d} | **{data['overall']}** | {data['crime']} | {data['terror']} | {data['natural']} | {data['health']} | {data['traffic']} | {data['level']} |\n"
    output += "\n"

    # 推荐
    sorted_dests = sorted(valid, key=lambda x: DESTINATIONS[x]["overall"], reverse=True)
    output += f"🏆 **安全排名**：{' > '.join(sorted_dests)}\n"

    return output


# ========== 主入口 ==========
def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "status": "error",
            "message": "用法: destination_safety_index.py <command> [args]\n命令: check <目的地> | rank [区域] | compare <目的地1,目的地2,...>"
        }, ensure_ascii=False))
        return

    command = sys.argv[1]

    if command == "check":
        if len(sys.argv) < 3:
            print(json.dumps({"status": "error", "message": "请提供目的地名称"}, ensure_ascii=False))
            return
        print(cmd_check(sys.argv[2]))

    elif command == "rank":
        region = sys.argv[2] if len(sys.argv) > 2 else None
        print(cmd_rank(region=region))

    elif command == "compare":
        if len(sys.argv) < 3:
            print(json.dumps({"status": "error", "message": "请提供目的地列表，逗号分隔"}, ensure_ascii=False))
            return
        print(cmd_compare(sys.argv[2]))

    else:
        print(json.dumps({
            "status": "error",
            "message": f"未知命令: {command}\n支持: check | rank | compare"
        }, ensure_ascii=False))


if __name__ == "__main__":
    main()
