#!/usr/bin/env python3
"""
🌙 睡前故事精靈 — 朗讀腳本
整合 OpenClaw TTS，自動朗讀故事
"""

import sys
import os
import time

# ─────────────────────────────────────────────
# ANSI 彩色輸出
# ─────────────────────────────────────────────

COLORS = {
    "title": "\033[95m",    # 粉紫色標題
    "story": "\033[96m",    # 青色故事文字
    "lesson": "\033[93m",   # 黃色金句
    "prompt": "\033[92m",   # 綠色提示
    "end": "\033[0m",       # 重置
    "bold": "\033[1m",
    "dim": "\033[2m",
}

EMOJI_STORY = ["🐰", "🧸", "🦊", "🐱", "🐶", "🐢", "🦋", "⭐", "🌙", "✨"]
CUSTOM_PROMPT = None  # 由外部設定的 TTS 工具


def color(text: str, key: str) -> str:
    return f"{COLORS.get(key, '')}{text}{COLORS['end']}"


# ─────────────────────────────────────────────
# TTS 整合層（由 Agent 注入 tts tool）
# ─────────────────────────────────────────────

class TTSPlayer:
    """TTS 朗讀管理器"""

    def __init__(self, tts_tool=None, slow: bool = True):
        """
        tts_tool: 外部注入的 tts 函數，簽名為 tts(text: str, channel: str)
                  若為 None，則使用彩色文字模式
        slow: 是否使用慢速朗讀（幼兒模式）
        """
        self.tts_tool = tts_tool
        self.slow = slow
        self._stop_requested = False

    def stop(self):
        """請求中斷朗讀"""
        self._stop_requested = True

    def speak(self, text: str, channel: str = "voice") -> bool:
        """
        朗讀一段文字。
        成功返回 True，若中途被中斷返回 False。
        """
        self._stop_requested = False

        if self.tts_tool:
            try:
                self.tts_tool(text=text, channel=channel)
                return True
            except Exception as e:
                print(color(f"[TTS 錯誤] {e}", "title"))
                # fallback 到文字模式
                self._print_text(text)
        else:
            self._print_text(text)

        return not self._stop_requested

    def _print_text(self, text: str):
        """彩色文字輸出（當 TTS 不可用時）"""
        print(color(f"\n  {text}\n", "story"))

    def speak_story(self, story_data: dict, tts_channel: str = "voice") -> bool:
        """
        朗讀完整故事，包含標題、段落、結尾。
        返回是否完整朗讀完畢（未被中斷）。
        """
        emoji = story_data.get("emoji", "🌙")
        title = story_data.get("title", "✨ 睡前故事 ✨")
        story = story_data.get("story", "")
        lesson = story_data.get("lesson", "")

        # ── 標題 ──
        title_block = f"{emoji} {title} {emoji}"
        print()
        print(color("=" * 50, "title"))
        print(color(f"  {title_block}", "bold title"))
        print(color("=" * 50, "title"))
        print()

        # 朗讀標題
        self.speak(title_block)

        # ── 分段朗讀 ──
        paragraphs = [p.strip() for p in story.split("\n") if p.strip()]
        total = len(paragraphs)

        for i, para in enumerate(paragraphs, 1):
            if self._stop_requested:
                print(color(f"\n⚠ 已中斷朗讀", "prompt"))
                return False

            # 進度提示
            progress = color(f"  {emoji} 第 {i}/{total} 段", "dim")
            print(progress)

            # 朗讀
            self.speak(para, channel=tts_channel)
            time.sleep(0.3)  # 段落間距

        # ── 金句 ──
        if lesson:
            print(color("─" * 40, "title"))
            print(color(f"  💡 {lesson}", "lesson"))
            print(color("─" * 40, "title"))
            self.speak(f"今天的金句是：{lesson}")
            print()

        # ── 晚安 ──
        goodnight = "🌙 晚安，做個甜甜的夢喔…… 💤"
        print(color(f"\n  {goodnight}\n", "bold story"))
        self.speak("晚安，做個甜甜的夢喔。")
        return True


# ─────────────────────────────────────────────
# 互動式朗讀選單
# ─────────────────────────────────────────────

def prompt_play(story_data: dict):
    """顯示朗讀提示選單"""
    print(color("  🎵 要我朗讀這個故事嗎？", "prompt"))
    print(color("  1️⃣  用聲音朗讀（🌙 溫柔慢速）", "prompt"))
    print(color("  2️⃣  只顯示文字就好", "prompt"))
    print(color("  3️⃣  這個故事很棒！存到我的最愛", "prompt"))
    print()


def interactive_player():
    """互動式朗讀模式"""
    from story_generator import StoryGenerator

    print(color("\n🌙 睡前故事精靈 — 朗讀模式 🌙\n", "bold title"))
    print(color("  請選擇想要的功能：\n", "story"))
    print(color("  1️⃣  隨機故事（適合所有年齡）", "prompt"))
    print(color("  2️⃣  小一點的故事（2-3歲）", "prompt"))
    print(color("  3️⃣  比較大的故事（4-6歲）", "prompt"))
    print(color("  4️⃣  情緒相關的故事", "prompt"))
    print(color("  5️⃣  友誼冒險的故事", "prompt"))
    print(color("  6️⃣  成語改編故事", "prompt"))
    print(color("  7️⃣  格林童話改編", "prompt"))
    print()

    choice = input(color("  請輸入數字（1-7）：", "prompt")).strip()

    age_map = {"1": None, "2": "toddler", "3": "preschool",
               "4": "emotion", "5": "friendship",
               "6": "idiom", "7": "fairytale"}
    theme_map = {"4": "emotion", "5": "friendship",
                 "6": "idiom", "7": "fairytale"}

    gen = StoryGenerator(
        protagonist=None,
        age=age_map.get(choice, "toddler") or "toddler",
        theme=theme_map.get(choice),
        length="short",
    )

    story = gen.generate()
    player = TTSPlayer()

    print()
    play_choice = input(
        color("  🎵 朗讀故事（按 Enter），或輸入 2 只看文字：", "prompt")
    ).strip()

    if play_choice != "2":
        player.speak_story(story)
    else:
        print_story_text(story)


def print_story_text(story_data: dict):
    """純文字顯示故事（不朗讀）"""
    emoji = story_data.get("emoji", "🌙")
    title = story_data.get("title", "✨ 睡前故事 ✨")
    story = story_data.get("story", "")
    lesson = story_data.get("lesson", "")

    print(color(f"\n{emoji} {title} {emoji}\n", "bold title"))
    paragraphs = [p.strip() for p in story.split("\n") if p.strip()]
    for para in paragraphs:
        print(color(f"  {para}\n", "story"))
    if lesson:
        print(color(f"  💡 {lesson}\n", "lesson"))


# ─────────────────────────────────────────────
# 主程式
# ─────────────────────────────────────────────

def main():
    import argparse

    parser = argparse.ArgumentParser(description="🌙 睡前故事朗讀器")
    parser.add_argument("--story-json", help="從 JSON 載入故事資料")
    parser.add_argument("--text", "-t", help="直接朗讀指定文字")
    parser.add_argument("--no-interact", action="store_true", help="非互動模式")
    args = parser.parse_args()

    if args.text:
        player = TTSPlayer()
        player.speak(args.text)
        return

    if args.story_json:
        import json
        with open(args.story_json) as f:
            story_data = json.load(f)
        player = TTSPlayer()
        player.speak_story(story_data)
        return

    # 預設進入互動模式
    interactive_player()


if __name__ == "__main__":
    main()
