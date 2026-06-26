import json
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path
import importlib.util

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = PROJECT_ROOT / "scripts" / "migrate_legacy_entries.py"
MODULE_NAME = "chronos_migrate_legacy_entries"

spec = importlib.util.spec_from_file_location(MODULE_NAME, SCRIPT_PATH)
migrate_module = importlib.util.module_from_spec(spec)
sys.modules[MODULE_NAME] = migrate_module
spec.loader.exec_module(migrate_module)


class LegacyMigrationScriptTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.db_path = Path(self.temp_dir.name) / "todo.db"
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
                weekday INTEGER,
                day_of_month INTEGER,
                range_start INTEGER,
                range_end INTEGER,
                n_per_month INTEGER,
                interval_hours INTEGER,
                time_of_day TEXT NOT NULL,
                event_time TEXT,
                timezone TEXT DEFAULT 'Asia/Shanghai',
                is_active BOOLEAN DEFAULT 1,
                count_current_month INTEGER DEFAULT 0,
                end_date TEXT,
                reminder_template TEXT,
                dates_list TEXT,
                task_kind TEXT NOT NULL DEFAULT 'scheduled',
                source TEXT NOT NULL DEFAULT 'chronos',
                legacy_entry_id INTEGER,
                special_handler TEXT,
                handler_payload TEXT,
                start_date TEXT,
                delivery_target TEXT,
                delivery_mode TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            );
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
            );
            """
        )
        conn.execute("INSERT INTO groups (id, name) VALUES (1, 'System')")
        conn.execute("INSERT INTO groups (id, name) VALUES (2, '活动提醒')")
        conn.execute(
            "INSERT INTO entries (id, text, status, group_id, created_at) VALUES (15, '每 4 小时：同步 subagent 记忆 (memory_manager.py sync)', 'pending', 1, '2026-03-20 08:00:00')"
        )
        conn.execute(
            "INSERT INTO entries (id, text, status, group_id, created_at) VALUES (16, 'Meta-Review (daily 02:00): Run meta_auditor.py analyze --days 1 and apply high-confidence suggestions', 'done', 1, '2026-03-01 02:00:00')"
        )
        conn.execute(
            "INSERT INTO entries (id, text, status, group_id, created_at) VALUES (21, '[每周重复] 华夏精彩Fun肆日 (每周四 10:00)', 'done', 2, '2026-03-10 10:00:00')"
        )
        conn.execute(
            "INSERT INTO entries (id, text, status, group_id, created_at) VALUES (22, '[每月重复] 福建农行秒杀京东卡 (每日 9:00)', 'done', 2, '2026-03-03 09:00:00')"
        )
        conn.execute(
            "INSERT INTO periodic_tasks (id, name, category, cycle_type, weekday, time_of_day, event_time, source) VALUES (2, '华夏精彩Fun肆日', '活动提醒', 'weekly', 3, '10:00', '10:00', 'chronos')"
        )
        conn.commit()
        conn.close()

    def test_classify_dry_run_separates_link_create_and_manual_review(self):
        conn = migrate_module.connect(str(self.db_path))
        try:
            plans = [migrate_module.classify_entry(conn, row) for row in migrate_module.load_entries(conn)]
        finally:
            conn.close()

        by_id = {plan.entry_id: plan for plan in plans}
        self.assertEqual(by_id[21].action, 'link_existing')
        self.assertEqual(by_id[21].task_id, 2)
        self.assertEqual(by_id[16].action, 'create_task')
        self.assertEqual(by_id[16].task_params['special_handler'], 'meta_review_fallback')
        self.assertEqual(by_id[15].action, 'create_task')
        self.assertEqual(by_id[15].task_params['cycle_type'], 'hourly')
        self.assertEqual(by_id[15].task_params['interval_hours'], 4)
        self.assertEqual(by_id[15].task_params['special_handler'], 'sync_subagent_memory')
        self.assertEqual(by_id[22].action, 'create_task')
        self.assertEqual(by_id[22].task_params['cycle_type'], 'monthly_n_times')
        self.assertEqual(by_id[22].task_params['n_per_month'], 1)
        self.assertIsNone(by_id[22].task_params.get('weekday'))

    def test_apply_links_existing_and_creates_meta_review_and_hourly_sync_tasks(self):
        conn = migrate_module.connect(str(self.db_path))
        try:
            plans = [migrate_module.classify_entry(conn, row) for row in migrate_module.load_entries(conn)]
            applied = [
                migrate_module.apply_plan(conn, plan, today=migrate_module.date(2026, 3, 25))
                for plan in plans
                if plan.action in {'link_existing', 'create_task'}
            ]
            conn.commit()

            linked = conn.execute("SELECT legacy_entry_id, source FROM periodic_tasks WHERE id = 2").fetchone()
            meta_task = conn.execute(
                "SELECT id, cycle_type, task_kind, source, legacy_entry_id, special_handler, start_date, time_of_day, handler_payload FROM periodic_tasks WHERE special_handler = 'meta_review_fallback'"
            ).fetchone()
            hourly_task = conn.execute(
                "SELECT id, cycle_type, interval_hours, task_kind, source, legacy_entry_id, special_handler, time_of_day, handler_payload FROM periodic_tasks WHERE special_handler = 'sync_subagent_memory'"
            ).fetchone()
            monthly_quota_task = conn.execute(
                "SELECT id, cycle_type, weekday, n_per_month, task_kind, source, legacy_entry_id, time_of_day FROM periodic_tasks WHERE legacy_entry_id = 22"
            ).fetchone()
            occs = conn.execute(
                "SELECT task_id, date, status, scheduled_time, legacy_entry_id FROM periodic_occurrences WHERE task_id = ? ORDER BY scheduled_time",
                (hourly_task[0],),
            ).fetchall()
        finally:
            conn.close()

        self.assertEqual(linked[0], 21)
        self.assertEqual(linked[1], 'legacy_entries_linked')
        self.assertIsNotNone(meta_task)
        self.assertEqual(meta_task[1], 'daily')
        self.assertEqual(meta_task[2], 'system')
        self.assertEqual(meta_task[3], 'legacy_entries_migrated')
        self.assertEqual(meta_task[4], 16)
        self.assertEqual(meta_task[5], 'meta_review_fallback')
        self.assertEqual(meta_task[6], '2026-03-01')
        self.assertEqual(meta_task[7], '02:00')
        payload = json.loads(meta_task[8])
        self.assertEqual(payload['scope_days'], 1)
        self.assertEqual(payload['fallback_sources'], ['PREDICTIONS.md', 'FRICTION.md'])

        self.assertIsNotNone(hourly_task)
        self.assertEqual(hourly_task[1], 'hourly')
        self.assertEqual(hourly_task[2], 4)
        self.assertEqual(hourly_task[3], 'system')
        self.assertEqual(hourly_task[4], 'legacy_entries_migrated')
        self.assertEqual(hourly_task[5], 15)
        self.assertEqual(hourly_task[6], 'sync_subagent_memory')
        self.assertEqual(hourly_task[7], '00:00')
        hourly_payload = json.loads(hourly_task[8])
        self.assertEqual(hourly_payload['session_filter'], ':subagent:')
        self.assertEqual([row[3] for row in occs], ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00'])
        self.assertTrue(all(row[4] == 15 for row in occs))

        self.assertIsNotNone(monthly_quota_task)
        self.assertEqual(monthly_quota_task[1], 'monthly_n_times')
        self.assertIsNone(monthly_quota_task[2])
        self.assertEqual(monthly_quota_task[3], 1)
        self.assertEqual(monthly_quota_task[4], 'scheduled')
        self.assertEqual(monthly_quota_task[5], 'legacy_entries_migrated')
        self.assertEqual(monthly_quota_task[6], 22)
        self.assertEqual(monthly_quota_task[7], '09:00')

        notes = [item.note for item in applied]
        self.assertTrue(any('linked entry 21 -> task 2' in note for note in notes))
        self.assertTrue(any('created task' in note and 'entry 16' in note for note in notes))
        self.assertTrue(any('created task' in note and 'entry 15' in note for note in notes))


if __name__ == '__main__':
    unittest.main()
