"""
职业分析框架
基于八字和紫微斗数输出职业方向、性格特点、事业走势
"""

from calc.bazi import STEMS, BRANCHES, ELEMENTS, BRANCH_ELEMENTS

# 性格关键词库
STEM_PERSONALITY = {
    '甲': '开创型 · 直来直去 · 领导欲强 · 上进不服输',
    '乙': '细腻型 · 善于变通 · 配合度高 · 善于思考',
    '丙': '热烈型 · 执行力快 · 表面外向 · 内心需要认可',
    '丁': '内敛型 · 观察力强 · 温和但有主见 · 善于幕后',
    '戊': '稳重型 · 踏实诚信 · 物质导向 · 抗压能力强',
    '己': '包容型 · 善于协调 · 务实灵活 · 讨厌浮夸',
    '庚': '刚烈型 · 果断决绝 · 原则性强 · 不喜欢绕弯子',
    '辛': '精致型 · 审美敏锐 · 追求完美 · 善于表达',
    '壬': '流动型 · 好奇心强 · 适应力强 · 喜欢自由',
    '癸': '深沉型 · 直觉敏锐 · 善于洞察 · 内向安静',
}

# 食伤星性格
STEM_EATJOY = {
    '甲': '食神：温和表达、享受生活、口福好',
    '乙': '伤官：才华外露、表演欲强、不服管教',
    '丙': '食神：热情洋溢、表达直接、喜欢被认可',
    '丁': '伤官：才华横溢、想法多、容易挑剔',
    '戊': '食神：务实沉稳、做事有耐心、不喜表现',
    '己': '伤官：灵活变通、脑子快、善于批判',
    '庚': '食神：直接爽快、执行力强、不喜欢拖沓',
    '辛': '伤官：审美精致、口才流利、追求独特',
    '壬': '食神：自由洒脱、兴趣广泛、不拘小节',
    '癸': '伤官：思想深邃、直觉敏锐、善于分析',
}

# 八字十神职业倾向
TEN_GOD_JOBS = {
    '比': ['合伙人创业', '专业技术', '自由职业', '销售'],
    '劫': ['体力劳动', '竞技体育', '安保', '执行'],
    '食': ['创意设计', '餐饮美食', '教育培训', '咨询顾问'],
    '伤': ['技术创新', '艺术创作', '写作出版', '律师'],
    '财': ['企业管理', '财务金融', '销售', '商务'],
    '才': ['艺术设计', '审美相关', '品牌管理', '媒体'],
    '官': ['公务员', '企业管理', '法律合规', '组织管理'],
    '杀': ['司法公安', '军事', '执法', '高压职业'],
    '枭': ['学术研究', '医疗健康', '技术研发', '神秘学'],
    '印': ['教育', '文化', '出版', '政府机构'],
}

# 紫微主星事业特征
STAR_CAREER = {
    '紫微': '管理型 · 权力欲望强 · 适合高层管理、政府、决策',
    '天机': '智囊型 · 策划能力强 · 适合策划、咨询、技术',
    '太阳': '领导型 · 社交能力强 · 适合外交、教育、媒体',
    '武曲': '刚毅型 · 执行力强 · 适合金融、军警、技术',
    '天同': '温和型 · 人际和谐 · 适合服务、教育、艺术',
    '廉贞': '复杂型 · 适应力强 · 适合销售、公关、自由职业',
    '天府': '保守型 · 管理稳健 · 适合财务、行政、地产',
    '太阴': '内敛型 · 思考深沉 · 适合幕后、财务、艺术',
    '贪狼': '欲望型 · 野心勃勃 · 适合商业、销售、公关',
    '巨门': '口才型 · 争论能力强 · 适合律师、销售、教育',
    '天相': '协调型 · 辅佐能力强 · 适合行政、助理、服务',
    '天梁': '稳定型 · 监督能力强 · 适合监察、稳健投资',
    '七杀': '开创型 · 冲击力强 · 适合创业、军警、外科',
    '破军': '破坏型 · 变革力强 · 适合转型、创新、破坏性建设',
}

# 五行行业倾向
ELEMENT_JOBS = {
    '木': '教育、文化出版、农业造林、医药卫生、宗教',
    '火': '能源、照明、电子、互联网、餐饮、化妆品',
    '土': '房地产、建筑、矿业、农业、仓储、政府',
    '金': '金融、珠宝、五金器械、汽车、司法、军队',
    '水': '贸易、物流、运输、航海、旅游、媒体',
}


def analyze_career(bazi: dict, chart: dict) -> dict:
    """综合职业分析"""
    day_master = bazi['day_master']
    year_stem = bazi['year']['stem']
    month_stem = bazi['month']['stem']
    strength = bazi.get('strength', '身中')
    elements = bazi['elements']
    main_stars = chart['_meta']['main_stars']
    geshi = chart.get('_geshi', ['普通格局'])

    # 1. 性格本质
    personality = STEM_PERSONALITY.get(day_master, '未知')

    # 2. 食伤性格
    month_stem_idx = STEMS.index(month_stem)
    if month_stem_idx < 5:  # 甲乙丙丁戊
        eatjoy = f"月柱透出{month_stem}：{STEM_EATJOY.get(month_stem, '')}"
    else:  # 己庚辛壬癸
        eatjoy = f"月柱透出{month_stem}：{STEM_EATJOY.get(month_stem, '')}"

    # 3. 日主强弱与职业选择
    if strength == '身强':
        strength_tip = '身强则宜主动出击，适合开创性、竞争性工作'
    elif strength == '身弱':
        strength_tip = '身弱则宜稳中求进，适合配合型、稳定型工作'
    else:
        strength_tip = '身中则进退自如，适应面广'

    # 4. 五行最旺 → 最适合行业
    dominant = max(elements, key=elements.get)
    recommended_industries = ELEMENT_JOBS.get(dominant, '')

    # 5. 命宫主星事业特征
    minggong_zhi = chart.get('命', {}).get('zhi', '')
    minggong_stars = chart.get('命', {}).get('stars', [])
    minggong_career = '、'.join([STAR_CAREER.get(s, s) for s in minggong_stars]) if minggong_stars else '普通命宫'

    # 6. 迁移宫（外地/出行发展）
    qianyi_stars = chart.get('迁移', {}).get('stars', [])
    qianyi_tip = f"迁移宫主星：{'、'.join(qianyi_stars) if qianyi_stars else '无主星'}，"
    if qianyi_stars:
        for star in qianyi_stars:
            if star in STAR_CAREER:
                qianyi_tip += STAR_CAREER[star]
                break
    else:
        qianyi_tip += '宜本地发展'

    # 7. 事业宫
    shiye_stars = chart.get('事业', {}).get('stars', [])
    shiye_tip = f"事业宫主星：{'、'.join(shiye_stars) if shiye_stars else '无主星'}"

    # 8. 综合建议
    suggestions = []

    # 强弱建议
    suggestions.append(f"▎强弱判断：{strength} → {strength_tip}")

    # 行业建议
    suggestions.append(f"▎推荐行业（五行{dominant}旺）：{recommended_industries}")

    # 命宫建议
    if minggong_stars:
        suggestions.append(f"▎命宫主星：{'、'.join(minggong_stars)} → {minggong_career.split('·')[0] if '·' in minggong_career else minggong_career}")

    # 格局建议
    if geshi and geshi[0] != '普通格局':
        suggestions.append(f"▎命格：{'、'.join(geshi)} → 适合挑战性工作，不宜安于现状")

    return {
        'personality': personality,
        'eatjoy': eatjoy,
        'strength': strength,
        'strength_tip': strength_tip,
        'dominant_element': dominant,
        'industries': recommended_industries,
        'minggong_stars': minggong_stars,
        'minggong_career': minggong_career,
        'qianyi_tip': qianyi_tip,
        'shiye_tip': shiye_tip,
        'shiye_stars': shiye_stars,
        'suggestions': suggestions,
        'geshi': geshi,
    }


def format_career_report(analysis: dict, bazi: dict) -> str:
    """格式化输出职业分析报告"""
    lines = []
    lines.append("【职业性格分析】")
    lines.append(f"日主：{bazi['day_master']}（{ELEMENTS[bazi['day_master']]}）")
    lines.append(f"性格本质：{analysis['personality']}")
    lines.append(f"食伤表现：{analysis['eatjoy']}")
    lines.append("")

    lines.append("【事业特征】")
    lines.append(f"命宫主星：{'、'.join(analysis['minggong_stars']) if analysis['minggong_stars'] else '无主星'}")
    lines.append(f"事业宫：{analysis['shiye_tip']}")
    lines.append(f"迁移宫：{analysis['qianyi_tip']}")
    lines.append(f"命格格局：{'、'.join(analysis['geshi']) if analysis['geshi'] else '普通格局'}")
    lines.append("")

    lines.append("【五行与行业】")
    lines.append(f"日主五行：{ELEMENTS[bazi['day_master']]}")
    lines.append(f"最旺五行：{analysis['dominant_element']}（{bazi['elements'][analysis['dominant_element']]}个）")
    lines.append(f"推荐行业：{analysis['industries']}")
    lines.append("")

    lines.append("【综合建议】")
    for s in analysis['suggestions']:
        lines.append(s)

    return '\n'.join(lines)


if __name__ == '__main__':
    from calc.bazi import get_bazi, analyze_wuxing
    from calc.ziwei import build_chart, analyze_geshi

    # 测试
    test = get_bazi(1984, 4, 4, 10)
    analyze_wuxing(test)
    chart = build_chart(test)
    chart['_geshi'] = analyze_geshi(chart)

    result = analyze_career(test, chart)
    print(format_career_report(result, test))
