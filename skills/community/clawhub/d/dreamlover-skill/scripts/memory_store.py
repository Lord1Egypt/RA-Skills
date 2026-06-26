from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def default_data_root() -> Path:
    return repo_root() / ".dreamlover-data"


def resolve_data_root(value: str | None) -> Path:
    if not value:
        return default_data_root()
    path = Path(value)
    return path if path.is_absolute() else repo_root() / path


def db_path(data_root_value: str | None = None) -> Path:
    root = resolve_data_root(data_root_value)
    root.mkdir(parents=True, exist_ok=True)
    return root / "memory.sqlite3"


def connect_memory_db(data_root_value: str | None = None) -> sqlite3.Connection:
    connection = sqlite3.connect(db_path(data_root_value))
    connection.row_factory = sqlite3.Row
    ensure_schema(connection)
    return connection


def ensure_schema(connection: sqlite3.Connection) -> None:
    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS profile_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            character_slug TEXT NOT NULL,
            user_id TEXT NOT NULL,
            memory_key TEXT NOT NULL,
            memory_value TEXT NOT NULL,
            confidence REAL NOT NULL DEFAULT 1.0,
            source TEXT NOT NULL DEFAULT '',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            UNIQUE(character_slug, user_id, memory_key)
        );

        CREATE TABLE IF NOT EXISTS episodic_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            character_slug TEXT NOT NULL,
            user_id TEXT NOT NULL,
            summary TEXT NOT NULL,
            event_type TEXT NOT NULL DEFAULT 'event',
            emotional_intensity INTEGER NOT NULL DEFAULT 0,
            source_excerpt TEXT NOT NULL DEFAULT '',
            created_at TEXT NOT NULL,
            summarized INTEGER NOT NULL DEFAULT 0,
            summary_id INTEGER
        );

        CREATE TABLE IF NOT EXISTS relationship_state (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            character_slug TEXT NOT NULL,
            user_id TEXT NOT NULL,
            relationship_label TEXT NOT NULL DEFAULT '',
            trust_level INTEGER NOT NULL DEFAULT 0,
            closeness_level INTEGER NOT NULL DEFAULT 0,
            status_summary TEXT NOT NULL DEFAULT '',
            updated_at TEXT NOT NULL,
            UNIQUE(character_slug, user_id)
        );

        CREATE TABLE IF NOT EXISTS conversation_summary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            character_slug TEXT NOT NULL,
            user_id TEXT NOT NULL,
            turn_start INTEGER NOT NULL,
            turn_end INTEGER NOT NULL,
            summary TEXT NOT NULL,
            created_at TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_profile_memory_lookup
        ON profile_memory(character_slug, user_id, updated_at DESC);

        CREATE INDEX IF NOT EXISTS idx_episodic_memory_lookup
        ON episodic_memory(character_slug, user_id, summarized, created_at DESC);

        CREATE INDEX IF NOT EXISTS idx_conversation_summary_lookup
        ON conversation_summary(character_slug, user_id, created_at DESC);
        """
    )
    connection.commit()


def count_unsummarized_episodes(connection: sqlite3.Connection, character_slug: str, user_id: str) -> int:
    row = connection.execute(
        """
        SELECT COUNT(*) AS total
        FROM episodic_memory
        WHERE character_slug = ? AND user_id = ? AND summarized = 0
        """,
        (character_slug, user_id),
    ).fetchone()
    return int(row["total"] if row else 0)

