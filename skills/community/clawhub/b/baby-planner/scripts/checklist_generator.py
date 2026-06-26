#!/usr/bin/env python3
"""
待产清单生成器
用法: python3 checklist_generator.py 顺产 2026-05-01
     第二个参数为预产期，第三个参数为生产方式（顺产/剖宫产）
"""

import sys
from datetime import datetime, timedelta

MOM_LIST = {
    "衣物类": [
        "哺乳睡衣 × 2-3套（侧开/上下开扣款）",
        "哺乳内衣 × 2-3件（选大一码，产后涨奶需要空间）",
        "一次性纯棉内裤 × 10条",
        "出院衣服 × 1套（宽松哺乳衣+帽子+围巾）",
        "拖鞋 × 1双（包跟款，防滑）",
    ],
    "护理类": [
        "产褥垫 × 20片（60×90cm，医院会提供部分但不够用）",
        "产妇卫生巾/安心裤 × 2-3包（前几天安心裤更方便）",
        "会阴冷敷贴 × 4片（顺产侧切/撕裂用，敷在伤口上）",
        "收腹带 × 1条（剖宫产下床走路必须带）",
        "羊脂膏 × 1支（乳头皲裂救星，必买）",
        "防溢乳垫 × 1包（奶阵来了防止衣服湿）",
        "痔疮膏 × 1支（顺产大概率用到，怀孕时就可以备好）",
    ],
    "餐具/日用": [
        "保温杯 × 1（带吸管款的，躺着喝）",
        "弯头吸管 × 1包（剖宫产前两天只能躺着喝流食）",
        "洗漱用品 × 1套（软毛牙刷+牙膏+毛巾）",
        "充电宝 × 1（产房等待时间很长）",
        "胎心监护带 × 1副（孕晚期产检需要，住院也要带）",
        "纸巾/湿巾 × 各1包",
    ],
    "证件类": [
        "双方身份证原件+复印件",
        "医保卡/社保卡",
        "产检本（所有检查单都带上）",
        "生育服务证/准生证（电子版也行）",
        "住院押金（提前问好支付方式）",
    ],
}

BABY_LIST = {
    "衣物类": [
        "和尚服/半背衣 × 3-5件（59码，新生儿容易吐奶弄脏）",
        "包被 × 2条（一薄一厚，视季节）",
        "胎帽 × 1顶",
        "袜子 × 2双（夏天可以不用）",
    ],
    "喂养类": [
        "奶瓶 × 2个（宽口径，SS奶嘴）",
        "奶粉 × 1小罐（备用，医院会提供但品牌固定）",
        "奶瓶刷 × 1套",
        "婴儿硅胶勺 × 1（喂水/药用）",
        "恒温水壶 × 1（医院不一定有，准备好）",
    ],
    "护理类": [
        "NB纸尿裤 × 1包（不要囤多，先看娃体重，8斤+直接用S）",
        "婴儿湿巾 × 1包（换尿布用，温水打湿也能当湿巾）",
        "护臀膏 × 1支（含氧化锌的，预防红屁股）",
        "婴儿洗衣液 × 1瓶",
        "宝宝沐浴露 × 1（医院会洗，但备着）",
        "婴儿润肤霜 × 1",
    ],
    "其他": [
        "婴儿提篮/安全座椅 × 1（出院必须，正向安装）",
        "小脸盆 × 2个（洗脸+洗屁股分开）",
    ],
}

CAESAREAN_EXTRAS = [
    "收腹带 × 1条（手术后就要绑，固定伤口）",
    "吸管数量增加到2包（前24小时只能喝流食）",
    "藕粉 × 1盒（剖宫产后排气前只能吃流食，藕粉好消化）",
    "静脉曲张袜 × 1双（手术后排气前需卧床，防血栓）",
]

SEASON_TIPS = {
    "spring": "🌸 春天（3-5月）：注意防风，准备薄外套，新生儿体温调节差",
    "summer": "☀️ 夏天（6-8月）：重点防暑，产妇和新生儿都怕热，多备纱布巾",
    "autumn": "🍂 秋天（9-11月）：早晚温差大，包被选厚薄适中的",
    "winter": "❄️ 冬天（12-2月）：保暖第一，宝宝衣服提前捂热再穿",
}

def get_season(date_str: str) -> str:
    month = int(date_str.split("-")[1])
    if month in [3, 4, 5]:
        return "spring"
    elif month in [6, 7, 8]:
        return "summer"
    elif month in [9, 10, 11]:
        return "autumn"
    else:
        return "winter"

def generate_checklist(delivery_type: str, edd_str: str):
    edd = datetime.strptime(edd_str, "%Y-%m-%d")
    today = datetime.today()
    days_until = (edd - today).days
    season = get_season(edd_str)

    print(f"\n{'='*45}")
    print(f"  📋 待产包清单 — 预产期 {edd_str}")
    print(f"  🏥 分娩方式: {delivery_type}")
    print(f"  ⏰ 距预产期还有 {days_until} 天")
    print(f"  {SEASON_TIPS.get(season, '')}")
    print(f"{'='*45}")

    # 建议打包时机
    if days_until <= 30:
        print("\n  ⚠️  建议现在就开始打包！")
    else:
        print(f"\n  💡 建议孕{30 + (7 - today.day % 7) if today.day % 7 != 0 else 30}周左右开始准备")
    print(f"  📦 打包好放门口/后备箱，见红/破水随时出发")

    print(f"\n\n{'─'*45}")
    print(f"  👩 妈妈物品")
    print(f"{'─'*45}")
    for category, items in MOM_LIST.items():
        print(f"\n  【{category}】")
        for i, item in enumerate(items, 1):
            print(f"    {'✅' if i <= 3 else '  '} {item}")
    if delivery_type == "剖宫产":
        print(f"\n  【剖宫产额外】")
        for item in CAESAREAN_EXTRAS:
            print(f"    ⚡ {item}")

    print(f"\n\n{'─'*45}")
    print(f"  👶 宝宝物品")
    print(f"{'─'*45}")
    for category, items in BABY_LIST.items():
        print(f"\n  【{category}】")
        for i, item in enumerate(items, 1):
            print(f"    {'✅' if i <= 3 else '  '} {item}")

    print(f"\n\n{'─'*45}")
    print(f"  🏠 到家后第一时间需要的")
    print(f"{'─'*45}")
    home_items = [
        "婴儿床/安全睡篮（独立睡，避同床）",
        "隔尿垫 × 2（换尿布垫着）",
        "温湿度计（室温保持22-24°C，湿度50-60%）",
        "耳温枪（博朗耳温枪，出生1周后可能用到）",
        "婴儿指甲剪（新生儿指甲软，贝亲那款好用）",
        "尿布台（不弯腰换尿布，护腰神器）",
    ]
    for item in home_items:
        print(f"  · {item}")

    print(f"\n{'='*45}")
    print(f"  💡 小贴士:")
    print(f"  · 住院期间医院提供部分物品，可提前问护士站")
    print(f"  · 爸爸/家属要知道待产包位置！产妇发动时顾不上")
    print(f"  · 宝宝衣服和包被提前洗一遍（用婴儿洗衣液）")
    print(f"  · 手机、充电宝充好电，产房可以带")
    print(f"{'='*45}\n")

if __name__ == "__main__":
    delivery = sys.argv[1] if len(sys.argv) > 1 else "顺产"
    edd = sys.argv[2] if len(sys.argv) > 2 else datetime.today().strftime("%Y-%m-%d")
    generate_checklist(delivery, edd)
