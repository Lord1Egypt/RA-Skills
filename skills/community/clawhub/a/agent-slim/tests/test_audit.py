#!/usr/bin/env python3
"""Tests for the Agent Slim read-only audit engine (stdlib only)."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
FIXTURE = ROOT / "tests" / "fixtures" / "aging-agent"
AUDIT = SCRIPTS / "agent_slim.py"
sys.path.insert(0, str(SCRIPTS))

import agent_slim  # noqa: E402


# ClawHub 的发布器会跳过任何含点号路径段的文件，安装副本里这些隐藏 fixture
# 文件只能由测试在运行期补齐；本地源码树里它们已存在时保持不变。
HIDDEN_FIXTURE_FILES = {
    "skills/.usage.json": {
        "skills": {
            "alpha": {"lastUsedAt": "2026-10-20T10:00:00Z"},
            "beta": {"lastUsedAt": "2026-10-21T10:00:00Z"},
            "gamma": {"lastUsedAt": "2026-10-22T10:00:00Z"},
        }
    },
    "plugins/cache/test-market/plug-a/1.0.0/.mcp.json": {
        "mcpServers": {
            "fixture-tools": {
                "enabled": True,
                "tools": {"list_items": {}, "read_item": {}},
            }
        }
    },
    "plugins/cache/test-market/plug-a/1.0.0/.app.json": {
        "apps": {"fixture-app": {"required": False}}
    },
}


def ensure_hidden_fixture_files(home: Path) -> None:
    """Recreate dot-path fixture files that a ClawHub install cannot carry."""
    for rel, payload in HIDDEN_FIXTURE_FILES.items():
        path = home / rel
        if path.is_file():
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )


def tree_digest(root: Path):
    """Snapshot path metadata without opening fixture file contents."""
    result = {}
    for path in sorted(root.rglob("*")):
        if path.is_file():
            stat = path.stat()
            result[path.relative_to(root).as_posix()] = (stat.st_size, stat.st_mtime_ns)
    return result


class AuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="agent-slim-test-")
        self.home = Path(self.temp.name) / "home"
        shutil.copytree(FIXTURE, self.home)
        ensure_hidden_fixture_files(self.home)
        self.now = datetime(2026, 11, 5, 12, 0, tzinfo=timezone.utc)
        old = (self.now - timedelta(days=120)).timestamp()
        recent = (self.now - timedelta(days=1)).timestamp()
        for suffix in (
            "sessions/2024/01/rollout-old.jsonl",
            "archived_sessions/old-archive.jsonl.zst",
            "backups/snapshot.zip",
            "log/codex.log",
            "state.db",
        ):
            os.utime(self.home / suffix, (old, old))
        os.utime(self.home / "sessions/2026/01/rollout-recent.jsonl", (recent, recent))

    def tearDown(self):
        self.temp.cleanup()

    def audit(self, **kwargs):
        return agent_slim.audit_home(self.home, kwargs.get("max_depth", 8), now=self.now)

    def find_item(self, report, evidence_path):
        for layer in ("hot", "warm", "cold"):
            for item in report["layers"][layer]:
                if item["evidencePath"] == evidence_path:
                    return item
        self.fail("missing item: {}".format(evidence_path))

    def test_contract_and_aging_fixture(self):
        report = self.audit()
        for key in (
            "schemaVersion", "runId", "createdAt", "host", "scope", "tokenEstimate",
            "summary", "layers", "candidates", "referenceGraph", "plugins",
            "warnings", "unknowns", "errors",
        ):
            self.assertIn(key, report)
        self.assertEqual(report["schemaVersion"], "1.0")
        self.assertEqual(report["mode"], "dry-run")
        self.assertFalse(report["scope"]["sessionContentRead"])
        self.assertEqual(report["tokenEstimate"]["algorithm"], "ceil(chars * tokensPerChar)")
        self.assertIn("approximate", report["tokenEstimate"]["kind"])
        self.assertEqual(report["summary"]["status"], "WARN")

        hot = report["layers"]["hot"]
        warm = report["layers"]["warm"]
        cold = report["layers"]["cold"]
        self.assertTrue(any(item["category"] == "instructions" for item in hot))
        self.assertTrue(any(item["category"] == "memory" for item in hot))
        self.assertTrue(any(item["category"] == "plugin" for item in hot))
        self.assertTrue(any(item["category"] == "skill-metadata" for item in hot))
        self.assertTrue(any(item["category"] == "skill-body" for item in warm))
        self.assertTrue(any(item["category"] == "reference" for item in warm))
        self.assertTrue(any(item["category"] == "sessions" for item in cold))
        self.assertTrue(any(item["category"] == "backups" for item in cold))
        self.assertTrue(any(item["category"] == "logs" for item in cold))
        self.assertTrue(any(item["category"] == "databases" for item in cold))

        beta_meta = self.find_item(report, "skills/beta/SKILL.md")
        self.assertEqual(beta_meta["layer"], "hot")
        self.assertGreater(beta_meta["chars"], 600)
        self.assertTrue(beta_meta["candidate"])

        huge = self.find_item(report, "skills/beta/references/huge.md")
        self.assertEqual(huge["layer"], "warm")
        self.assertGreater(huge["estimatedTokens"], 10000)

        sessions = self.find_item(report, "sessions/")
        self.assertGreaterEqual(sessions["meta"]["oldFileCount"], 1)
        self.assertGreaterEqual(sessions["meta"]["oldBytes"], 1)
        self.assertTrue(any(c["action"] == "archive-verified-old-sessions" for c in report["candidates"]))
        self.assertTrue(any(c["action"] == "review-backup-retention" for c in report["candidates"]))
        self.assertTrue(any(w["code"] == "WIDE_SKILL_DESCRIPTION" for w in report["warnings"]))
        self.assertTrue(any(w["code"] == "DUPLICATE_HOT_CONTENT" for w in report["warnings"]))
        self.assertTrue(any(w["code"] == "BROKEN_REFERENCE" for w in report["warnings"]) is False)

        plugins = {record["name"]: record for record in report["plugins"]}
        self.assertTrue(plugins["plug-a"]["discovered"])
        self.assertIn("fixture-tools", plugins["plug-a"]["toolSurface"]["mcpServers"])
        self.assertIn("list_items", plugins["plug-a"]["toolSurface"]["declaredTools"])
        self.assertIn("fixture-app", plugins["plug-a"]["toolSurface"]["apps"])
        self.assertFalse(plugins["missing"]["discovered"])
        self.assertTrue(any(u["code"] == "SESSION_BODY_NOT_READ" for u in report["unknowns"]))

        alpha = self.find_item(report, "skills/alpha/SKILL.md")
        # The same evidence path has both hot metadata and warm body; pick the hot item explicitly.
        self.assertEqual(alpha["layer"], "hot")
        self.assertTrue(alpha["meta"]["recentUse"]["recorded"])

    def test_ordering_and_two_runs_are_stable_except_time(self):
        first = self.audit()
        second = self.audit()
        first.pop("createdAt")
        second.pop("createdAt")
        self.assertEqual(first, second)
        self.assertEqual(first["runId"], second["runId"])
        layer_order = {"hot": 0, "warm": 1, "cold": 2}
        seen = [layer_order[c["layer"]] for c in first["candidates"]]
        self.assertEqual(seen, sorted(seen))
        for layer in ("hot", "warm"):
            tokens = [item["estimatedTokens"] or 0 for item in first["layers"][layer]]
            by_category = {}
            for item in first["layers"][layer]:
                by_category.setdefault(item["category"], []).append(item["estimatedTokens"] or 0)
            for values in by_category.values():
                self.assertEqual(values, sorted(values, reverse=True))

    def test_session_bodies_and_database_content_are_not_read(self):
        opened = []
        original_open = Path.open

        def recording_open(path, *args, **kwargs):
            opened.append(Path(path).resolve())
            return original_open(path, *args, **kwargs)

        with mock.patch.object(Path, "open", new=recording_open):
            self.audit()
        protected_roots = {"sessions", "archived_sessions"}
        for path in opened:
            self.assertFalse(protected_roots.intersection(path.parts), str(path))
            self.assertFalse(path.name in {"state.db", "snapshot.zip", "codex.log"}, str(path))

    def test_audit_does_not_write_home(self):
        before = tree_digest(self.home)
        self.audit()
        after = tree_digest(self.home)
        self.assertEqual(before, after)

    def test_cli_json_warning_gate_usage_and_output(self):
        before = tree_digest(self.home)
        command = [sys.executable, str(AUDIT), "audit", "--home", str(self.home), "--json"]
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        parsed = json.loads(result.stdout)
        self.assertEqual(parsed["schemaVersion"], "1.0")

        warning_result = subprocess.run(command + ["--fail-on-warning"], capture_output=True, text=True)
        self.assertEqual(warning_result.returncode, 2, warning_result.stderr)
        json.loads(warning_result.stdout)

        usage_result = subprocess.run([sys.executable, str(AUDIT)], capture_output=True, text=True)
        self.assertEqual(usage_result.returncode, 64, usage_result.stderr)

        missing = Path(self.temp.name) / "does-not-exist"
        missing_result = subprocess.run(
            [sys.executable, str(AUDIT), "audit", "--home", str(missing), "--json"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(missing_result.returncode, 74, missing_result.stderr)
        self.assertEqual(json.loads(missing_result.stdout)["summary"]["status"], "FAIL")

        output_path = Path(self.temp.name) / "audit-output.json"
        output_result = subprocess.run(
            [sys.executable, str(AUDIT), "audit", "--home", str(self.home), "--json", "--output", str(output_path)],
            capture_output=True,
            text=True,
        )
        self.assertEqual(output_result.returncode, 0, output_result.stderr)
        self.assertTrue(output_path.is_file())
        self.assertEqual(json.loads(output_path.read_text(encoding="utf-8"))["schemaVersion"], "1.0")
        self.assertEqual(before, tree_digest(self.home))

    def test_markdown_and_max_depth(self):
        report = self.audit(max_depth=1)
        markdown = agent_slim.render_markdown(report)
        self.assertIn("# Agent Slim 只读审计报告", markdown)
        self.assertIn("近似值", markdown)
        self.assertIn("Cold 仅为磁盘账本", markdown)

    def test_empty_home_degrades_without_crash(self):
        empty = Path(self.temp.name) / "empty-home"
        empty.mkdir()
        report = agent_slim.audit_home(empty, 3, now=self.now)
        self.assertEqual(report["summary"]["status"], "WARN")
        codes = {warning["code"] for warning in report["warnings"]}
        self.assertTrue({"AGENTS_MISSING", "RULES_INDEX_MISSING", "MEMORY_SUMMARY_MISSING", "SKILLS_NOT_FOUND"}.issubset(codes))

    def test_codex_home_environment_and_no_private_path_hardcoding(self):
        with mock.patch.dict(os.environ, {"CODEX_HOME": str(self.home)}, clear=False):
            detected, source = agent_slim.detect_codex_home()
        self.assertEqual(detected, self.home.resolve())
        self.assertEqual(source, "environment")
        source_text = AUDIT.read_text(encoding="utf-8")
        self.assertNotIn("/" + "Users/", source_text)
        self.assertNotIn("C:" + "\\\\Users\\\\", source_text)
        self.assertNotRegex(source_text, r"(?i)sk-[a-z0-9_-]{16,}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
