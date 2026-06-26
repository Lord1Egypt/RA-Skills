import importlib.util
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import MagicMock, patch


PROJECT_ROOT = Path(__file__).resolve().parent.parent
MANAGER_SCRIPT = PROJECT_ROOT / "scripts" / "periodic_task_manager.py"

spec = importlib.util.spec_from_file_location("chronos_periodic_task_manager", MANAGER_SCRIPT)
manager_module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(manager_module)


class ReminderDeliveryTests(unittest.TestCase):
    def setUp(self):
        self.manager = manager_module.PeriodicTaskManager()

    def tearDown(self):
        self.manager.db.close()

    def _mock_task_lookup(self, task_name="测试任务", reminder_template=None):
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (task_name, reminder_template)
        return patch.object(self.manager.db, "execute", return_value=mock_cursor)

    def test_schedule_reminder_cron_uses_explicit_delivery_target(self):
        with self._mock_task_lookup(), \
             patch.object(manager_module, "get_chat_id", return_value="123456"), \
             patch.object(manager_module, "datetime", wraps=manager_module.datetime) as mock_datetime, \
             patch.object(manager_module.subprocess, "run") as mock_run:
            mock_datetime.now.return_value = manager_module.datetime(2026, 3, 23, 0, 0, tzinfo=manager_module.ZoneInfo("UTC"))
            mock_run.return_value = MagicMock(returncode=0, stderr="")

            job_name = self.manager.schedule_reminder_cron(7, date(2026, 3, 23), "10:00")

            self.assertEqual(job_name, "task_reminder_7_20260323")
            cmd = mock_run.call_args.args[0]
            self.assertIn("--announce", cmd)
            self.assertIn("--to", cmd)
            self.assertEqual(cmd[cmd.index("--to") + 1], "123456")
            self.assertIn("--session", cmd)
            self.assertEqual(cmd[cmd.index("--session") + 1], "isolated")

    def test_immediate_reminder_uses_explicit_delivery_target(self):
        with self._mock_task_lookup(), \
             patch.object(manager_module, "get_chat_id", return_value="123456"), \
             patch.object(manager_module, "datetime", wraps=manager_module.datetime) as mock_datetime, \
             patch.object(manager_module.subprocess, "run") as mock_run:
            mock_datetime.now.return_value = manager_module.datetime(2026, 3, 23, 5, 0, tzinfo=manager_module.ZoneInfo("UTC"))
            mock_run.return_value = MagicMock(returncode=0, stderr="")

            job_name = self.manager.schedule_reminder_cron(8, date(2026, 3, 23), "10:00")

            self.assertIsNone(job_name)
            cmd = mock_run.call_args.args[0]
            self.assertIn("--announce", cmd)
            self.assertIn("--to", cmd)
            self.assertEqual(cmd[cmd.index("--to") + 1], "123456")
            self.assertIn("--session", cmd)
            self.assertEqual(cmd[cmd.index("--session") + 1], "isolated")
            self.assertIn("reminder_immediate_8_20260323_1000", cmd)


if __name__ == "__main__":
    unittest.main()
