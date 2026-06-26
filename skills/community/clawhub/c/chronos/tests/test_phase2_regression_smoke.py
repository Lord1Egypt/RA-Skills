import importlib.util
import io
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from datetime import datetime
from pathlib import Path
from unittest.mock import patch


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TODO_SCRIPT = PROJECT_ROOT / "scripts" / "todo.py"
MIGRATE_SCRIPT = PROJECT_ROOT / "scripts" / "migrate_legacy_entries.py"
TODO_MODULE_NAME = "chronos_todo_phase2_smoke"
MIGRATE_MODULE_NAME = "chronos_migrate_phase2_smoke"
CORE_MODULES = [
    "core.paths",
    "core.db",
    "core.scheduler",
    "core.config",
    "core.learning",
    "core.models",
    "core.openclaw_cron",
]


def load_module(module_name: str, script_path: Path, db_path: Path, workspace_path: Path):
    for name in CORE_MODULES + [module_name]:
        sys.modules.pop(name, None)

    os.environ["CHRONOS_DB_PATH"] = str(db_path)
    os.environ["CHRONOS_WORKSPACE"] = str(workspace_path)
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def create_schema(db_path: Path):
    conn = sqlite3.connect(db_path)
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
            group_id INTEGER,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE periodic_tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        CREATE UNIQUE INDEX idx_periodic_tasks_name ON periodic_tasks(name);
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
            legacy_entry_id INTEGER,
            FOREIGN KEY (task_id) REFERENCES periodic_tasks(id) ON DELETE CASCADE,
            UNIQUE(task_id, date)
        );
        """
    )
    conn.commit()
    conn.close()


class Phase2RegressionSmokeTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.root = Path(self.tempdir.name)
        self.workspace = self.root / "workspace"
        self.workspace.mkdir()
        (self.workspace / "memory").mkdir()
        self.db_path = self.workspace / "todo.db"
        create_schema(self.db_path)
        self.todo_module = load_module(TODO_MODULE_NAME, TODO_SCRIPT, self.db_path, self.workspace)
        self.migrate_module = load_module(MIGRATE_MODULE_NAME, MIGRATE_SCRIPT, self.db_path, self.workspace)
        self._seed_base_data()

    def tearDown(self):
        os.environ.pop("CHRONOS_DB_PATH", None)
        os.environ.pop("CHRONOS_WORKSPACE", None)

    def _seed_base_data(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("INSERT INTO groups (id, name) VALUES (1, 'Inbox')")
        conn.execute("INSERT INTO groups (id, name) VALUES (2, 'System')")
        conn.execute("INSERT INTO entries (id, text, status, group_id, created_at) VALUES (1, '普通任务', 'pending', 1, '2026-03-25 08:00:00')")
        conn.execute("INSERT INTO entries (id, text, status, group_id, created_at) VALUES (2, '[每周重复] 迁移周任务 (每周三 09:00)', 'pending', 1, '2026-03-20 08:00:00')")
        conn.execute("INSERT INTO entries (id, text, status, group_id, created_at) VALUES (3, 'Meta-Review (daily 02:00): Run meta_auditor.py analyze --days 1', 'pending', 2, '2026-03-01 02:00:00')")
        conn.execute("INSERT INTO entries (id, text, status, group_id, created_at) VALUES (4, '每 4 小时：同步 subagent 记忆 (memory_manager.py sync)', 'pending', 2, '2026-03-01 08:00:00')")
        conn.execute(
            "INSERT INTO periodic_tasks (id, name, category, cycle_type, time_of_day, event_time, timezone, source) VALUES (10, '现有显式任务', 'Inbox', 'daily', '08:00', '08:00', 'Asia/Shanghai', 'chronos')"
        )
        conn.execute(
            "INSERT INTO periodic_occurrences (id, task_id, date, status, scheduled_time, scheduled_at) VALUES (100, 10, '2026-03-25', 'pending', '08:00', '2026-03-25T08:00:00')"
        )
        conn.commit()
        conn.close()

    def test_migration_dry_run_apply_and_idempotence_on_copied_dbs(self):
        dry_db = self.root / "dry.db"
        apply_db = self.root / "apply.db"
        shutil.copy2(self.db_path, dry_db)
        shutil.copy2(self.db_path, apply_db)

        dry_conn = self.migrate_module.connect(str(dry_db))
        try:
            plans = [self.migrate_module.classify_entry(dry_conn, row) for row in self.migrate_module.load_entries(dry_conn)]
        finally:
            dry_conn.close()
        by_id = {plan.entry_id: plan for plan in plans}
        self.assertEqual(by_id[2].action, "create_task")
        self.assertEqual(by_id[3].action, "create_task")
        self.assertEqual(by_id[4].action, "create_task")
        self.assertEqual(by_id[4].task_params["cycle_type"], "hourly")
        self.assertEqual(by_id[4].task_params["interval_hours"], 4)
        self.assertEqual(by_id[4].task_params["special_handler"], "sync_subagent_memory")
        self.assertEqual(by_id[1].action, "skip_inbox")

        apply_conn = self.migrate_module.connect(str(apply_db))
        try:
            first_plans = [self.migrate_module.classify_entry(apply_conn, row) for row in self.migrate_module.load_entries(apply_conn)]
            first_applied = [
                self.migrate_module.apply_plan(apply_conn, plan, today=self.migrate_module.date(2026, 3, 25))
                for plan in first_plans
                if plan.action in {"link_existing", "create_task"}
            ]
            apply_conn.commit()

            task_rows = apply_conn.execute(
                "SELECT name, source, legacy_entry_id, special_handler, start_date FROM periodic_tasks ORDER BY id"
            ).fetchall()
            occ_rows = apply_conn.execute(
                "SELECT task_id, date, status, legacy_entry_id FROM periodic_occurrences ORDER BY id"
            ).fetchall()

            second_plans = [self.migrate_module.classify_entry(apply_conn, row) for row in self.migrate_module.load_entries(apply_conn)]
        finally:
            apply_conn.close()

        self.assertEqual(len(first_applied), 3)
        self.assertTrue(any(row[0] == "迁移周任务" and row[1] == "legacy_entries_migrated" and row[2] == 2 for row in task_rows))
        self.assertTrue(any(row[0] == "Meta-Review fallback" and row[3] == "meta_review_fallback" and row[4] == "2026-03-01" for row in task_rows))
        self.assertTrue(any(row[0] == "同步 subagent 记忆" and row[3] == "sync_subagent_memory" for row in task_rows))
        self.assertTrue(any(row[3] == 2 for row in occ_rows), "migrated pending recurring entry should seed today's occurrence")
        self.assertTrue(any(row[3] == 4 for row in occ_rows), "migrated hourly legacy entry should seed today's occurrences")
        by_id_second = {plan.entry_id: plan for plan in second_plans}
        self.assertEqual(by_id_second[2].action, "already_migrated")
        self.assertEqual(by_id_second[3].action, "already_migrated")
        self.assertEqual(by_id_second[4].action, "already_migrated")

    def test_cli_smoke_list_show_complete_complete_overdue_and_add(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            "INSERT INTO periodic_tasks (id, name, category, cycle_type, time_of_day, event_time, timezone, special_handler, source) VALUES (11, 'Meta fallback task', 'System', 'daily', '02:00', '02:00', 'Asia/Shanghai', 'meta_review_fallback', 'legacy_entries_migrated')"
        )
        conn.execute(
            "INSERT INTO periodic_occurrences (id, task_id, date, status, scheduled_time, scheduled_at) VALUES (111, 11, '2026-03-25', 'pending', '02:00', '2026-03-25T02:00:00')"
        )
        conn.execute("INSERT INTO entries (id, text, status, group_id) VALUES (5, '跳过普通任务', 'skipped', 1)")
        conn.commit()
        conn.close()

        with patch.object(self.todo_module, "ensure_today_occurrences"):
            list_buf = io.StringIO()
            with redirect_stdout(list_buf):
                self.todo_module.cmd_list(include_skipped=True)
        list_output = list_buf.getvalue()
        self.assertIn("FIN-100", list_output)
        self.assertIn("FIN-111", list_output)
        self.assertIn("ID1", list_output)
        self.assertIn("ID5", list_output)

        show_buf = io.StringIO()
        with redirect_stdout(show_buf):
            self.todo_module.cmd_show("FIN-111")
        show_output = show_buf.getvalue()
        self.assertIn("special_handler：meta_review_fallback", show_output)
        self.assertIn("状态：pending", show_output)

        with patch.object(self.todo_module, "ensure_today_occurrences"), \
             patch.object(self.todo_module.subprocess, "run") as mock_run:
            mock_run.return_value = subprocess.CompletedProcess(args=["python3"], returncode=0, stdout="", stderr="")
            complete_buf = io.StringIO()
            with redirect_stdout(complete_buf):
                self.todo_module.cmd_complete("FIN-100")
        self.assertIn("已完成 FIN-100", complete_buf.getvalue())

        dry_buf = io.StringIO()
        with redirect_stdout(dry_buf):
            self.todo_module.cmd_complete_overdue(now_override="2026-03-25T09:30", dry_run=True)
        dry_output = dry_buf.getvalue()
        self.assertIn("DRY-RUN FIN-111 Meta fallback task @ 02:00 [meta_review_fallback]", dry_output)
        self.assertIn("DRY-RUN ID2 [每周重复] 迁移周任务 (每周三 09:00) @ 09:00", dry_output)

        live_buf = io.StringIO()
        with redirect_stdout(live_buf):
            self.todo_module.cmd_complete_overdue(now_override="2026-03-25T09:30", dry_run=False)
        live_output = live_buf.getvalue()
        self.assertIn("Meta-Review fallback completed", live_output)
        self.assertIn("已完成 FIN-111", live_output)
        self.assertIn("已完成任务 ID 2", live_output)

        conn = sqlite3.connect(self.db_path)
        periodic_row = conn.execute(
            "SELECT status, completion_mode, special_handler_result FROM periodic_occurrences WHERE id = 111"
        ).fetchone()
        legacy_row = conn.execute("SELECT status FROM entries WHERE id = 2").fetchone()
        conn.close()
        self.assertEqual(periodic_row[0], "completed")
        self.assertEqual(periodic_row[1], "fallback_handler")
        self.assertIn("Pending predictions", periodic_row[2])
        self.assertEqual(legacy_row[0], "done")

        with patch.object(self.todo_module.subprocess, "run") as mock_run:
            mock_run.return_value = subprocess.CompletedProcess(args=["python3"], returncode=0, stdout="ok", stderr="")
            add_buf = io.StringIO()
            with redirect_stdout(add_buf):
                self.todo_module.cmd_add(
                    "新增周期任务",
                    category="Inbox",
                    cycle_type="weekly",
                    time="18:30",
                    weekday=2,
                    task_kind="scheduled",
                )
        self.assertIn("已添加周期任务：新增周期任务", add_buf.getvalue())
        cmd = mock_run.call_args.args[0]
        self.assertIn("--add", cmd)
        self.assertIn("--weekday", cmd)
        self.assertIn("18:30", cmd)

    def test_unknown_special_handler_fails_closed_without_completion(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            "INSERT INTO periodic_tasks (id, name, category, cycle_type, time_of_day, event_time, timezone, special_handler, source) VALUES (12, '未知处理器任务', 'System', 'daily', '03:00', '03:00', 'Asia/Shanghai', 'unknown_handler', 'legacy_entries_migrated')"
        )
        conn.execute(
            "INSERT INTO periodic_occurrences (id, task_id, date, status, scheduled_time, scheduled_at) VALUES (112, 12, '2026-03-25', 'pending', '03:00', '2026-03-25T03:00:00')"
        )
        conn.commit()
        conn.close()

        result = self.todo_module.complete_overdue_tasks(now=datetime(2026, 3, 25, 9, 0), dry_run=False)

        self.assertIn("FIN-112", result["handled"])
        self.assertTrue(any("不支持的 special_handler" in err for err in result["errors"]))

        conn = sqlite3.connect(self.db_path)
        status = conn.execute("SELECT status FROM periodic_occurrences WHERE id = 112").fetchone()[0]
        conn.close()
        self.assertEqual(status, "pending")

    def test_snapshot_and_list_hide_migrated_legacy_entries_from_simple_views(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("ALTER TABLE entries ADD COLUMN chronos_readonly INTEGER NOT NULL DEFAULT 0")
        conn.execute("ALTER TABLE entries ADD COLUMN chronos_archived_at TEXT")
        conn.execute("ALTER TABLE entries ADD COLUMN chronos_archive_reason TEXT")
        conn.execute("ALTER TABLE entries ADD COLUMN chronos_archived_from_status TEXT")
        conn.execute("ALTER TABLE entries ADD COLUMN chronos_linked_task_id INTEGER")
        conn.execute("INSERT INTO entries (id, text, status, group_id, chronos_readonly, chronos_archived_at, chronos_archive_reason, chronos_archived_from_status, chronos_linked_task_id) VALUES (6, '已迁移旧任务', 'archived', 1, 1, '2026-03-25T16:50:00', 'Chronos legacy archive: linked to periodic_tasks.id=13', 'pending', 13)")
        conn.execute(
            "INSERT INTO periodic_tasks (id, name, category, cycle_type, time_of_day, event_time, timezone, legacy_entry_id, source) VALUES (13, '已迁移旧任务', 'Inbox', 'daily', '12:00', '12:00', 'Asia/Shanghai', 6, 'legacy_entries_migrated')"
        )
        conn.execute(
            "INSERT INTO periodic_occurrences (id, task_id, date, status, scheduled_time, scheduled_at, legacy_entry_id) VALUES (113, 13, '2026-03-25', 'pending', '12:00', '2026-03-25T12:00:00', 6)"
        )
        conn.commit()
        conn.close()

        with patch.object(self.todo_module, "ensure_today_occurrences"):
            simple_rows = self.todo_module.get_simple_pending()
        self.assertEqual([row[0] for row in simple_rows], [1, 2, 3, 4])

        show_buf = io.StringIO()
        with redirect_stdout(show_buf):
            self.todo_module.cmd_show('ID6')
        self.assertIn('状态：archived', show_buf.getvalue())
        self.assertIn('legacy 归档（只读）', show_buf.getvalue())

        manager_module = load_module("chronos_ptm_phase2_smoke", PROJECT_ROOT / "scripts" / "periodic_task_manager.py", self.db_path, self.workspace)
        manager = manager_module.PeriodicTaskManager()
        try:
            snapshot = manager._build_today_todo_snapshot(manager_module.date(2026, 3, 25))
        finally:
            manager.db.close()

        self.assertIn("FIN-113", snapshot)
        self.assertNotIn("ID6", snapshot)


if __name__ == "__main__":
    unittest.main()
