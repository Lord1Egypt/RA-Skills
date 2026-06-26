#!/usr/bin/env python3
"""Chinese holiday calendar — query and cron helper."""

import sys
import json
from datetime import date, timedelta, datetime
from pathlib import Path

# Fix encoding on Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# ── Holiday data ────────────────────────────────────────────────────────────
# Source: 国务院办公厅 official announcements
# Format: each holiday has name, dates (off), workdays (调休上班)

HOLIDAYS = {
    2025: [
        {
            "name": "元旦", "emoji": "🎉",
            "off": ["2025-01-01"],
            "work": [],  # 无调休
        },
        {
            "name": "春节", "emoji": "🧧",
            "off": ["2025-01-28", "2025-01-29", "2025-01-30", "2025-01-31",
                    "2025-02-01", "2025-02-02", "2025-02-03", "2025-02-04"],
            "work": ["2025-01-26"],  # 周日上班
        },
        {
            "name": "清明节", "emoji": "🌿",
            "off": ["2025-04-04", "2025-04-05", "2025-04-06"],
            "work": [],
        },
        {
            "name": "劳动节", "emoji": "💪",
            "off": ["2025-05-01", "2025-05-02", "2025-05-03", "2025-05-04", "2025-05-05"],
            "work": ["2025-04-27"],  # 周日上班
        },
        {
            "name": "端午节", "emoji": "🐉",
            "off": ["2025-05-31", "2025-06-01", "2025-06-02"],
            "work": [],
        },
        {
            "name": "中秋节", "emoji": "🥮",
            "off": ["2025-10-06"],  # 与国庆连休
            "work": [],
        },
        {
            "name": "国庆节", "emoji": "🇨🇳",
            "off": ["2025-10-01", "2025-10-02", "2025-10-03", "2025-10-04",
                    "2025-10-05", "2025-10-06", "2025-10-07", "2025-10-08"],
            "work": ["2025-09-28", "2025-10-11"],  # 周日、周六上班
        },
    ],
    2026: [
        # 2026年放假安排尚未公布，以下为基于惯例的预测，国务院公布后需更新
        {
            "name": "元旦", "emoji": "🎉",
            "off": ["2026-01-01", "2026-01-02", "2026-01-03"],
            "work": [],
            "predicted": True,
        },
        {
            "name": "春节", "emoji": "🧧",
            "off": ["2026-02-14", "2026-02-15", "2026-02-16", "2026-02-17",
                    "2026-02-18", "2026-02-19", "2026-02-20", "2026-02-21"],
            "work": ["2026-02-11", "2026-02-14"],
            "predicted": True,
        },
        {
            "name": "清明节", "emoji": "🌿",
            "off": ["2026-04-04", "2026-04-05", "2026-04-06"],
            "work": [],
            "predicted": True,
        },
        {
            "name": "劳动节", "emoji": "💪",
            "off": ["2026-05-01", "2026-05-02", "2026-05-03", "2026-05-04", "2026-05-05"],
            "work": ["2026-04-26"],
            "predicted": True,
        },
        {
            "name": "端午节", "emoji": "🐉",
            "off": ["2026-06-19", "2026-06-20", "2026-06-21"],
            "work": [],
            "predicted": True,
        },
        {
            "name": "中秋节", "emoji": "🥮",
            "off": ["2026-09-25", "2026-09-26", "2026-09-27"],
            "work": [],
            "predicted": True,
        },
        {
            "name": "国庆节", "emoji": "🇨🇳",
            "off": ["2026-10-01", "2026-10-02", "2026-10-03", "2026-10-04",
                    "2026-10-05", "2026-10-06", "2026-10-07"],
            "work": ["2026-09-27", "2026-10-10"],
            "predicted": True,
        },
    ],
}

WEEKDAYS_CN = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]


def parse_date(s):
    return date.fromisoformat(s)


def get_all_off_dates(year):
    """Get all holiday off dates for a year."""
    off = set()
    for h in HOLIDAYS.get(year, []):
        for d in h["off"]:
            off.add(parse_date(d))
    return off


def get_all_work_dates(year):
    """Get all 调休 workdays for a year."""
    work = set()
    for h in HOLIDAYS.get(year, []):
        for d in h["work"]:
            work.add(parse_date(d))
    return work


def is_workday(d):
    """Check if a date is a workday (considering holidays and 调休)."""
    year = d.year
    off_dates = get_all_off_dates(year)
    work_dates = get_all_work_dates(year)

    if d in work_dates:
        return True  # 调休上班
    if d in off_dates:
        return False  # 放假
    if d.weekday() >= 5:
        return False  # 周末
    return True  # 普通工作日


def get_holiday_name(d):
    """Get holiday name for a date, or None."""
    year = d.year
    for h in HOLIDAYS.get(year, []):
        if d.isoformat() in h["off"]:
            return h["name"], h["emoji"]
    return None, None


def get_work_reason(d):
    """Get 调休 reason for a workday on weekend."""
    year = d.year
    for h in HOLIDAYS.get(year, []):
        if d.isoformat() in h["work"]:
            return h["name"]
    return None


def query_date(d):
    """Query a single date."""
    weekday = WEEKDAYS_CN[d.weekday()]
    workday = is_workday(d)
    name, emoji = get_holiday_name(d)
    reason = get_work_reason(d)

    result = {"date": d.isoformat(), "weekday": weekday, "workday": workday}

    if name:
        result["holiday"] = name
        result["emoji"] = emoji
    if reason:
        result["调休"] = reason

    return result


def next_holiday(from_date=None):
    """Find the next upcoming holiday."""
    d = from_date or date.today()
    for year in [d.year, d.year + 1]:
        for h in HOLIDAYS.get(year, []):
            first_off = parse_date(h["off"][0])
            last_off = parse_date(h["off"][-1])
            if first_off > d:
                days_left = (first_off - d).days
                duration = (last_off - first_off).days + 1
                return {
                    "name": h["name"],
                    "emoji": h["emoji"],
                    "start": first_off.isoformat(),
                    "end": last_off.isoformat(),
                    "days": duration,
                    "days_until": days_left,
                    "work_before": [w for w in h["work"] if parse_date(w) > d],
                    "predicted": h.get("predicted", False),
                }
    return None


def upcoming_alerts(days_ahead=7):
    """Generate alerts for the next N days."""
    today = date.today()
    alerts = []

    for i in range(days_ahead):
        d = today + timedelta(days=i)
        info = query_date(d)

        if info.get("holiday"):
            if i == 0:
                alerts.append(f"{info['emoji']} 今天是{info['holiday']}！放假快乐！")
            elif i == 1:
                alerts.append(f"📅 明天是{info['holiday']}，放假！")
        
        if info.get("调休"):
            if i == 0:
                alerts.append(f"⚠️ 今天（{info['weekday']}）需要上班！{info['调休']}调休")
            elif i == 1:
                alerts.append(f"🔔 调休提醒：明天（{info['weekday']}）需要上班，{info['调休']}调休")
            elif i <= 3:
                alerts.append(f"📋 {i}天后（{info['weekday']} {d.strftime('%m/%d')}）需要调休上班（{info['调休']}）")

    return alerts


def show_calendar(year=None):
    """Show full holiday calendar for a year."""
    year = year or date.today().year
    holidays = HOLIDAYS.get(year, [])

    if not holidays:
        print(f"❌ 暂无 {year} 年节假日数据")
        return

    print(f"📅 {year} 年中国法定节假日")
    predicted = any(h.get("predicted") for h in holidays)
    if predicted:
        print("⚠️  标记 * 的为预测数据，以国务院公布为准")
    print("=" * 55)

    for h in holidays:
        first = parse_date(h["off"][0])
        last = parse_date(h["off"][-1])
        duration = (last - first).days + 1
        star = " *" if h.get("predicted") else ""
        
        print(f"\n  {h['emoji']} {h['name']}{star}")
        print(f"    放假：{first.strftime('%m/%d')} - {last.strftime('%m/%d')}（{duration}天）")
        
        if h["work"]:
            work_str = ", ".join(
                f"{parse_date(w).strftime('%m/%d')}({WEEKDAYS_CN[parse_date(w).weekday()]})"
                for w in h["work"]
            )
            print(f"    调休上班：{work_str}")

    print()


def show_status():
    """Show today's status and upcoming info."""
    today = date.today()
    info = query_date(today)
    weekday = info["weekday"]

    print(f"📅 今天：{today.strftime('%Y-%m-%d')} {weekday}")

    if info.get("holiday"):
        print(f"  {info.get('emoji', '')} {info['holiday']}！放假！")
    elif info.get("调休"):
        print(f"  ⚠️ 调休上班日（{info['调休']}调休）")
    elif info["workday"]:
        print(f"  💼 工作日")
    else:
        print(f"  🏖️ 休息日")

    # Next holiday
    nh = next_holiday(today)
    if nh:
        star = "（预测）" if nh["predicted"] else ""
        print(f"\n  下一个假期：{nh['emoji']} {nh['name']}{star}")
        print(f"  {nh['start']} 起，共 {nh['days']} 天，还有 {nh['days_until']} 天")
        if nh["work_before"]:
            print(f"  ⚠️ 调休上班日：{', '.join(nh['work_before'])}")

    # Alerts
    alerts = upcoming_alerts(7)
    if alerts:
        print(f"\n  📢 近期提醒：")
        for a in alerts:
            print(f"    {a}")

    print()


def main():
    args = sys.argv[1:]

    if not args or "--help" in args or "-h" in args:
        print("CN Holiday — 中国节假日查询")
        print()
        print("Usage:")
        print("  holiday.py --status               今日状态 + 下个假期 + 近期提醒")
        print("  holiday.py --calendar [year]       显示全年节假日日历")
        print("  holiday.py --check YYYY-MM-DD      查询某天是否上班")
        print("  holiday.py --next                  下一个假期")
        print("  holiday.py --alerts [days]          未来 N 天的提醒（默认 7 天）")
        print("  holiday.py --workday YYYY-MM-DD    是否工作日（返回 true/false）")
        print("  holiday.py --json                  以 JSON 输出今日状态")
        sys.exit(0)

    if "--status" in args:
        show_status()
        sys.exit(0)

    if "--calendar" in args:
        idx = args.index("--calendar")
        year = int(args[idx + 1]) if idx + 1 < len(args) and args[idx + 1].isdigit() else None
        show_calendar(year)
        sys.exit(0)

    if "--check" in args:
        idx = args.index("--check")
        if idx + 1 < len(args):
            d = parse_date(args[idx + 1])
            info = query_date(d)
            weekday = info["weekday"]
            if info.get("holiday"):
                print(f"{info.get('emoji', '')} {d} {weekday} — {info['holiday']}，放假")
            elif info.get("调休"):
                print(f"⚠️ {d} {weekday} — 上班（{info['调休']}调休）")
            elif info["workday"]:
                print(f"💼 {d} {weekday} — 工作日")
            else:
                print(f"🏖️ {d} {weekday} — 休息日")
        sys.exit(0)

    if "--next" in args:
        nh = next_holiday()
        if nh:
            star = "（预测）" if nh["predicted"] else ""
            print(f"{nh['emoji']} {nh['name']}{star}")
            print(f"  {nh['start']} ~ {nh['end']}（{nh['days']}天）")
            print(f"  还有 {nh['days_until']} 天")
            if nh["work_before"]:
                print(f"  ⚠️ 调休：{', '.join(nh['work_before'])}")
        else:
            print("暂无假期数据")
        sys.exit(0)

    if "--alerts" in args:
        idx = args.index("--alerts")
        days = int(args[idx + 1]) if idx + 1 < len(args) and args[idx + 1].isdigit() else 7
        alerts = upcoming_alerts(days)
        if alerts:
            for a in alerts:
                print(a)
        else:
            print("近期无特殊提醒 ✅")
        sys.exit(0)

    if "--workday" in args:
        idx = args.index("--workday")
        if idx + 1 < len(args):
            d = parse_date(args[idx + 1])
            print("true" if is_workday(d) else "false")
        sys.exit(0)

    if "--json" in args:
        today = date.today()
        info = query_date(today)
        nh = next_holiday(today)
        alerts = upcoming_alerts(7)
        output = {
            "today": info,
            "next_holiday": nh,
            "alerts": alerts,
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
        sys.exit(0)

    # Default: show status
    show_status()


if __name__ == "__main__":
    main()
