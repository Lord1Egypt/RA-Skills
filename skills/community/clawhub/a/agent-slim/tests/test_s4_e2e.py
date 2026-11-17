#!/usr/bin/env python3
"""s4 end-to-end tests for the synthesized three-month-old Agent fixture.

The suite exercises the public CLI only.  It proves that audit and planning are
read-only, that all three allowlisted actions can be applied and verified, that
restore returns the whole fixture Home to its exact pre-transaction state, and
that stale/conflicting inputs stop without overwriting user content.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
TESTS = ROOT / "tests"
FIXTURES = TESTS / "fixtures"
CLI = SCRIPTS / "agent_slim.py"
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(TESTS))
sys.path.insert(0, str(FIXTURES))

import build_aging_agent_s4 as fixture_builder  # noqa: E402
from test_workflow import file_state, load_schema, validate_json_schema  # noqa: E402


def state_digest(state):
    payload = json.dumps(state, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


class S4EndToEnd(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="agent-slim-s4-")
        self.base = Path(self.temp.name)
        self.home = self.base / "home"
        self.meta = fixture_builder.build(self.home)
        self.baseline = file_state(self.home)
        self.baseline_digest = state_digest(self.baseline)
        self.state_root = self.base / "transactions"
        self.audit_path = self.base / "audit.json"
        self.plan_path = self.base / "plan.json"
        self.audit_log = self.base / "audit.log"
        self.prompts_path = self.base / "test-prompts.json"
        self.router_path = self.base / "trigger-router.json"

    def tearDown(self):
        self.temp.cleanup()

    def run_cli(self, *args, expect=0):
        completed = subprocess.run(
            [sys.executable, str(CLI), *map(str, args)],
            capture_output=True,
            text=True,
        )
        if completed.returncode != expect:
            self.fail(
                "CLI returned {} expected {}:\nstdout={}\nstderr={}".format(
                    completed.returncode, expect, completed.stdout, completed.stderr
                )
            )
        value = json.loads(completed.stdout) if completed.stdout.strip() else None
        return completed, value

    def audit(self):
        self.run_cli("audit", "--home", self.home, "--json", "--output", self.audit_path)
        report = json.loads(self.audit_path.read_text(encoding="utf-8"))
        self.assertEqual(report["schemaVersion"], "1.0")
        self.assertEqual(report["scope"]["sessionContentRead"], False)
        return report

    def plan(self, report):
        self.run_cli(
            "plan",
            "--audit",
            self.audit_path,
            "--confirm",
            self.meta["oldSession"],
            "--confirm",
            self.meta["orphanFile"],
            "--state-root",
            self.state_root,
            "--output",
            self.plan_path,
        )
        value = json.loads(self.plan_path.read_text(encoding="utf-8"))
        self.assertEqual(validate_json_schema(value, load_schema("plan.schema.json")), [])
        return value

    def write_prompt_contract(self, report):
        mapping = {}
        for record in report["triggerIndex"]:
            mapping.setdefault(record["trigger"], []).append(record["skill"])
        self.router_path.write_text(json.dumps(mapping, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        router_code = (
            "import json,os,sys;"
            "m=json.load(open(sys.argv[1],encoding='utf-8'));"
            "p=os.environ.get('AGENT_SLIM_PROMPT','');"
            "print(','.join(m.get(p,['none'])))"
        )
        command = [sys.executable, "-c", router_code, str(self.router_path)]
        cases = [
            {"id": "trigger-inbox", "prompt": "整理收件箱", "command": command, "expect": {"exitCode": 0, "stdoutContains": "skill-01"}},
            {"id": "trigger-monthly", "prompt": "生成月报", "command": command, "expect": {"exitCode": 0, "stdoutContains": "skill-30"}},
            {"id": "ambiguous-room", "prompt": self.meta["ambiguousTrigger"], "command": command, "expect": {"exitCode": 0, "stdoutContains": "none"}},
            {"id": "plugin-route", "prompt": "插件能力", "command": command, "expect": {"exitCode": 0, "stdoutContains": "plugin-skill"}},
        ]
        self.prompts_path.write_text(
            json.dumps({"test_cases": cases}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        return mapping

    def test_full_roundtrip_preserves_every_home_file(self):
        report = self.audit()
        self.assertEqual(file_state(self.home), self.baseline)

        self.assertEqual(len([item for item in report["layers"]["hot"] if item["category"] == "skill-metadata"]), 31)
        self.assertEqual(len(report["layers"]["warm"]), 61)
        self.assertEqual(len(report["triggerIndex"]), 61)
        disk_categories = report["summary"]["disk"]["categories"]
        self.assertEqual(disk_categories["sessions"]["fileCount"], 100)
        self.assertEqual(disk_categories["archived-sessions"]["fileCount"], 3)
        self.assertEqual(disk_categories["backups"]["fileCount"], 3)
        session_item = next(item for item in report["layers"]["cold"] if item["evidencePath"] == "sessions/")
        archived_item = next(item for item in report["layers"]["cold"] if item["evidencePath"] == "archived-sessions/")
        self.assertEqual(session_item["meta"]["fileCount"], 100)
        self.assertEqual(session_item["meta"]["oldFileCount"], 40)
        self.assertEqual(archived_item["meta"]["fileCount"], 3)
        self.assertEqual({warning["code"] for warning in report["warnings"]}, {"DUPLICATE_HOT_CONTENT"})
        self.assertEqual(report["errors"], [])
        disabled = next(record for record in report["plugins"] if record["name"] == "legacy-helper")
        active = next(record for record in report["plugins"] if record["name"] == "active-helper")
        self.assertFalse(disabled["declaredEnabled"])
        self.assertFalse(disabled["discovered"])
        self.assertTrue(active["declaredEnabled"])
        self.assertTrue(active["discovered"])

        triggers = {}
        for record in report["triggerIndex"]:
            triggers.setdefault(record["trigger"], set()).add(record["skill"])
        self.assertEqual(triggers["整理收件箱"], {"skill-01"})
        self.assertEqual(triggers["生成月报"], {"skill-30"})
        self.assertNotIn(self.meta["ambiguousTrigger"], triggers)
        mapping = self.write_prompt_contract(report)

        plan = self.plan(report)
        self.assertEqual(file_state(self.home), self.baseline)
        self.assertEqual(state_digest(file_state(self.home)), self.baseline_digest)
        self.assertFalse(self.state_root.exists())
        ready = [action for action in plan["actions"] if action["status"] == "ready"]
        self.assertEqual(len(ready), 3)
        self.assertEqual(
            {action["action"] for action in ready},
            {
                "quarantine-redundant-backup",
                "archive-verified-old-session",
                "quarantine-low-frequency-file",
            },
        )
        self.assertGreaterEqual(len(plan["preservedFiles"]), 60)
        self.assertTrue(plan["parseChecks"])

        _, dry = self.run_cli("apply", "--plan", self.plan_path, "--audit-log", self.audit_log)
        self.assertEqual(dry["status"], "dry-run")
        self.assertEqual(len(dry["planned"]), 3)
        self.assertEqual(file_state(self.home), self.baseline)
        self.assertFalse(self.state_root.exists())
        self.assertFalse(self.audit_log.exists())

        target_paths = {action["target"]["path"] for action in ready}
        _, applied = self.run_cli(
            "apply", "--plan", self.plan_path, "--apply", "--audit-log", self.audit_log
        )
        self.assertEqual(applied["status"], "applied")
        self.assertEqual(len(applied["applied"]), 3)
        for relative in target_paths:
            self.assertFalse((self.home / relative).exists(), relative)

        manifest_path = Path(plan["transaction"]["manifestPath"])
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(validate_json_schema(manifest, load_schema("transaction-manifest.schema.json")), [])
        sidecar = (manifest_path.parent / "manifest.sha256").read_text(encoding="utf-8").strip()
        self.assertEqual(hashlib.sha256(manifest_path.read_bytes()).hexdigest(), sidecar)
        restore_shell = Path(plan["transaction"]["restoreShellPath"])
        shell_check = subprocess.run(["sh", "-n", str(restore_shell)], capture_output=True, text=True)
        self.assertEqual(shell_check.returncode, 0, shell_check.stderr)

        for record in plan["preservedFiles"]:
            path = self.home / record["path"]
            self.assertTrue(path.is_file(), record["path"])
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), record["sha256"])

        _, verified = self.run_cli(
            "verify",
            "--plan",
            self.plan_path,
            "--phase",
            "applied",
            "--test-prompts",
            self.prompts_path,
        )
        self.assertEqual(validate_json_schema(verified, load_schema("verification.schema.json")), [])
        self.assertEqual(verified["summary"]["status"], "PASS")
        checks = {check["id"]: check for check in verified["checks"]}
        self.assertEqual(checks["target-state"]["status"], "PASS")
        self.assertEqual(checks["backup-sha256"]["status"], "PASS")
        self.assertEqual(checks["retained-files"]["status"], "PASS")
        self.assertEqual(checks["reference-integrity"]["status"], "PASS")
        self.assertEqual(checks["json-yaml-frontmatter"]["status"], "PASS")
        self.assertEqual(checks["trigger-routing-regression"]["status"], "PASS")
        self.assertEqual(len(checks["trigger-routing-regression"]["cases"]), 4)

        _, restored = self.run_cli(
            "restore",
            "--manifest",
            str(manifest_path),
            "--apply",
            "--audit-log",
            self.audit_log,
        )
        self.assertEqual(restored["status"], "restored")
        self.assertTrue(restored["hashMatches"])
        self.assertEqual(file_state(self.home), self.baseline)
        self.assertEqual(state_digest(file_state(self.home)), self.baseline_digest)

        _, again = self.run_cli(
            "restore",
            "--manifest",
            str(manifest_path),
            "--apply",
            "--audit-log",
            self.audit_log,
        )
        self.assertEqual(again["status"], "already-restored")
        self.assertEqual(file_state(self.home), self.baseline)

        _, restored_verify = self.run_cli(
            "verify",
            "--plan",
            self.plan_path,
            "--phase",
            "restored",
            "--test-prompts",
            self.prompts_path,
        )
        self.assertEqual(restored_verify["summary"]["status"], "PASS")
        self.assertEqual(mapping["整理收件箱"], ["skill-01"])
        self.assertNotIn(self.meta["ambiguousTrigger"], mapping)

        events = {
            json.loads(line)["event"]
            for line in self.audit_log.read_text(encoding="utf-8").splitlines()
        }
        self.assertTrue(
            {
                "transaction-begin",
                "apply-move",
                "transaction-applied",
                "restore-begin",
                "restore-move",
                "restore-complete",
            }.issubset(events)
        )

    def test_invalid_action_is_rejected_with_usage_exit(self):
        plan = self.plan(self.audit())
        ready = next(action for action in plan["actions"] if action["status"] == "ready")
        ready["action"] = "delete-original"
        bad_plan = self.base / "bad-plan.json"
        bad_plan.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        _, result = self.run_cli(
            "apply", "--plan", bad_plan, "--apply", "--audit-log", self.audit_log, expect=64
        )
        self.assertEqual(result["code"], "ACTION_NOT_ALLOWED")
        self.assertEqual(file_state(self.home), self.baseline)

    def test_stale_plan_stops_before_transaction(self):
        plan = self.plan(self.audit())
        target = self.home / self.meta["orphanFile"]
        target.write_text("user changed this file after planning\n", encoding="utf-8")
        changed = target.read_text(encoding="utf-8")
        _, result = self.run_cli(
            "apply", "--plan", self.plan_path, "--apply", "--audit-log", self.audit_log, expect=3
        )
        self.assertEqual(result["status"], "blocked")
        self.assertEqual(result["failed"][0]["code"], "PLAN_STALE")
        self.assertFalse(Path(plan["transaction"]["dir"]).exists())
        self.assertEqual(target.read_text(encoding="utf-8"), changed)

    def test_existing_transaction_directory_is_never_reused(self):
        plan = self.plan(self.audit())
        Path(plan["transaction"]["dir"]).mkdir(parents=True)
        _, result = self.run_cli(
            "apply", "--plan", self.plan_path, "--apply", "--audit-log", self.audit_log, expect=3
        )
        self.assertEqual(result["status"], "blocked")
        self.assertEqual(result["failed"][0]["code"], "TRANSACTION_EXISTS")
        for action in plan["actions"]:
            if action["status"] == "ready":
                self.assertTrue((self.home / action["target"]["path"]).is_file())

    def test_restore_conflict_keeps_new_user_content_and_backup(self):
        report = self.audit()
        plan = self.plan(report)
        self.run_cli("apply", "--plan", self.plan_path, "--apply", "--audit-log", self.audit_log)
        target = self.home / self.meta["orphanFile"]
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("later user content must survive\n", encoding="utf-8")
        manifest_path = Path(plan["transaction"]["manifestPath"])
        _, result = self.run_cli(
            "restore",
            "--manifest",
            manifest_path,
            "--apply",
            "--audit-log",
            self.audit_log,
            expect=3,
        )
        self.assertEqual(result["status"], "conflict")
        self.assertEqual(result["conflicts"][0]["code"], "SOURCE_CONFLICT")
        self.assertEqual(target.read_text(encoding="utf-8"), "later user content must survive\n")
        moved = next(action for action in plan["actions"] if action["target"]["path"] == self.meta["orphanFile"])
        self.assertTrue((Path(plan["transaction"]["dir"]) / moved["backupPath"]).is_file())


if __name__ == "__main__":
    unittest.main(verbosity=2)
