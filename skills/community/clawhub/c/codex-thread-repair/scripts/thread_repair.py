#!/usr/bin/env python3
"""Diagnose and repair one local Codex rollout selected by title or thread ID."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shlex
import shutil
import sqlite3
import subprocess
import sys
import tempfile
from collections import Counter
from contextlib import contextmanager
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Iterator


APP_PATTERN = re.compile(
    r"/Applications/ChatGPT\.app/Contents/"
    r"(?:MacOS/ChatGPT|Resources/codex.*app-server|Frameworks/.*Codex)"
)
ORDINAL_PATTERN = re.compile(r'("ordinal"\s*:\s*)(\d+)', re.ASCII)
SAFE_THREAD_ID_PATTERN = re.compile(r"^[A-Za-z0-9._-]+$")


class RepairError(RuntimeError):
    pass


class AmbiguousSelector(RepairError):
    def __init__(self, selector: str, candidates: list[dict[str, Any]]) -> None:
        super().__init__(f"Selector is ambiguous: {selector}")
        self.selector = selector
        self.candidates = candidates


def default_codex_home() -> Path:
    configured = os.environ.get("CODEX_HOME")
    return Path(configured).expanduser() if configured else Path.home() / ".codex"


@contextmanager
def connect_readonly(path: Path) -> Iterator[sqlite3.Connection]:
    if not path.is_file():
        raise RepairError(f"Database not found: {path}")
    connection = sqlite3.connect(f"{path.resolve().as_uri()}?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    try:
        yield connection
    finally:
        connection.close()


def table_columns(connection: sqlite3.Connection, table: str) -> set[str]:
    return {row[1] for row in connection.execute(f"PRAGMA table_info({table})")}


def load_threads(codex_home: Path) -> list[dict[str, Any]]:
    state_db = codex_home / "state_5.sqlite"
    with connect_readonly(state_db) as connection:
        required = {"id", "title", "rollout_path", "cwd", "updated_at", "archived"}
        available = table_columns(connection, "threads")
        missing = required - available
        if missing:
            raise RepairError(f"Unsupported threads schema; missing columns: {sorted(missing)}")
        rows = connection.execute(
            "SELECT id,title,rollout_path,cwd,updated_at,archived FROM threads"
        ).fetchall()

    catalog_titles: dict[str, str] = {}
    catalog_db = codex_home / "sqlite" / "codex-dev.db"
    if catalog_db.is_file():
        with connect_readonly(catalog_db) as connection:
            columns = table_columns(connection, "local_thread_catalog")
            if {"thread_id", "display_title", "missing_candidate"} <= columns:
                for row in connection.execute(
                    "SELECT thread_id,display_title FROM local_thread_catalog WHERE missing_candidate=0"
                ):
                    catalog_titles[row["thread_id"]] = row["display_title"]

    result = []
    for row in rows:
        item = dict(row)
        item["display_title"] = catalog_titles.get(item["id"])
        result.append(item)
    return result


def public_thread(thread: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": thread["id"],
        "display_title": thread.get("display_title"),
        "source_title": thread.get("title"),
        "cwd": thread.get("cwd"),
        "rollout_path": thread.get("rollout_path"),
        "updated_at": thread.get("updated_at"),
        "archived": bool(thread.get("archived")),
    }


def confine_rollout_path(codex_home: Path, thread: dict[str, Any]) -> dict[str, Any]:
    """Return a copy whose rollout path is proven to stay inside this Codex home."""
    raw_path = thread.get("rollout_path")
    if not isinstance(raw_path, str) or not raw_path:
        raise RepairError(f"Thread {thread.get('id')} has no rollout path")
    candidate = Path(raw_path).expanduser()
    if not candidate.is_absolute():
        raise RepairError(f"Thread rollout path is not absolute: {candidate}")
    resolved = candidate.resolve()
    sessions_root = (codex_home / "sessions").resolve()
    try:
        resolved.relative_to(sessions_root)
    except ValueError as error:
        raise RepairError(f"Thread rollout path is outside Codex sessions: {resolved}") from error
    return {**thread, "rollout_path": str(resolved)}


def resolve_thread(codex_home: Path, selector: str) -> dict[str, Any]:
    selector = selector.strip()
    if not selector:
        raise RepairError("A non-empty title or thread ID is required")
    threads = load_threads(codex_home)
    folded = selector.casefold()

    def choose(matches: list[dict[str, Any]]) -> dict[str, Any] | None:
        values = list({item["id"]: item for item in matches}.values())
        if len(values) == 1:
            return values[0]
        if len(values) > 1:
            values.sort(key=lambda item: (-(item.get("updated_at") or 0), item["id"]))
            raise AmbiguousSelector(selector, [public_thread(item) for item in values])
        return None

    matched = choose([item for item in threads if item["id"].casefold() == folded])
    if matched:
        return confine_rollout_path(codex_home, matched)
    matched = choose(
        [
            item
            for item in threads
            if folded
            in {
                (item.get("display_title") or "").casefold(),
                (item.get("title") or "").casefold(),
            }
        ]
    )
    if matched:
        return confine_rollout_path(codex_home, matched)
    matched = choose(
        [
            item
            for item in threads
            if folded in (item.get("display_title") or "").casefold()
            or folded in (item.get("title") or "").casefold()
        ]
    )
    if matched:
        return confine_rollout_path(codex_home, matched)
    raise RepairError(f"No local Codex task matched: {selector}")


def desktop_running() -> bool:
    try:
        result = subprocess.run(
            ["/bin/ps", "-axo", "command="], check=True, capture_output=True, text=True
        )
    except (OSError, subprocess.CalledProcessError) as error:
        raise RepairError(f"Could not check whether Codex is running: {error}") from error
    return any(APP_PATTERN.search(line) for line in result.stdout.splitlines())


def parse_timestamp(value: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (AttributeError, TypeError, ValueError) as error:
        raise RepairError(f"Invalid timestamp: {value!r}") from error
    if parsed.tzinfo is None:
        raise RepairError(f"Timestamp has no timezone: {value!r}")
    return parsed


def collect_turn_ids(value: Any) -> set[str]:
    """Collect non-empty values of every nested `turn_id` key."""
    found: set[str] = set()
    if isinstance(value, dict):
        for key, child in value.items():
            if key == "turn_id" and isinstance(child, str) and child:
                found.add(child)
            found.update(collect_turn_ids(child))
    elif isinstance(value, list):
        for child in value:
            found.update(collect_turn_ids(child))
    return found


def replace_top_level_ordinal(raw: str, expected: int, replacement: str | int) -> str:
    """Replace the serialized top-level ordinal only after proving it matches the parsed value."""
    match = ORDINAL_PATTERN.search(raw)
    if not match:
        raise RepairError("Serialized record has no ordinal field")
    if int(match.group(2)) != expected:
        raise RepairError("The first serialized ordinal is not the parsed top-level ordinal")
    return f"{raw[:match.start(2)]}{replacement}{raw[match.end(2):]}"


def inspect_rollout(thread: dict[str, Any]) -> dict[str, Any]:
    path = Path(thread.get("rollout_path") or "")
    if not path.is_file():
        return {
            "status": "missing_rollout",
            "supported": False,
            "reason": f"Rollout not found: {path}",
        }

    ordinals: list[tuple[int, int]] = []
    starts: dict[str, dict[str, Any]] = {}
    ends: dict[str, dict[str, Any]] = {}
    turn_refs: list[tuple[int, str]] = []
    lifecycle_errors: list[str] = []
    session_id = None
    line_count = 0

    try:
        with path.open("r", encoding="utf-8") as source:
            for line_no, raw in enumerate(source, 1):
                line_count = line_no
                record = json.loads(raw)
                if not isinstance(record, dict):
                    raise RepairError(f"Record {line_no} is not an object")
                ordinal = record.get("ordinal")
                if not isinstance(ordinal, int):
                    raise RepairError(f"Record {line_no} has no integer ordinal")
                ordinals.append((line_no, ordinal))
                payload = record.get("payload") or {}
                if record.get("type") == "session_meta":
                    session_id = payload.get("id")
                for turn_id in collect_turn_ids(payload):
                    turn_refs.append((line_no, turn_id))
                if record.get("type") == "event_msg" and payload.get("type") == "task_started":
                    turn_id = payload.get("turn_id")
                    if not isinstance(turn_id, str) or not turn_id:
                        lifecycle_errors.append(f"task_started at line {line_no} has no turn ID")
                        continue
                    if turn_id in starts:
                        lifecycle_errors.append(f"turn {turn_id} starts more than once")
                        continue
                    starts[turn_id] = {
                        "line": line_no,
                        "timestamp": record.get("timestamp"),
                        "started_at": payload.get("started_at"),
                    }
                if record.get("type") == "event_msg" and payload.get("type") in {
                    "task_complete",
                    "turn_aborted",
                }:
                    turn_id = payload.get("turn_id")
                    if not isinstance(turn_id, str) or not turn_id:
                        lifecycle_errors.append(
                            f"{payload.get('type')} at line {line_no} has no turn ID"
                        )
                        continue
                    if turn_id in ends:
                        lifecycle_errors.append(f"turn {turn_id} ends more than once")
                        continue
                    ends[turn_id] = {
                        "line": line_no,
                        "type": payload.get("type"),
                    }
    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        return {
            "status": "malformed_rollout",
            "supported": False,
            "reason": str(error),
            "rollout_path": str(path),
        }

    if session_id != thread["id"]:
        return {
            "status": "session_id_mismatch",
            "supported": False,
            "session_id": session_id,
            "expected_thread_id": thread["id"],
            "rollout_path": str(path),
        }

    breaks = []
    for previous, current in zip(ordinals, ordinals[1:]):
        if current[1] <= previous[1]:
            breaks.append({"previous": previous, "current": current})
    duplicate_ordinals = sorted(
        ordinal for ordinal, count in Counter(value for _, value in ordinals).items() if count > 1
    )
    open_turns = sorted(set(starts) - set(ends), key=lambda item: starts[item]["line"])
    stale_open_turns = [
        turn_id
        for turn_id in open_turns
        if any(start["line"] > starts[turn_id]["line"] for start in starts.values())
    ]
    current_open_turns = [item for item in open_turns if item not in stale_open_turns]
    base = {
        "rollout_path": str(path),
        "session_id": session_id,
        "records": line_count,
        "ordinal_min": ordinals[0][1] if ordinals else None,
        "ordinal_max": ordinals[-1][1] if ordinals else None,
        "non_monotonic_breaks": breaks,
        "duplicate_ordinals": duplicate_ordinals,
        "open_turns": open_turns,
        "stale_open_turns": stale_open_turns,
        "current_open_turns": current_open_turns,
        "lifecycle_errors": lifecycle_errors,
    }

    orphan_end_turns = sorted(set(ends) - set(starts))
    if orphan_end_turns:
        lifecycle_errors.append(f"turns end without starting: {orphan_end_turns}")
    if lifecycle_errors:
        return {
            **base,
            "lifecycle_errors": lifecycle_errors,
            "status": "unsupported",
            "supported": False,
            "reason": "Malformed or ambiguous turn lifecycle",
        }

    expected_contiguous = [(index + 1, index) for index in range(len(ordinals))]
    if ordinals == expected_contiguous and not open_turns:
        return {**base, "status": "healthy", "supported": False, "reason": "No repair needed"}
    if ordinals == expected_contiguous and not stale_open_turns and current_open_turns:
        return {
            **base,
            "status": "active_latest_turn",
            "supported": False,
            "reason": "The only open turn is the latest turn; automatic closure is unsafe",
        }
    if len(breaks) != 1 or len(stale_open_turns) != 1 or current_open_turns:
        return {
            **base,
            "status": "unsupported",
            "supported": False,
            "reason": "Expected exactly one ordinal regression and one superseded open turn",
        }

    previous_line, previous_ordinal = breaks[0]["previous"]
    boundary_line, boundary_ordinal = breaks[0]["current"]
    boundary_index = boundary_line - 1
    prefix_values = [value for _, value in ordinals[:boundary_index]]
    suffix_values = [value for _, value in ordinals[boundary_index:]]
    if prefix_values != list(range(len(prefix_values))):
        return {
            **base,
            "status": "unsupported",
            "supported": False,
            "reason": "Ordinal prefix is not contiguous from zero",
        }
    if any(current != previous + 1 for previous, current in zip(suffix_values, suffix_values[1:])):
        return {
            **base,
            "status": "unsupported",
            "supported": False,
            "reason": "Ordinal suffix is not internally contiguous",
        }

    orphan_turn = stale_open_turns[0]
    if any(line_no >= boundary_line and turn_id == orphan_turn for line_no, turn_id in turn_refs):
        return {
            **base,
            "status": "unsupported",
            "supported": False,
            "reason": "The stale turn is referenced after the proposed boundary",
        }
    later_starts = [
        value for value in starts.values() if value["line"] >= boundary_line and value.get("started_at")
    ]
    if not later_starts:
        return {
            **base,
            "status": "unsupported",
            "supported": False,
            "reason": "No later task start supplies a safe completion boundary",
        }
    later_starts.sort(key=lambda item: item["line"])
    insert_ordinal = previous_ordinal + 1
    ordinal_shift = previous_ordinal + 2 - boundary_ordinal
    planned_ordinals = prefix_values + [insert_ordinal] + [
        value + ordinal_shift for value in suffix_values
    ]
    if planned_ordinals != list(range(len(planned_ordinals))):
        return {
            **base,
            "status": "unsupported",
            "supported": False,
            "reason": "Proposed repair would not produce contiguous ordinals",
        }

    boundary_timestamp = None
    with path.open("r", encoding="utf-8") as source:
        for line_no, raw in enumerate(source, 1):
            if line_no == boundary_line:
                boundary_timestamp = json.loads(raw).get("timestamp")
                break
    if not boundary_timestamp or not starts[orphan_turn].get("timestamp"):
        return {
            **base,
            "status": "unsupported",
            "supported": False,
            "reason": "Missing timestamps at repair boundary",
        }
    try:
        abort_time = parse_timestamp(boundary_timestamp) - timedelta(milliseconds=1)
        start_time = parse_timestamp(starts[orphan_turn]["timestamp"])
        completion_time = parse_timestamp(later_starts[0]["started_at"])
    except RepairError as error:
        return {
            **base,
            "status": "unsupported",
            "supported": False,
            "reason": str(error),
        }
    if abort_time < start_time or completion_time < abort_time:
        return {
            **base,
            "status": "unsupported",
            "supported": False,
            "reason": "Turn timestamps are not chronologically safe for repair",
        }
    abort_timestamp = abort_time.isoformat(timespec="milliseconds").replace("+00:00", "Z")
    plan = {
        "boundary_line": boundary_line,
        "previous_line": previous_line,
        "previous_ordinal": previous_ordinal,
        "boundary_ordinal": boundary_ordinal,
        "insert_ordinal": insert_ordinal,
        "ordinal_shift": ordinal_shift,
        "orphan_turn_id": orphan_turn,
        "abort_timestamp": abort_timestamp,
        "started_at": starts[orphan_turn].get("started_at"),
        "completed_at": later_starts[0]["started_at"],
        "duration_ms": int((abort_time - start_time).total_seconds() * 1000),
        "expected_output_records": line_count + 1,
    }
    return {
        **base,
        "status": "supported_ordinal_orphan",
        "supported": True,
        "reason": "One stale open turn overlaps one restarted ordinal segment",
        "plan": plan,
    }


def integrity_check(path: Path) -> str:
    with connect_readonly(path) as connection:
        row = connection.execute("PRAGMA integrity_check").fetchone()
    return row[0] if row else "no result"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalized_rollout_hash(path: Path, skip_abort_turn: str | None = None) -> str:
    digest = hashlib.sha256()
    with path.open("r", encoding="utf-8") as source:
        for raw in source:
            record = json.loads(raw)
            payload = record.get("payload") or {}
            if (
                skip_abort_turn
                and record.get("type") == "event_msg"
                and payload.get("type") == "turn_aborted"
                and payload.get("turn_id") == skip_abort_turn
            ):
                continue
            ordinal = record.get("ordinal")
            if not isinstance(ordinal, int):
                raise RepairError("Cannot normalize a record without an integer ordinal")
            digest.update(replace_top_level_ordinal(raw, ordinal, "#").encode("utf-8"))
    return digest.hexdigest()


def backup_database(source: Path, destination: Path) -> None:
    if not source.is_file():
        raise RepairError(f"Database not found: {source}")
    source_connection = sqlite3.connect(str(source))
    destination_connection = sqlite3.connect(str(destination))
    try:
        source_connection.backup(destination_connection)
    finally:
        destination_connection.close()
        source_connection.close()


def create_backup(codex_home: Path, thread: dict[str, Any], diagnosis: dict[str, Any]) -> Path:
    thread_id = thread["id"]
    if not SAFE_THREAD_ID_PATTERN.fullmatch(thread_id) or thread_id in {".", ".."}:
        raise RepairError(f"Unsafe thread ID for backup path: {thread_id!r}")
    stamp = datetime.now().astimezone().strftime("%Y%m%d-%H%M%S-%f")
    backup_dir = Path.home() / ".codex-repair-backups" / thread["id"] / stamp
    backup_dir.mkdir(parents=True, exist_ok=False)
    try:
        rollout = Path(thread["rollout_path"])
        shutil.copy2(rollout, backup_dir / "original-rollout.jsonl")
        global_state = codex_home / ".codex-global-state.json"
        if global_state.is_file():
            shutil.copy2(global_state, backup_dir / ".codex-global-state.json")
        backup_database(codex_home / "state_5.sqlite", backup_dir / "state_5.sqlite")
        backup_database(codex_home / "sqlite" / "codex-dev.db", backup_dir / "codex-dev.db")
        if integrity_check(backup_dir / "state_5.sqlite") != "ok":
            raise RepairError("Backed-up state_5.sqlite failed integrity_check")
        if integrity_check(backup_dir / "codex-dev.db") != "ok":
            raise RepairError("Backed-up codex-dev.db failed integrity_check")
        manifest = {
            "created_at": datetime.now().astimezone().isoformat(),
            "thread": public_thread(thread),
            "original_sha256": sha256_file(rollout),
            "diagnosis": diagnosis,
        }
        (backup_dir / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    except Exception:
        shutil.rmtree(backup_dir)
        raise
    return backup_dir


def build_repaired_rollout(
    source_path: Path, output_path: Path, diagnosis: dict[str, Any]
) -> dict[str, Any]:
    plan = diagnosis["plan"]
    boundary_line = plan["boundary_line"]
    source_normalized = normalized_rollout_hash(source_path)
    abort_event = {
        "timestamp": plan["abort_timestamp"],
        "ordinal": plan["insert_ordinal"],
        "type": "event_msg",
        "payload": {
            "type": "turn_aborted",
            "turn_id": plan["orphan_turn_id"],
            "reason": "interrupted",
            "started_at": plan["started_at"],
            "completed_at": plan["completed_at"],
            "duration_ms": plan["duration_ms"],
        },
    }
    inserted_line = json.dumps(abort_event, ensure_ascii=False, separators=(",", ":")) + "\n"
    with source_path.open("r", encoding="utf-8") as source, output_path.open(
        "x", encoding="utf-8"
    ) as output:
        for line_no, raw in enumerate(source, 1):
            if line_no == boundary_line:
                output.write(inserted_line)
            if line_no >= boundary_line:
                record = json.loads(raw)
                ordinal = record.get("ordinal")
                if not isinstance(ordinal, int):
                    raise RepairError(f"Source line {line_no} has no integer ordinal")
                output.write(
                    replace_top_level_ordinal(
                        raw,
                        ordinal,
                        ordinal + plan["ordinal_shift"],
                    )
                )
            else:
                output.write(raw)
        output.flush()
        os.fsync(output.fileno())
    shutil.copystat(source_path, output_path)
    repaired_thread = {**diagnosis["thread"], "rollout_path": str(output_path)}
    repaired_diagnosis = inspect_rollout(repaired_thread)
    if repaired_diagnosis["status"] != "healthy":
        raise RepairError(f"Repaired copy is not healthy: {repaired_diagnosis}")
    repaired_normalized = normalized_rollout_hash(output_path, plan["orphan_turn_id"])
    if source_normalized != repaired_normalized:
        raise RepairError("Original record bodies changed during repair")
    return repaired_diagnosis


def reopen_codex() -> bool:
    try:
        result = subprocess.run(
            ["/usr/bin/open", "-a", "ChatGPT"],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError as error:
        print(f"WARNING: Repair succeeded, but Codex could not be reopened: {error}", file=sys.stderr)
        return False
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip() or f"exit code {result.returncode}"
        print(f"WARNING: Repair succeeded, but Codex could not be reopened: {detail}", file=sys.stderr)
        return False
    return True


def diagnose(codex_home: Path, selector: str) -> dict[str, Any]:
    thread = resolve_thread(codex_home, selector)
    result = inspect_rollout(thread)
    result["thread"] = public_thread(thread)
    result["desktop_running"] = desktop_running()
    return result


def print_json(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True))


def command_resolve(args: argparse.Namespace) -> int:
    print_json(public_thread(resolve_thread(args.codex_home, args.selector)))
    return 0


def command_diagnose(args: argparse.Namespace) -> int:
    result = diagnose(args.codex_home, args.selector)
    print_json(result)
    return 0 if result["status"] in {"healthy", "supported_ordinal_orphan"} else 3


def command_prepare(args: argparse.Namespace) -> int:
    result = diagnose(args.codex_home, args.selector)
    if result["status"] == "healthy":
        print_json(result)
        print("No launcher created because the task is already healthy.")
        return 0
    if result["status"] != "supported_ordinal_orphan":
        print_json(result)
        raise RepairError("This rollout pattern is not safe for automatic repair")
    thread_id = result["thread"]["id"]
    output_path = Path(args.output).expanduser() if args.output else (
        Path.home() / "Desktop" / f"repair-codex-thread-{thread_id[:8]}.command"
    )
    output_path = output_path.resolve()
    if not output_path.parent.is_dir():
        raise RepairError(f"Launcher parent directory does not exist: {output_path.parent}")
    if output_path.exists():
        raise RepairError(
            f"Refusing to overwrite existing launcher: {output_path}; choose another --output path"
        )
    log_path = output_path.with_suffix(".log")
    script_path = Path(__file__).resolve()
    command = " ".join(
        [
            "/usr/bin/env",
            "python3",
            shlex.quote(str(script_path)),
            "--codex-home",
            shlex.quote(str(args.codex_home)),
            "apply",
            shlex.quote(thread_id),
            "--reopen",
        ]
    )
    launcher = f"""#!/bin/bash
set -uo pipefail
export PATH=\"/usr/bin:/bin:/usr/sbin:/sbin:/opt/homebrew/bin\"
readonly REPAIR_LOG={shlex.quote(str(log_path))}
printf '\\n=== Codex thread repair: {thread_id} ===\\n'
printf 'Press Cmd+Q in Codex before continuing.\\n'
{command} 2>&1 | tee -a \"$REPAIR_LOG\"
repair_exit_code=${{PIPESTATUS[0]}}
printf '\\nFinished with exit code: %s\\n' \"$repair_exit_code\" | tee -a \"$REPAIR_LOG\"
if [[ \"$repair_exit_code\" -ne 0 ]]; then
  printf 'Press Enter to keep this window open for review...'
  read -r _
fi
exit \"$repair_exit_code\"
"""
    with output_path.open("x", encoding="utf-8") as output:
        output.write(launcher)
        output.flush()
        os.fsync(output.fileno())
    output_path.chmod(0o755)
    print_json(
        {
            "launcher": str(output_path),
            "log": str(log_path),
            "thread": result["thread"],
            "plan": result["plan"],
        }
    )
    return 0


def command_apply(args: argparse.Namespace) -> int:
    if desktop_running():
        raise RepairError("Codex/ChatGPT is running; press Cmd+Q before applying repair")
    result = diagnose(args.codex_home, args.selector)
    if result["status"] == "healthy":
        print_json(result)
        if args.reopen:
            reopen_codex()
        return 0
    if result["status"] != "supported_ordinal_orphan":
        print_json(result)
        raise RepairError("This rollout pattern is not safe for automatic repair")
    if integrity_check(args.codex_home / "state_5.sqlite") != "ok":
        raise RepairError("Live state_5.sqlite failed integrity_check")
    thread = resolve_thread(args.codex_home, result["thread"]["id"])
    rollout = Path(thread["rollout_path"])
    backup_dir = create_backup(args.codex_home, thread, result)
    handle, temporary_name = tempfile.mkstemp(
        prefix=f".{rollout.name}.repair-", suffix=".tmp", dir=rollout.parent
    )
    os.close(handle)
    temporary_path = Path(temporary_name)
    temporary_path.unlink()
    replaced = False
    try:
        build_input = {**result, "thread": public_thread(thread)}
        build_repaired_rollout(rollout, temporary_path, build_input)
        os.replace(temporary_path, rollout)
        replaced = True
        final_result = diagnose(args.codex_home, thread["id"])
        if final_result["status"] != "healthy":
            raise RepairError(f"Installed rollout is not healthy: {final_result}")
        if integrity_check(args.codex_home / "state_5.sqlite") != "ok":
            raise RepairError("Post-repair state_5.sqlite failed integrity_check")
        repair_result = {
            "completed_at": datetime.now().astimezone().isoformat(),
            "backup_directory": str(backup_dir),
            "repaired_sha256": sha256_file(rollout),
            "verification": final_result,
        }
        (backup_dir / "repair-result.json").write_text(
            json.dumps(repair_result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print_json(repair_result)
    except Exception:
        if temporary_path.exists():
            temporary_path.unlink()
        if replaced:
            restore_temp = rollout.with_name(f".{rollout.name}.automatic-rollback.tmp")
            shutil.copy2(backup_dir / "original-rollout.jsonl", restore_temp)
            os.replace(restore_temp, rollout)
        raise
    if args.reopen:
        reopen_codex()
    return 0


def command_verify(args: argparse.Namespace) -> int:
    result = diagnose(args.codex_home, args.selector)
    result["state_integrity"] = integrity_check(args.codex_home / "state_5.sqlite")
    result["catalog_integrity"] = integrity_check(args.codex_home / "sqlite" / "codex-dev.db")
    print_json(result)
    return (
        0
        if result["status"] == "healthy"
        and result["state_integrity"] == "ok"
        and result["catalog_integrity"] == "ok"
        else 3
    )


def command_rollback(args: argparse.Namespace) -> int:
    if desktop_running():
        raise RepairError("Codex/ChatGPT is running; press Cmd+Q before rollback")
    backup_dir = Path(args.backup_directory).expanduser().resolve()
    manifest_path = backup_dir / "manifest.json"
    original_path = backup_dir / "original-rollout.jsonl"
    if not manifest_path.is_file() or not original_path.is_file():
        raise RepairError(f"Invalid backup directory: {backup_dir}")
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        thread_id = manifest["thread"]["id"]
        target = Path(manifest["thread"]["rollout_path"]).expanduser().resolve()
        expected_hash = manifest["original_sha256"]
    except (json.JSONDecodeError, KeyError, TypeError) as error:
        raise RepairError(f"Malformed backup manifest: {error}") from error
    if not isinstance(thread_id, str) or not SAFE_THREAD_ID_PATTERN.fullmatch(thread_id):
        raise RepairError("Backup manifest has an unsafe thread ID")
    sessions_root = (args.codex_home / "sessions").resolve()
    try:
        target.relative_to(sessions_root)
    except ValueError as error:
        raise RepairError(f"Rollback target is outside Codex sessions: {target}") from error
    live_thread = resolve_thread(args.codex_home, thread_id)
    if Path(live_thread["rollout_path"]).expanduser().resolve() != target:
        raise RepairError("Backup target does not match the live thread database row")
    original_diagnosis = inspect_rollout({"id": thread_id, "rollout_path": str(original_path)})
    if original_diagnosis["status"] in {
        "missing_rollout",
        "malformed_rollout",
        "session_id_mismatch",
    }:
        raise RepairError(f"Backup rollout identity check failed: {original_diagnosis}")
    handle, temporary_name = tempfile.mkstemp(
        prefix=f".{target.name}.rollback-", suffix=".tmp", dir=target.parent
    )
    os.close(handle)
    restore_temp = Path(temporary_name)
    shutil.copy2(original_path, restore_temp)
    if sha256_file(restore_temp) != expected_hash:
        restore_temp.unlink(missing_ok=True)
        raise RepairError("Backup hash does not match manifest")
    os.replace(restore_temp, target)
    result = {
        "restored": str(target),
        "backup_directory": str(backup_dir),
        "sha256": sha256_file(target),
    }
    print_json(result)
    if args.reopen:
        reopen_codex()
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--codex-home",
        type=Path,
        default=default_codex_home(),
        help="Codex state directory (default: CODEX_HOME or ~/.codex)",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    for name, handler in (("resolve", command_resolve), ("diagnose", command_diagnose)):
        command = subparsers.add_parser(name)
        command.add_argument("selector", help="Exact thread ID, UI title, or unique title fragment")
        command.set_defaults(handler=handler)
    prepare = subparsers.add_parser("prepare")
    prepare.add_argument("selector")
    prepare.add_argument("--output", help="Launcher output path")
    prepare.set_defaults(handler=command_prepare)
    apply_command = subparsers.add_parser("apply")
    apply_command.add_argument("selector", help="Prefer an exact thread ID")
    apply_command.add_argument("--reopen", action="store_true")
    apply_command.set_defaults(handler=command_apply)
    verify = subparsers.add_parser("verify")
    verify.add_argument("selector")
    verify.set_defaults(handler=command_verify)
    rollback = subparsers.add_parser("rollback")
    rollback.add_argument("backup_directory")
    rollback.add_argument("--reopen", action="store_true")
    rollback.set_defaults(handler=command_rollback)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    args.codex_home = args.codex_home.expanduser().resolve()
    try:
        return args.handler(args)
    except AmbiguousSelector as error:
        print_json(
            {"error": str(error), "selector": error.selector, "candidates": error.candidates}
        )
        return 2
    except (RepairError, OSError, sqlite3.Error) as error:
        print_json({"error": str(error), "type": type(error).__name__})
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
