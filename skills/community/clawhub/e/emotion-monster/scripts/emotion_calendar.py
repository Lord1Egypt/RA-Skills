#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
情緒小怪獸 - 情緒日曆
Emotion Monster: Monthly Emotion Calendar (Text Mode)
"""

import os
import sys
import json
import datetime
import calendar

# ── ANSI colour constants ──────────────────────────────────────────────
C_RESET   = "\033[0m"
C_BOLD    = "\033[1m"
C_YELLOW  = "\033[93m"
C_BLUE    = "\033[94m"
C_RED     = "\033[91m"
C_PURPLE  = "\033[95m"
C_GREEN   = "\033[92m"
C_GRAY    = "\033[90m"
C_WHITE   = "\033[97m"
C_ORANGE  = "\033[33m"
C_PINK    = "\033[35m"

DIARY_DIR  = os.path.expanduser("~/.bookshelf-plus/kids")
DIARY_FILE = os.path.join(DIARY_DIR, "mood_diary.json")

EMOTIONS = {
    "😊": {"name": "開心",  "color": C_YELLOW},
    "😢": {"name": "難過",  "color": C_BLUE},
    "😠": {"name": "生氣",  "color": C_RED},
    "😨": {"name": "害怕",  "color": C_PURPLE},
    "😮": {"name": "驚訝",  "color": C_ORANGE},
    "😴": {"name": "累了",  "color": C_GRAY},
    "🤗": {"name": "舒服",  "color": C_PINK},
    "🤔": {"name": "好奇",  "color": C_GREEN},
}

WEEKDAY_HEADER = ["一", "二", "三", "四", "五", "六", "日"]
WEEKDAY_FULL   = ["週一", "週二", "週三", "週四", "週五", "週六", "週日"]


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def load_entries() -> list:
    if not os.path.exists(DIARY_FILE):
        return []
    try:
        with open(DIARY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, IOError):
        return []


def ask(prompt: str) -> str:
    try:
        return input(C_BOLD + C_WHITE + prompt + " " + C_RESET).strip()
    except (EOFError, KeyboardInterrupt):
        return ""


def day_emojis(entries: list, date_str: str, max_emoji: int = 3) -> str:
    """Return up to max_emoji Emojis summarizing that day's moods."""
    day_entries = [e for e in entries if e.get("date") == date_str]
    if not day_entries:
        return ""
    top = sorted(day_entries, key=lambda x: -x.get("intensity", 0))[:max_emoji]
    return "".join(e.get("emotion", "?") for e in top)


def month_view(year: int, month: int, entries: list):
    """Render a coloured monthly calendar in text mode."""
    cal = calendar.Calendar(firstweekday=0)  # Monday first

    month_name = datetime.date(year, month, 1).strftime("%Y 年 %m 月")
    print()
    print(C_BOLD + C_BLUE + f"   📅 {month_name}" + C_RESET)
    print()

    # ── Weekday header ───────────────────────────────────────────────
    header = "  "
    for i, wd in enumerate(WEEKDAY_HEADER):
        if i >= 5:
            header += C_BOLD + C_ORANGE + f" {wd:^3} " + C_RESET + " "
        else:
            header += C_BOLD + C_WHITE + f" {wd:^3} " + C_RESET + " "
    print(header)
    print(C_GRAY + "  " + "─" * 46 + C_RESET)

    today = datetime.date.today()
    rows = cal.monthdayscalendar(year, month)

    for week in rows:
        line = "  "
        for i, day in enumerate(week):
            if day == 0:
                line += C_GRAY + "    " + C_RESET + " "
                continue

            date_str = f"{year:04d}-{month:02d}-{day:02d}"
            emojis   = day_emojis(entries, date_str)

            # Highlight today
            is_today = (datetime.date(year, month, day) == today)
            day_str  = f"{day:2d}"

            # Weekend
            if i >= 5:
                if is_today:
                    line += C_BOLD + C_ORANGE + f"[{day_str}]" + C_RESET + C_ORANGE + emojis + C_RESET + " "
                else:
                    line += C_ORANGE + f" {day_str} " + C_RESET + C_ORANGE + emojis + C_RESET + " "
            else:
                if is_today:
                    line += C_BOLD + C_GREEN + f"[{day_str}]" + C_RESET + C_YELLOW + emojis + C_RESET + " "
                else:
                    line += C_WHITE + f" {day_str} " + C_RESET + C_YELLOW + emojis + C_RESET + " "

        print(line)

    print()


def weekly_summary(entries: list, year: int, month: int):
    """Show weekend summary: what emotions appeared most."""
    today = datetime.date.today()

    # Get all entries for this month up to today
    month_str  = f"{year:04d}-{month:02d}"
    month_data = [e for e in entries if e.get("date", "").startswith(month_str)]

    if not month_data:
        print()
        print(C_GRAY + "  本月還沒有情緒記錄 📝" + C_RESET)
        print()
        return

    # Count per emotion
    counts = {}
    for e in month_data:
        em = e.get("emotion", "?")
        counts[em] = counts.get(em, 0) + 1

    total   = sum(counts.values())
    top_em  = max(counts, key=counts.get)
    top_cnt = counts[top_em]
    top_name  = EMOTIONS.get(top_em, {}).get("name", top_em)
    top_color = EMOTIONS.get(top_em, {}).get("color", C_GRAY)

    print()
    print(C_BOLD + C_PURPLE + "  🌟 月度情緒統計（本月迄今）" + C_RESET)
    print(C_GRAY + "  " + "─" * 36 + C_RESET)
    print(f"  記錄總筆數：{C_YELLOW}{total} 筆{C_RESET}")
    print(f"  最常出現：  {top_em} {top_color}{top_name}（{top_cnt} 筆）{C_RESET}")
    print()

    # Show all emotions with bar
    print(C_BOLD + C_WHITE + "  📊 情緒分佈：" + C_RESET)
    sorted_em = sorted(counts.items(), key=lambda x: -x[1])
    max_count  = max(c for _, c in sorted_em) if sorted_em else 1

    for em, cnt in sorted_em:
        name   = EMOTIONS.get(em, {}).get("name", em)
        color  = EMOTIONS.get(em, {}).get("color", C_GRAY)
        bar_len = int(round(cnt / max_count * 20))
        bar    = color + "█" * bar_len + C_GRAY + "░" * (20 - bar_len) + C_RESET
        pct    = int(round(cnt / total * 100))
        print(f"  {em} {color}{name:<4}{C_RESET} {bar} {pct:3d}%  ({cnt}筆)")

    print()
    # Unique emotions discovered this month
    unique_em = list(counts.keys())
    if len(unique_em) == len(EMOTIONS):
        msg = f"  🌟🌟🌟 太棒了！你認識了全部 8 種情緒小怪獸！🦋"
    elif len(unique_em) >= 5:
        msg = f"  🌟🌟 很棒！你認識了 {len(unique_em)} 種情緒小怪獸！"
    elif len(unique_em) >= 3:
        msg = f"  🌟 繼續加油！你認識了 {len(unique_em)} 種情緒小怪獸 🌱"
    else:
        msg = f"  🌱 慢慢來，你認識了 {len(unique_em)} 種情緒小怪獸 🌱"
    print(C_GREEN + C_BOLD + msg + C_RESET)
    print()


def day_detail(entries: list, date_str: str):
    """Show all entries for a specific day."""
    day_entries = [e for e in entries if e.get("date") == date_str]
    if not day_entries:
        print(C_GRAY + f"  這天還沒有記錄 📝" + C_RESET)
        return

    for e in day_entries:
        em    = e.get("emotion", "?")
        name  = EMOTIONS.get(em, {}).get("name", em)
        color = EMOTIONS.get(em, {}).get("color", C_GRAY)
        time_ = e.get("time", "")
        stars = "⭐" * e.get("intensity", 3) + "☆" * (5 - e.get("intensity", 3))
        note  = e.get("note", "")
        trig  = e.get("trigger", "")

        print(f"  {em} {color}{name}{C_RESET}  ⏰ {time_}  {stars}")
        if trig and trig != "（未記錄）":
            print(f"       📌 {trig}")
        if note:
            print(f"       💬 {note}")
        print()


def select_date() -> tuple:
    today = datetime.date.today()
    year  = today.year
    month = today.month

    clear_screen()
    print()
    print(C_BOLD + C_BLUE + "  📅 情緒日曆：選擇月份" + C_RESET)
    print()
    print(f"  1. {year} 年 {month} 月（本月）")
    if month == 1:
        print(f"  2. {year-1} 年 12 月")
    else:
        print(f"  2. {year} 年 {month-1} 月")
    if month == 12:
        print(f"  3. {year+1} 年 1 月")
    else:
        print(f"  3. {year} 年 {month+1} 月")
    print(f"  4. 自訂月份")
    print()

    choice = ask("  選擇（1-4 或 Q 離開）：")
    if choice == "1":
        return year, month
    elif choice == "2":
        if month == 1:
            return year - 1, 12
        return year, month - 1
    elif choice == "3":
        if month == 12:
            return year + 1, 1
        return year, month + 1
    elif choice == "4":
        clear_screen()
        print()
        print(C_BOLD + C_WHITE + "  請輸入年月（例：2025 6）：" + C_RESET)
        parts = ask("  年 月：").split()
        if len(parts) == 2:
            try:
                y, m = int(parts[0]), int(parts[1])
                if 2000 <= y <= 2100 and 1 <= m <= 12:
                    return y, m
            except ValueError:
                pass
        print(C_GRAY + "  輸入格式不正確，使用本月。" + C_RESET)
    return today.year, today.month


def main():
    entries = load_entries()
    today   = datetime.date.today()
    year, month = today.year, today.month

    while True:
        clear_screen()
        print()
        print(C_BOLD + C_YELLOW + " ╭─────────────────────────────────────────╮" + C_RESET)
        print(C_BOLD + C_YELLOW + " │  📅 情緒小怪獸：情緒日曆                 │" + C_RESET)
        print(C_BOLD + C_YELLOW + " ╰─────────────────────────────────────────╯" + C_RESET)
        print()
        print(f"  {C_GREEN}1.{C_RESET}  📆  查看月曆（瀏覽 + 統計）")
        print(f"  {C_GREEN}2.{C_RESET}  📋  查看某一天的所有記錄")
        print(f"  {C_GREEN}3.{C_RESET}  🔄  切換月份")
        print()
        print(f"  {C_GRAY}Q.{C_RESET}  離開")
        print()

        choice = ask("  選擇（1-3 或 Q）：")

        if choice in ("q", "Q"):
            clear_screen()
            print()
            print(C_BOLD + C_GREEN + "  🌟 下次再見！情緒小怪獸永遠陪著你！🦋" + C_RESET)
            print()
            break

        elif choice == "1":
            year, month = select_date()
            clear_screen()
            month_view(year, month, entries)
            weekly_summary(entries, year, month)
            print(C_GRAY + "  按 Enter 回到主選單..." + C_RESET)
            try:
                input()
            except (EOFError, KeyboardInterrupt):
                pass

        elif choice == "2":
            clear_screen()
            print()
            print(C_BOLD + C_WHITE + "  📋 查看特定日期的記錄" + C_RESET)
            print()
            print(f"  📌 輸入格式：YYYY-MM-DD（例：{today.isoformat()}）" + C_RESET)
            date_str = ask("  日期（Enter = 今天）：")
            if not date_str:
                date_str = today.isoformat()
            # Validate format
            try:
                datetime.datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                print(C_GRAY + "  格式不對，請用 YYYY-MM-DD，例如 2025-06-15" + C_RESET)
                ask("  按 Enter 繼續：")
                continue

            clear_screen()
            print()
            print(C_BOLD + C_BLUE + f"  📋 {date_str} 的情緒記錄" + C_RESET)
            print()
            day_detail(entries, date_str)
            print()
            print(C_GRAY + "  按 Enter 回到主選單..." + C_RESET)
            try:
                input()
            except (EOFError, KeyboardInterrupt):
                pass

        elif choice == "3":
            year, month = select_date()


if __name__ == "__main__":
    main()
