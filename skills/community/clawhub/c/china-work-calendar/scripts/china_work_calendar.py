#!/usr/bin/env python3
"""
China Work Calendar Calculator
Author: Lin Hui
"""

import sys
import json
from datetime import date, timedelta

# Chinese holidays: year -> list of (start_date_str, name, total_days)
HOLIDAYS = {
    2024: [
        ["2024-01-01", "元旦", 1],
        ["2024-02-10", "春节", 7],
        ["2024-04-04", "清明节", 3],
        ["2024-05-01", "劳动节", 3],
        ["2024-06-10", "端午节", 3],
        ["2024-09-15", "中秋节", 3],
        ["2024-10-01", "国庆节", 7],
    ],
    2025: [
        ["2025-01-01", "元旦", 1],
        ["2025-01-28", "春节", 7],
        ["2025-04-04", "清明节", 3],
        ["2025-05-01", "劳动节", 3],
        ["2025-05-31", "端午节", 3],
        ["2025-10-01", "中秋节+国庆", 8],
    ],
    2026: [
        ["2026-01-01", "元旦", 1],
        ["2026-02-16", "春节", 7],
        ["2026-04-03", "清明节", 3],
        ["2026-05-01", "劳动节", 3],
        ["2026-06-20", "端午节", 3],
        ["2026-09-24", "中秋节", 3],
        ["2026-10-01", "国庆节", 7],
    ],
    2027: [
        ["2027-01-01", "元旦", 1],
        ["2027-02-07", "春节", 7],
        ["2027-04-05", "清明节", 3],
        ["2027-05-01", "劳动节", 3],
        ["2027-06-10", "端午节", 3],
        ["2027-09-15", "中秋节", 3],
        ["2027-10-01", "国庆节", 7],
    ],
}

# Adjusted workdays (weekend shifts) - confirmed by State Council announcements
ADJUSTED_WORKDAYS = {
    "2024-02-04": True, "2024-02-17": True,
    "2024-04-06": True,
    "2024-04-28": True, "2024-05-11": True,
    "2024-06-09": True, "2024-06-23": True,
    "2024-09-14": True, "2024-09-29": True, "2024-10-12": True,
    "2025-01-26": True, "2025-02-01": True, "2025-02-04": True, "2025-02-08": True,
    "2025-04-06": True, "2025-04-27": True,
    "2025-05-03": True, "2025-06-01": True,
    "2025-09-27": True, "2025-10-04": True, "2025-10-11": True,
    "2026-02-15": True, "2026-02-22": True, "2026-02-28": True, "2026-03-01": True,
    "2026-04-05": True, "2026-04-26": True,
    "2026-05-03": True, "2026-06-07": True,
    "2026-06-21": True,
    "2026-09-20": True, "2026-09-27": True,
    "2026-09-26": True, "2026-10-03": True, "2026-10-10": True,
    "2027-02-01": True, "2027-02-07": True, "2027-02-14": True, "2027-02-15": True,
    "2027-04-05": True, "2027-04-25": True,
}


def parse_date(s):
    parts = s.split("-")
    return date(int(parts[0]), int(parts[1]), int(parts[2]))


def is_workday(d):
    ds = d.strftime("%Y-%m-%d")
    if ds in ADJUSTED_WORKDAYS:
        return True
    if d.weekday() >= 5:
        return False
    year_holidays = HOLIDAYS.get(d.year, [])
    for hs, name, days in year_holidays:
        hd = parse_date(hs)
        for i in range(days):
            if hd + timedelta(days=i) == d:
                return False
    return True


def all_holidays_for_year(year):
    result = []
    for hs, name, days in HOLIDAYS.get(year, []):
        hd = parse_date(hs)
        for i in range(days):
            result.append((hd + timedelta(days=i), name))
    return sorted(result)


def count_workdays_in_range(start, end):
    count = 0
    d = start
    while d <= end:
        if is_workday(d):
            count += 1
        d += timedelta(days=1)
    return count


def cmd_workdays(args):
    if len(args) == 2:
        start = parse_date(args[0])
        end = parse_date(args[1])
        count = count_workdays_in_range(start, end)
        print(json.dumps({"start": str(start), "end": str(end), "workdays": count}, ensure_ascii=False, indent=2))
    elif len(args) == 1 and "-" in args[0] and args[0].count("-") == 1:
        parts = args[0].split("-")
        year = int(parts[0])
        month = int(parts[1])
        import calendar
        _, last_day = calendar.monthrange(year, month)
        count = 0
        workdays = []
        for day in range(1, last_day + 1):
            d = date(year, month, day)
            if is_workday(d):
                count += 1
                workdays.append(str(d))
        print(json.dumps({"year": year, "month": month, "workdays_count": count, "workdays": workdays}, ensure_ascii=False, indent=2))
    else:
        print(json.dumps({"error": "Usage: workdays <yyyy-mm-dd> <yyyy-mm-dd> OR workdays <yyyy-mm>"}, ensure_ascii=False))


def cmd_is_workday(args):
    d = parse_date(args[0])
    result = is_workday(d)
    weekday_names = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    print(json.dumps({
        "date": str(d),
        "weekday": weekday_names[d.weekday()],
        "is_workday": result,
        "label": "工作日" if result else "休息日/节假日"
    }, ensure_ascii=False, indent=2))


def cmd_holidays(args):
    year = int(args[0]) if args else date.today().year
    holidays = all_holidays_for_year(year)
    print(json.dumps({
        "year": year,
        "holidays": [{"date": str(d), "name": name} for d, name in holidays]
    }, ensure_ascii=False, indent=2))


def cmd_countdown(args):
    target = parse_date(args[0])
    today = date.today()
    days_left = (target - today).days
    is_wd = is_workday(target)
    print(json.dumps({
        "target": str(target),
        "days_remaining": days_left,
        "is_workday": is_wd,
        "label": "工作日" if is_wd else "休息日/节假日"
    }, ensure_ascii=False, indent=2))


def cmd_next_workday(args):
    from_date = parse_date(args[0]) if args else date.today()
    d = from_date
    for _ in range(30):
        if is_workday(d):
            print(json.dumps({"from": str(from_date), "next_workday": str(d)}, ensure_ascii=False, indent=2))
            return
        d += timedelta(days=1)


def main():
    if len(sys.argv) < 2:
        print("Usage: china_work_calendar.py <command> [args...]")
        sys.exit(1)
    cmd = sys.argv[1]
    args = sys.argv[2:]
    if cmd == "workdays":
        cmd_workdays(args)
    elif cmd == "is-workday":
        cmd_is_workday(args)
    elif cmd == "holidays":
        cmd_holidays(args)
    elif cmd == "countdown":
        cmd_countdown(args)
    elif cmd == "next-workday":
        cmd_next_workday(args)
    else:
        print("Unknown command: " + cmd)


if __name__ == "__main__":
    main()
