import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import core.openclaw_cron as cron_module


class OpenClawCronHelperTests(unittest.TestCase):
    def test_build_cron_add_command_includes_explicit_delivery_target(self):
        cmd = cron_module.build_cron_add_command(
            job_name="task_reminder_1_20260323",
            at_iso="2026-03-23T01:55:00.000Z",
            message="hello",
            chat_id="123456",
        )

        self.assertEqual(cmd[:3], [cron_module.OPENCLAW_BIN, "cron", "add"])
        self.assertIn("--announce", cmd)
        self.assertIn("--to", cmd)
        self.assertEqual(cmd[cmd.index("--to") + 1], "123456")
        self.assertEqual(cmd[cmd.index("--session") + 1], "isolated")

    def test_build_cron_remove_command_uses_job_name(self):
        cmd = cron_module.build_cron_remove_command("task_reminder_1_20260323")
        self.assertEqual(cmd, [cron_module.OPENCLAW_BIN, "cron", "remove", "task_reminder_1_20260323"])


if __name__ == "__main__":
    unittest.main()
