from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SCHEMA = '''
CREATE TABLE IF NOT EXISTS reminders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_text TEXT NOT NULL,
    summary TEXT NOT NULL,
    receive_id TEXT NOT NULL,
    receive_id_type TEXT NOT NULL,
    sender_open_id TEXT,
    sender_name TEXT,
    deadline_iso TEXT NOT NULL,
    reminder_iso TEXT NOT NULL,
    confirm_text TEXT NOT NULL,
    reminder_text TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    created_at TEXT NOT NULL,
    sent_at TEXT,
    extra_json TEXT
);
CREATE INDEX IF NOT EXISTS idx_reminders_status_reminder_iso ON reminders(status, reminder_iso);
'''


@dataclass
class Reminder:
    id: int
    source_text: str
    summary: str
    receive_id: str
    receive_id_type: str
    sender_open_id: str | None
    sender_name: str | None
    deadline_iso: str
    reminder_iso: str
    confirm_text: str
    reminder_text: str
    status: str
    created_at: str
    sent_at: str | None
    extra_json: str | None


class ReminderStore:
    def __init__(self, db_path: str | Path) -> None:
        self.db_path = str(db_path)
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.executescript(SCHEMA)
            conn.commit()

    def add(self, payload: dict[str, Any]) -> int:
        with self._connect() as conn:
            cur = conn.execute(
                '''
                INSERT INTO reminders (
                    source_text, summary, receive_id, receive_id_type,
                    sender_open_id, sender_name, deadline_iso, reminder_iso,
                    confirm_text, reminder_text, status, created_at, extra_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending', ?, ?)
                ''',
                (
                    payload['source_text'],
                    payload['summary'],
                    payload['receive_id'],
                    payload['receive_id_type'],
                    payload.get('sender_open_id'),
                    payload.get('sender_name'),
                    payload['deadline_iso'],
                    payload['reminder_iso'],
                    payload['confirm_text'],
                    payload['reminder_text'],
                    payload['created_at'],
                    payload.get('extra_json'),
                ),
            )
            conn.commit()
            return int(cur.lastrowid)

    def list_due(self, now_iso: str) -> list[Reminder]:
        with self._connect() as conn:
            rows = conn.execute(
                '''
                SELECT * FROM reminders
                WHERE status = 'pending' AND reminder_iso <= ?
                ORDER BY reminder_iso ASC, id ASC
                ''',
                (now_iso,),
            ).fetchall()
        return [Reminder(**dict(row)) for row in rows]

    def mark_sent(self, reminder_id: int, sent_at_iso: str) -> None:
        with self._connect() as conn:
            conn.execute(
                'UPDATE reminders SET status = ?, sent_at = ? WHERE id = ?',
                ('sent', sent_at_iso, reminder_id),
            )
            conn.commit()
