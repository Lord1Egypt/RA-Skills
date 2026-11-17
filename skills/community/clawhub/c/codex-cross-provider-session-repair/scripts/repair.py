#!/usr/bin/env python3
"""Diagnose and repair one Codex session without touching unrelated sessions.

The script deliberately uses only Python's standard library so it can run on a
fresh machine. It is dry-run by default; pass --apply to write changes.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


STALE_ITEM_RE = re.compile(r"Item with id ['\"](rs_[^'\"]+)['\"] not found")
PROVIDER_RE = re.compile(r"^\s*model_provider\s*=\s*['\"]([^'\"]+)['\"]", re.MULTILINE)
MODEL_TURN_ERROR_RE = re.compile(r"Requests ending with a model turn are not supported", re.IGNORECASE)
REMOTE_COMPACTION_ERROR_RE = re.compile(
    r"remote compaction v2 expected exactly one compaction output item",
    re.IGNORECASE,
)



def resolve_codex_home(value: str | None) -> Path:
    if value:
        return Path(value).expanduser().resolve()
    configured = os.environ.get("CODEX_HOME")
    if configured:
        return Path(configured).expanduser().resolve()
    if os.name == "nt":
        profile = os.environ.get("USERPROFILE")
        if profile:
            return (Path(profile) / ".codex").resolve()
    return (Path.home() / ".codex").resolve()


def find_rollout(codex_home: Path, session_id: str) -> Path:
    sessions = codex_home / "sessions"
    if not sessions.is_dir():
        raise FileNotFoundError(f"sessions directory not found: {sessions}")

    exact = sorted(sessions.rglob(f"rollout-*-{session_id}.jsonl"))
    if exact:
        return exact[0]

    # Filename conventions have changed across Codex versions, so fall back to
    # checking session_meta records without reading any other Codex artifacts.
    for candidate in sorted(sessions.rglob("rollout-*.jsonl")):
        try:
            with candidate.open("r", encoding="utf-8") as handle:
                for line in handle:
                    try:
                        item = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    payload = item.get("payload", {})
                    if item.get("type") == "session_meta" and payload.get("id") == session_id:
                        return candidate
        except OSError:
            continue
    raise FileNotFoundError(f"rollout for session {session_id} not found under {sessions}")


def read_jsonl(path: Path) -> tuple[list[str], list[dict[str, Any] | None], list[int]]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    records: list[dict[str, Any] | None] = []
    errors: list[int] = []
    for number, line in enumerate(lines, 1):
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            records.append(None)
            errors.append(number)
    return lines, records, errors


def read_global_provider(codex_home: Path) -> str | None:
    config = codex_home / "config.toml"
    if not config.is_file():
        return None
    match = PROVIDER_RE.search(config.read_text(encoding="utf-8", errors="replace"))
    return match.group(1) if match else None


def read_thread_row(database: Path, session_id: str) -> dict[str, Any] | None:
    if not database.is_file():
        return None
    connection: sqlite3.Connection | None = None
    try:
        connection = sqlite3.connect(database)
        connection.execute("PRAGMA query_only = ON")
        tables = {row[0] for row in connection.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        if "threads" not in tables:
            return None
        columns = [row[1] for row in connection.execute("PRAGMA table_info(threads)")]
        wanted = [name for name in ("id", "model_provider", "model", "cwd", "archived") if name in columns]
        if "id" not in wanted:
            return None
        row = connection.execute(
            f"SELECT {', '.join(wanted)} FROM threads WHERE id = ?", (session_id,)
        ).fetchone()
        return dict(zip(wanted, row)) if row else None
    except sqlite3.Error as exc:
        return {"error": f"SQLite read failed: {exc}"}
    finally:
        try:
            if connection is not None:
                connection.close()
        except Exception:
            pass


def read_stale_ids(database: Path, session_id: str) -> list[str]:
    if not database.is_file():
        return []
    connection: sqlite3.Connection | None = None
    try:
        connection = sqlite3.connect(database)
        connection.execute("PRAGMA query_only = ON")
        tables = {row[0] for row in connection.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        if "logs" not in tables:
            return []
        rows = connection.execute(
            "SELECT feedback_log_body FROM logs WHERE thread_id = ?", (session_id,)
        ).fetchall()
        found: set[str] = set()
        for (body,) in rows:
            found.update(STALE_ITEM_RE.findall(body or ""))
        return sorted(found)
    except sqlite3.Error:
        return []
    finally:
        try:
            if connection is not None:
                connection.close()
        except Exception:
            pass


def read_model_turn_error(database: Path, session_id: str) -> bool:
    """Check if logs contain Gemini model-turn-ending compaction errors."""
    if not database.is_file():
        return False
    connection: sqlite3.Connection | None = None
    try:
        connection = sqlite3.connect(database)
        connection.execute("PRAGMA query_only = ON")
        tables = {row[0] for row in connection.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        if "logs" not in tables:
            return False
        rows = connection.execute(
            "SELECT feedback_log_body FROM logs WHERE thread_id = ? AND level IN ('ERROR', 'WARN')",
            (session_id,),
        ).fetchall()
        for (body,) in rows:
            if body and MODEL_TURN_ERROR_RE.search(body):
                return True
        return False
    except sqlite3.Error:
        return False
    finally:
        try:
            if connection is not None:
                connection.close()
        except Exception:
            pass


def read_remote_compaction_error(database: Path, session_id: str) -> bool:
    """Check if logs contain Codex remote-compaction-v2 failures.

    These failures mean the current provider/model did not return the
    ``type: "compaction"`` output item that Codex remote compaction v2
    requires. The fix is not a session rewrite: the user should disable
    remote compaction or switch to a provider/model that supports it.
    """
    if not database.is_file():
        return False
    connection: sqlite3.Connection | None = None
    try:
        connection = sqlite3.connect(database)
        connection.execute("PRAGMA query_only = ON")
        tables = {row[0] for row in connection.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        if "logs" not in tables:
            return False
        rows = connection.execute(
            "SELECT feedback_log_body FROM logs WHERE thread_id = ? AND level IN ('ERROR', 'WARN')",
            (session_id,),
        ).fetchall()
        for (body,) in rows:
            if body and REMOTE_COMPACTION_ERROR_RE.search(body):
                return True
        return False
    except sqlite3.Error:
        return False
    finally:
        try:
            if connection is not None:
                connection.close()
        except Exception:
            pass


def detect_compaction_model_turn(records: list[dict[str, Any] | None]) -> dict[str, Any]:
    """Detect if the effective history ends with a model turn.

    Walks the JSONL records simulating Codex turn management: turns are
    delimited by task_started/task_complete events, and thread_rolled_back
    events pop completed turns.  After applying rollbacks, the last effective
    response_item message role is checked.  If it is ``assistant`` or
    ``model``, a Gemini compaction request would fail with HTTP 400
    "Requests ending with a model turn are not supported."
    """
    turns: list[list[tuple[int, str]]] = []
    current_turn: list[tuple[int, str]] = []

    for i, record in enumerate(records):
        if not record:
            continue
        rtype = record.get("type", "")
        payload = record.get("payload", {})
        ptype = payload.get("type", "")

        if rtype == "response_item" and ptype == "message":
            role = payload.get("role", "")
            current_turn.append((i, role))
        elif rtype == "event_msg":
            if ptype == "task_started":
                current_turn = []
            elif ptype == "task_complete":
                if current_turn:
                    turns.append(current_turn)
                current_turn = []
            elif ptype == "thread_rolled_back":
                num = payload.get("num_turns", 1)
                for _ in range(num):
                    if turns:
                        turns.pop()
                current_turn = []

    # Effective history = all completed turns after rollbacks.
    # The current (incomplete) turn's messages belong to the new turn and
    # are NOT part of the compaction input.
    effective: list[tuple[int, str]] = []
    for turn in turns:
        effective.extend(turn)

    if effective:
        last_idx, last_role = effective[-1]
        return {
            "model_turn_risk": last_role in ("assistant", "model"),
            "last_effective_role": last_role,
            "last_effective_line": last_idx + 1,
            "effective_message_count": len(effective),
            "effective_turn_count": len(turns),
        }

    return {
        "model_turn_risk": False,
        "last_effective_role": None,
        "last_effective_line": None,
        "effective_message_count": 0,
        "effective_turn_count": len(turns),
    }


def effective_last_message_after_rollback_removal(records: list[dict[str, Any] | None]) -> tuple[int, str] | None:
    """Return the last effective response_item message after ``thread_rolled_back``
    events are stripped, as ``(record_index, role)``, or ``None``.

    This mirrors :func:`detect_compaction_model_turn` but treats every
    ``thread_rolled_back`` event as already removed, which is what
    :func:`rewrite_session` does when *fix_model_turn* is set.  The rewrite then
    appends a dummy user message when that last effective message is an
    assistant/model turn.
    """
    turns: list[list[tuple[int, str]]] = []
    current_turn: list[tuple[int, str]] = []

    for i, record in enumerate(records):
        if not record:
            continue
        rtype = record.get("type", "")
        payload = record.get("payload", {})
        ptype = payload.get("type", "")

        if rtype == "response_item" and ptype == "message":
            current_turn.append((i, payload.get("role", "")))
        elif rtype == "event_msg":
            if ptype == "task_started":
                current_turn = []
            elif ptype == "task_complete":
                if current_turn:
                    turns.append(current_turn)
                current_turn = []
            # thread_rolled_back is intentionally ignored: rewrite_session strips it.

    effective: list[tuple[int, str]] = []
    for turn in turns:
        effective.extend(turn)
    if effective:
        return effective[-1]
    return None


def read_structured_models(records: list[dict[str, Any] | None]) -> list[str]:
    """Collect model values from structured per-turn settings in the rollout."""
    models: list[str] = []
    for record in records:
        if not record or record.get("type") != "event_msg":
            continue
        payload = record.get("payload") or {}
        event_type = payload.get("type")
        if event_type == "turn_context" and isinstance(payload.get("model"), str):
            models.append(payload["model"])
            continue
        if event_type != "thread_settings_applied":
            continue
        settings = payload.get("thread_settings")
        if not isinstance(settings, dict):
            continue
        if isinstance(settings.get("model"), str):
            models.append(settings["model"])
        collaboration = settings.get("collaboration_mode")
        if isinstance(collaboration, dict):
            collaboration_settings = collaboration.get("settings")
            if isinstance(collaboration_settings, dict) and isinstance(
                collaboration_settings.get("model"), str
            ):
                models.append(collaboration_settings["model"])
    return models


def inspect_session(codex_home: Path, session_id: str) -> dict[str, Any]:
    rollout = find_rollout(codex_home, session_id)
    lines, records, parse_errors = read_jsonl(rollout)
    session_meta: list[dict[str, Any]] = []
    reasoning_ids: list[str] = []
    for record in records:
        if not record:
            continue
        payload = record.get("payload") or {}
        if record.get("type") == "session_meta":
            session_meta.append({
                "id": payload.get("id"),
                "model_provider": payload.get("model_provider"),
                "cwd": payload.get("cwd"),
            })
        if record.get("type") == "response_item" and payload.get("type") == "reasoning":
            if payload.get("id"):
                reasoning_ids.append(payload["id"])

    root_db = codex_home / "state_5.sqlite"
    logs_db = codex_home / "logs_2.sqlite"
    stale_ids = read_stale_ids(logs_db, session_id)
    reasoning_set = set(reasoning_ids)
    target_meta = [item for item in session_meta if item.get("id") == session_id]
    model_turn_info = detect_compaction_model_turn(records)
    model_turn_info["logged_error"] = read_model_turn_error(logs_db, session_id)
    remote_compaction_error = read_remote_compaction_error(logs_db, session_id)
    return {
        "session_id": session_id,
        "codex_home": str(codex_home),
        "rollout_path": str(rollout),
        "line_count": len(lines),
        "json_parse_errors": parse_errors,
        "session_meta": session_meta,
        "target_session_meta": target_meta,
        "global_provider": read_global_provider(codex_home),
        "root_thread": read_thread_row(root_db, session_id),
        "stale_remote_item_ids": stale_ids,
        "stale_ids_present_as_reasoning": sorted(set(stale_ids) & reasoning_set),
        "reasoning_item_count": len(reasoning_ids),
        "reasoning_item_ids": reasoning_ids,
        "structured_model_values": read_structured_models(records),
        "child_database_present": (codex_home / "sqlite" / "state_5.sqlite").is_file(),
        "model_turn": model_turn_info,
        "remote_compaction": {
            "logged_error": remote_compaction_error,
            "unsupported": remote_compaction_error,
        },
    }


def timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def backup_file(path: Path, label: str) -> Path:
    destination = path.with_name(f"{path.name}.bak-{label}-{timestamp()}")
    shutil.copy2(path, destination)
    return destination


def rewrite_session(
    report: dict[str, Any],
    provider: str | None,
    fix_provider: bool,
    remove_reasoning: str,
    fix_model_turn: bool = False,
    fix_model: bool = False,
    model: str | None = None,
) -> tuple[Path | None, int, int, int, int]:
    """Rewrite session JSONL.

    Returns ``(backup_path, removed_reasoning, provider_updates, model_turn_inserts, model_updates)``.

    When *fix_model_turn* is set the function also strips ``thread_rolled_back``
    events so that previously rolled-back turns become effective again.  If the
    last response_item message is still an assistant turn after that, a dummy
    user message is appended to satisfy Gemini's requirement that requests must
    not end with a model turn. When *fix_model* is set, structured model
    settings in the target rollout are changed to *model*.
    """
    path = Path(report["rollout_path"])
    lines, records, parse_errors = read_jsonl(path)
    if parse_errors:
        raise ValueError(f"refusing to rewrite malformed JSONL; lines: {parse_errors[:10]}")

    if fix_model and not model:
        raise ValueError("fix_model requires a target model")

    stale = set(report["stale_ids_present_as_reasoning"])
    needs_write = remove_reasoning != "none" or fix_provider or fix_model_turn or fix_model
    backup = backup_file(path, "session-repair") if needs_write else None
    output: list[str] = []
    removed = 0
    provider_updates = 0
    model_turn_inserts = 0
    model_updates = 0
    rollbacks_removed = 0

    # When fixing model-turn, find the last effective response_item message
    # AFTER thread_rolled_back events are stripped (the rewrite does the same
    # stripping below). Using the raw tail of the JSONL is wrong: a rolled-back
    # or unfinished turn can leave a trailing user message while the effective
    # history ends with an assistant turn, which would skip the dummy insert.
    last_message_idx: int | None = None
    last_message_role: str | None = None
    if fix_model_turn:
        mt = report.get("model_turn", {})
        if mt.get("model_turn_risk") or mt.get("logged_error"):
            last_effective = effective_last_message_after_rollback_removal(records)
            if last_effective is not None:
                last_message_idx, last_message_role = last_effective

    for original, record in zip(lines, records):
        assert record is not None
        payload = record.get("payload") or {}
        if record.get("type") == "response_item" and payload.get("type") == "reasoning":
            item_id = payload.get("id")
            if remove_reasoning == "all" or (remove_reasoning == "stale" and item_id in stale):
                removed += 1
                continue
        # Strip thread_rolled_back events so rolled-back turns become effective.
        if (
            fix_model_turn
            and record.get("type") == "event_msg"
            and payload.get("type") == "thread_rolled_back"
        ):
            rollbacks_removed += 1
            continue
        if (
            fix_provider
            and provider
            and record.get("type") == "session_meta"
            and payload.get("id") == report["session_id"]
            and payload.get("model_provider") != provider
        ):
            payload["model_provider"] = provider
            record["payload"] = payload
            provider_updates += 1
            output.append(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")
            continue
        if fix_model and model and record.get("type") == "event_msg":
            model_changed = False
            event_type = payload.get("type")
            if event_type == "thread_settings_applied":
                settings = payload.get("thread_settings")
                if isinstance(settings, dict):
                    if settings.get("model") != model:
                        settings["model"] = model
                        model_changed = True
                    collaboration = settings.get("collaboration_mode")
                    if isinstance(collaboration, dict):
                        collaboration_settings = collaboration.get("settings")
                        if (
                            isinstance(collaboration_settings, dict)
                            and collaboration_settings.get("model") != model
                        ):
                            collaboration_settings["model"] = model
                            model_changed = True
            elif event_type == "turn_context" and payload.get("model") != model:
                payload["model"] = model
                model_changed = True
            if model_changed:
                record["payload"] = payload
                model_updates += 1
                output.append(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")
                continue
        output.append(original)

        # Insert a user message right after the last assistant message so
        # that compaction sent to Gemini does not end with a model turn.
        if (
            fix_model_turn
            and last_message_idx is not None
            and last_message_role in ("assistant", "model")
            and record is records[last_message_idx]
        ):
            meta = payload.get("internal_chat_message_metadata_passthrough") or {}
            repair_msg = {
                "timestamp": record.get("timestamp", ""),
                "type": "response_item",
                "payload": {
                    "type": "message",
                    "id": f"msg_repair_model_turn_{model_turn_inserts:04d}",
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": "(session repair: appended user turn to prevent Gemini compaction failure on model-turn-ending)",
                        }
                    ],
                    "internal_chat_message_metadata_passthrough": meta,
                },
            }
            output.append(json.dumps(repair_msg, ensure_ascii=False, separators=(",", ":")) + "\n")
            model_turn_inserts += 1

    if not needs_write:
        return None, 0, 0, 0, 0

    temporary = path.with_name(f".{path.name}.repair-{os.getpid()}.tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        handle.write("".join(output))
    try:
        os.replace(temporary, path)
    except Exception:
        try:
            temporary.unlink()
        except OSError:
            pass
        raise
    if rollbacks_removed:
        print(f"Removed {rollbacks_removed} thread_rolled_back event(s) to restore effective turns.")
    return backup, removed, provider_updates, model_turn_inserts, model_updates


def update_thread_provider(codex_home: Path, session_id: str, provider: str) -> Path | None:
    database = codex_home / "state_5.sqlite"
    row = read_thread_row(database, session_id)
    if not row or row.get("error") or "model_provider" not in row:
        return None
    if row["model_provider"] == provider:
        return None
    backup = backup_file(database, "session-repair")
    for suffix in ("-wal", "-shm"):
        sidecar = Path(str(database) + suffix)
        if sidecar.is_file():
            shutil.copy2(sidecar, Path(str(backup) + suffix))
    connection = sqlite3.connect(database)
    try:
        connection.execute("BEGIN IMMEDIATE")
        connection.execute(
            "UPDATE threads SET model_provider = ? WHERE id = ?", (provider, session_id)
        )
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()
    return backup


def update_thread_model(codex_home: Path, session_id: str, model: str) -> Path | None:
    """Update only the target thread's model snapshot, with a database backup."""
    database = codex_home / "state_5.sqlite"
    row = read_thread_row(database, session_id)
    if not row or row.get("error") or "model" not in row:
        return None
    if row["model"] == model:
        return None
    backup = backup_file(database, "session-model-repair")
    for suffix in ("-wal", "-shm"):
        sidecar = Path(str(database) + suffix)
        if sidecar.is_file():
            shutil.copy2(sidecar, Path(str(backup) + suffix))
    connection = sqlite3.connect(database)
    try:
        connection.execute("BEGIN IMMEDIATE")
        connection.execute("UPDATE threads SET model = ? WHERE id = ?", (model, session_id))
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()
    return backup


def disable_remote_compaction(codex_home: Path) -> Path | None:
    """Add ``remote_compaction_v2 = false`` under ``[features]`` in config.toml.

    Backs up the file first. Returns the backup path, or ``None`` when the
    feature is already disabled. The user must explicitly approve this write;
    it affects the global Codex config, not just one session.
    """
    config = codex_home / "config.toml"
    if not config.is_file():
        raise FileNotFoundError(f"config.toml not found: {config}")
    text = config.read_text(encoding="utf-8")

    if re.search(r"^\s*remote_compaction_v2\s*=\s*false\s*$", text, re.MULTILINE):
        return None

    backup = backup_file(config, "disable-remote-compaction")

    if re.search(r"^\s*remote_compaction_v2\s*=\s*true\s*$", text, re.MULTILINE):
        text = re.sub(
            r"^\s*remote_compaction_v2\s*=\s*true\s*$",
            "remote_compaction_v2 = false",
            text,
            count=1,
            flags=re.MULTILINE,
        )
    else:
        if not re.search(r"^\[features\]\s*$", text, re.MULTILINE):
            text = text.rstrip() + "\n\n[features]\n"
            text += "remote_compaction_v2 = false\n"
        else:
            text = re.sub(
                r"^(\[features\]\s*)$",
                r"\1remote_compaction_v2 = false\n",
                text,
                count=1,
                flags=re.MULTILINE,
            )
    config.write_text(text, encoding="utf-8")
    return backup


def print_report(report: dict[str, Any], as_json: bool) -> None:
    safe = dict(report)
    # The full reasoning ID list is useful for local debugging but noisy in the
    # normal report. Keep the count and the exact stale IDs only.
    safe.pop("reasoning_item_ids", None)
    if as_json:
        print(json.dumps(safe, ensure_ascii=False, indent=2))
        return
    print(f"Session: {safe['session_id']}")
    print(f"Rollout: {safe['rollout_path']}")
    print(f"JSONL: {safe['line_count']} lines; parse errors={len(safe['json_parse_errors'])}")
    print(f"Global provider: {safe['global_provider'] or '(not found)'}")
    print(f"Target session_meta: {safe['target_session_meta']}")
    print(f"Root threads row: {safe['root_thread'] or '(not found)'}")
    print(f"Historical remote stale IDs (from logs): {safe['stale_remote_item_ids']}")
    print(f"Stale IDs present as local reasoning: {safe['stale_ids_present_as_reasoning']}")
    print(f"Local reasoning records: {safe['reasoning_item_count']}")
    print(f"Child sqlite database present: {safe['child_database_present']}")
    mt = safe.get("model_turn", {})
    risk = mt.get("model_turn_risk", False)
    logged = mt.get("logged_error", False)
    flag = "RISK" if risk else "ok"
    if logged:
        flag += " + logged-error"
    print(
        f"Model-turn compaction: {flag} | last_role={mt.get('last_effective_role')} "
        f"line={mt.get('last_effective_line')} msgs={mt.get('effective_message_count')} "
        f"turns={mt.get('effective_turn_count')}"
    )

    rc = safe.get("remote_compaction", {})
    if rc.get("logged_error"):
        print()
        print("Remote compaction not supported by current provider/model:")
        print("  The backend did not return the `type: \"compaction\"` output item that Codex")
        print("  remote compaction v2 requires (error: 'expected exactly one compaction")
        print("  output item, got 0 from N output items').")
        print("  Fix: disable remote compaction (add `remote_compaction_v2 = false` under")
        print("  `[features]` in config.toml, or run with --disable-remote-compaction")
        print("  after user approval), or switch to a provider/model that supports it,")
        print("  then fully quit and relaunch Codex Desktop.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--session-id", required=True, help="Target Codex session UUID")
    parser.add_argument("--codex-home", help="Override CODEX_HOME")
    parser.add_argument("--provider", help="Current provider to write when --fix-provider is used")
    parser.add_argument("--fix-provider", action="store_true", help="Repair target session_meta and DB provider")
    parser.add_argument("--model", help="Target model to write when --fix-model is used")
    parser.add_argument("--fix-model", action="store_true", help="Repair target model settings and DB model")
    parser.add_argument(
        "--remove-reasoning",
        choices=("none", "stale", "all"),
        default="none",
        help="Remove exact stale reasoning IDs, or all internal reasoning records",
    )
    parser.add_argument(
        "--fix-model-turn",
        action="store_true",
        help="Append a user message after the last assistant message so Gemini "
        "compaction does not fail with 'Requests ending with a model turn are not supported'",
    )
    parser.add_argument(
        "--disable-remote-compaction",
        action="store_true",
        help="Add remote_compaction_v2 = false under [features] in config.toml "
        "(backup first). Requires --apply; use only with user approval.",
    )
    parser.add_argument("--apply", action="store_true", help="Write the requested repair; default is dry-run")
    parser.add_argument("--json", action="store_true", help="Print the diagnostic report as JSON")
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        codex_home = resolve_codex_home(args.codex_home)
        report = inspect_session(codex_home, args.session_id)
        print_report(report, args.json)
        if not args.apply:
            print("Dry run only. Re-run with --apply after fully quitting Codex Desktop.")
            return 0
        if report["json_parse_errors"]:
            raise ValueError("refusing to apply: JSONL has parse errors")
        if args.fix_provider and not args.provider:
            raise ValueError("--fix-provider requires --provider")
        if args.fix_model and not args.model:
            raise ValueError("--fix-model requires --model")
        if args.remove_reasoning == "stale" and not report["stale_ids_present_as_reasoning"]:
            print("No stale local reasoning IDs matched; no session rewrite needed.")
        mt = report.get("model_turn", {})
        if args.fix_model_turn and not (mt.get("model_turn_risk") or mt.get("logged_error")):
            print("No model-turn risk detected; --fix-model-turn has nothing to do.")
        session_backup = None
        removed = 0
        provider_updates = 0
        model_turn_inserts = 0
        model_updates = 0
        if args.remove_reasoning != "none" or args.fix_provider or args.fix_model_turn or args.fix_model:
            session_backup, removed, provider_updates, model_turn_inserts, model_updates = rewrite_session(
                report,
                args.provider,
                args.fix_provider,
                args.remove_reasoning,
                args.fix_model_turn,
                args.fix_model,
                args.model,
            )
        db_backup = None
        if args.fix_provider and args.provider:
            db_backup = update_thread_provider(codex_home, args.session_id, args.provider)
        model_db_backup = None
        if args.fix_model and args.model:
            model_db_backup = update_thread_model(codex_home, args.session_id, args.model)
        config_backup = None
        if args.disable_remote_compaction:
            config_backup = disable_remote_compaction(codex_home)
        print(
            f"Applied: removed_reasoning={removed}, "
            f"session_meta_provider_updates={provider_updates}, "
            f"model_turn_inserts={model_turn_inserts}, "
            f"model_settings_updates={model_updates}"
        )
        if session_backup:
            print(f"Session backup: {session_backup}")
        if db_backup:
            print(f"Database backup: {db_backup}")
        if model_db_backup:
            print(f"Model database backup: {model_db_backup}")
        if args.disable_remote_compaction:
            if config_backup:
                print(f"config.toml backup: {config_backup}")
                print("Remote compaction disabled (remote_compaction_v2 = false under [features]).")
            else:
                print("Remote compaction already disabled in config.toml; no change.")
        print("Post-repair report:")
        print_report(inspect_session(codex_home, args.session_id), args.json)
        return 0
    except (OSError, ValueError, FileNotFoundError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
