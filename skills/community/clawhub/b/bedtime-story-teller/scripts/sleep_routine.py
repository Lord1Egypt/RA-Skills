#!/usr/bin/env python3
"""
🌙 睡前作息引導腳本
溫柔提醒爸媽和孩子準備睡覺，配合 Cron Job 使用

使用方法：
  python3 sleep_routine.py --mode cron        # 每日定時提醒
  python3 sleep_routine.py --mode check        # 檢查是否到作息時間
  python3 sleep_routine.py --mode story         # 直接打開故事精靈
  python3 sleep_routine.py --mode setup         # 互動式設定作息時間
"""

import os
import json
import sys
import time
import datetime
from pathlib import Path

# ─────────────────────────────────────────────
# 儲存路徑
# ─────────────────────────────────────────────

DATA_DIR = Path.home() / ".qclaw" / "kids"
CONFIG_FILE = DATA_DIR / "sleep_routine.json"
DATA_DIR.mkdir(parents=True, exist_ok=True)


# ─────────────────────────────────────────────
# 預設作息時間
# ─────────────────────────────────────────────

DEFAULT_ROUTINE = {
    "sleep_hour": 21,       # 21:00 開始睡覺
    "brush_teeth_reminder": 20,  # 20:00 刷牙提醒
    "bath_reminder": 19,    # 19:00 洗澡提醒
    "dinner_reminder": 18,  # 18:00 晚餐提醒
    "enabled": True,
    "quiet_hours_start": 22, # 22:00 後安靜時間
    "quiet_hours_end": 7,    # 早上 7:00 前不提醒
}

EMOJI = {
    "moon": "🌙",
    "star": "⭐",
    "bed": "🛏️",
    "tooth": "🦷",
    "bath": "🛁",
    "food": "🍽️",
    "book": "📖",
    "sleep": "💤",
    "rabbit": "🐰",
}


# ─────────────────────────────────────────────
# 設定管理
# ─────────────────────────────────────────────

def load_config() -> dict:
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return {**DEFAULT_ROUTINE, **json.load(f)}
        except (json.JSONDecodeError, IOError):
            pass
    return dict(DEFAULT_ROUTINE)


def save_config(cfg: dict):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)


def get_current_stage(cfg: dict) -> str:
    """根據現在時間，回傳作息階段"""
    now = datetime.datetime.now()
    hour = now.hour

    # 安靜時段：不打擾
    if hour < cfg.get("quiet_hours_end", 7):
        return "quiet_hours"
    if hour >= cfg.get("quiet_hours_start", 22):
        return "quiet_hours"

    if hour >= cfg.get("sleep_hour", 21):
        return "bedtime"
    if hour >= cfg.get("brush_teeth_reminder", 20):
        return "brushing"
    if hour >= cfg.get("bath_reminder", 19):
        return "bathing"
    if hour >= cfg.get("dinner_reminder", 18):
        return "dinner"
    return "waiting"


STAGE_MESSAGES = {
    "quiet_hours": {
        "title": "🌙 安靜時段",
        "body": "已經是安靜時間了，小朋友應該已經睡著了吧？晚安！💤",
        "action": None,
    },
    "bedtime": {
        "title": "🌙 該睡覺啦！",
        "body": "月亮都高高掛在天上囉，星星也在眨眼睛。\n"
                "小朋友，晚安，做個甜甜的夢 🌙✨\n\n"
                "💡 明天再來聽故事吧！",
        "action": None,
    },
    "brushing": {
        "title": "🦷 刷牙俠上線！",
        "body": "現在是 {current_time}，該刷牙囉！\n\n"
                "上排牙齒刷一刷，下排牙齒刷一刷，\n"
                "舌頭也要刷一刷，這樣才乾淨喔！\n\n"
                "刷完牙了嗎？✨\n"
                "刷完之後，就可以選一個最喜歡的故事聽啦！📖",
        "action": "story",
    },
    "bathing": {
        "title": "🛁 洗澡時間到！",
        "body": "現在是 {current_time}，該洗澡囉！\n\n"
                "身體洗香香，頭髮洗乾淨，\n"
                "穿好睡衣，暖暖的準備睡覺！\n\n"
                "洗完之後就是刷牙時間，然後就是故事時間啦～ 🐰",
        "action": None,
    },
    "dinner": {
        "title": "🍽️ 吃晚餐時間！",
        "body": "肚子餓餓了嗎？先吃飽飽才有力氣長大喔！\n\n"
                "吃完晚餐、洗澡、刷牙之後，\n"
                "就是最期待的睡前故事時間啦！🌙",
        "action": None,
    },
    "waiting": {
        "title": "🌙 睡前作息引導",
        "body": "今天過得怎麼樣呀？\n\n"
                "晚餐後、洗澡後、刷牙後，\n"
                "就是我們的睡前故事時間囉！\n\n"
                "現在幾點了呢？\n"
                "🌙 21:00 睡覺\n"
                "🦷 20:00 刷牙\n"
                "🛁 19:00 洗澡\n"
                "🍽️ 18:00 晚餐",
        "action": None,
    },
}


# ─────────────────────────────────────────────
# 訊息格式化
# ─────────────────────────────────────────────

def format_message(stage: str, cfg: dict) -> dict:
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M")
    sleep_time = f"{cfg.get('sleep_hour', 21)}:00"
    brush_time = f"{cfg.get('brush_teeth_reminder', 20)}:00"
    bath_time = f"{cfg.get('bath_reminder', 19)}:00"
    dinner_time = f"{cfg.get('dinner_reminder', 18)}:00"

    msg = STAGE_MESSAGES.get(stage, STAGE_MESSAGES["waiting"]).copy()
    body = msg["body"].format(
        current_time=current_time,
        sleep_time=sleep_time,
        brush_time=brush_time,
        bath_time=bath_time,
        dinner_time=dinner_time,
    )
    return {
        "title": msg["title"],
        "body": body,
        "action": msg["action"],
        "stage": stage,
    }


# ─────────────────────────────────────────────
# 互動式設定
# ─────────────────────────────────────────────

def interactive_setup():
    """引導爸媽設定作息時間"""
    print()
    print("=" * 50)
    print("  🌙 睡前作息設定 🌙")
    print("=" * 50)
    print()
    print("  請依序設定每天的作息時間\n")

    cfg = {}

    prompts = [
        ("晚餐提醒時間（時，18-20）", "dinner_reminder", 18),
        ("洗澡提醒時間（時，19-21）", "bath_reminder", 19),
        ("刷牙提醒時間（時，20-21）", "brush_teeth_reminder", 20),
        ("睡覺時間（時，20-22）", "sleep_hour", 21),
        ("安靜時段開始（時，預設 22）", "quiet_hours_start", 22),
        ("安靜時段結束（時，預設 7）", "quiet_hours_end", 7),
    ]

    for label, key, default in prompts:
        while True:
            raw = input(f"  {label}：").strip()
            if not raw:
                value = default
                break
            try:
                value = int(raw)
                if key == "quiet_hours_end" and (value < 0 or value > 12):
                    print("  請輸入 0-12 的數字")
                    continue
                elif value < 0 or value > 23:
                    print("  請輸入 0-23 的數字")
                    continue
                break
            except ValueError:
                print("  請輸入數字")
        cfg[key] = value

    cfg["enabled"] = True
    save_config(cfg)

    print()
    print("  ✅ 設定已儲存！")
    print()
    print("  📋 今天的作息時間表：")
    print(f"  🍽️  {cfg['dinner_reminder']}:00  晚餐提醒")
    print(f"  🛁  {cfg['bath_reminder']}:00  洗澡提醒")
    print(f"  🦷  {cfg['brush_teeth_reminder']:02d}:00  刷牙提醒")
    print(f"  🌙  {cfg['sleep_hour']:02d}:00  睡覺時間")
    print()
    return cfg


# ─────────────────────────────────────────────
# Cron 模式
# ─────────────────────────────────────────────

def cron_mode():
    """
    Cron Job 呼叫：根據當下時間輸出相應的作息提醒。
    由外部 agent 讀取並發送給爸媽。
    """
    cfg = load_config()

    if not cfg.get("enabled", True):
        sys.exit(0)

    stage = get_current_stage(cfg)
    msg = format_message(stage, cfg)

    # 輸出給 agent
    print("=== SLEEP ROUTINE ===")
    print(f"stage:{msg['stage']}")
    print(f"title:{msg['title']}")
    print(f"action:{msg['action'] or 'none'}")
    print("=== BODY ===")
    print(msg["body"])
    print("=== END ===")

    # 如果是刷牙階段，給爸媽一個故事精靈的觸發提示
    if msg["action"] == "story":
        print("\n[skill:bedtime-story-teller]")


def check_mode():
    """檢查當前作息狀態"""
    cfg = load_config()
    stage = get_current_stage(cfg)
    msg = format_message(stage, cfg)

    print()
    print(f"🌙 目前階段：{msg['title']}")
    print()
    print(msg["body"])
    print()

    if msg["action"] == "story":
        print("💡 準備進入睡前故事時間！")
        print("   說「講個睡前故事」就會啟動 🌙")
    return msg


# ─────────────────────────────────────────────
# 主程式
# ─────────────────────────────────────────────

def main():
    import argparse

    parser = argparse.ArgumentParser(description="🌙 睡前作息引導")
    parser.add_argument("--mode", choices=["cron", "check", "story", "setup"],
                        default="check",
                        help="模式：cron=定時提醒, check=查看狀態, story=直接講故事, setup=設定時間")
    parser.add_argument("--enabled", type=lambda x: x.lower() == "true",
                        help="啟用/停用作息提醒")
    parser.add_argument("--quiet", action="store_true",
                        help="安靜模式（不輸出細節）")
    args = parser.parse_args()

    cfg = load_config()

    # 設定模式
    if args.mode == "setup":
        cfg = interactive_setup()
        return

    # 啟用/停用
    if args.enabled is not None:
        cfg["enabled"] = args.enabled
        save_config(cfg)
        state = "啟用" if cfg["enabled"] else "停用"
        print(f"\n  ✅ 作息提醒已{state}\n")
        return

    # Cron 模式
    if args.mode == "cron":
        cron_mode()
        return

    # 檢查模式
    if args.mode == "check":
        check_mode()
        return

    # 直接進故事
    if args.mode == "story":
        from story_generator import StoryGenerator
        gen = StoryGenerator(age="toddler", length="short")
        story = gen.generate()
        print(f"\n🌙 {story['title']}\n")
        for para in story["story"].split("\n"):
            if para.strip():
                print(f"  {para.strip()}\n")
        print(f"💡 {story['lesson']}\n")
        return


if __name__ == "__main__":
    main()
