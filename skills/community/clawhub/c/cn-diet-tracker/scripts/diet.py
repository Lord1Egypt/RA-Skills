#!/usr/bin/env python3
"""中文饮食记录 - cn-diet-tracker"""

import json, os, sys, argparse
from datetime import datetime, timedelta
from collections import defaultdict

WORKSPACE = os.path.expanduser("~/.qclaw/workspace")
DATA_FILE = os.path.join(WORKSPACE, "diet.json")

CATEGORIES = {
    "主食": "🍚", "菜品": "🍳", "汤": "🍲", "水果": "🍎",
    "饮品": "🥤", "零食": "🍪", "外卖": "🥡", "其他": "📌"
}

def load():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"records": [], "target": 2000}

def save(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add(food, calories, category="其他", note=""):
    data = load()
    record = {
        "id": len(data["records"]) + 1,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "datetime": datetime.now().isoformat(),
        "food": food,
        "calories": float(calories),
        "category": category,
        "note": note
    }
    data["records"].append(record)
    save(data)
    emoji = CATEGORIES.get(category, "📌")
    today_total = sum(r["calories"] for r in data["records"] if r["date"] == record["date"])
    target = data.get("target", 2000)
    pct = today_total / target * 100
    status = "🔴超了" if pct > 100 else f"🟢{pct:.0f}%"
    print(f"\n✅ {emoji} {food} {calories:.0f}kcal")
    print(f"   今日合计: {today_total:.0f}/{target}kcal {status}")

def today_report():
    data = load()
    today = datetime.now().strftime("%Y-%m-%d")
    today_recs = [r for r in data["records"] if r["date"] == today]
    total = sum(r["calories"] for r in today_recs)
    target = data.get("target", 2000)

    print(f"\n🥗 今日饮食（{today}）")
    print("=" * 40)
    if not today_recs:
        print("  📭 还没记录")
        return
    for r in today_recs:
        emoji = CATEGORIES.get(r["category"], "📌")
        print(f"  {emoji} {r['food']} {r['calories']:.0f}kcal")
    print(f"\n  合计: {total:.0f}/{target}kcal", end="")
    if total > target:
        print(" 🔴超了！")
    elif total > target * 0.8:
        print(" 🟡接近目标")
    else:
        print(" 🟢正常")

def week_report():
    data = load()
    now = datetime.now()
    start = now - timedelta(days=now.weekday())
    week_recs = [r for r in data["records"]
                 if datetime.fromisoformat(r["datetime"]) >= start]
    if not week_recs:
        print("\n📭 本周无记录")
        return
    by_day = defaultdict(float)
    for r in week_recs:
        by_day[r["date"]] += r["calories"]
    target = data.get("target", 2000)
    print(f"\n🥗 本周饮食报告")
    print("=" * 40)
    for date in sorted(by_day.keys()):
        cal = by_day[date]
        bar = "▓" * int(cal / target * 10)
        status = "🔴" if cal > target else "🟢"
        print(f"  {date} {cal:>7.0f}kcal {bar} {status}")
    avg = sum(by_day.values()) / len(by_day)
    print(f"\n  日均: {avg:.0f}kcal / 目标: {target}kcal")

def main():
    parser = argparse.ArgumentParser(description="🥗 中文饮食记录")
    parser.add_argument("--add", nargs="+", help="食物名 热量")
    parser.add_argument("--category", "-c", default="其他", help="分类")
    parser.add_argument("--note", help="备注")
    parser.add_argument("--today", action="store_true", help="今日统计")
    parser.add_argument("--week", action="store_true", help="周报")
    parser.add_argument("--target", type=float, help="设定每日热量目标")
    args = parser.parse_args()

    if args.add:
        food = args.add[0] if len(args.add) > 1 else "食物"
        cal = float(args.add[1] if len(args.add) > 1 else args.add[0])
        if len(args.add) == 1:
            food = "食物"
        add(food, cal, args.category, args.note or "")
    elif args.today:
        today_report()
    elif args.week:
        week_report()
    elif args.target:
        data = load()
        data["target"] = args.target
        save(data)
        print(f"\n✅ 每日热量目标设为 {args.target:.0f}kcal")
    else:
        today_report()

if __name__ == "__main__":
    main()