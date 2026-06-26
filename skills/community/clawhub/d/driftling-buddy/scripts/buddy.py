#!/usr/bin/env python3
import argparse
import json
import os
import random
import sys
import textwrap
import unicodedata
from pathlib import Path

from theme_data import THEMES

CARD_WIDTH = 33
STAT_ORDER = ["focus", "curiosity", "warmth", "mischief", "rarity"]
STARTER_THEMES = ["general", "coffee", "study", "sleep", "tea", "library"]
STARTER_NAMES = [
    "Mori", "Nilo", "Sumi", "Aru", "Tavi", "Lio", "Mika", "Rune",
    "Koto", "Yumi", "Haku", "Lumi", "Pico", "Zuri", "Olm", "Dew",
    "Fenn", "Cleo", "Juno", "Obi", "Pip", "Sol", "Rue", "Wren",
    "Kai", "Elm", "Ori", "Tao", "Ivy", "Lark", "Moss", "Brin",
]
RARITY_LEVELS = {
    "common": {
        "threshold": 0,
        "stars": 1,
        "frame": ("╭", "─", "╮", "│", "│", "╰", "─", "╯"),
        "en": "Common",
        "zh": "普通",
    },
    "uncommon": {
        "threshold": 35,
        "stars": 2,
        "frame": ("┌", "─", "┐", "│", "│", "└", "─", "┘"),
        "en": "Uncommon",
        "zh": "少见",
    },
    "rare": {
        "threshold": 55,
        "stars": 3,
        "frame": ("╔", "═", "╗", "║", "║", "╚", "═", "╝"),
        "en": "Rare",
        "zh": "稀有",
    },
    "epic": {
        "threshold": 72,
        "stars": 4,
        "frame": ("╭", "═", "╮", "║", "║", "╰", "═", "╯"),
        "en": "Epic",
        "zh": "奇异",
    },
    "mythic": {
        "threshold": 88,
        "stars": 5,
        "frame": ("┏", "━", "┓", "┃", "┃", "┗", "━", "┛"),
        "en": "Mythic",
        "zh": "传闻",
    },
}
STAT_LABELS = {
    "en": {
        "focus": "Focus",
        "curiosity": "Curiosity",
        "warmth": "Warmth",
        "mischief": "Mischief",
        "rarity": "Rarity",
    },
    "zh": {
        "focus": "专注",
        "curiosity": "好奇",
        "warmth": "温度",
        "mischief": "顽皮",
        "rarity": "稀有",
    },
}
FILLED_CHIP = "▓"
EMPTY_CHIP = "░"
STAR_ICON = "★"
STATE_FILE = Path(os.environ.get("BUDDY_STATE_FILE", Path.home() / ".buddy_mode_state.json"))
ANSI_RESET = "\033[0m"
WARM_YELLOW = "\033[38;5;221m"
UI_TEXT = {
    "en": {
        "task": "> task:",
        "next": "> next:",
        "watch": "> watch:",
        "side": "> side:",
        "how_to_get": "how to get more",
        "first_buddy": "first buddy",
        "buddy_ready": "buddy ready",
        "trigger": "trigger",
        "main_buddy": "main buddy",
        "summoned": "summoned",
        "unlocked": "unlocked",
        "why_now": "why now",
        "collection": "collection",
        "help": "help",
        "auto_saved": "auto-saved to collection",
        "debug": "debug",
        "total": "total",
        "active": "active",
        "none_yet": "no buddies yet",
        "pool": "pool",
        "species": "species",
        "unlock_via": "unlock via",
        "hint": "hint",
        "name_hint": "name hint",
        "obsession": "obsession",
        "rule": "rule",
        "story": "story",
        "rarity": "rarity",
        "stars": "stars",
        "pool_names": {
            "reference pool": "reference pool",
            "ember pool": "ember pool",
            "studio pool": "studio pool",
            "coffee pool": "coffee pool",
            "house pool": "house pool",
            "study pool": "study pool",
            "sleep pool": "sleep pool",
            "weather pool": "weather pool",
            "travel pool": "travel pool",
            "music pool": "music pool",
            "kitchen pool": "kitchen pool",
            "library pool": "library pool",
            "garden pool": "garden pool",
            "mail pool": "mail pool",
            "clock pool": "clock pool",
            "errands pool": "errands pool",
            "market pool": "market pool",
            "tea pool": "tea pool",
            "winter pool": "winter pool",
            "fitness pool": "fitness pool",
            "photo pool": "photo pool",
            "craft pool": "craft pool",
            "language pool": "language pool",
            "laundry pool": "laundry pool",
            "stargazing pool": "stargazing pool",
            "pond pool": "pond pool",
            "chill pool": "chill pool",
            "stationery pool": "stationery pool",
            "queue pool": "queue pool",
            "nap pool": "nap pool",
            "morning pool": "morning pool",
        },
        "phase": {
            "alignment": "alignment",
            "research": "research",
            "planning": "planning",
            "implementation": "implementation",
            "testing": "testing",
            "blocked": "blocked",
            "complete": "complete",
        },
        "mood": {
            "curious": "curious",
            "focused": "focused",
            "steady": "steady",
            "concerned": "concerned",
            "celebrating": "celebrating",
        },
    },
    "zh": {
        "task": "> 任务:",
        "next": "> 下一步:",
        "watch": "> 注意:",
        "side": "> 小动作:",
        "how_to_get": "后续获取",
        "first_buddy": "第一只",
        "buddy_ready": "buddy 已就位",
        "trigger": "触发方式",
        "main_buddy": "主 buddy",
        "summoned": "已召唤",
        "unlocked": "已获得",
        "why_now": "出现原因",
        "collection": "图鉴",
        "help": "帮助",
        "auto_saved": "已自动加入图鉴",
        "debug": "调试",
        "total": "总数",
        "active": "当前主 buddy",
        "none_yet": "还没有获得 buddy",
        "pool": "池子",
        "species": "物种",
        "unlock_via": "解锁方式",
        "hint": "提示",
        "name_hint": "名字提示",
        "obsession": "执念",
        "rule": "规矩",
        "story": "来历",
        "rarity": "稀有度",
        "stars": "星级",
        "pool_names": {
            "reference pool": "文献池",
            "ember pool": "余烬池",
            "studio pool": "设计池",
            "coffee pool": "咖啡池",
            "house pool": "家务池",
            "study pool": "学习池",
            "sleep pool": "睡眠池",
            "weather pool": "天气池",
            "travel pool": "旅行池",
            "music pool": "音乐池",
            "kitchen pool": "厨房池",
            "library pool": "书架池",
            "garden pool": "花园池",
            "mail pool": "信件池",
            "clock pool": "时钟池",
            "errands pool": "跑腿池",
            "market pool": "集市池",
            "tea pool": "茶歇池",
            "winter pool": "冬日池",
            "fitness pool": "运动池",
            "photo pool": "影像池",
            "craft pool": "手作池",
            "language pool": "语言池",
            "laundry pool": "洗衣池",
            "stargazing pool": "观星池",
            "pond pool": "池塘池",
            "chill pool": "悠闲池",
            "stationery pool": "文具池",
            "queue pool": "排队池",
            "nap pool": "打盹池",
            "morning pool": "早起池",
        },
        "phase": {
            "alignment": "对齐",
            "research": "调研",
            "planning": "规划",
            "implementation": "实现",
            "testing": "验证",
            "blocked": "受阻",
            "complete": "完成",
        },
        "mood": {
            "curious": "好奇",
            "focused": "专注",
            "steady": "稳定",
            "concerned": "警觉",
            "celebrating": "雀跃",
        },
    },
}


VALID_PHASES = {
    "alignment",
    "research",
    "planning",
    "implementation",
    "testing",
    "blocked",
    "complete",
}


VALID_MOODS = {
    "curious",
    "focused",
    "steady",
    "concerned",
    "celebrating",
}

def pick_theme(theme: str) -> dict:
    if theme in THEMES:
        return THEMES[theme]
    state = load_state()
    if theme in state.get("custom_pools", {}):
        return state["custom_pools"][theme]
    return THEMES["general"]


def vary_profile(profile: dict) -> dict:
    """Return a shallow copy with randomized stats (+-15 per stat)."""
    varied = dict(profile)
    original_stats = profile["stats"]
    varied["stats"] = {
        key: max(0, min(100, val + random.randint(-15, 15)))
        for key, val in original_stats.items()
    }
    return varied


def pick_lang(lang: str) -> str:
    if lang == "mixed":
        return "zh"
    if lang in UI_TEXT:
        return lang
    return "en"


def rarity_key_for_score(score: int, luck: bool = True) -> str:
    """Convert a base rarity score to a rarity tier.

    When luck=True (default), a random roll of -20 to +30 is added to the
    base score before mapping to tiers.  This means a base-50 buddy is
    usually Uncommon but can occasionally land on Rare, Epic, or even Mythic.
    """
    if luck:
        score = score + random.randint(-20, 30)
    score = max(0, min(100, score))
    chosen = "common"
    for key, config in RARITY_LEVELS.items():
        if score >= config["threshold"]:
            chosen = key
    return chosen


def rarity_meta(key: str, lang: str) -> dict:
    lang = pick_lang(lang)
    meta = RARITY_LEVELS.get(key, RARITY_LEVELS["common"]).copy()
    meta["label"] = meta[lang]
    return meta


def localized_pool_name(pool_name: str, lang: str) -> str:
    lang = pick_lang(lang)
    return UI_TEXT[lang]["pool_names"].get(pool_name, pool_name)


def descriptor_line(profile: dict, lang: str) -> str:
    lang = pick_lang(lang)
    if lang == "zh":
        return profile["side_zh"][0]
    return profile["side_en"][0]


def load_state() -> dict:
    default = {"unlocked": [], "main": None, "custom_pools": {}}
    if not STATE_FILE.exists():
        return default
    try:
        state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
        state.setdefault("custom_pools", {})
        return state
    except (json.JSONDecodeError, OSError):
        return default


def save_state(state: dict) -> None:
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def add_to_collection(theme: str, name: str, custom_profile=None, context: str = "") -> dict:
    state = load_state()
    entry: dict = {"theme": theme, "name": name}
    if custom_profile:
        entry["custom"] = True
        if theme not in state["custom_pools"]:
            state["custom_pools"][theme] = custom_profile
    if context:
        entry["obtained_context"] = context
    # Check by theme+name to avoid exact-dict mismatch on extra fields
    existing = [e for e in state["unlocked"] if e.get("theme") == theme and e.get("name") == name]
    if not existing:
        entry["times_shown"] = 0
        state["unlocked"].append(entry)
    save_state(state)
    return state


def find_buddy(theme: str, name: str) -> dict:
    """Find a specific buddy entry in the state, or return empty dict."""
    state = load_state()
    for entry in state["unlocked"]:
        if entry.get("theme") == theme and entry.get("name") == name:
            return entry
    return {}


def bump_shown(theme: str, name: str) -> dict:
    """Increment times_shown for a buddy and return updated entry."""
    state = load_state()
    for entry in state["unlocked"]:
        if entry.get("theme") == theme and entry.get("name") == name:
            entry["times_shown"] = entry.get("times_shown", 0) + 1
            save_state(state)
            return entry
    return {}


def choose_starter_theme(theme: str) -> str:
    if theme and theme != "auto":
        return theme
    return random.choice(STARTER_THEMES)


def choose_buddy_name(name: str) -> str:
    if name and name != "auto":
        return name
    state = load_state()
    used = {e.get("name") for e in state.get("unlocked", [])}
    available = [n for n in STARTER_NAMES if n not in used]
    if not available:
        available = STARTER_NAMES
    return random.choice(available)


def set_main_buddy(theme: str, name: str) -> dict:
    state = add_to_collection(theme, name)
    state["main"] = {"theme": theme, "name": name}
    save_state(state)
    return state


def clamp(text: str, width: int) -> str:
    text = " ".join(text.split())
    if display_width(text) <= width:
        return text
    return truncate_display(text, width, "...")


def pad_line(text: str) -> str:
    inner_width = CARD_WIDTH - 2
    wrapped = wrap_display(text, inner_width)
    return "\n".join(f"│ {line}" for line in wrapped)


def frame_parts(rarity: dict) -> tuple[str, str, str, str, str, str, str, str]:
    return rarity["frame"]


def make_border(rarity: dict, top: bool, title: str = "") -> str:
    left, horizontal, _, _, _, bottom_left, bottom_horizontal, _ = frame_parts(rarity)
    if top and title:
        prefix = left + horizontal + " " + title + " "
        fill = max(0, CARD_WIDTH - display_width(prefix))
        return prefix + (horizontal * fill)
    if top:
        return left + (horizontal * (CARD_WIDTH - 1))
    return bottom_left + (bottom_horizontal * (CARD_WIDTH - 1))


def make_plain_border(top: bool, title: str = "") -> str:
    if top and title:
        prefix = "╭─ " + title + " "
        fill = max(0, CARD_WIDTH - display_width(prefix))
        return prefix + ("─" * fill)
    if top:
        return "╭" + ("─" * (CARD_WIDTH - 1))
    return "╰" + ("─" * (CARD_WIDTH - 1))


def framed_line(text: str, rarity: dict) -> str:
    _, _, _, side_left, _, _, _, _ = frame_parts(rarity)
    return f"{side_left} {text}"


def framed_lines(text: str, rarity: dict) -> list[str]:
    _, _, _, side_left, _, _, _, _ = frame_parts(rarity)
    inner_width = CARD_WIDTH - display_width(side_left) - 1
    wrapped = wrap_display(text, inner_width)
    return [f"{side_left} {line}" for line in wrapped]


def make_bar(value: int) -> str:
    score = max(0, min(100, value))
    chips = min(5, max(0, round(score / 20)))
    return FILLED_CHIP * chips + EMPTY_CHIP * (5 - chips)


def apply_growth(stats: dict, growth: dict) -> dict:
    """Apply stat_growth on top of base stats, capped at +30."""
    result = {}
    for key, val in stats.items():
        delta = min(30, max(0, int(growth.get(key, 0))))
        result[key] = max(0, min(100, val + delta))
    return result


def stats_lines(stats: dict, lang: str, growth=None) -> list[str]:
    if growth:
        stats = apply_growth(stats, growth)
    parts = []
    labels = STAT_LABELS[lang]
    label_width = max(len(label) for label in labels.values())
    for key in STAT_ORDER:
        value = int(stats.get(key, 50))
        delta = int((growth or {}).get(key, 0))
        label = labels[key].ljust(label_width)
        suffix = f" +{delta}" if delta > 0 else ""
        parts.append(f"{label} {make_bar(value)} {value:>3}{suffix}")
    return parts


def box_line(text: str) -> str:
    return pad_line(text)


def char_width(char: str) -> int:
    if unicodedata.combining(char):
        return 0
    if unicodedata.east_asian_width(char) in {"W", "F"}:
        return 2
    return 1


def display_width(text: str) -> int:
    return sum(char_width(char) for char in text)


def truncate_display(text: str, width: int, placeholder: str = "...") -> str:
    if width <= 0:
        return ""
    if display_width(text) <= width:
        return text
    placeholder_width = display_width(placeholder)
    available = max(0, width - placeholder_width)
    pieces = []
    used = 0
    for char in text:
        char_w = char_width(char)
        if used + char_w > available:
            break
        pieces.append(char)
        used += char_w
    return "".join(pieces).rstrip() + placeholder


def pad_display(text: str, width: int) -> str:
    clipped = truncate_display(text, width, "")
    padding = max(0, width - display_width(clipped))
    return clipped + (" " * padding)


def wrap_display(text: str, width: int) -> list[str]:
    if width <= 0:
        return [""]
    if display_width(text) <= width:
        return [text]
    lines: list[str] = []
    current: list[str] = []
    current_width = 0
    for char in text:
        cw = char_width(char)
        if current_width + cw > width:
            lines.append("".join(current))
            current = [] if char == " " else [char]
            current_width = 0 if char == " " else cw
        else:
            current.append(char)
            current_width += cw
    if current:
        lines.append("".join(current))
    return lines if lines else [""]


def center_display(text: str, width: int) -> str:
    clipped = truncate_display(text, width, "")
    remaining = max(0, width - display_width(clipped))
    left = remaining // 2
    right = remaining - left
    return (" " * left) + clipped + (" " * right)


def color_enabled(mode: str) -> bool:
    if mode == "always":
        return True
    if mode == "never":
        return False
    if os.environ.get("NO_COLOR"):
        return False
    term = os.environ.get("TERM", "")
    return sys.stdout.isatty() and term and term != "dumb"


def paint(text: str, color: str, enabled: bool) -> str:
    if not enabled:
        return text
    return f"{color}{text}{ANSI_RESET}"


def pick_hints(profile: dict, lang: str) -> list[str]:
    key = f"hints_{lang}"
    return profile.get(key, profile.get("hints_en", []))


def pick_unlock_examples(profile: dict, lang: str) -> list[str]:
    key = f"unlock_examples_{lang}"
    return profile.get(key, profile.get("unlock_examples_en", []))


def pool_summary(theme: str, lang: str) -> str:
    profile = pick_theme(theme)
    lang = pick_lang(lang)
    ui = UI_TEXT[lang]
    rarity = rarity_meta(rarity_key_for_score(profile["stats"]["rarity"]), lang)
    examples = ", ".join(pick_unlock_examples(profile, lang)[:3])
    hint = random.choice(pick_hints(profile, lang))
    shape = profile["shape"]
    title = f"{rarity['label']} {STAR_ICON * rarity['stars']}"
    top = make_border(rarity, top=True, title=title)
    bottom = make_border(rarity, top=False)
    lines = [
        *shape,
        f"{ui['pool']}: {localized_pool_name(profile['pool'], lang)}",
        f"{ui['species']}: {profile['species']}",
        f"{ui['unlock_via']}: {examples}",
        f"{ui['hint']}: {hint}",
    ]
    framed = []
    for line in lines:
        framed.extend(framed_lines(line, rarity))
    return "\n".join([top, *framed, bottom])


def init_summary(theme: str, lang: str, name: str) -> str:
    theme = choose_starter_theme(theme)
    name = choose_buddy_name(name)
    add_to_collection(theme, name)
    profile = vary_profile(pick_theme(theme))
    lang = pick_lang(lang)
    ui = UI_TEXT[lang]
    rolled_rarity = rarity_key_for_score(profile["stats"]["rarity"])
    rarity = rarity_meta(rolled_rarity, lang)

    buddy_card = render_block(
        phase="alignment",
        mood="curious",
        task="你刚获得了第一只 buddy",
        next_step="看看它来自哪个池子",
        risk="先熟悉它，再去碰运气开新池",
        theme=theme,
        species=profile["species"],
        name=name,
        lang=lang,
        rarity=rolled_rarity,
        side_quest=random.choice(profile["side_zh"] if lang == "zh" else profile["side_en"]),
    )

    info_title = ui['buddy_ready']
    top_border = make_border(rarity, top=True, title=info_title)
    bottom_border = make_border(rarity, top=False)
    if lang == "zh":
        lines = [
            f"{ui['first_buddy']}: {name} | {profile['species']}",
            f"{ui['pool']}: {localized_pool_name(profile['pool'], lang)}",
            f"{rarity['label']} {STAR_ICON * rarity['stars']}",
            f"{ui['trigger']}: /buddy",
            f"{ui['how_to_get']}: 提醒、检索、整理、计划、复盘都可能开新池",
            '提示: 你也可以直接问"怎么获得新的 buddy？"',
        ]
    else:
        lines = [
            f"{ui['first_buddy']}: {name} | {profile['species']}",
            f"{ui['pool']}: {localized_pool_name(profile['pool'], lang)}",
            f"{rarity['label']} {STAR_ICON * rarity['stars']}",
            f"{ui['trigger']}: /buddy",
            f"{ui['how_to_get']}: reminders, search, cleanup, planning, and check-ins can open more pools",
            'Hint: you can also ask “how do I unlock more buddies?”',
        ]
    info_framed = []
    for line in lines:
        info_framed.extend(framed_lines(line, rarity))
    info_card = "\n".join([top_border, *info_framed, bottom_border])
    return f"{buddy_card}\n{info_card}"


def summon_summary(theme: str, lang: str, name: str, main: bool) -> str:
    name = choose_buddy_name(name)
    lang = pick_lang(lang)
    profile = pick_theme(theme)
    ui = UI_TEXT[lang]
    if lang == "zh":
        task = "和你的 buddy 打个招呼"
        next_step = "问问它最近在忙什么"
        risk = "别一次叫出太多只，留点惊喜"
        side_quest = random.choice(profile["side_zh"])
    else:
        task = "check in with your buddy"
        next_step = "ask what it has been busy with"
        risk = "do not summon too many at once"
        side_quest = random.choice(profile["side_en"])
    card = render_block(
        phase="alignment",
        mood="curious",
        task=task,
        next_step=next_step,
        risk=risk,
        theme=theme,
        species=profile["species"],
        name=name,
        lang=lang,
        rarity="",
        side_quest=side_quest,
    )
    if main:
        set_main_buddy(theme, name)
        rarity = rarity_meta(rarity_key_for_score(profile["stats"]["rarity"]), lang)
        top_border = make_border(rarity, top=True, title=ui['summoned'])
        bottom_border = make_border(rarity, top=False)
        lines = [
            f"{ui['main_buddy']}: {name} | {profile['species']}",
        ]
        info_framed = []
        for line in lines:
            info_framed.extend(framed_lines(line, rarity))
        info_card = "\n".join([top_border, *info_framed, bottom_border])
        return f"{card}\n{info_card}"
    return card


def unlock_summary(theme: str, lang: str, name: str, reason: str) -> str:
    name = choose_buddy_name(name)
    add_to_collection(theme, name)
    lang = pick_lang(lang)
    profile = pick_theme(theme)
    ui = UI_TEXT[lang]
    if lang == "zh":
        task = "你刚获得了一只新的 buddy"
        next_step = "看看它适合在哪些时刻出现"
        risk = "别急着全都设成主 buddy"
        side_quest = random.choice(profile["side_zh"])
        default_reason = f"你刚才的动作碰到了{localized_pool_name(profile['pool'], lang)}"
    else:
        task = "you just unlocked a new buddy"
        next_step = "see when it likes to appear"
        risk = "do not set every buddy as main at once"
        side_quest = random.choice(profile["side_en"])
        default_reason = f"your recent action brushed against the {localized_pool_name(profile['pool'], lang)}"
    card = render_block(
        phase="complete",
        mood="celebrating",
        task=task,
        next_step=next_step,
        risk=risk,
        theme=theme,
        species=profile["species"],
        name=name,
        lang=lang,
        rarity="",
        side_quest=side_quest,
    )
    rarity = rarity_meta(rarity_key_for_score(profile["stats"]["rarity"]), lang)
    info_title = f"{ui['debug']} {ui['unlocked']}"
    top_border = make_border(rarity, top=True, title=info_title)
    bottom_border = make_border(rarity, top=False)
    lines = [
        f"{name} | {profile['species']}",
        f"{ui['pool']}: {localized_pool_name(profile['pool'], lang)}",
        f"{ui['auto_saved']}",
        f"{ui['why_now']}: {reason or default_reason}",
    ]
    info_framed = []
    for line in lines:
        info_framed.extend(framed_lines(line, rarity))
    info_card = "\n".join([top_border, *info_framed, bottom_border])
    return f"{card}\n{info_card}"


def collection_summary(lang: str, color_mode: str) -> str:
    lang = pick_lang(lang)
    ui = UI_TEXT[lang]
    state = load_state()
    unlocked = state.get("unlocked", [])
    main = state.get("main")
    use_color = color_enabled(color_mode)
    collection_title = f"✨ {ui['collection']} ✨"
    border = make_plain_border(top=True, title=collection_title)
    bottom = make_plain_border(top=False)
    lines = [f"{ui['total']}: {len(unlocked)}"]
    if main:
        main_profile = pick_theme(main["theme"])
        lines.append(f"{ui['active']}: {main['name']} | {main_profile['species']}")
    else:
        lines.append(f"{ui['active']}: -")
    if not unlocked:
        lines.append(ui["none_yet"])
    else:
        for entry in unlocked:
            profile = pick_theme(entry["theme"])
            rarity = rarity_meta(rarity_key_for_score(profile["stats"]["rarity"], luck=False), lang)
            line = f"{STAR_ICON * rarity['stars']} {entry['name']} | {profile['species']}"
            lines.append(line)
            memo = entry.get("obtained_context") or entry.get("memorable")
            if memo:
                lines.append(f'  "{memo}"')
    rendered_lines = [paint(border, WARM_YELLOW, use_color)]
    for line in lines:
        rendered_lines.append(box_line(line))
    rendered_lines.append(paint(bottom, WARM_YELLOW, use_color))
    return "\n".join(rendered_lines)


def inspect_summary(theme: str, name: str, lang: str) -> str:
    entry = find_buddy(theme, name)
    if not entry:
        return f"buddy not found: {name} ({theme})"
    bump_shown(theme, name)
    profile = pick_theme(theme)
    lang = pick_lang(lang)
    growth = entry.get("stat_growth", {})
    stats = profile["stats"]
    rolled_rarity = rarity_key_for_score(stats["rarity"], luck=False)
    rarity = rarity_meta(rolled_rarity, lang)
    title = f"{rarity['label']} {STAR_ICON * rarity['stars']}"
    top_border = make_border(rarity, top=True, title=title)
    bottom_border = make_border(rarity, top=False)
    times = entry.get("times_shown", 0)
    context = entry.get("obtained_context", "")
    memorable = entry.get("memorable", "")
    content = [
        *profile["shape"],
        f"{name} | {profile['species']}",
        descriptor_line(profile, lang),
    ]
    content.extend(stats_lines(stats, lang, growth))
    if context:
        if lang == "zh":
            content.append(f"> 初遇: {context}")
        else:
            content.append(f"> met: {context}")
    if memorable:
        if lang == "zh":
            content.append(f"> 记忆: {memorable}")
        else:
            content.append(f"> memo: {memorable}")
    if lang == "zh":
        content.append(f"> 出场: {times} 次")
    else:
        content.append(f"> shown: {times} times")
    boxed = [top_border]
    for line in content:
        boxed.extend(framed_lines(line, rarity))
    boxed.append(bottom_border)
    return "\n".join(boxed)


def help_summary(lang: str) -> str:
    lang = pick_lang(lang)
    help_title = "✨ /buddy-help ✨"
    border = make_plain_border(top=True, title=help_title)
    bottom = make_plain_border(top=False)
    if lang == "zh":
        lines = [
            "/buddy  领取第一只",
            "/collection  查看图鉴",
            "/inspect  查看某只详情",
            "/summon  召唤 buddy",
            "/pool  查看池子提示",
            "新 buddy 自动加入图鉴",
        ]
    else:
        lines = [
            "/buddy  get your first",
            "/collection  view all",
            "/inspect  view one buddy",
            "/summon  call one back",
            "/pool  inspect a pool",
            "auto-saved to collection",
        ]
    return "\n".join([border, *(box_line(line) for line in lines), bottom])


def normalize_slash_command(argv: list[str]) -> list[str]:
    if len(argv) < 2:
        return argv
    aliases = {
        "/buddy": "init",
        "/init": "init",
        "/unlock": "unlock",
        "/summon": "summon",
        "/pool": "pool",
        "/collection": "collection",
        "/buddy-help": "help",
        "/inspect": "inspect",
    }
    cmd = aliases.get(argv[1])
    if cmd:
        return [argv[0], cmd, *argv[2:]]
    return argv


def render_block(
    phase: str,
    mood: str,
    task: str,
    next_step: str,
    risk: str,
    theme: str,
    species: str,
    name: str,
    lang: str,
    rarity: str,
    side_quest: str,
) -> str:
    name = choose_buddy_name(name)
    phase = phase.lower()
    mood = mood.lower()
    if phase not in VALID_PHASES:
        raise SystemExit(f"invalid phase: {phase}")
    if mood not in VALID_MOODS:
        raise SystemExit(f"invalid mood: {mood}")
    profile = pick_theme(theme)
    lang = pick_lang(lang)
    ui = UI_TEXT[lang]
    shape = profile["shape"]
    stats = profile["stats"]
    rarity_score = int(stats.get("rarity", 50))
    rarity = rarity or rarity_key_for_score(rarity_score)
    rarity_info = rarity_meta(rarity, lang)
    if not species:
        species = profile["species"]
    title = f"{rarity_info['label']} {STAR_ICON * rarity_info['stars']}"
    content = [
        *shape,
        f"{name} | {species}",
        descriptor_line(profile, lang),
        f"{ui['mood'][mood]} | {ui['phase'][phase]} | {localized_pool_name(profile['pool'], lang)}",
        *stats_lines(stats, lang),
        f"{ui['task']} {task}",
        f"{ui['next']} {next_step}",
        f"{ui['watch']} {risk}",
    ]
    if side_quest:
        content.append(f"{ui['side']} {side_quest}")
    top_border = make_border(rarity_info, top=True, title=title)
    bottom_border = make_border(rarity_info, top=False)
    boxed = [top_border]
    for line in content:
        boxed.extend(framed_lines(line, rarity_info))
    boxed.append(bottom_border)
    return "\n".join(boxed)


def hatch(theme: str, lang: str) -> str:
    profile = pick_theme(theme)
    lang = pick_lang(lang)
    ui = UI_TEXT[lang]
    species = profile["species"]
    stats = profile["stats"]
    obsession = random.choice(profile["obsessions"])
    rule = random.choice(profile["rules"])
    story = random.choice(profile["stories"])
    return "\n".join(
        [
            f"{ui['species']}: {species}",
            f"{ui['pool']}: {localized_pool_name(profile['pool'], lang)}",
            f"{ui['name_hint']}: {random.choice(['Mori', 'Nilo', 'Sumi', 'Aru'])}",
            f"{ui['rarity']}: {rarity_meta(rarity_key_for_score(stats['rarity']), lang)['label']}",
            f"{ui['stars']}: {STAR_ICON * rarity_meta(rarity_key_for_score(stats['rarity']), lang)['stars']}",
            *[
                f"{STAT_LABELS[lang][key]}: {value}/100"
                for key, value in stats.items()
            ],
            f"{ui['obsession']}: {obsession}",
            f"{ui['rule']}: {rule}",
            f"{ui['story']}: {story}",
        ]
    )


def random_side_quest(theme: str, lang: str) -> str:
    profile = pick_theme(theme)
    if lang == "zh":
        return random.choice(profile["side_zh"])
    if lang == "mixed":
        options = profile["side_zh"] + profile["side_en"]
        return random.choice(options)
    return random.choice(profile["side_en"])


def main() -> None:
    sys.argv = normalize_slash_command(sys.argv)
    parser = argparse.ArgumentParser(description="Render a compact coding buddy block.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    render = subparsers.add_parser("render", help="render a buddy block")
    render.add_argument("--phase", required=True)
    render.add_argument("--mood", required=True)
    render.add_argument("--task", required=True)
    render.add_argument("--next", dest="next_step", required=True)
    render.add_argument("--risk", required=True)
    render.add_argument("--theme", default="general")
    render.add_argument("--species", default="")
    render.add_argument("--name", default="auto")
    render.add_argument("--lang", default="en", choices=["zh", "en", "mixed"])
    render.add_argument("--rarity", default="", choices=["", *RARITY_LEVELS.keys()])
    render.add_argument("--side-quest", default="")

    hatch_parser = subparsers.add_parser("hatch", help="generate a lightweight buddy profile")
    hatch_parser.add_argument("--theme", default="general")
    hatch_parser.add_argument("--lang", default="en", choices=["zh", "en", "mixed"])

    side_parser = subparsers.add_parser("sidequest", help="generate a side quest line")
    side_parser.add_argument("--theme", default="general")
    side_parser.add_argument("--lang", default="en", choices=["zh", "en", "mixed"])

    pool_parser = subparsers.add_parser("pool", help="render a themed unlock pool summary")
    pool_parser.add_argument("--theme", default="general")
    pool_parser.add_argument("--lang", default="en", choices=["zh", "en", "mixed"])

    init_parser = subparsers.add_parser("init", help="initialize the first buddy and show onboarding")
    init_parser.add_argument("--theme", default="auto")
    init_parser.add_argument("--lang", default="en", choices=["zh", "en", "mixed"])
    init_parser.add_argument("--name", default="auto")

    register_parser = subparsers.add_parser("register", help="register a custom buddy from a generated profile")
    register_parser.add_argument("--theme", required=True)
    register_parser.add_argument("--name", required=True)
    register_parser.add_argument("--profile", required=True, help="JSON string of the full buddy profile")
    register_parser.add_argument("--context", default="", help="one-line note about what user was doing when this buddy appeared")

    summon_parser = subparsers.add_parser("summon", help="call out an unlocked buddy")
    summon_parser.add_argument("--theme", default="general")
    summon_parser.add_argument("--lang", default="en", choices=["zh", "en", "mixed"])
    summon_parser.add_argument("--name", default="auto")
    summon_parser.add_argument("--main", action="store_true")

    unlock_parser = subparsers.add_parser("unlock", help="show a newly unlocked buddy")
    unlock_parser.add_argument("--theme", default="general")
    unlock_parser.add_argument("--lang", default="en", choices=["zh", "en", "mixed"])
    unlock_parser.add_argument("--name", default="auto")
    unlock_parser.add_argument("--reason", default="")

    collection_parser = subparsers.add_parser("collection", help="show unlocked buddies")
    collection_parser.add_argument("--lang", default="en", choices=["zh", "en", "mixed"])
    collection_parser.add_argument("--color", default="auto", choices=["auto", "always", "never"])

    help_parser = subparsers.add_parser("help", help="show buddy commands and usage")
    help_parser.add_argument("--lang", default="en", choices=["zh", "en", "mixed"])

    inspect_parser = subparsers.add_parser("inspect", help="show detailed profile of one buddy")
    inspect_parser.add_argument("--theme", required=True)
    inspect_parser.add_argument("--name", required=True)
    inspect_parser.add_argument("--lang", default="en", choices=["zh", "en", "mixed"])

    args = parser.parse_args()
    if args.command == "render":
        print(
            render_block(
                args.phase,
                args.mood,
                args.task,
                args.next_step,
                args.risk,
                args.theme,
                args.species,
                args.name,
                args.lang,
                args.rarity,
                args.side_quest,
            )
        )
    elif args.command == "hatch":
        print(hatch(args.theme, args.lang))
    elif args.command == "sidequest":
        print(random_side_quest(args.theme, args.lang))
    elif args.command == "pool":
        print(pool_summary(args.theme, args.lang))
    elif args.command == "init":
        print(init_summary(args.theme, args.lang, args.name))
    elif args.command == "summon":
        print(summon_summary(args.theme, args.lang, args.name, args.main))
    elif args.command == "unlock":
        print(unlock_summary(args.theme, args.lang, args.name, args.reason))
    elif args.command == "collection":
        print(collection_summary(args.lang, args.color))
    elif args.command == "help":
        print(help_summary(args.lang))
    elif args.command == "inspect":
        print(inspect_summary(args.theme, args.name, args.lang))
    elif args.command == "register":
        profile = json.loads(args.profile)
        add_to_collection(args.theme, args.name, custom_profile=profile, context=args.context)
        print(f"registered {args.name} in {args.theme}")


if __name__ == "__main__":
    main()
