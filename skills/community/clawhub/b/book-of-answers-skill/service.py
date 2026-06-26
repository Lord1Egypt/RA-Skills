from __future__ import annotations

import dataclasses
import functools
import json
import os
import random
import re
from datetime import datetime, timezone
from pathlib import Path

from router import detect_switch_book_intent, route_question_to_book
from storage import UserState, load_user_state, save_user_state

BASE_DIR = Path(__file__).resolve().parent
DUPLICATE_WINDOW_SECONDS = 300

WELCOME_MESSAGE = """欢迎翻开答案之书。

此刻馆内向你敞开的，是三座各有气质的书架：用银幕对白照亮犹疑的《电影答案之书》，用名句与章节安放心绪的《文学答案之书》，以及用歌词与旋律替情绪命名的《音乐答案之书》。

你可以把问题直接交给我，我会在这三本书之间替你随机翻开最适合的一页；若你心里已有偏爱的语气，也可以亲手指定想问的那一本，让电影回答你的悬念，让文学安放你的心事，让音乐替你唱出未说出口的话。若想领走今天的一句微光，回复“每日一签”。

现在，请把那个最牵动你心绪的问题，轻轻放到桌上。"""
FALLBACK_MESSAGE = "抱歉，图书馆灯光太暗，我没看清。请用文字提出具体的疑问。"
DUPLICATE_MESSAGE = "你刚刚已经问过这个问题了，《答案之书》不接受反复试探，请相信你的第一直觉。刚才给你的指引是：\n{last_answer}"
SWITCH_WITHOUT_CONTEXT_MESSAGE = "你还没有上一题可以换书重测，请先提出一个问题。"
HISTORY_DISABLED_MESSAGE = "借阅记录功能已关闭，当前版本不会保存或展示历史记录。"
STANDARD_RESPONSE_TEMPLATE = """我感受到了你的困惑。
正在为你翻开 {book_name}...

它给你的指引是：
{answer_block}"""

LAUNCH_PHRASES = {"", "开始", "打开答案之书", "欢迎", "进入答案之书", "launch", "start"}
HISTORY_PHRASES = {"查看记录", "历史记录", "查看历史", "我的记录", "浏览记录"}
DAILY_PHRASES = {"每日一签", "今日一签", "今天的签", "来一张今日签文"}
LEGACY_UNSUPPORTED_PHRASES = {"生成卡片", "生成贺卡"}


@dataclasses.dataclass(frozen=True)
class AnswerEntry:
    text: str
    source: str | None = None


@dataclasses.dataclass(frozen=True)
class BookCatalog:
    books: dict[str, list[AnswerEntry]]
    content_mode: str
    notice: str | None = None


def get_books_path() -> Path:
    return Path(os.getenv("ANSWER_LIBRARY_BOOKS", BASE_DIR / "data" / "books.json"))


def parse_answer_string(raw_text: str) -> AnswerEntry:
    line = raw_text.strip()
    if "——" in line:
        text_part, source_part = line.rsplit("——", 1)
        source = source_part.strip() or None
    else:
        text_part = line
        source = None

    text = text_part.strip().strip('"').strip("“”").strip()
    if not text:
        raise ValueError("Answer text cannot be empty.")
    return AnswerEntry(text=text, source=source)


def load_answer_entry(raw_entry: object) -> AnswerEntry:
    if isinstance(raw_entry, dict):
        text = str(raw_entry.get("text", "")).strip()
        source = str(raw_entry.get("source", "")).strip() or None
        if not text:
            raise ValueError("Answer entry is missing text.")
        return AnswerEntry(text=text, source=source)
    if isinstance(raw_entry, str):
        return parse_answer_string(raw_entry)
    raise ValueError(f"Unsupported answer entry type: {type(raw_entry).__name__}")


@functools.lru_cache(maxsize=4)
def load_books_from_path(books_path: str) -> BookCatalog:
    with Path(books_path).open("r", encoding="utf-8") as handle:
        raw_books = json.load(handle)

    meta = raw_books.get("_meta", {}) if isinstance(raw_books, dict) else {}
    content_mode = str(meta.get("content_mode", "provided"))
    notice = meta.get("notice")
    books: dict[str, list[AnswerEntry]] = {}
    for book_name, payload in raw_books.items():
        if str(book_name).startswith("_"):
            continue
        answers = [load_answer_entry(item) for item in payload.get("answers", [])]
        if not answers:
            raise ValueError(f"Book {book_name} has no answers configured.")
        books[book_name] = answers
    return BookCatalog(books=books, content_mode=content_mode, notice=str(notice) if notice else None)


def load_books() -> BookCatalog:
    return load_books_from_path(str(get_books_path().resolve()))


def normalize_text(user_input: str) -> str:
    return re.sub(r"\s+", " ", user_input or "").strip()


def is_launch_intent(user_input: str) -> bool:
    return user_input in LAUNCH_PHRASES


def is_history_intent(user_input: str) -> bool:
    return user_input in HISTORY_PHRASES


def is_daily_fortune_intent(user_input: str) -> bool:
    return user_input in DAILY_PHRASES


def is_unsupported_legacy_intent(user_input: str) -> bool:
    return user_input in LEGACY_UNSUPPORTED_PHRASES


def is_invalid_input(user_input: str) -> bool:
    if not user_input:
        return False
    if re.search(r"[A-Za-z\u4e00-\u9fff]", user_input):
        return False
    return re.fullmatch(r"[\W\d_]+", user_input, re.UNICODE) is not None


def draw_answer(books: dict[str, list[AnswerEntry]], book_name: str) -> AnswerEntry:
    return random.choice(books[book_name])


def render_answer_block(answer: AnswerEntry) -> str:
    if answer.source:
        return f"「 {answer.text} 」\n出处：{answer.source}"
    return f"「 {answer.text} 」"


def format_standard_response(book_name: str, answer: AnswerEntry) -> str:
    return STANDARD_RESPONSE_TEMPLATE.format(book_name=book_name, answer_block=render_answer_block(answer))


def persist_answer_context(
    state: UserState,
    question: str,
    answer: AnswerEntry,
    book_name: str,
    now: datetime,
    *,
    update_last_context: bool = True,
) -> None:
    answer_display = render_answer_block(answer)
    state.history_log = []
    if update_last_context:
        state.last_question = question
        state.last_answer = answer_display
        state.last_book = book_name
        state.last_timestamp = int(now.timestamp())
    save_user_state(state)


def handle_request(user_id: str, user_input: str, now: datetime | None = None) -> str:
    current_time = (now or datetime.now(timezone.utc)).astimezone()
    normalized_input = normalize_text(user_input)
    state = load_user_state(user_id)
    catalog = load_books()

    if is_launch_intent(normalized_input):
        return WELCOME_MESSAGE

    if is_invalid_input(normalized_input):
        return FALLBACK_MESSAGE

    if is_unsupported_legacy_intent(normalized_input):
        return FALLBACK_MESSAGE

    if is_history_intent(normalized_input):
        return HISTORY_DISABLED_MESSAGE

    if is_daily_fortune_intent(normalized_input):
        selected_book = random.choice(list(catalog.books))
        answer = draw_answer(catalog.books, selected_book)
        persist_answer_context(
            state,
            normalized_input,
            answer,
            selected_book,
            current_time,
            update_last_context=False,
        )
        return f"【每日一签】\n{render_answer_block(answer)}"

    switch_book = detect_switch_book_intent(normalized_input)
    if switch_book:
        if not state.last_question:
            return SWITCH_WITHOUT_CONTEXT_MESSAGE
        current_question = state.last_question
        selected_book = switch_book
        bypass_duplicate_check = True
    else:
        current_question = normalized_input
        selected_book = route_question_to_book(normalized_input).book_name
        bypass_duplicate_check = False

    if selected_book not in catalog.books:
        selected_book = random.choice(list(catalog.books))

    if (
        not bypass_duplicate_check
        and state.last_question == current_question
        and state.last_timestamp is not None
        and int(current_time.timestamp()) - state.last_timestamp < DUPLICATE_WINDOW_SECONDS
    ):
        return DUPLICATE_MESSAGE.format(last_answer=state.last_answer or "")

    answer = draw_answer(catalog.books, selected_book)
    persist_answer_context(state, current_question, answer, selected_book, current_time)
    return format_standard_response(selected_book, answer)
