"""HTTP access log: visitor IP + UTC timestamp, 30-day retention.

Implements the retention commitment published in PRIVACY_POLICY.md:
IP access logs are kept for a maximum of ACCESS_LOG_RETENTION_DAYS days for
anti-DDoS protection and rate limiting, then purged automatically.

The store is SQLite (same auto-commit/close pattern as the task store, so
Windows file locks are never leaked). ":memory:" keeps everything in RAM
(tests / ephemeral deployments).
"""

from __future__ import annotations

import logging
import sqlite3
import threading
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import UTC, datetime, timedelta
from pathlib import Path

logger = logging.getLogger("agentSAFE.web.access_log")

ACCESS_LOG_RETENTION_DAYS = 30

_SCHEMA = """
CREATE TABLE IF NOT EXISTS access_log (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    ts      TEXT NOT NULL,
    ip      TEXT NOT NULL,
    method  TEXT NOT NULL,
    path    TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_access_log_ts ON access_log (ts);
"""


class AccessLogStore:
    """Persistent access log with bounded retention."""

    def __init__(self, db_path: str = "data/access_log.db") -> None:
        self._db_path = db_path
        if db_path != ":memory:":
            Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as conn:
            conn.executescript(_SCHEMA)
        self._lock = threading.Lock()

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        conn = sqlite3.connect(self._db_path)
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def log(self, ip: str, method: str, path: str, *, when: datetime | None = None) -> None:
        """Record one request. `when` is injectable for retention tests."""
        ts = (when or datetime.now(UTC)).isoformat()
        with self._lock, self._connect() as conn:
            conn.execute(
                "INSERT INTO access_log (ts, ip, method, path) VALUES (?, ?, ?, ?)",
                (ts, ip, method, path),
            )

    def purge(self, days: int = ACCESS_LOG_RETENTION_DAYS, *, now: datetime | None = None) -> int:
        """Delete entries older than `days`; returns the number removed."""
        cutoff = ((now or datetime.now(UTC)) - timedelta(days=days)).isoformat()
        with self._lock, self._connect() as conn:
            cur = conn.execute("DELETE FROM access_log WHERE ts < ?", (cutoff,))
            return cur.rowcount

    def count(self) -> int:
        with self._connect() as conn:
            return int(conn.execute("SELECT COUNT(*) FROM access_log").fetchone()[0])

    def entries(self, limit: int = 100) -> list[dict[str, str]]:
        with self._connect() as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT ts, ip, method, path FROM access_log ORDER BY id DESC LIMIT ?",
                (limit,),
            ).fetchall()
        return [dict(r) for r in rows]


class AccessLogMiddleware:
    """Pure-ASGI middleware that records visitor IP + time for every HTTP
    request (see PRIVACY_POLICY.md - IP logs, 30-day retention, anti-DDoS).

    Behind a reverse proxy the client IP is taken from X-Forwarded-For
    (first hop); otherwise the transport peer address is used.
    """

    def __init__(self, app, store: AccessLogStore) -> None:
        self.app = app
        self.store = store

    async def __call__(self, scope, receive, send) -> None:
        if scope["type"] == "http":
            self.store.log(self._client_ip(scope), scope.get("method", "?"), scope.get("path", "?"))
        await self.app(scope, receive, send)

    @staticmethod
    def _client_ip(scope) -> str:
        for name, value in scope.get("headers", []):
            if name == b"x-forwarded-for":
                first = value.decode("latin-1", "replace").split(",")[0].strip()
                if first:
                    return first
        client = scope.get("client")
        return client[0] if client else "unknown"
