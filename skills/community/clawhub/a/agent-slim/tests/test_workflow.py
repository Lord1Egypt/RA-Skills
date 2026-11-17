#!/usr/bin/env python3
"""End-to-end tests for Agent Slim plan/apply/verify/restore (stdlib only)."""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
FIXTURE = ROOT / "tests" / "fixtures" / "aging-agent"
CLI = SCRIPTS / "agent_slim.py"
SCHEMAS = ROOT / "schemas"
sys.path.insert(0, str(SCRIPTS))

import agent_slim_workflow as workflow  # noqa: E402


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def file_state(root: Path):
    result = {}
    for path in sorted(root.rglob("*")):
        if path.is_file():
            stat = path.stat()
            result[path.relative_to(root).as_posix()] = (
                sha256_file(path),
                stat.st_size,
                stat.st_mode,
                stat.st_mtime_ns,
            )
    return result


def json_type(value, expected):
    if isinstance(expected, list):
        return any(json_type(value, item) for item in expected)
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "null":
        return value is None
    return True


def validate_json_schema(value, schema, path="$"):
    """Validate the small JSON-Schema subset used by this project's schemas."""
    errors = []
    if "type" in schema and not json_type(value, schema["type"]):
        return ["{}: expected type {}".format(path, schema["type"])]
    if "const" in schema and value != schema["const"]:
        errors.append("{}: expected const {!r}".format(path, schema["const"]))
    if "enum" in schema and value not in schema["enum"]:
        errors.append("{}: value not in enum".format(path))
    if isinstance(value, str):
        if "minLength" in schema and len(value) < schema["minLength"]:
            errors.append("{}: shorter than minLength".format(path))
        if "pattern" in schema and not re.search(schema["pattern"], value):
            errors.append("{}: does not match pattern".format(path))
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            errors.append("{}: below minimum".format(path))
    if isinstance(value, dict):
        for key in schema.get("required", []):
            if key not in value:
                errors.append("{}: missing {}".format(path, key))
        properties = schema.get("properties", {})
        for key, child in properties.items():
            if key in value:
                errors.extend(validate_json_schema(value[key], child, "{}.{}".format(path, key)))
    if isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            errors.append("{}: fewer than minItems".format(path))
        if "items" in schema:
            for index, item in enumerate(value):
                errors.extend(validate_json_schema(item, schema["items"], "{}[{}]".format(path, index)))
    return errors


def load_schema(name: str):
    return json.loads((SCHEMAS / name).read_text(encoding="utf-8"))


class WorkflowFixture(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="agent-slim-workflow-")
        self.base = Path(self.temp.name)
        self.home = self.base / "home"
        self.state_root = self.base / "transactions"
        self.audit_log = self.base / "audit.log"
        self.audit_path = self.base / "audit.json"
        self.plan_path = self.base / "plan.json"
        shutil.copytree(FIXTURE, self.home)
        shutil.copy2(self.home / "backups/snapshot.zip", self.home / "backups/snapshot-copy.zip")
        old = (workflow.datetime.now(workflow.timezone.utc) - timedelta(days=120)).timestamp()
        os.utime(self.home / "sessions/2024/01/rollout-old.jsonl", (old, old))
        self.low_frequency = "skills/gamma/references/unreferenced.md"
        self.old_session = "sessions/2024/01/rollout-old.jsonl"

    def tearDown(self):
        self.temp.cleanup()

    def run_cli(self, *args, expect=0):
        result = subprocess.run([sys.executable, str(CLI), *map(str, args)], capture_output=True, text=True)
        if expect is not None and result.returncode != expect:
            self.fail("CLI returned {} expected {}:\nstdout={}\nstderr={}".format(result.returncode, expect, result.stdout, result.stderr))
        parsed = json.loads(result.stdout) if result.stdout.strip() else None
        return result, parsed

    def audit(self):
        self.run_cli("audit", "--home", self.home, "--json", "--output", self.audit_path)
        report = json.loads(self.audit_path.read_text(encoding="utf-8"))
        self.assertEqual(report["schemaVersion"], "1.0")
        return report

    def plan(self, confirm_all=True):
        args = ["plan", "--audit", self.audit_path, "--state-root", self.state_root, "--output", self.plan_path]
        if confirm_all:
            args.extend(["--confirm", self.low_frequency, "--confirm", self.old_session])
        self.run_cli(*args)
        plan = json.loads(self.plan_path.read_text(encoding="utf-8"))
        schemas_errors = validate_json_schema(plan, load_schema("plan.schema.json"))
        self.assertEqual(schemas_errors, [])
        return plan

    def prompts_file(self):
        prompt_path = self.base / "test-prompts.json"
        command = [
            sys.executable,
            "-c",
            "import os; p=os.environ.get('AGENT_SLIM_PROMPT',''); print('agent-slim' if '瘦身' in p else 'none')",
        ]
        data = {
            "test_cases": [
                {"id": "trigger-positive", "prompt": "给这个 Agent 整体瘦身", "command": command, "expect": {"exitCode": 0, "stdoutContains": "agent-slim"}},
                {"id": "trigger-negative", "prompt": "只读一个普通文件", "command": command, "expect": {"exitCode": 0, "stdoutContains": "none"}},
            ]
        }
        prompt_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return prompt_path

    def test_plan_dry_run_apply_verify_restore_roundtrip(self):
        baseline = file_state(self.home)
        self.audit()
        self.assertEqual(file_state(self.home), baseline)
        plan = self.plan(confirm_all=True)
        self.assertEqual(file_state(self.home), baseline)
        ready = [action for action in plan["actions"] if action["status"] == "ready"]
        self.assertEqual(
            {action["action"] for action in ready},
            {"quarantine-redundant-backup", "archive-verified-old-session", "quarantine-low-frequency-file"},
        )

        dry_result, dry = self.run_cli("apply", "--plan", self.plan_path, "--audit-log", self.audit_log)
        self.assertEqual(dry["status"], "dry-run")
        self.assertEqual(len(dry["planned"]), 3)
        self.assertEqual(file_state(self.home), baseline)
        self.assertFalse(self.state_root.exists())
        self.assertFalse(self.audit_log.exists())

        apply_result, applied = self.run_cli(
            "apply", "--plan", self.plan_path, "--apply", "--audit-log", self.audit_log
        )
        self.assertEqual(applied["status"], "applied")
        self.assertEqual(len(applied["applied"]), 3)
        backup_action = next(action for action in plan["actions"] if action["action"] == "quarantine-redundant-backup" and action["status"] == "ready")
        moved_backup = backup_action["target"]["path"]
        for relative in (self.low_frequency, self.old_session, moved_backup):
            self.assertFalse((self.home / relative).exists(), relative)

        manifest_path = Path(plan["transaction"]["manifestPath"])
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest_errors = validate_json_schema(manifest, load_schema("transaction-manifest.schema.json"))
        self.assertEqual(manifest_errors, [])
        expected_manifest_hash = (manifest_path.parent / "manifest.sha256").read_text(encoding="utf-8").strip()
        self.assertEqual(sha256_file(manifest_path), expected_manifest_hash)
        restore_script = Path(plan["transaction"]["restoreScriptPath"])
        restore_shell = Path(plan["transaction"]["restoreShellPath"])
        self.assertTrue(restore_script.is_file())
        self.assertTrue(restore_shell.is_file())
        shell_check = subprocess.run(["sh", "-n", str(restore_shell)], capture_output=True, text=True)
        self.assertEqual(shell_check.returncode, 0, shell_check.stderr)

        prompts = self.prompts_file()
        _, verified = self.run_cli("verify", "--plan", self.plan_path, "--phase", "applied", "--test-prompts", prompts)
        verification_errors = validate_json_schema(verified, load_schema("verification.schema.json"))
        self.assertEqual(verification_errors, [])
        self.assertEqual(verified["summary"]["status"], "PASS", verified)

        generated_dry = subprocess.run([sys.executable, str(restore_script)], capture_output=True, text=True)
        self.assertEqual(generated_dry.returncode, 0, generated_dry.stderr)
        self.assertEqual(json.loads(generated_dry.stdout)["status"], "dry-run")
        self.assertFalse((self.home / self.low_frequency).exists())

        result_path = Path(plan["transaction"]["resultPath"])
        result_before_restore_dry = result_path.read_bytes()
        _, restore_dry = self.run_cli(
            "restore", "--manifest", manifest_path, "--audit-log", self.audit_log
        )
        self.assertEqual(restore_dry["status"], "dry-run")
        self.assertEqual(result_path.read_bytes(), result_before_restore_dry)

        _, restored = self.run_cli(
            "restore", "--manifest", manifest_path, "--apply", "--audit-log", self.audit_log
        )
        self.assertEqual(restored["status"], "restored")
        self.assertTrue(restored["hashMatches"])
        self.assertEqual(file_state(self.home), baseline)

        _, verified_after_restore = self.run_cli(
            "verify", "--plan", self.plan_path, "--phase", "restored", "--test-prompts", prompts
        )
        self.assertEqual(verified_after_restore["summary"]["status"], "PASS", verified_after_restore)

        _, restored_again = self.run_cli(
            "restore", "--manifest", manifest_path, "--apply", "--audit-log", self.audit_log
        )
        self.assertEqual(restored_again["status"], "already-restored")
        self.assertEqual(file_state(self.home), baseline)

        audit_lines = [json.loads(line) for line in self.audit_log.read_text(encoding="utf-8").splitlines()]
        events = {line["event"] for line in audit_lines}
        self.assertTrue({"transaction-begin", "apply-move", "transaction-applied", "restore-begin", "restore-move", "restore-complete"}.issubset(events))
        for line in audit_lines:
            serialized = json.dumps(line, ensure_ascii=False)
            self.assertNotIn("synthetic OLD_SESSION_BODY", serialized)
            self.assertNotIn("API_KEY", serialized)

    def test_plan_without_confirmation_keeps_unproven_actions_pending(self):
        baseline = file_state(self.home)
        self.audit()
        plan = self.plan(confirm_all=False)
        self.assertEqual(file_state(self.home), baseline)
        actions = {action["target"]["path"]: action for action in plan["actions"]}
        self.assertEqual(actions[self.low_frequency]["status"], "pending-confirmation")
        self.assertFalse(actions[self.low_frequency]["executable"])
        self.assertEqual(actions[self.old_session]["status"], "pending-confirmation")
        self.assertFalse(actions[self.old_session]["executable"])
        duplicate = [a for a in plan["actions"] if a["action"] == "quarantine-redundant-backup" and a["status"] == "ready"]
        self.assertEqual(len(duplicate), 1)
        self.assertTrue(duplicate[0]["target"]["path"].startswith("backups/"))

    def test_apply_stops_on_stale_target_and_existing_transaction(self):
        self.audit()
        plan = self.plan(confirm_all=True)
        target = self.home / self.low_frequency
        target.write_text("user changed this file after planning\n", encoding="utf-8")
        _, blocked = self.run_cli(
            "apply", "--plan", self.plan_path, "--apply", "--audit-log", self.audit_log, expect=3
        )
        self.assertEqual(blocked["status"], "blocked")
        self.assertEqual(blocked["failed"][0]["code"], "PLAN_STALE")
        self.assertFalse(Path(plan["transaction"]["dir"]).exists())

        # Re-plan and show that an existing transaction directory blocks all mutation.
        shutil.copy2(FIXTURE / self.low_frequency, target)
        self.audit()
        plan = self.plan(confirm_all=True)
        Path(plan["transaction"]["dir"]).mkdir(parents=True)
        _, conflict = self.run_cli(
            "apply", "--plan", self.plan_path, "--apply", "--audit-log", self.audit_log, expect=3
        )
        self.assertEqual(conflict["status"], "blocked")
        self.assertEqual(conflict["failed"][0]["code"], "TRANSACTION_EXISTS")
        self.assertTrue(target.is_file())

    def test_invalid_action_and_restore_conflict_fail_nonzero(self):
        self.audit()
        plan = self.plan(confirm_all=True)
        plan["actions"][0]["action"] = "delete-original"
        plan["actions"][0]["executable"] = True
        plan["actions"][0]["status"] = "ready"
        bad_plan = self.base / "bad-plan.json"
        bad_plan.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
        _, invalid = self.run_cli(
            "apply", "--plan", bad_plan, "--apply", "--audit-log", self.audit_log, expect=64
        )
        self.assertEqual(invalid["code"], "ACTION_NOT_ALLOWED")

        self.audit()
        valid_plan = self.plan(confirm_all=True)
        _, applied = self.run_cli(
            "apply", "--plan", self.plan_path, "--apply", "--audit-log", self.audit_log
        )
        self.assertEqual(applied["status"], "applied")
        target = self.home / self.low_frequency
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("later user content must survive\n", encoding="utf-8")
        _, conflict = self.run_cli(
            "restore",
            "--manifest",
            valid_plan["transaction"]["manifestPath"],
            "--apply",
            "--audit-log",
            self.audit_log,
            expect=3,
        )
        self.assertEqual(conflict["status"], "conflict")
        self.assertEqual(conflict["conflicts"][0]["code"], "SOURCE_CONFLICT")
        self.assertEqual(target.read_text(encoding="utf-8"), "later user content must survive\n")
        self.assertTrue((Path(valid_plan["transaction"]["dir"]) / valid_plan["actions"][0]["backupPath"]).exists())

    def test_verify_without_prompts_is_partial_not_pass(self):
        self.audit()
        self.plan(confirm_all=True)
        self.run_cli("apply", "--plan", self.plan_path, "--apply", "--audit-log", self.audit_log)
        _, report = self.run_cli("verify", "--plan", self.plan_path, "--phase", "applied", expect=2)
        self.assertEqual(report["summary"]["status"], "PARTIAL")
        prompt_check = next(check for check in report["checks"] if check["id"] == "trigger-routing-regression")
        self.assertEqual(prompt_check["status"], "SKIPPED")


if __name__ == "__main__":
    unittest.main(verbosity=2)
