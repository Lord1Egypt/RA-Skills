"""Shared SQLite utilities for the email-only CRM skill."""

from __future__ import annotations

import argparse
import json
import os
import re
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

SCHEMA_VERSION = 1
EVENT_TYPES = ("drafted", "queued", "sent", "delivered", "opened", "replied", "bounced", "failed")
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
DEFAULT_DATA_HOME = Path(os.environ.get("XDG_DATA_HOME") or Path.home() / ".local" / "share")
DEFAULT_DB_PATH = DEFAULT_DATA_HOME / "openclaw-email-crm" / "email_crm.sqlite"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize_email(value: str) -> str:
    normalized = value.strip().lower()
    if not EMAIL_RE.fullmatch(normalized):
        raise ValueError("invalid email address")
    return normalized


def add_db_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--db", help="SQLite database path; defaults to EMAIL_CRM_DB or the per-user data directory")


def add_email_arguments(parser: argparse.ArgumentParser) -> None:
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--email", help="email address (prefer --email-stdin in agent automation)")
    group.add_argument("--email-stdin", action="store_true", help="read the email address from standard input")


def read_email_argument(args: argparse.Namespace) -> str:
    return sys.stdin.read() if args.email_stdin else args.email


def resolve_db_path(value: Optional[str]) -> Path:
    return Path(value or os.environ.get("EMAIL_CRM_DB") or DEFAULT_DB_PATH).expanduser()


def enforce_database_permissions(path: Path) -> None:
    for candidate in (path, Path(f"{path}-wal"), Path(f"{path}-shm"), Path(f"{path}-journal")):
        try:
            candidate.chmod(0o600)
        except FileNotFoundError:
            pass


def connect(db_path: Optional[str]) -> sqlite3.Connection:
    path = resolve_db_path(db_path)
    previous_umask = os.umask(0o077)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(path)
    finally:
        os.umask(previous_umask)
    enforce_database_permissions(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def initialize(conn: sqlite3.Connection) -> int:
    # Compatibility must be established before any DDL or journal-mode change.
    # That keeps an unsupported database byte-for-byte untouched.
    meta_exists = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = 'schema_meta'"
    ).fetchone()
    if meta_exists:
        row = conn.execute("SELECT schema_version FROM schema_meta WHERE singleton = 1").fetchone()
        if row is None:
            raise RuntimeError("database schema metadata is invalid")
        if row["schema_version"] > SCHEMA_VERSION:
            raise RuntimeError("database schema is newer than this skill")
        if row["schema_version"] < SCHEMA_VERSION:
            raise RuntimeError("no migration is available for this database version")

    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS schema_meta (
            singleton INTEGER PRIMARY KEY CHECK (singleton = 1),
            schema_version INTEGER NOT NULL CHECK (schema_version >= 1),
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY,
            email TEXT NOT NULL,
            email_normalized TEXT NOT NULL UNIQUE,
            source TEXT NOT NULL CHECK (length(trim(source)) > 0),
            do_not_contact INTEGER NOT NULL DEFAULT 0 CHECK (do_not_contact IN (0, 1)),
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS email_suppressions (
            id INTEGER PRIMARY KEY,
            email_normalized TEXT NOT NULL UNIQUE,
            reason TEXT NOT NULL CHECK (length(trim(reason)) > 0),
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS email_events (
            id INTEGER PRIMARY KEY,
            contact_id INTEGER NOT NULL REFERENCES contacts(id),
            event_type TEXT NOT NULL CHECK (event_type IN ('drafted', 'queued', 'sent', 'delivered', 'opened', 'replied', 'bounced', 'failed')),
            metadata_json TEXT,
            occurred_at TEXT NOT NULL
        );
        """
    )
    row = conn.execute("SELECT schema_version FROM schema_meta WHERE singleton = 1").fetchone()
    now = utc_now()
    if row is None:
        conn.execute("INSERT INTO schema_meta (singleton, schema_version, updated_at) VALUES (1, ?, ?)", (SCHEMA_VERSION, now))
    conn.commit()
    conn.execute("PRAGMA journal_mode = WAL")
    database_path = conn.execute("PRAGMA database_list").fetchone()[2]
    if database_path:
        enforce_database_permissions(Path(database_path))
    return SCHEMA_VERSION


def require_initialized(conn: sqlite3.Connection) -> None:
    row = conn.execute("SELECT schema_version FROM schema_meta WHERE singleton = 1").fetchone()
    if row is None:
        raise RuntimeError("database is not initialized; run init_email_crm.py first")


def parse_metadata(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    parsed = json.loads(value)
    return json.dumps(parsed, sort_keys=True, separators=(",", ":"))


def emit(payload: dict) -> None:
    print(json.dumps(payload, sort_keys=True))
