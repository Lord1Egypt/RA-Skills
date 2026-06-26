from __future__ import annotations

import random
import re
from dataclasses import dataclass

MOVIE_BOOK = "《电影答案之书》"
LITERARY_BOOK = "《文学答案之书》"
MUSIC_BOOK = "《音乐答案之书》"
DEFAULT_BOOKS = (MOVIE_BOOK, LITERARY_BOOK, MUSIC_BOOK)

SWITCH_BOOK_ALIASES = [
    ("电影答案之书", MOVIE_BOOK),
    ("电影之书", MOVIE_BOOK),
    ("电影版", MOVIE_BOOK),
    ("电影", MOVIE_BOOK),
    ("文学答案之书", LITERARY_BOOK),
    ("文学之书", LITERARY_BOOK),
    ("文学版", LITERARY_BOOK),
    ("文学", LITERARY_BOOK),
    ("音乐答案之书", MUSIC_BOOK),
    ("音乐之书", MUSIC_BOOK),
    ("音乐版", MUSIC_BOOK),
    ("音乐", MUSIC_BOOK),
]

EXPLICIT_BOOK_PATTERNS = {
    MOVIE_BOOK: [
        re.compile(r"(用|请用|给我用|翻开|打开).{0,4}电影(答案之书|之书|版)?"),
        re.compile(r"电影(答案之书|之书|版).{0,4}(问|看看|测|回答)"),
    ],
    LITERARY_BOOK: [
        re.compile(r"(用|请用|给我用|翻开|打开).{0,4}文学(答案之书|之书|版)?"),
        re.compile(r"文学(答案之书|之书|版).{0,4}(问|看看|测|回答)"),
    ],
    MUSIC_BOOK: [
        re.compile(r"(用|请用|给我用|翻开|打开).{0,4}音乐(答案之书|之书|版)?"),
        re.compile(r"音乐(答案之书|之书|版).{0,4}(问|看看|测|回答)"),
    ],
}

SWITCH_HINTS = ("换", "换成", "再测", "再来", "重新", "再试", "用")
SWITCH_FILLER_PHRASES = [
    "那就",
    "那用",
    "那",
    "的",
    "请",
    "帮我",
    "给我",
    "一下",
    "再测一次",
    "再来一次",
    "再试一次",
    "再测",
    "再来",
    "再试",
    "一次",
    "版本",
    "版的",
    "之书",
    "答案之书",
    "用",
    "换成",
    "换",
    "吧",
    "呀",
    "啊",
    "重新",
]

ROUTING_SIGNALS = {
    MOVIE_BOOK: {
        "keywords": {
            "电影": 2.4,
            "镜头": 2.8,
            "结局": 1.8,
            "台词": 2.6,
            "主角": 2.0,
            "配乐": 2.0,
            "荧幕": 2.2,
            "导演": 1.8,
            "剧情": 2.2,
        },
        "regex": [
            (r"(像|如同).{0,8}(电影|镜头|结局)", 2.4),
            (r"(这段|这一场|这次).{0,10}(像什么电影|会是什么结局)", 2.6),
        ],
    },
    LITERARY_BOOK: {
        "keywords": {
            "文学": 2.4,
            "名著": 2.8,
            "小说": 2.4,
            "诗": 1.8,
            "诗句": 2.2,
            "章节": 2.0,
            "书页": 2.0,
            "段落": 1.8,
            "句子": 1.6,
            "注脚": 2.0,
        },
        "regex": [
            (r"(像|如同).{0,8}(小说|诗|章节|名著)", 2.2),
            (r"(写进|放进).{0,8}(小说|书里|章节)", 2.0),
        ],
    },
    MUSIC_BOOK: {
        "keywords": {
            "音乐": 2.6,
            "歌词": 2.8,
            "旋律": 2.4,
            "歌单": 2.6,
            "歌曲": 2.6,
            "副歌": 2.2,
            "前奏": 2.0,
            "耳机": 1.8,
            "节拍": 2.0,
            "唱片": 1.8,
            "听歌": 2.6,
        },
        "regex": [
            (r"(像|如同).{0,8}(一首歌|歌词|旋律)", 2.4),
            (r"(适合|想听|该听).{0,8}(什么歌|哪首歌|什么音乐)", 2.6),
        ],
    },
}


@dataclass(frozen=True)
class RouteDecision:
    book_name: str
    confidence: float
    scores: dict[str, float]
    reasons: list[str]


def find_book_alias(user_input: str, aliases: list[tuple[str, str]]) -> str | None:
    for alias, book_name in aliases:
        if alias in user_input:
            return book_name
    return None


def detect_switch_book_intent(user_input: str) -> str | None:
    requested_book = find_book_alias(user_input, SWITCH_BOOK_ALIASES)
    if not requested_book:
        return None
    if not any(hint in user_input for hint in SWITCH_HINTS):
        return None

    residual = user_input
    for alias, _book_name in SWITCH_BOOK_ALIASES:
        residual = residual.replace(alias, " ")
    for filler in SWITCH_FILLER_PHRASES:
        residual = residual.replace(filler, " ")

    residual = re.sub(r"[，。！？!?、,.~～\s]+", "", residual)
    if residual:
        return None
    return requested_book


def detect_explicit_book(user_input: str) -> RouteDecision | None:
    for book_name, patterns in EXPLICIT_BOOK_PATTERNS.items():
        for pattern in patterns:
            if pattern.search(user_input):
                return RouteDecision(book_name, 0.98, {book_name: 9.5}, [f"explicit:{book_name}"])
    return None


def score_implicit_books(user_input: str) -> tuple[dict[str, float], dict[str, list[str]]]:
    scores = {book_name: 0.0 for book_name in ROUTING_SIGNALS}
    reasons = {book_name: [] for book_name in ROUTING_SIGNALS}

    for book_name, rules in ROUTING_SIGNALS.items():
        for keyword, weight in rules["keywords"].items():
            if keyword in user_input:
                scores[book_name] += weight
                reasons[book_name].append(f"kw:{keyword}")

        for pattern, weight in rules["regex"]:
            if re.search(pattern, user_input):
                scores[book_name] += weight
                reasons[book_name].append(f"re:{pattern}")

    return scores, reasons


def resolve_confidence(scores: dict[str, float], book_name: str) -> float:
    ordered_scores = sorted(scores.values(), reverse=True)
    top_score = ordered_scores[0]
    second_score = ordered_scores[1] if len(ordered_scores) > 1 else 0.0
    margin = top_score - second_score

    if top_score <= 0:
        return 0.35
    if top_score >= 4 or margin >= 2:
        return min(0.92, 0.58 + top_score / 16)
    if top_score >= 2:
        return min(0.8, 0.46 + top_score / 18)
    if book_name in DEFAULT_BOOKS:
        return 0.35
    return 0.4


def route_question_to_book(user_input: str) -> RouteDecision:
    explicit_decision = detect_explicit_book(user_input)
    if explicit_decision is not None:
        return explicit_decision

    scores, reasons = score_implicit_books(user_input)
    ordered = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    top_book, top_score = ordered[0]
    second_score = ordered[1][1] if len(ordered) > 1 else 0.0

    if top_score < 2 or top_score - second_score < 0.8:
        fallback_book = random.choice(DEFAULT_BOOKS)
        return RouteDecision(fallback_book, 0.35, scores, ["fallback:random"])

    confidence = resolve_confidence(scores, top_book)
    return RouteDecision(top_book, confidence, scores, reasons[top_book])


def select_book(user_input: str) -> str:
    return route_question_to_book(user_input).book_name
