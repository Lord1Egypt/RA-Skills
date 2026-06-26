"""
一句话摘要生成
将完整命理报告压缩为3-5句核心信息
适用于微信等短阅读场景
"""

from calc.ganzhi import STEM_ELEMENTS, BRANCH_ELEMENTS, SHENG, KE, MONTH_LING

STEMS = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
BRANCHES = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

# 性格速读关键词
PERSONALITY_SHORT = {
    '甲': '开创冲动、领导型、不服输',
    '乙': '细腻敏感、适应力强、善于变通',
    '丙': '热情外放、执行力快、渴望认可',
    '丁': '内敛直觉、观察力强、有主见',
    '戊': '踏实诚信、务实稳重、抗压强',
    '己': '包容灵活、善于协调、讨厌浮夸',
    '庚': '果断决绝、原则性强、不喜欢绕弯',
    '辛': '审美精致、追求完美、口才好',
    '壬': '好奇心强、适应力强、喜欢自由',
    '癸': '深沉敏锐、直觉强、内向安静',
}

# 五行行业速配
ELEMENT_JOBS = {
    '木': '教育/文化/医药',
    '火': '互联网/能源/餐饮/互联网',
    '土': '地产/建筑/政府/农业',
    '金': '金融/司法/军警/机械',
    '水': '贸易/物流/航海/媒体',
}

# 五行养护重点
ELEMENT_HEALTH_TIPS = {
    '木': '肝胆养护，忌熬夜生气',
    '火': '心血管养护，忌情绪激动',
    '土': '脾胃养护，忌暴饮暴食',
    '金': '肺大肠养护，忌烟酒辛辣',
    '水': '肾泌尿养护，忌过度劳累',
}

# 流年好坏判断关键词
QUALITY_WORDS = {
    '🟢': '利',
    '🟡': '平',
    '🔴': '慎',
}


def get_current_status(dayun_list: list, birth_year: int, current_year: int) -> dict:
    """获取当前大运和流年状态"""
    current_age = current_year - birth_year
    current_du = None
    for du in dayun_list:
        if du['age_start'] <= current_age <= du['age_end']:
            current_du = du
            break
    return current_du


def generate_summary(bazi: dict, dayun_list: list,
                     liunian: str, birth_year: int,
                     current_year: int,
                     health_warnings: list) -> str:
    """
    生成一句话摘要
    格式：性格本质 + 当下运势 + 今年重点 + 健康提醒 + 行动建议
    """
    day_master = bazi['day_master']
    day_elem = STEM_ELEMENTS[day_master]
    strength = bazi.get('strength', '身中')
    strength_tip = bazi.get('strength_tip', '')

    # 1. 性格速读
    personality = PERSONALITY_SHORT.get(day_master, '综合型')

    # 2. 当前大运
    current_du = get_current_status(dayun_list, birth_year, current_year)
    if current_du:
        du_quality = current_du['quality']
        du_desc = f"{current_du['age_start']}-{current_du['age_end']}岁{current_du['stem']}{current_du['branch']}运"
    else:
        du_quality = '🟡'
        du_desc = '大运待起'

    # 3. 今年流年
    ln_stem, ln_branch = liunian[0], liunian[1]
    ln_elem_stem = STEM_ELEMENTS[ln_stem]
    ln_elem_branch = BRANCH_ELEMENTS[ln_branch]

    # 4. 健康重点（只说有问题的）
    health_focus = health_warnings if health_warnings else []

    # 5. 最旺五行行业
    dominant = max(bazi['elements'], key=bazi['elements'].get)
    top_industry = ELEMENT_JOBS.get(dominant, '综合')

    # ========== 组装摘要 ==========
    lines = []

    # 第1句：性格+行业
    lines.append(f"「{day_master}日主」—— {personality}，五行{day_elem}气旺盛，最适合{top_industry}方向发展")

    # 第2句：当前大运
    du_word = {'🟢': '顺利', '🟡': '平稳', '🔴': '波折'}.get(du_quality, '一般')
    du_detail = current_du['quality_tip'].split('，')[1] if current_du else ''
    lines.append(f"当前大运：{du_desc}，整体{du_word}，{du_detail}")

    # 第3句：今年运势
    ln_word = '有机会' if ln_elem_stem in [day_elem] or SHENG.get(day_elem) == ln_elem_stem else '有挑战'
    lines.append(f"今年流年{current_year}年{liunian}，{ln_elem_stem}气主导，{ln_word}，{ln_branch}地支{ln_elem_branch}需关注")

    # 第4句：健康提醒（如果有）
    if health_focus:
        weakest = bazi.get('strength', '身中')
        tips = ELEMENT_HEALTH_TIPS.get(day_elem, '注意休息')
        lines.append(f"健康重点：{tips}，今年{ln_branch}字运势需重点关注")
    else:
        lines.append(f"健康状态：整体平稳，{ELEMENT_HEALTH_TIPS.get(day_elem, '注意休息')}")

    # 第5句：行动建议
    if du_quality == '🟢':
        action = '宜主动出击，适合换赛道/争取晋升/尝试新方向'
    elif du_quality == '🔴':
        action = '宜守成，不宜冒险，优先保住现有成果，修炼内功'
    else:
        action = '稳步推进，专注本业，有机会可小试，但勿冒进'

    lines.append(f"行动建议：{action}")

    return '\n'.join(lines)


if __name__ == '__main__':
    from calc.bazi import get_bazi
    from calc.ganzhi import analyze_strength_detailed
    from calc.dayun_v2 import get_dayun_v2
    from calc.bazi import STEMS, BRANCHES

    test = get_bazi(1990, 5, 15, 10)
    test['_year'] = 1990; test['_month'] = 5; test['_day'] = 15
    analyze_strength_detailed(test)
    dayun = get_dayun_v2(test, '男')

    # 今年流年：丙午
    offset = 2026 - 1984
    liunian = STEMS[offset % 10] + BRANCHES[offset % 12]

    health_warnings = ['心脑血管']  # 假设有警告
    summary = generate_summary(test, dayun, liunian, 1990, 2026, health_warnings)
    print("=== 一句话摘要 ===")
    print(summary)
