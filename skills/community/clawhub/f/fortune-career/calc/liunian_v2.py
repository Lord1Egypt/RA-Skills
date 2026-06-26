"""
流年分析 v2：完整地支关系判断
支持：冲、合、刑、害、三合、三会
"""

from calc.ganzhi import STEMS, BRANCHES, STEM_ELEMENTS, BRANCH_ELEMENTS, ZANGAN

STEM_IDX = {s: i for i, s in enumerate(STEMS)}
BRANCH_IDX = {b: i for i, b in enumerate(BRANCHES)}

# 地支关系表
BRANCH_CONFLICT = {  # 六冲
    ('子', '午'): ('冲', '心血管/心脏、情绪波动'),
    ('丑', '未'): ('冲', '脾胃肝胆、消化系统'),
    ('寅', '申'): ('冲', '肝胆/肺部、肢体'),
    ('卯', '酉'): ('冲', '肝肺、神经系统'),
    ('辰', '戌'): ('冲', '脾胃皮肤、精神'),
    ('巳', '亥'): ('冲', '心肾、血液'),
}

BRANCH_HARMONY = {  # 六合
    ('子', '丑'): ('合', '助力合作、运势稳定'),
    ('寅', '亥'): ('合', '事业推进、贵人运'),
    ('卯', '戌'): ('合', '感情/财运'),
    ('辰', '酉'): ('合', '财运人脉'),
    ('午', '未'): ('合', '学业/名声'),
    ('申', '巳'): ('合', '智慧输出'),
}

BRANCH_XING = {  # 三刑
    ('子', '卯'): ('刑', '是非纠纷、健康波折'),
    ('寅', '巳', '申'): ('三刑', '是非官讼、健康意外'),
    ('丑', '未', '戌'): ('三刑', '小人阻碍、脾胃受损'),
    ('午', '午'): ('自刑', '自我纠结、慢性损耗'),
}

BRANCH_HAI = {  # 六害
    ('子', '未'): ('害', '脾胃不和、感情波折'),
    ('丑', '午'): ('害', '心肾不交、事业阻碍'),
    ('寅', '巳'): ('害', '人际是非、呼吸系统'),
    ('卯', '辰'): ('害', '小人暗算、肝胆问题'),
    ('申', '亥'): ('害', '口舌是非、肾水受损'),
    ('酉', '戌'): ('害', '肺大肠、财运阻碍'),
}

# 三合局（生地半合）
BRANCH_SANHE = {
    ('申', '子', '辰'): ('水局', '水旺、财运/感情推进'),
    ('亥', '卯', '未'): ('木局', '木旺、文创/学业进步'),
    ('寅', '午', '戌'): ('火局', '火旺、事业/名声上升'),
    ('巳', '酉', '丑'): ('金局', '金旺、财运/武职有利'),
}

# 三会局
BRANCH_SANHUI = {
    ('寅', '卯', '辰'): ('木会', '木旺'),
    ('巳', '午', '未'): ('火会', '火旺'),
    ('申', '酉', '戌'): ('金会', '金旺'),
    ('亥', '子', '丑'): ('水会', '水旺'),
}

ELEM_NAMES = {'木': '木', '火': '火', '土': '土', '金': '金', '水': '水'}


def get_branch_pair_key(a: str, b: str) -> tuple:
    """标准化配对key（用于冲/合/害的tuple查表）"""
    return tuple(sorted([a, b], key=lambda x: BRANCH_IDX[x]))


def check_relationships(liunian_branch: str, bazi: dict) -> list:
    """
    检查流年地支与命局所有地支的作用关系
    返回描述列表
    """
    results = []
    bazi_branches = [bazi['year']['branch'], bazi['month']['branch'],
                     bazi['day']['branch'], bazi['hour']['branch']]

    # 1. 冲（6组）
    for my_branch in bazi_branches:
        pair = get_branch_pair_key(liunian_branch, my_branch)
        if pair in BRANCH_CONFLICT:
            rel, desc = BRANCH_CONFLICT[pair]
            results.append(f"⚠️ **{rel}**：{desc}")

    # 2. 合（6组）
    for my_branch in bazi_branches:
        pair = get_branch_pair_key(liunian_branch, my_branch)
        if pair in BRANCH_HARMONY:
            rel, desc = BRANCH_HARMONY[pair]
            results.append(f"✅ **{rel}**：{desc}")

    # 3. 害（6组）
    for my_branch in bazi_branches:
        pair = get_branch_pair_key(liunian_branch, my_branch)
        if pair in BRANCH_HAI:
            rel, desc = BRANCH_HAI[pair]
            results.append(f"⚡ **{rel}**：{desc}")

    # 4. 刑（两组常见）
    # 子卯刑
    pair_limao = get_branch_pair_key(liunian_branch, '卯')
    if pair_limao in [('子', '卯')] and '卯' in bazi_branches:
        results.append(f"⚡ **子卯刑**：是非纠纷、健康波折")

    # 5. 三合局检查（流年+命局两个支）
    liunian_elem = BRANCH_ELEMENTS[liunian_branch]
    # 流年是否参与某个三合局
    for he_组成, (ju_name, ju_desc) in BRANCH_SANHE.items():
        count = sum(1 for b in bazi_branches if b in he_组成)
        if liunian_branch in he_组成 and count >= 1:
            # 流年加入命局已有三合
            results.append(f"✨ **半三合{ju_name}**：{ju_desc}")

    return results


def analyze_liunian_v2(liunian: str, bazi: dict, year: int) -> dict:
    """v2版流年分析"""
    stem = liunian[0]
    branch = liunian[1]
    liunian_elem = STEM_ELEMENTS[stem]
    liunian_branch_elem = BRANCH_ELEMENTS[branch]

    # 五行生克关系
    day_stem = bazi['day']['stem']
    day_elem = STEM_ELEMENTS[day_stem]
    SHENG = {'木': '火', '火': '土', '土': '金', '金': '水', '水': '木'}
    KE = {'木': '土', '火': '金', '土': '水', '金': '木', '水': '火'}

    relations = []
    if SHENG.get(day_elem) == liunian_elem:
        relations.append(f"流年天干{stem}（{liunian_elem}）生助日主→有情转化")
    elif KE.get(day_elem) == liunian_elem:
        relations.append(f"流年天干{stem}（{liunian_elem}）克耗日主→压力增大")

    # 地支关系
    branch_effects = check_relationships(branch, bazi)

    return {
        'year': year,
        'liunian': liunian,
        'stem': stem,
        'branch': branch,
        'stem_element': liunian_elem,
        'branch_element': liunian_branch_elem,
        'stem_relations': relations,
        'branch_effects': branch_effects,
    }


def format_liunian_v2(analysis: dict) -> str:
    """格式化v2流年报告"""
    parts = []
    parts.append(f"{analysis['stem_element']}气（{analysis['stem']}）")

    if analysis['stem_relations']:
        parts.append(' | '.join(analysis['stem_relations']))

    if analysis['branch_effects']:
        parts.append(' | '.join(analysis['branch_effects']))
    else:
        parts.append('无明显冲合刑害')

    return f"({analysis['liunian']}）" + ' / '.join(parts)


if __name__ == '__main__':
    from calc.bazi import get_bazi
    from calc.ganzhi import analyze_strength_detailed

    test = get_bazi(1990, 5, 15, 10)
    analyze_strength_detailed(test)

    print("=== 流年分析 v2 测试 ===")
    for y in [2024, 2025, 2026, 2027]:
        offset = y - 1984
        liunian = STEMS[offset % 10] + BRANCHES[offset % 12]
        a = analyze_liunian_v2(liunian, test, y)
        print(f"{y}年 {liunian}：{format_liunian_v2(a)}")
