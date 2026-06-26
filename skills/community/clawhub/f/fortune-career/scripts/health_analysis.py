"""
健康分析框架
基于八字五行强弱和紫微疾厄宫分析健康风险
"""

from calc.bazi import STEMS, BRANCHES, ELEMENTS, BRANCH_ELEMENTS

# 十天干对应脏腑
STEM_ORGANS = {
    '甲': '肝、胆（筋骨）',
    '乙': '肝、胆（毛发）',
    '丙': '小肠、心（血液、眼睛）',
    '丁': '心脏、血（眼睛）',
    '戊': '胃、脾（消化）',
    '己': '脾、胃（肌肉）',
    '庚': '大肠、肺（呼吸、皮肤）',
    '辛': '肺、呼吸系统（牙齿、骨骼）',
    '壬': '膀胱、肾（血液、代谢）',
    '癸': '肾、心包（免疫、内分泌）',
}

# 地支对应身体部位
BRANCH_BODY = {
    '子': '耳、肾、泌尿、生殖',
    '丑': '肚腹、脾、肝',
    '寅': '胆、手臂、肝',
    '卯': '肝、神经、手指',
    '辰': '肩、胸、胃',
    '巳': '脸、咽、心',
    '午': '眼、心、小肠',
    '未': '脊背、脾、消化',
    '申': '大肠、肺、呼吸',
    '酉': '肺、骨、齿',
    '戌': '腿、命门、消化',
    '亥': '肾、血、循环',
}

# 五行过弱/过旺的健康表现
ELEMENT_HEALTH = {
    '木': {'弱': '肝胆不适、筋骨酸痛、情绪抑郁',
           '旺': '肝火旺盛、偏头痛、易怒',
           'note': '木对应肝胆，肝主疏泄，木弱者易情绪郁结'},
    '火': {'弱': '心脏血液循环不佳、手脚冰冷、面色苍白',
           '旺': '心火旺、口舌生疮、失眠多梦、血压高',
           'note': '火对应心和小肠，火旺者易心血管问题'},
    '土': {'弱': '消化不良、脾胃虚弱、容易疲劳',
           '旺': '脾胃湿热、体内毒素、口臭、皮肤问题',
           'note': '土对应脾胃，是后天之本'},
    '金': {'弱': '呼吸系统弱、易感冒、皮肤粗糙',
           '旺': '肺部燥热、咳嗽、便秘、痔',
           'note': '金对应肺大肠，金旺者呼吸系统敏感'},
    '水': {'弱': '肾虚、腰酸、泌尿问题、精力不济',
           '旺': '肾水过旺、水肿、体寒、妇科/男科问题',
           'note': '水对应肾和膀胱，肾为先天之本'},
}

# 流年冲克健康预警
YEAR_CONFLICT = {
    '子午冲': '心肾不交、心脏血压问题、情绪波动大',
    '丑未冲': '脾胃肝胆问题、消化系统紊乱',
    '寅申冲': '肝胆、肺大肠问题、肢体疼痛',
    '卯酉冲': '肝肺不和、神经系统、呼吸系统',
    '辰戌冲': '脾胃皮肤病、精神压力、失眠',
    '巳亥冲': '心肾不交、心脏、血液问题',
}

# 紫微疾厄宫重点
STAR_HEALTH = {
    '紫微': '身体一般较好，但易因权力欲望引发情志问题',
    '天机': '神经系统易受损，用脑过度则失眠头痛',
    '太阳': '眼睛、血液、血压、心脏问题',
    '武曲': '肺部、呼吸系统、骨骼',
    '天同': '消化系统、肾脏、水液代谢',
    '廉贞': '泌尿系统、血液循环、肿瘤需注意',
    '天府': '消化系统、脾胃',
    '太阴': '肝肾、妇科、血液',
    '贪狼': '肝胆、欲望引发的情志病',
    '巨门': '口舌、脾胃、呼吸系统',
    '天相': '皮肤、脾胃、泌尿',
    '天梁': '心脏、血管、需注意肿瘤',
    '七杀': '肝胆、骨骼、意外伤害',
    '破军': '消耗性疾病、泌尿系统、手术',
}


def analyze_health(bazi: dict, chart: dict, year: int = None) -> dict:
    """综合健康分析"""
    elements = bazi['elements']
    day_master = bazi['day_master']
    month_branch = bazi['month']['branch']

    # 1. 五行强弱分析
    weakness = []
    strength_issues = []

    for elem, count in elements.items():
        if count == 0:
            weakness.append(f"{elem}（严重缺损）")
        elif count == 1:
            weakness.append(f"{elem}（较弱）")

    # 2. 日主对应脏腑
    day_organs = STEM_ORGANS.get(day_master, '未知')

    # 3. 疾厄宫分析
    jihe_info = chart.get('疾厄', {})
    jihe_stars = jihe_info.get('stars', [])
    jihe_zhi = jihe_info.get('zhi', '')
    jihe_body = BRANCH_BODY.get(jihe_zhi, '全身')

    jihe_tip = f"疾厄宫{jihe_zhi}宫，主星：{'、'.join(jihe_stars) if jihe_stars else '无主星'}"
    jihe_health = []
    for star in jihe_stars:
        if star in STAR_HEALTH:
            jihe_health.append(STAR_HEALTH[star])

    # 4. 流年分析（如果有）
    year_warnings = []
    if year:
        # 简化：计算该年地支
        year_zhi_idx = (year - 1984) % 12 + 1  # 简化
        # 需要精确计算，这里仅提示
        year_warnings.append(f"{year}年流年健康预警：需关注心血管、情绪波动问题")

    # 5. 综合养护建议
    suggestions = []

    # 五行养护
    if weakness:
        suggestions.append(f"▎五行较弱：{'、'.join(weakness)}，需重点养护对应脏腑")

    # 食伤重者
    month_stem_idx = STEMS.index(bazi['month']['stem'])
    if month_stem_idx < 5:  # 食神月
        suggestions.append("▎食神透出：消化系统需注意，忌暴饮暴食")
    else:  # 伤官月
        suggestions.append("▎伤官透出：神经系统消耗大，忌过度思虑，宜多运动")

    # 水火交战预警（张雪峰案例）
    if bazi['year']['branch'] == '子' or bazi['month']['branch'] == '午':
        suggestions.append("▎⚠️ 子午冲或壬午月柱：心血管系统为薄弱环节，忌高强度情绪波动")

    return {
        'day_organs': day_organs,
        'elements': elements,
        'weakness': weakness,
        'jihe_zhi': jihe_zhi,
        'jihe_stars': jihe_stars,
        'jihe_body': jihe_body,
        'jihe_tip': jihe_tip,
        'jihe_health': jihe_health,
        'year_warnings': year_warnings,
        'suggestions': suggestions,
    }


def format_health_report(analysis: dict, bazi: dict) -> str:
    """格式化健康分析报告"""
    lines = []
    lines.append("【先天体质】")
    lines.append(f"日主：{bazi['day_master']}（{ELEMENTS[bazi['day_master']]}）")
    lines.append(f"日主对应脏腑：{analysis['day_organs']}")
    lines.append("")

    lines.append("【五行强弱】")
    for elem, count in bazi['elements'].items():
        status = '旺' if count >= 3 else ('平' if count >= 2 else '弱')
        lines.append(f"  {elem}：{count}个 {'✅' if count >= 2 else '⚠️' if count == 1 else '❌'}（{status}）")
    lines.append("")

    if analysis['weakness']:
        lines.append(f"【重点关注】五行偏弱：{'、'.join(analysis['weakness'])}")
        lines.append("")

    lines.append("【疾厄宫分析】")
    lines.append(analysis['jihe_tip'])
    lines.append(f"疾厄宫身体部位：{analysis['jihe_body']}")
    if analysis['jihe_health']:
        for tip in analysis['jihe_health']:
            lines.append(f"  → {tip}")
    lines.append("")

    lines.append("【健康建议】")
    for s in analysis['suggestions']:
        lines.append(s)

    if analysis['year_warnings']:
        lines.append("")
        for w in analysis['year_warnings']:
            lines.append(w)

    return '\n'.join(lines)


if __name__ == '__main__':
    from calc.bazi import get_bazi, analyze_wuxing
    from calc.ziwei import build_chart

    test = get_bazi(1984, 4, 4, 10)
    analyze_wuxing(test)
    chart = build_chart(test)

    result = analyze_health(test, chart, 2026)
    print(format_health_report(result, test))
