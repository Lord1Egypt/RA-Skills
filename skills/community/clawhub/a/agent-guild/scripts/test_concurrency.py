#!/usr/bin/env python3
"""Offline regressions for shared-state writers and their archive operations.

Run: python3 scripts/test_concurrency.py
All workers use an isolated guild. A start gate and delayed reads make lost
updates observable without depending on a particular process start order.
"""
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parent
WORKER = r'''
import json, os, sys, time
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import ag
action = json.loads(sys.argv[2])
gate = Path(sys.argv[3])
ready = Path(sys.argv[4])

# Delay after a read to expose stale read-modify-write snapshots. Correct
# writers hold their lock across both the read and this delay.
read_text = Path.read_text
def slow_read(path, *args, **kwargs):
    text = read_text(path, *args, **kwargs)
    if path in (ag.REGISTRY, ag.FOCUS, ag.AUDIT) or path.parent == ag.LEARNINGS:
        time.sleep(0.025)
    return text
Path.read_text = slow_read
ready.touch()
while not gate.exists():
    time.sleep(0.005)

if action[0] == "audit":
    for n in range(12):
        ag.audit("test", {"id": action[1] + "-" + str(n)})
        time.sleep(0.002)
elif action[0] == "groom":
    for _ in range(8):
        ag._groom(dict(ag.RETENTION_DEFAULTS, audit_max_lines=4, audit_keep_lines=2))
        time.sleep(0.005)
else:
    command = action[0].replace("-", "_")
    sys.exit(getattr(ag, "cmd_" + command)(action[1:]))
'''


class SharedStateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="ag-concurrency-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.guild = self.root / "guild"
        self.guild.mkdir()
        self.env = dict(os.environ, AGENT_GUILD_DIR=str(self.guild),
                        AG_HOST_ID="test-host", AG_AGENT="test-agent")

    def path(self, name):
        p = self.guild / name
        p.parent.mkdir(parents=True, exist_ok=True)
        return p

    def command(self, args, body="details"):
        result = subprocess.run([sys.executable, str(SCRIPTS / "ag.py"), *args],
                                env=self.env, input=body, text=True,
                                capture_output=True, timeout=20)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return result.stdout

    def parallel(self, actions):
        gate = self.root / "start"
        gate.unlink(missing_ok=True)
        workers = []
        try:
            for i, action in enumerate(actions):
                ready = self.root / ("ready-" + str(i))
                ready.unlink(missing_ok=True)
                proc = subprocess.Popen(
                    [sys.executable, "-c", WORKER, str(SCRIPTS),
                     json.dumps(action), str(gate), str(ready)],
                    env=self.env, stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                proc.stdin.write("worker details")
                proc.stdin.close()
                proc.stdin = None
                workers.append((proc, ready))
            deadline = time.monotonic() + 20
            while not all(ready.exists() for _, ready in workers):
                self.assertLess(time.monotonic(), deadline, "workers failed to start")
                time.sleep(0.01)
            gate.touch()
            for proc, _ in workers:
                out, err = proc.communicate(timeout=30)
                self.assertEqual(proc.returncode, 0, out + err)
        finally:
            for proc, _ in workers:
                if proc.poll() is None:
                    proc.kill()
                proc.communicate()

    def entries(self):
        body = self.path("learnings/LEARNINGS.md").read_text(encoding="utf-8")
        return body, re.findall(r"^## \[([^\]]+)\]", body, re.M)

    def test_registry_preserves_concurrent_agents_and_presence(self):
        # BOM is emitted by legacy Windows PowerShell installations.
        registry = self.path("registry.json")
        registry.write_text(json.dumps({"agents": {"existing": {"home": "/old"}}}),
                            encoding="utf-8-sig")
        self.parallel([["register", f"agent-{i}", "/tmp/home", "readonly"]
                       for i in range(12)] + [["last-seen", "existing"]])
        agents = json.loads(registry.read_text(encoding="utf-8"))["agents"]
        self.assertEqual(set(agents), {"existing"} | {f"agent-{i}" for i in range(12)})
        self.assertTrue(agents["existing"]["hosts"]["test-host"]["last_seen"])

    def test_learning_ids_unique_and_resolutions_preserve_new_entries(self):
        self.parallel([["learn", "alice", "learning", f"entry-{i}",
                        "--pattern-key", "same-pattern"] for i in range(12)])
        body, ids = self.entries()
        self.assertEqual(len(ids), 12)
        self.assertEqual(len(set(ids)), 12)
        self.assertEqual(body.count("- See Also:"), 11)
        self.parallel([["resolve", entry_id, "fixed"] for entry_id in ids]
                      + [["learn", "alice", "learning", f"new-{i}"] for i in range(4)])
        body, ids = self.entries()
        self.assertEqual(len(ids), 16)
        self.assertEqual(len(set(ids)), 16)
        self.assertEqual(body.count("**Status**: resolved"), 12)
        self.assertEqual(body.count("**Status**: pending"), 4)

    def test_global_focus_is_retired_without_changing_legacy_data(self):
        focus = self.path("handoff/shared-state/current-focus.md")
        focus.write_text("# Current Focus\n\nlegacy details\n", encoding="utf-8")
        before = focus.read_bytes()
        result = subprocess.run([sys.executable, str(SCRIPTS / "ag.py"),
                                 "focus", "alice", "new"], env=self.env,
                                input="must not write", text=True,
                                capture_output=True, timeout=20)
        self.assertEqual(result.returncode, 2)
        self.assertIn("retired", result.stderr)
        self.assertEqual(focus.read_bytes(), before)

    def test_ledger_compaction_preserves_concurrent_learning_entries(self):
        self.path("learnings/LEARNINGS.md").write_text(
            "# Learnings\n\n## [LRN-20000101-001] insight\n\n"
            "**Logged**: 2000-01-01T00:00:00+00:00\n**Status**: resolved\n\n"
            "### Summary\nold learning\n\n---\n", encoding="utf-8")
        self.parallel([["learn", "alice", "learning", f"entry-{i}"] for i in range(12)]
                      + [["groom"], ["groom"]])
        body, ids = self.entries()
        self.assertEqual(len(ids), 12)
        self.assertEqual(len(set(ids)), 12)
        self.assertNotIn("LRN-20000101-001", ids)
        archive = self.path("learnings/archive/LEARNINGS.md").read_text(encoding="utf-8")
        self.assertEqual(archive.count("## [LRN-20000101-001]"), 1)
        for i in range(12):
            self.assertEqual(body.count(f"### Summary\nentry-{i}\n"), 1)

    def test_audit_rotations_preserve_all_records(self):
        self.path("log/audit.jsonl").write_text("", encoding="utf-8")
        self.parallel([["audit", f"writer-{i}"] for i in range(4)]
                      + [["groom"], ["groom"]])
        records = []
        for p in (self.guild / "log").rglob("*.jsonl"):
            records.extend(json.loads(line) for line in p.read_text(encoding="utf-8").splitlines()
                           if line.strip())
        ids = [record["id"] for record in records if record["action"] == "test"]
        self.assertEqual(len(ids), 48)
        self.assertEqual(len(set(ids)), 48)

    def test_groom_ignores_lock_sidecars_and_dry_run_is_readonly(self):
        sidecars = [self.path("messages/inbox/.from-alice-to-bob-note.md.ag-lock"),
                    self.path("messages/archive/.from-alice-to-bob-note.md.ag-lock")]
        for p in sidecars:
            p.touch()
            os.utime(p, (1, 1))
        before = sorted(str(p.relative_to(self.guild)) for p in self.guild.rglob("*"))
        output = self.command(["groom", "--dry-run"])
        after = sorted(str(p.relative_to(self.guild)) for p in self.guild.rglob("*"))
        self.assertEqual(before, after)
        self.assertNotIn("unread inbox", output)
        self.assertNotIn("archived message", output)
        self.command(["groom"])
        self.assertTrue(all(p.exists() for p in sidecars))


if __name__ == "__main__":
    unittest.main(verbosity=2)
