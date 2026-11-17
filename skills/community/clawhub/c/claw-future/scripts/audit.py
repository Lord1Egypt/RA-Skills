"""Idempotent management-plane audit ledger."""

from __future__ import annotations

import json
import sqlite3
import threading
import time
from pathlib import Path
from typing import Any, Dict


_REDACTED_KEYS = {
    "password", "td_password", "md_password", "auth_code", "token",
    "confirmation_token",
}


def _sanitise(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            str(key): "[REDACTED]" if str(key).lower() in _REDACTED_KEYS else _sanitise(item)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [_sanitise(item) for item in value]
    return value


class AuditLog:
    def __init__(self, path: Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.RLock()
        self._initialise()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.path), timeout=5.0)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=FULL")
        return conn

    def _initialise(self) -> None:
        with self._lock, self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS audit_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at REAL NOT NULL,
                    actor TEXT NOT NULL,
                    channel TEXT NOT NULL,
                    account_id TEXT NOT NULL,
                    action TEXT NOT NULL,
                    request_key TEXT NOT NULL,
                    request_json TEXT NOT NULL,
                    response_json TEXT NOT NULL,
                    UNIQUE(channel, account_id, action, request_key)
                )
                """
            )

    def record(
        self,
        *,
        actor: str,
        channel: str,
        account_id: str,
        action: str,
        request_key: str,
        request: Dict[str, Any],
        response: Dict[str, Any],
    ) -> None:
        with self._lock, self._connect() as conn:
            conn.execute(
                """
                INSERT OR IGNORE INTO audit_events (
                    created_at, actor, channel, account_id, action,
                    request_key, request_json, response_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    time.time(), actor, channel, account_id, action,
                    request_key,
                    json.dumps(_sanitise(request), ensure_ascii=False, sort_keys=True),
                    json.dumps(_sanitise(response), ensure_ascii=False, sort_keys=True),
                ),
            )
