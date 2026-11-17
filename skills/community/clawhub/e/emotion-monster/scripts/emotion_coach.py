#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
情緒小怪獸 - 情緒急救箱
Emotion Monster: Emotion First-Aid Coach for Parents
When a child is crying / angry / scared — a step-by-step guide.
"""

import sys
import os
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

# ── Emotion definitions ─────────────────────────────────────────────────
EMOTIONS = {
    "😠": {
        "name":        "生氣",
        "monster":     "生氣小怪獸",
        "color":       C_RED,
        "arrived_msg": "我看到生氣小怪獸跑出來了！",
        "body":        "身體可能：臉漲紅、握拳、跺腳、心跳加速",
    },
    "😢": {
        "name":        "難過",
        "monster":     "難過小怪獸",
        "color":       C_BLUE,
        "arrived_msg": "我看到難過小怪獸跑出來了！",
        "body":        "身體可能：眼眶紅、眼淚、肩膀垂下來",
    },
    "😨": {
        "name":        "害怕",
        "monster":     "害怕小怪獸",
        "color":       C_PURPLE,
        "arrived_msg": "我看到害怕小怪獸跑出來了！",
        "body":        "身體可能：發抖、躲起來、心跳很快",
    },
    "😮": {
        "name":        "驚訝（被嚇到）",
        "monster":     "驚訝小怪獸",
        "color":       C_ORANGE,
        "arrived_msg": "哇！驚訝小怪獸來了！",
        "body":        "身體可能：大叫、跳起來、愣住",
    },
    "😴": {
        "name":        "累了（鬧脾氣）",
        "monster":     "愛睏小怪獸",
        "color":       C_GRAY,
        "arrived_msg": "我看到愛睏小怪獸跑出來了！",
        "body":        "身體可能：揉眼睛、亂發脾氣、動作變慢",
    },
}


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def ask(prompt: str) -> str:
    try:
        return input(C_BOLD + C_WHITE + prompt + " " + C_RESET).strip()
    except (EOFError, KeyboardInterrupt):
        return ""


def banner(title: str, color: str):
    print()
    print(color + " ╭─────────────────────────────────────────────╮" + C_RESET)
    print(color + f" │  {title}" + " " * (43 - len(title)) + "│" + C_RESET)
    print(color + " ╰─────────────────────────────────────────────╯" + C_RESET)
    print()


def step_header(num: int, title: str, emoji: str, color: str):
    print()
    print(color + C_BOLD + f" ┌─ 【步驟 {num}】{emoji} {title}" + C_RESET)
    print(color + C_BOLD + " └" + "─" * 40 + C_RESET + C_RESET)
    print()


def parent_line(text: str, color: str, indent: str = "  "):
    print(indent + color + C_BOLD + "【爸媽說】" + C_RESET + color + text + C_RESET)


def child_line(text: str, color: str, indent: str = "  "):
    print(indent + color + "【給孩子】" + C_RESET + color + "「" + text + "」" + C_RESET)


def tip(text: str):
    print(C_GRAY + f"  💡 小技巧：{text}" + C_RESET)


def breath_guide(stars: int = 3):
    print()
    print(C_BOLD + C_GREEN + "  🌬️ 深呼吸練習（泡泡呼吸法）🌬️" + C_RESET)
    print()
    for i in range(1, stars + 1):
        print(C_BLUE + C_BOLD + f"  第 {i} 次：吸一口氣 → 慢慢吐成一個大泡泡 🫧" + C_RESET)
    print()
    print(C_GRAY + "  如果孩子比較小，可以說：")
    child_line("我們一起變成一隻大魚，吹出大大的泡泡！🐟🫧", C_BLUE)


def coping_tips(emotion_key: str):
    """Print extra coping strategies based on emotion type."""
    tips = {
        "😠": [
            "提供「安全發洩物」：枕頭、捏捏球、可以捶的毛巾",
            "「跺腳區」：讓孩子在墊子上用力跺 5 下",
            "避免說：'不要生气了' → 改說：'我陪你一起冷靜'",
        ],
        "😢": [
            "遞上「眼淚收集器」（一張衛生紙）—— 讓孩子知道流眼淚是 OK 的",
            "說：'我看到你好傷心，想哭就哭，我陪著你'",
            "不要急著說「沒事了」，先讓孩子感受被聽見",
        ],
        "😨": [
            "蹲下來與孩子平視，輕輕說：'我保護你'",
            "不要否認孩子的恐懼（'有什麼好怕的'），先接受恐懼是真的",
            "一起靠近看看恐懼的來源，降低神秘感",
        ],
        "😮": [
            "先穩住自己的情緒（父母先深呼吸）",
            "說：'哇！好意外！我也嚇一跳！' — 示範如何命名驚訝",
            "引導孩子：「現在感覺怎麼樣？」",
        ],
        "😴": [
            "先排除生理需求：餓了？渴了？尿布濕了？",
            "用低沉、溫柔的聲音說：'小熊也想睡覺了……'",
            "提供一個安撫物：最愛的毯子、玩偶",
        ],
    }
    if emotion_key in tips:
        print()
        print(C_BOLD + C_WHITE + "  🌟 根據這個情緒的特別建議：" + C_RESET)
        for t in tips[emotion_key]:
            print(C_GRAY + f"  ✅ {t}" + C_RESET)
        print()


def coach_quick(emotion_key: str = None):
    """One-page quick coach without interactivity."""
    if emotion_key and emotion_key in EMOTIONS:
        target = EMOTIONS[emotion_key]
    else:
        # Pick most intense feeling
        target = None

    clear_screen()
    banner("⚡ 情緒急救箱 — 快速版 ⚡", C_BOLD + C_RED)

    if target:
        e = target
        print(C_BOLD + C_WHITE + f"  偵測到：{emotion_key} {e['monster']}" + C_RESET)
        print(C_GRAY + f"  {e['body']}" + C_RESET)
        print()

    # Step 1
    step_header(1, "命名情緒", "🏷️", C_BOLD + C_YELLOW)
    print(C_YELLOW + "  爸媽的第一步：說出情緒的名字，讓孩子知道他被看見了。" + C_RESET)
    print()
    if target:
        parent_line(f"「{target['arrived_msg']} {target['name']}小怪獸跑出來了！」", C_YELLOW)
        child_line(f"（輕輕蹲下來，平靜地說）", C_GRAY)
        print()
    else:
        parent_line("「我看到你很生氣（難過/害怕）……」", C_YELLOW)
    print()
    print(C_GRAY + "  ✅ 為什麼重要：當孩子知道有人理解他，大腦的「杏仁核」會開始冷靜。" + C_RESET)
    print()

    # Step 2
    step_header(2, "接受情緒", "🤗", C_BOLD + C_BLUE)
    print(C_BLUE + "  爸媽說：這個情緒是正常的，每個人都會有這個情緒。" + C_RESET)
    print()
    parent_line("「生氣（難過/害怕）是正常的，不是你不乖。", C_BLUE)
    parent_line("每個人都會生氣，媽媽也會生氣。」", C_BLUE)
    print()
    child_line("「情緒小怪獸來了，不是壞事，我們陪它坐一坐。」（抱抱）", C_BLUE)
    print()
    print(C_GRAY + "  ❌ 避免：'這有什麼好哭的' / '不准生氣' / '你是哥哥，不可以這樣'" + C_RESET)
    print()

    # Step 3
    step_header(3, "深呼吸引導", "🌬️", C_BOLD + C_GREEN)
    print(C_GREEN + "  深呼吸是最快讓身體冷靜的方法！" + C_RESET)
    print()
    breath_guide(3)
    print()

    # Step 4
    step_header(4, "表達情緒", "🗣️", C_BOLD + C_PURPLE)
    print(C_PURPLE + "  教孩子用嘴巴說出來，而不是用行動爆發出來。" + C_RESET)
    print()
    parent_line("「用嘴巴說：'我因為......很生氣'", C_PURPLE)
    child_line("「我因為......好生氣！」（可以握拳說）", C_PURPLE)
    print()
    print(C_GRAY + "  示範：'我因為弟弟拿了我的玩具，很生氣！'" + C_RESET)
    print()

    # Step 5
    step_header(5, "找到解決方案", "🌟", C_BOLD + C_ORANGE)
    print(C_ORANGE + "  問問孩子：「現在可以怎麼做？」給他選擇。" + C_RESET)
    print()
    options = [
        "🧸 抱一抱最喜歡的玩偶",
        "🏃 出去跑一跑、跳一跳",
        "🎨 畫畫（把情緒畫出來）",
        "🚪 去冷靜角坐一坐",
        "👋 請大人幫忙",
    ]
    for opt in options:
        print(C_ORANGE + f"  {opt}" + C_RESET)
    print()

    # Extra tips
    if target:
        coping_tips(emotion_key)

    # After the storm
    print(C_BOLD + C_GREEN + "  🌈 風暴過後：「我好驕傲你冷靜下來了！🌟」" + C_RESET)
    print()


def coach_interactive():
    """Step-by-step guided session for parents."""
    clear_screen()
    banner("🩹 情緒急救箱 — 互動引導版 🩹", C_BOLD + C_BLUE)

    print(C_BOLD + C_WHITE + "  孩子現在哪個情緒小怪獸跑出來了？" + C_RESET)
    print(C_GRAY + "  （如果不太確定，選『綜合（全部）』也可以）" + C_RESET)
    print()

    options = list(EMOTIONS.items()) + [("all", {"name": "綜合（全部）", "monster": "全部小怪獸", "color": C_GRAY})]

    for i, (key, em) in enumerate(options, 1):
        print(f"  {C_GREEN}{i}.{C_RESET}  {key} {em['name']}")

    print()
    valid_nums = [str(i) for i in range(1, len(options) + 1)]
    num = ask(f"  選擇（1-{len(options)}）：")
    if num not in valid_nums:
        num = "1"

    idx = int(num) - 1
    choice_key = list(EMOTIONS.keys())[idx] if idx < len(EMOTIONS) else None

    coach_quick(choice_key)

    # Ask if user wants to save a log
    print(C_GRAY + "  按 Enter 回到主選單..." + C_RESET)
    try:
        input()
    except (EOFError, KeyboardInterrupt):
        pass


def coach_tts_script(emotion_key: str):
    """Generate TTS-ready short scripts for the child."""
    clear_screen()
    banner("🗣️ 情緒急救 TTS 短語（給孩子聽）", C_BOLD + C_PURPLE)

    if emotion_key not in EMOTIONS:
        print(C_GRAY + "  請先選擇一種情緒（見上方教練模式）" + C_RESET)
        return

    e = EMOTIONS[emotion_key]
    print()
    print(C_BOLD + C_YELLOW + f"  {emotion_key} {e['monster']} 的 TTS 短語：" + C_RESET)
    print()

    scripts = [
        f"我看到{e['name']}小怪獸跑出來了！",
        "生氣（難過/害怕）是正常的，我們陪它坐一坐。",
        "我們一起做三個大泡泡呼吸。",
        "用嘴巴說：我因為……很生氣（很難過）。",
        "現在可以怎麼做？我可以抱一抱我最喜歡的玩偶。",
    ]

    for s in scripts:
        print(C_GREEN + f"  🗣️ 「{s}」" + C_RESET)
        print()

    print(C_GRAY + "  💡 可直接用 TTS 朗讀給孩子聽，或由爸媽說給孩子聽。" + C_RESET)
    print()


def main():
    while True:
        clear_screen()
        print()
        print(C_BOLD + C_RED + " ╭─────────────────────────────────────────────╮" + C_RESET)
        print(C_BOLD + C_RED + " │  🩹 情緒急救箱  —  爸媽的隨身情緒教練       │" + C_RESET)
        print(C_BOLD + C_RED + " ╰─────────────────────────────────────────────╯" + C_RESET)
        print()
        print(C_BOLD + C_WHITE + "  請選擇模式：" + C_RESET)
        print()
        print(f"  {C_GREEN}1.{C_RESET}  ⚡ 快速教練（馬上用，按情緒分類）")
        print(f"  {C_GREEN}2.{C_RESET}  🩹 互動引導（一步一步帶著爸媽做）")
        print()
        print(f"  {C_GRAY}Q.{C_RESET}  離開")
        print()

        choice = ask("  選擇（1-2 或 Q）：")
        if choice in ("q", "Q"):
            clear_screen()
            print()
            print(C_BOLD + C_GREEN + "  🌟 情緒急救箱永遠在這裡！需要的時候再來 🩹" + C_RESET)
            print()
            break
        if choice == "1":
            # Show emotion picker
            clear_screen()
            banner("⚡ 快速教練：選擇情緒 ⚡", C_BOLD + C_YELLOW)
            print(C_BOLD + C_WHITE + "  哪個情緒小怪獸來了？" + C_RESET)
            print()
            for i, (key, em) in enumerate(EMOTIONS.items(), 1):
                print(f"  {C_GREEN}{i}.{C_RESET}  {key} {em['name']}")
            print()
            valid = [str(i) for i in range(1, len(EMOTIONS) + 1)]
            num = ask(f"  選擇（1-{len(EMOTIONS)} 或 Enter 跳過）：")
            key = None
            if num in valid:
                key = list(EMOTIONS.keys())[int(num) - 1]
            coach_quick(key)
            ask("  按 Enter 回到主選單：")
        elif choice == "2":
            coach_interactive()


if __name__ == "__main__":
    main()
