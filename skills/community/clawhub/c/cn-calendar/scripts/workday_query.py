#!/usr/bin/env python3
"""
cn-calendar: 中国大陆工作日/节假日查询工具
数据来源：NateScarlet/holiday-cn（基于国务院官方通知）
用法: python3 workday_query.py <命令> [参数]

命令:
  is_workday YYYY-MM-DD          判断某天是否为工作日
  next_workday YYYY-MM-DD        查找某天之后的下一个工作日
  add_workdays YYYY-MM-DD N      从某天起加N个工作日
  count_workdays YYYY-MM-DD YYYY-MM-DD  统计两日期间工作日数量
  deadline YYYY-MM-DD            计算申报截止日（遇节假日顺延）
  month_workdays YYYY-MM          列出某月所有工作日
"""

import sys
import json
from datetime import date, timedelta

# ============================================================
# 数据来源：NateScarlet/holiday-cn
# https://github.com/NateScarlet/holiday-cn
# 引用国务院官方通知原文，数据可信
# ============================================================

# 2025年 - 来源: https://www.gov.cn/zhengce/zhengceku/202411/content_6986383.htm
# isOffDay=true 的日期（法定节假日，非工作日）
HOLIDAYS_2025 = {
    date(2025, 1, 1),   # 元旦
    date(2025, 1, 28), date(2025, 1, 29), date(2025, 1, 30),
    date(2025, 1, 31), date(2025, 2, 1), date(2025, 2, 2),
    date(2025, 2, 3), date(2025, 2, 4),   # 春节
    date(2025, 4, 4), date(2025, 4, 5), date(2025, 4, 6),  # 清明节
    date(2025, 4, 27),  # 劳动节调休（isOffDay=false，但在下方WORKDAYS中）—— 此处是错误占位，见下文
    date(2025, 5, 1), date(2025, 5, 2), date(2025, 5, 3),
    date(2025, 5, 4), date(2025, 5, 5),   # 劳动节
    date(2025, 5, 31), date(2025, 6, 1), date(2025, 6, 2),  # 端午节
    date(2025, 10, 1), date(2025, 10, 2), date(2025, 10, 3),
    date(2025, 10, 4), date(2025, 10, 5), date(2025, 10, 6),
    date(2025, 10, 7), date(2025, 10, 8),  # 国庆节、中秋节
}
# 修正：4月27日是调休工作日，不是节假日
HOLIDAYS_2025.discard(date(2025, 4, 27))

# 2025年调休工作日（isOffDay=false，原为周末但需上班）
WORKDAYS_2025 = {
    date(2025, 1, 26),   # 春节前调休（周日）
    date(2025, 2, 8),    # 春节后调休（周六）
    date(2025, 4, 27),   # 劳动节前调休（周日）
    date(2025, 9, 28),   # 国庆节前调休（周日）
    date(2025, 10, 11),  # 国庆节后调休（周六）
}

# 2026年 - 来源: https://www.gov.cn/zhengce/zhengceku/202511/content_7047091.htm
# isOffDay=true 的日期（法定节假日，非工作日）
HOLIDAYS_2026 = {
    date(2026, 1, 1), date(2026, 1, 2), date(2026, 1, 3),  # 元旦
    date(2026, 2, 15), date(2026, 2, 16), date(2026, 2, 17),
    date(2026, 2, 18), date(2026, 2, 19), date(2026, 2, 20),
    date(2026, 2, 21), date(2026, 2, 22), date(2026, 2, 23),  # 春节
    date(2026, 4, 4), date(2026, 4, 5), date(2026, 4, 6),   # 清明节
    date(2026, 5, 1), date(2026, 5, 2), date(2026, 5, 3),
    date(2026, 5, 4), date(2026, 5, 5),   # 劳动节
    date(2026, 6, 19), date(2026, 6, 20), date(2026, 6, 21),  # 端午节
    date(2026, 9, 25), date(2026, 9, 26), date(2026, 9, 27),  # 中秋节
    date(2026, 10, 1), date(2026, 10, 2), date(2026, 10, 3),
    date(2026, 10, 4), date(2026, 10, 5), date(2026, 10, 6),
    date(2026, 10, 7),  # 国庆节
}

# 2026年调休工作日（isOffDay=false，原为周末但需上班）
WORKDAYS_2026 = {
    date(2026, 1, 4),    # 元旦后调休（周日）
    date(2026, 2, 14),   # 春节前调休（周六）
    date(2026, 2, 28),   # 春节后调休（周六）
    date(2026, 5, 9),    # 劳动节后调休（周六）
    date(2026, 9, 20),   # 国庆节前调休（周日）
    date(2026, 10, 10),  # 国庆节后调休（周六）
}

ALL_HOLIDAYS = HOLIDAYS_2025 | HOLIDAYS_2026
ALL_EXTRA_WORKDAYS = WORKDAYS_2025 | WORKDAYS_2026

# 数据覆盖年份
COVERED_YEARS = {2025, 2026}


def is_workday(d: date) -> bool:
    """判断某天是否为工作日"""
    if d in ALL_HOLIDAYS:
        return False
    if d in ALL_EXTRA_WORKDAYS:
        return True
    return d.weekday() < 5  # 0=周一 … 4=周五


def next_workday(d: date, skip_self=True) -> date:
    """查找下一个工作日，skip_self=True则从d+1开始"""
    current = d + timedelta(days=1) if skip_self else d
    while not is_workday(current):
        current += timedelta(days=1)
    return current


def add_workdays(d: date, n: int) -> date:
    """从d（含）起，向后数n个工作日"""
    current = d
    count = 1 if is_workday(current) else 0
    while count < n:
        current += timedelta(days=1)
        if is_workday(current):
            count += 1
    return current


def count_workdays(start: date, end: date) -> int:
    """统计[start, end]区间内工作日数量"""
    count = 0
    current = start
    while current <= end:
        if is_workday(current):
            count += 1
        current += timedelta(days=1)
    return count


def filing_deadline(base_date: date) -> date:
    """计算纳税申报截止日：若base_date非工作日则顺延"""
    if is_workday(base_date):
        return base_date
    return next_workday(base_date, skip_self=False)


def month_workdays(year: int, month: int) -> list:
    """返回某月所有工作日列表"""
    result = []
    d = date(year, month, 1)
    while d.month == month:
        if is_workday(d):
            result.append(d)
        d += timedelta(days=1)
    return result


WEEKDAY_CN = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]


def check_year_coverage(year: int) -> bool:
    """检查该年份是否在本地数据覆盖范围内"""
    return year in COVERED_YEARS


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(0)

    cmd = args[0]

    # 提取查询年份并检查覆盖
    query_year = None
    if len(args) >= 2:
        try:
            query_year = int(args[1][:4])
        except (ValueError, IndexError):
            pass

    if query_year and not check_year_coverage(query_year):
        print(f"⚠️  {query_year} 年数据不在本地缓存中，需要从 NateScarlet/holiday-cn 获取后更新脚本。")
        print(f"   参考: https://raw.githubusercontent.com/NateScarlet/holiday-cn/master/{query_year}.json")
        sys.exit(2)

    if cmd == "is_workday" and len(args) == 2:
        d = date.fromisoformat(args[1])
        result = is_workday(d)
        wd = WEEKDAY_CN[d.weekday()]
        reason = ""
        if d in ALL_HOLIDAYS:
            reason = "（法定节假日）"
        elif d in ALL_EXTRA_WORKDAYS:
            reason = "（调休工作日）"
        elif d.weekday() >= 5:
            reason = "（周末）"
        print(f"{d} {wd}：{'✅ 工作日' if result else '❌ 非工作日'}{reason}")

    elif cmd == "next_workday" and len(args) == 2:
        d = date.fromisoformat(args[1])
        nwd = next_workday(d)
        print(f"{d} 之后的下一个工作日：{nwd} {WEEKDAY_CN[nwd.weekday()]}")

    elif cmd == "add_workdays" and len(args) == 3:
        d = date.fromisoformat(args[1])
        n = int(args[2])
        result = add_workdays(d, n)
        print(f"从 {d} 起第 {n} 个工作日：{result} {WEEKDAY_CN[result.weekday()]}")

    elif cmd == "count_workdays" and len(args) == 3:
        start = date.fromisoformat(args[1])
        end = date.fromisoformat(args[2])
        count = count_workdays(start, end)
        print(f"{start} 至 {end} 共有 {count} 个工作日")

    elif cmd == "deadline" and len(args) >= 2:
        d = date.fromisoformat(args[1])
        result = filing_deadline(d)
        if result == d:
            print(f"申报截止日：{d} {WEEKDAY_CN[d.weekday()]}（无需顺延）")
        else:
            print(f"申报截止日：{d} 为非工作日，顺延至 {result} {WEEKDAY_CN[result.weekday()]}")

    elif cmd == "month_workdays" and len(args) == 2:
        year, month = map(int, args[1].split("-"))
        days = month_workdays(year, month)
        print(f"{year}年{month}月工作日（共{len(days)}天）：")
        for d in days:
            print(f"  {d} {WEEKDAY_CN[d.weekday()]}")

    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
