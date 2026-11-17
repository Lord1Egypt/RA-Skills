from __future__ import annotations

import json
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Mapping, Optional


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class SubmissionStore:
    JSON_COLUMNS = {
        "event_json",
        "invoice_json",
        "approval_request_json",
        "approval_response_json",
    }
    ALLOWED_COLUMNS = {
        "status",
        "updated_at",
        "image_path",
        "image_sha256",
        "invoice_fingerprint",
        "invoice_json",
        "approval_uuid",
        "approval_request_json",
        "approval_response_json",
        "instance_code",
        "card_message_id",
        "decision_event_id",
        "decision_operator_id",
        "decision_action",
        "error",
        "reply_error",
    }

    def __init__(self, path: Path) -> None:
        path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        self.path = path
        self.connection = sqlite3.connect(str(path))
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA journal_mode=WAL")
        self.connection.execute("PRAGMA foreign_keys=ON")
        self._create_schema()
        try:
            os.chmod(path, 0o600)
        except OSError:
            pass

    def _create_schema(self) -> None:
        self.connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS submission_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id TEXT NOT NULL UNIQUE,
                message_id TEXT NOT NULL UNIQUE,
                chat_id TEXT,
                sender_open_id TEXT,
                event_json TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                image_path TEXT,
                image_sha256 TEXT,
                invoice_fingerprint TEXT,
                invoice_json TEXT,
                approval_uuid TEXT,
                approval_request_json TEXT,
                approval_response_json TEXT,
                instance_code TEXT,
                card_message_id TEXT,
                decision_event_id TEXT,
                decision_operator_id TEXT,
                decision_action TEXT,
                error TEXT,
                reply_error TEXT
            );
            CREATE INDEX IF NOT EXISTS idx_submission_fingerprint
                ON submission_records(invoice_fingerprint, status);
            CREATE INDEX IF NOT EXISTS idx_submission_created
                ON submission_records(created_at);
            """
        )
        # 兼容功能升级前已经创建的数据库。
        existing_columns = {
            str(row["name"])
            for row in self.connection.execute(
                "PRAGMA table_info(submission_records)"
            ).fetchall()
        }
        migrations = {
            "card_message_id": "TEXT",
            "decision_event_id": "TEXT",
            "decision_operator_id": "TEXT",
            "decision_action": "TEXT",
        }
        for column, sql_type in migrations.items():
            if column not in existing_columns:
                self.connection.execute(
                    f"ALTER TABLE submission_records ADD COLUMN {column} {sql_type}"
                )
        self.connection.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS idx_submission_card_message
                ON submission_records(card_message_id)
                WHERE card_message_id IS NOT NULL
            """
        )
        self.connection.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS idx_submission_decision_event
                ON submission_records(decision_event_id)
                WHERE decision_event_id IS NOT NULL
            """
        )
        self.connection.commit()

    def begin(self, event: Mapping[str, Any]) -> bool:
        event_id = str(event.get("event_id") or f"message:{event['message_id']}")
        now = _now()
        try:
            self.connection.execute(
                """
                INSERT INTO submission_records (
                    event_id, message_id, chat_id, sender_open_id,
                    event_json, status, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, 'received', ?, ?)
                """,
                (
                    event_id,
                    str(event["message_id"]),
                    event.get("chat_id"),
                    event.get("sender_id"),
                    json.dumps(event, ensure_ascii=False, separators=(",", ":")),
                    now,
                    now,
                ),
            )
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def update(self, message_id: str, **values: Any) -> None:
        invalid = set(values) - self.ALLOWED_COLUMNS
        if invalid:
            raise ValueError(f"不可更新的字段：{sorted(invalid)}")
        values["updated_at"] = _now()
        encoded: Dict[str, Any] = {}
        for key, value in values.items():
            if key in self.JSON_COLUMNS and value is not None and not isinstance(value, str):
                encoded[key] = json.dumps(
                    value, ensure_ascii=False, separators=(",", ":")
                )
            else:
                encoded[key] = value
        assignments = ", ".join(f"{key} = ?" for key in encoded)
        params = [*encoded.values(), message_id]
        self.connection.execute(
            f"UPDATE submission_records SET {assignments} WHERE message_id = ?",
            params,
        )
        self.connection.commit()

    def duplicate_instance(
        self, fingerprint: str, current_message_id: str
    ) -> Optional[str]:
        row = self.connection.execute(
            """
            SELECT instance_code
            FROM submission_records
            WHERE invoice_fingerprint = ?
              AND message_id != ?
              AND status = 'submitted'
              AND instance_code IS NOT NULL
            ORDER BY id DESC
            LIMIT 1
            """,
            (fingerprint, current_message_id),
        ).fetchone()
        return str(row["instance_code"]) if row else None

    def get(self, message_id: str) -> Optional[Dict[str, Any]]:
        row = self.connection.execute(
            "SELECT * FROM submission_records WHERE message_id = ?", (message_id,)
        ).fetchone()
        return dict(row) if row else None

    def claim_decision(
        self,
        message_id: str,
        *,
        card_message_id: str,
        event_id: str,
        operator_id: str,
        action: str,
    ) -> bool:
        """原子认领一次卡片决策，防止重复点击或他人操作。"""

        now = _now()
        try:
            cursor = self.connection.execute(
                """
                UPDATE submission_records
                SET status = 'decision_processing',
                    decision_event_id = ?,
                    decision_operator_id = ?,
                    decision_action = ?,
                    updated_at = ?
                WHERE message_id = ?
                  AND card_message_id = ?
                  AND sender_open_id = ?
                  AND status = 'pending_confirmation'
                  AND decision_event_id IS NULL
                """,
                (
                    event_id,
                    operator_id,
                    action,
                    now,
                    message_id,
                    card_message_id,
                    operator_id,
                ),
            )
            self.connection.commit()
            return cursor.rowcount == 1
        except sqlite3.IntegrityError:
            self.connection.rollback()
            return False

    def recent(self, limit: int = 20) -> list[Dict[str, Any]]:
        rows = self.connection.execute(
            """
            SELECT id, message_id, sender_open_id, status, created_at,
                   invoice_fingerprint, instance_code, error
            FROM submission_records
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
        return [dict(row) for row in rows]

    def close(self) -> None:
        self.connection.close()
