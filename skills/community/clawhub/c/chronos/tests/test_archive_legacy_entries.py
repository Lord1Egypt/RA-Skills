import importlib.util
import json
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = PROJECT_ROOT / 'scripts' / 'archive_legacy_entries.py'
MODULE_NAME = 'chronos_archive_legacy_entries'

spec = importlib.util.spec_from_file_location(MODULE_NAME, SCRIPT_PATH)
archive_module = importlib.util.module_from_spec(spec)
sys.modules[MODULE_NAME] = archive_module
spec.loader.exec_module(archive_module)


class LegacyArchiveScriptTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.db_path = Path(self.temp_dir.name) / 'todo.db'
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.executescript(
            """
            CREATE TABLE groups (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            );
            CREATE TABLE entries (
                id INTEGER PRIMARY KEY,
                text TEXT NOT NULL,
                status TEXT NOT NULL,
                group_id INTEGER NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE periodic_tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                category TEXT DEFAULT 'Inbox',
                cycle_type TEXT NOT NULL,
                time_of_day TEXT NOT NULL,
                source TEXT NOT NULL DEFAULT 'chronos',
                legacy_entry_id INTEGER,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
        conn.execute("INSERT INTO groups (id, name) VALUES (1, 'Inbox')")
        conn.execute("INSERT INTO entries (id, text, status, group_id) VALUES (6, '已迁移旧任务', 'pending', 1)")
        conn.execute("INSERT INTO entries (id, text, status, group_id) VALUES (7, '已归档旧任务', 'archived', 1)")
        conn.execute("INSERT INTO periodic_tasks (id, name, category, cycle_type, time_of_day, source, legacy_entry_id) VALUES (13, '已迁移旧任务', 'Inbox', 'daily', '12:00', 'legacy_entries_migrated', 6)")
        conn.execute("INSERT INTO periodic_tasks (id, name, category, cycle_type, time_of_day, source, legacy_entry_id) VALUES (14, '已归档旧任务', 'Inbox', 'daily', '18:00', 'legacy_entries_linked', 7)")
        conn.commit()
        conn.close()

    def test_dry_run_classifies_archive_candidates(self):
        conn = archive_module.connect(str(self.db_path))
        try:
            rows = archive_module.select_linked_rows(conn)
            plans = [archive_module.classify_row(row) for row in rows]
        finally:
            conn.close()

        by_id = {plan.entry_id: plan for plan in plans}
        self.assertEqual(by_id[6].action, 'archive')
        self.assertEqual(by_id[6].task_id, 13)
        self.assertEqual(by_id[7].action, 'repair_archive_metadata')
        self.assertEqual(by_id[7].task_id, 14)

    def test_apply_marks_rows_archived_and_readonly(self):
        conn = archive_module.connect(str(self.db_path))
        try:
            archive_module.ensure_archive_columns(conn)
            rows = archive_module.select_linked_rows(conn)
            plans = [archive_module.classify_row(row) for row in rows]
            applied = [
                archive_module.apply_plan(conn, plan, archived_at='2026-03-25T16:50:00')
                for plan in plans
                if plan.action in {'archive', 'repair_archive_metadata'}
            ]
            conn.commit()
            entry_6 = conn.execute(
                "SELECT status, chronos_readonly, chronos_archived_at, chronos_archived_from_status, chronos_linked_task_id, chronos_archive_reason FROM entries WHERE id = 6"
            ).fetchone()
            entry_7 = conn.execute(
                "SELECT status, chronos_readonly, chronos_archived_at, chronos_archived_from_status, chronos_linked_task_id, chronos_archive_reason FROM entries WHERE id = 7"
            ).fetchone()
            reread_rows = archive_module.select_linked_rows(conn)
            reread_plans = [archive_module.classify_row(row) for row in reread_rows]
        finally:
            conn.close()

        self.assertEqual(entry_6[0], 'archived')
        self.assertEqual(entry_6[1], 1)
        self.assertEqual(entry_6[2], '2026-03-25T16:50:00')
        self.assertEqual(entry_6[3], 'pending')
        self.assertEqual(entry_6[4], 13)
        self.assertIn('periodic_tasks.id=13', entry_6[5])

        self.assertEqual(entry_7[0], 'archived')
        self.assertEqual(entry_7[1], 1)
        self.assertEqual(entry_7[2], '2026-03-25T16:50:00')
        self.assertEqual(entry_7[3], 'archived')
        self.assertEqual(entry_7[4], 14)
        self.assertIn('periodic_tasks.id=14', entry_7[5])

        self.assertEqual(len(applied), 2)
        self.assertTrue(any('entry 6 -> task 13' in item.note for item in applied))
        by_id = {plan.entry_id: plan for plan in reread_plans}
        self.assertEqual(by_id[6].action, 'already_archived')
        self.assertEqual(by_id[7].action, 'already_archived')

    def test_resolve_archive_status_preserves_current_status_when_archived_not_allowed(self):
        conn = archive_module.connect(str(self.db_path))
        try:
            resolved = archive_module.resolve_archive_status(conn, 'pending')
        finally:
            conn.close()

        self.assertEqual(resolved, 'archived')

        with tempfile.TemporaryDirectory() as temp_dir:
            constrained_db = Path(temp_dir) / 'todo.db'
            conn = sqlite3.connect(constrained_db)
            try:
                conn.execute(
                    """
                    CREATE TABLE entries (
                        id INTEGER PRIMARY KEY,
                        text TEXT NOT NULL,
                        status TEXT NOT NULL CHECK (status IN ('pending','done','skipped')),
                        group_id INTEGER NOT NULL,
                        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                    )
                    """
                )
                constrained = archive_module.resolve_archive_status(conn, 'pending')
            finally:
                conn.close()

        self.assertEqual(constrained, 'pending')

    def test_classify_metadata_only_archive_as_archived_state(self):
        conn = archive_module.connect(str(self.db_path))
        try:
            archive_module.ensure_archive_columns(conn)
            conn.execute(
                "UPDATE entries SET status = 'pending', chronos_archived_at = '2026-03-25T16:50:00', chronos_archived_from_status = 'pending', chronos_linked_task_id = 13 WHERE id = 6"
            )
            conn.commit()
            row = conn.execute(
                "SELECT e.id, e.text, e.status, t.id AS task_id, t.name AS task_name, COALESCE(t.source, 'chronos') AS task_source, COALESCE(e.chronos_readonly, 0) AS chronos_readonly, e.chronos_archived_at AS chronos_archived_at, e.chronos_archived_from_status AS chronos_archived_from_status, e.chronos_linked_task_id AS chronos_linked_task_id, e.chronos_archive_reason AS chronos_archive_reason FROM entries e JOIN periodic_tasks t ON t.legacy_entry_id = e.id WHERE e.id = 6"
            ).fetchone()
            plan = archive_module.classify_row(row)
        finally:
            conn.close()

        self.assertEqual(plan.action, 'repair_archive_metadata')
        self.assertIn('archived state', plan.reason)

    def test_summary_json_shape(self):
        summary = archive_module.summarize(
            [archive_module.ArchivePlan(1, 'x', 'pending', 2, 'task', 'legacy_entries_migrated', 'archive', 'reason')],
            [archive_module.AppliedResult(1, 2, 'archived legacy entry 1 -> task 2')],
            apply_mode=True,
        )
        encoded = json.dumps(summary, ensure_ascii=False)
        self.assertIn('"mode": "apply"', encoded)
        self.assertIn('"archive": 1', encoded)


if __name__ == '__main__':
    unittest.main()
