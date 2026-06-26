#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import date, datetime, time
from pathlib import Path
from typing import Any


CODEX_HOME = Path.home() / ".codex"
INDEX_PATH = CODEX_HOME / "session_index.jsonl"
ACTIVE_SESSIONS_DIR = CODEX_HOME / "sessions"
ARCHIVED_SESSIONS_DIR = CODEX_HOME / "archived_sessions"
DEFAULT_LIMIT = 20
TITLE_LIMIT = 72
DEFAULT_SOURCE = "active"


@dataclass(slots=True)
class IndexEntry:
    thread_name: str | None
    updated_at: str | None


@dataclass(slots=True)
class SessionRecord:
    id: str
    title: str
    updated_at: str
    started_at: str
    matched_from: str | None
    matched_to: str | None
    source: str
    cwd: str
    project: str
    project_path: str
    session_file: str
    first_user_message: str | None


def load_history_titles() -> dict[str, str]:
    history_path = CODEX_HOME / "history.jsonl"
    titles: dict[str, str] = {}
    if not history_path.exists():
        return titles

    with history_path.open() as handle:
        for raw_line in handle:
            raw_line = raw_line.strip()
            if not raw_line:
                continue
            try:
                row = json.loads(raw_line)
            except json.JSONDecodeError:
                continue

            session_id = row.get("session_id")
            text = row.get("text")
            if not isinstance(session_id, str) or not isinstance(text, str):
                continue
            if session_id in titles:
                continue

            normalized = normalize_user_message(text)
            if normalized:
                titles[session_id] = normalized

    return titles


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="List local Codex sessions with ids and project information.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=DEFAULT_LIMIT,
        help="Maximum number of sessions to print in table mode. Use 0 for no limit.",
    )
    parser.add_argument(
        "--project",
        default="",
        help="Filter by project name, project path, or cwd substring.",
    )
    parser.add_argument(
        "--session-id",
        default="",
        help="Filter to one exact session id.",
    )
    parser.add_argument(
        "--contains",
        default="",
        help="Filter by title or first user message substring.",
    )
    parser.add_argument(
        "--source",
        choices=("all", "active", "archived"),
        default=DEFAULT_SOURCE,
        help="Choose which session store to scan. Defaults to unarchived active sessions.",
    )
    parser.add_argument(
        "--date",
        default="",
        help="Anchor date for time-only filters like 11:00. Defaults to today in local time.",
    )
    parser.add_argument(
        "--from",
        dest="time_from",
        default="",
        help="Filter sessions that overlap the start of a local time window.",
    )
    parser.add_argument(
        "--to",
        dest="time_to",
        default="",
        help="Filter sessions that overlap the end of a local time window.",
    )
    parser.add_argument(
        "--details",
        action="store_true",
        help="Print one block per session with full details.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Return JSON instead of formatted text.",
    )
    return parser.parse_args()


def load_index() -> dict[str, IndexEntry]:
    index: dict[str, IndexEntry] = {}
    if not INDEX_PATH.exists():
        return index

    for raw_line in INDEX_PATH.read_text().splitlines():
        raw_line = raw_line.strip()
        if not raw_line:
            continue
        try:
            payload = json.loads(raw_line)
        except json.JSONDecodeError:
            continue

        session_id = payload.get("id")
        if not isinstance(session_id, str) or not session_id:
            continue

        thread_name = payload.get("thread_name")
        updated_at = payload.get("updated_at")
        index[session_id] = IndexEntry(
            thread_name=thread_name if isinstance(thread_name, str) else None,
            updated_at=updated_at if isinstance(updated_at, str) else None,
        )
    return index


def iter_session_files(source: str) -> list[tuple[str, Path]]:
    files: list[tuple[str, Path]] = []

    if source in {"all", "active"} and ACTIVE_SESSIONS_DIR.exists():
        for path in ACTIVE_SESSIONS_DIR.rglob("*.jsonl"):
            files.append(("active", path))

    if source in {"all", "archived"} and ARCHIVED_SESSIONS_DIR.exists():
        for path in ARCHIVED_SESSIONS_DIR.glob("*.jsonl"):
            files.append(("archived", path))

    return files


def parse_text_content(content: Any) -> str | None:
    if not isinstance(content, list):
        return None

    parts: list[str] = []
    for item in content:
        if not isinstance(item, dict):
            continue
        if item.get("type") not in {"input_text", "output_text", "text"}:
            continue
        text = item.get("text")
        if isinstance(text, str) and text.strip():
            parts.append(text.strip())

    if not parts:
        return None
    return " ".join(parts)


def compact_text(text: str | None, limit: int = TITLE_LIMIT) -> str | None:
    if text is None:
        return None

    compacted = " ".join(text.split())
    if not compacted:
        return None
    if len(compacted) <= limit:
        return compacted
    return f"{compacted[: limit - 3]}..."


def local_timezone() -> datetime.tzinfo:
    return datetime.now().astimezone().tzinfo


def parse_session_timestamp(value: str | None) -> datetime | None:
    if not value:
        return None

    normalized = value.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return None

    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=local_timezone())
    return parsed.astimezone(local_timezone())


def format_session_timestamp(value: str | None) -> str:
    parsed = parse_session_timestamp(value)
    if parsed is None:
        return value or ""
    return parsed.isoformat(timespec="seconds")


def parse_anchor_date(value: str) -> date | None:
    if not value:
        return datetime.now().astimezone().date()

    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def parse_time_filter(
    value: str,
    *,
    anchor_date: date,
    is_end: bool,
) -> datetime | None:
    if not value:
        return None

    normalized = value.strip()
    if not normalized:
        return None

    candidates = [
        "%Y-%m-%dT%H:%M",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
        "%H:%M",
        "%H:%M:%S",
    ]
    parsed: datetime | None = None
    for fmt in candidates:
        try:
            parsed = datetime.strptime(normalized, fmt)
            break
        except ValueError:
            continue

    if parsed is None:
        return None

    if normalized.count("-") == 2 and "T" not in normalized and " " not in normalized:
        boundary_time = time(23, 59, 59) if is_end else time(0, 0, 0)
        parsed = datetime.combine(parsed.date(), boundary_time)
    elif normalized.count(":") in {1, 2} and normalized.count("-") == 0:
        parsed = datetime.combine(anchor_date, parsed.time())

    return parsed.replace(tzinfo=local_timezone())


def normalize_user_message(text: str | None) -> str | None:
    compacted = compact_text(text, 400)
    if compacted is None:
        return None

    markers = [
        "## My request for Codex:",
        "My request for Codex:",
        "## My request:",
        "My request:",
    ]
    for marker in markers:
        if marker in compacted:
            compacted = compacted.split(marker, 1)[1].strip()
            break

    if compacted.startswith("# AGENTS.md instructions for "):
        return None

    return compact_text(compacted)


def derive_project_root(cwd_text: str | None) -> tuple[str, str]:
    if not cwd_text:
        return "", ""

    cwd = Path(cwd_text).expanduser()
    search_points = [cwd, *cwd.parents]

    for candidate in search_points:
        git_marker = candidate / ".git"
        if git_marker.exists():
            return candidate.name, str(candidate)

    return cwd.name, str(cwd)


def extract_session_record(
    session_file: Path,
    source: str,
    index: dict[str, IndexEntry],
    history_titles: dict[str, str],
    time_from: datetime | None,
    time_to: datetime | None,
) -> SessionRecord | None:
    session_id: str | None = None
    started_at = ""
    updated_at = ""
    cwd = ""
    first_user_message: str | None = None
    matched_from: str | None = None
    matched_to: str | None = None

    with session_file.open() as handle:
        for raw_line in handle:
            raw_line = raw_line.strip()
            if not raw_line:
                continue
            try:
                row = json.loads(raw_line)
            except json.JSONDecodeError:
                continue

            timestamp = row.get("timestamp")
            if isinstance(timestamp, str):
                updated_at = timestamp
                parsed_timestamp = parse_session_timestamp(timestamp)
                if parsed_timestamp is not None and (time_from or time_to):
                    if time_from and parsed_timestamp < time_from:
                        pass
                    elif time_to and parsed_timestamp > time_to:
                        pass
                    else:
                        matched_timestamp = parsed_timestamp.isoformat(timespec="seconds")
                        if matched_from is None:
                            matched_from = matched_timestamp
                        matched_to = matched_timestamp

            row_type = row.get("type")
            payload = row.get("payload")

            if row_type == "session_meta" and isinstance(payload, dict):
                payload_id = payload.get("id")
                if isinstance(payload_id, str):
                    session_id = payload_id
                payload_timestamp = payload.get("timestamp")
                if isinstance(payload_timestamp, str):
                    started_at = payload_timestamp
                payload_cwd = payload.get("cwd")
                if isinstance(payload_cwd, str):
                    cwd = payload_cwd
                continue

            if row_type == "turn_context" and isinstance(payload, dict) and not cwd:
                payload_cwd = payload.get("cwd")
                if isinstance(payload_cwd, str):
                    cwd = payload_cwd

            if first_user_message is not None:
                continue

            if row_type == "event_msg" and isinstance(payload, dict):
                if payload.get("type") == "user_message":
                    message = payload.get("message")
                    if isinstance(message, str):
                        normalized = normalize_user_message(message)
                        if normalized:
                            first_user_message = normalized
                        continue

            if row_type == "response_item" and isinstance(payload, dict):
                if payload.get("type") == "message" and payload.get("role") == "user":
                    normalized = normalize_user_message(parse_text_content(payload.get("content")))
                    if normalized:
                        first_user_message = normalized

    if not session_id:
        return None
    if (time_from or time_to) and matched_from is None:
        return None

    index_entry = index.get(session_id)
    title = None
    if index_entry is not None:
        title = compact_text(index_entry.thread_name)

    if title is None:
        title = history_titles.get(session_id) or first_user_message or session_id

    if index_entry is not None and index_entry.updated_at:
        updated_at = index_entry.updated_at

    project, project_path = derive_project_root(cwd)

    return SessionRecord(
        id=session_id,
        title=title,
        updated_at=format_session_timestamp(updated_at or started_at),
        started_at=format_session_timestamp(started_at),
        matched_from=matched_from,
        matched_to=matched_to,
        source=source,
        cwd=cwd,
        project=project,
        project_path=project_path,
        session_file=str(session_file),
        first_user_message=first_user_message,
    )


def collect_sessions(args: argparse.Namespace) -> list[SessionRecord]:
    anchor_date = parse_anchor_date(args.date)
    if args.date and anchor_date is None:
        raise SystemExit("--date must use YYYY-MM-DD format.")

    if anchor_date is None:
        anchor_date = datetime.now().astimezone().date()

    time_from = parse_time_filter(args.time_from, anchor_date=anchor_date, is_end=False)
    if args.time_from and time_from is None:
        raise SystemExit("--from must use YYYY-MM-DD, YYYY-MM-DDTHH:MM, or HH:MM.")

    time_to = parse_time_filter(args.time_to, anchor_date=anchor_date, is_end=True)
    if args.time_to and time_to is None:
        raise SystemExit("--to must use YYYY-MM-DD, YYYY-MM-DDTHH:MM, or HH:MM.")

    if time_from and time_to and time_from > time_to:
        raise SystemExit("--from must be earlier than or equal to --to.")

    index = load_index()
    history_titles = load_history_titles()
    records: dict[str, SessionRecord] = {}

    for source, session_file in iter_session_files(args.source):
        record = extract_session_record(
            session_file,
            source,
            index,
            history_titles,
            time_from,
            time_to,
        )
        if record is None:
            continue

        existing = records.get(record.id)
        if existing is None or existing.source == "archived":
            records[record.id] = record

    sessions = list(records.values())
    sessions.sort(
        key=lambda item: (
            parse_session_timestamp(item.matched_to or item.updated_at)
            or datetime.min.replace(tzinfo=local_timezone()),
            parse_session_timestamp(item.matched_from or item.started_at)
            or datetime.min.replace(tzinfo=local_timezone()),
            item.id,
        ),
        reverse=True,
    )

    project_filter = args.project.lower().strip()
    if project_filter:
        sessions = [
            item
            for item in sessions
            if project_filter in item.project.lower()
            or project_filter in item.project_path.lower()
            or project_filter in item.cwd.lower()
        ]

    contains_filter = args.contains.lower().strip()
    if contains_filter:
        sessions = [
            item
            for item in sessions
            if contains_filter in item.title.lower()
            or contains_filter in (item.first_user_message or "").lower()
        ]

    session_id_filter = args.session_id.strip()
    if session_id_filter:
        sessions = [item for item in sessions if item.id == session_id_filter]

    if not args.json and not args.details and args.limit > 0:
        sessions = sessions[: args.limit]

    return sessions


def render_table(records: list[SessionRecord]) -> str:
    if not records:
        return "No matching Codex sessions found."

    headers = {
        "id": "ID",
        "project": "PROJECT",
        "source": "SOURCE",
        "title": "TITLE",
    }
    if any(item.matched_from or item.matched_to for item in records):
        headers["matched_from"] = "MATCHED_FROM"
        headers["matched_to"] = "MATCHED_TO"
    headers["started_at"] = "STARTED_AT"
    headers["updated_at"] = "UPDATED_AT"

    rows = []
    for item in records:
        rows.append(
            {
                "id": item.id,
                "project": item.project or "-",
                "source": item.source,
                "title": compact_text(item.title, TITLE_LIMIT) or "-",
                "matched_from": item.matched_from or "-",
                "matched_to": item.matched_to or "-",
                "started_at": item.started_at or "-",
                "updated_at": item.updated_at or "-",
            }
        )

    widths = {
        key: max(len(headers[key]), *(len(row[key]) for row in rows))
        for key in headers
    }

    lines = []
    header_line = "  ".join(f"{headers[key]:<{widths[key]}}" for key in headers)
    separator_line = "  ".join("-" * widths[key] for key in headers)
    lines.append(header_line)
    lines.append(separator_line)

    for row in rows:
        lines.append("  ".join(f"{row[key]:<{widths[key]}}" for key in headers))

    return "\n".join(lines)


def render_details(records: list[SessionRecord]) -> str:
    if not records:
        return "No matching Codex sessions found."

    blocks = []
    for item in records:
        block = [
            f"id: {item.id}",
            f"title: {item.title}",
            f"project: {item.project or '-'}",
            f"project_path: {item.project_path or '-'}",
            f"cwd: {item.cwd or '-'}",
            f"source: {item.source}",
            f"matched_from: {item.matched_from or '-'}",
            f"matched_to: {item.matched_to or '-'}",
            f"started_at: {item.started_at or '-'}",
            f"updated_at: {item.updated_at or '-'}",
            f"session_file: {item.session_file}",
            f"first_user_message: {item.first_user_message or '-'}",
        ]
        blocks.append("\n".join(block))

    return "\n\n".join(blocks)


def main() -> None:
    args = parse_args()
    sessions = collect_sessions(args)

    if args.limit > 0 and (args.json or args.details):
        sessions = sessions[: args.limit]

    if args.json:
        print(
            json.dumps(
                [asdict(item) for item in sessions],
                ensure_ascii=False,
                indent=2,
            )
        )
        return

    if args.details:
        print(render_details(sessions))
        return

    print(render_table(sessions))


if __name__ == "__main__":
    main()
