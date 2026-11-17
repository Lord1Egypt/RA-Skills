#!/usr/bin/env python3
"""CLI-only acceptance tests for the complete opt-in retention lifecycle."""
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

CLI = Path(__file__).with_name("ag.py")


class RetentionAcceptance(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="retention-acceptance-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.root = self.base / "guild"
        self.root.mkdir()
        self.env = dict(os.environ, AGENT_GUILD_DIR=str(self.root), AG_HOST_ID="acceptance-host",
                        AG_AGENT="alpha", PYTHONDONTWRITEBYTECODE="1")
        (self.root / "UPGRADE.md").write_text("mode = off\n")
        self.call(["init", "alpha"], decode=False)

    def call(self, args, body="", decode=True, expected=0):
        p = subprocess.run([sys.executable, str(CLI), *map(str, args)], input=body, text=True,
                           env=self.env, capture_output=True, timeout=40)
        self.assertEqual(p.returncode, expected, p.stdout + p.stderr)
        return json.loads(p.stdout or p.stderr) if decode else p

    def task(self, action, *options, body="", expected=0):
        return self.call(["task", action, "--session", "acceptance-session", "--agent", "alpha", *options],
                         body, expected=expected)

    def history(self, action, *options, body="", expected=0):
        return self.call(["history", action, *options], body, expected=expected)

    def closed_task(self, name="可恢复任务", attachment=True):
        text = "# Goal\nRetention acceptance\n# Decisions\nKeep stable identifiers\n" + "repeated context\n" * 8000
        x = self.task("create", "--title", name, "--project", "acceptance", body=text)
        tid = x["task"]["task_id"]
        if attachment:
            source = self.base / (tid + ".bin")
            source.write_bytes(b"binary\x00evidence" * 100000)
            x = self.task("attach", "--id", tid, "--expected-revision", x["task"]["revision"], "--file", source)
        x = self.task("close", "--id", tid, "--expected-revision", x["task"]["revision"], "--evidence", "All acceptance assertions passed")
        package = Path(x["package"])
        files = {str(p.relative_to(package)): hashlib.sha256(p.read_bytes()).hexdigest()
                 for p in package.rglob("*") if p.is_file()}
        return x, text, files

    def apply(self, command, plan, irreversible=False):
        opts = ["--plan", "-", "--confirm", plan["token"]]
        if irreversible:
            opts += ["--confirm-data-loss", plan["data_loss_token"]]
        return self.history(command, *opts, body=json.dumps(plan, ensure_ascii=False))

    def finish_batches(self, command, plan, irreversible=False):
        for _ in range(50):
            result = self.apply(command, plan, irreversible)
            self.assertLessEqual(result.get("unlinked_files", result.get("deleted_files", 0)), 10)
            if result.get("state") == "complete":
                return result
            self.assertEqual(result.get("state"), "in_progress", result)
        self.fail("finite approved plan did not complete")

    def test_compact_metadata_only_list_and_full_reopen(self):
        x, text, original = self.closed_task()
        tid = x["task"]["task_id"]
        before = self.history("status")["total_bytes"]
        plan = self.history("compact-plan", "--id", tid)
        self.finish_batches("compact", plan)
        package = Path(x["package"])
        self.assertTrue((package / "pack.json").exists())
        self.assertTrue((package / "payload.zip").exists())
        self.assertLess(self.history("status")["total_bytes"], before)
        listing = self.task("list", "--archive")
        self.assertNotIn("repeated context", json.dumps(listing))
        self.assertEqual(len(listing["items"]), 1)
        x = self.task("reopen", "--id", tid, "--expected-revision", x["task"]["revision"])
        package = Path(x["package"])
        for relative, digest in original.items():
            if relative != "meta.json":
                self.assertEqual(hashlib.sha256((package / relative).read_bytes()).hexdigest(), digest)
        self.assertFalse((package / "pack.json").exists())
        loaded = self.task("resume", "--id", tid)
        self.assertEqual(loaded["context"], text)

    def test_whole_package_retirement_restore_and_last_copy_purge(self):
        x, _, original = self.closed_task()
        tid = x["task"]["task_id"]
        plan = self.history("retire-plan", "--id", tid)
        retired = self.finish_batches("retire", plan)
        self.assertEqual(self.task("list", "--archive")["items"], [])
        ticket = retired["ticket"]
        self.history("restore", "--ticket", ticket)
        package = Path(x["package"])
        self.assertEqual(original, {str(p.relative_to(package)): hashlib.sha256(p.read_bytes()).hexdigest()
                                    for p in package.rglob("*") if p.is_file()})
        plan = self.history("retire-plan", "--id", tid)
        retired = self.finish_batches("retire", plan)
        purge = self.history("purge-plan", "--ticket", retired["ticket"])
        self.history("purge", "--plan", "-", "--confirm", purge["token"],
                     body=json.dumps(purge), expected=1)
        before = self.history("status")["total_bytes"]
        self.finish_batches("purge", purge, True)
        self.assertLess(self.history("status")["total_bytes"], before)
        self.assertFalse(package.exists())
        self.assertEqual(self.task("list", "--archive")["items"], [])

    def test_pinned_and_referenced_packages_cannot_be_retired(self):
        a, _, _ = self.closed_task("受保护任务")
        b = self.task("create", "--title", "Current task", "--project", "acceptance", body="Still working")
        self.task("checkpoint", "--id", b["task"]["task_id"], "--expected-revision", b["task"]["revision"],
                  "--ref", a["task"]["task_id"], body="Dependency is still required")
        self.history("retire-plan", "--id", a["task"]["task_id"], expected=1)
        self.assertTrue(Path(a["package"]).is_dir())

    def test_cycle_remeasures_until_below_target(self):
        self.closed_task("周期任务甲")
        self.closed_task("周期任务乙")
        (self.root / "RETENTION.md").write_text("history_max_bytes=1048576\nhistory_target_bytes=524288\n"
                                                 "history_full_days=0\nhistory_retention_days=180\n"
                                                 "history_max_tasks=1\n")
        plan = self.history("cycle")
        for _ in range(80):
            result = self.apply("cycle", plan, bool(plan.get("data_loss_token")))
            self.assertLessEqual((result.get("batch") or {}).get("unlinked_files", 0), 10)
            if result["state"] == "complete":
                self.assertLessEqual(result["total_bytes"], 524288)
                self.assertLessEqual(len(self.task("list", "--archive")["items"]), 1)
                break
            self.assertEqual(result["state"], "in_progress", result)
        else:
            self.fail("approved cycle did not reach low watermark")


if __name__ == "__main__":
    unittest.main(verbosity=2)
