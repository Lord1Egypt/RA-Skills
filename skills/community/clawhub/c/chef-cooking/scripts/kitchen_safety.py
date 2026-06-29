#!/usr/bin/env python3
"""厨房安全知识库 — 油温预警/食材禁忌/食物中毒预防/急救措施"""

import sys
import json
import argparse

SAFETY_DB = {
    "油温安全": [
        {
            "q": "油锅起火了怎么办",
            "a": "❌ 绝对禁止用水泼！（水遇热油会爆炸式飞溅）\n✅ 正确步骤：\n1. 立即关火关闭燃气\n2. 用锅盖从侧面滑盖（隔绝氧气）\n3. 或用大块湿抹布覆盖\n4. 有灭火器用灭火器（干粉或F类）\n5. 火势失控：立即撤离，打119！",
            "severity": "danger"
        },
        {
            "q": "各种油的烟点是多少",
            "a": "烟点=油开始冒烟的温度，超过烟点产生有害物质：\n• 猪油 190°C\n• 黄油 150°C（不适合高温）\n• 菜籽油 210°C\n• 花生油 230°C\n• 大豆油 230°C\n• 橄榄油 190°C（特级初榨不适合炒菜）\n• 玉米油 230°C\n⚠️ 炒菜选高烟点油（花生油/大豆油），凉拌选低烟点油（橄榄油/芝麻油）。",
            "severity": "warning"
        },
        {
            "q": "怎么安全地炸东西",
            "a": "1. 油量不超过锅深1/3\n2. 食材必须沥干水分（水入油锅会爆溅）\n3. 用长筷子或漏勺操作，保持距离\n4. 温度计监测油温（不超过180°C）\n5. 炸完等油冷却再处理\n6. 油炸时人不能离开厨房！",
            "severity": "warning"
        },
    ],
    "食材禁忌": [
        {
            "q": "发芽的土豆能吃吗",
            "a": "❌ 不能！发芽土豆含龙葵碱毒素，可导致恶心/呕吐/腹泻/头痛，严重可致死。\n即使挖掉芽眼也不安全（毒素已扩散）。\n⚠️ 整个扔掉！别心疼那几块钱！",
            "severity": "danger"
        },
        {
            "q": "木耳泡多久安全",
            "a": "⚠️ 致命警告！木耳在常温泡发超过4小时（尤其夏天）会产生米酵菌酸毒素。\n致死率高达40-100%，无特效解药！\n✅ 正确做法：冷水泡1-2小时 → 泡好尽快吃 → 吃不完密封冷藏（不超过24小时）。\n⚠️ 闻到酸味/摸到发黏 = 立刻扔掉！",
            "severity": "danger"
        },
        {
            "q": "变绿的马铃薯/土豆",
            "a": "❌ 土豆皮变绿说明产生了龙葵碱（和发芽同样的毒素）。绿皮部分扔掉，如果内部也发绿，整个扔掉。别削掉绿皮就吃——毒素可能已渗入内部。",
            "severity": "danger"
        },
        {
            "q": "发霉的食物切掉坏的部分能吃吗",
            "a": "⚠️ 看情况：\n• 硬质食物（硬奶酪/胡萝卜）：切掉发霉部分+周围2cm，可以吃\n• 软质食物（面包/水果/果酱/酸奶）：❌ 整个扔掉！霉菌菌丝已深入内部，肉眼看不到\n• 花生/玉米发霉：❌ 可能含黄曲霉素（强致癌物），必须扔！",
            "severity": "warning"
        },
        {
            "q": "生豆浆能喝吗",
            "a": "❌ 不能！生豆浆含皂苷和胰蛋白酶抑制剂，会引起恶心/呕吐/腹泻。\n✅ 豆浆必须煮沸！且要注意\"假沸\"现象——豆浆在80°C就开始起泡看起来像沸了，但实际上没煮熟！\n真沸标准：起泡后继续煮5-8分钟，泡沫消失、豆香味出来才算熟。",
            "severity": "danger"
        },
        {
            "q": "四季豆没炒熟会怎样",
            "a": "❌ 未熟四季豆含植物血凝素和皂苷，导致恶心/呕吐/腹泻/头晕。\n✅ 四季豆必须彻底做熟！判断标准：颜色由鲜绿变暗绿，口感由脆变软，没有豆腥味。\n集体食堂食物中毒最常见的元凶之一！",
            "severity": "danger"
        },
        {
            "q": "海鲜和维生素C一起吃会中毒吗",
            "a": "⚠️ 理论上有风险，实际很难发生。海鲜中的五价砷+大量维C→三价砷（砒霜）。\n但需要吃几百公斤海鲜+几百片维C才可能中毒，正常饮食完全安全。\n不过海鲜+大量富含维C的水果（如大量鲜枣）不建议短时间内大量同食。",
            "severity": "info"
        },
        {
            "q": "柿子不能和什么一起吃",
            "a": "柿子含鞣酸+胃酸→胃结石风险。禁忌搭配：\n❌ 空腹吃柿子\n❌ 柿子+螃蟹/虾等高蛋白食物（鞣酸+蛋白=难消化沉淀物）\n❌ 柿子+红薯（刺激胃酸分泌）\n✅ 饭后1小时再吃，每天不超过1-2个。",
            "severity": "warning"
        },
        {
            "q": "隔夜菜能吃不",
            "a": "⚠️ 视菜品而定：\n• 绿叶蔬菜：❌ 不要隔夜！亚硝酸盐含量显著升高\n• 肉类：✅ 密封冷藏可放1-2天，但必须加热透\n• 凉拌菜：❌ 不要隔夜！细菌繁殖风险高\n• 海鲜：⚠️ 最好不隔夜，蛋白质降解产生有害物\n✅ 通用原则：趁热密封放冰箱（别等凉了），吃之前彻底加热到100°C。",
            "severity": "warning"
        },
        {
            "q": "蜂蜜能给婴儿吃吗",
            "a": "❌ 1岁以下婴儿绝对不能吃蜂蜜！\n蜂蜜可能含肉毒杆菌孢子，婴儿肠道未发育完全，会引发婴儿肉毒中毒（可致死）。\n1岁以上儿童和成人肠道成熟，可以安全食用。",
            "severity": "danger"
        },
        {
            "q": "味精加热会致癌吗",
            "a": "✅ 完全不用担心。味精=谷氨酸钠，120°C以上产生焦谷氨酸钠（无毒！不是致癌物）。\n焦谷氨酸钠只会让鲜味降低，没有任何健康危害。\n建议出锅前放味精（为了鲜味，不是为了安全）。",
            "severity": "info"
        },
        {
            "q": "炒菜油烟致癌吗",
            "a": "⚠️ 长期大量吸入厨房油烟确实增加肺癌风险（中式烹饪女性肺癌高发的重要因素）。\n✅ 防护措施：\n1. 开抽油烟机（炒菜前就开，炒完再开5分钟）\n2. 控制油温不冒烟（热锅凉油）\n3. 定期清洗抽油烟机滤网\n4. 戴口罩炒菜（最直接防护）",
            "severity": "warning"
        },
    ],
    "刀具安全": [
        {
            "q": "菜刀怎么安全使用",
            "a": "1. 刀用完了不要放水池里（看不到会割伤）\n2. 砧板下面垫湿布防滑\n3. 手指内扣（关节顶住刀面），指尖绝不伸到刀刃下\n4. 刀掉落了不要接，让它掉！\n5. 锋利的刀比钝刀更安全（钝刀需要更大力气，更容易滑）",
            "severity": "warning"
        },
        {
            "q": "切到手了怎么办",
            "a": "1. 立即用流动清水冲洗\n2. 干净纱布/纸巾按压止血（至少5分钟）\n3. 止血后碘伏消毒\n4. 创可贴包扎\n⚠️ 以下情况必须去医院：\n• 伤口深/长/止不住血\n• 切到手指功能部位\n• 刀上有锈（打破伤风针）\n• 伤口超过6小时未处理",
            "severity": "warning"
        },
    ],
    "燃气安全": [
        {
            "q": "闻到煤气味怎么办",
            "a": "🚨 紧急处理：\n1. 立即关掉燃气总阀\n2. 打开所有门窗通风\n3. ❌ 不要开关任何电器（包括抽油烟机/电灯！）\n4. ❌ 不要打电话/用打火机\n5. ❌ 不要穿脱化纤衣物（静电火花）\n6. 撤离到室外再打燃气公司电话或119\n⚠️ 燃气泄漏+电火花=爆炸！",
            "severity": "danger"
        },
        {
            "q": "燃气灶火焰什么颜色正常",
            "a": "🔵 蓝色=燃烧充分，正常。\n🟡 黄色=燃烧不充分，产生一氧化碳，危险！\n🔴 原因：灶头堵塞/进风量不足。解决方法：清理灶头/调节风门。\n⚠️ 黄色火焰一定要处理，长期吸入一氧化碳会中毒。",
            "severity": "warning"
        },
    ],
    "食品安全": [
        {
            "q": "生熟为什么要分开",
            "a": "⚠️ 生肉/生鱼上的细菌（沙门氏菌/副溶血性弧菌等）会污染熟食。\n✅ 必须做到：\n• 生熟砧板/刀具分开使用\n• 切完生肉的刀和砧板必须彻底清洗再切熟食\n• 盛过生肉的盘子不能再盛熟食\n• 冰箱里生肉放下层（防止血水滴到熟食上）",
            "severity": "warning"
        },
        {
            "q": "冰箱温度怎么设置才安全",
            "a": "• 冷藏室：0-4°C（抑制细菌繁殖）\n• 冷冻室：-18°C以下（细菌停止活动）\n⚠️ 危险温度带：4-60°C，细菌快速增长！\n✅ 食物不要在室温放超过2小时（夏天不超过1小时）。",
            "severity": "info"
        },
        {
            "q": "食物中毒有什么症状",
            "a": "通常在食后2-24小时出现：恶心/呕吐/腹痛/腹泻/发热。\n⚠️ 以下情况立即就医：\n• 血便\n• 高烧超过38.5°C\n• 持续呕吐无法进水\n• 严重脱水（口干/尿少/头晕）\n• 症状持续超过3天\n• 孕妇/老人/儿童/免疫低下者",
            "severity": "danger"
        },
        {
            "q": "怎么判断肉熟了没有",
            "a": "最安全：用食品温度计！\n• 鸡肉：中心温度≥74°C\n• 猪肉/牛肉块：≥63°C\n• 绞肉：≥71°C\n• 鱼肉：≥63°C 或肉变不透明易分离\n没有温度计：\n• 鸡肉：筷子能轻松插入，流出清澈汁液（不是粉色）\n• 猪肉：切开中心不再粉红",
            "severity": "warning"
        },
    ],
    "厨房急救": [
        {
            "q": "烫伤了怎么办",
            "a": "🔥 牢记五字诀：冲→脱→泡→盖→送\n1. 冲：流动冷水冲15-20分钟（最重要！）\n2. 脱：小心脱掉覆盖的衣物（粘连不要硬扯）\n3. 泡：冷水浸泡15-30分钟\n4. 盖：干净纱布覆盖\n5. 送：严重烫伤去医院\n❌ 禁止：涂牙膏/酱油/醋/面粉（会感染+影响医生判断）\n❌ 禁止：挑破水泡（自然吸收或医生处理）",
            "severity": "danger"
        },
        {
            "q": "异物卡喉（气道堵塞）怎么办",
            "a": "🚨 海姆立克急救法（成人）：\n1. 站患者背后，双手环抱腰部\n2. 一手握拳，拳眼对准肚脐上方两指处\n3. 另一手包住拳头\n4. 向内上方快速冲击，重复直到异物排出\n⚠️ 自己一个人：弯腰，用椅背顶住上腹部，用力冲击。\n⚠️ 如果患者昏迷/孕妇/婴儿：方法不同！拨打120！",
            "severity": "danger"
        },
    ],
}


def search_safety(query: str = None, topic: str = None) -> dict:
    """搜索厨房安全知识"""
    results = []

    if topic:
        tips = SAFETY_DB.get(topic, [])
        if query:
            tips = [t for t in tips if query.lower() in t["q"].lower() or query.lower() in t["a"].lower()]
        results = tips
    elif query:
        for cat, tips in SAFETY_DB.items():
            for t in tips:
                if query.lower() in t["q"].lower() or query.lower() in t["a"].lower():
                    results.append({**t, "category": cat})
    else:
        categories = {}
        for cat, tips in SAFETY_DB.items():
            danger = sum(1 for t in tips if t["severity"] == "danger")
            warning = sum(1 for t in tips if t["severity"] == "warning")
            categories[cat] = {"total": len(tips), "danger": danger, "warning": warning}
        return {"categories": categories}

    return {"query": query, "topic": topic, "results": results, "count": len(results)}


def print_safety_result(result: dict):
    """格式化输出安全知识"""
    if "categories" in result:
        print("\n🛡️ 厨房安全知识库\n")
        for cat, stats in result["categories"].items():
            icons = f"🔴{stats['danger']} 🟡{stats['warning']}" if stats['danger'] + stats['warning'] > 0 else "🟢"
            print(f"  {icons} {cat}: {stats['total']}条")
        total = sum(s["total"] for s in result["categories"].values())
        print(f"\n  共 {total} 条安全知识\n")
        return

    print(f"\n🛡️ 搜索: {result['query'] or '全部'} | 主题: {result['topic'] or '全部'}")
    print(f"📊 找到 {result['count']} 条:\n")

    for i, t in enumerate(result["results"], 1):
        sev = {"danger": "🔴 危险", "warning": "🟡 注意", "info": "🔵 知识"}.get(t["severity"], "")
        cat_tag = f" [{t.get('category', '')}]" if t.get('category') else ""
        print(f"{i}. {sev} {t['q']}{cat_tag}")
        print(f"   {t['a']}")
        print()


def main():
    parser = argparse.ArgumentParser(description="厨房安全知识库")
    parser.add_argument("--query", type=str, help="搜索关键词")
    parser.add_argument("--topic", type=str, help="安全主题（油温安全/食材禁忌/刀具安全/燃气安全/食品安全/厨房急救）")
    parser.add_argument("--json", action="store_true", help="JSON 格式输出")
    args = parser.parse_args()

    result = search_safety(args.query, args.topic)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_safety_result(result)


if __name__ == "__main__":
    main()
