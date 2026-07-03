# -*- coding: utf-8 -*-
"""Entity / profile memory -- structured facts stored in SQLite.

Corresponds to the "实体画像记忆" layer: facts like "User: 白小纯, Fear: 狗"
are extracted and stored as structured key-value pairs.
This is the "精准记忆" (precision memory) that never fails.
"""

from __future__ import annotations

import sqlite3
from datetime import datetime
from typing import Optional

from .models import Entity


class EntityMemory:
    """Structured key-value store for user facts with confidence scoring.

    Uses SQLite for simplicity -- in production this could be Postgres.
    Supports conflict resolution: newer higher-confidence facts
    replace older lower-confidence ones for the same key.
    """

    def __init__(self, db_path: str = ":memory:") -> None:
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self) -> None:
        self._conn.execute("""
            CREATE TABLE IF NOT EXISTS entities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT NOT NULL,
                value TEXT NOT NULL,
                evidence TEXT DEFAULT '',
                confidence REAL DEFAULT 1.0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        self._conn.execute(
            "CREATE UNIQUE INDEX IF NOT EXISTS idx_entity_key ON entities(key)"
        )
        self._conn.commit()

    def upsert(self, entity: Entity) -> None:
        """Insert or update an entity. Higher confidence wins on conflict."""
        now = datetime.now().isoformat()
        existing = self.get(entity.key)

        if existing and existing.confidence >= entity.confidence:
            # Keep existing higher-confidence fact, but update evidence
            merged_evidence = (
                f"{existing.evidence}; {entity.evidence}"
                if entity.evidence and entity.evidence not in existing.evidence
                else existing.evidence
            )
            self._conn.execute(
                """UPDATE entities SET evidence=?, updated_at=?
                   WHERE key=?""",
                (merged_evidence, now, entity.key),
            )
        else:
            self._conn.execute(
                """INSERT OR REPLACE INTO entities
                   (key, value, evidence, confidence, created_at, updated_at)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (
                    entity.key,
                    entity.value,
                    entity.evidence,
                    entity.confidence,
                    entity.created_at.isoformat(),
                    now,
                ),
            )
        self._conn.commit()

    def get(self, key: str) -> Optional[Entity]:
        row = self._conn.execute(
            "SELECT * FROM entities WHERE key=?", (key,)
        ).fetchone()
        if row is None:
            return None
        return Entity(
            key=row["key"],
            value=row["value"],
            evidence=row["evidence"] or "",
            confidence=row["confidence"],
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
        )

    def get_all(self) -> list[Entity]:
        rows = self._conn.execute(
            "SELECT * FROM entities ORDER BY updated_at DESC"
        ).fetchall()
        return [
            Entity(
                key=r["key"],
                value=r["value"],
                evidence=r["evidence"] or "",
                confidence=r["confidence"],
                created_at=datetime.fromisoformat(r["created_at"]),
                updated_at=datetime.fromisoformat(r["updated_at"]),
            )
            for r in rows
        ]

    def search(self, keyword: str) -> list[Entity]:
        rows = self._conn.execute(
            "SELECT * FROM entities WHERE key LIKE ? OR value LIKE ?",
            (f"%{keyword}%", f"%{keyword}%"),
        ).fetchall()
        return [
            Entity(
                key=r["key"],
                value=r["value"],
                evidence=r["evidence"] or "",
                confidence=r["confidence"],
                created_at=datetime.fromisoformat(r["created_at"]),
                updated_at=datetime.fromisoformat(r["updated_at"]),
            )
            for r in rows
        ]

    def delete(self, key: str) -> None:
        self._conn.execute("DELETE FROM entities WHERE key=?", (key,))
        self._conn.commit()

    def forget_low_confidence(self, threshold: float = 0.3) -> int:
        """Forgetting mechanism: remove stale low-confidence facts."""
        cursor = self._conn.execute(
            "DELETE FROM entities WHERE confidence < ?", (threshold,)
        )
        self._conn.commit()
        return cursor.rowcount
    def count_entities(self) -> int:
        """Return the number of entity cards stored."""
        row = self._conn.execute("SELECT COUNT(*) FROM entities").fetchone()
        return row[0] if row else 0
