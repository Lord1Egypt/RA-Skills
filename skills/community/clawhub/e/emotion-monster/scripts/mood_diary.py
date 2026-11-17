#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
情緒小怪獸 - 情緒日記
Emotion Monster: Mood Diary for Kids (Ages 2-6)
"""

import os
import sys
import json
import datetime

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


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


# ── Emotion mapping ────────────────────────────────────────────────────
EMOTIONS = {
    "😊": {"name": "開心",   "color": C_YELLOW, "monster": "開心小怪獸"},
    "😢": {"name": "難過",   "color": C_BLUE,   "monster": "難過小怪獸"},
    "😠": {"name": "生氣",   "color": C_RED,    "monster": "生氣小怪獸"},
    "😨": {"name": "害怕",   "color": C_PURPLE,  "monster": "害怕小怪獸"},
    "😮": {"name": "驚訝",   "color": C_ORANGE,  "monster": "驚訝小怪獸"},
    "😴": {"name": "累了",   "color": C_GRAY,    "monster": "愛睏小怪獸"},
    "🤗": {"name": "舒服",   "color": C_PINK,    "monster": "滿足小怪獸"},
    "🤔": {"name": "好奇",   "color": C_GREEN,   "monster": "好奇小怪獸"},
}


def ensure_dir():
    os.makedirs(DIARY_DIR, exist_ok=True)


def load_entries() -> list:
    ensure_dir()
    if not os.path.exists(DIARY_FILE):
        return []
    try:
        with open(DIARY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, IOError):
        return []


def save_entries(entries: list):
    ensure_dir()
    with open(DIARY_FILE, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)


def ask(prompt: str, allowed: list = None) -> str:
    """Ask user input, optionally validating against allowed list."""
    while True:
        try:
            answer = input(C_BOLD + C_WHITE + prompt + " " + C_RESET).strip()
        except (EOFError, KeyboardInterrupt):
            return ""
        if allowed is None or answer in allowed:
            return answer
        print(C_GRAY + f"  請輸入：{' / '.join(allowed)}" + C_RESET)


def ask_int(prompt: str, low: int = 1, high: int = 5) -> int:
    while True:
        try:
            val = input(C_BOLD + C_WHITE + prompt + " " + C_RESET).strip()
            i = int(val)
            if low <= i <= high:
                return i
            print(C_GRAY + f"  請輸入數字 {low} 到 {high}" + C_RESET)
        except (ValueError, EOFError, KeyboardInterrupt):
            return 3


def record_entry() -> dict:
    clear_screen()
    print()
    print(C_BOLD + C_BLUE + " ╭───────────────────────────────────────╮" + C_RESET)
    print(C_BOLD + C_BLUE + " │  📔 情緒小怪獸：情緒日記              │" + C_RESET)
    print(C_BOLD + C_BLUE + " ╰───────────────────────────────────────╯" + C_RESET)
    print()

    now   = datetime.datetime.now()
    date  = now.strftime("%Y-%m-%d")
    time_ = now.strftime("%H:%M")

    print(C_BOLD + C_WHITE + f"  📅 今天日期：{date}" + C_RESET)
    print()

    # ── Step 1: Choose emotion ──────────────────────────────────────
    print(C_BOLD + C_WHITE + "  🌟 第一步：現在感覺怎麼樣？" + C_RESET)
    print(C_GRAY + "  選一個情緒小怪獸（輸入代號）：" + C_RESET)
    print()

    rows = [
        [("😊", "開心"), ("😢", "難過"), ("😠", "生氣"), ("😨", "害怕")],
        [("😮", "驚訝"), ("😴", "累了"), ("🤗", "舒服"), ("🤔", "好奇")],
    ]
    for row in rows:
        line = "  "
        for emoji, name in row:
            line += f"  {emoji} {name:<4}"
        print(line)
    print()

    while True:
        emoji = ask("  你的選擇（例：😊）：").strip()
        if emoji in EMOTIONS:
            break
        print(C_GRAY + "  試試看選一個情緒哦 😊" + C_RESET)

    emotion_name = EMOTIONS[emoji]["name"]

    # ── Step 2: Trigger ─────────────────────────────────────────────
    clear_screen()
    print()
    print(C_BOLD + C_BLUE + f"  {emoji} 你選了「{emotion_name}情緒小怪獸」！" + C_RESET)
    print()
    print(C_BOLD + C_WHITE + "  🌟 第二步：是什麼事情讓你這樣呢？" + C_RESET)
    print(C_GRAY + "  （爸爸媽媽可以幫忙說明，幼兒可以說『不知道』）" + C_RESET)
    print()
    trigger = ask("  事件（直接按Enter也可以）：")

    # ── Step 3: Intensity ───────────────────────────────────────────
    clear_screen()
    print()
    print(C_BOLD + C_BLUE + f"  {emoji} {emotion_name}情緒小怪獸，多大呢？" + C_RESET)
    print()
    print(C_BOLD + C_WHITE + "  🌟 第三步：這個情緒有多強烈？" + C_RESET)
    print()
    print("  " + "⭐" * 1 + "  " + "   很小")
    print("  " + "⭐" * 2 + "  " + "   小")
    print("  " + "⭐" * 3 + "  " + "   普通")
    print("  " + "⭐" * 4 + "  " + "   大")
    print("  " + "⭐" * 5 + "  " + "   超級大 💥")
    print()
    intensity = ask_int("  選 1-5 顆星（直接 Enter = 3）：", 1, 5)

    # ── Step 4: Note ────────────────────────────────────────────────
    clear_screen()
    print()
    print(C_BOLD + C_BLUE + f"  {emoji} {emotion_name}情緒小怪獸！" + C_RESET)
    print()
    print(C_BOLD + C_WHITE + "  🌟 最後一步：有什麼想說的話嗎？" + C_RESET)
    print(C_GRAY + "  （可以畫個表情，或是說一句話）" + C_RESET)
    print()
    note = ask("  想說的話（直接 Enter 也可以）：")

    # ── Save ────────────────────────────────────────────────────────
    entry = {
        "date":      date,
        "time":      time_,
        "emotion":   emoji,
        "name":      emotion_name,
        "trigger":   trigger or "（未記錄）",
        "intensity": intensity,
        "note":      note,
    }

    entries = load_entries()
    entries.append(entry)
    save_entries(entries)

    clear_screen()
    print()
    print(C_BOLD + C_GREEN + "  🌟 紀錄完成！情緒小怪獸收到你的訊息了！" + C_RESET)
    print(C_GREEN + f"  {emoji} {emotion_name} · {date} {time_}" + C_RESET)
    print()
    print(C_GRAY + "  按 Enter 回到主選單..." + C_RESET)
    try:
        input()
    except (EOFError, KeyboardInterrupt):
        pass


# ── Statistics ──────────────────────────────────────────────────────────

def mood_stars(n: int) -> str:
    return "⭐" * n + "☆" * (5 - n)


def show_stats():
    clear_screen()
    entries = load_entries()

    print()
    print(C_BOLD + C_PURPLE + " ╭───────────────────────────────────────╮" + C_RESET)
    print(C_BOLD + C_PURPLE + " │  📊 情緒小怪獸：本週情緒報告          │" + C_RESET)
    print(C_BOLD + C_PURPLE + " ╰───────────────────────────────────────╯" + C_RESET)
    print()

    if not entries:
        print(C_GRAY + "  還沒有情緒記錄喔！先去記錄一筆吧 📔" + C_RESET)
        print()
        print(C_GRAY + "  按 Enter 回到主選單..." + C_RESET)
        try:
            input()
        except (EOFError, KeyboardInterrupt):
            pass
        return

    # Filter last 7 days
    today   = datetime.date.today()
    cutoff  = (today - datetime.timedelta(days=7)).isoformat()
    week    = [e for e in entries if e["date"] >= cutoff]

    if not week:
        print(C_GRAY + "  本週還沒有記錄喔！" + C_RESET)
    else:
        # ── Emotion counts ──────────────────────────────────────────
        counts = {}
        for e in week:
            key = e["emotion"]
            counts[key] = counts.get(key, 0) + 1

        print(C_BOLD + C_WHITE + "  🌟 本週最常見的情緒小怪獸：" + C_RESET)
        print()
        sorted_emotions = sorted(counts.items(), key=lambda x: -x[1])
        for emoji, cnt in sorted_emotions:
            name = EMOTIONS.get(emoji, {}).get("name", emoji)
            bar  = "█" * cnt
            color = EMOTIONS.get(emoji, {}).get("color", C_GRAY)
            print(f"  {emoji} {color}{name:<4}{C_RESET} {cnt} 筆  {color}{bar}{C_RESET}")
        print()

        # ── Trend bar (day by day) ───────────────────────────────────
        day_names = ["一", "二", "三", "四", "五", "六", "日"]
        print(C_BOLD + C_WHITE + "  📈 本週情緒趨勢（按強度）：" + C_RESET)
        print()

        day_avg = {}
        for i in range(7):
            day = (today - datetime.timedelta(days=6 - i)).isoformat()
            day_entries = [e for e in week if e["date"] == day]
            if day_entries:
                avg = sum(e["intensity"] for e in day_entries) / len(day_entries)
            else:
                avg = 0
            day_avg[i] = avg

        # Print bar chart (max height = 5 stars)
        for row in range(5, 0, -1):
            line = "  "
            for i in range(7):
                if day_avg[i] >= row:
                    line += C_ORANGE + "█  " + C_RESET
                else:
                    line += C_GRAY + "·  " + C_RESET
            label = C_GRAY + day_names[i] + C_RESET
            print(line + C_GRAY + f" {row}星" + C_RESET)

        print(C_GRAY + "  " + "─" * 23 + C_RESET)
        print(C_GRAY + "  " + " ".join(f"{n:>1}" for n in day_names) + C_RESET)
        print()

        # ── Progress tracker ─────────────────────────────────────────
        print(C_BOLD + C_WHITE + "  🌟 進步追蹤：" + C_RESET)
        all_sorted = sorted(entries, key=lambda x: (x["date"], x["time"]))
        anger_days = {}
        for e in all_sorted:
            if e["emotion"] == "😠":
                anger_days.setdefault(e["date"], 0)
                anger_days[e["date"]] += 1

        if len(anger_days) >= 2:
            sorted_dates = sorted(anger_days.keys())
            older = anger_days.get(sorted_dates[-2], 0)
            newer = anger_days.get(sorted_dates[-1], 0)
            if newer < older:
                print(C_GREEN + f"  🌟🌟 太好了！生氣小怪獸來的次數變少了！繼續加油！" + C_RESET)
            else:
                print(C_GRAY + "  每個情緒都是正常的，慢慢學習就是進步 🌱" + C_RESET)
        else:
            print(C_GRAY + "  每個情緒都是正常的，慢慢學習就是進步 🌱" + C_RESET)
        print()

    print(C_GRAY + "  按 Enter 回到主選單..." + C_RESET)
    try:
        input()
    except (EOFError, KeyboardInterrupt):
        pass


def show_all_entries():
    clear_screen()
    entries = load_entries()

    print()
    print(C_BOLD + C_PURPLE + " ╭───────────────────────────────────────╮" + C_RESET)
    print(C_BOLD + C_PURPLE + " │  📖 情緒小怪獸：所有記錄              │" + C_RESET)
    print(C_BOLD + C_PURPLE + " ╰───────────────────────────────────────╯" + C_RESET)
    print()

    if not entries:
        print(C_GRAY + "  還沒有任何記錄喔！📔" + C_RESET)
    else:
        # Show last 20 entries
        for e in entries[-20:][::-1]:
            emoji  = e["emotion"]
            name   = EMOTIONS.get(emoji, {}).get("name", emoji)
            color  = EMOTIONS.get(emoji, {}).get("color", C_GRAY)
            stars  = mood_stars(e["intensity"])
            date   = e["date"]
            time_  = e["time"]
            print(f"  {emoji} {color}{name:<4}{C_RESET} {date} {time_}  {stars}")
            print(f"       💬 {e.get('note', '')}")
            print()

    print(C_GRAY + "  按 Enter 回到主選單..." + C_RESET)
    try:
        input()
    except (EOFError, KeyboardInterrupt):
        pass


def show_menu():
    clear_screen()
    print()
    print(C_BOLD + C_YELLOW + " ╭───────────────────────────────────────╮" + C_RESET)
    print(C_BOLD + C_YELLOW + " │  📔 情緒小怪獸：情緒日記              │" + C_RESET)
    print(C_BOLD + C_YELLOW + " ╰───────────────────────────────────────╯" + C_RESET)
    print()
    print(C_BOLD + C_WHITE + "  請選擇功能：" + C_RESET)
    print()
    print(f"  {C_GREEN}1.{C_RESET}  📝  新增一筆情緒記錄")
    print(f"  {C_GREEN}2.{C_RESET}  📊  查看本週情緒報告")
    print(f"  {C_GREEN}3.{C_RESET}  📖  查看所有記錄")
    print()
    print(f"  {C_GRAY}Q.{C_RESET}  離開")
    print()


def main():
    while True:
        show_menu()
        choice = ask("  選擇（1-3 或 Q）：", ["1", "2", "3", "q", "Q"])
        if choice in ("q", "Q"):
            clear_screen()
            print()
            print(C_BOLD + C_GREEN + "  🌟 下次再見！情緒小怪獸永遠陪著你！🦋" + C_RESET)
            print()
            break
        if choice == "1":
            record_entry()
        elif choice == "2":
            show_stats()
        elif choice == "3":
            show_all_entries()


if __name__ == "__main__":
    main()
