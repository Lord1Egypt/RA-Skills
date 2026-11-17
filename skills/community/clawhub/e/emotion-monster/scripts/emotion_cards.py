#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
情緒小怪獸 - 情緒卡片
Emotion Monster: Emotion Cards for Kids (Ages 2-6)
"""

import sys
import os

# ── ANSI colour constants ──────────────────────────────────────────────
C_RESET  = "\033[0m"
C_BOLD   = "\033[1m"
C_YELLOW = "\033[93m"
C_BLUE   = "\033[94m"
C_RED    = "\033[91m"
C_PURPLE = "\033[95m"
C_ORANGE = "\033[33m"
C_GRAY   = "\033[90m"
C_PINK   = "\033[35m"
C_GREEN  = "\033[92m"
C_WHITE  = "\033[97m"
C_BG_YEL = "\033[43m"
C_BG_BLU = "\033[44m"
C_BG_RED = "\033[41m"
C_BG_PUR = "\033[45m"
C_BG_ORA = "\033[48;5;208m"
C_BG_GRY = "\033[47m"
C_BG_PNK = "\033[48;5;218m"
C_BG_GRN = "\033[42m"

# ── Emotion card data ──────────────────────────────────────────────────
# ASCII art stored as \n-joined strings to avoid triple-quote conflicts.
EMOTIONS = [
    {
        "emoji": "😊",
        "name": "開心",
        "color": C_YELLOW,
        "bg": C_BG_YEL,
        "monster": "開心小怪獸",
        "ascii": (
            "    .- - - -.   \n"
            "   /        \\  \n"
            "  |  O    O  | \n"
            "  |    __    | \n"
            "   \\  \\__/  /  \n"
            "    '-.__.--'  "
        ),
        "desc": "太陽公公笑眯眯 🌞",
        "quote": "我好開心！今天是好日子！",
        "why": (
            "開心是因為事情很順利，或是有人對我很好，"
            "或是做了喜歡的事。開心小怪獸來了，太陽公公也開心！"
        ),
        "what_to_do": [
            "👉 大聲說：『我好開心！』",
            "👉 把開心的事告訴爸爸媽媽",
            "👉 給身邊的人一個大大的笑容 😊",
        ],
    },
    {
        "emoji": "😢",
        "name": "難過",
        "color": C_BLUE,
        "bg": C_BG_BLU,
        "monster": "難過小怪獸",
        "ascii": (
            "    .- - - -.   \n"
            "   /  .__.  \\  \n"
            "  |  ( oo )  | \n"
            "  |    __    | \n"
            "   \\  '-__'  /  \n"
            "    '-.__.--'  "
        ),
        "desc": "小雨滴滴答答下 💧",
        "quote": "我有一點點傷心……",
        "why": (
            "難過可能是因為心愛的東西不見了，或是有人讓你傷心，"
            "或是事情不如預期。小雨滴是天空在流眼淚，也是正常的。"
        ),
        "what_to_do": [
            "👉 可以輕輕抱一抱小熊或毯毯",
            "👉 試著說：『我因為……覺得難過』",
            "👉 哭一哭也沒關係，眼淚是身體在說話 💧",
        ],
    },
    {
        "emoji": "😠",
        "name": "生氣",
        "color": C_RED,
        "bg": C_BG_RED,
        "monster": "生氣小怪獸（最知名！）",
        "ascii": (
            "    .- - - -.   \n"
            "   /  >  <   \\  \n"
            "  |  /====\\  | \n"
            "  |  |^^^^|  | \n"
            "   \\  \\\\../  /  \n"
            "    '-.__.--'  \n"
            "  ~~火山噴發~~ "
        ),
        "desc": "小火山要爆發 🌋💥",
        "quote": "我好生氣！事情不對了！",
        "why": (
            "生氣是因為事情不像我們想要的那樣，"
            "或是有人踩到了我們的底線。火山累了，小怪獸也需要冷靜。"
        ),
        "what_to_do": [
            "👉 先停一下，深呼吸 3 次 🫧🫧🫧",
            "👉 大聲說：『我因為……好生氣！』",
            "👉 跺跺腳（但不要踢東西），把力氣用掉",
        ],
    },
    {
        "emoji": "😨",
        "name": "害怕",
        "color": C_PURPLE,
        "bg": C_BG_PUR,
        "monster": "害怕小怪獸",
        "ascii": (
            "    .- - - -.   \n"
            "   /  .--.   \\  \n"
            "  |  ( @  @ ) | \n"
            "  |    ??    | \n"
            "   \\  '-..-'  /  \n"
            "    '-.__.--'  "
        ),
        "desc": "大烏雲飄過來了 ☁️",
        "quote": "有點怕怕的……",
        "why": (
            "害怕是身體在保護我們，讓我們遠離危險。"
            "這是很正常的感覺，每個人都會害怕。"
        ),
        "what_to_do": [
            "👉 找大人抱一抱：『我害怕……』",
            "👉 慢慢靠近看看，原來沒有那麼可怕？",
            "👉 對自己說：『我長大了，我勇敢 💪』",
        ],
    },
    {
        "emoji": "😮",
        "name": "驚訝",
        "color": C_ORANGE,
        "bg": C_BG_ORA,
        "monster": "驚訝小怪獸",
        "ascii": (
            "    .- - - -.   \n"
            "   /  \\  /   \\  \n"
            "  |   O    O  | \n"
            "  |    (  )   | \n"
            "   \\   /==\\   /  \n"
            "    '-.__.--'  "
        ),
        "desc": "大嘴巴張得大大的 😲",
        "quote": "哇！好意外！",
        "why": (
            "驚訝是因為發生了意料之外的事，"
            "可能是好的，也可能是壞的。"
        ),
        "what_to_do": [
            "👉 好的驚訝 → 大聲說『哇！』開心一下 🎉",
            "👉 壞的驚訝 → 先深呼吸，冷靜想一想",
            "👉 有任何問題都可以問爸爸媽媽",
        ],
    },
    {
        "emoji": "😴",
        "name": "累了",
        "color": C_GRAY,
        "bg": C_BG_GRY,
        "monster": "愛睏小怪獸",
        "ascii": (
            "    .- - - -.   \n"
            "   /  -  -   \\  \n"
            "  |  ( u  u ) | \n"
            "  |    ----   | \n"
            "   \\  '-..-'  /  \n"
            "    '-.__.--'  \n"
            "      zzZZ "
        ),
        "desc": "小熊打哈欠 🐻💤",
        "quote": "好累喔……我想睡覺……",
        "why": (
            "累了是身體在說：『我要休息了！』"
            "可能是玩太久、沒睡飽，或是肚子餓了。"
        ),
        "what_to_do": [
            "👉 伸個大懶腰，試試看 🌟",
            "👉 喝點水，或是吃一點小點心",
            "👉 小睡一下，或躺在床上休息",
        ],
    },
    {
        "emoji": "🤗",
        "name": "舒服 / 滿足",
        "color": C_PINK,
        "bg": C_BG_PNK,
        "monster": "滿足小怪獸",
        "ascii": (
            "    .- - - -.   \n"
            "   /  \\__/   \\  \n"
            "  |  (^_^)   | \n"
            "  |    口     | \n"
            "   \\  '-..-'  /  \n"
            "    '-.__.--'  "
        ),
        "desc": "暖暖的抱抱 🤗",
        "quote": "我好舒服，好滿足 ☺️",
        "why": (
            "舒服是因為身體和心裡都很安心，"
            "被愛的感覺真好！"
        ),
        "what_to_do": [
            "👉 把這個感覺記在心裡 💗",
            "👉 跟喜歡的人說：『謝謝你，我很滿足』",
            "👉 享受這個moment，什麼都不用做 🌟",
        ],
    },
    {
        "emoji": "🤔",
        "name": "好奇",
        "color": C_GREEN,
        "bg": C_BG_GRN,
        "monster": "好奇小怪獸",
        "ascii": (
            "    .- - - -.   \n"
            "   /  ?  ?   \\  \n"
            "  |  ( oo )   | \n"
            "  |    \\/    | \n"
            "   \\  '-..-'  /  \n"
            "    '-.__.--'  \n"
            "     ??? ? "
        ),
        "desc": "問號蟲爬過來 🐛",
        "quote": "咦？這是什麼呢？",
        "why": (
            "好奇是因為我們想學習新東西！"
            "問問題是很棒的事情，好奇蟲蟲最愛問問題了。"
        ),
        "what_to_do": [
            "👉 大聲問出來：『為什麼？』👆",
            "👉 動手摸一摸、玩一玩、探索一下",
            "👉 試著自己找答案，你很聰明 🧠",
        ],
    },
]


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def render_card(emotion: dict, index: int, total: int):
    color  = emotion["color"]
    name   = emotion["name"]
    width  = 46

    print()
    print(color + f" ╭{'─' * (width - 2)}╮" + C_RESET)
    title  = f" {emotion['emoji']} {name}情緒小怪獸 "
    print(color + f" │{C_RESET}{C_BOLD}{C_WHITE}{title:<{width - 2}}│" + C_RESET)
    print(color + f" │{'─' * (width - 2)}│" + C_RESET)

    # ASCII art
    for line in emotion["ascii"].splitlines():
        print(color + f" │{C_RESET}  {C_BOLD}{line:<{width - 4}}│" + C_RESET)

    print(color + f" │{'─' * (width - 2)}│" + C_RESET)

    # Description
    desc_line = f"  {emotion['desc']}"
    print(color + f" │{C_RESET}{C_WHITE}{desc_line:<{width - 2}}│" + C_RESET)
    print(color + f" │{'─' * (width - 2)}│" + C_RESET)

    # Quote
    q = f"「{emotion['quote']}」"
    print(color + f" │{C_RESET}{C_YELLOW}{q:<{width - 2}}│" + C_RESET)
    print(color + f" │{'─' * (width - 2)}│" + C_RESET)

    # Why
    print(color + f" │{C_RESET}{C_BOLD}{C_WHITE}  🌱 為什麼會這樣？{' ' * (width - 18)}│" + C_RESET)
    chars = width - 4
    for chunk in _wrap(emotion["why"], chars):
        print(color + f" │{C_RESET}{C_WHITE}{chunk:<{width - 2}}│" + C_RESET)
    print(color + f" │{'─' * (width - 2)}│" + C_RESET)

    # What to do
    print(color + f" │{C_RESET}{C_BOLD}{C_WHITE}  🌟 我可以怎麼做？{' ' * (width - 18)}│" + C_RESET)
    for tip in emotion["what_to_do"]:
        for chunk in _wrap(tip, chars):
            print(color + f" │{C_RESET}{C_WHITE}{chunk:<{width - 2}}│" + C_RESET)
    print(color + f" │{'─' * (width - 2)}│" + C_RESET)

    footer = f"  卡片 {index}/{total}  ·  ◀ ▶ 換卡  ·  Q 離開"
    print(color + f" │{C_RESET}{C_GRAY}{footer:<{width - 2}}│" + C_RESET)
    print(color + f" ╰{'─' * (width - 2)}╯" + C_RESET)
    print()


def _wrap(text: str, width: int) -> list:
    """Simple word-wrap returning a list of lines."""
    lines = []
    for paragraph in text.splitlines():
        paragraph = paragraph.strip()
        while len(paragraph) > width:
            lines.append(paragraph[:width])
            paragraph = "  " + paragraph[width:]
        if paragraph:
            lines.append(paragraph)
    return lines


def show_intro():
    clear_screen()
    print()
    print(C_BOLD + C_PURPLE + " ╭────────────────────────────────────────╮" + C_RESET)
    print(C_BOLD + C_PURPLE + " │                                        │" + C_RESET)
    print(C_BOLD + C_PURPLE + " │   🦋 情緒小怪獸來了！                 │" + C_RESET)
    print(C_BOLD + C_PURPLE + " │                                        │" + C_RESET)
    print(C_BOLD + C_PURPLE + " │   嗨！我是情緒小怪獸 🦋                 │" + C_RESET)
    print(C_BOLD + C_PURPLE + " │   我有 8 個好朋友，                    │" + C_RESET)
    print(C_BOLD + C_PURPLE + " │   每個都代表一種情緒。                 │" + C_RESET)
    print(C_BOLD + C_PURPLE + " │                                        │" + C_RESET)
    print(C_BOLD + C_PURPLE + " │   🌱 情緒不是壞東西，                   │" + C_RESET)
    print(C_BOLD + C_PURPLE + " │   認識它們，就不會害怕了！              │" + C_RESET)
    print(C_BOLD + C_PURPLE + " │                                        │" + C_RESET)
    print(C_BOLD + C_PURPLE + " ╰────────────────────────────────────────╯" + C_RESET)
    print()
    print(C_BOLD + C_WHITE + "   按 " + C_YELLOW + "Enter" + C_WHITE + " 開始認識 8 種情緒小怪獸 " + C_BOLD + " →" + C_RESET)
    print()


def main():
    show_intro()
    try:
        input()
    except (EOFError, KeyboardInterrupt):
        print("\n下次再見囉！👋")
        return

    clear_screen()
    index = 0

    while True:
        render_card(EMOTIONS[index], index + 1, len(EMOTIONS))

        print(C_BOLD + C_WHITE + "  你現在像哪個小怪獸？ " + C_RESET, end="")
        print(C_GRAY + "(◀ ▶ 換卡  /  Q 離開)" + C_RESET)
        try:
            key = input("  > ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\n" + C_BOLD + C_GREEN + "  🌟 下次再見！情緒小怪獸永遠陪著你！🦋" + C_RESET)
            break

        if key in ("q", "quit", "exit"):
            print()
            print(C_BOLD + C_GREEN + "  🌟 下次再見！情緒小怪獸永遠陪著你！🦋" + C_RESET)
            break
        elif key in ("右", "→", "d", "l", "6", "arrowright"):
            index = (index + 1) % len(EMOTIONS)
        elif key in ("左", "◀", "←", "a", "h", "4", "arrowleft"):
            index = (index - 1) % len(EMOTIONS)
        else:
            print(C_GRAY + "  試試看 ◀ 或 ▶ 來換卡片哦！" + C_RESET)

        clear_screen()


if __name__ == "__main__":
    main()
