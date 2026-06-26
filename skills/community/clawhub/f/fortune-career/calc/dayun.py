"""
大运流年分析模块
大运：10年一步运，从出生月开始推算
流年：每一年的天干地支
"""

from typing import List, Dict
from calc.bazi import STEMS, BRANCHES

STEMS10 = STEMS  # 甲乙丙丁戊己庚辛壬癸
BRANCHES12 = BRANCHES  # 子丑寅卯辰巳午未申酉戌亥

# 天干索引
STEM_IDX = {s: i for i, s in enumerate(STEMS10)}
BRANCH_IDX = {b: i for i, b in enumerate(BRANCHES12)}


def get_dayun(bazi: dict, gender: str = '男') -> List[dict]:
    """
    计算大运
    bazi: 八字字典（来自 bazi.py）
    gender: '男' 或 '女'

    算法：
    1. 找月柱天干索引、月落地支索引
    2. 阳男阴女顺排（天干/地支各+1），阴男阳女逆排（各-1）
    3. 每步大运管10年
    4. 起始年龄 = 3 + (下一步干序 - 月干序) % 10
    """
    month_stem = bazi['month']['stem']
    month_branch = bazi['month']['branch']
    month_stem_idx = STEM_IDX[month_stem]
    month_branch_idx = BRANCH_IDX[month_branch]

    # 阴阳：甲丙戊庚壬为阳，乙丁己辛癸为阴
    day_stem = bazi['day']['stem']
    is_yang_day = STEM_IDX[day_stem] % 2 == 0  # 0=甲=阳, 2=丙=阳, ...

    # 阳男阴女顺排，阴男阳女逆排
    if (gender == '男' and is_yang_day) or (gender == '女' and not is_yang_day):
        direction = 1  # 顺
    else:
        direction = -1  # 逆

    dayun_list = []

    # 起始年龄 = 3 + 差值（至少为0）
    # 下一步天干索引
    next_stem_idx = (month_stem_idx + direction) % 10
    # 差值：跨越的步数（每步+1或-1，需取正值）
    diff = (next_stem_idx - month_stem_idx) % 10 if direction == 1 else (month_stem_idx - next_stem_idx) % 10
    start_age = 3 + diff

    for i in range(10):
        # 第i步大运
        stem_idx = (month_stem_idx + direction * (i + 1)) % 10
        branch_idx = (month_branch_idx + direction * (i + 1)) % 12

        age_start = start_age + i * 10
        age_end = age_start + 9

        dayun_list.append({
            'stem': STEMS10[stem_idx],
            'branch': BRANCHES12[branch_idx],
            'age_start': age_start,
            'age_end': age_end,
            'direction': '顺' if direction == 1 else '逆',
        })

    return dayun_list


def get_liunian(year: int, birth_year: int) -> dict:
    """
    计算流年（某一年）
    year: 要查询的年份
    birth_year: 出生年份
    """
    # 年干：基准年（1984=甲子年），距1984的年数模10
    offset = year - 1984
    year_stem_idx = offset % 10
    year_branch_idx = offset % 12

    return {
        'stem': STEMS10[year_stem_idx],
        'branch': BRANCHES12[year_branch_idx],
        'year': year,
    }


def get_current_liunian(birth_year: int, current_year: int = 2026) -> List[dict]:
    """
    获取从出生到今年的流年列表
    """
    results = []
    for y in range(birth_year, current_year + 1):
        results.append(get_liunian(y, birth_year))
    return results


# 流年与八字的作用关系（简化版）
BRANCH_CONFLICT = {
    ('子', '午'): '子午冲 - 心血管/心脏问题，情绪波动大',
    ('丑', '未'): '丑未冲 - 脾胃/肝胆问题',
    ('寅', '申'): '寅申冲 - 肝胆/肺部问题',
    ('卯', '酉'): '卯酉冲 - 肝肺不和，神经/呼吸',
    ('辰', '戌'): '辰戌冲 - 脾胃皮肤病',
    ('巳', '亥'): '巳亥冲 - 心脏血液问题',
}

BRANCH_HARMONY = {
    ('子', '丑'): '子丑合 - 助力合作，运势稳定',
    ('寅', '亥'): '寅亥合 - 事业推进，贵人运',
    ('卯', '戌'): '卯戌合 - 感情/财运',
    ('辰', '酉'): '辰酉合 - 财运人脉',
    ('午', '未'): '午未合 - 学业/名声',
    ('申', '巳'): '申巳合 - 智慧输出',
}


def analyze_liunian_influence(liunian: str, bazi: dict, year: int) -> dict:
    """
    分析流年对八字的影响
    liunian: 流年干支字符串，如 '丙午'
    bazi: 八字字典
    year: 年份
    """
    stem = liunian[0]
    branch = liunian[1]

    effects = []

    # 1. 流年地支与命局地支的冲合
    bazi_branches = [bazi['year']['branch'], bazi['month']['branch'],
                     bazi['day']['branch'], bazi['hour']['branch']]

    conflict = None
    harmony = None
    for my_branch in bazi_branches:
        pair = tuple(sorted([branch, my_branch], key=lambda x: BRANCH_IDX[x]))
        # Check conflict
        for c_pair, desc in BRANCH_CONFLICT.items():
            if set(c_pair) == set([branch, my_branch]):
                conflict = desc
                effects.append(f"⚠️ {desc}")
        # Check harmony
        for h_pair, desc in BRANCH_HARMONY.items():
            if set(h_pair) == set([branch, my_branch]):
                effects.append(f"✅ {desc}")

    # 2. 流年天干生克
    day_stem = bazi['day']['stem']
    day_stem_idx = STEM_IDX[day_stem]

    # 3. 五行影响
    BRANCH_ELEMENTS = {
        '子': '水', '丑': '土', '寅': '木', '卯': '木', '辰': '土',
        '巳': '火', '午': '火', '未': '土', '申': '金', '酉': '金',
        '戌': '土', '亥': '水'
    }
    STEM_ELEMENTS = {
        '甲': '木', '乙': '木', '丙': '火', '丁': '火', '戊': '土',
        '己': '土', '庚': '金', '辛': '金', '壬': '水', '癸': '水'
    }

    liunian_elem = STEM_ELEMENTS[stem]
    bazi_elems = [STEM_ELEMENTS[bazi['year']['stem']], STEM_ELEMENTS[bazi['month']['stem']],
                  STEM_ELEMENTS[bazi['day']['stem']], STEM_ELEMENTS[bazi['hour']['stem']]]

    # 流年地支五行
    liunian_branch_elem = BRANCH_ELEMENTS[branch]

    return {
        'year': year,
        'liunian': liunian,
        'stem': stem,
        'branch': branch,
        'stem_element': liunian_elem,
        'branch_element': liunian_branch_elem,
        'effects': effects if effects else ['平稳过渡'],
    }


def format_dayun_report(dayun_list: List[dict], current_year: int = 2026,
                         birth_year: int = 1990) -> str:
    """格式化大运报告（无标题，供嵌入使用）"""
    lines = []

    # 找当前年龄落在哪步大运
    current_age = current_year - birth_year
    for du in dayun_list:
        marker = ''
        if du['age_start'] <= current_age <= du['age_end']:
            marker = ' ◀ 当前'
        lines.append(f"  {du['age_start']}-{du['age_end']}岁：{du['stem']}{du['branch']}（{du['direction']}运）{marker}")

    return '\n'.join(lines)


if __name__ == '__main__':
    from calc.bazi import get_bazi, analyze_wuxing

    test = get_bazi(1990, 5, 15, 10)
    analyze_wuxing(test)

    print("大运：")
    dayun = get_dayun(test, '男')
    for du in dayun:
        print(f"  {du['age_start']}-{du['age_end']}岁：{du['stem']}{du['branch']}")

    print("\n流年（2024-2027）：")
    for y in [2024, 2025, 2026, 2027]:
        ln = get_liunian(y, 1990)
        print(f"  {y}年：{ln['stem']}{ln['branch']}")

    print("\n流年影响分析（2026）：")
    analysis = analyze_liunian_influence('丙午', test, 2026)
    print(f"  流年：{analysis['liunian']}")
    print(f"  天干五行：{analysis['stem_element']}")
    print(f"  地支五行：{analysis['branch_element']}")
    print(f"  影响：{analysis['effects']}")
