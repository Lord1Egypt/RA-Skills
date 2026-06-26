#!/usr/bin/env python3
from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import hashlib
import json
import re
import shutil
import sqlite3
import sys
import tarfile
import tempfile
import uuid
from pathlib import Path
from typing import Any, Callable, Iterable, Iterator


VISIBLE_MESSAGE_TYPES = {"user_message", "agent_message"}
DEFAULT_BACKUP_ROOT = Path(__file__).resolve().parents[1] / "backups"


@dataclasses.dataclass
class ThreadRecord:
    id: str
    rollout_path: Path
    created_at: int
    updated_at: int
    source: str
    model_provider: str
    cwd: str
    title: str
    sandbox_policy: str
    approval_mode: str
    tokens_used: int
    has_user_event: int
    archived: int
    archived_at: int | None
    git_sha: str | None
    git_branch: str | None
    git_origin_url: str | None
    cli_version: str
    first_user_message: str
    agent_nickname: str | None
    agent_role: str | None
    memory_mode: str
    model: str | None
    reasoning_effort: str | None
    agent_path: str | None

    @classmethod
    def from_row(cls, row: sqlite3.Row) -> "ThreadRecord":
        payload = dict(row)
        payload["rollout_path"] = Path(payload["rollout_path"])
        return cls(**payload)

    def to_dict(self) -> dict[str, Any]:
        data = dataclasses.asdict(self)
        data["rollout_path"] = str(self.rollout_path)
        return data


@dataclasses.dataclass
class TranscriptMessage:
    timestamp: str
    role: str
    text: str
    phase: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return dataclasses.asdict(self)


@dataclasses.dataclass
class ThreadData:
    thread: ThreadRecord
    session_meta: dict[str, Any] | None
    transcript: list[TranscriptMessage]

    def to_dict(self) -> dict[str, Any]:
        return {
            "thread": self.thread.to_dict(),
            "session_meta": self.session_meta,
            "transcript": [message.to_dict() for message in self.transcript],
        }


@dataclasses.dataclass
class DangerousEditChange:
    location: str
    before_preview: str
    after_preview: str
    occurrences: int

    def to_dict(self) -> dict[str, Any]:
        return dataclasses.asdict(self)


class CodexHistoryError(RuntimeError):
    pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Search, export, and safely mutate local Codex history."
    )
    parser.add_argument(
        "--codex-home",
        type=Path,
        default=Path.home() / ".codex",
        help="Codex home directory. Defaults to ~/.codex",
    )
    parser.add_argument(
        "--backup-root",
        type=Path,
        default=DEFAULT_BACKUP_ROOT,
        help="Backup directory for write operations.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    search = subparsers.add_parser("search", help="Search thread metadata and visible transcript text.")
    search.add_argument("--query", help="Case-insensitive text query.")
    search.add_argument("--cwd", help="Filter by workspace path.")
    search.add_argument("--provider", help="Filter by model provider.")
    search.add_argument("--source", help="Filter by source, for example vscode or cli.")
    search.add_argument("--limit", type=int, default=20, help="Maximum number of results.")
    search.add_argument("--json", action="store_true", help="Emit JSON instead of text.")

    show = subparsers.add_parser("show-thread", help="Show one thread and its visible transcript.")
    show.add_argument("--id", required=True, help="Thread id.")
    show.add_argument("--json", action="store_true", help="Emit JSON instead of text.")
    show.add_argument(
        "--max-messages",
        type=int,
        default=80,
        help="Maximum visible transcript messages to show.",
    )

    export = subparsers.add_parser("export-thread", help="Export one thread.")
    export.add_argument("--id", required=True, help="Thread id.")
    export.add_argument(
        "--format",
        required=True,
        choices=("markdown", "json", "jsonl"),
        help="Export format.",
    )
    export.add_argument("--output", type=Path, required=True, help="Output path.")

    handoff = subparsers.add_parser("handoff", help="Generate a deterministic handoff note for one thread.")
    handoff.add_argument("--id", required=True, help="Thread id.")
    handoff.add_argument("--output", type=Path, required=True, help="Output markdown path.")
    handoff.add_argument(
        "--recent-messages",
        type=int,
        default=10,
        help="How many recent visible messages to include.",
    )

    dangerous_plan = subparsers.add_parser(
        "plan-dangerous-edit",
        help="Prepare a transcript rewrite plan for one thread. This does not modify history.",
    )
    dangerous_plan.add_argument("--id", required=True, help="Thread id.")
    dangerous_plan.add_argument("--find", required=True, help="Exact text to replace.")
    dangerous_plan.add_argument("--replace", required=True, help="Replacement text.")
    dangerous_plan.add_argument("--output", type=Path, help="Optional path to write the plan JSON.")

    dangerous_apply = subparsers.add_parser(
        "apply-dangerous-edit",
        help="Apply a previously planned transcript rewrite after explicit confirmation.",
    )
    dangerous_apply.add_argument("--plan", type=Path, required=True, help="Plan JSON from plan-dangerous-edit.")
    dangerous_apply.add_argument("--confirm-plan-id", required=True, help="Plan id shown by the planning step.")
    dangerous_apply.add_argument(
        "--acknowledge-history-rewrite",
        action="store_true",
        help="Required acknowledgement that this permanently rewrites history content.",
    )
    add_write_flags(dangerous_apply)

    move = subparsers.add_parser("move-thread", help="Change a thread's workspace path.")
    move.add_argument("--id", required=True, help="Thread id.")
    move.add_argument("--to-cwd", required=True, help="Target workspace path.")
    add_write_flags(move)

    move_workspace = subparsers.add_parser("move-workspace", help="Move every thread from one workspace to another.")
    move_workspace.add_argument("--cwd", required=True, help="Source workspace path.")
    move_workspace.add_argument("--to-cwd", required=True, help="Target workspace path.")
    add_write_flags(move_workspace)

    clone = subparsers.add_parser("clone-thread", help="Clone a thread into another workspace.")
    clone.add_argument("--id", required=True, help="Thread id.")
    clone.add_argument("--to-cwd", required=True, help="Target workspace path.")
    clone.add_argument(
        "--unarchive",
        action="store_true",
        help="Mark the cloned thread as active even if the source thread was archived.",
    )
    add_write_flags(clone)

    clone_workspace = subparsers.add_parser("clone-workspace", help="Clone every thread from one workspace to another.")
    clone_workspace.add_argument("--cwd", required=True, help="Source workspace path.")
    clone_workspace.add_argument("--to-cwd", required=True, help="Target workspace path.")
    clone_workspace.add_argument(
        "--unarchive",
        action="store_true",
        help="Mark cloned threads as active even if the source threads were archived.",
    )
    add_write_flags(clone_workspace)

    provider = subparsers.add_parser("change-provider", help="Change a thread's provider metadata.")
    provider.add_argument("--id", required=True, help="Thread id.")
    provider.add_argument("--provider", required=True, help="Target provider name.")
    provider.add_argument("--model", help="Optional model name to set on thread and turn_context.")
    add_write_flags(provider)

    provider_workspace = subparsers.add_parser(
        "change-provider-workspace",
        help="Change provider metadata for every thread in one workspace.",
    )
    provider_workspace.add_argument("--cwd", required=True, help="Workspace path to match.")
    provider_workspace.add_argument("--provider", required=True, help="Target provider name.")
    provider_workspace.add_argument("--model", help="Optional model name to set on matching threads.")
    add_write_flags(provider_workspace)

    provider_all = subparsers.add_parser(
        "change-provider-all",
        help="Change provider metadata for every local Codex thread.",
    )
    provider_all.add_argument("--provider", required=True, help="Target provider name.")
    provider_all.add_argument("--model", help="Optional model name to set on every thread.")
    add_write_flags(provider_all)

    return parser.parse_args()


def add_write_flags(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply changes. Without this flag the command is a dry run.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned changes without mutating files.",
    )


def ensure_codex_home(codex_home: Path) -> tuple[Path, Path]:
    codex_home = codex_home.expanduser().resolve()
    db_path = codex_home / "state_5.sqlite"
    if not codex_home.exists():
        raise CodexHistoryError(f"Codex home does not exist: {codex_home}")
    if not db_path.exists():
        raise CodexHistoryError(f"Codex database does not exist: {db_path}")
    return codex_home, db_path


def connect_db(db_path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def normalize_query(text: str | None) -> str | None:
    if text is None:
        return None
    cleaned = text.strip().lower()
    return cleaned or None


def fetch_threads(
    conn: sqlite3.Connection,
    cwd: str | None = None,
    provider: str | None = None,
    source: str | None = None,
) -> list[ThreadRecord]:
    conditions: list[str] = []
    values: list[Any] = []
    if cwd:
        conditions.append("cwd = ?")
        values.append(cwd)
    if provider:
        conditions.append("model_provider = ?")
        values.append(provider)
    if source:
        conditions.append("source = ?")
        values.append(source)

    sql = "select * from threads"
    if conditions:
        sql += " where " + " and ".join(conditions)
    sql += " order by updated_at desc"

    rows = conn.execute(sql, values).fetchall()
    return [ThreadRecord.from_row(row) for row in rows]


def fetch_thread(conn: sqlite3.Connection, thread_id: str) -> ThreadRecord:
    row = conn.execute("select * from threads where id = ?", (thread_id,)).fetchone()
    if row is None:
        raise CodexHistoryError(f"Thread not found: {thread_id}")
    return ThreadRecord.from_row(row)


def fetch_threads_by_ids(conn: sqlite3.Connection, thread_ids: Iterable[str]) -> list[ThreadRecord]:
    ids = list(dict.fromkeys(thread_ids))
    if not ids:
        return []
    placeholders = ", ".join("?" for _ in ids)
    rows = conn.execute(
        f"select * from threads where id in ({placeholders}) order by updated_at desc",
        ids,
    ).fetchall()
    return [ThreadRecord.from_row(row) for row in rows]


def iter_rollout_records(path: Path) -> Iterator[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        for line_no, raw_line in enumerate(handle, start=1):
            try:
                yield json.loads(raw_line)
            except json.JSONDecodeError as exc:
                raise CodexHistoryError(f"Invalid JSON in {path}:{line_no}: {exc}") from exc


def visible_transcript(path: Path) -> list[TranscriptMessage]:
    messages: list[TranscriptMessage] = []
    for record in iter_rollout_records(path):
        if record.get("type") != "event_msg":
            continue
        payload = record.get("payload")
        if not isinstance(payload, dict):
            continue
        message_type = payload.get("type")
        if message_type not in VISIBLE_MESSAGE_TYPES:
            continue
        text = payload.get("message")
        if not isinstance(text, str):
            continue
        role = "assistant" if message_type == "agent_message" else "user"
        phase = payload.get("phase") if isinstance(payload.get("phase"), str) else None
        messages.append(
            TranscriptMessage(
                timestamp=str(record.get("timestamp", "")),
                role=role,
                text=text.rstrip(),
                phase=phase,
            )
        )
    return messages


def load_session_meta(path: Path) -> dict[str, Any] | None:
    for record in iter_rollout_records(path):
        if record.get("type") == "session_meta":
            payload = record.get("payload")
            return payload if isinstance(payload, dict) else None
    return None


def load_thread_data(thread: ThreadRecord) -> ThreadData:
    return ThreadData(
        thread=thread,
        session_meta=load_session_meta(thread.rollout_path),
        transcript=visible_transcript(thread.rollout_path),
    )


def timestamp_to_iso(value: int | None) -> str | None:
    if value is None:
        return None
    try:
        # Codex thread timestamps are currently stored as Unix seconds in SQLite.
        # Keep a millisecond fallback so the tool stays resilient if that changes.
        seconds = value / 1000 if value > 10_000_000_000 else value
        return dt.datetime.fromtimestamp(seconds, tz=dt.timezone.utc).isoformat()
    except (OSError, OverflowError, ValueError):
        return None


def truncate_text(text: str, limit: int = 120) -> str:
    compact = " ".join(text.split())
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3] + "..."


def replace_literal(text: str, old: str, new: str) -> tuple[str, int]:
    occurrences = text.count(old)
    if occurrences == 0:
        return text, 0
    return text.replace(old, new), occurrences


def matches_query(thread: ThreadRecord, transcript: list[TranscriptMessage], query: str | None) -> tuple[bool, list[str]]:
    if not query:
        return True, []

    haystacks = {
        "title": thread.title,
        "first_user_message": thread.first_user_message,
        "transcript": "\n".join(message.text for message in transcript),
    }
    matched_fields = [
        name for name, value in haystacks.items() if query in value.lower()
    ]
    return bool(matched_fields), matched_fields


def command_search(args: argparse.Namespace) -> int:
    codex_home, db_path = ensure_codex_home(args.codex_home)
    query = normalize_query(args.query)
    with connect_db(db_path) as conn:
        candidates = fetch_threads(conn, cwd=args.cwd, provider=args.provider, source=args.source)

    results: list[dict[str, Any]] = []
    for thread in candidates:
        transcript: list[TranscriptMessage] = []
        if query:
            transcript = visible_transcript(thread.rollout_path)
        matched, matched_fields = matches_query(thread, transcript, query)
        if not matched:
            continue
        if not transcript:
            transcript = visible_transcript(thread.rollout_path)
        latest_message = transcript[-1].text if transcript else thread.first_user_message
        results.append(
            {
                "id": thread.id,
                "title": thread.title,
                "cwd": thread.cwd,
                "provider": thread.model_provider,
                "source": thread.source,
                "archived": bool(thread.archived),
                "updated_at": timestamp_to_iso(thread.updated_at),
                "matched_fields": matched_fields,
                "preview": truncate_text(latest_message),
                "rollout_path": str(thread.rollout_path),
            }
        )
        if len(results) >= args.limit:
            break

    if args.json:
        print(json.dumps({"codex_home": str(codex_home), "results": results}, ensure_ascii=False, indent=2))
        return 0

    print(f"Codex home: {codex_home}")
    print(f"Results: {len(results)}")
    for index, result in enumerate(results, start=1):
        print(f"{index}. {result['id']}")
        print(f"   title: {result['title']}")
        print(f"   cwd: {result['cwd']}")
        print(f"   provider: {result['provider']} source: {result['source']} archived: {result['archived']}")
        print(f"   updated_at: {result['updated_at']}")
        if result["matched_fields"]:
            print(f"   matched: {', '.join(result['matched_fields'])}")
        print(f"   preview: {result['preview']}")
    return 0


def render_thread_text(data: ThreadData, max_messages: int) -> str:
    lines = [
        f"Thread ID: {data.thread.id}",
        f"Title: {data.thread.title}",
        f"CWD: {data.thread.cwd}",
        f"Provider: {data.thread.model_provider}",
        f"Model: {data.thread.model or 'unknown'}",
        f"Source: {data.thread.source}",
        f"Archived: {bool(data.thread.archived)}",
        f"Created: {timestamp_to_iso(data.thread.created_at)}",
        f"Updated: {timestamp_to_iso(data.thread.updated_at)}",
        f"Rollout: {data.thread.rollout_path}",
        "",
        "Transcript:",
    ]
    for message in data.transcript[:max_messages]:
        header = f"[{message.timestamp}] {message.role}"
        if message.phase:
            header += f" ({message.phase})"
        lines.append(header)
        lines.append(message.text)
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def command_show_thread(args: argparse.Namespace) -> int:
    _, db_path = ensure_codex_home(args.codex_home)
    with connect_db(db_path) as conn:
        thread = fetch_thread(conn, args.id)
    data = load_thread_data(thread)
    if args.json:
        print(json.dumps(data.to_dict(), ensure_ascii=False, indent=2))
    else:
        sys.stdout.write(render_thread_text(data, max_messages=args.max_messages))
    return 0


def render_markdown_export(data: ThreadData) -> str:
    lines = [
        f"# {data.thread.title}",
        "",
        f"- Thread ID: `{data.thread.id}`",
        f"- CWD: `{data.thread.cwd}`",
        f"- Provider: `{data.thread.model_provider}`",
        f"- Model: `{data.thread.model or 'unknown'}`",
        f"- Source: `{data.thread.source}`",
        f"- Archived: `{bool(data.thread.archived)}`",
        f"- Created: `{timestamp_to_iso(data.thread.created_at)}`",
        f"- Updated: `{timestamp_to_iso(data.thread.updated_at)}`",
        f"- Rollout: `{data.thread.rollout_path}`",
        "",
        "## Transcript",
        "",
    ]
    for message in data.transcript:
        heading = f"### {message.role.title()}"
        if message.phase:
            heading += f" ({message.phase})"
        lines.extend([heading, "", message.text, ""])
    return "\n".join(lines).rstrip() + "\n"


def write_text(path: Path, text: str) -> None:
    path = path.expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def command_export_thread(args: argparse.Namespace) -> int:
    _, db_path = ensure_codex_home(args.codex_home)
    with connect_db(db_path) as conn:
        thread = fetch_thread(conn, args.id)
    data = load_thread_data(thread)
    output_path = args.output.expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if args.format == "markdown":
        write_text(output_path, render_markdown_export(data))
    elif args.format == "json":
        write_text(output_path, json.dumps(data.to_dict(), ensure_ascii=False, indent=2) + "\n")
    else:
        with output_path.open("w", encoding="utf-8") as handle:
            for record in data.transcript:
                handle.write(json.dumps(record.to_dict(), ensure_ascii=False) + "\n")

    print(f"Wrote {args.format} export to {output_path}")
    return 0


def extract_paths(transcript: Iterable[TranscriptMessage]) -> list[str]:
    pattern = re.compile(r"(?:/Users|/Applications|~\/)[^\s`'\"\)\]]+")
    seen: list[str] = []
    for message in transcript:
        for match in pattern.findall(message.text):
            if match not in seen:
                seen.append(match)
    return seen[:20]


def render_handoff(data: ThreadData, recent_messages: int) -> str:
    recent = data.transcript[-recent_messages:]
    recent_user = next((message for message in reversed(data.transcript) if message.role == "user"), None)
    recent_assistant = next((message for message in reversed(data.transcript) if message.role == "assistant"), None)
    lines = [
        f"# Handoff: {data.thread.title}",
        "",
        "## Thread",
        "",
        f"- Thread ID: `{data.thread.id}`",
        f"- CWD: `{data.thread.cwd}`",
        f"- Provider: `{data.thread.model_provider}`",
        f"- Model: `{data.thread.model or 'unknown'}`",
        f"- Source: `{data.thread.source}`",
        f"- Updated: `{timestamp_to_iso(data.thread.updated_at)}`",
        f"- Rollout: `{data.thread.rollout_path}`",
        "",
        "## Current State",
        "",
        f"- Latest user message: {truncate_text(recent_user.text, 240) if recent_user else 'n/a'}",
        f"- Latest assistant message: {truncate_text(recent_assistant.text, 240) if recent_assistant else 'n/a'}",
        f"- Visible message count: {len(data.transcript)}",
        "",
        "## Referenced Paths",
        "",
    ]
    paths = extract_paths(data.transcript)
    if paths:
        lines.extend([f"- `{path}`" for path in paths])
    else:
        lines.append("- None detected")

    lines.extend(
        [
            "",
            "## Recent Transcript",
            "",
        ]
    )
    for message in recent:
        heading = f"### {message.role.title()}"
        if message.phase:
            heading += f" ({message.phase})"
        lines.extend([heading, "", message.text, ""])
    return "\n".join(lines).rstrip() + "\n"


def command_handoff(args: argparse.Namespace) -> int:
    _, db_path = ensure_codex_home(args.codex_home)
    with connect_db(db_path) as conn:
        thread = fetch_thread(conn, args.id)
    data = load_thread_data(thread)
    write_text(args.output, render_handoff(data, recent_messages=args.recent_messages))
    print(f"Wrote handoff to {args.output.expanduser().resolve()}")
    return 0


def build_dangerous_edit_plan(thread: ThreadRecord, find: str, replace: str) -> dict[str, Any]:
    if not find:
        raise CodexHistoryError("--find must be a non-empty string")
    if find == replace:
        raise CodexHistoryError("--find and --replace are identical; nothing to change")

    changes: list[DangerousEditChange] = []
    total_occurrences = 0

    for field_name, field_value in (
        ("threads.title", thread.title),
        ("threads.first_user_message", thread.first_user_message),
    ):
        updated, occurrences = replace_literal(field_value, find, replace)
        if occurrences:
            changes.append(
                DangerousEditChange(
                    location=field_name,
                    before_preview=truncate_text(field_value, 180),
                    after_preview=truncate_text(updated, 180),
                    occurrences=occurrences,
                )
            )
            total_occurrences += occurrences

    for line_no, record in enumerate(iter_rollout_records(thread.rollout_path), start=1):
        record_type = record.get("type")
        if record_type == "event_msg":
            payload = record.get("payload")
            if isinstance(payload, dict) and payload.get("type") in VISIBLE_MESSAGE_TYPES:
                message = payload.get("message")
                if isinstance(message, str):
                    updated, occurrences = replace_literal(message, find, replace)
                    if occurrences:
                        changes.append(
                            DangerousEditChange(
                                location=f"rollout:{line_no}:event_msg.payload.message",
                                before_preview=truncate_text(message, 180),
                                after_preview=truncate_text(updated, 180),
                                occurrences=occurrences,
                            )
                        )
                        total_occurrences += occurrences
        if record_type == "response_item":
            payload = record.get("payload")
            if isinstance(payload, dict) and payload.get("type") == "message" and payload.get("role") in {"user", "assistant"}:
                content = payload.get("content")
                if isinstance(content, list):
                    for index, item in enumerate(content):
                        if not isinstance(item, dict):
                            continue
                        if item.get("type") not in {"input_text", "output_text"}:
                            continue
                        text = item.get("text")
                        if not isinstance(text, str):
                            continue
                        updated, occurrences = replace_literal(text, find, replace)
                        if occurrences:
                            changes.append(
                                DangerousEditChange(
                                    location=f"rollout:{line_no}:response_item.payload.content[{index}].text",
                                    before_preview=truncate_text(text, 180),
                                    after_preview=truncate_text(updated, 180),
                                    occurrences=occurrences,
                                )
                            )
                            total_occurrences += occurrences

    if not changes:
        raise CodexHistoryError("No matching editable history content found for the requested replacement.")

    plan_core = {
        "thread_id": thread.id,
        "rollout_path": str(thread.rollout_path),
        "find": find,
        "replace": replace,
        "change_count": len(changes),
        "total_occurrences": total_occurrences,
    }
    plan_id = hashlib.sha256(
        json.dumps(plan_core, ensure_ascii=False, sort_keys=True).encode("utf-8")
    ).hexdigest()[:16]

    return {
        "version": 1,
        "plan_id": plan_id,
        "warning": (
            "Dangerous operation. This rewrites stored history content and can permanently change "
            "search results, exports, and future handoff context. Review the change list with the user "
            "and obtain explicit approval before applying."
        ),
        "thread": thread.to_dict(),
        "find": find,
        "replace": replace,
        "change_count": len(changes),
        "total_occurrences": total_occurrences,
        "changes": [change.to_dict() for change in changes],
    }


def apply_dangerous_edit_plan(
    conn: sqlite3.Connection,
    thread: ThreadRecord,
    plan: dict[str, Any],
) -> tuple[int, int]:
    find = str(plan["find"])
    replace = str(plan["replace"])

    title, title_count = replace_literal(thread.title, find, replace)
    first_user_message, first_count = replace_literal(thread.first_user_message, find, replace)
    conn.execute(
        "update threads set title = ?, first_user_message = ?, updated_at = ? where id = ?",
        (title, first_user_message, now_timestamp(), thread.id),
    )
    conn.commit()

    def transform(record: dict[str, Any]) -> dict[str, Any]:
        if record.get("type") == "event_msg":
            payload = record.get("payload")
            if isinstance(payload, dict) and payload.get("type") in VISIBLE_MESSAGE_TYPES:
                message = payload.get("message")
                if isinstance(message, str):
                    payload["message"] = message.replace(find, replace)
        if record.get("type") == "response_item":
            payload = record.get("payload")
            if isinstance(payload, dict) and payload.get("type") == "message" and payload.get("role") in {"user", "assistant"}:
                content = payload.get("content")
                if isinstance(content, list):
                    for item in content:
                        if not isinstance(item, dict):
                            continue
                        if item.get("type") not in {"input_text", "output_text"}:
                            continue
                        text = item.get("text")
                        if isinstance(text, str):
                            item["text"] = text.replace(find, replace)
        return record

    rollout_changed = replace_in_place(thread.rollout_path, transform)
    return title_count + first_count, rollout_changed


def command_plan_dangerous_edit(args: argparse.Namespace) -> int:
    _, db_path = ensure_codex_home(args.codex_home)
    with connect_db(db_path) as conn:
        thread = fetch_thread(conn, args.id)
    plan = build_dangerous_edit_plan(thread, args.find, args.replace)
    payload = json.dumps(plan, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        write_text(args.output, payload)
        print(f"Wrote dangerous edit plan to {args.output.expanduser().resolve()}")
    print(payload, end="" if args.output else "")
    return 0


def command_apply_dangerous_edit(args: argparse.Namespace) -> int:
    if not args.acknowledge_history_rewrite:
        raise CodexHistoryError(
            "Refusing to rewrite history without --acknowledge-history-rewrite."
        )
    if not should_apply(args):
        print("Dangerous edit is still in dry-run mode. Re-run with --apply after user approval.")
        return 0

    plan_path = args.plan.expanduser().resolve()
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    plan_id = plan.get("plan_id")
    if not isinstance(plan_id, str) or plan_id != args.confirm_plan_id:
        raise CodexHistoryError("Confirmation failed: --confirm-plan-id does not match the plan.")
    if plan.get("version") != 1:
        raise CodexHistoryError("Unsupported dangerous edit plan version.")

    codex_home, db_path = ensure_codex_home(args.codex_home)
    thread_info = plan.get("thread")
    if not isinstance(thread_info, dict) or not isinstance(thread_info.get("id"), str):
        raise CodexHistoryError("Plan is missing thread metadata.")

    with connect_db(db_path) as conn:
        thread = fetch_thread(conn, thread_info["id"])
    if str(thread.rollout_path) != str(thread_info.get("rollout_path")):
        raise CodexHistoryError("Thread rollout path no longer matches the plan. Regenerate the plan first.")

    backup_root = backup_dir(args.backup_root, f"dangerous-edit-{thread.id}")
    backup_database(db_path, backup_root)
    backup_rollouts(codex_home, [thread.rollout_path], backup_root)

    with connect_db(db_path) as conn:
        sqlite_occurrences, rollout_changed = apply_dangerous_edit_plan(conn, thread, plan)

    print(f"Applied dangerous history rewrite. Backup: {backup_root}")
    print(f"Plan id: {plan_id}")
    print(f"SQLite field replacements: {sqlite_occurrences}")
    print(f"Updated rollout records: {rollout_changed}")
    return 0


def should_apply(args: argparse.Namespace) -> bool:
    return bool(args.apply and not args.dry_run)


def backup_dir(backup_root: Path, label: str) -> Path:
    timestamp = dt.datetime.now().strftime("%Y%m%dT%H%M%S")
    path = backup_root.expanduser().resolve() / f"{timestamp}-{label}"
    path.mkdir(parents=True, exist_ok=False)
    return path


def backup_database(db_path: Path, target_dir: Path) -> Path:
    destination = target_dir / "state_5.before.sqlite"
    shutil.copy2(db_path, destination)
    return destination


def backup_rollouts(codex_home: Path, rollout_paths: list[Path], target_dir: Path) -> Path:
    tar_path = target_dir / "rollouts-before.tar.gz"
    manifest_path = target_dir / "rollout-files.txt"
    manifest_path.write_text("\n".join(str(path) for path in rollout_paths) + "\n", encoding="utf-8")
    resolved_home = codex_home.resolve()
    with tarfile.open(tar_path, "w:gz") as archive:
        for rollout_path in rollout_paths:
            resolved_rollout = rollout_path.resolve()
            try:
                arcname = str(resolved_rollout.relative_to(resolved_home))
            except ValueError:
                arcname = rollout_path.name
            archive.add(rollout_path, arcname=arcname)
    return tar_path


def rewrite_jsonl_file(
    source_path: Path,
    destination_path: Path,
    transform: Callable[[dict[str, Any]], dict[str, Any] | None],
) -> int:
    changed = 0
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    with source_path.open("r", encoding="utf-8") as source, destination_path.open("w", encoding="utf-8") as dest:
        for line_no, raw_line in enumerate(source, start=1):
            try:
                record = json.loads(raw_line)
            except json.JSONDecodeError as exc:
                raise CodexHistoryError(f"Invalid JSON in {source_path}:{line_no}: {exc}") from exc
            before = json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            updated = transform(record)
            if updated is None:
                continue
            after = json.dumps(updated, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            if after != before:
                changed += 1
            dest.write(json.dumps(updated, ensure_ascii=False, separators=(",", ":")) + "\n")
    return changed


def replace_in_place(path: Path, transform: Callable[[dict[str, Any]], dict[str, Any] | None]) -> int:
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False, dir=path.parent) as temp_file:
        temp_path = Path(temp_file.name)
    changed = rewrite_jsonl_file(path, temp_path, transform)
    temp_path.replace(path)
    return changed


def validate_target_cwd(value: str) -> str:
    target = Path(value).expanduser().resolve()
    if not target.exists():
        raise CodexHistoryError(f"Target cwd does not exist: {target}")
    return str(target)


def unique_rollout_paths(threads: Iterable[ThreadRecord]) -> list[Path]:
    seen: dict[str, Path] = {}
    for thread in threads:
        seen[str(thread.rollout_path)] = thread.rollout_path
    return list(seen.values())


def summarize_threads(threads: list[ThreadRecord]) -> tuple[int, int]:
    return len(threads), len(unique_rollout_paths(threads))


def print_thread_batch_summary(label: str, threads: list[ThreadRecord]) -> None:
    thread_count, rollout_count = summarize_threads(threads)
    print(f"{label}: {thread_count} threads across {rollout_count} rollout files")


def load_threads_for_workspace(conn: sqlite3.Connection, cwd: str) -> list[ThreadRecord]:
    threads = fetch_threads(conn, cwd=cwd)
    if not threads:
        raise CodexHistoryError(f"No threads found for workspace: {cwd}")
    return threads


def update_threads_cwd(conn: sqlite3.Connection, thread_ids: list[str], target_cwd: str) -> None:
    if not thread_ids:
        return
    updated_at = now_timestamp()
    conn.executemany(
        "update threads set cwd = ?, updated_at = ? where id = ?",
        [(target_cwd, updated_at, thread_id) for thread_id in thread_ids],
    )
    conn.commit()


def update_threads_provider(
    conn: sqlite3.Connection,
    thread_ids: list[str],
    provider: str,
    model: str | None,
) -> None:
    if not thread_ids:
        return
    updated_at = now_timestamp()
    if model:
        conn.executemany(
            "update threads set model_provider = ?, model = ?, updated_at = ? where id = ?",
            [(provider, model, updated_at, thread_id) for thread_id in thread_ids],
        )
    else:
        conn.executemany(
            "update threads set model_provider = ?, updated_at = ? where id = ?",
            [(provider, updated_at, thread_id) for thread_id in thread_ids],
        )
    conn.commit()


def update_rollouts_for_cwd(rollout_paths: Iterable[Path], target_cwd: str) -> int:
    changed = 0
    for rollout_path in rollout_paths:
        def transform(record: dict[str, Any]) -> dict[str, Any]:
            if record.get("type") == "session_meta":
                payload = record.get("payload")
                if isinstance(payload, dict):
                    payload["cwd"] = target_cwd
            return record

        changed += replace_in_place(rollout_path, transform)
    return changed


def update_rollouts_for_provider(rollout_paths: Iterable[Path], provider: str, model: str | None) -> int:
    changed = 0
    for rollout_path in rollout_paths:
        def transform(record: dict[str, Any]) -> dict[str, Any]:
            if record.get("type") == "session_meta":
                payload = record.get("payload")
                if isinstance(payload, dict):
                    payload["model_provider"] = provider
                    if model:
                        payload["model"] = model
            if record.get("type") == "turn_context" and model:
                payload = record.get("payload")
                if isinstance(payload, dict):
                    payload["model"] = model
            return record

        changed += replace_in_place(rollout_path, transform)
    return changed


def command_move_thread(args: argparse.Namespace) -> int:
    codex_home, db_path = ensure_codex_home(args.codex_home)
    target_cwd = validate_target_cwd(args.to_cwd)
    apply_changes = should_apply(args)

    with connect_db(db_path) as conn:
        thread = fetch_thread(conn, args.id)
    rollout_paths = unique_rollout_paths([thread])

    print(f"Plan: move thread {thread.id}")
    print(f"  from cwd: {thread.cwd}")
    print(f"  to cwd:   {target_cwd}")
    print(f"  rollout:  {thread.rollout_path}")
    if not apply_changes:
        print("Dry run only. Re-run with --apply to perform the move.")
        return 0

    backup_root = backup_dir(args.backup_root, f"move-thread-{thread.id}")
    backup_database(db_path, backup_root)
    backup_rollouts(codex_home, rollout_paths, backup_root)

    with connect_db(db_path) as conn:
        update_threads_cwd(conn, [thread.id], target_cwd)

    changed = update_rollouts_for_cwd(rollout_paths, target_cwd)
    print(f"Applied move. Backup: {backup_root}")
    print(f"Updated rollout records: {changed}")
    return 0


def now_timestamp() -> int:
    return int(dt.datetime.now(tz=dt.timezone.utc).timestamp())


def clone_rollout_path(codex_home: Path, new_id: str) -> Path:
    now = dt.datetime.now()
    target_dir = codex_home / "sessions" / now.strftime("%Y") / now.strftime("%m") / now.strftime("%d")
    filename = f"rollout-{now.strftime('%Y-%m-%dT%H-%M-%S')}-{new_id}.jsonl"
    return target_dir / filename


def clone_threads(
    conn: sqlite3.Connection,
    codex_home: Path,
    source_threads: list[ThreadRecord],
    target_cwd: str,
    unarchive: bool,
) -> tuple[list[str], int]:
    inserted_ids: list[str] = []
    changed_records = 0
    for source_thread in source_threads:
        new_id = str(uuid.uuid4())
        new_rollout_path = clone_rollout_path(codex_home, new_id)
        archived_value = 0 if unarchive else source_thread.archived
        archived_at = None if archived_value == 0 else source_thread.archived_at

        def transform(record: dict[str, Any]) -> dict[str, Any]:
            if record.get("type") == "session_meta":
                payload = record.get("payload")
                if isinstance(payload, dict):
                    payload["id"] = new_id
                    payload["cwd"] = target_cwd
                    payload["timestamp"] = dt.datetime.now(tz=dt.timezone.utc).isoformat().replace("+00:00", "Z")
            return record

        changed_records += rewrite_jsonl_file(source_thread.rollout_path, new_rollout_path, transform)

        row = source_thread.to_dict()
        row.update(
            {
                "id": new_id,
                "rollout_path": str(new_rollout_path),
                "cwd": target_cwd,
                "created_at": now_timestamp(),
                "updated_at": now_timestamp(),
                "archived": archived_value,
                "archived_at": archived_at,
            }
        )
        columns = list(row.keys())
        placeholders = ", ".join("?" for _ in columns)
        conn.execute(
            f"insert into threads ({', '.join(columns)}) values ({placeholders})",
            [row[column] for column in columns],
        )
        inserted_ids.append(new_id)
    conn.commit()
    return inserted_ids, changed_records


def command_clone_thread(args: argparse.Namespace) -> int:
    codex_home, db_path = ensure_codex_home(args.codex_home)
    target_cwd = validate_target_cwd(args.to_cwd)
    apply_changes = should_apply(args)

    with connect_db(db_path) as conn:
        source_thread = fetch_thread(conn, args.id)

    print(f"Plan: clone thread {source_thread.id}")
    print(f"  new cwd:  {target_cwd}")
    print(f"  source rollout: {source_thread.rollout_path}")
    print(f"  unarchive clones: {bool(args.unarchive)}")
    if not apply_changes:
        print("Dry run only. Re-run with --apply to perform the clone.")
        return 0

    backup_root = backup_dir(args.backup_root, f"clone-thread-{source_thread.id}")
    backup_database(db_path, backup_root)
    backup_rollouts(codex_home, [source_thread.rollout_path], backup_root)

    with connect_db(db_path) as conn:
        inserted_ids, changed = clone_threads(conn, codex_home, [source_thread], target_cwd, args.unarchive)

    print(f"Applied clone. Backup: {backup_root}")
    print(f"New thread id: {inserted_ids[0]}")
    print(f"Written rollout records: {changed}")
    return 0


def command_change_provider(args: argparse.Namespace) -> int:
    codex_home, db_path = ensure_codex_home(args.codex_home)
    apply_changes = should_apply(args)

    with connect_db(db_path) as conn:
        thread = fetch_thread(conn, args.id)
    rollout_paths = unique_rollout_paths([thread])

    print(f"Plan: change provider for thread {thread.id}")
    print(f"  from provider: {thread.model_provider}")
    print(f"  to provider:   {args.provider}")
    if args.model:
        print(f"  set model:     {args.model}")
    print(f"  rollout:       {thread.rollout_path}")
    if not apply_changes:
        print("Dry run only. Re-run with --apply to perform the change.")
        return 0

    backup_root = backup_dir(args.backup_root, f"change-provider-{thread.id}")
    backup_database(db_path, backup_root)
    backup_rollouts(codex_home, rollout_paths, backup_root)

    with connect_db(db_path) as conn:
        update_threads_provider(conn, [thread.id], args.provider, args.model)

    changed = update_rollouts_for_provider(rollout_paths, args.provider, args.model)
    print(f"Applied provider change. Backup: {backup_root}")
    print(f"Updated rollout records: {changed}")
    return 0


def command_move_workspace(args: argparse.Namespace) -> int:
    codex_home, db_path = ensure_codex_home(args.codex_home)
    source_cwd = str(Path(args.cwd).expanduser().resolve())
    target_cwd = validate_target_cwd(args.to_cwd)
    apply_changes = should_apply(args)

    with connect_db(db_path) as conn:
        threads = load_threads_for_workspace(conn, source_cwd)
    rollout_paths = unique_rollout_paths(threads)

    print("Plan: move workspace threads")
    print(f"  from cwd: {source_cwd}")
    print(f"  to cwd:   {target_cwd}")
    print_thread_batch_summary("  scope", threads)
    if not apply_changes:
        print("Dry run only. Re-run with --apply to perform the move.")
        return 0

    backup_root = backup_dir(args.backup_root, "move-workspace")
    backup_database(db_path, backup_root)
    backup_rollouts(codex_home, rollout_paths, backup_root)

    with connect_db(db_path) as conn:
        update_threads_cwd(conn, [thread.id for thread in threads], target_cwd)

    changed = update_rollouts_for_cwd(rollout_paths, target_cwd)
    print(f"Applied workspace move. Backup: {backup_root}")
    print(f"Updated rollout records: {changed}")
    return 0


def command_clone_workspace(args: argparse.Namespace) -> int:
    codex_home, db_path = ensure_codex_home(args.codex_home)
    source_cwd = str(Path(args.cwd).expanduser().resolve())
    target_cwd = validate_target_cwd(args.to_cwd)
    apply_changes = should_apply(args)

    with connect_db(db_path) as conn:
        threads = load_threads_for_workspace(conn, source_cwd)
    rollout_paths = unique_rollout_paths(threads)

    print("Plan: clone workspace threads")
    print(f"  from cwd: {source_cwd}")
    print(f"  to cwd:   {target_cwd}")
    print(f"  unarchive clones: {bool(args.unarchive)}")
    print_thread_batch_summary("  scope", threads)
    if not apply_changes:
        print("Dry run only. Re-run with --apply to perform the clone.")
        return 0

    backup_root = backup_dir(args.backup_root, "clone-workspace")
    backup_database(db_path, backup_root)
    backup_rollouts(codex_home, rollout_paths, backup_root)

    with connect_db(db_path) as conn:
        inserted_ids, changed = clone_threads(conn, codex_home, threads, target_cwd, args.unarchive)

    print(f"Applied workspace clone. Backup: {backup_root}")
    print(f"Cloned threads: {len(inserted_ids)}")
    print(f"Written rollout records: {changed}")
    return 0


def command_change_provider_workspace(args: argparse.Namespace) -> int:
    codex_home, db_path = ensure_codex_home(args.codex_home)
    source_cwd = str(Path(args.cwd).expanduser().resolve())
    apply_changes = should_apply(args)

    with connect_db(db_path) as conn:
        threads = load_threads_for_workspace(conn, source_cwd)
    rollout_paths = unique_rollout_paths(threads)

    print("Plan: change provider for workspace threads")
    print(f"  cwd:      {source_cwd}")
    print(f"  provider: {args.provider}")
    if args.model:
        print(f"  model:    {args.model}")
    print_thread_batch_summary("  scope", threads)
    if not apply_changes:
        print("Dry run only. Re-run with --apply to perform the change.")
        return 0

    backup_root = backup_dir(args.backup_root, "change-provider-workspace")
    backup_database(db_path, backup_root)
    backup_rollouts(codex_home, rollout_paths, backup_root)

    with connect_db(db_path) as conn:
        update_threads_provider(conn, [thread.id for thread in threads], args.provider, args.model)

    changed = update_rollouts_for_provider(rollout_paths, args.provider, args.model)
    print(f"Applied workspace provider change. Backup: {backup_root}")
    print(f"Updated rollout records: {changed}")
    return 0


def command_change_provider_all(args: argparse.Namespace) -> int:
    codex_home, db_path = ensure_codex_home(args.codex_home)
    apply_changes = should_apply(args)

    with connect_db(db_path) as conn:
        threads = fetch_threads(conn)
    if not threads:
        raise CodexHistoryError("No local Codex threads found.")
    rollout_paths = unique_rollout_paths(threads)

    print("Plan: change provider for all local threads")
    print(f"  provider: {args.provider}")
    if args.model:
        print(f"  model:    {args.model}")
    print_thread_batch_summary("  scope", threads)
    if not apply_changes:
        print("Dry run only. Re-run with --apply to perform the change.")
        return 0

    backup_root = backup_dir(args.backup_root, "change-provider-all")
    backup_database(db_path, backup_root)
    backup_rollouts(codex_home, rollout_paths, backup_root)

    with connect_db(db_path) as conn:
        update_threads_provider(conn, [thread.id for thread in threads], args.provider, args.model)

    changed = update_rollouts_for_provider(rollout_paths, args.provider, args.model)
    print(f"Applied global provider change. Backup: {backup_root}")
    print(f"Updated rollout records: {changed}")
    return 0


def dispatch(args: argparse.Namespace) -> int:
    command = args.command
    if command == "search":
        return command_search(args)
    if command == "show-thread":
        return command_show_thread(args)
    if command == "export-thread":
        return command_export_thread(args)
    if command == "handoff":
        return command_handoff(args)
    if command == "plan-dangerous-edit":
        return command_plan_dangerous_edit(args)
    if command == "apply-dangerous-edit":
        return command_apply_dangerous_edit(args)
    if command == "move-thread":
        return command_move_thread(args)
    if command == "move-workspace":
        return command_move_workspace(args)
    if command == "clone-thread":
        return command_clone_thread(args)
    if command == "clone-workspace":
        return command_clone_workspace(args)
    if command == "change-provider":
        return command_change_provider(args)
    if command == "change-provider-workspace":
        return command_change_provider_workspace(args)
    if command == "change-provider-all":
        return command_change_provider_all(args)
    raise CodexHistoryError(f"Unsupported command: {command}")


def main() -> int:
    args = parse_args()
    try:
        return dispatch(args)
    except CodexHistoryError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
