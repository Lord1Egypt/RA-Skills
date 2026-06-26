import importlib.util
import io
import json
import sqlite3
import tempfile
import unittest
from contextlib import redirect_stdout
from datetime import datetime
from pathlib import Path
from unittest.mock import patch


PROJECT_ROOT = Path(__file__).resolve().parent.parent
TODO_SCRIPT = PROJECT_ROOT / "scripts" / "todo.py"

spec = importlib.util.spec_from_file_location("chronos_todo", TODO_SCRIPT)
todo_module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(todo_module)


class TodoHelpersTests(unittest.TestCase):
    def test_build_parser_list_supports_include_skipped_flag(self):
        parser = todo_module.build_parser()
        args = parser.parse_args(["list", "--include-skipped"])

        self.assertEqual(args.command, "list")
        self.assertTrue(args.include_skipped)

    def test_parse_entry_identifier_accepts_prefixed_ids(self):
        self.assertEqual(todo_module.parse_entry_identifier("ID45"), 45)
        self.assertEqual(todo_module.parse_entry_identifier("45"), 45)

    def test_parse_compact_end_date_supports_yymmdd(self):
        self.assertEqual(todo_module.parse_compact_end_date("260630"), "2026-06-30")
        self.assertEqual(todo_module.parse_compact_end_date("20260630"), "2026-06-30")
        self.assertIsNone(todo_module.parse_compact_end_date("20261340"))

    def test_natural_language_parser_extracts_compact_end_date(self):
        parsed = todo_module.parse_natural_language("添加任务 每周三 10:00 周三抢券 结束日期260630")

        self.assertEqual(parsed["cmd"], "add")
        self.assertEqual(parsed["cycle_type"], "weekly")
        self.assertEqual(parsed["weekday"], 2)
        self.assertEqual(parsed["time_of_day"], "10:00")
        self.assertEqual(parsed["end_date"], "2026-06-30")

    def test_natural_language_parser_detects_complete_overdue(self):
        parsed = todo_module.parse_natural_language("自动完成逾期待办")
        self.assertEqual(parsed["cmd"], "complete-overdue")

    def test_natural_language_parser_detects_every_four_hours(self):
        parsed = todo_module.parse_natural_language("添加任务 每4小时 08:00 同步subagent记忆")
        self.assertEqual(parsed["cmd"], "add")
        self.assertEqual(parsed["cycle_type"], "hourly")
        self.assertEqual(parsed["interval_hours"], 4)
        self.assertEqual(parsed["time_of_day"], "08:00")


class TodoListVisibilityTests(unittest.TestCase):
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
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT,
                cycle_type TEXT NOT NULL,
                time_of_day TEXT,
                count_current_month INTEGER DEFAULT 0,
                legacy_entry_id INTEGER
            );
            CREATE TABLE periodic_occurrences (
                id INTEGER PRIMARY KEY,
                task_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                status TEXT NOT NULL,
                reminder_job_id TEXT,
                completed_at TEXT,
                is_auto_completed INTEGER DEFAULT 0,
                completion_mode TEXT,
                special_handler_result TEXT,
                scheduled_time TEXT,
                scheduled_at TEXT,
                legacy_entry_id INTEGER
            );
            """
        )
        conn.execute("INSERT INTO groups (id, name) VALUES (1, 'Inbox')")
        conn.execute("INSERT INTO periodic_tasks (id, name, category, cycle_type, time_of_day) VALUES (1, '活跃周期任务', 'Inbox', 'daily', '09:00')")
        conn.execute("INSERT INTO periodic_tasks (id, name, category, cycle_type, time_of_day) VALUES (2, '已跳过周期任务', 'Inbox', 'daily', '10:00')")
        conn.execute("INSERT INTO periodic_occurrences (id, task_id, date, status, scheduled_time) VALUES (101, 1, '2026-03-25', 'pending', '09:00')")
        conn.execute("INSERT INTO periodic_occurrences (id, task_id, date, status, scheduled_time) VALUES (102, 2, '2026-03-25', 'skipped', '10:00')")
        conn.execute("INSERT INTO entries (id, text, status, group_id) VALUES (11, '活跃普通任务', 'pending', 1)")
        conn.execute("INSERT INTO entries (id, text, status, group_id) VALUES (12, '已跳过普通任务', 'skipped', 1)")
        conn.commit()
        conn.close()

    def test_pending_queries_hide_skipped_by_default(self):
        with patch.object(todo_module, 'TODO_DB', self.db_path):
            periodic = todo_module.get_periodic_pending()
            simple = todo_module.get_simple_pending()

        self.assertEqual([row[4] for row in periodic], [101])
        self.assertEqual([row[0] for row in simple], [11])

    def test_pending_queries_can_include_skipped(self):
        with patch.object(todo_module, 'TODO_DB', self.db_path):
            periodic = todo_module.get_periodic_pending(include_skipped=True)
            simple = todo_module.get_simple_pending(include_skipped=True)

        self.assertEqual(sorted(row[4] for row in periodic), [101, 102])
        self.assertEqual(sorted(row[0] for row in simple), [11, 12])

    def test_cmd_list_hides_skipped_by_default(self):
        with patch.object(todo_module, 'TODO_DB', self.db_path), \
             patch.object(todo_module, 'ensure_today_occurrences'):
            buf = io.StringIO()
            with redirect_stdout(buf):
                todo_module.cmd_list()

        output = buf.getvalue()
        self.assertIn('FIN-101', output)
        self.assertIn('@ 09:00', output)
        self.assertIn('ID11', output)
        self.assertNotIn('FIN-102', output)
        self.assertNotIn('ID12', output)
        self.assertNotIn('已包含 skipped 项', output)

    def test_cmd_list_include_skipped_shows_marker_and_rows(self):
        with patch.object(todo_module, 'TODO_DB', self.db_path), \
             patch.object(todo_module, 'ensure_today_occurrences'):
            buf = io.StringIO()
            with redirect_stdout(buf):
                todo_module.cmd_list(include_skipped=True)

        output = buf.getvalue()
        self.assertIn('FIN-102', output)
        self.assertIn('ID12', output)
        self.assertIn('已包含 skipped 项', output)
        self.assertIn('已跳过', output)


class TodoOverdueCompletionTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.db_path = Path(self.temp_dir.name) / "todo.db"
        self.workspace = Path(self.temp_dir.name) / "workspace"
        self.workspace.mkdir()
        (self.workspace / "memory").mkdir()
        (self.workspace / "scripts").mkdir()
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
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT,
                cycle_type TEXT NOT NULL,
                weekday INTEGER,
                n_per_month INTEGER,
                interval_hours INTEGER,
                time_of_day TEXT,
                count_current_month INTEGER DEFAULT 0,
                special_handler TEXT,
                handler_payload TEXT,
                legacy_entry_id INTEGER,
                start_date TEXT,
                task_kind TEXT DEFAULT 'scheduled',
                source TEXT DEFAULT 'chronos',
                delivery_target TEXT,
                delivery_mode TEXT
            );
            CREATE TABLE periodic_occurrences (
                id INTEGER PRIMARY KEY,
                task_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                status TEXT NOT NULL,
                reminder_job_id TEXT,
                completed_at TEXT,
                is_auto_completed INTEGER DEFAULT 0,
                completion_mode TEXT,
                special_handler_result TEXT,
                scheduled_time TEXT,
                scheduled_at TEXT,
                legacy_entry_id INTEGER
            );
            """
        )
        conn.execute("INSERT INTO groups (id, name) VALUES (1, 'System')")
        conn.execute(
            "INSERT INTO periodic_tasks (id, name, category, cycle_type, time_of_day, count_current_month) VALUES (1, '周期测试任务', 'System', 'daily', '09:00', 0)"
        )
        conn.execute(
            "INSERT INTO periodic_occurrences (id, task_id, date, status, scheduled_time) VALUES (101, 1, '2026-03-25', 'pending', '09:00')"
        )
        conn.execute(
            "INSERT INTO periodic_tasks (id, name, category, cycle_type, time_of_day, count_current_month, special_handler, task_kind, source, start_date) VALUES (2, 'Meta-Review fallback', 'System', 'daily', '02:00', 0, 'meta_review_fallback', 'system', 'system_seeded', '2026-03-01')"
        )
        conn.execute(
            "INSERT INTO periodic_occurrences (id, task_id, date, status, scheduled_time) VALUES (202, 2, '2026-03-25', 'pending', '02:00')"
        )
        conn.execute(
            "INSERT INTO periodic_tasks (id, name, category, cycle_type, interval_hours, time_of_day, count_current_month, special_handler, task_kind, source, start_date) VALUES (3, '同步 subagent 记忆', 'System', 'hourly', 4, '08:00', 0, 'sync_subagent_memory', 'system', 'legacy_entries_migrated', '2026-03-01')"
        )
        conn.execute(
            "INSERT INTO periodic_occurrences (id, task_id, date, status, scheduled_time) VALUES (303, 3, '2026-03-25', 'pending', '00:00')"
        )
        conn.execute(
            "INSERT INTO periodic_occurrences (id, task_id, date, status, scheduled_time) VALUES (304, 3, '2026-03-25', 'pending', '04:00')"
        )
        conn.execute(
            "INSERT INTO periodic_occurrences (id, task_id, date, status, scheduled_time) VALUES (305, 3, '2026-03-25', 'pending', '08:00')"
        )
        conn.execute(
            "INSERT INTO entries (id, text, status, group_id) VALUES (16, 'Meta-Review (daily 02:00): Run meta_auditor.py analyze --days 1 and apply high-confidence suggestions', 'pending', 1)"
        )
        conn.execute(
            "INSERT INTO entries (id, text, status, group_id) VALUES (17, '每 4 小时 08:00：同步 subagent 记忆 (memory_manager.py sync)', 'pending', 1)"
        )
        conn.execute(
            "INSERT INTO entries (id, text, status, group_id) VALUES (18, '给朋友发消息 21:00', 'pending', 1)"
        )
        conn.commit()
        conn.close()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def test_get_overdue_legacy_entries_filters_to_recurring_and_due(self):
        with patch.object(todo_module, 'TODO_DB', self.db_path):
            entries = todo_module.get_overdue_legacy_entries(datetime(2026, 3, 25, 11, 30))

        identifiers = [entry['identifier'] for entry in entries]
        self.assertEqual(identifiers, ['ID16', 'ID17'])
        self.assertEqual(entries[0]['special_handler'], 'meta_review_fallback')
        self.assertIsNone(entries[1]['special_handler'])

    def test_archived_readonly_legacy_entry_is_rejected_by_complete_skip_and_show(self):
        conn = self._connect()
        conn.execute("ALTER TABLE entries ADD COLUMN chronos_readonly INTEGER NOT NULL DEFAULT 0")
        conn.execute("ALTER TABLE entries ADD COLUMN chronos_archived_at TEXT")
        conn.execute("ALTER TABLE entries ADD COLUMN chronos_archive_reason TEXT")
        conn.execute("ALTER TABLE entries ADD COLUMN chronos_archived_from_status TEXT")
        conn.execute("ALTER TABLE entries ADD COLUMN chronos_linked_task_id INTEGER")
        conn.execute(
            "UPDATE entries SET status = 'archived', chronos_readonly = 1, chronos_archived_at = '2026-03-25T16:50:00', chronos_archive_reason = 'Chronos legacy archive: linked to periodic_tasks.id=2', chronos_archived_from_status = 'pending', chronos_linked_task_id = 2 WHERE id = 16"
        )
        conn.commit()
        conn.close()

        with patch.object(todo_module, 'TODO_DB', self.db_path):
            ok_complete, message_complete = todo_module.complete_legacy_entry(16)
        self.assertFalse(ok_complete)
        self.assertIn('legacy 归档记录（只读）', message_complete)
        self.assertIn('关联周期任务 2', message_complete)

        with patch.object(todo_module, 'TODO_DB', self.db_path):
            skip_buf = io.StringIO()
            with redirect_stdout(skip_buf):
                todo_module.cmd_skip('ID16')
        self.assertIn('legacy 归档记录（只读）', skip_buf.getvalue())

        with patch.object(todo_module, 'TODO_DB', self.db_path):
            show_buf = io.StringIO()
            with redirect_stdout(show_buf):
                todo_module.cmd_show('ID16')
        show_output = show_buf.getvalue()
        self.assertIn('状态：archived', show_output)
        self.assertIn('Chronos：legacy 归档（只读）', show_output)
        self.assertIn('关联周期任务：2', show_output)

    def test_metadata_only_archived_legacy_entry_is_also_blocked(self):
        conn = self._connect()
        conn.execute("ALTER TABLE entries ADD COLUMN chronos_readonly INTEGER NOT NULL DEFAULT 0")
        conn.execute("ALTER TABLE entries ADD COLUMN chronos_archived_at TEXT")
        conn.execute("ALTER TABLE entries ADD COLUMN chronos_archive_reason TEXT")
        conn.execute("ALTER TABLE entries ADD COLUMN chronos_archived_from_status TEXT")
        conn.execute("ALTER TABLE entries ADD COLUMN chronos_linked_task_id INTEGER")
        conn.execute(
            "UPDATE entries SET status = 'pending', chronos_archived_at = '2026-03-25T16:50:00', chronos_archive_reason = 'Chronos legacy archive: linked to periodic_tasks.id=2', chronos_archived_from_status = 'pending', chronos_linked_task_id = 2 WHERE id = 16"
        )
        conn.commit()
        conn.close()

        with patch.object(todo_module, 'TODO_DB', self.db_path):
            ok_complete, message_complete = todo_module.complete_legacy_entry(16)
        self.assertFalse(ok_complete)
        self.assertIn('legacy 归档记录', message_complete)
        self.assertIn('关联周期任务 2', message_complete)

        with patch.object(todo_module, 'TODO_DB', self.db_path):
            skip_buf = io.StringIO()
            with redirect_stdout(skip_buf):
                todo_module.cmd_skip('ID16')
        self.assertIn('legacy 归档记录', skip_buf.getvalue())

        with patch.object(todo_module, 'TODO_DB', self.db_path):
            show_buf = io.StringIO()
            with redirect_stdout(show_buf):
                todo_module.cmd_show('ID16')
        show_output = show_buf.getvalue()
        self.assertIn('状态：pending', show_output)
        self.assertIn('Chronos：legacy 归档', show_output)
        self.assertIn('归档时间：2026-03-25T16:50:00', show_output)

    def test_archived_from_status_only_entry_is_treated_as_archived(self):
        conn = self._connect()
        conn.execute("ALTER TABLE entries ADD COLUMN chronos_readonly INTEGER NOT NULL DEFAULT 0")
        conn.execute("ALTER TABLE entries ADD COLUMN chronos_archived_at TEXT")
        conn.execute("ALTER TABLE entries ADD COLUMN chronos_archive_reason TEXT")
        conn.execute("ALTER TABLE entries ADD COLUMN chronos_archived_from_status TEXT")
        conn.execute("ALTER TABLE entries ADD COLUMN chronos_linked_task_id INTEGER")
        conn.execute(
            "UPDATE entries SET status = 'pending', chronos_archived_from_status = 'pending', chronos_linked_task_id = 2 WHERE id = 16"
        )
        conn.commit()
        conn.close()

        with patch.object(todo_module, 'TODO_DB', self.db_path):
            ok_complete, message_complete = todo_module.complete_legacy_entry(16)
        self.assertFalse(ok_complete)
        self.assertIn('legacy 归档记录', message_complete)
        self.assertIn('关联周期任务 2', message_complete)

        with patch.object(todo_module, 'TODO_DB', self.db_path):
            show_buf = io.StringIO()
            with redirect_stdout(show_buf):
                todo_module.cmd_show('ID16')
        show_output = show_buf.getvalue()
        self.assertIn('状态：pending', show_output)
        self.assertIn('Chronos：legacy 归档', show_output)

    def test_complete_overdue_tasks_runs_special_handler_from_periodic_metadata(self):
        pending_subagents = json.dumps([
            {'session_id': 'agent:main:subagent:abc', 'status': 'completed', 'handled_at': None}
        ])

        def fake_run(args, capture_output=True, text=True, timeout=None):
            if 'pending-subagents' in args:
                return type('Result', (), {'returncode': 0, 'stdout': pending_subagents, 'stderr': ''})()
            if 'sync' in args:
                return type('Result', (), {'returncode': 0, 'stdout': 'Synced 2 memories from agent:main:subagent:abc\n', 'stderr': ''})()
            if 'mark-subagent-synced' in args:
                return type('Result', (), {'returncode': 0, 'stdout': '{"session_id": "agent:main:subagent:abc", "status": "synced"}', 'stderr': ''})()
            return type('Result', (), {'returncode': 0, 'stdout': '', 'stderr': ''})()

        memory_manager_script = self.workspace / 'scripts' / 'memory_manager.py'
        memory_manager_script.write_text('# stub', encoding='utf-8')

        with patch.object(todo_module, 'TODO_DB', self.db_path), \
             patch.object(todo_module, 'WORKSPACE', self.workspace), \
             patch.object(todo_module, 'subprocess') as mock_subprocess:
            mock_subprocess.run.side_effect = fake_run
            result = todo_module.complete_overdue_tasks(now=datetime(2026, 3, 25, 11, 30))

        self.assertFalse(result['errors'])
        self.assertEqual(result['handled'], ['FIN-303', 'FIN-202', 'FIN-304', 'FIN-305', 'FIN-101', 'ID16', 'ID17'])

        conn = self._connect()
        special_row = conn.execute(
            "SELECT status, completion_mode, special_handler_result FROM periodic_occurrences WHERE id = 202"
        ).fetchone()
        sync_rows = conn.execute(
            "SELECT id, status, completion_mode, special_handler_result FROM periodic_occurrences WHERE id IN (303, 304, 305) ORDER BY id"
        ).fetchall()
        occ_status = conn.execute("SELECT status FROM periodic_occurrences WHERE id = 101").fetchone()[0]
        meta_status = conn.execute("SELECT status FROM entries WHERE id = 16").fetchone()[0]
        recurring_status = conn.execute("SELECT status FROM entries WHERE id = 17").fetchone()[0]
        future_status = conn.execute("SELECT status FROM entries WHERE id = 18").fetchone()[0]
        conn.close()

        self.assertEqual(special_row[0], 'completed')
        self.assertEqual(special_row[1], 'fallback_handler')
        self.assertIn('Meta-Review fallback completed via direct PREDICTIONS.md/FRICTION.md inspection', special_row[2])
        self.assertEqual([row[1] for row in sync_rows], ['completed', 'completed', 'completed'])
        self.assertEqual([row[2] for row in sync_rows], ['fallback_handler_merged', 'fallback_handler_merged', 'fallback_handler_merged'])
        for index, row in enumerate(sync_rows, start=1):
            self.assertIn('Subagent memory sync completed', row[3])
            self.assertIn('merge_key=sync_subagent_memory:3:2026-03-25', row[3])
            self.assertIn(f'merged occurrence {index}/3', row[3])
        self.assertEqual(occ_status, 'completed')
        self.assertEqual(meta_status, 'done')
        self.assertEqual(recurring_status, 'done')
        self.assertEqual(future_status, 'pending')

        memory_log = (self.workspace / 'memory' / '2026-03-25.md').read_text(encoding='utf-8')
        self.assertIn('Meta-Review fallback completed via direct PREDICTIONS.md/FRICTION.md inspection', memory_log)
        self.assertEqual(memory_log.count('Subagent memory sync completed'), 1)

    def test_run_sync_subagent_memory_marks_failure_in_ledger(self):
        pending_subagents = json.dumps([
            {'session_id': 'agent:main:subagent:abc', 'status': 'completed', 'handled_at': None}
        ])

        def fake_run(args, capture_output=True, text=True, timeout=None):
            if 'pending-subagents' in args:
                return type('Result', (), {'returncode': 0, 'stdout': pending_subagents, 'stderr': ''})()
            if 'sync' in args:
                return type('Result', (), {'returncode': 1, 'stdout': '', 'stderr': 'boom'})()
            if 'mark-subagent-failed' in args:
                return type('Result', (), {'returncode': 0, 'stdout': '', 'stderr': ''})()
            raise AssertionError(f'unexpected args: {args}')

        memory_manager_script = self.workspace / 'scripts' / 'memory_manager.py'
        memory_manager_script.write_text('# stub', encoding='utf-8')

        with patch.object(todo_module, 'WORKSPACE', self.workspace), \
             patch.object(todo_module, 'subprocess') as mock_subprocess:
            mock_subprocess.run.side_effect = fake_run
            ok, message = todo_module.run_sync_subagent_memory(None, now=datetime(2026, 3, 25, 11, 30))

        self.assertFalse(ok)
        self.assertIn('同步 agent:main:subagent:abc 失败', message)

    def test_complete_overdue_tasks_dry_run_does_not_change_state(self):
        memory_manager_script = self.workspace / 'scripts' / 'memory_manager.py'
        memory_manager_script.write_text('# stub', encoding='utf-8')

        with patch.object(todo_module, 'TODO_DB', self.db_path), \
             patch.object(todo_module, 'WORKSPACE', self.workspace), \
             patch.object(todo_module, 'subprocess') as mock_subprocess:
            mock_subprocess.run.return_value = type('Result', (), {'returncode': 0, 'stdout': '', 'stderr': ''})()
            result = todo_module.complete_overdue_tasks(now=datetime(2026, 3, 25, 11, 30), dry_run=True)

        self.assertEqual(result['handled'], ['FIN-303', 'FIN-202', 'FIN-304', 'FIN-305', 'FIN-101', 'ID16', 'ID17'])
        self.assertEqual(len(result['simulated']), 7)
        self.assertIn('FIN-303 同步 subagent 记忆 @ 00:00 [sync_subagent_memory] [merge-once day-batch x3]', result['simulated'])
        self.assertIn('FIN-304 同步 subagent 记忆 @ 04:00 [sync_subagent_memory] [merge-once day-batch x3]', result['simulated'])
        self.assertIn('FIN-305 同步 subagent 记忆 @ 08:00 [sync_subagent_memory] [merge-once day-batch x3]', result['simulated'])

        conn = self._connect()
        occ_status = conn.execute("SELECT status FROM periodic_occurrences WHERE id = 101").fetchone()[0]
        meta_status = conn.execute("SELECT status FROM entries WHERE id = 16").fetchone()[0]
        special_status = conn.execute("SELECT status FROM periodic_occurrences WHERE id = 202").fetchone()[0]
        sync_rows = conn.execute("SELECT status FROM periodic_occurrences WHERE id IN (303, 304, 305) ORDER BY id").fetchall()
        conn.close()

        self.assertEqual(occ_status, 'pending')
        self.assertEqual(meta_status, 'pending')
        self.assertEqual(special_status, 'pending')
        self.assertEqual([row[0] for row in sync_rows], ['pending', 'pending', 'pending'])
        self.assertFalse((self.workspace / 'memory' / '2026-03-25.md').exists())

    def test_complete_overdue_tasks_system_only_limits_scope(self):
        memory_manager_script = self.workspace / 'scripts' / 'memory_manager.py'
        memory_manager_script.write_text('# stub', encoding='utf-8')

        with patch.object(todo_module, 'TODO_DB', self.db_path), \
             patch.object(todo_module, 'WORKSPACE', self.workspace), \
             patch.object(todo_module, 'subprocess') as mock_subprocess:
            mock_subprocess.run.return_value = type('Result', (), {'returncode': 0, 'stdout': '[]', 'stderr': ''})()
            result = todo_module.complete_overdue_tasks(now=datetime(2026, 3, 25, 11, 30), dry_run=True, system_only=True)

        self.assertEqual(result['handled'], ['FIN-303', 'FIN-202', 'FIN-304', 'FIN-305'])
        self.assertEqual(result['legacy'], [])
        self.assertEqual(len(result['simulated']), 4)
        self.assertFalse(any(item.startswith('FIN-101') for item in result['simulated']))
        self.assertFalse(any(item.startswith('ID16') for item in result['simulated']))
        self.assertFalse(any(item.startswith('ID17') for item in result['simulated']))

    def test_complete_periodic_occurrence_auto_completes_rest_of_month_for_monthly_quota_task(self):
        conn = self._connect()
        conn.execute("INSERT INTO periodic_tasks (id, name, category, cycle_type, n_per_month, time_of_day, count_current_month) VALUES (4, '福建农行秒杀京东卡', 'System', 'monthly_n_times', 1, '09:00', 0)")
        conn.execute("INSERT INTO periodic_occurrences (id, task_id, date, status, scheduled_time) VALUES (401, 4, '2026-03-25', 'pending', '09:00')")
        conn.execute("INSERT INTO periodic_occurrences (id, task_id, date, status, scheduled_time) VALUES (402, 4, '2026-03-26', 'pending', '09:00')")
        conn.execute("INSERT INTO periodic_occurrences (id, task_id, date, status, scheduled_time) VALUES (403, 4, '2026-03-31', 'reminded', '09:00')")
        conn.commit()
        conn.close()

        with patch.object(todo_module, 'TODO_DB', self.db_path):
            ok, message = todo_module.complete_periodic_occurrence(401)

        self.assertTrue(ok)
        self.assertIn('已完成 FIN-401', message)

        conn = self._connect()
        task_row = conn.execute("SELECT count_current_month FROM periodic_tasks WHERE id = 4").fetchone()
        occ_rows = conn.execute("SELECT id, status, is_auto_completed, completion_mode FROM periodic_occurrences WHERE task_id = 4 ORDER BY id").fetchall()
        conn.close()

        self.assertEqual(task_row[0], 1)
        self.assertEqual(occ_rows[0], (401, 'completed', 0, 'manual'))
        self.assertEqual(occ_rows[1], (402, 'completed', 1, 'auto_quota'))
        self.assertEqual(occ_rows[2], (403, 'completed', 1, 'auto_quota'))


if __name__ == "__main__":
    unittest.main()
