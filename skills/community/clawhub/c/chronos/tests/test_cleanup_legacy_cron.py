import importlib.util
import json
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCRIPT_PATH = PROJECT_ROOT / "scripts" / "cleanup_legacy_cron.py"
MODULE_NAME = "chronos_cleanup_legacy_cron"


def load_module(db_path: Path):
    for name in [MODULE_NAME, "core.paths", "core.openclaw_cron"]:
        sys.modules.pop(name, None)

    import os
    os.environ["CHRONOS_DB_PATH"] = str(db_path)

    spec = importlib.util.spec_from_file_location(MODULE_NAME, SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class CleanupLegacyCronTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.tempdir.name) / "todo.db"
        conn = sqlite3.connect(self.db_path)
        conn.execute("CREATE TABLE periodic_occurrences (id INTEGER PRIMARY KEY, reminder_job_id TEXT)")
        conn.execute("INSERT INTO periodic_occurrences (reminder_job_id) VALUES (?)", ("task_reminder_1_20260323",))
        conn.commit()
        conn.close()
        self.module = load_module(self.db_path)

    def tearDown(self):
        import os
        os.environ.pop("CHRONOS_DB_PATH", None)
        self.tempdir.cleanup()

    def test_classify_jobs_detects_legacy_bad_delivery(self):
        jobs = [
            {
                "id": "job-1",
                "name": "task_reminder_2_20260318",
                "enabled": False,
                "delivery": {"mode": "announce", "channel": "last"},
                "state": {"lastError": "Telegram recipient @heartbeat could not be resolved"},
            }
        ]

        candidates = self.module.classify_jobs(jobs, known_job_ids=set())

        self.assertEqual(len(candidates), 1)
        self.assertIn("legacy-bad-delivery", candidates[0]["reasons"])

    def test_classify_jobs_detects_orphaned_job(self):
        jobs = [
            {
                "id": "job-2",
                "name": "task_reminder_999_20260318",
                "enabled": True,
                "delivery": {"mode": "announce", "to": "123"},
                "state": {},
            }
        ]

        candidates = self.module.classify_jobs(jobs, known_job_ids={"task_reminder_1_20260323"})

        self.assertEqual(len(candidates), 1)
        self.assertIn("orphaned-db-reference", candidates[0]["reasons"])

    def test_remove_jobs_uses_job_id_for_cron_remove(self):
        candidates = [{"id": "job-3", "name": "task_reminder_3_20260318", "enabled": False, "reasons": ["legacy-bad-delivery"]}]

        with patch.object(self.module.subprocess, "run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stderr="")
            removed = self.module.remove_jobs(candidates)

        self.assertEqual(removed, ["job-3"])
        cmd = mock_run.call_args.args[0]
        self.assertEqual(cmd[:3], [self.module.OPENCLAW_BIN, "cron", "remove"])
        self.assertEqual(cmd[3], "job-3")

    def test_load_cron_jobs_parses_json(self):
        payload = {"jobs": [{"id": "job-4", "name": "task_reminder_4_20260318"}]}
        with patch.object(self.module.subprocess, "run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout=json.dumps(payload), stderr="")
            jobs = self.module.load_cron_jobs()

        self.assertEqual(jobs, payload["jobs"])


if __name__ == "__main__":
    unittest.main()
