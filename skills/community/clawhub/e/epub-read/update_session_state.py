"""
Manage session_state.json for EPUB reading workflows.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from utils import write_json


DEFAULT_STATE: dict[str, Any] = {
    "current_mode": None,
    "current_chapter_id": None,
    "current_chunk": None,
    "last_action": None,
    "last_query": None,
    "updated_at": None,
    "reading_history": [],
}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalized_state(raw_state: dict[str, Any] | None) -> dict[str, Any]:
    state = DEFAULT_STATE.copy()
    if raw_state:
        state.update(raw_state)
    if not isinstance(state.get("reading_history"), list):
        state["reading_history"] = []
    return state


def load_state(book_dir: Path) -> dict[str, Any]:
    state_file = book_dir / "session_state.json"
    if not state_file.exists():
        return normalized_state(None)
    try:
        return normalized_state(json.loads(state_file.read_text(encoding="utf-8")))
    except Exception:
        return normalized_state(None)


def save_state(book_dir: Path, state: dict[str, Any]) -> Path:
    state_file = book_dir / "session_state.json"
    serializable = normalized_state(state)
    serializable["updated_at"] = now_iso()
    write_json(state_file, serializable)
    return state_file


def update_progress(
    book_dir: Path,
    *,
    mode: str | None = None,
    chapter_id: str | None = None,
    chunk_index: int | None = None,
    action: str | None = None,
    query: str | None = None,
    **extra_fields: Any,
) -> dict[str, Any]:
    state = load_state(book_dir)

    if mode is not None:
        state["current_mode"] = mode
    if chapter_id is not None:
        state["current_chapter_id"] = chapter_id
    if chunk_index is not None:
        state["current_chunk"] = chunk_index
    if action is not None:
        state["last_action"] = action
    if query is not None:
        state["last_query"] = query

    if extra_fields:
        state.update(extra_fields)

    history_entry = {
        "timestamp": now_iso(),
        "mode": state.get("current_mode"),
        "action": action or state.get("last_action"),
        "chapter_id": state.get("current_chapter_id"),
        "chunk_index": state.get("current_chunk"),
        "query": query if query is not None else state.get("last_query"),
    }
    if any(value is not None for value in history_entry.values()):
        state.setdefault("reading_history", []).append(history_entry)
        state["reading_history"] = state["reading_history"][-100:]

    save_state(book_dir, state)
    return state


def clear_state(book_dir: Path) -> Path:
    return save_state(book_dir, normalized_state(None))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="管理 EPUB 阅读会话状态")
    parser.add_argument("book_dir", help="书籍输出目录")
    parser.add_argument("command", choices=["get", "set", "clear"], help="操作类型")
    parser.add_argument("--mode", type=str, help="设置当前模式")
    parser.add_argument("--chapter", type=str, help="设置当前章节 ID")
    parser.add_argument("--chunk", type=int, help="设置当前 chunk")
    parser.add_argument("--action", type=str, help="设置最后动作")
    parser.add_argument("--query", type=str, help="设置最后查询")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        book_dir = Path(args.book_dir).expanduser().resolve()
        if not book_dir.exists():
            print(f"Error: 目录不存在: {book_dir}", file=sys.stderr)
            return 1

        if args.command == "get":
            state = load_state(book_dir)
            print(json.dumps(state, ensure_ascii=False, indent=2))
            return 0

        if args.command == "clear":
            state_file = clear_state(book_dir)
            print(f"状态已重置: {state_file}")
            return 0

        updated_state = update_progress(
            book_dir,
            mode=args.mode,
            chapter_id=args.chapter,
            chunk_index=args.chunk,
            action=args.action,
            query=args.query,
        )
        print(json.dumps(updated_state, ensure_ascii=False, indent=2))
        return 0

    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
