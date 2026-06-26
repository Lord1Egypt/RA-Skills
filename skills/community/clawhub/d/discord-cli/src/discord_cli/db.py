"""SQLite database for storing Discord chat messages."""

from __future__ import annotations

import json
import logging
import sqlite3
from datetime import datetime, timedelta, timezone, tzinfo
from pathlib import Path
from typing import Any

from .config import get_db_path

log = logging.getLogger(__name__)

_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS messages (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    platform      TEXT    NOT NULL DEFAULT 'discord',
    guild_id      TEXT,
    guild_name    TEXT,
    channel_id    TEXT    NOT NULL,
    channel_name  TEXT,
    msg_id        TEXT    NOT NULL,
    sender_id     TEXT,
    sender_name   TEXT,
    content       TEXT,
    timestamp     TEXT    NOT NULL,
    raw_json      TEXT,
    UNIQUE(platform, channel_id, msg_id)
);
"""

_CREATE_INDEX = """
CREATE INDEX IF NOT EXISTS idx_messages_channel_ts ON messages(channel_id, timestamp);
CREATE INDEX IF NOT EXISTS idx_messages_content ON messages(content);
CREATE INDEX IF NOT EXISTS idx_messages_sender ON messages(sender_name);
CREATE INDEX IF NOT EXISTS idx_messages_guild ON messages(guild_id);
"""


class ChannelResolutionError(ValueError):
    """Base error for channel lookup failures."""


class ChannelNotFoundError(ChannelResolutionError):
    """Raised when a channel cannot be found in local storage."""

    def __init__(self, query: str):
        super().__init__(f"Channel '{query}' not found in database.")


class AmbiguousChannelError(ChannelResolutionError):
    """Raised when a channel query matches multiple stored channels."""

    def __init__(self, query: str, matches: list[dict]):
        preview = ", ".join(_format_channel_match(match) for match in matches[:5])
        if len(matches) > 5:
            preview += ", ..."
        super().__init__(
            f"Channel '{query}' is ambiguous. Matches: {preview}. "
            "Use a more specific name or a channel ID."
        )
        self.matches = matches


def _format_channel_match(channel: dict) -> str:
    """Format a channel record for error messages."""
    name = channel.get("channel_name") or channel.get("channel_id") or "unknown"
    guild = channel.get("guild_name")
    if guild:
        return f"{guild} > #{name} ({channel['channel_id']})"
    return f"#{name} ({channel['channel_id']})"


class MessageDB:
    """SQLite message store with context manager support."""

    def __init__(self, db_path: Path | str | None = None):
        if db_path is None:
            self.db_path = get_db_path()
        else:
            self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.executescript(_CREATE_TABLE + _CREATE_INDEX)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False

    def insert_batch(self, messages: list[dict], platform: str = "discord") -> int:
        """Batch insert messages. Returns rows actually inserted (excluding dupes)."""
        if not messages:
            return 0
        rows = [
            (
                platform,
                m.get("guild_id"),
                m.get("guild_name"),
                m["channel_id"],
                m.get("channel_name"),
                m["msg_id"],
                m.get("sender_id"),
                m.get("sender_name"),
                m.get("content"),
                m["timestamp"].isoformat() if isinstance(m["timestamp"], datetime) else m["timestamp"],
                json.dumps(m["raw_json"], ensure_ascii=False) if m.get("raw_json") else None,
            )
            for m in messages
        ]
        try:
            before = self.conn.total_changes
            self.conn.executemany(
                """INSERT OR IGNORE INTO messages
                   (platform, guild_id, guild_name, channel_id, channel_name,
                    msg_id, sender_id, sender_name, content, timestamp, raw_json)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                rows,
            )
            self.conn.commit()
            return self.conn.total_changes - before
        except sqlite3.Error as e:
            log.warning("insert_batch failed: %s", e)
            return 0

    def resolve_channel_id(self, channel_str: str) -> str | None:
        """Resolve a channel string (name or ID) to a database channel_id.

        Returns None if not found in the database.
        """
        try:
            return self.resolve_channel(channel_str)["channel_id"]
        except ChannelResolutionError:
            return None

    def find_channels(self, channel_str: str) -> list[dict]:
        """Find candidate stored channels by ID, exact name, or partial name."""
        channels = self.get_channels()
        query = channel_str.lower()

        exact_id_matches = [c for c in channels if c["channel_id"] == channel_str]
        if exact_id_matches:
            return exact_id_matches

        exact_name_matches = [
            c
            for c in channels
            if c.get("channel_name") and c["channel_name"].lower() == query
        ]
        if exact_name_matches:
            return exact_name_matches

        return [
            c
            for c in channels
            if c.get("channel_name") and query in c["channel_name"].lower()
        ]

    def resolve_channel(self, channel_str: str) -> dict:
        """Resolve a stored channel, rejecting missing or ambiguous matches."""
        matches = self.find_channels(channel_str)
        if not matches:
            raise ChannelNotFoundError(channel_str)
        if len(matches) > 1:
            raise AmbiguousChannelError(channel_str, matches)
        return matches[0]

    def search(
        self,
        keyword: str,
        channel_id: str | None = None,
        limit: int = 50,
    ) -> list[dict]:
        """Search messages by keyword."""
        query = "SELECT * FROM messages WHERE content LIKE ?"
        params: list[Any] = [f"%{keyword}%"]
        if channel_id:
            query += " AND channel_id = ?"
            params.append(channel_id)
        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)
        rows = self.conn.execute(query, params).fetchall()
        return [dict(r) for r in rows]

    def get_recent(
        self,
        channel_id: str | None = None,
        hours: int | None = 24,
        limit: int = 500,
    ) -> list[dict]:
        """Get recent messages in chronological order."""
        if hours is not None:
            cutoff = (datetime.now(timezone.utc) - timedelta(hours=hours)).isoformat()
            query = "SELECT * FROM messages WHERE timestamp >= ?"
            params: list[Any] = [cutoff]
        else:
            query = "SELECT * FROM messages WHERE 1=1"
            params = []
        if channel_id:
            query += " AND channel_id = ?"
            params.append(channel_id)
        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)
        rows = self.conn.execute(query, params).fetchall()
        return [dict(r) for r in reversed(rows)]

    def get_latest(
        self,
        channel_id: str | None = None,
        hours: int | None = None,
        limit: int = 50,
    ) -> list[dict]:
        """Get the most recent messages, returned in chronological order."""
        query = "SELECT * FROM messages WHERE 1=1"
        params: list[Any] = []
        if channel_id:
            query += " AND channel_id = ?"
            params.append(channel_id)
        if hours is not None:
            cutoff = (datetime.now(timezone.utc) - timedelta(hours=hours)).isoformat()
            query += " AND timestamp >= ?"
            params.append(cutoff)
        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)
        rows = self.conn.execute(query, params).fetchall()
        return [dict(r) for r in reversed(rows)]

    def get_today(
        self,
        channel_id: str | None = None,
        tz: tzinfo | None = None,
        limit: int = 5000,
        now: datetime | None = None,
    ) -> list[dict]:
        """Get today's messages (in local timezone)."""
        now_utc = now.astimezone(timezone.utc) if now else datetime.now(timezone.utc)
        local_tz = tz or datetime.now().astimezone().tzinfo or timezone.utc
        today_local = now_utc.astimezone(local_tz).replace(hour=0, minute=0, second=0, microsecond=0)
        cutoff_utc = today_local.astimezone(timezone.utc).isoformat()

        query = "SELECT * FROM messages WHERE timestamp >= ?"
        params: list[Any] = [cutoff_utc]
        if channel_id:
            query += " AND channel_id = ?"
            params.append(channel_id)
        query += " ORDER BY channel_name, timestamp ASC LIMIT ?"
        params.append(limit)
        rows = self.conn.execute(query, params).fetchall()
        return [dict(r) for r in rows]

    def get_channels(self) -> list[dict]:
        """Get all known channels with message counts."""
        rows = self.conn.execute(
            """SELECT channel_id, channel_name, guild_id, guild_name,
                      COUNT(*) as msg_count,
                      MIN(timestamp) as first_msg, MAX(timestamp) as last_msg
               FROM messages
               GROUP BY channel_id
               ORDER BY msg_count DESC"""
        ).fetchall()
        return [dict(r) for r in rows]

    def get_last_msg_id(self, channel_id: str) -> str | None:
        """Get the latest msg_id for a channel, used for incremental sync."""
        row = self.conn.execute(
            "SELECT MAX(msg_id) FROM messages WHERE channel_id = ?", (channel_id,)
        ).fetchone()
        return row[0] if row and row[0] is not None else None

    def count(self, channel_id: str | None = None) -> int:
        if channel_id:
            row = self.conn.execute(
                "SELECT COUNT(*) FROM messages WHERE channel_id = ?", (channel_id,)
            ).fetchone()
        else:
            row = self.conn.execute("SELECT COUNT(*) FROM messages").fetchone()
        return row[0]

    def delete_channel(self, channel_id: str) -> int:
        """Delete all messages for a channel. Returns number of deleted rows."""
        cursor = self.conn.execute(
            "DELETE FROM messages WHERE channel_id = ?", (channel_id,)
        )
        self.conn.commit()
        return cursor.rowcount

    def top_senders(
        self,
        channel_id: str | None = None,
        hours: int | None = None,
        limit: int = 20,
    ) -> list[dict]:
        """Get most active senders."""
        conditions = ["sender_name IS NOT NULL"]
        params: list[Any] = []
        if channel_id:
            conditions.append("channel_id = ?")
            params.append(channel_id)
        if hours:
            cutoff = (datetime.now(timezone.utc) - timedelta(hours=hours)).isoformat()
            conditions.append("timestamp >= ?")
            params.append(cutoff)

        where = " AND ".join(conditions)
        rows = self.conn.execute(
            f"""SELECT COALESCE(MAX(sender_name), 'Unknown') as sender_name,
                       sender_id,
                       COUNT(*) as msg_count,
                       MIN(timestamp) as first_msg, MAX(timestamp) as last_msg
                FROM messages WHERE {where}
                GROUP BY COALESCE(sender_id, sender_name)
                ORDER BY msg_count DESC
                LIMIT ?""",
            params + [limit],
        ).fetchall()
        return [dict(r) for r in rows]

    def timeline(
        self,
        channel_id: str | None = None,
        hours: int | None = None,
        granularity: str = "day",
    ) -> list[dict]:
        """Get message count grouped by time period."""
        if granularity == "hour":
            time_expr = "substr(timestamp, 1, 13)"  # YYYY-MM-DDTHH
        else:
            time_expr = "substr(timestamp, 1, 10)"  # YYYY-MM-DD

        conditions = ["1=1"]
        params: list[Any] = []
        if channel_id:
            conditions.append("channel_id = ?")
            params.append(channel_id)
        if hours:
            cutoff = (datetime.now(timezone.utc) - timedelta(hours=hours)).isoformat()
            conditions.append("timestamp >= ?")
            params.append(cutoff)

        where = " AND ".join(conditions)
        rows = self.conn.execute(
            f"""SELECT {time_expr} as period, COUNT(*) as msg_count
                FROM messages WHERE {where}
                GROUP BY period
                ORDER BY period ASC""",
            params,
        ).fetchall()
        return [dict(r) for r in rows]

    def close(self):
        self.conn.close()
