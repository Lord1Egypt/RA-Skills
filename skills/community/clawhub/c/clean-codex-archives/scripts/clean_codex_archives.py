#!/usr/bin/env python3
"""Safely remove locally archived Codex conversation data."""

from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


@dataclass(frozen=True)
class IndexEntry:
    session_id: str
    line: str


def resolve_codex_home(requested: str | None) -> Path:
    candidate = requested or os.environ.get("CODEX_HOME") or (Path.home() / ".codex")
    root = Path(candidate).expanduser().resolve()
    if not root.is_dir():
        raise RuntimeError(f"Codex data directory does not exist: {root}")
    return root


def connect(database: Path, *, read_only: bool = False) -> sqlite3.Connection:
    if read_only:
        uri_path = str(database.resolve()).replace("\\", "/")
        uri = f"file:{uri_path}?mode=ro"
        return sqlite3.connect(uri, uri=True)
    return sqlite3.connect(database)


def table_names(database: Path) -> set[str]:
    if not database.is_file():
        return set()
    with connect(database, read_only=True) as connection:
        rows = connection.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
    return {str(row[0]) for row in rows}


def scalar(database: Path, sql: str, parameters: Sequence[object] = ()) -> object:
    with connect(database, read_only=True) as connection:
        row = connection.execute(sql, parameters).fetchone()
    return None if row is None else row[0]


def ids(database: Path, sql: str) -> list[str]:
    with connect(database, read_only=True) as connection:
        rows = connection.execute(sql).fetchall()
    return [str(row[0]) for row in rows if row[0] is not None]


def count_for_ids(
    database: Path,
    table: str,
    column: str,
    session_ids: Sequence[str],
) -> int:
    if not session_ids or table not in table_names(database):
        return 0
    total = 0
    for offset in range(0, len(session_ids), 500):
        batch = session_ids[offset : offset + 500]
        placeholders = ",".join("?" for _ in batch)
        sql = f"SELECT COUNT(*) FROM {table} WHERE {column} IN ({placeholders})"
        total += int(scalar(database, sql, batch) or 0)
    return total


def delete_for_ids(
    connection: sqlite3.Connection,
    table: str,
    column: str,
    session_ids: Sequence[str],
) -> int:
    if not session_ids:
        return 0
    total = 0
    for offset in range(0, len(session_ids), 500):
        batch = session_ids[offset : offset + 500]
        placeholders = ",".join("?" for _ in batch)
        sql = f"DELETE FROM {table} WHERE {column} IN ({placeholders})"
        cursor = connection.execute(sql, batch)
        total += cursor.rowcount
    return total


def read_index(path: Path) -> list[IndexEntry]:
    if not path.is_file():
        return []

    entries: list[IndexEntry] = []
    with path.open("r", encoding="utf-8", newline="") as stream:
        for line_number, raw_line in enumerate(stream, start=1):
            line = raw_line.rstrip("\r\n")
            if not line.strip():
                raise RuntimeError(
                    f"Blank line in session index at line {line_number}; refusing to rewrite it"
                )
            try:
                entry = json.loads(line)
            except json.JSONDecodeError as error:
                raise RuntimeError(
                    f"Invalid JSON in session index at line {line_number}; refusing to rewrite it"
                ) from error
            session_id = entry.get("id") if isinstance(entry, dict) else None
            if not isinstance(session_id, str) or not session_id:
                raise RuntimeError(
                    f"Missing session ID in session index at line {line_number}; refusing to rewrite it"
                )
            entries.append(IndexEntry(session_id=session_id, line=line))
    return entries


def write_index(path: Path, lines: Iterable[str]) -> None:
    kept_lines = list(lines)
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        if kept_lines:
            stream.write("\n".join(kept_lines) + "\n")


def quick_check(database: Path) -> str:
    if not database.is_file():
        return "missing"
    result = scalar(database, "PRAGMA quick_check")
    return str(result).strip()


def vacuum(database: Path) -> None:
    if not database.is_file():
        return
    with connect(database) as connection:
        connection.execute("PRAGMA wal_checkpoint(TRUNCATE)")
        connection.execute("VACUUM")


def delete_logs(logs_database: Path, session_ids: Sequence[str]) -> None:
    if not logs_database.is_file() or not session_ids:
        return
    if "logs" not in table_names(logs_database):
        return
    with connect(logs_database) as connection:
        try:
            connection.execute("BEGIN IMMEDIATE")
            delete_for_ids(connection, "logs", "thread_id", session_ids)
            connection.commit()
        except Exception:
            connection.rollback()
            raise


def delete_goals(goals_database: Path, session_ids: Sequence[str]) -> None:
    if not goals_database.is_file() or not session_ids:
        return
    if "thread_goals" not in table_names(goals_database):
        return
    with connect(goals_database) as connection:
        try:
            connection.execute("BEGIN IMMEDIATE")
            delete_for_ids(connection, "thread_goals", "thread_id", session_ids)
            connection.commit()
        except Exception:
            connection.rollback()
            raise


def delete_state(
    state_database: Path,
    session_ids: Sequence[str],
    state_tables: set[str],
) -> None:
    if not session_ids:
        return
    with connect(state_database) as connection:
        try:
            connection.execute("PRAGMA foreign_keys=ON")
            connection.execute("BEGIN IMMEDIATE")
            if "thread_dynamic_tools" in state_tables:
                delete_for_ids(
                    connection, "thread_dynamic_tools", "thread_id", session_ids
                )
            if "thread_spawn_edges" in state_tables:
                delete_for_ids(
                    connection,
                    "thread_spawn_edges",
                    "parent_thread_id",
                    session_ids,
                )
                delete_for_ids(
                    connection,
                    "thread_spawn_edges",
                    "child_thread_id",
                    session_ids,
                )
            connection.execute(
                "DELETE FROM threads WHERE archived=1"
            )
            connection.commit()
        except Exception:
            connection.rollback()
            raise


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inspect or remove locally archived Codex conversation data."
    )
    parser.add_argument(
        "--codex-home",
        help="Codex data directory; defaults to CODEX_HOME or ~/.codex",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply deletion; without this flag the command is a dry run",
    )
    parser.add_argument(
        "--vacuum",
        action="store_true",
        help="Checkpoint and compact modified SQLite databases after deletion",
    )
    return parser.parse_args()


def run(arguments: argparse.Namespace) -> int:
    root = resolve_codex_home(arguments.codex_home)
    archive_directory = root / "archived_sessions"
    state_database = root / "state_5.sqlite"
    logs_database = root / "logs_2.sqlite"
    goals_database = root / "goals_1.sqlite"
    session_index = root / "session_index.jsonl"

    if not state_database.is_file():
        raise RuntimeError(f"Codex state database does not exist: {state_database}")
    state_tables = table_names(state_database)
    if "threads" not in state_tables:
        raise RuntimeError(f"The state database has no threads table: {state_database}")

    active_thread_ids = set(ids(state_database, "SELECT id FROM threads WHERE archived=0"))
    archived_thread_ids = set(ids(state_database, "SELECT id FROM threads WHERE archived=1"))
    index_entries = read_index(session_index)
    stale_index_entries = [
        entry for entry in index_entries if entry.session_id not in active_thread_ids
    ]
    archive_files = (
        sorted(archive_directory.glob("*.jsonl"))
        if archive_directory.is_dir()
        else []
    )

    dynamic_tool_count = count_for_ids(
        state_database,
        "thread_dynamic_tools",
        "thread_id",
        sorted(archived_thread_ids),
    )
    spawn_edge_count = 0
    if "thread_spawn_edges" in state_tables and archived_thread_ids:
        with connect(state_database, read_only=True) as connection:
            edge_rows = connection.execute(
                "SELECT parent_thread_id, child_thread_id FROM thread_spawn_edges"
            ).fetchall()
        spawn_edge_count = sum(
            1
            for parent_id, child_id in edge_rows
            if parent_id in archived_thread_ids or child_id in archived_thread_ids
        )
    log_count = count_for_ids(
        logs_database, "logs", "thread_id", sorted(archived_thread_ids)
    )
    goal_count = count_for_ids(
        goals_database, "thread_goals", "thread_id", sorted(archived_thread_ids)
    )

    print(f"Codex home: {root}")
    print(f"Archive JSONL files: {len(archive_files)}")
    print(f"Archived thread rows: {len(archived_thread_ids)}")
    print(f"Related dynamic-tool rows: {dynamic_tool_count}")
    print(f"Related spawn-edge rows: {spawn_edge_count}")
    print(f"Related log rows: {log_count}")
    print(f"Related goal rows: {goal_count}")
    print(f"Stale session-index rows: {len(stale_index_entries)}")

    if not arguments.apply:
        print("DRY RUN: no changes made. Rerun with --apply after explicit authorization.")
        return 0

    delete_logs(logs_database, sorted(archived_thread_ids))
    delete_goals(goals_database, sorted(archived_thread_ids))
    delete_state(state_database, sorted(archived_thread_ids), state_tables)

    for archive_file in archive_files:
        archive_file.unlink()

    if session_index.is_file():
        post_cleanup_ids = set(ids(state_database, "SELECT id FROM threads"))
        write_index(
            session_index,
            (
                entry.line
                for entry in index_entries
                if entry.session_id in post_cleanup_ids
            ),
        )

    if arguments.vacuum:
        for database in (state_database, logs_database, goals_database):
            vacuum(database)

    archived_after = int(
        scalar(state_database, "SELECT COUNT(*) FROM threads WHERE archived=1") or 0
    )
    files_after = (
        len(list(archive_directory.glob("*.jsonl")))
        if archive_directory.is_dir()
        else 0
    )
    current_after = set(ids(state_database, "SELECT id FROM threads"))
    index_missing_after = 0
    if session_index.is_file():
        index_missing_after = sum(
            1
            for entry in read_index(session_index)
            if entry.session_id not in current_after
        )
    checks = {
        str(database): quick_check(database)
        for database in (state_database, logs_database, goals_database)
        if database.is_file()
    }

    if archived_after != 0 or files_after != 0 or index_missing_after != 0:
        raise RuntimeError(
            "Verification failed: "
            f"archived={archived_after}, archiveFiles={files_after}, "
            f"missingIndexRefs={index_missing_after}"
        )
    bad_checks = {database: result for database, result in checks.items() if result != "ok"}
    if bad_checks:
        raise RuntimeError(f"SQLite quick_check failed: {bad_checks}")

    print(f"Cleanup applied. Archived threads remaining: {archived_after}")
    print(f"Archive JSONL files remaining: {files_after}")
    print(f"Session-index references missing from state: {index_missing_after}")
    for database, result in checks.items():
        print(f"SQLite quick_check ({database}): {result}")
    return 0


def main() -> int:
    try:
        return run(parse_args())
    except (OSError, RuntimeError, sqlite3.Error) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
