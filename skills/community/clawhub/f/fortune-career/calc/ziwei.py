"""
紫微斗数排盘算法
基于八字月柱和年柱推算各宫位主星
"""

from typing import Dict, List, Optional

# 十二宫顺序（从命宫逆时针排）
PALACES = ['命', '父母', '福德', '田宅', '事业', '交友', '迁移', '疾厄', '财帛', '子女', '夫妻', '官禄']

# 地支对应索引
ZHI_INDEX = {'子': 0, '丑': 1, '寅': 2, '卯': 3, '辰': 4, '巳': 5,
             '午': 6, '未': 7, '申': 8, '酉': 9, '戌': 10, '亥': 11}

# 藏干表
ZANGAN = {
    '子': ['癸'], '丑': ['己', '癸', '辛'], '寅': ['甲', '丙', '戊'],
    '卯': ['乙'], '辰': ['戊', '乙', '癸'], '巳': ['丙', '庚', '戊'],
    '午': ['丁', '己'], '未': ['己', '丁', '乙'], '申': ['庚', '壬', '戊'],
    '酉': ['辛'], '戌': ['戊', '辛', '丁'], '亥': ['壬', '甲']
}

# 十四正曜分类
# 第一等：紫微、天机、太阳、武曲、天同、廉贞
# 第二等：天府、太阴、贪狼、巨门、天相、天梁、七杀、破军

def get_ziwei_position(month_zhi: str) -> str:
    """
    紫微星落宫（简化版）
    规则：紫微星永远落在亥、子、丑三宫
    确切宫位根据月支和时支推算
    口诀：紫微子在亥午未申，卯戌二宫空
    """
    # 简化规则：月支为亥/子/丑 → 紫微在亥
    # 月支为寅/午/未/申 → 紫微在午
    # 月支为卯/戌 → 空
    # 月支为辰/巳/酉 → 紫微在丑
    mapping = {
        '亥': '亥', '子': '亥', '丑': '亥',
        '寅': '午', '午': '午', '未': '午', '申': '午',
        '卯': '空', '戌': '空',
        '辰': '丑', '巳': '丑', '酉': '丑',
    }
    return mapping.get(month_zhi, '亥')


def get_main_stars(year_gan: str, year_zhi: str, month_zhi: str) -> Dict[str, str]:
    """
    排十四正曜
    年干用于定三合局，月支用于定紫微位置
    """
    stars = {}

    # 1. 紫微星 - 根据月支定
    stars['紫微'] = get_ziwei_position(month_zhi)

    # 2. 天机 - 永远在丑宫
    stars['天机'] = '丑'

    # 3. 太阳 - 根据年支定（年支为申子辰→亥，寅午戌→午，亥卯未→未，巳酉丑→申）
    sun_table = {
        '申': '亥', '子': '亥', '辰': '亥',
        '寅': '午', '午': '午', '戌': '午',
        '亥': '未', '卯': '未', '未': '未',
        '巳': '申', '酉': '申', '丑': '申',
    }
    stars['太阳'] = sun_table.get(year_zhi, '午')

    # 4. 武曲 - 根据年支定
    wuqu_table = {
        '申': '辰', '子': '辰', '辰': '辰',
        '寅': '戌', '午': '戌', '戌': '戌',
        '亥': '巳', '卯': '巳', '未': '巳',
        '巳': '丑', '酉': '丑', '丑': '丑',
    }
    stars['武曲'] = wuqu_table.get(year_zhi, '辰')

    # 5. 天同 - 根据年支定
    tiantong_table = {
        '申': '未', '子': '未', '辰': '未',
        '寅': '辰', '午': '辰', '戌': '辰',
        '亥': '酉', '卯': '酉', '未': '酉',
        '巳': '子', '酉': '子', '丑': '子',
    }
    stars['天同'] = tiantong_table.get(year_zhi, '未')

    # 6. 廉贞 - 根据年支定
    lianzhen_table = {
        '申': '寅', '子': '寅', '辰': '寅',
        '寅': '申', '午': '申', '戌': '申',
        '亥': '亥', '卯': '亥', '未': '亥',
        '巳': '巳', '酉': '巳', '丑': '巳',
    }
    stars['廉贞'] = lianzhen_table.get(year_zhi, '寅')

    # 7. 天府 - 与紫微相对
    ziwei_pos = ZHI_INDEX[stars['紫微']]
    tianfu_pos = (ziwei_pos + 6) % 12
    tianfu_zhi = list(ZHI_INDEX.keys())[list(ZHI_INDEX.values()).index(tianfu_pos)]
    stars['天府'] = tianfu_zhi

    # 8. 太阴 - 根据年支定
    taiyin_table = {
        '申': '戌', '子': '戌', '辰': '戌',
        '寅': '丑', '午': '丑', '戌': '丑',
        '亥': '卯', '卯': '卯', '未': '卯',
        '巳': '亥', '酉': '亥', '丑': '亥',
    }
    stars['太阴'] = taiyin_table.get(year_zhi, '戌')

    # 9. 贪狼 - 根据年支和月支定（简化）
    tanlang_pos = (ZHI_INDEX[year_zhi] + 1) % 12
    stars['贪狼'] = list(ZHI_INDEX.keys())[tanlang_pos]

    # 10. 巨门 - 根据年支定
    jumen_table = {
        '申': '子', '子': '子', '辰': '子',
        '寅': '卯', '午': '卯', '戌': '卯',
        '亥': '丑', '卯': '丑', '未': '丑',
        '巳': '寅', '酉': '寅', '丑': '寅',
    }
    stars['巨门'] = jumen_table.get(year_zhi, '子')

    # 11. 天相 - 根据年支和月支推（简化：永远在巳或午）
    tianxiang_table = {
        '子': '巳', '丑': '巳', '寅': '午', '卯': '午',
        '辰': '巳', '巳': '午', '午': '巳', '未': '午',
        '申': '巳', '酉': '午', '戌': '巳', '亥': '午',
    }
    stars['天相'] = tianxiang_table.get(year_zhi, '巳')

    # 12. 天梁 - 根据年支定
    tianliang_table = {
        '申': '午', '子': '午', '辰': '午',
        '寅': '未', '午': '未', '戌': '未',
        '亥': '寅', '卯': '寅', '未': '寅',
        '巳': '卯', '酉': '卯', '丑': '卯',
    }
    stars['天梁'] = tianliang_table.get(year_zhi, '午')

    # 13. 七杀 - 根据年支定
    qisha_table = {
        '申': '子', '子': '子', '辰': '子',
        '寅': '丑', '午': '丑', '戌': '丑',
        '亥': '卯', '卯': '卯', '未': '卯',
        '巳': '亥', '酉': '亥', '丑': '亥',
    }
    stars['七杀'] = qisha_table.get(year_zhi, '子')

    # 14. 破军 - 根据年支定
    pojund_table = {
        '申': '辰', '子': '辰', '辰': '辰',
        '寅': '午', '午': '午', '戌': '午',
        '亥': '寅', '卯': '寅', '未': '寅',
        '巳': '亥', '酉': '亥', '丑': '亥',
    }
    stars['破军'] = pojund_table.get(year_zhi, '辰')

    return stars


def build_chart(bazi: dict) -> dict:
    """
    构建完整命盘
    输入：八字字典（from bazi.py）
    输出：十二宫及每个宫位的主星
    """
    year_gan = bazi['year']['stem']
    year_zhi = bazi['year']['branch']
    month_zhi = bazi['month']['branch']

    # 1. 命宫位置 = 逆布：年支起正月，顺数至生月，再逆时针布十二宫
    # 简化：用年支地支索引找命宫
    year_zhi_idx = ZHI_INDEX[year_zhi]
    month_zhi_idx = ZHI_INDEX[month_zhi]

    # 命宫 = (年支索引 - 生月 + 12) % 12（简化算法）
    minggong_idx = (year_zhi_idx - month_zhi_idx) % 12

    # 2. 排十二宫
    palaces = {}
    zhi_list = list(ZHI_INDEX.keys())

    for i, palace in enumerate(PALACES):
        palace_idx = (minggong_idx - i) % 12
        palaces[palace] = zhi_list[palace_idx]

    # 3. 排十四正曜
    main_stars = get_main_stars(year_gan, year_zhi, month_zhi)

    # 4. 分配主星到各宫
    chart = {}
    for palace_name, palace_zhi in palaces.items():
        stars_in_palace = []

        # 找出哪些星落在此宫
        for star_name, star_zhi in main_stars.items():
            if star_zhi == palace_zhi:
                stars_in_palace.append(star_name)

        chart[palace_name] = {
            'zhi': palace_zhi,
            'stars': stars_in_palace
        }

    # 5. 标记格局
    chart['_meta'] = {
        'minggong_zhi': palaces['命'],
        'main_stars': main_stars
    }

    return chart


def analyze_geshi(chart: dict) -> List[str]:
    """分析格局"""
    geshi = []
    main_stars = chart['_meta']['main_stars']

    # 杀破狼格局
    if '七杀' in main_stars.values() and '破军' in main_stars.values() and '贪狼' in main_stars.values():
        if '命' in str(main_stars):
            geshi.append('杀破狼')

    # 紫府同宫
    if '紫微' in main_stars.values() and '天府' in main_stars.values():
        geshi.append('紫府同宫')

    # 日月同宫
    if '太阳' in main_stars.values() and '太阴' in main_stars.values():
        geshi.append('日月同宫')

    return geshi if geshi else ['普通格局']


if __name__ == '__main__':
    from bazi import get_bazi, analyze_wuxing

    # 测试八字：甲子 己巳 壬子 乙巳
    # 需要找一个能排出这个八字的生日，这里用估计
    # 壬子日柱...
    test = get_bazi(1984, 4, 4, 10)
    print("八字:", test['str'])
    analyze_wuxing(test)

    chart = build_chart(test)
    for palace, info in chart.items():
        if palace != '_meta':
            print(f"{palace}宫({info['zhi']}): {', '.join(info['stars']) if info['stars'] else '无主星'}")
    print("格局:", analyze_geshi(chart))
