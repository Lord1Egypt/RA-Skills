from __future__ import annotations

import importlib.util
import os
import tempfile
import unittest
from argparse import Namespace
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("sentinel_wrapper.py")
SPEC = importlib.util.spec_from_file_location("sentinel_wrapper", MODULE_PATH)
assert SPEC and SPEC.loader
sentinel_wrapper = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(sentinel_wrapper)


class SentinelWrapperTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.prev_cwd = os.getcwd()
        self.prev_home = os.environ.get("AGENT_SENTINEL_HOME")
        os.chdir(self.temp_dir.name)
        os.environ["AGENT_SENTINEL_HOME"] = str(Path(self.temp_dir.name) / ".state")

    def tearDown(self) -> None:
        os.chdir(self.prev_cwd)
        if self.prev_home is None:
            os.environ.pop("AGENT_SENTINEL_HOME", None)
        else:
            os.environ["AGENT_SENTINEL_HOME"] = self.prev_home
        self.temp_dir.cleanup()

    def _json_from_stdout(self, fn, *args):
        buffer = StringIO()
        with redirect_stdout(buffer):
            fn(*args)
        return sentinel_wrapper.json.loads(buffer.getvalue())

    def test_bootstrap_creates_default_files(self) -> None:
        payload = self._json_from_stdout(sentinel_wrapper.bootstrap)

        self.assertEqual(payload["status"], "READY")
        self.assertTrue(Path("callguard.yaml").exists())
        self.assertTrue((Path(os.environ["AGENT_SENTINEL_HOME"]) / "openclaw_state.json").exists())

    def test_denied_action_is_blocked(self) -> None:
        self._json_from_stdout(sentinel_wrapper.bootstrap)

        payload = self._json_from_stdout(
            sentinel_wrapper.cmd_check,
            Namespace(cmd="rm -rf /tmp/test", cost=0.01),
        )

        self.assertEqual(payload["status"], "BLOCKED")
        self.assertIn("denied pattern", payload["error"])

    def test_allowed_action_updates_local_state(self) -> None:
        self._json_from_stdout(sentinel_wrapper.bootstrap)

        payload = self._json_from_stdout(
            sentinel_wrapper.cmd_check,
            Namespace(cmd="echo hello", cost=0.25),
        )

        self.assertEqual(payload["status"], "ALLOWED")
        self.assertEqual(payload["run_total"], 0.25)
        self.assertEqual(payload["session_total"], 0.25)
        self.assertEqual(payload["remote_sync"], False)
        self.assertTrue((Path(os.environ["AGENT_SENTINEL_HOME"]) / "openclaw_events.jsonl").exists())

    def test_sync_requires_api_key(self) -> None:
        self._json_from_stdout(sentinel_wrapper.bootstrap)
        self._json_from_stdout(
            sentinel_wrapper.cmd_check,
            Namespace(cmd="echo hello", cost=0.25),
        )

        payload = self._json_from_stdout(sentinel_wrapper.cmd_sync)

        self.assertEqual(payload["status"], "ERROR")
        self.assertIn("AGENT_SENTINEL_API_KEY", payload["message"])

    def test_reset_run_preserves_session_total(self) -> None:
        self._json_from_stdout(sentinel_wrapper.bootstrap)
        self._json_from_stdout(
            sentinel_wrapper.cmd_check,
            Namespace(cmd="echo hello", cost=0.25),
        )

        reset_payload = self._json_from_stdout(
            sentinel_wrapper.cmd_reset,
            Namespace(scope="run"),
        )

        self.assertEqual(reset_payload["status"], "RESET")
        self.assertEqual(reset_payload["run_total"], 0.0)
        self.assertEqual(reset_payload["session_total"], 0.25)


if __name__ == "__main__":
    unittest.main()
