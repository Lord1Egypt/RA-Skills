"""
地支藏干系统 + 身强弱精确判断
藏干：每个地支内藏的天干及其中余气力量
"""

STEMS = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
BRANCHES = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
STEM_ELEMENTS = {
    '甲': '木', '乙': '木', '丙': '火', '丁': '火', '戊': '土',
    '己': '土', '庚': '金', '辛': '金', '壬': '水', '癸': '水'
}
BRANCH_ELEMENTS = {
    '子': '水', '丑': '土', '寅': '木', '卯': '木', '辰': '土',
    '巳': '火', '午': '火', '未': '土', '申': '金', '酉': '金',
    '戌': '土', '亥': '水'
}

# 地支藏干表（本气、中气、余气）
# 格式：(天干, 力量等级)
# 力量等级：本气=1.0，中气=0.5，余气=0.3
ZANGAN = {
    '子': [('癸', 1.0)],
    '丑': [('己', 1.0), ('癸', 0.5), ('辛', 0.3)],
    '寅': [('甲', 1.0), ('丙', 0.5), ('戊', 0.3)],
    '卯': [('乙', 1.0)],
    '辰': [('戊', 1.0), ('乙', 0.5), ('癸', 0.3)],
    '巳': [('丙', 1.0), ('庚', 0.5), ('戊', 0.3)],
    '午': [('丁', 1.0), ('己', 0.5)],
    '未': [('己', 1.0), ('丁', 0.5), ('乙', 0.3)],
    '申': [('庚', 1.0), ('壬', 0.5), ('戊', 0.3)],
    '酉': [('辛', 1.0)],
    '戌': [('戊', 1.0), ('辛', 0.5), ('丁', 0.3)],
    '亥': [('壬', 1.0), ('甲', 0.5)],
}

# 月令（地支）对应季节的当令五行
MONTH_LING = {
    '寅': '木', '卯': '木',    # 春
    '巳': '火', '午': '火',    # 夏
    '申': '金', '酉': '金',    # 秋
    '亥': '水', '子': '水',    # 冬
    '辰': '土', '戌': '土', '未': '土', '丑': '土',  # 四季末
}

# 五行相生
SHENG = {'木': '火', '火': '土', '土': '金', '金': '水', '水': '木'}
# 五行相克
KE = {'木': '土', '土': '水', '水': '火', '火': '金', '金': '木'}


def get_all_stems_with_weight(bazi: dict) -> dict:
    """
    展开八字所有天干（含藏干），计算每个天干的权重
    返回：{天干: 总权重分}
    """
    weights = {s: 0.0 for s in STEMS}

    # 明柱天干（各占1分）
    for col in ['year', 'month', 'day', 'hour']:
        stem = bazi[col]['stem']
        weights[stem] += 1.0

    # 地支藏干
    for col in ['year', 'month', 'day', 'hour']:
        branch = bazi[col]['branch']
        for hidden_stem, weight in ZANGAN[branch]:
            weights[hidden_stem] += weight

    return weights


def analyze_strength_detailed(bazi: dict) -> dict:
    """
    精确身强弱分析
    1. 计算日主总权重
    2. 月令当令程度
    3. 通根判断（地支是否有日主同类）
    4. 综合打分
    """
    day_master = bazi['day']['stem']
    day_elem = STEM_ELEMENTS[day_master]
    month_branch = bazi['month']['branch']
    month_elem = BRANCH_ELEMENTS[month_branch]

    # 计算所有天干权重
    weights = get_all_stems_with_weight(bazi)
    day_total = weights[day_master]

    # 1. 月令判断（当令=1.5分，相=0.8分，死=0.3分，囚=0.5分）
    ling_table = {'当令': 1.5, '相': 0.8, '死': 0.3, '囚': 0.5}
    season_elem = MONTH_LING.get(month_branch, '土')

    if month_elem == day_elem:
        ling_score = 1.5  # 当令
    elif SHENG.get(month_elem) == day_elem:
        ling_score = 0.8  # 月令相
    elif KE.get(month_elem) == day_elem:
        ling_score = 0.3  # 月令死
    else:
        ling_score = 0.5  # 月令囚

    # 2. 通根：天干地支里有没有和日主同五行
    # 有根则强，无根则弱（天干一片比劫但地支无根 = 假强）
    same_elem_stems = [s for s in STEMS if STEM_ELEMENTS[s] == day_elem]
    has_root = any(
        STEM_ELEMENTS.get(bazi[col]['stem']) == day_elem or
        BRANCH_ELEMENTS.get(bazi[col]['branch']) == day_elem
        for col in ['year', 'month', 'day', 'hour']
    )

    # 地支本气是否为日主同类
    month_branch_main = ZANGAN[month_branch][0][0]  # 本气
    has_month_root = STEM_ELEMENTS[month_branch_main] == day_elem

    # 3. 综合评分
    # 基准 = 日主权重 + 月令分 + 通根加分
    base_score = day_total + ling_score
    if has_root:
        base_score += 0.5
    if has_month_root:
        base_score += 0.5

    # 4. 定性
    if base_score >= 5.0:
        strength = '极强'
        tip = '日主极旺，不宜再补同气，宜泄不宜助'
    elif base_score >= 3.5:
        strength = '身强'
        tip = '日主偏旺，宜泄宜克，适合竞争性、开创性工作'
    elif base_score >= 2.5:
        strength = '身中'
        tip = '日主中和，进退自如，适应面广'
    elif base_score >= 1.5:
        strength = '身弱'
        tip = '日主偏弱，宜生宜助，不宜过度消耗'
    else:
        strength = '极弱'
        tip = '日主极弱，宜大补元气，谨慎高压环境'

    bazi['strength'] = strength
    bazi['strength_score'] = round(base_score, 1)
    bazi['strength_tip'] = tip
    bazi['day_total_weight'] = round(day_total, 1)
    bazi['ling_score'] = ling_score
    bazi['has_root'] = has_root
    bazi['has_month_root'] = has_month_root

    return bazi


def format_strength_detail(bazi: dict) -> str:
    """格式化身强弱详情"""
    lines = []
    lines.append(f"日主：{bazi['day_master']}（{STEM_ELEMENTS[bazi['day_master']]}）")
    lines.append(f"月令：{bazi['month']['branch']}（{BRANCH_ELEMENTS[bazi['month']['branch']]}）")
    lines.append(f"日主权重分：{bazi['day_total_weight']}（天干1.0 + 藏干加权）")
    lines.append(f"月令当令分：{bazi['ling_score']}")
    lines.append(f"通根状态：{'有根' if bazi['has_root'] else '无根'}")
    lines.append(f"综合评分：{bazi['strength_score']}")
    lines.append(f"定性：{bazi['strength']} → {bazi['strength_tip']}")
    return '\n'.join(lines)


if __name__ == '__main__':
    from calc.bazi import get_bazi

    # 测试1：张雪峰 甲子 己巳 壬子 乙巳
    # 需要找这个生日...先测试庚金日主
    test = get_bazi(1990, 5, 15, 10)
    analyze_strength_detailed(test)
    print("八字:", test['str'])
    print("旧版判断:", test.get('strength', 'N/A'))
    print("旧版得分:", test.get('strength_score', 'N/A'))
    print()
    print("精确版:")
    print(format_strength_detail(test))

    print()
    weights = get_all_stems_with_weight(test)
    print("各天干权重:", {k: round(v, 1) for k, v in weights.items() if v > 0})
