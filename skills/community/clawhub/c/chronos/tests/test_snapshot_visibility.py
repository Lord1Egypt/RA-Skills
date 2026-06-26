import importlib.util
import os
import sqlite3
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
MANAGER_SCRIPT = PROJECT_ROOT / "scripts" / "periodic_task_manager.py"
MODULE_NAME = "chronos_periodic_task_manager_snapshot_visibility"
CORE_MODULES = [
    "core.paths",
    "core.db",
    "core.scheduler",
    "core.config",
    "core.learning",
    "core.models",
]


def load_manager_module(db_path: Path):
    for name in CORE_MODULES + [MODULE_NAME]:
        sys.modules.pop(name, None)

    os.environ["CHRONOS_DB_PATH"] = str(db_path)
    spec = importlib.util.spec_from_file_location(MODULE_NAME, MANAGER_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def create_test_db(db_path: Path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE groups (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE entries (
            id INTEGER PRIMARY KEY,
            text TEXT NOT NULL,
            status TEXT NOT NULL,
            group_id INTEGER,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE periodic_tasks (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT DEFAULT 'Inbox',
            cycle_type TEXT NOT NULL,
            weekday INTEGER,
            day_of_month INTEGER,
            range_start INTEGER,
            range_end INTEGER,
            n_per_month INTEGER,
            time_of_day TEXT,
            event_time TEXT,
            timezone TEXT DEFAULT 'Asia/Shanghai',
            is_active INTEGER DEFAULT 1,
            count_current_month INTEGER DEFAULT 0,
            end_date TEXT,
            reminder_template TEXT,
            dates_list TEXT,
            task_kind TEXT DEFAULT 'scheduled',
            source TEXT DEFAULT 'chronos',
            legacy_entry_id INTEGER,
            special_handler TEXT,
            handler_payload TEXT,
            start_date TEXT,
            delivery_target TEXT,
            delivery_mode TEXT,
            created_at TEXT,
            updated_at TEXT
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE periodic_occurrences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            reminder_job_id TEXT,
            is_auto_completed INTEGER DEFAULT 0,
            completed_at TEXT,
            completion_mode TEXT,
            special_handler_result TEXT,
            scheduled_time TEXT,
            scheduled_at TEXT,
            legacy_entry_id INTEGER
        )
        """
    )
    conn.commit()
    conn.close()


class TodoSnapshotVisibilityTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.tempdir.name) / "todo.db"
        create_test_db(self.db_path)
        self.module = load_manager_module(self.db_path)
        self.manager = self.module.PeriodicTaskManager()
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("INSERT INTO groups (id, name) VALUES (1, 'Inbox')")
        self.conn.execute(
            "INSERT INTO periodic_tasks (id, name, category, cycle_type, time_of_day, event_time, timezone, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)",
            (1, "活跃周期任务", "Inbox", "daily", "09:00", "09:00", "Asia/Shanghai"),
        )
        self.conn.execute(
            "INSERT INTO periodic_tasks (id, name, category, cycle_type, time_of_day, event_time, timezone, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)",
            (2, "已跳过周期任务", "Inbox", "daily", "10:00", "10:00", "Asia/Shanghai"),
        )
        self.conn.execute(
            "INSERT INTO periodic_occurrences (id, task_id, date, status) VALUES (?, ?, ?, ?)",
            (101, 1, "2026-03-25", "pending"),
        )
        self.conn.execute(
            "INSERT INTO periodic_occurrences (id, task_id, date, status) VALUES (?, ?, ?, ?)",
            (102, 2, "2026-03-25", "skipped"),
        )
        self.conn.execute(
            "INSERT INTO entries (id, text, status, group_id) VALUES (?, ?, ?, ?)",
            (11, "活跃普通任务", "pending", 1),
        )
        self.conn.execute(
            "INSERT INTO entries (id, text, status, group_id) VALUES (?, ?, ?, ?)",
            (12, "已跳过普通任务", "skipped", 1),
        )
        self.conn.execute("ALTER TABLE entries ADD COLUMN chronos_readonly INTEGER NOT NULL DEFAULT 0")
        self.conn.execute("ALTER TABLE entries ADD COLUMN chronos_archived_at TEXT")
        self.conn.execute("ALTER TABLE entries ADD COLUMN chronos_archive_reason TEXT")
        self.conn.execute("ALTER TABLE entries ADD COLUMN chronos_archived_from_status TEXT")
        self.conn.execute("ALTER TABLE entries ADD COLUMN chronos_linked_task_id INTEGER")
        self.conn.execute(
            "INSERT INTO entries (id, text, status, group_id, chronos_readonly, chronos_archived_at, chronos_archive_reason, chronos_archived_from_status, chronos_linked_task_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (13, "已迁移旧周期任务", "archived", 1, 1, "2026-03-25T16:50:00", "Chronos legacy archive: linked to periodic_tasks.id=3", "pending", 3),
        )
        self.conn.execute(
            "INSERT INTO periodic_tasks (id, name, category, cycle_type, time_of_day, event_time, timezone, legacy_entry_id, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)",
            (3, "已迁移旧周期任务", "Inbox", "daily", "11:00", "11:00", "Asia/Shanghai", 13),
        )
        self.conn.execute(
            "INSERT INTO periodic_occurrences (id, task_id, date, status, legacy_entry_id) VALUES (?, ?, ?, ?, ?)",
            (103, 3, "2026-03-25", "pending", 13),
        )
        self.conn.commit()

    def tearDown(self):
        self.conn.close()
        self.manager.db.close()
        self.tempdir.cleanup()
        os.environ.pop("CHRONOS_DB_PATH", None)

    def test_build_today_todo_snapshot_separates_skipped_items(self):
        snapshot = self.manager._build_today_todo_snapshot(date(2026, 3, 25))

        active_section = snapshot.split("【已跳过】", 1)[0]
        self.assertIn("FIN-101", active_section)
        self.assertIn("FIN-103", active_section)
        self.assertIn("ID11", active_section)
        self.assertNotIn("FIN-102", active_section)
        self.assertNotIn("ID12", active_section)
        self.assertNotIn("ID13", active_section)

        self.assertIn("【已跳过】共 2 项（默认不混入活跃待办）", snapshot)
        self.assertIn("FIN-102", snapshot)
        self.assertIn("ID12", snapshot)
        self.assertNotIn("ID13", snapshot)


if __name__ == "__main__":
    unittest.main()
