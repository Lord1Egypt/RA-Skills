from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from threading import Lock
from uuid import uuid4

import pandas as pd

from app.models import Indicator


@dataclass
class TaskRecord:
    task_id: str
    indicator_id: str
    indicator_name: str
    data: pd.DataFrame
    created_at: datetime
    expires_at: datetime


class InMemoryTaskStore:
    """Small process-local store for the latest extraction result only."""

    def __init__(self, ttl_minutes: int = 30) -> None:
        self._ttl = timedelta(minutes=ttl_minutes)
        self._records: dict[str, TaskRecord] = {}
        self._lock = Lock()

    def create(self, indicator: Indicator, data: pd.DataFrame) -> TaskRecord:
        now = datetime.now(timezone.utc)
        record = TaskRecord(
            task_id=str(uuid4()),
            indicator_id=indicator.id,
            indicator_name=indicator.name,
            data=data.copy(),
            created_at=now,
            expires_at=now + self._ttl,
        )

        with self._lock:
            self._records.clear()
            self._records[record.task_id] = record
        return record

    def get(self, task_id: str) -> TaskRecord | None:
        self.cleanup()
        with self._lock:
            return self._records.get(task_id)

    def delete(self, task_id: str) -> bool:
        with self._lock:
            return self._records.pop(task_id, None) is not None

    def clear(self) -> None:
        with self._lock:
            self._records.clear()

    def cleanup(self) -> None:
        now = datetime.now(timezone.utc)
        with self._lock:
            expired_ids = [
                task_id
                for task_id, record in self._records.items()
                if record.expires_at <= now
            ]
            for task_id in expired_ids:
                self._records.pop(task_id, None)


task_store = InMemoryTaskStore()
