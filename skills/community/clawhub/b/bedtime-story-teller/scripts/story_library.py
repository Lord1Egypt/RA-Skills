#!/usr/bin/env python3
"""
🌙 睡前故事精靈 — 故事圖書館
收藏最愛、歷史記錄、引導式點播、分類管理
"""

import os
import json
import sys
import time
from pathlib import Path

# ─────────────────────────────────────────────
# 儲存路徑
# ─────────────────────────────────────────────

LIB_DIR = Path.home() / ".qclaw" / "kids"
FAVORITES_FILE = LIB_DIR / "favorites.json"
HISTORY_FILE = LIB_DIR / "history.json"
SETTINGS_FILE = LIB_DIR / "settings.json"

LIB_DIR.mkdir(parents=True, exist_ok=True)


# ─────────────────────────────────────────────
# 資料庫管理
# ─────────────────────────────────────────────

def load_json(path: Path, default):
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return default


def save_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ─────────────────────────────────────────────
# 故事資料結構
# ─────────────────────────────────────────────

def make_entry(story_data: dict) -> dict:
    return {
        "id": f"{story_data['protagonist']}_{int(time.time())}",
        "title": story_data["title"],
        "story_preview": story_data["story"][:80] + "……",
        "lesson": story_data.get("lesson", ""),
        "emoji": story_data.get("emoji", "🌙"),
        "theme": story_data.get("theme", ""),
        "age": story_data.get("age", "toddler"),
        "protagonist": story_data.get("protagonist", ""),
        "pet": story_data.get("pet", ""),
        "length": story_data.get("length", "short"),
        "duration_min": _parse_duration(story_data),
        "saved_at": time.strftime("%Y-%m-%d %H:%M"),
        "times_played": 0,
        "last_played": None,
    }


def _parse_duration(story_data: dict) -> int:
    length = story_data.get("length", "short")
    age = story_data.get("age", "toddler")
    table = {
        ("short", "toddler"): 2,
        ("short", "preschool"): 3,
        ("medium", "toddler"): 4,
        ("medium", "preschool"): 5,
        ("long", "toddler"): 7,
        ("long", "preschool"): 8,
    }
    return table.get((length, age), 3)


# ─────────────────────────────────────────────
# 圖書館操作
# ─────────────────────────────────────────────

class StoryLibrary:
    """故事圖書館管理器"""

    def __init__(self):
        self.favorites = load_json(FAVORITES_FILE, [])
        self.history = load_json(HISTORY_FILE, [])
        self.settings = load_json(SETTINGS_FILE, {
            "default_age": "toddler",
            "default_length": "short",
            "last_pet": None,
            "last_protagonist": None,
        })

    # ── 最愛管理 ──

    def add_favorite(self, story_data: dict) -> bool:
        """加入最愛"""
        entry = make_entry(story_data)
        # 防重複：依 title 比對
        for fav in self.favorites:
            if fav["title"] == entry["title"]:
                return False
        self.favorites.insert(0, entry)
        self._trim(self.favorites, max_items=50)
        save_json(FAVORITES_FILE, self.favorites)
        return True

    def remove_favorite(self, story_id: str) -> bool:
        """移除最愛"""
        before = len(self.favorites)
        self.favorites = [f for f in self.favorites if f["id"] != story_id]
        if len(self.favorites) < before:
            save_json(FAVORITES_FILE, self.favorites)
            return True
        return False

    def list_favorites(self,
                       theme: str = None,
                       age: str = None,
                       protagonist: str = None) -> list:
        """篩選最愛"""
        result = self.favorites
        if theme:
            result = [f for f in result if f.get("theme") == theme]
        if age:
            result = [f for f in result if f.get("age") == age]
        if protagonist:
            result = [f for f in result
                      if protagonist in f.get("protagonist", "")]
        return result

    # ── 歷史記錄 ──

    def add_history(self, story_data: dict):
        """加入歷史記錄"""
        entry = make_entry(story_data)
        entry["times_played"] = 1
        entry["last_played"] = time.strftime("%Y-%m-%d %H:%M")
        # 合併相同 title
        for h in self.history:
            if h["title"] == entry["title"]:
                h["times_played"] = h.get("times_played", 0) + 1
                h["last_played"] = entry["last_played"]
                save_json(HISTORY_FILE, self.history)
                return
        self.history.insert(0, entry)
        self._trim(self.history, max_items=30)
        save_json(HISTORY_FILE, self.history)

    def list_history(self, limit: int = 10) -> list:
        return self.history[:limit]

    def clear_history(self):
        self.history = []
        save_json(HISTORY_FILE, self.history)

    # ── 設定 ──

    def save_settings(self, **kwargs):
        self.settings.update(kwargs)
        save_json(SETTINGS_FILE, self.settings)

    @staticmethod
    def _trim(lst: list, max_items: int):
        while len(lst) > max_items:
            lst.pop()


# ─────────────────────────────────────────────
# 引導式點播介面
# ─────────────────────────────────────────────

THEME_QUESTIONS = [
    {
        "q": "今晚想聽什麼主題的故事呀？",
        "options": [
            ("🌈 友誼冒險", "friendship"),
            ("💤 認識情緒", "emotion"),
            ("🏠 成語改編", "idiom"),
            ("📖 格林童話", "fairytale"),
            ("✨ 隨便一個", None),
        ]
    },
    {
        "q": "故事的主角是誰呢？",
        "options": [
            ("🐰 小兔子", "小兔子"),
            ("🧸 小熊", "小熊"),
            ("🦊 小狐狸", "小狐狸"),
            ("🐱 小貓咪", "小貓咪"),
            ("🤖 自己選", None),
            ("✨ 隨機", "random"),
        ]
    },
    {
        "q": "小朋友今年幾歲呀？",
        "options": [
            ("👶 2-3 歲（小班的）」", "toddler"),
            ("🧒 4-6 歲（中班的）」", "preschool"),
        ]
    },
    {
        "q": "想要多長的故事呀？",
        "options": [
            ("🌙 短短的（2-3分鐘）」", "short"),
            ("📖 中等的（4-5分鐘）」", "medium"),
            ("🏰 長長的（7-8分鐘）」", "long"),
        ]
    },
]


def guided_mode(library: StoryLibrary = None):
    """
    引導式點播：一步步問問題，最後生成故事。
    返回 (story_data, user_choices)
    """
    from story_generator import StoryGenerator

    choices = {}
    answers = {}

    print()
    print_separator("🌙 今晚想聽什麼故事？")

    for i, step in enumerate(THEME_QUESTIONS, 1):
        q = step["q"]
        options = step["options"]

        print()
        print(f"  {q}")
        for j, (label, value) in enumerate(options, 1):
            print(f"    {j}. {label}")

        # 嘗試自動回答（使用上次設定）
        if library:
            default_answer = None
            if i == 1:  # 主題
                default_answer = library.settings.get("last_theme")
            elif i == 3:  # 年齡
                default_answer = library.settings.get("default_age")

            if default_answer:
                for j, (label, value) in enumerate(options, 1):
                    if value == default_answer:
                        print(f"\n  💡 使用上次設定：{label}")
                        choices[q] = value
                        answers[q] = label
                        break
                if q in choices:
                    continue

        while True:
            try:
                raw = input("\n  請輸入數字：").strip()
                if not raw:
                    continue
                idx = int(raw) - 1
                if 0 <= idx < len(options):
                    label, value = options[idx]
                    choices[q] = value
                    answers[q] = label
                    break
            except (ValueError, IndexError):
                pass
            print("  請輸入正確的數字喔！")

    # 產出參數
    protagonist = choices.get(THEME_QUESTIONS[1]["q"])
    if protagonist == "random":
        protagonist = None
    elif protagonist == "自己選":
        protagonist = input("  請輸入主角名稱：").strip() or None

    age = choices.get(THEME_QUESTIONS[2]["q"], "toddler")
    length = choices.get(THEME_QUESTIONS[3]["q"], "short")
    theme = choices.get(THEME_QUESTIONS[0]["q"])

    # 生成故事
    gen = StoryGenerator(
        protagonist=protagonist,
        age=age,
        length=length,
        theme=theme,
    )
    story_data = gen.generate()

    # 儲存設定
    if library:
        library.save_settings(
            default_age=age,
            default_length=length,
            last_theme=theme,
        )

    return story_data, answers


# ─────────────────────────────────────────────
# 文字選單
# ─────────────────────────────────────────────

def print_separator(title: str = ""):
    bar = "─" * 40
    print(f"\n  {bar}")
    if title:
        print(f"  {title}")
    print(f"  {bar}\n")


def print_story_card(entry: dict, index: int = None):
    """單一故事卡片"""
    emoji = entry.get("emoji", "🌙")
    title = entry.get("title", "???")
    protagonist = entry.get("protagonist", "")
    age_display = "👶" if entry.get("age") == "toddler" else "🧒"
    duration = entry.get("duration_min", 3)
    saved_at = entry.get("saved_at", "")
    times = entry.get("times_played", 0)

    if index is not None:
        print(f"  {index:2d}. {emoji} {title}")
    else:
        print(f"  {emoji} {title}")

    meta = f"     {age_display} {protagonist} · 約{duration}分鐘"
    if saved_at:
        meta += f" · {saved_at}"
    if times > 1:
        meta += f" · 已聽{times}次"
    print(f"  {meta}\n")


def list_all(library: StoryLibrary):
    """列出所有最愛"""
    favs = library.list_favorites()
    if not favs:
        print("\n  🌙 收藏夾是空的喔，聽完故事可以按 3 存起來！\n")
        return

    print_separator("📚 我的最愛收藏")
    for i, fav in enumerate(favs, 1):
        print_story_card(fav, i)


def list_history_menu(library: StoryLibrary):
    """列出最近歷史"""
    history = library.list_history(limit=15)
    if not history:
        print("\n  🌙 還沒有播放記錄，開始聽故事吧！\n")
        return

    print_separator("🕐 最近播放")
    for i, h in enumerate(history, 1):
        print_story_card(h, i)


# ─────────────────────────────────────────────
# 主程式
# ─────────────────────────────────────────────

def main():
    import argparse

    parser = argparse.ArgumentParser(description="🌙 故事圖書館")
    parser.add_argument("--list-favorites", action="store_true")
    parser.add_argument("--list-history", action="store_true")
    parser.add_argument("--clear-history", action="store_true")
    parser.add_argument("--add-favorite", help="加入最愛（故事 JSON 檔案）")
    parser.add_argument("--guided", action="store_true",
                        help="引導式點播模式")
    args = parser.parse_args()

    library = StoryLibrary()

    if args.clear_history:
        library.clear_history()
        print("\n  ✅ 歷史記錄已清除\n")
        return

    if args.add_favorite:
        import json
        with open(args.add_favorite) as f:
            story_data = json.load(f)
        if library.add_favorite(story_data):
            print(f"\n  ✅ 已加入最愛：{story_data.get('title', '???')}\n")
        else:
            print("\n  ⚠  這個故事已經在最愛裡了\n")
        return

    if args.list_favorites:
        list_all(library)
        return

    if args.list_history:
        list_history_menu(library)
        return

    # 預設：引導式點播
    print("\n🌙 睡前故事精靈 — 圖書館模式 🌙")
    print("  📚 顯示最愛收藏  →  python3 story_library.py --list-favorites")
    print("  🕐 顯示播放記錄  →  python3 story_library.py --list-history")
    print("  🌙 開始點播      →  python3 story_library.py --guided")
    print()


if __name__ == "__main__":
    main()
