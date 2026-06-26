from __future__ import annotations

import json
import os
import sqlite3
from dataclasses import dataclass, field
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


@dataclass
class UserState:
    user_id: str
    last_question: str | None = None
    last_answer: str | None = None
    last_book: str | None = None
    last_timestamp: int | None = None
    history_log: list[dict[str, str]] = field(default_factory=list)


def get_db_path() -> Path:
    return Path(os.getenv("ANSWER_LIBRARY_DB", BASE_DIR / "data" / "book-of-answers-skill.sqlite3"))


def connect_db() -> sqlite3.Connection:
    db_path = get_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS user_state (
            user_id TEXT PRIMARY KEY,
            last_question TEXT,
            last_answer TEXT,
            last_book TEXT,
            last_timestamp INTEGER,
            history_log TEXT NOT NULL DEFAULT '[]'
        )
        """
    )
    conn.commit()
    return conn


def parse_history_log(raw_history_log: str | None) -> list[dict[str, str]]:
    try:
        parsed = json.loads(raw_history_log or "[]")
    except json.JSONDecodeError:
        return []

    if not isinstance(parsed, list):
        return []

    history_log: list[dict[str, str]] = []
    for item in parsed:
        if not isinstance(item, dict):
            continue
        history_log.append(
            {
                "date": str(item.get("date", "")),
                "question": str(item.get("question", "")),
                "book_name": str(item.get("book_name", "")),
                "answer": str(item.get("answer", "")),
            }
        )
    return history_log


def coerce_optional_str(value: object) -> str | None:
    if value is None:
        return None
    return str(value)


def coerce_optional_int(value: object) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def load_user_state(user_id: str) -> UserState:
    with connect_db() as conn:
        row = conn.execute(
            """
            SELECT user_id, last_question, last_answer, last_book, last_timestamp, history_log
            FROM user_state
            WHERE user_id = ?
            """,
            (user_id,),
        ).fetchone()

    if row is None:
        return UserState(user_id=user_id)

    return UserState(
        user_id=str(row["user_id"]),
        last_question=coerce_optional_str(row["last_question"]),
        last_answer=coerce_optional_str(row["last_answer"]),
        last_book=coerce_optional_str(row["last_book"]),
        last_timestamp=coerce_optional_int(row["last_timestamp"]),
        history_log=parse_history_log(row["history_log"]),
    )


def save_user_state(state: UserState) -> None:
    with connect_db() as conn:
        conn.execute(
            """
            INSERT INTO user_state (
                user_id,
                last_question,
                last_answer,
                last_book,
                last_timestamp,
                history_log
            ) VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                last_question = excluded.last_question,
                last_answer = excluded.last_answer,
                last_book = excluded.last_book,
                last_timestamp = excluded.last_timestamp,
                history_log = excluded.history_log
            """,
            (
                state.user_id,
                state.last_question,
                state.last_answer,
                state.last_book,
                state.last_timestamp,
                json.dumps(state.history_log, ensure_ascii=False),
            ),
        )
        conn.commit()
