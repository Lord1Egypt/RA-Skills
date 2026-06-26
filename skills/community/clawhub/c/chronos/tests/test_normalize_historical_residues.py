import json
import sqlite3
import subprocess
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT_ROOT / 'scripts' / 'normalize_historical_residues.py'


class NormalizeHistoricalResiduesTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.db_path = Path(self.temp_dir.name) / 'todo.db'
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.executescript(
            """
            CREATE TABLE periodic_tasks (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT,
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
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                end_date TEXT,
                start_date TEXT
            );
            CREATE TABLE periodic_occurrences (
                id INTEGER PRIMARY KEY,
                task_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                status TEXT NOT NULL,
                reminder_job_id TEXT,
                is_auto_completed INTEGER DEFAULT 0,
                completed_at TEXT,
                completion_mode TEXT,
                special_handler_result TEXT,
                scheduled_time TEXT,
                scheduled_at TEXT,
                legacy_entry_id INTEGER
            );
            """
        )
        conn.execute("INSERT INTO periodic_tasks (id, name, cycle_type, time_of_day, event_time, start_date) VALUES (1, 'single-occ once', 'once', '15:00', '2026-03-20 15:00', NULL)")
        conn.execute("INSERT INTO periodic_occurrences (id, task_id, date, status) VALUES (101, 1, '2026-03-20', 'completed')")

        conn.execute("INSERT INTO periodic_tasks (id, name, cycle_type, time_of_day, event_time, end_date, start_date) VALUES (2, 'future-once', 'once', '10:00', '10:00', '2026-03-27', NULL)")
        conn.execute("INSERT INTO periodic_tasks (id, name, cycle_type, time_of_day, event_time, start_date) VALUES (3, 'ambiguous-once', 'once', '10:00', '10:00', NULL)")
        conn.execute("INSERT INTO periodic_occurrences (id, task_id, date, status) VALUES (103, 3, '2026-03-20', 'pending')")
        conn.execute("INSERT INTO periodic_occurrences (id, task_id, date, status) VALUES (104, 3, '2026-03-21', 'pending')")

        conn.execute("INSERT INTO periodic_occurrences (id, task_id, date, status) VALUES (201, 999, '2026-03-16', 'pending')")
        conn.commit()
        conn.close()

    def _run(self, *args):
        result = subprocess.run(
            ['python3', str(SCRIPT), '--db', str(self.db_path), '--json', *args],
            capture_output=True,
            text=True,
            check=True,
        )
        return json.loads(result.stdout)

    def test_dry_run_classifies_safe_and_ambiguous_rows(self):
        summary = self._run()
        counts = summary['counts']
        self.assertEqual(counts['orphan_occurrence:delete'], 1)
        self.assertEqual(counts['once_null_start_date:set_start_date'], 2)
        self.assertEqual(counts['once_null_start_date:manual_review'], 1)

        plans = {plan['row_id']: plan for plan in summary['plans'] if plan['kind'] == 'once_null_start_date'}
        self.assertEqual(plans[1]['inferred_start_date'], '2026-03-20')
        self.assertEqual(plans[2]['inferred_start_date'], '2026-03-27')
        self.assertEqual(plans[3]['action'], 'manual_review')

    def test_apply_updates_safe_rows_only(self):
        summary = self._run('--apply')
        applied_notes = [item['note'] for item in summary['applied']]
        self.assertTrue(any('deleted orphan occurrence 201' in note for note in applied_notes))
        self.assertTrue(any('periodic_tasks.id=1 start_date=2026-03-20' in note for note in applied_notes))
        self.assertTrue(any('periodic_tasks.id=2 start_date=2026-03-27' in note for note in applied_notes))

        conn = sqlite3.connect(self.db_path)
        start_dates = dict(conn.execute("SELECT id, start_date FROM periodic_tasks WHERE id IN (1,2,3)").fetchall())
        orphan_count = conn.execute("SELECT COUNT(*) FROM periodic_occurrences WHERE id = 201").fetchone()[0]
        conn.close()

        self.assertEqual(start_dates[1], '2026-03-20')
        self.assertEqual(start_dates[2], '2026-03-27')
        self.assertIsNone(start_dates[3])
        self.assertEqual(orphan_count, 0)


if __name__ == '__main__':
    unittest.main()
