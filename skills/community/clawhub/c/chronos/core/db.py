"""Database layer with connection pooling and caching."""
import sqlite3
from functools import lru_cache
from typing import Optional

from .paths import TODO_DB


TASK_SCHEMA_COLUMNS = {
    'reminder_template': "ALTER TABLE periodic_tasks ADD COLUMN reminder_template TEXT",
    'last_reminder_error': "ALTER TABLE periodic_tasks ADD COLUMN last_reminder_error TEXT",
    'reminder_error_count': "ALTER TABLE periodic_tasks ADD COLUMN reminder_error_count INTEGER DEFAULT 0",
    'last_reminder_error_at': "ALTER TABLE periodic_tasks ADD COLUMN last_reminder_error_at TIMESTAMP",
    'task_kind': "ALTER TABLE periodic_tasks ADD COLUMN task_kind TEXT NOT NULL DEFAULT 'scheduled'",
    'source': "ALTER TABLE periodic_tasks ADD COLUMN source TEXT NOT NULL DEFAULT 'chronos'",
    'legacy_entry_id': "ALTER TABLE periodic_tasks ADD COLUMN legacy_entry_id INTEGER",
    'special_handler': "ALTER TABLE periodic_tasks ADD COLUMN special_handler TEXT",
    'handler_payload': "ALTER TABLE periodic_tasks ADD COLUMN handler_payload TEXT",
    'start_date': "ALTER TABLE periodic_tasks ADD COLUMN start_date TEXT",
    'delivery_target': "ALTER TABLE periodic_tasks ADD COLUMN delivery_target TEXT",
    'delivery_mode': "ALTER TABLE periodic_tasks ADD COLUMN delivery_mode TEXT",
    'dates_list': "ALTER TABLE periodic_tasks ADD COLUMN dates_list TEXT",
    'interval_hours': "ALTER TABLE periodic_tasks ADD COLUMN interval_hours INTEGER",
}

OCCURRENCE_SCHEMA_COLUMNS = {
    'completion_mode': "ALTER TABLE periodic_occurrences ADD COLUMN completion_mode TEXT",
    'special_handler_result': "ALTER TABLE periodic_occurrences ADD COLUMN special_handler_result TEXT",
    'scheduled_time': "ALTER TABLE periodic_occurrences ADD COLUMN scheduled_time TEXT",
    'scheduled_at': "ALTER TABLE periodic_occurrences ADD COLUMN scheduled_at TEXT",
    'legacy_entry_id': "ALTER TABLE periodic_occurrences ADD COLUMN legacy_entry_id INTEGER",
}


class DB:
    """Singleton database connection with query caching."""
    _instance: Optional['DB'] = None
    _conn: Optional[sqlite3.Connection] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._conn is None:
            TODO_DB.parent.mkdir(parents=True, exist_ok=True)
            self._conn = sqlite3.connect(str(TODO_DB))
            self._conn.row_factory = sqlite3.Row
            try:
                ensure_schema(self)
            except sqlite3.Error as exc:
                print(f"Warning: failed to ensure schema: {exc}")

    def execute(self, query: str, params: tuple = ()):
        cur = self._conn.cursor()
        cur.execute(query, params)
        return cur

    def executemany(self, query: str, params_list: list):
        cur = self._conn.cursor()
        cur.executemany(query, params_list)
        return cur

    def commit(self):
        self._conn.commit()

    def close(self):
        if self._conn:
            self._conn.close()
            self._conn = None


# Convenience functions
def db_execute(query: str, params: tuple = ()):
    return DB().execute(query, params)


def db_commit():
    DB().commit()


@lru_cache(maxsize=128)
def get_periodic_tasks(active_only: bool = True):
    """Fetch all periodic tasks (cached)."""
    query = "SELECT * FROM periodic_tasks"
    if active_only:
        query += " WHERE is_active = 1"
    cur = DB().execute(query)
    rows = cur.fetchall()
    return [dict(row) for row in rows]


@lru_cache(maxsize=128)
def get_periodic_task(task_id: int):
    """Fetch single task by ID (cached)."""
    cur = DB().execute("SELECT * FROM periodic_tasks WHERE id = ?", (task_id,))
    row = cur.fetchone()
    return dict(row) if row else None


def clear_task_cache():
    """Clear task cache (called after updates)."""
    get_periodic_tasks.cache_clear()
    get_periodic_task.cache_clear()


def _ensure_table_columns(db: DB, table_name: str, statements: dict[str, str]) -> None:
    cur = db.execute(f"PRAGMA table_info({table_name})")
    columns = {row[1] for row in cur.fetchall()}
    changed = False
    for column_name, statement in statements.items():
        if column_name not in columns:
            db.execute(statement)
            changed = True
    if changed:
        db.commit()


def _get_table_sql(db: DB, table_name: str) -> str:
    row = db.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name = ?", (table_name,)).fetchone()
    return row[0] if row and row[0] else ""


def _rebuild_occurrences_for_hourly(db: DB) -> None:
    sql = _get_table_sql(db, 'periodic_occurrences')
    if 'UNIQUE(task_id, date, scheduled_time)' in sql:
        return

    db.execute("ALTER TABLE periodic_occurrences RENAME TO periodic_occurrences_old")
    db.execute(
        """
        CREATE TABLE periodic_occurrences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            reminder_job_id TEXT,
            is_auto_completed BOOLEAN DEFAULT 0,
            completed_at TEXT,
            completion_mode TEXT,
            special_handler_result TEXT,
            scheduled_time TEXT,
            scheduled_at TEXT,
            legacy_entry_id INTEGER,
            FOREIGN KEY (task_id) REFERENCES periodic_tasks(id) ON DELETE CASCADE,
            UNIQUE(task_id, date, scheduled_time)
        )
        """
    )
    db.execute(
        """
        INSERT INTO periodic_occurrences (
            id, task_id, date, status, reminder_job_id, is_auto_completed, completed_at,
            completion_mode, special_handler_result, scheduled_time, scheduled_at, legacy_entry_id
        )
        SELECT
            id, task_id, date, status, reminder_job_id, COALESCE(is_auto_completed, 0), completed_at,
            completion_mode, special_handler_result, scheduled_time, scheduled_at, legacy_entry_id
        FROM periodic_occurrences_old
        """
    )
    db.execute("DROP TABLE periodic_occurrences_old")
    db.commit()


def ensure_schema(db: Optional[DB] = None):
    """Ensure database schema has all phase-1 Chronos columns."""
    db = db or DB()

    tasks_table = db.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='periodic_tasks'"
    ).fetchone()
    if tasks_table:
        _ensure_table_columns(db, 'periodic_tasks', TASK_SCHEMA_COLUMNS)

    occurrences_table = db.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='periodic_occurrences'"
    ).fetchone()
    if occurrences_table:
        _ensure_table_columns(db, 'periodic_occurrences', OCCURRENCE_SCHEMA_COLUMNS)
        _rebuild_occurrences_for_hourly(db)
