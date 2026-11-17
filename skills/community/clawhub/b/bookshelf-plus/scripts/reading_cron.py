#!/usr/bin/env python3
"""
reading_cron.py — 閱讀習慣養成 Cron Script
由 OpenClaw Cron Job 每日呼叫，檢查今日打卡狀態並發送提醒
"""

import sys
import json
import datetime
import argparse
from pathlib import Path

LOG_PATH = "~/.bookshelf-plus/reading_log.json"


def get_today_record(log_path: Path) -> dict | None:
    """取得今日打卡記錄"""
    if not log_path.exists():
        return None
    with open(log_path) as f:
        data = json.load(f)
    today = datetime.date.today().isoformat()
    for s in data.get("sessions", []):
        if s.get("date") == today:
            return s
    return None


def update_streak(log_path: Path) -> dict:
    """更新連續打卡天數"""
    if not log_path.exists():
        return {"current": 0, "longest": 0, "last_date": ""}
    with open(log_path) as f:
        data = json.load(f)

    streak = data.get("streak", {"current": 0, "longest": 0, "last_date": ""})
    today = datetime.date.today()
    yesterday = (today - datetime.timedelta(days=1)).isoformat()

    # 檢查今日是否已打卡
    today_record = get_today_record(log_path)

    if today_record:
        # 今日已打卡
        if streak.get("last_date") == yesterday:
            # 昨天也有 → streak +1
            streak["current"] += 1
        elif streak.get("last_date") != today.isoformat():
            # 昨天沒打 → 重置為 1
            streak["current"] = 1
        streak["last_date"] = today.isoformat()
        streak["longest"] = max(streak["longest"], streak["current"])
    else:
        # 今日未打卡 → 檢查是否斷了 streak
        if streak.get("last_date") and streak.get("last_date") != today.isoformat():
            days_since = (today - datetime.date.fromisoformat(streak["last_date"])).days
            if days_since > 1:
                streak["current"] = 0  # 斷了

    data["streak"] = streak
    with open(log_path, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return streak


def get_reminder_message(streak: dict, today_record: dict | None) -> str:
    """產生提醒訊息"""
    today = datetime.date.today()
    weekday_names = ["一", "二", "三", "四", "五", "六", "日"]
    weekday = weekday_names[today.weekday()]

    if today_record:
        pages = today_record.get("pages_read", 0)
        note = today_record.get("note", "")
        msg = f"""📖 今日閱讀已完成！

今天（週{weekday}）你讀了 **{pages} 頁**
{f"備註：{note}" if note else ""}

🔥 連續打卡：{streak.get('current', 0)} 天
🏆 歷史最高：{streak.get('longest', 0)} 天

今天辛苦了，繼續保持 📚"""
        return msg

    # 未打卡
    messages = [
        f"📚 今日閱讀提醒（週{weekday}）\n\n今天還沒打卡呢！\n\n",
        f"📖 今日閱讀提醒\n\n今天是週{weekday}，你還沒有記錄今天的閱讀。\n\n",
        f"📚 閱讀打卡（週{weekday}）\n\n一天不讀書，面目可憎。\n快去翻開書本吧！\n\n",
    ]
    import random
    base = random.choice(messages)

    if streak.get("current", 0) > 0:
        return base + f"🔥 目前連續打卡 **{streak['current']} 天**，今天繼續保持！"
    else:
        return base + "💡 今天開始你的閱讀之旅吧！"


def get_weekly_summary(log_path: Path) -> str:
    """產生本週閱讀摘要（週日時觸發）"""
    if not log_path.exists():
        return ""
    with open(log_path) as f:
        data = json.load(f)

    today = datetime.date.today()
    week_start = today - datetime.timedelta(days=today.weekday())
    week_sessions = [
        s for s in data.get("sessions", [])
        if s.get("date", "") >= week_start.isoformat()
    ]

    if not week_sessions:
        return ""

    total_pages = sum(s.get("pages_read", 0) for s in week_sessions)
    total_minutes = sum(s.get("duration_minutes", 0) for s in week_sessions)
    book_count = len(set(s.get("book_title", "") for s in week_sessions))

    return f"""📊 本週閱讀週報

• 打卡天數：{len(week_sessions)} 天
• 閱讀頁數：{total_pages} 頁
• 閱讀時長：{total_minutes // 60}h {total_minutes % 60}min
• 閱讀書籍：{book_count} 本

→ 表現得棒！"""

def main():
    parser = argparse.ArgumentParser(description="閱讀習慣 Cron Script")
    parser.add_argument("--log", default=LOG_PATH, help="reading_log.json 路徑")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    log_path = Path(args.log).expanduser()

    # 更新 streak
    streak = update_streak(log_path)

    # 檢查今日記錄
    today_record = get_today_record(log_path)
    reminder = get_reminder_message(streak, today_record)

    # 週報（週日時額外附加）
    today = datetime.date.today()
    weekly = get_weekly_summary(log_path) if today.weekday() == 6 else ""

    result = {
        "date": today.isoformat(),
        "checked_in": today_record is not None,
        "streak": streak,
        "reminder": reminder,
        "weekly_summary": weekly,
    }

    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(reminder)
        if weekly:
            print()
            print(weekly)

    sys.exit(0)


if __name__ == "__main__":
    main()
