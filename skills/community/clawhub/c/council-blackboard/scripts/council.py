#!/usr/bin/env python3
"""Create and inspect visible Open WebUI council rooms safely."""
from __future__ import annotations

import argparse
import json
import os
import sqlite3
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_WORKSPACE = Path.home() / ".openclaw" / "workspace"
WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", DEFAULT_WORKSPACE)).expanduser()
BOARDS = WORKSPACE / "blackboards" / "councils"
BB = Path(
    os.environ.get(
        "COUNCIL_BLACKBOARD_SCRIPT",
        WORKSPACE / "skills" / "blackboard" / "scripts" / "blackboard.py",
    )
).expanduser()
PYTHON = os.environ.get("COUNCIL_PYTHON", sys.executable)
WEBUI_MODEL = os.environ.get("COUNCIL_WEBUI_MODEL", "local-model:latest")
WEBUI_MODEL_NAME = os.environ.get("COUNCIL_WEBUI_MODEL_NAME", "Local WebUI Model")
WEBUI_BASE_URL = os.environ.get("OPENWEBUI_BASE_URL", "http://127.0.0.1:8080").rstrip("/")
USER_WRITER_ID = os.environ.get("COUNCIL_USER_WRITER", "user/local-user")


def _utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")


def _clean_topic(value: str) -> str:
    topic = " ".join(str(value or "").split())
    if not topic:
        raise ValueError("topic must not be empty")
    if len(topic) > 4000:
        raise ValueError("topic is too long")
    return topic


def safe_board(value: str) -> Path:
    path = Path(value).expanduser().resolve()
    root = BOARDS.resolve()
    if path.parent != root or path.suffix.lower() != ".json":
        raise ValueError("board must be a JSON file directly under the council board directory")
    return path


def run_command(command: list[str], timeout: int = 60) -> str:
    try:
        process = subprocess.run(
            command,
            text=True,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        raise RuntimeError(f"command timed out after {timeout}s: {command[0]}") from error
    if process.returncode:
        detail = (process.stderr or process.stdout or "command failed")[-4000:]
        raise RuntimeError(detail.strip())
    return process.stdout


def run_bb(*args: str) -> str:
    if not BB.is_file():
        raise FileNotFoundError(f"blackboard helper not found: {BB}")
    return run_command([PYTHON, str(BB), *args], timeout=60)


def _database_candidates() -> list[Path]:
    candidates: list[Path] = []
    explicit = os.environ.get("OPENWEBUI_DB")
    if explicit:
        candidates.append(Path(explicit).expanduser())
    candidates.extend(
        [
            WORKSPACE
            / ".venvs"
            / "open-webui"
            / "lib"
            / "python3.12"
            / "site-packages"
            / "open_webui"
            / "data"
            / "webui.db",
            Path.home() / ".open-webui" / "webui.db",
            Path.home() / ".local" / "share" / "open-webui" / "webui.db",
        ]
    )
    unique: list[Path] = []
    seen: set[Path] = set()
    for candidate in candidates:
        resolved = candidate.expanduser()
        if resolved not in seen:
            seen.add(resolved)
            unique.append(resolved)
    return unique


def discover_db() -> Path:
    for candidate in _database_candidates():
        if candidate.is_file():
            return candidate
    searched = "\n- ".join(str(item) for item in _database_candidates())
    raise FileNotFoundError(f"Open WebUI database not found; checked:\n- {searched}")


def _table_info(connection: sqlite3.Connection, table: str) -> list[sqlite3.Row]:
    rows = connection.execute(f'PRAGMA table_info("{table}")').fetchall()
    if not rows:
        raise RuntimeError(f"required Open WebUI table is missing: {table}")
    return rows


def _insert_dynamic(
    connection: sqlite3.Connection,
    table: str,
    values: dict[str, Any],
) -> None:
    info = _table_info(connection, table)
    columns = {str(row[1]): row for row in info}

    missing_required: list[str] = []
    for name, row in columns.items():
        not_null = bool(row[3])
        default = row[4]
        primary_key = bool(row[5])
        if not_null and default is None and not primary_key and name not in values:
            missing_required.append(name)
    if missing_required:
        raise RuntimeError(
            f"Open WebUI schema drift: {table} requires unsupported column(s): "
            + ", ".join(sorted(missing_required))
        )

    selected = [name for name in values if name in columns]
    if not selected:
        raise RuntimeError(f"no compatible columns found for {table}")
    placeholders = ",".join("?" for _ in selected)
    quoted = ",".join(f'"{name}"' for name in selected)
    connection.execute(
        f'INSERT INTO "{table}" ({quoted}) VALUES ({placeholders})',
        tuple(values[name] for name in selected),
    )


def reserve_board_path() -> Path:
    BOARDS.mkdir(parents=True, exist_ok=True)
    return BOARDS / f"council-{_utc_stamp()}-{uuid.uuid4().hex[:10]}.json"


def initialise_board(topic: str, board: Path) -> None:
    run_bb(
        "init",
        str(board),
        "--goal",
        topic,
        "--model",
        USER_WRITER_ID,
        "--max-hops",
        os.environ.get("COUNCIL_MAX_HOPS", "8"),
    )


def cleanup_board(board: Path) -> None:
    candidates = [board, Path(f"{board}.lock")]
    candidates.extend(board.parent.glob(f"{board.name}.bak.*"))
    for candidate in candidates:
        try:
            candidate.unlink()
        except FileNotFoundError:
            pass


def _room_payload(topic: str, board: Path) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    chat_id = str(uuid.uuid4())
    user_message_id = str(uuid.uuid4())
    assistant_message_id = str(uuid.uuid4())
    timestamp = int(time.time())

    intro = (
        f"Council topic: {topic}\n\n"
        f"Blackboard: {board}\n\n"
        f"This room is shared working space for the user, OpenClaw, and {WEBUI_MODEL_NAME}. "
        "Use the Council Blackboard tool for cross-model turns. Preserve claims, evidence, "
        "decisions, failed attempts, tests, and unresolved questions on the board."
    )
    ready = (
        f"Council room ready. I am {WEBUI_MODEL_NAME}. The board is attached through the "
        "Council Blackboard tool. I will use route IDs so one OpenClaw consultation cannot "
        "be confused with another."
    )

    messages = {
        user_message_id: {
            "id": user_message_id,
            "parentId": None,
            "childrenIds": [assistant_message_id],
            "role": "user",
            "content": intro,
            "timestamp": timestamp,
            "models": [WEBUI_MODEL],
            "done": True,
        },
        assistant_message_id: {
            "id": assistant_message_id,
            "parentId": user_message_id,
            "childrenIds": [],
            "role": "assistant",
            "content": ready,
            "done": True,
            "model": WEBUI_MODEL,
            "timestamp": timestamp,
        },
    }
    chat = {
        "id": chat_id,
        "title": "🧠 Council: " + topic[:72],
        "models": [WEBUI_MODEL],
        "history": {"currentId": assistant_message_id, "messages": messages},
        "messages": [
            {"role": "user", "content": intro},
            {"role": "assistant", "content": ready},
        ],
        "files": [],
        "tags": [{"name": "council"}],
        "timestamp": timestamp * 1000,
    }
    return chat, messages


def make_room(topic: str, user_id: str, board: Path, db_path: Path) -> dict[str, Any]:
    chat, messages = _room_payload(topic, board)
    timestamp = int(time.time())
    encoded_chat = json.dumps(chat, ensure_ascii=False)
    encoded_meta = json.dumps(
        {
            "council_board": str(board),
            "council_schema": 1,
            "created_by": "council.py",
        },
        ensure_ascii=False,
    )

    with sqlite3.connect(db_path, timeout=30) as connection:
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA busy_timeout=30000")
        connection.execute("PRAGMA foreign_keys=ON")
        connection.execute("BEGIN IMMEDIATE")
        try:
            _insert_dynamic(
                connection,
                "chat",
                {
                    "id": chat["id"],
                    "user_id": user_id,
                    "title": chat["title"],
                    "share_id": None,
                    "archived": 0,
                    "created_at": timestamp,
                    "updated_at": timestamp,
                    "chat": encoded_chat,
                    "pinned": 0,
                    "meta": encoded_meta,
                    "folder_id": None,
                    "tasks": None,
                    "summary": None,
                    "last_read_at": timestamp,
                },
            )
            for message_id, message in messages.items():
                _insert_dynamic(
                    connection,
                    "chat_message",
                    {
                        "id": message_id,
                        "chat_id": chat["id"],
                        "user_id": user_id,
                        "role": message["role"],
                        "parent_id": message.get("parentId"),
                        "content": json.dumps(message["content"], ensure_ascii=False),
                        "model_id": message.get("model"),
                        "files": json.dumps([]),
                        "sources": json.dumps([]),
                        "embeds": json.dumps([]),
                        "done": bool(message.get("done", True)),
                        "status_history": json.dumps([]),
                        "error": None,
                        "usage": None,
                        "created_at": timestamp,
                        "updated_at": timestamp,
                    },
                )
            connection.commit()
        except BaseException:
            connection.rollback()
            raise

    return {
        "chat_id": chat["id"],
        "chat_url": f"{WEBUI_BASE_URL}/c/{chat['id']}",
        "board": str(board),
        "database": str(db_path),
    }


def create_room(topic: str, user_id: str) -> dict[str, Any]:
    cleaned_topic = _clean_topic(topic)
    cleaned_user_id = str(user_id or "").strip()
    if not cleaned_user_id:
        raise ValueError("user_id is required")

    board = reserve_board_path()
    initialise_board(cleaned_topic, board)
    try:
        return make_room(cleaned_topic, cleaned_user_id, board, discover_db())
    except BaseException:
        cleanup_board(board)
        raise


def doctor() -> dict[str, Any]:
    result: dict[str, Any] = {
        "ok": True,
        "workspace": str(WORKSPACE),
        "boards": str(BOARDS),
        "blackboard": str(BB),
        "python": PYTHON,
        "webui_model": WEBUI_MODEL,
        "base_url": WEBUI_BASE_URL,
    }
    try:
        database = discover_db()
        result["database"] = str(database)
        with sqlite3.connect(database) as connection:
            result["chat_columns"] = [row[1] for row in connection.execute("PRAGMA table_info(chat)")]
            result["chat_message_columns"] = [
                row[1] for row in connection.execute("PRAGMA table_info(chat_message)")
            ]
        if not result["chat_columns"] or not result["chat_message_columns"]:
            raise RuntimeError("chat or chat_message table missing")
    except Exception as error:  # doctor reports instead of aborting
        result["ok"] = False
        result["error"] = str(error)
    return result


def main() -> None:
    argument_parser = argparse.ArgumentParser(description=__doc__)
    commands = argument_parser.add_subparsers(dest="cmd", required=True)

    room = commands.add_parser("room")
    room.add_argument("--topic", required=True)
    room.add_argument("--user-id", required=True)

    show = commands.add_parser("show")
    show.add_argument("--board", required=True)
    show.add_argument("--summary", action="store_true")
    show.add_argument("--limit", type=int, default=6)

    commands.add_parser("doctor")

    args = argument_parser.parse_args()
    if args.cmd == "room":
        print(json.dumps(create_room(args.topic, args.user_id), ensure_ascii=False, indent=2))
    elif args.cmd == "show":
        board = safe_board(args.board)
        command = "summary" if args.summary else "show"
        extra = ["--limit", str(args.limit)] if args.summary else []
        print(run_bb(command, str(board), *extra), end="")
    else:
        print(json.dumps(doctor(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, RuntimeError, sqlite3.Error, json.JSONDecodeError) as error:
        print(json.dumps({"ok": False, "error": str(error)}, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(2) from error
