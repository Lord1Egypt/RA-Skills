import json
import os
import subprocess
import tempfile
import unittest


SCRIPT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BIN_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "bin"))
DEV_RELAY = os.path.join(BIN_DIR, "dev-relay.sh")


class GuardActivateBypassTests(unittest.TestCase):
    def test_guard_activate_does_not_require_platform_credentials(self):
        with tempfile.TemporaryDirectory() as td:
            env = dict(os.environ)
            env["XDG_STATE_HOME"] = td
            env["HOME"] = td
            env["OPENCLAW_SESSION_KEY"] = "acct:discord:thread:123"
            env["OPENCLAW_SESSION"] = env["OPENCLAW_SESSION_KEY"]

            proc = subprocess.run(
                ["/bin/bash", DEV_RELAY, "--activate", "-P", "auto"],
                capture_output=True,
                text=True,
                env=env,
            )

            self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)
            self.assertIn("Codeflow guard activated.", proc.stdout)
            self.assertNotIn(".webhook-url", proc.stderr)
            self.assertNotIn("Telegram bot token", proc.stderr)

            state_path = os.path.join(td, "codeflow", "guard.json")
            with open(state_path, "r", encoding="utf-8") as f:
                state = json.load(f)

            self.assertTrue(state["guard"]["active"])
            self.assertEqual(state["guard"]["platform"], "discord")


if __name__ == "__main__":
    unittest.main()
