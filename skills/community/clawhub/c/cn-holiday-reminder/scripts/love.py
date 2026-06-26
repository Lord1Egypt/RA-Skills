#!/usr/bin/env python3
"""Love Assistant — Anniversary & relationship date tracker."""

import sys
import json
from datetime import date, datetime, timedelta
from pathlib import Path

# Fix encoding on Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# ── Data file ───────────────────────────────────────────────────────────────

DEFAULT_DATA_PATH = Path.home() / "agent-memory" / "love.json"

# ── Romantic holidays (annual, MM-DD) ───────────────────────────────────────

LOVE_HOLIDAYS = [
    {"date": "02-14", "name": "情人节", "emoji": "💝", "tip": "准备礼物和浪漫晚餐"},
    {"date": "03-08", "name": "女神节", "emoji": "👸", "tip": "送她一份惊喜"},
    {"date": "03-14", "name": "白色情人节", "emoji": "🤍", "tip": "回赠礼物的日子"},
    {"date": "05-20", "name": "520表白日", "emoji": "💕", "tip": "说出你的爱"},
    {"date": "06-01", "name": "儿童节", "emoji": "🎈", "tip": "陪她做一天小朋友"},
    {"date": "08-25", "name": "七夕节", "emoji": "🎋", "tip": "中国情人节，最浪漫的夜晚"},  # 2025年七夕
    {"date": "11-11", "name": "光棍节/双十一", "emoji": "🛍️", "tip": "一起买买买"},
    {"date": "12-24", "name": "平安夜", "emoji": "🎄", "tip": "送苹果，许平安"},
    {"date": "12-25", "name": "圣诞节", "emoji": "🎅", "tip": "交换圣诞礼物"},
]

# 七夕是农历，每年不同，这里存公历日期
QIXI_DATES = {
    2025: "08-25",
    2026: "08-14",
    2027: "09-02",
}


def load_data(path=None):
    """Load love data from JSON file."""
    p = Path(path) if path else DEFAULT_DATA_PATH
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def save_data(data, path=None):
    """Save love data to JSON file."""
    p = Path(path) if path else DEFAULT_DATA_PATH
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✅ 数据已保存到 {p}")


def create_template():
    """Return empty data template."""
    return {
        "partner_name": "",
        "anniversary": "",
        "partner_birthday": "",
        "my_birthday": "",
        "custom_dates": [],
        "reminders": {
            "anniversary": True,
            "birthday": True,
            "love_holidays": True,
            "monthly": False,
            "days_before": 1,
        },
    }


def parse_date_str(s):
    """Parse date string (YYYY-MM-DD)."""
    return date.fromisoformat(s)


def time_together(anniversary_str):
    """Calculate time together with precision."""
    start = datetime.strptime(anniversary_str, "%Y-%m-%d")
    now = datetime.now()
    delta = now - start

    total_seconds = int(delta.total_seconds())
    days = delta.days
    hours = (total_seconds % 86400) // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    years = days // 365
    remaining_days = days % 365
    months = remaining_days // 30
    remaining_days = remaining_days % 30

    return {
        "total_days": days,
        "total_hours": total_seconds // 3600,
        "total_minutes": total_seconds // 60,
        "total_seconds": total_seconds,
        "years": years,
        "months": months,
        "days": remaining_days,
        "hours": hours,
        "minutes": minutes,
        "seconds": seconds,
        "display": f"{years}年{months}个月{remaining_days}天{hours}小时{minutes}分{seconds}秒",
        "display_short": f"{days}天",
    }


def next_occurrence(mm_dd, from_date=None):
    """Get next occurrence of a MM-DD date."""
    today = from_date or date.today()
    this_year = date(today.year, int(mm_dd[:2]), int(mm_dd[3:]))
    if this_year > today:
        return this_year
    return date(today.year + 1, int(mm_dd[:2]), int(mm_dd[3:]))


def get_love_holidays_for_year(year):
    """Get love holidays with correct Qixi date for the year."""
    holidays = []
    for h in LOVE_HOLIDAYS:
        if h["name"] == "七夕节" and year in QIXI_DATES:
            holidays.append({**h, "date": QIXI_DATES[year]})
        else:
            holidays.append(h)
    return holidays


def upcoming_love_alerts(data, days_ahead=7):
    """Generate love-related alerts for the next N days."""
    today = date.today()
    alerts = []
    days_before = data.get("reminders", {}).get("days_before", 1)

    # Check anniversary
    if data.get("anniversary") and data["reminders"].get("anniversary"):
        ann = data["anniversary"]
        ann_mmdd = ann[5:]  # MM-DD
        next_ann = next_occurrence(ann_mmdd, today)
        days_until = (next_ann - today).days
        partner = data.get("partner_name", "TA")
        together = time_together(ann)

        if days_until == 0:
            alerts.append(f"💑 今天是你和{partner}的恋爱纪念日！在一起 {together['display_short']} 了！")
        elif days_until <= days_before:
            alerts.append(f"💝 还有{days_until}天就是你和{partner}的恋爱纪念日！准备惊喜吧～")

        # Monthly anniversary
        if data["reminders"].get("monthly"):
            ann_day = int(ann[8:])
            if today.day == ann_day:
                alerts.append(f"📅 今天是你和{partner}的月纪念日（每月{ann_day}号）～ 在一起 {together['display_short']}")

    # Check partner birthday
    if data.get("partner_birthday") and data["reminders"].get("birthday"):
        bday = data["partner_birthday"]
        bday_mmdd = bday[5:]
        next_bday = next_occurrence(bday_mmdd, today)
        days_until = (next_bday - today).days
        partner = data.get("partner_name", "TA")

        if days_until == 0:
            alerts.append(f"🎂 今天是{partner}的生日！别忘了说生日快乐！")
        elif days_until <= days_before:
            alerts.append(f"🎁 还有{days_until}天就是{partner}的生日！准备礼物了吗？")

    # Check custom dates
    for cd in data.get("custom_dates", []):
        cd_mmdd = cd["date"][5:] if len(cd["date"]) > 5 else cd["date"]
        next_cd = next_occurrence(cd_mmdd, today)
        days_until = (next_cd - today).days

        if days_until == 0:
            alerts.append(f"{cd.get('emoji', '💫')} 今天是{cd['name']}！")
        elif days_until <= days_before:
            alerts.append(f"{cd.get('emoji', '💫')} 还有{days_until}天就是{cd['name']}！")

    # Check love holidays
    if data["reminders"].get("love_holidays"):
        love_holidays = get_love_holidays_for_year(today.year)
        for lh in love_holidays:
            next_lh = next_occurrence(lh["date"], today)
            days_until = (next_lh - today).days

            if days_until == 0:
                alerts.append(f"{lh['emoji']} 今天是{lh['name']}！{lh['tip']}")
            elif days_until <= days_before:
                alerts.append(f"{lh['emoji']} 还有{days_until}天就是{lh['name']}！{lh['tip']}")

    return alerts


def show_status(data):
    """Show love assistant status."""
    partner = data.get("partner_name", "TA")

    print(f"💑 恋爱助手")
    print("=" * 50)

    if data.get("anniversary"):
        together = time_together(data["anniversary"])
        print(f"\n  你和{partner}在一起:")
        print(f"  ❤️  {together['display']}")
        print(f"  📊 共 {together['total_days']} 天 / {together['total_hours']} 小时 / {together['total_seconds']} 秒")

        # Next anniversary
        ann_mmdd = data["anniversary"][5:]
        next_ann = next_occurrence(ann_mmdd)
        days_until = (next_ann - date.today()).days
        print(f"\n  📅 下一个纪念日：{next_ann} （还有 {days_until} 天）")

    if data.get("partner_birthday"):
        bday_mmdd = data["partner_birthday"][5:]
        next_bday = next_occurrence(bday_mmdd)
        days_until = (next_bday - date.today()).days
        print(f"  🎂 {partner}生日：{next_bday} （还有 {days_until} 天）")

    # Custom dates
    if data.get("custom_dates"):
        print(f"\n  📋 自定义纪念日：")
        for cd in data["custom_dates"]:
            cd_mmdd = cd["date"][5:] if len(cd["date"]) > 5 else cd["date"]
            next_cd = next_occurrence(cd_mmdd)
            days_until = (next_cd - date.today()).days
            print(f"    {cd.get('emoji', '💫')} {cd['name']}：{next_cd}（还有 {days_until} 天）")

    # Next love holiday
    love_holidays = get_love_holidays_for_year(date.today().year)
    upcoming = []
    for lh in love_holidays:
        next_lh = next_occurrence(lh["date"])
        days_until = (next_lh - date.today()).days
        upcoming.append((days_until, lh, next_lh))
    upcoming.sort()

    if upcoming:
        days_until, lh, next_lh = upcoming[0]
        print(f"\n  {lh['emoji']} 下一个浪漫节日：{lh['name']}（{next_lh}，还有 {days_until} 天）")

    # Alerts
    alerts = upcoming_love_alerts(data, 7)
    if alerts:
        print(f"\n  📢 近期提醒：")
        for a in alerts:
            print(f"    {a}")

    print()


def interactive_setup(data_path=None):
    """Interactive setup wizard."""
    print("💑 恋爱助手设置向导")
    print("=" * 50)
    print()

    data = create_template()

    data["partner_name"] = input("  另一半的名字/昵称：").strip()
    if not data["partner_name"]:
        data["partner_name"] = "TA"

    ann = input("  在一起的日期（YYYY-MM-DD）：").strip()
    if ann:
        data["anniversary"] = ann

    bday = input(f"  {data['partner_name']}的生日（YYYY-MM-DD）：").strip()
    if bday:
        data["partner_birthday"] = bday

    my_bday = input("  你的生日（YYYY-MM-DD，可跳过）：").strip()
    if my_bday:
        data["my_birthday"] = my_bday

    # Custom dates
    print(f"\n  添加自定义纪念日（直接回车跳过）：")
    while True:
        name = input("    纪念日名称（回车结束）：").strip()
        if not name:
            break
        cd_date = input("    日期（YYYY-MM-DD）：").strip()
        emoji = input("    emoji（可选，回车默认💫）：").strip() or "💫"
        if cd_date:
            data["custom_dates"].append({"name": name, "date": cd_date, "emoji": emoji})

    # Reminder settings
    print(f"\n  提醒设置：")
    monthly = input("  每月纪念日提醒？(y/N)：").strip().lower()
    data["reminders"]["monthly"] = monthly in ("y", "yes", "是")

    days_b = input("  提前几天提醒？(默认1)：").strip()
    if days_b.isdigit():
        data["reminders"]["days_before"] = int(days_b)

    save_data(data, data_path)

    if data.get("anniversary"):
        together = time_together(data["anniversary"])
        print(f"\n  ❤️ 你和{data['partner_name']}已经在一起 {together['display']} 了！")

    print(f"\n✅ 设置完成！")
    print(f"💡 提示：告诉 Agent '在一起多久了' 可以随时查看")


def main():
    args = sys.argv[1:]
    data_path = None

    # Extract --data-path
    for i, arg in enumerate(args):
        if arg == "--data-path" and i + 1 < len(args):
            data_path = args[i + 1]
            args = args[:i] + args[i+2:]
            break

    if not args or "--help" in args or "-h" in args:
        print("Love Assistant — 恋爱助手")
        print()
        print("Usage:")
        print("  love.py --setup                    交互式设置向导")
        print("  love.py --status                   查看状态（在一起多久、下个纪念日）")
        print("  love.py --together                 在一起多久了（精确到秒）")
        print("  love.py --alerts [days]             未来 N 天的恋爱提醒")
        print("  love.py --holidays                 浪漫节日日历")
        print("  love.py --json                     JSON 输出（供 Agent 用）")
        print("  love.py --data-path <path>         指定数据文件路径")
        print()
        print(f"Data file: {data_path or DEFAULT_DATA_PATH}")
        sys.exit(0)

    if "--setup" in args:
        interactive_setup(data_path)
        sys.exit(0)

    if "--holidays" in args:
        year = date.today().year
        holidays = get_love_holidays_for_year(year)
        print(f"💝 {year} 年浪漫节日日历")
        print("=" * 50)
        for lh in holidays:
            next_lh = next_occurrence(lh["date"])
            days_until = (next_lh - date.today()).days
            status = "✅ 已过" if days_until > 300 else f"还有 {days_until} 天"
            print(f"  {lh['emoji']} {lh['date']} {lh['name']:10s} — {status}")
            print(f"              💡 {lh['tip']}")
        sys.exit(0)

    # Load data for other commands
    data = load_data(data_path)
    if not data:
        print("❌ 尚未设置恋爱助手")
        print(f"   运行: love.py --setup")
        print(f"   或告诉 Agent: \"设置恋爱助手\"")
        sys.exit(1)

    if "--status" in args:
        show_status(data)
        sys.exit(0)

    if "--together" in args:
        if data.get("anniversary"):
            together = time_together(data["anniversary"])
            partner = data.get("partner_name", "TA")
            print(f"❤️ 你和{partner}在一起了：")
            print(f"  {together['display']}")
            print(f"  = {together['total_days']} 天")
            print(f"  = {together['total_hours']} 小时")
            print(f"  = {together['total_minutes']} 分钟")
            print(f"  = {together['total_seconds']} 秒")
        else:
            print("❌ 未设置在一起的日期")
        sys.exit(0)

    if "--alerts" in args:
        idx = args.index("--alerts")
        days = int(args[idx + 1]) if idx + 1 < len(args) and args[idx + 1].isdigit() else 7
        alerts = upcoming_love_alerts(data, days)
        if alerts:
            for a in alerts:
                print(a)
        else:
            print("近期无恋爱相关提醒 ✅")
        sys.exit(0)

    if "--json" in args:
        output = {"data": data}
        if data.get("anniversary"):
            output["together"] = time_together(data["anniversary"])
        output["alerts"] = upcoming_love_alerts(data, 7)
        # Next love holiday
        love_holidays = get_love_holidays_for_year(date.today().year)
        upcoming = []
        for lh in love_holidays:
            next_lh = next_occurrence(lh["date"])
            days_until = (next_lh - date.today()).days
            upcoming.append({"name": lh["name"], "emoji": lh["emoji"], "date": next_lh.isoformat(), "days_until": days_until, "tip": lh["tip"]})
        upcoming.sort(key=lambda x: x["days_until"])
        output["love_holidays"] = upcoming[:5]
        print(json.dumps(output, indent=2, ensure_ascii=False))
        sys.exit(0)

    # Default
    show_status(data)


if __name__ == "__main__":
    main()
