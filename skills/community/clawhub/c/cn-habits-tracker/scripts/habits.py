#!/usr/bin/env python3
"""
中文习惯打卡追踪器 - cn-habits-tracker
每日打卡 + 连续天数 + 统计报告

用法:
  python3 habits.py --checkin "早起"
  python3 habits.py --add "早起" --goal "每天7点前" --unit "天"
  python3 habits.py --today
  python3 habits.py --report week
"""

import json
import os
import sys
import argparse
from datetime import datetime, timedelta
from collections import defaultdict

WORKSPACE = os.path.expanduser("~/.qclaw/workspace")
DATA_FILE = os.path.join(WORKSPACE, "habits.json")


def load():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"habits": {}, "records": []}


def save(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def today_str():
    return datetime.now().strftime("%Y-%m-%d")


def streak_for(records, habit_id):
    """计算连续打卡天数"""
    today = today_str()
    dates = set(r["date"] for r in records if r.get("habit_id") == habit_id or r.get("habit") == habit_id)
    if not dates:
        return 0

    # 从今天/昨天开始算
    streak = 0
    d = datetime.now()
    for _ in range(365):
        ds = d.strftime("%Y-%m-%d")
        if ds in dates:
            streak += 1
            d -= timedelta(days=1)
        else:
            # 昨天没打卡就断了
            if d.strftime("%Y-%m-%d") == today:
                d -= timedelta(days=1)
                if d.strftime("%Y-%m-%d") in dates:
                    streak += 1
                    d -= timedelta(days=1)
                else:
                    break
            else:
                break
    return streak


def add_habit(name, goal="", unit="天"):
    data = load()
    if name in data["habits"]:
        print("\n⚠️ 习惯「{}」已存在".format(name))
        return

    habit_id = len(data["habits"]) + 1
    data["habits"][str(habit_id)] = {
        "name": name,
        "goal": goal,
        "unit": unit,
        "created": today_str(),
        "id": habit_id
    }
    save(data)
    print("\n✅ 习惯「{}」已添加（目标：{}）".format(name, goal or "每日打卡"))


def checkin(name, amount="", note=""):
    data = load()
    today = today_str()

    # 找习惯
    habit_id = None
    for hid, h in data["habits"].items():
        if h["name"] == name:
            habit_id = hid
            break

    if not habit_id:
        print("\n⚠️ 未找到习惯「{}」，先添加：--add \"{}\"".format(name, name))
        return

    # 检查今天是否已打卡
    today_record = [r for r in data["records"] if r.get("habit_id") == habit_id and r["date"] == today]
    if today_record:
        today_record[0]["amount"] = amount
        today_record[0]["note"] = note
        print("\n🔄 已更新今日打卡记录")
        save(data)
    else:
        data["records"].append({
            "habit_id": habit_id,
            "date": today,
            "datetime": datetime.now().isoformat(),
            "amount": amount,
            "note": note
        })
        streak = streak_for(data["records"], habit_id)
        emoji = "🔥" if streak >= 3 else "✅"
        print("\n{} 打卡成功！「{}」连续{}天 {}！".format(
            emoji, name, streak, data["habits"][habit_id]["unit"]))
        save(data)


def show_today():
    data = load()
    today = today_str()
    habits = data["habits"]
    records = data["records"]

    today_records = {r.get("habit_id"): r for r in records if r["date"] == today}

    print("\n🎯 今日打卡（{}）".format(today))
    print("=" * 44)

    if not habits:
        print("  📭 还没有习惯，添加一个：--add \"习惯名\"")
        return

    incomplete = []
    for hid, h in habits.items():
        record = today_records.get(hid)
        if record:
            amount_str = "（{}）".format(record.get("amount", "")) if record.get("amount") else ""
            streak = streak_for(records, hid)
            fire = "🔥" * min(streak // 7 + 1, 3)
            print("  ☑ {} {} 已打卡 {} 连续{}天 {}".format(
                fire, h["name"], amount_str, streak, fire))
        else:
            incomplete.append(h)
            print("  ☐ {} 未打卡".format(h["name"]))

    if incomplete:
        print("\n⚠️ 今天还需要完成：")
        for h in incomplete:
            print("  • {}：{}".format(h["name"], h["goal"]))


def list_habits():
    data = load()
    habits = data["habits"]
    records = data["records"]

    if not habits:
        print("\n📭 还没有习惯")
        return

    print("\n📋 习惯列表（共{}个）".format(len(habits)))
    print("-" * 44)
    for hid, h in habits.items():
        streak = streak_for(records, hid)
        fire = "🔥" * min(streak // 7 + 1, 3)
        print("  {} {} 连续{}天 {}".format(
            "☑" if streak > 0 else "☐", h["name"], streak, fire))
        if h["goal"]:
            print("     目标：{}".format(h["goal"]))


def report(period="week"):
    data = load()
    habits = data["habits"]
    records = data["records"]

    now = datetime.now()
    if period == "week":
        start = now - timedelta(days=now.weekday())
    else:
        start = datetime(now.year, now.month, 1)

    period_records = [
        r for r in records
        if start <= datetime.fromisoformat(r["datetime"]) <= now
    ]

    if not habits:
        print("\n📭 还没有习惯")
        return

    days = (now - start).days + 1
    print("\n📊 {}报告（{}月{}日-{}月{}日，共{}天）".format(
        "周" if period == "week" else "月",
        start.month, start.day, now.month, now.day, days))
    print("=" * 44)

    for hid, h in habits.items():
        habit_records = [r for r in period_records if r.get("habit_id") == hid]
        done_days = len(set(r["date"] for r in habit_records))
        rate = done_days / days * 100

        bar_len = int(rate / 10)
        bar = "▓" * bar_len + "░" * (10 - bar_len)
        status = "✅" if rate >= 80 else ("🟡" if rate >= 50 else "❌")
        streak = streak_for(records, hid)

        print("  {} {}  {:>6.1f}% {} {}/{}天 连续{}天".format(
            status, h["name"][:6].ljust(6), rate, bar, done_days, days, streak))


def remind():
    data = load()
    today = today_str()
    habits = data["habits"]
    records = data["records"]
    today_records = set(r.get("habit_id") for r in records if r["date"] == today)

    incomplete = [h for hid, h in habits.items() if hid not in today_records]
    if incomplete:
        print("\n📌 今日待完成习惯：")
        for h in incomplete:
            print("  ☐ {}：{}".format(h["name"], h.get("goal", "打卡")))
    else:
        print("\n🎉 今日习惯全部完成！")


def delete_habit(name):
    data = load()
    habit_id = None
    for hid, h in data["habits"].items():
        if h["name"] == name:
            habit_id = hid
            break

    if not habit_id:
        print("\n⚠️ 未找到习惯「{}」".format(name))
        return

    del data["habits"][habit_id]
    data["records"] = [r for r in data["records"] if r.get("habit_id") != habit_id]
    save(data)
    print("\n✅ 习惯「{}」已删除".format(name))


def main():
    parser = argparse.ArgumentParser(description="🎯 中文习惯打卡")
    parser.add_argument("--add",
                        help="添加习惯")
    parser.add_argument("--goal",
                        help="习惯目标")
    parser.add_argument("--unit", default="天",
                        help="打卡单位（默认：天）")
    parser.add_argument("--checkin",
                        help="打卡")
    parser.add_argument("--amount",
                        help="打卡数量/程度")
    parser.add_argument("--note",
                        help="备注")
    parser.add_argument("--today", action="store_true",
                        help="今日状态")
    parser.add_argument("--list", action="store_true",
                        help="习惯列表")
    parser.add_argument("--report",
                        choices=["week", "month"],
                        help="报告（week/month）")
    parser.add_argument("--delete",
                        help="删除习惯")
    parser.add_argument("--remind", action="store_true",
                        help="未打卡提醒")
    args = parser.parse_args()

    if args.add:
        add_habit(args.add, args.goal or "", args.unit)
    elif args.checkin:
        checkin(args.checkin, args.amount or "", args.note or "")
    elif args.today:
        show_today()
    elif args.list:
        list_habits()
    elif args.report:
        report(args.report)
    elif args.remind:
        remind()
    elif args.delete:
        delete_habit(args.delete)
    else:
        show_today()


if __name__ == "__main__":
    main()
