#!/usr/bin/env python3
"""Focused tests for LaunchAgent sync lifecycle and conditional indexing."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch


MODULE_PATH = Path(__file__).parents[2] / "scripts" / "auto_sync.py"
if str(MODULE_PATH.parent) not in sys.path:
    sys.path.insert(0, str(MODULE_PATH.parent))


def load_module():
    spec = importlib.util.spec_from_file_location("agent_asset_auto_sync", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class AutoSyncTest(unittest.TestCase):
    def setUp(self) -> None:
        self.module = load_module()

    def test_launch_agent_payload_has_watch_and_heartbeat(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            tool = root / "tools" / "cleanup_convert.py"
            tool.parent.mkdir(parents=True)
            tool.write_text("#!/usr/bin/env python3\n", encoding="utf-8")
            payload = self.module.launch_agent_payload(root, "docs", tool, 90)
        self.assertEqual(payload["StartInterval"], 3600)
        self.assertIn(str(root / "docs"), payload["WatchPaths"])
        self.assertIn(str(root / "Archived" / "docs"), payload["WatchPaths"])
        self.assertIn("--run", payload["ProgramArguments"])
        self.assertIn("--debounce-seconds", payload["ProgramArguments"])

    def test_status_reports_pending_and_stale_heartbeat(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self.module.atomic_json(
                self.module.state_path(root),
                {
                    "last_success_at": "2020-01-01T00:00:00+00:00",
                    "last_heartbeat_at": "2020-01-01T00:00:00+00:00",
                    "last_sync": {"pending_review": 1, "failed": 0},
                },
            )
            status = self.module.status_for_state(root)
        self.assertEqual(status["status"], "attention")
        self.assertIn("pending_over_15m", status["problems"])
        self.assertIn("heartbeat_overdue", status["problems"])

    def test_run_refreshes_index_only_when_adapter_marks_change_set_ready(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            tool = root / "tools" / "cleanup_convert.py"
            tool.parent.mkdir(parents=True)
            tool.write_text(
                "import json, sys\n"
                "payload = {'summary': {'ready_for_scope_index': True}} if '--audit-agent-assets' in sys.argv else "
                "{'added': 1, 'modified': 0, 'removed': 0, 'moved': 0, 'failed': 0, 'index_ready': True}\n"
                "print(json.dumps(payload))\n",
                encoding="utf-8",
            )
            index = root / "routine_update.py"
            index.write_text(
                "import json\n"
                "print(json.dumps({'summary': {'indexed_documents': 1}}))\n",
                encoding="utf-8",
            )
            with (
                patch.object(self.module, "SECOND_BRAIN_ROUTINE", index),
                patch.object(self.module, "notify"),
            ):
                result = self.module.run_automatic_sync(root, ".", tool, debounce_seconds=0, auto_keep=True)
            state = self.module.load_state(root)
        self.assertEqual(result["status"], "ok")
        self.assertIsNotNone(result["index"])
        self.assertTrue(state["last_indexed_at"])

    def test_run_keeps_prior_index_when_adapter_reports_pending_or_no_change(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            tool = root / "tools" / "cleanup_convert.py"
            tool.parent.mkdir(parents=True)
            tool.write_text(
                "import json\n"
                "print(json.dumps({'added': 0, 'modified': 0, 'removed': 0, 'moved': 0, 'failed': 0, 'index_ready': False}))\n",
                encoding="utf-8",
            )
            with patch.object(self.module, "notify"):
                result = self.module.run_automatic_sync(root, ".", tool, debounce_seconds=0)
            state = self.module.load_state(root)
        self.assertEqual(result["status"], "ok")
        self.assertIsNone(result["index"])
        self.assertNotIn("last_indexed_at", state)


if __name__ == "__main__":
    unittest.main()
