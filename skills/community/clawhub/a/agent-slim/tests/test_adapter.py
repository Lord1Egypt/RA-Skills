#!/usr/bin/env python3
"""Tests for the side-effect-free Codex host capability adapter."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
CLI = SCRIPTS / "agent_slim.py"
sys.path.insert(0, str(SCRIPTS))

import agent_slim_adapter as adapter  # noqa: E402


def metadata_snapshot(root: Path):
    result = {}
    for path in sorted(root.rglob("*")):
        if path.is_file():
            stat = path.stat()
            result[path.relative_to(root).as_posix()] = (stat.st_size, stat.st_mtime_ns, stat.st_mode)
    return result


class AdapterTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="agent-slim-adapter-")
        self.base = Path(self.temp.name)
        self.home = self.base / "home"
        self.home.mkdir()
        (self.home / "sessions").mkdir()
        (self.home / "skills").mkdir()
        (self.home / "skills" / ".usage.json").write_text("{}\n", encoding="utf-8")
        (self.home / "scripts").mkdir()
        token_tool = self.home / "scripts" / "token-usage.sh"
        token_tool.write_text("#!/bin/sh\nprintf '0 0\\n'\n", encoding="utf-8")
        token_tool.chmod(0o755)
        (self.home / "config.toml").write_text("[plugins.'demo@fixture']\nenabled = false\n", encoding="utf-8")

    def tearDown(self):
        self.temp.cleanup()

    def test_complete_home_reports_proven_capabilities(self):
        report = adapter.probe_codex_home(self.home)
        caps = report["capabilities"]
        for name in (
            "hot_warm_cold_inventory",
            "frontmatter_parse",
            "reference_graph",
            "token_usage_read",
            "skill_usage_index",
            "safe_move",
            "quarantine",
            "session_archive",
            "rollback",
        ):
            self.assertEqual(caps[name], "supported", name)
        self.assertEqual(caps["plugin_management"], "unsupported")
        self.assertEqual(caps["plugin_disable"], "unsupported")
        self.assertEqual(caps["regression_runner"], "unknown")
        self.assertEqual(report["unknown"], ["regression_runner"])
        self.assertIn("plugin_disable", report["unsupported"])
        self.assertFalse(report["scope"]["contentRead"])
        self.assertNotIn(str(self.home), json.dumps(report, ensure_ascii=False))

    def test_missing_sessions_usage_and_token_tool_degrade(self):
        (self.home / "sessions").rmdir()
        (self.home / "skills" / ".usage.json").unlink()
        (self.home / "scripts" / "token-usage.sh").unlink()
        caps = adapter.probe_codex_home(self.home)["capabilities"]
        self.assertEqual(caps["session_archive"], "unknown")
        self.assertEqual(caps["skill_usage_index"], "unknown")
        self.assertEqual(caps["token_usage_read"], "unknown")

    def test_missing_home_never_pretends_to_support_work(self):
        missing = self.base / "missing-home"
        report = adapter.probe_codex_home(missing)
        caps = report["capabilities"]
        for name in (
            "hot_warm_cold_inventory",
            "frontmatter_parse",
            "reference_graph",
            "safe_move",
            "quarantine",
            "session_archive",
        ):
            self.assertEqual(caps[name], "unknown", name)
        self.assertEqual(caps["plugin_management"], "unsupported")
        self.assertEqual(caps["plugin_disable"], "unsupported")
        self.assertEqual(caps["rollback"], "supported")
        self.assertEqual(report["detected"]["homeExists"], False)

    def test_non_writable_home_degrades_move_and_quarantine(self):
        real_access = os.access

        def fake_access(path, mode):
            try:
                if Path(path).resolve() == self.home.resolve() and mode == os.W_OK:
                    return False
            except OSError:
                pass
            return real_access(path, mode)

        with mock.patch.object(adapter.os, "access", side_effect=fake_access):
            caps = adapter.probe_codex_home(self.home)["capabilities"]
        self.assertEqual(caps["safe_move"], "unknown")
        self.assertEqual(caps["quarantine"], "unknown")
        self.assertEqual(caps["session_archive"], "supported")

    def test_require_capability_refuses_unknown_and_unsupported(self):
        report = adapter.probe_codex_home(self.home)
        self.assertEqual(adapter.capability_status(report, "plugin_disable"), "unsupported")
        with self.assertRaises(adapter.CapabilityUnavailable) as unsupported:
            adapter.require_capability(report, "plugin_disable")
        self.assertEqual(unsupported.exception.status, "unsupported")
        with self.assertRaises(adapter.CapabilityUnavailable) as unknown:
            adapter.require_capability(report, "regression_runner")
        self.assertEqual(unknown.exception.status, "unknown")
        adapter.require_capability(report, "safe_move")

    def test_host_cli_is_read_only_and_emits_no_absolute_home(self):
        before = metadata_snapshot(self.home)
        result = subprocess.run(
            [sys.executable, str(CLI), "host", "--home", str(self.home)],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["kind"], "agent-slim-host-capabilities")
        self.assertNotIn(str(self.home), result.stdout)
        self.assertNotIn("/" + "Users/", result.stdout)
        self.assertEqual(metadata_snapshot(self.home), before)

    def test_adapter_source_has_no_memory_threshold_copy(self):
        source = (SCRIPTS / "agent_slim_adapter.py").read_text(encoding="utf-8")
        self.assertNotRegex(source, r"150(?:,|，)?000|15\s*万\s*Token")
        self.assertNotRegex(source, r"(?<![A-Za-z0-9])8\s*轮")


if __name__ == "__main__":
    unittest.main(verbosity=2)
