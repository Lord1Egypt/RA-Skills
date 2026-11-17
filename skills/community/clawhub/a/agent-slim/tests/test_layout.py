#!/usr/bin/env python3
"""Tests for the optional layout description that makes the audit host-agnostic."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "agent_slim.py"


class LayoutTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="agent-slim-layout-")
        self.base = Path(self.temp.name)
        self.home = self.base / "home"
        (self.home / "my").mkdir(parents=True)
        (self.home / "skills" / "alpha").mkdir(parents=True)
        (self.home / "state" / "sessions").mkdir(parents=True)
        (self.home / "logs").mkdir(parents=True)
        (self.home / "my" / "rules.md").write_text("# rules\nAlways answer briefly.\n", encoding="utf-8")
        (self.home / "my" / "MEMORY.md").write_text("User prefers short answers.\n", encoding="utf-8")
        (self.home / "skills" / "alpha" / "SKILL.md").write_text(
            "---\nname: alpha\ndescription: demo skill\n---\n\n# Alpha\n", encoding="utf-8"
        )
        (self.home / "state" / "sessions" / "s1.jsonl").write_text('{"role":"user"}\n', encoding="utf-8")
        (self.home / "logs" / "app.log").write_text("boot\n", encoding="utf-8")
        # Default vendor detection still sees a Codex-shaped home.
        (self.home / "AGENTS.md").write_text("# agents\n", encoding="utf-8")
        (self.home / "config.toml").write_text("[plugins]\n", encoding="utf-8")
        (self.home / "sessions").mkdir(exist_ok=True)

    def tearDown(self):
        self.temp.cleanup()

    def write_layout(self, payload) -> Path:
        path = self.base / "layout.json"
        if isinstance(payload, str):
            path.write_text(payload, encoding="utf-8")
        else:
            path.write_text(json.dumps(payload), encoding="utf-8")
        return path

    def run_audit(self, *extra):
        return subprocess.run(
            [sys.executable, str(CLI), "audit", "--home", str(self.home), "--json", *extra],
            capture_output=True,
            text=True,
        )

    def test_layout_is_reported_and_drives_the_hot_layer(self):
        layout = self.write_layout(
            {
                "host": "my-agent",
                "hot": [
                    {"path": "my/rules.md", "category": "instructions"},
                    {"path": "my/MEMORY.md", "category": "memory", "loadedWhen": "startup-memory-summary"},
                ],
                "skillRoots": ["skills"],
                "sessionRoots": ["state/sessions"],
                "logRoots": ["logs"],
            }
        )
        result = self.run_audit("--layout", str(layout))
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["host"]["kind"], "my-agent")
        self.assertTrue(report["host"]["layoutDescribed"])
        hot = report["layers"]["hot"]
        names = [item.get("source") or item.get("path") or item.get("name") for item in hot]
        rendered = json.dumps(hot, ensure_ascii=False)
        self.assertIn("MEMORY.md", rendered)
        self.assertIn("rules.md", rendered)
        self.assertTrue(names)
        self.assertGreater(report["summary"]["layers"]["hot"]["estimatedTokens"], 0)
        self.assertEqual(report["summary"]["disk"]["categories"]["sessions"]["fileCount"], 1)

    def test_layout_replaces_vendor_missing_warnings(self):
        layout = self.write_layout({"host": "my-agent", "hot": ["missing/NOT_THERE.md"]})
        report = json.loads(self.run_audit("--layout", str(layout)).stdout)
        codes = [warning["code"] for warning in report["warnings"]]
        self.assertIn("HOT_FILE_MISSING", codes)
        for vendor_code in ("AGENTS_MISSING", "RULES_INDEX_MISSING", "MEMORY_SUMMARY_MISSING"):
            self.assertNotIn(vendor_code, codes)

    def test_without_layout_vendor_detection_is_unchanged(self):
        report = json.loads(self.run_audit().stdout)
        self.assertEqual(report["host"]["kind"], "codex")
        self.assertFalse(report["host"]["layoutDescribed"])

    def test_path_escape_is_rejected(self):
        layout = self.write_layout({"hot": ["../../etc/passwd"]})
        result = self.run_audit("--layout", str(layout))
        self.assertEqual(result.returncode, 64)
        self.assertIn("LAYOUT_PATH_REJECTED", result.stderr)

    def test_absolute_path_is_rejected(self):
        layout = self.write_layout({"sessionRoots": ["/tmp/anywhere"]})
        result = self.run_audit("--layout", str(layout))
        self.assertEqual(result.returncode, 64)
        self.assertIn("LAYOUT_PATH_REJECTED", result.stderr)

    def test_unreadable_layout_fails_closed(self):
        layout = self.write_layout("{not json")
        result = self.run_audit("--layout", str(layout))
        self.assertEqual(result.returncode, 64)
        self.assertIn("LAYOUT_UNREADABLE", result.stderr)

    def test_host_command_echoes_declared_layout(self):
        layout = self.write_layout({"host": "my-agent", "hot": ["my/rules.md"], "sessionRoots": ["state/sessions"]})
        result = subprocess.run(
            [sys.executable, str(CLI), "host", "--home", str(self.home), "--layout", str(layout)],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["host"], "my-agent")
        self.assertTrue(report["layoutDescribed"])
        self.assertEqual(report["layout"]["hotEntryCount"], 1)
        self.assertEqual(report["layout"]["sessionRoots"], ["state/sessions"])


if __name__ == "__main__":
    unittest.main()
