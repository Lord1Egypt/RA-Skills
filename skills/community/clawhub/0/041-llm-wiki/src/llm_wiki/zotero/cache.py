"""Small SQLite cache for Zotero metadata enrichment requests."""

from __future__ import annotations

import json
import sqlite3
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Self


class EnrichmentCache:
    """Store only the latest result for each item/provider operation."""

    def __init__(self, path: Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._connection = sqlite3.connect(self.path)
        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS enrichment_cache (
                item_key TEXT NOT NULL,
                provider TEXT NOT NULL,
                operation TEXT NOT NULL,
                checked_at TEXT NOT NULL,
                status TEXT NOT NULL,
                value_json TEXT,
                error TEXT,
                PRIMARY KEY (item_key, provider, operation)
            )
            """
        )
        self._connection.commit()

    def close(self) -> None:
        self._connection.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        self.close()

    def get_json(
        self,
        item_key: str,
        provider: str,
        operation: str,
        *,
        max_age_days: int,
        now: datetime | None = None,
    ) -> Any | None:
        row = self._connection.execute(
            """
            SELECT checked_at, status, value_json
            FROM enrichment_cache
            WHERE item_key = ? AND provider = ? AND operation = ?
            """,
            (item_key, provider, operation),
        ).fetchone()
        if not row or row[1] != "ok" or not row[2]:
            return None

        checked_at = datetime.fromisoformat(row[0])
        if checked_at.tzinfo is None:
            checked_at = checked_at.replace(tzinfo=UTC)
        current = now or datetime.now(UTC)
        if current - checked_at > timedelta(days=max_age_days):
            return None
        return json.loads(row[2])

    def put_json(
        self,
        item_key: str,
        provider: str,
        operation: str,
        value: Any,
        *,
        checked_at: datetime | None = None,
    ) -> None:
        timestamp = (checked_at or datetime.now(UTC)).isoformat()
        self._connection.execute(
            """
            INSERT INTO enrichment_cache (
                item_key, provider, operation, checked_at, status, value_json, error
            ) VALUES (?, ?, ?, ?, 'ok', ?, NULL)
            ON CONFLICT(item_key, provider, operation) DO UPDATE SET
                checked_at = excluded.checked_at,
                status = excluded.status,
                value_json = excluded.value_json,
                error = NULL
            """,
            (
                item_key,
                provider,
                operation,
                timestamp,
                json.dumps(value, ensure_ascii=False),
            ),
        )
        self._connection.commit()

    def put_error(
        self,
        item_key: str,
        provider: str,
        operation: str,
        error: str,
        *,
        checked_at: datetime | None = None,
    ) -> None:
        timestamp = (checked_at or datetime.now(UTC)).isoformat()
        self._connection.execute(
            """
            INSERT INTO enrichment_cache (
                item_key, provider, operation, checked_at, status, value_json, error
            ) VALUES (?, ?, ?, ?, 'error', NULL, ?)
            ON CONFLICT(item_key, provider, operation) DO UPDATE SET
                checked_at = excluded.checked_at,
                status = excluded.status,
                value_json = NULL,
                error = excluded.error
            """,
            (item_key, provider, operation, timestamp, error[:1000]),
        )
        self._connection.commit()
