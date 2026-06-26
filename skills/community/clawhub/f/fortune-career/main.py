#!/usr/bin/env python3
"""
fortune-career skill 主入口
v2.1: 一句话摘要模式（--brief）
"""

import sys
import datetime
from calc.bazi import get_bazi
from calc.ganzhi import analyze_strength_detailed
from calc.ziwei import build_chart, analyze_geshi
from calc.lunar import parse_birth_date
from calc.dayun_v2 import get_dayun_v2, format_dayun_v2
from calc.liunian_v2 import analyze_liunian_v2, format_liunian_v2
from scripts.career_analysis import analyze_career, format_career_report
from scripts.health_analysis import analyze_health, format_health_report
from scripts.summary import generate_summary
from calc.bazi import STEMS, BRANCHES


def run_full_analysis(year: int, month: int, day: int, hour: int,
                      gender: str = '男', mode: str = 'all',
                      is_lunar: bool = False,
                      brief: bool = False) -> str:
    """执行命理分析"""
    current_year = datetime.datetime.now().year
    lunar_note = '（农历）' if is_lunar else ''

    bazi = get_bazi(year, month, day, hour)
    bazi['_year'] = year
    bazi['_month'] = month
    bazi['_day'] = day

    analyze_strength_detailed(bazi)
    chart = build_chart(bazi)
    geshi = analyze_geshi(chart)
    chart['_geshi'] = geshi

    dayun = get_dayun_v2(bazi, gender)

    # 流年
    offset = current_year - 1984
    liunian = STEMS[offset % 10] + BRANCHES[offset % 12]
    ln_analysis = analyze_liunian_v2(liunian, bazi, current_year)

    health_result = analyze_health(bazi, chart, year=current_year)

    # ========== brief 摘要模式 ==========
    if brief:
        health_warnings = []
        if health_result.get('jihe_health'):
            health_warnings = health_result['jihe_health']
        return generate_summary(
            bazi, dayun, liunian, year, current_year, health_warnings
        )

    # ========== 完整报告模式 ==========
    lines = []
    lines.append(f"**出生信息：{year}年{month}月{day}日 {hour}时**{lunar_note}")
    lines.append(f"**八字：{bazi['str']}**\n")

    # 大运
    lines.append("---")
    lines.append("**【大运走势】**")
    lines.append(format_dayun_v2(dayun, current_year, year))

    # 流年
    lines.append("")
    lines.append("**【近三年流年】**")
    for y in [current_year - 1, current_year, current_year + 1]:
        off = y - 1984
        ln = STEMS[off % 10] + BRANCHES[off % 12]
        a = analyze_liunian_v2(ln, bazi, y)
        marker = ' ◀ 今年' if y == current_year else ''
        lines.append(f"  {y}年 {ln}：{format_liunian_v2(a)}{marker}")

    # 职业分析
    if mode in ('all', 'career'):
        lines.append("")
        lines.append("---")
        lines.append("**【职业分析】**\n")
        career = analyze_career(bazi, chart)
        lines.append(format_career_report(career, bazi))

    # 健康分析
    if mode in ('all', 'health'):
        lines.append("")
        lines.append("---")
        lines.append("**【健康分析】**\n")
        lines.append(format_health_report(health_result, bazi))

    lines.append("")
    lines.append("---")
    lines.append("*本分析基于传统命理学规则框架，仅供参考*")

    return '\n'.join(lines)


def cmd_main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法:")
        print("  python3 main.py 算命 <出生信息> [性别]")
        print("  python3 main.py 摘要 <出生信息> [性别]   ← 一句话版")
        print("  python3 main.py 职业 <出生信息> [性别]")
        print("  python3 main.py 健康 <出生信息> [性别]")
        print()
        print("示例:")
        print("  python3 main.py 算命 1990年5月15日10时")
        print("  python3 main.py 摘要 1990年5月15日10时")
        print("  python3 main.py 摘要 农历1990年5月15日10时 女")
        sys.exit(1)

    cmd = sys.argv[1]
    birth_text = sys.argv[2] if len(sys.argv) > 2 else sys.argv[1]
    gender = sys.argv[3] if len(sys.argv) > 3 else '男'

    if birth_text in ('算命', '摘要', '职业', '健康', 'all'):
        print(f"用法: python3 main.py 算命/摘要 <出生信息> [性别]")
        sys.exit(1)

    try:
        year, month, day, hour, is_lun = parse_birth_date(birth_text)
    except Exception as e:
        print(f"解析失败：{e}")
        sys.exit(1)

    mode_map = {'算命': 'all', '摘要': 'brief', '职业': 'career', '健康': 'health', 'all': 'all'}
    mode = mode_map.get(cmd, 'all')
    brief = (cmd == '摘要')

    result = run_full_analysis(year, month, day, hour, gender, mode, is_lun, brief)
    print(result)


if __name__ == '__main__':
    cmd_main()
