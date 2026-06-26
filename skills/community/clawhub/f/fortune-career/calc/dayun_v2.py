"""
大运分析 v2：
1. 精确起运年龄（节气算法）
2. 每步运定性（好坏+建议）
"""

from calc.ganzhi import STEMS, BRANCHES, STEM_ELEMENTS, BRANCH_ELEMENTS, ZANGAN, MONTH_LING, SHENG, KE

STEM_IDX = {s: i for i, s in enumerate(STEMS)}
BRANCH_IDX = {b: i for i, b in enumerate(BRANCHES)}


def get_accurate_dayun_start(gender: str, bazi: dict) -> int:
    """
    精确起运年龄计算

    原理：
    - 大运从出生后第1个"节"开始起算
    - 起运月数 = (出生到下一个节的天数) / 3（每月按3天算）
    - 岁数 = 3 + 起运月数（向下取整）

    简化版：用24节气判断
    - 寅月节：立春（2月4日左右）
    - 卯月节：惊蛰（3月5日左右）
    - 辰月节：清明（4月5日左右）
    - 巳月节：立夏（5月5日左右）
    - 午月节：芒种（6月5日左右）
    - 未月节：小暑（7月7日左右）
    - 申月节：立秋（8月7日左右）
    - 酉月节：白露（9月7日左右）
    - 戌月节：寒露（10月8日左右）
    - 亥月节：立冬（11月7日左右）
    - 子月节：大雪（12月7日左右）
    - 丑月节：小寒（1月5日左右）

    我们用简化近似：出生月距下一个节的天数/30 ≈ 月数
    """
    month = None
    for i, b in enumerate(BRANCHES):
        if b == bazi['month']['branch']:
            month = i + 1  # 1=子月, 2=丑月...
            break

    # 节气近似日期（每月两个节气，前一个为节）
    JIEQI_APPROX = {
        1: 5,   # 小寒 ~ 1月5日
        2: 4,   # 立春 ~ 2月4日
        3: 5,   # 惊蛰 ~ 3月5日
        4: 5,   # 清明 ~ 4月5日
        5: 5,   # 立夏 ~ 5月5日
        6: 5,   # 芒种 ~ 6月5日
        7: 7,   # 小暑 ~ 7月7日
        8: 7,   # 立秋 ~ 8月7日
        9: 7,   # 白露 ~ 9月7日
        10: 8,  # 寒露 ~ 10月8日
        11: 7,  # 立冬 ~ 11月7日
        12: 7,  # 大雪 ~ 12月7日
    }

    import datetime
    birth_date = datetime.date(bazi.get('_year', 1990), bazi.get('_month', 5), bazi.get('_day', 15))
    birth_month = birth_date.month

    # 计算下一个节
    year = birth_date.year
    next_month = (birth_month % 12) + 1
    next_jieqi_day = JIEQI_APPROX.get(next_month, 5)
    try:
        next_jieqi = datetime.date(year if next_month > birth_month else year + 1,
                                   next_month, next_jieqi_day)
    except:
        next_jieqi = datetime.date(year if next_month > birth_month else year + 1,
                                   next_month, 28)

    days_to_jieqi = (next_jieqi - birth_date).days
    if days_to_jieqi < 0:
        days_to_jieqi += 365

    # 起运月数 = 天数/3（向下取整）
    start_months = max(0, days_to_jieqi // 3)
    start_age = 3 + start_months

    return start_age


def get_dayun_v2(bazi: dict, gender: str = '男') -> list:
    """
    v2版大运计算
    - 精确起运年龄
    - 每步运定性（好/坏/平）
    """
    month_stem = bazi['month']['stem']
    month_branch = bazi['month']['branch']
    month_stem_idx = STEM_IDX[month_stem]
    month_branch_idx = BRANCH_IDX[month_branch]
    day_stem = bazi['day']['stem']
    is_yang_day = STEM_IDX[day_stem] % 2 == 0

    # 顺逆
    if (gender == '男' and is_yang_day) or (gender == '女' and not is_yang_day):
        direction = 1
    else:
        direction = -1

    # 精确起运年龄
    start_age = get_accurate_dayun_start(gender, bazi)

    dayun_list = []
    day_master_elem = STEM_ELEMENTS[day_stem]

    for i in range(10):
        stem_idx = (month_stem_idx + direction * (i + 1)) % 10
        branch_idx = (month_branch_idx + direction * (i + 1)) % 12

        age_start = start_age + i * 10
        age_end = age_start + 9

        stem = STEMS[stem_idx]
        branch = BRANCHES[branch_idx]
        stem_elem = STEM_ELEMENTS[stem]
        branch_elem = BRANCH_ELEMENTS[branch]

        # 定性：看地支五行对日主的影响
        # 生助日主 = 好，克耗日主 = 差，同类 = 平
        good_count = 0
        bad_count = 0

        # 天干对日主
        if SHENG.get(stem_elem) == day_master_elem or stem_elem == day_master_elem:
            good_count += 1
        elif KE.get(stem_elem) == day_master_elem:
            bad_count += 1

        # 地支对日主
        if SHENG.get(branch_elem) == day_master_elem or branch_elem == day_master_elem:
            good_count += 1
        elif KE.get(branch_elem) == day_master_elem:
            bad_count += 1

        if good_count >= 2:
            quality = '🟢好运'
            quality_tip = f'天干{stem}（{stem_elem}）、地支{branch}（{branch_elem}），助力日主'
        elif bad_count >= 2:
            quality = '🔴低谷'
            quality_tip = f'天干{stem}（{stem_elem}）、地支{branch}（{branch_elem}），克耗日主'
        else:
            quality = '🟡平缓'
            quality_tip = f'天干{stem}（{stem_elem}）、地支{branch}（{branch_elem}），平稳过渡'

        dayun_list.append({
            'stem': stem,
            'branch': branch,
            'stem_elem': stem_elem,
            'branch_elem': branch_elem,
            'age_start': age_start,
            'age_end': age_end,
            'direction': '顺' if direction == 1 else '逆',
            'quality': quality,
            'quality_tip': quality_tip,
        })

    return dayun_list


def format_dayun_v2(dayun_list: list, current_year: int, birth_year: int) -> str:
    """格式化v2大运报告"""
    current_age = current_year - birth_year
    lines = []
    for du in dayun_list:
        marker = ''
        if du['age_start'] <= current_age <= du['age_end']:
            marker = ' ◀ 当前'
        lines.append(
            f"  {du['age_start']}-{du['age_end']}岁："
            f"{du['stem']}{du['branch']}（{du['direction']}运）"
            f" {du['quality']}{marker}"
        )
        lines.append(f"    {du['quality_tip']}")
    return '\n'.join(lines)


if __name__ == '__main__':
    from calc.bazi import get_bazi
    from calc.ganzhi import analyze_strength_detailed

    test = get_bazi(1990, 5, 15, 10)
    test['_year'] = 1990
    test['_month'] = 5
    test['_day'] = 15

    print(f"八字: {test['str']}")
    print(f"起运年龄: {get_accurate_dayun_start('男', test)}岁")
    print()
    dayun = get_dayun_v2(test, '男')
    print(format_dayun_v2(dayun, 2026, 1990))
