#!/usr/bin/env python3
"""Real CLI integration of task packages, startup isolation and history budget."""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


CLI = Path(__file__).with_name("ag.py")


class HandoffIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="guild-e2e-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.root = self.base / "guild"
        self.root.mkdir()
        self.env = dict(os.environ, AGENT_GUILD_DIR=str(self.root), AG_HOST_ID="test-host",
                        AG_AGENT="alice", PYTHONDONTWRITEBYTECODE="1")
        (self.root / "UPGRADE.md").write_text("mode = off\n", encoding="utf-8")
        self.call(["init", "alice"])

    def call(self, args, body="", code=0, decode=False):
        result = subprocess.run([sys.executable, str(CLI), *args], env=self.env,
                                input=body, capture_output=True, text=True, timeout=25)
        self.assertEqual(result.returncode, code, result.stdout + result.stderr)
        return json.loads(result.stdout) if decode else result

    def task(self, command, *args, sid="session-a", agent="alice", body="", code=0):
        return self.call(["task", command, "--session", sid, "--agent", agent, *args],
                         body=body, code=code, decode=True)

    def create(self, title="Independent task", body="CURRENT_CONTEXT_SENTINEL", **kwargs):
        return self.task("create", "--title", title, "--project", "demo",
                         "--summary", "Run verification", body=body, **kwargs)

    def test_real_cross_agent_lifecycle_and_history_integrity(self):
        created = self.create(title="交接机制改进")
        tid = created["task"]["task_id"]
        rev = created["task"]["revision"]
        package = Path(created["package"])
        self.assertIn("交接机制改进", package.name)
        listing = self.task("list", sid="session-b", agent="bob")
        self.assertNotIn("CURRENT_CONTEXT_SENTINEL", json.dumps(listing))
        self.task("resume", "--list", listing["list_id"], "--number", "1",
                  sid="session-b", agent="bob", code=1)
        resumed = self.task("resume", "--id", tid, "--handover", sid="session-b", agent="bob")
        self.assertIn("CURRENT_CONTEXT_SENTINEL", json.dumps(resumed))
        self.task("checkpoint", "--id", tid, "--expected-revision", str(rev),
                  body="stale writer", code=1)
        rev = resumed["task"]["revision"]
        changed = self.task("checkpoint", "--id", tid, "--expected-revision", str(rev),
                            "--status", "waiting", "--pin", sid="session-b", agent="bob",
                            body="Verified complete context, awaiting acceptance")
        self.assertTrue(changed["task"]["pin"])
        marker = self.base / "script-ran"
        script = self.base / "example.py"
        script.write_text("from pathlib import Path\nPath(" + repr(str(marker)) + ").touch()\n")
        attached = self.task("attach", "--id", tid, "--expected-revision", str(changed["task"]["revision"]),
                             "--file", str(script), sid="session-b", agent="bob")
        self.assertFalse(marker.exists())
        closed = self.task("close", "--id", tid, "--expected-revision", str(attached["task"]["revision"]),
                           "--evidence", "Accepted integration fixture", sid="session-b", agent="bob")
        self.assertEqual(closed["task"]["status"], "closed")
        self.assertEqual(Path(closed["package"]).name, package.name)
        self.assertEqual(Path(closed["package"]).parent, self.root / "handoff/archive")
        self.assertEqual(self.task("list")["items"], [])
        history = self.call(["history", "status"], decode=True)
        self.assertTrue(history["complete"], history)
        self.assertGreater(history["total_bytes"], 0)
        plan = self.call(["history", "plan"], decode=True)
        self.assertNotIn("CURRENT_CONTEXT_SENTINEL", json.dumps(plan))
        reopened = self.task("reopen", "--id", tid, "--expected-revision", str(closed["task"]["revision"]),
                             sid="session-b", agent="bob")
        self.assertEqual(reopened["task"]["status"], "active")
        loaded = self.task("resume", "--id", tid, sid="session-b", agent="bob")
        self.assertIn("awaiting acceptance", json.dumps(loaded))
        self.assertFalse(marker.exists())

    def test_startup_never_loads_other_conversation_or_global_focus(self):
        self.create(body="UNRELATED_A_SECRET_CONTEXT")
        for relative in ("projects/active.md", "handoff/shared-state/current-focus.md",
                         "hosts/test-host/host-notes.md"):
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("UNRELATED_A_SECRET_CONTEXT", encoding="utf-8")
        self.call(["send", "bob", "UNRELATED_A_SECRET_CONTEXT"], body="another task")
        output = self.call(["bootstrap", "bob", "--no-maintenance"])
        self.assertNotIn("UNRELATED_A_SECRET_CONTEXT", output.stdout + output.stderr)
        self.assertNotIn("Independent task", output.stdout)
        self.assertIn("Task context: not loaded", output.stdout)

    def test_stale_list_cannot_select_a_changed_task(self):
        task = self.create()["task"]
        listing = self.task("list", sid="session-b", agent="bob")
        self.task("checkpoint", "--id", task["task_id"], "--expected-revision", str(task["revision"]),
                  body="new revision")
        stale = self.task("resume", "--list", listing["list_id"], "--number", "1",
                          "--handover", sid="session-b", agent="bob", code=1)
        self.assertEqual(stale["error"], "stale_list")
        self.assertNotIn("new revision", json.dumps(stale))

    def test_one_gib_budget_blocks_new_history_without_deleting(self):
        path = self.root / "log/archive/large.bin"
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("wb") as stream:
            stream.truncate(1024 * 1024 * 1024)
        before = path.stat().st_size
        result = self.call(["finish", "alice"], body="must be rejected", code=1)
        self.assertTrue(result.stderr)
        self.assertEqual(path.stat().st_size, before)
        self.assertFalse(any((self.root / "log/daily").glob("*.md")))
        report = self.call(["history", "status"], decode=True)
        self.assertGreaterEqual(report["total_bytes"], 1024 * 1024 * 1024)

    def test_inbox_archive_cannot_bypass_historical_budget(self):
        self.call(["send", "alpha", "large"], body="unread" * 20000)
        (self.root / "RETENTION.md").write_text("history_max_bytes=65536\nhistory_target_bytes=32768\n")
        self.call(["finish", "alpha", "--archive-inbox"], body="short summary", code=1)
        inbox = self.root / "messages/inbox"
        archive = self.root / "messages/archive"
        self.assertEqual(len(list(inbox.glob("*.md"))), 1)
        self.assertEqual(len(list(archive.glob("*.md"))), 0)
        self.assertLessEqual(self.call(["history", "status"], decode=True)["total_bytes"], 65536)

    def test_legacy_migration_is_preview_only(self):
        old = self.root / "handoff/inbox/from-alice-to-bob-note.md"
        old.parent.mkdir(parents=True, exist_ok=True)
        old.write_text("legacy note")
        result = self.call(["migrate", "--dry-run"], decode=True)
        self.assertFalse(result["mutated"])
        self.assertTrue(old.exists())
        self.assertFalse((self.root / "messages/inbox" / old.name).exists())
        self.assertEqual(self.task("list")["items"], [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
