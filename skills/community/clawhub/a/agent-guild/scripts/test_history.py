#!/usr/bin/env python3
"""历史模块隔离回归：所有数据仅位于临时 guild，禁止访问真实用户目录。"""
import contextlib
import io
import json
import os
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest import mock

import ag_history as history


class FakeAPI:
    def __init__(self, root):
        self.CENTRAL = root
        self.now = datetime(2026, 1, 1, tzinfo=timezone.utc)
        self.locks = []

    def now_iso(self):
        return self.now.isoformat()

    @contextlib.contextmanager
    def _append_lock(self, path):
        if path in self.locks:
            raise AssertionError("同一把锁不能重入")
        self.locks.append(path)
        try:
            yield
        finally:
            self.locks.pop()

    def _atomic_write_text(self, path, text):
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_name(".test-atomic-" + path.name)
        temporary.write_text(text, encoding="utf-8")
        os.replace(temporary, path)


class HistoryTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="ag-history-isolated-")
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.guild = self.base / "guild"
        self.guild.mkdir()
        self.api = FakeAPI(self.guild)
        self.old = self.api.now - timedelta(days=240)

    def file(self, rel, body="content", old=True):
        path = self.guild / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(body, bytes):
            path.write_bytes(body)
        else:
            path.write_text(body, encoding="utf-8")
        if old:
            os.utime(path, (self.old.timestamp(), self.old.timestamp()))
        return path

    def config(self, **values):
        self.file("RETENTION.md", "\n".join("%s = %s # test" % pair for pair in values.items()))

    def task(self, name="20250101-123456789abc-历史任务", active=False, **overrides):
        area = "active" if active else "archive"
        rel = "handoff/%s/%s" % (area, name)
        meta = {"id": name, "revision": 2, "status": "active" if active else "closed",
                "refs": [], "hold": False, "closed_at": None if active else self.old.isoformat()}
        meta.update(overrides)
        self.file(rel + "/meta.json", json.dumps(meta, ensure_ascii=False))
        self.file(rel + "/context.md", "摘要必须保留")
        self.file(rel + "/sessions/000001/context.md", "旧检查点详情")
        self.file(rel + "/artifacts/output.bin", b"artifact")
        return rel, meta

    def run_cli(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = history.run(list(args), self.api)
        return code, out.getvalue(), err.getvalue()

    def plan(self, save=False):
        args = ["plan"] + (["--output", history.PLAN_PATH] if save else [])
        code, out, err = self.run_cli(*args)
        self.assertEqual(code, 0, err)
        return json.loads(out)

    def test_default_budget_and_missing_policy(self):
        status = history.report(self.api)
        self.assertEqual(status["total_bytes"], 0)
        self.assertEqual(status["max_bytes"], 1024 ** 3)
        self.assertEqual(status["target_bytes"], 800 * 1024 ** 2)
        self.assertTrue(status["complete"])
        self.assertEqual(status["config"]["history_full_days"], 30)
        self.assertEqual(status["config"]["history_retention_days"], 180)
        history.ensure_capacity(self.api, 1024 ** 3)
        self.assertEqual(list(self.guild.iterdir()), [])

    def test_default_budget_can_be_explicitly_raised(self):
        self.file("RETENTION.md", "history_max_bytes=2147483648\n")
        self.assertEqual(history.report(self.api)["max_bytes"], 2 * 1024 ** 3)
        history.ensure_capacity(self.api, 1024 ** 3 + 1)

    def test_policy_comments_unknown_legacy_keys_and_strict_validation(self):
        self.file("RETENTION.md", "# retention\n```\ndaily_log_days=90\nhistory_max_tasks = 12 # comment\n```\n")
        self.assertEqual(history.report(self.api)["max_tasks"], 12)
        invalid = ["history_max_tasks=-1", "history_max_tasks=1.5", "history_max_tasks=no",
                   "history_max_tasks=", "history_max_tasks=1\nhistory_max_tasks=2",
                   "history_unknown=9", "history_full_days=181", "history_check_interval_hours=0",
                   "history_max_bytes=0",
                   "history_max_bytes=10\nhistory_target_bytes=11"]
        for value in invalid:
            with self.subTest(value=value):
                self.file("RETENTION.md", value)
                with self.assertRaises(ValueError):
                    history.ensure_capacity(self.api)

    def test_all_history_categories_are_counted_once(self):
        tracked = ["messages/archive/message.md", "log/daily/day.md", "log/archive/history.md",
                   "log/audit.jsonl", "learnings/archive/resolved.md", "handoff/archive/legacy.md",
                   "handoff/shared-state/archive/focus.md", ".trash/item", "backups/data",
                   "history/old-report.json", "history/recovery/old.zip",
                   "hosts/test-host/task-sessions/session.json", "handoff/.task-new-orphan/context.md"]
        for path in tracked:
            self.file(path, b"12345")
        ignored = ["messages/inbox/unread.md", "handoff/inbox/unread.md", "identity/person.md",
                   "rules/keep.md", "memory/shared/fact.md", "skills/tool.txt", "tools/command"]
        for path in ignored:
            self.file(path, b"not history")
        status = history.report(self.api)
        self.assertEqual(status["total_bytes"], len(tracked) * 5)
        self.assertEqual(status["file_count"], len(tracked))
        self.assertEqual(status["categories"]["logs"]["bytes"], 15)

    def test_archived_package_and_only_active_checkpoints_count(self):
        archived, _ = self.task()
        active, _ = self.task("20250102-abcdef123456-活跃任务", active=True)
        expected = sum(p.stat().st_size for p in (self.guild / archived).rglob("*") if p.is_file())
        expected += (self.guild / active / "sessions/000001/context.md").stat().st_size
        status = history.report(self.api)
        self.assertEqual(status["total_bytes"], expected)
        self.assertEqual(status["archived_tasks"], 1)
        self.assertEqual(status["categories"]["active_checkpoints"]["files"], 1)
        self.assertFalse(any(item["path"].startswith(active) for item in self.plan()["files"]))

    def test_hardlinks_are_deduplicated_and_never_retired(self):
        first = self.file("log/archive/a", b"1234567")
        second = self.guild / "log/archive/b"
        os.link(first, second)
        status = history.report(self.api)
        self.assertEqual(status["total_bytes"], 7)
        self.assertEqual(status["hardlink_duplicates"], 1)
        self.assertEqual(status["hardlink_duplicate_bytes"], 7)
        self.assertEqual(self.plan()["files"], [])

    def test_sparse_gib_is_counted_logically_and_blocks_append(self):
        path = self.file("log/archive/sparse.bin", b"")
        with path.open("r+b") as stream:
            stream.truncate(1024 ** 3 + 1)
        status = history.report(self.api)
        self.assertEqual(status["total_bytes"], 1024 ** 3 + 1)
        self.assertTrue(status["over_budget"])
        with self.assertRaisesRegex(RuntimeError, "预算不足"):
            history.ensure_capacity(self.api)

    def test_low_budget_and_invalid_growth(self):
        self.config(history_max_bytes=100, history_target_bytes=80)
        self.file("log/archive/data", b"x" * 90)
        history.ensure_capacity(self.api, 10)
        with self.assertRaises(RuntimeError):
            history.ensure_capacity(self.api, 11)
        for value in (-1, 1.1, "1", True):
            with self.subTest(value=value), self.assertRaises(ValueError):
                history.ensure_capacity(self.api, value)

    def test_symlink_file_directory_and_dangling_link_fail_closed(self):
        outside = self.base / "outside"
        outside.mkdir()
        (outside / "secret").write_text("must not read", encoding="utf-8")
        for name, target in (("link-file", outside / "secret"), ("link-dir", outside),
                             ("link-dangling", outside / "missing")):
            link = self.guild / "log" / name
            link.parent.mkdir(exist_ok=True)
            link.symlink_to(target)
        status = history.report(self.api)
        self.assertFalse(status["complete"])
        self.assertEqual(status["total_bytes"], 0)
        self.assertEqual(status["error_count"], 3)
        with self.assertRaises(RuntimeError):
            history.ensure_capacity(self.api)
        self.assertEqual((outside / "secret").read_text(encoding="utf-8"), "must not read")

    def test_symlink_config_root_and_history_parent_rejected(self):
        outside = self.base / "outside"
        outside.mkdir()
        (outside / "policy").write_text("history_max_bytes=999999999999", encoding="utf-8")
        (self.guild / "RETENTION.md").symlink_to(outside / "policy")
        with self.assertRaises(RuntimeError):
            history.report(self.api)
        (self.guild / "RETENTION.md").unlink()
        (self.guild / "history").symlink_to(outside, target_is_directory=True)
        self.assertFalse(history.report(self.api)["complete"])
        code, _, _ = self.run_cli("plan", "--output", history.PLAN_PATH)
        self.assertEqual(code, 1)
        other = self.base / "guild-link"
        other.symlink_to(self.guild, target_is_directory=True)
        with self.assertRaises(RuntimeError):
            history.report(FakeAPI(other))

    def test_permissions_or_scan_limits_fail_closed(self):
        self.file("log/archive/data")
        original = os.scandir
        def denied(path):
            if Path(path).resolve() == (self.guild / "log").resolve():
                raise PermissionError("denied")
            return original(path)
        with mock.patch.object(os, "scandir", side_effect=denied):
            self.assertFalse(history.report(self.api)["complete"])
            with self.assertRaises(RuntimeError):
                history.ensure_capacity(self.api)
        with mock.patch.object(history, "MAX_ENTRIES", 1):
            self.assertFalse(history.report(self.api)["complete"])

    @unittest.skipUnless(hasattr(os, "mkfifo"), "平台无命名管道")
    def test_special_file_is_never_opened(self):
        directory = self.guild / "log"
        directory.mkdir()
        os.mkfifo(directory / "pipe")
        self.assertFalse(history.report(self.api)["complete"])
        with self.assertRaises(RuntimeError):
            history.ensure_capacity(self.api)

    def test_status_and_maintenance_never_read_payload_bodies(self):
        self.file("log/archive/private.md", "sensitive body")
        self.task()
        original = history._open_file
        @contextlib.contextmanager
        def guarded(root, rel, expected=None):
            self.assertTrue(rel.endswith("meta.json") or rel in ("RETENTION.md", history.STATE_PATH), rel)
            with original(root, rel, expected) as stream:
                yield stream
        with mock.patch.object(history, "_open_file", side_effect=guarded):
            self.assertTrue(history.report(self.api)["complete"])
            result = history.maintenance(self.api)
        self.assertFalse(result["applied"])
        self.assertTrue((self.guild / "log/archive/private.md").exists())

    def test_closed_at_not_mtime_controls_task_retention(self):
        recent = (self.api.now - timedelta(days=5)).isoformat()
        rel, meta = self.task(closed_at=recent)
        self.assertFalse(any(item["task_id"] == meta["id"] for item in self.plan()["files"]))
        meta["closed_at"] = self.old.isoformat()
        self.file(rel + "/meta.json", json.dumps(meta))
        for path in (self.guild / rel).rglob("*"):
            if path.is_file():
                os.utime(path, (self.api.now.timestamp(), self.api.now.timestamp()))
        self.assertTrue(any(item["task_id"] == meta["id"] for item in self.plan()["files"]))

    def test_plan_oldest_first_ten_files_max_and_readonly(self):
        for index in range(14):
            path = self.file("messages/archive/%02d.md" % index)
            stamp = self.old.timestamp() + index * 100
            os.utime(path, (stamp, stamp))
        before = sorted(str(path) for path in self.guild.rglob("*"))
        plan = self.plan()
        after = sorted(str(path) for path in self.guild.rglob("*"))
        self.assertEqual(before, after)
        self.assertEqual(len(plan["files"]), 10)
        self.assertEqual(plan["remaining_files"], 4)
        self.assertEqual(plan["files"][0]["path"], "messages/archive/00.md")
        self.assertEqual(plan["files"][-1]["path"], "messages/archive/09.md")
        self.assertEqual(plan["physical_bytes_freed"], 0)
        self.assertTrue(all(len(item["sha256"]) == 64 for item in plan["files"]))

    def test_pin_hold_refs_and_missing_refs_protect_without_budget_exemption(self):
        archived, meta = self.task(hold=True)
        self.assertEqual(self.plan()["files"], [])
        meta["hold"] = False
        self.file(archived + "/meta.json", json.dumps(meta))
        active, live = self.task("20250102-abcdef123456-活跃任务", active=True, refs=[meta["id"]])
        self.assertEqual(self.plan()["files"], [])
        live.pop("refs")
        self.file(active + "/meta.json", json.dumps(live))
        self.file("log/archive/unrelated")
        plan = self.plan()
        self.assertFalse(plan["status"]["references_complete"])
        self.assertEqual(plan["files"], [])
        self.config(history_max_bytes=1, history_target_bytes=0)
        with self.assertRaises(RuntimeError):
            history.ensure_capacity(self.api)

    def test_metadata_references_paths_and_unknown_reference_are_conservative(self):
        target = self.file("log/archive/keep")
        _, live = self.task("20250102-abcdef123456-活跃任务", active=True,
                            metadata={"references": [{"path": "log/archive"}]})
        self.assertFalse(any(item["path"] == "log/archive/keep" for item in self.plan()["files"]))
        rel = "handoff/active/" + live["id"] + "/meta.json"
        live["metadata"]["references"] = [{"unknown": "format"}]
        self.file(rel, json.dumps(live))
        self.assertFalse(self.plan()["status"]["references_complete"])
        self.assertTrue(target.exists())

    def test_invalid_meta_is_reported_and_prevents_retirement(self):
        self.file("handoff/active/broken/meta.json", "not json")
        self.file("log/archive/old")
        code, out, err = self.run_cli("plan")
        self.assertEqual(code, 1, err)
        plan = json.loads(out)
        self.assertFalse(plan["status"]["complete"])
        self.assertFalse(plan["status"]["references_complete"])
        self.assertEqual(plan["files"], [])
        with self.assertRaises(RuntimeError):
            history.ensure_capacity(self.api)

    def test_task_count_and_full_days_trigger_suggestions(self):
        self.config(history_max_tasks=0)
        rel, _ = self.task(closed_at=(self.api.now - timedelta(days=40)).isoformat())
        plan = self.plan()
        self.assertTrue(plan["status"]["over_task_limit"])
        self.assertTrue(plan["compression_suggestions"])
        self.assertTrue(any("task_count" in item["reasons"] for item in plan["files"]))
        self.assertFalse(any(item["path"] in (rel + "/meta.json", rel + "/context.md") for item in plan["files"]))

    def test_high_and_low_watermarks_are_explicit(self):
        self.config(history_max_bytes=100, history_target_bytes=80)
        path = self.file("messages/archive/mid-age", b"x" * 101)
        stamp = (self.api.now - timedelta(days=60)).timestamp()
        os.utime(path, (stamp, stamp))
        plan = self.plan()
        self.assertEqual(plan["status"]["bytes_to_target"], 21)
        self.assertEqual(plan["files"][0]["reasons"], ["high_watermark"])
        self.assertTrue(plan["requires_manual_release"])

    def test_saved_plan_has_one_bounded_managed_path(self):
        self.file("messages/archive/old")
        first = self.plan(save=True)
        self.plan(save=True)
        paths = [p.relative_to(self.guild).as_posix() for p in (self.guild / "history").rglob("*") if p.is_file()]
        self.assertEqual(paths, [history.PLAN_PATH])
        self.assertEqual(json.loads((self.guild / history.PLAN_PATH).read_text())["files"], first["files"])
        for path in ("other-plan.json", "../escape.json", str(self.base / "escape.json")):
            code, _, _ = self.run_cli("plan", "--output", path)
            self.assertEqual(code, 1)
        self.assertFalse((self.base / "escape.json").exists())

    def test_apply_requires_confirmation_and_plan(self):
        source = self.file("messages/archive/old")
        self.plan(save=True)
        for args in (("apply", "--plan", history.PLAN_PATH), ("apply", "--confirm")):
            code, _, _ = self.run_cli(*args)
            self.assertEqual(code, 1)
        self.assertTrue(source.exists())

    def test_apply_copies_verifies_and_quarantines_without_freeing_space(self):
        source = self.file("messages/archive/old", b"old details")
        plan = self.plan(save=True)
        before = history.report(self.api)["total_bytes"]
        code, out, err = self.run_cli("apply", "--plan", history.PLAN_PATH, "--confirm")
        self.assertEqual(code, 0, err)
        result = json.loads(out)
        self.assertFalse(source.exists())
        self.assertEqual(result["physical_bytes_freed"], 0)
        self.assertTrue(result["manual_release_required"])
        for root in (result["backup_root"], result["quarantine_root"]):
            self.assertEqual((self.guild / root / "messages/archive/old").read_bytes(), b"old details")
        manifest = json.loads((self.guild / result["manifest"]).read_text())
        self.assertEqual(manifest["plan"]["token"], plan["token"])
        self.assertEqual(manifest["status"], "quarantined")
        self.assertGreater(history.report(self.api)["total_bytes"], before)
        self.assertEqual(self.run_cli("apply", "--plan", history.PLAN_PATH, "--confirm")[0], 1)
        self.assertEqual(self.plan()["files"], [])

    def test_apply_retains_task_summary_and_artifact_backup(self):
        rel, _ = self.task()
        self.plan(save=True)
        code, out, err = self.run_cli("apply", "--plan", history.PLAN_PATH, "--confirm")
        self.assertEqual(code, 0, err)
        result = json.loads(out)
        self.assertTrue((self.guild / rel / "meta.json").exists())
        self.assertTrue((self.guild / rel / "context.md").exists())
        self.assertTrue((self.guild / result["backup_root"] / rel / "artifacts/output.bin").exists())

    def test_apply_refuses_changed_stat_hash_and_revision(self):
        rel, meta = self.task()
        self.plan(save=True)
        meta["revision"] += 1
        self.file(rel + "/meta.json", json.dumps(meta))
        code, _, err = self.run_cli("apply", "--plan", history.PLAN_PATH, "--confirm")
        self.assertEqual(code, 1)
        self.assertIn("变化", err)
        self.assertFalse((self.guild / "history/backups").exists())
        self.plan(save=True)
        self.file(rel + "/artifacts/output.bin", b"changed")
        self.assertEqual(self.run_cli("apply", "--plan", history.PLAN_PATH, "--confirm")[0], 1)
        self.assertFalse((self.guild / "history/backups").exists())

    def test_apply_refuses_new_reference_and_new_hold(self):
        rel, meta = self.task()
        self.plan(save=True)
        self.task("20250102-abcdef123456-活跃任务", active=True, refs=[meta["id"]])
        self.assertEqual(self.run_cli("apply", "--plan", history.PLAN_PATH, "--confirm")[0], 1)
        self.assertTrue((self.guild / rel / "sessions/000001/context.md").exists())

    def test_apply_refuses_tampered_token_and_escaped_paths(self):
        self.file("messages/archive/old")
        plan = self.plan(save=True)
        plan["files"][0]["path"] = "../outside"
        self.file(history.PLAN_PATH, json.dumps(plan))
        self.assertEqual(self.run_cli("apply", "--plan", history.PLAN_PATH, "--confirm")[0], 1)
        plan["token"] = history._digest({k: v for k, v in plan.items() if k != "token"})
        self.file(history.PLAN_PATH, json.dumps(plan))
        self.assertEqual(self.run_cli("apply", "--plan", history.PLAN_PATH, "--confirm")[0], 1)
        self.assertFalse((self.guild / "history/backups").exists())

    def test_apply_refuses_other_guild_plan(self):
        self.file("messages/archive/old")
        plan = self.plan(save=True)
        plan["scope"] = "another guild"
        plan["token"] = history._digest({k: v for k, v in plan.items() if k != "token"})
        self.file(history.PLAN_PATH, json.dumps(plan))
        self.assertEqual(self.run_cli("apply", "--plan", history.PLAN_PATH, "--confirm")[0], 1)

    def test_apply_stops_without_moving_when_backup_verification_fails(self):
        source = self.file("messages/archive/old", "original")
        self.plan(save=True)
        original = history._copy_verified
        def corrupt(root, item, target):
            original(root, item, target)
            raise RuntimeError("模拟备份回读失败")
        with mock.patch.object(history, "_copy_verified", side_effect=corrupt):
            code, _, err = self.run_cli("apply", "--plan", history.PLAN_PATH, "--confirm")
        self.assertEqual(code, 1)
        self.assertIn("备份", err)
        self.assertEqual(source.read_text(), "original")
        self.assertTrue((self.guild / "history/backups").exists())
        self.assertEqual(self.run_cli("apply", "--plan", history.PLAN_PATH, "--confirm")[0], 1)

    def test_apply_over_budget_refuses_even_if_candidates_exist(self):
        self.config(history_max_bytes=5000, history_target_bytes=4000)
        source = self.file("messages/archive/old", b"x" * 500)
        self.plan(save=True)
        self.file("history/extra-report", b"x" * 1000)
        code, _, err = self.run_cli("apply", "--plan", history.PLAN_PATH, "--confirm")
        self.assertEqual(code, 1)
        self.assertIn("预算不足", err)
        self.assertTrue(source.exists())
        self.assertFalse((self.guild / "history/backups").exists())

    def test_maintenance_rate_limit_is_fixed_file_and_does_not_move(self):
        source = self.file("messages/archive/old")
        first = history.maintenance(self.api)
        second = history.maintenance(self.api)
        self.assertTrue(first["checked"])
        self.assertFalse(second["checked"])
        self.assertTrue(second["rate_limited"])
        self.api.now += timedelta(days=2)
        self.assertTrue(history.maintenance(self.api)["checked"])
        paths = [p.relative_to(self.guild).as_posix() for p in (self.guild / "history").rglob("*") if p.is_file()]
        self.assertEqual(paths, [history.STATE_PATH])
        self.assertTrue(source.exists())
        self.assertFalse((self.guild / "history/backups").exists())

    def test_maintenance_cannot_append_cache_above_budget(self):
        self.config(history_max_bytes=10, history_target_bytes=8)
        self.file("messages/archive/old", b"x" * 11)
        result = history.maintenance(self.api)
        self.assertFalse(result["state_written"])
        self.assertTrue(result["status"]["over_budget"])
        self.assertFalse((self.guild / "history").exists())

    def test_task_engine_snapshot_contract_and_reopen_protection(self):
        task_id = "20250101-123456789abc"
        directory = task_id + "-实际任务"
        rel = "handoff/active/" + directory
        current = "r00000002-abcdef123456"
        prior = "r00000001-123456abcdef"
        meta = {"id": task_id, "directory": directory, "revision": 3,
                "snapshot": current, "snapshot_revision": 2, "status": "active",
                "closure": None, "refs": [], "hold": False}
        self.file(rel + "/meta.json", json.dumps(meta))
        self.file(rel + "/context.md", "当前索引")
        self.file(rel + "/snapshots/" + current + "/context.md", "当前正文")
        self.file(rel + "/snapshots/" + current + "/manifest.json", json.dumps(
            {"task_id": task_id, "artifacts": [{"path": "artifacts/needed.bin"}]}))
        self.file(rel + "/snapshots/" + prior + "/context.md", "旧正文")
        self.file(rel + "/snapshots/" + prior + "/manifest.json", "{}")
        self.file(rel + "/artifacts/needed.bin", b"needed")
        self.file(rel + "/artifacts/old.bin", b"old")
        status = history.report(self.api)
        self.assertTrue(status["references_complete"])
        self.assertEqual(status["total_bytes"], len("旧正文".encode("utf-8")) + 2 + 3)
        archived = "handoff/archive/" + directory
        (self.guild / "handoff/archive").mkdir()
        os.rename(self.guild / rel, self.guild / archived)
        meta.update(status="closed", closure={"closed_at": self.old.isoformat()})
        self.file(archived + "/meta.json", json.dumps(meta))
        plan = self.plan(save=True)
        self.assertEqual(plan["status"]["archived_tasks"], 1)
        self.assertEqual(len(plan["files"]), 2)
        self.assertTrue(all("/snapshots/" + prior + "/" in item["path"] for item in plan["files"]))
        code, out, err = self.run_cli("apply", "--plan", history.PLAN_PATH, "--confirm")
        self.assertEqual(code, 0, err)
        self.assertTrue((self.guild / archived / "snapshots" / current / "context.md").exists())
        self.assertTrue((self.guild / archived / "artifacts/needed.bin").exists())

    def test_reference_to_task_child_protects_entire_package(self):
        rel, _ = self.task()
        self.task("20250102-abcdef123456-活跃任务", active=True,
                  refs=[{"path": rel + "/artifacts/output.bin"}])
        self.assertEqual(self.plan()["files"], [])

    def test_pending_transition_blocks_retirement(self):
        rel, _ = self.task()
        self.file(rel + "/.transition.json", "{}")
        self.assertFalse(self.plan()["status"]["references_complete"])
        self.assertEqual(self.plan()["files"], [])

    def test_watermark_plan_stops_at_low_target(self):
        self.config(history_max_bytes=100, history_target_bytes=80)
        for name in ("a", "b"):
            path = self.file("messages/archive/" + name, b"x" * 60)
            stamp = (self.api.now - timedelta(days=40)).timestamp()
            os.utime(path, (stamp, stamp))
        plan = self.plan()
        self.assertEqual(len(plan["files"]), 1)
        self.assertEqual(plan["status"]["bytes_to_target"], 40)

    def test_budget_lock_orders_after_business_lock_and_rejects_links(self):
        with self.api._append_lock(self.guild.resolve() / "handoff"):
            with history.budget_lock(self.api):
                self.assertEqual([path.name for path in self.api.locks], ["handoff", "history-budget"])
        outside = self.base / "outside-lock"
        outside.write_text("untouched", encoding="utf-8")
        (self.guild / ".history-budget.ag-lock").symlink_to(outside)
        with self.assertRaises(RuntimeError):
            with history.budget_lock(self.api):
                self.fail("不应进入外部锁")
        self.assertEqual(outside.read_text(encoding="utf-8"), "untouched")

    def test_tests_never_resolve_default_guild(self):
        root = history._root(self.api)
        self.assertTrue(root.is_relative_to(self.base.resolve()))
        self.assertNotEqual(root, Path.home() / ".agent-guild")
        code, out, err = self.run_cli("status", "--json")
        self.assertEqual(code, 0, err)
        self.assertEqual(json.loads(out)["total_bytes"], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
