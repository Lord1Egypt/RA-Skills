#!/usr/bin/env python3
"""保留循环隔离测试；所有数据和 CLI 环境只使用临时 guild。"""

import contextlib
import copy
import hashlib
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
import zipfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest import mock

import ag_history as H
import ag_retention as R
import ag_tasks as T


class API:
    def __init__(self, root):
        self.CENTRAL = root
        self.now = datetime(2026, 10, 19, tzinfo=timezone.utc)
        self.locks = []

    def now_iso(self):
        return self.now.isoformat()

    def host_id(self):
        return "test-host"

    @contextlib.contextmanager
    def _append_lock(self, path):
        if path in self.locks:
            raise AssertionError("锁不得重入")
        self.locks.append(path)
        try:
            yield
        finally:
            self.locks.pop()

    def _atomic_write_text(self, path, text):
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_name(".test-" + path.name)
        temporary.write_text(text, encoding="utf-8")
        os.replace(temporary, path)

    def atomic_write_json(self, path, value):
        self._atomic_write_text(path, json.dumps(value, ensure_ascii=False) + "\n")


class RetentionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="ag-retention-test-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.root = self.base / "guild"
        self.root.mkdir()
        self.api = API(self.root)
        self.counter = 0
        patch = mock.patch.dict(os.environ, {"AGENT_GUILD_DIR": str(self.root), "AG_HOST_ID": "test-host"})
        patch.start()
        self.addCleanup(patch.stop)

    def file(self, rel, data):
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data if isinstance(data, bytes) else data.encode("utf-8"))
        return path

    def task(self, age=240, count=1, size=262144, pin=False, references=None):
        self.counter += 1
        task_id = "20260101-" + ("%012x" % self.counter)
        name = task_id + "-历史任务"
        rel = "handoff/archive/" + name
        owner = {"host": "test-host", "session": "session-test", "agent": "coder"}
        now = (self.api.now - timedelta(days=age)).isoformat()
        context = "# 目标\n保留完整证据，不推断结论。\n# 决策\n经用户选择后继续。\n"
        meta = {"schema_version": 1, "id": task_id, "directory": name, "title": "历史任务", "project": "test",
                "summary": "待审阅的事实", "status": "closed", "revision": 2, "created_at": now,
                "updated_at": now, "snapshot": "r00000001-000000000001", "snapshot_revision": 1,
                "owners": [], "sessions": [owner], "closure": {"evidence": "临时测试通过", "closed_at": now, "by": owner},
                "references": references or [], "pin": pin, "hold": False}
        artifacts = []
        for index in range(count):
            data = (b"compressible-evidence-%d\n" % index) * (size // 24 + 1)
            digest = hashlib.sha256(data).hexdigest()
            name = "proof%d.bin" % index
            path = "artifacts/" + digest + "-" + name
            artifacts.append({"name": name, "path": path, "sha256": digest, "size": len(data)})
            self.file(rel + "/" + path, data)
        manifest = {"schema_version": 1, "task_id": task_id, "revision": 1,
                    "context": T._hash(context.encode("utf-8")), "artifacts": artifacts}
        self.file(rel + "/snapshots/" + meta["snapshot"] + "/context.md", context)
        self.file(rel + "/snapshots/" + meta["snapshot"] + "/manifest.json", json.dumps(manifest, ensure_ascii=False))
        self.file(rel + "/meta.json", json.dumps(meta, ensure_ascii=False))
        return rel, meta, context

    def config(self, **values):
        self.file("RETENTION.md", "\n".join("%s=%s" % item for item in values.items()))

    def cli(self, *args):
        output, error = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(error):
            code = R.run(args, self.api)
        return code, json.loads(output.getvalue() or error.getvalue()), error.getvalue()

    def apply(self, command, plan, data_loss=True, max_batches=100):
        path = self.base / (plan["token"] + ".json")
        path.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
        args = [command, "--plan", str(path), "--confirm", plan["token"]]
        if data_loss and plan.get("irreversible"):
            args += ["--confirm-data-loss", plan["data_loss_token"]]
        results = []
        for _ in range(max_batches):
            code, result, err = self.cli(*args)
            self.assertEqual(code, 0, err or result)
            results.append(result)
            batch = result.get("batch") or result
            self.assertLessEqual(batch.get("unlinked_files", 0), 10)
            if result["state"] == "complete":
                return results
        self.fail("维护批次未能有界完成: " + str(results[-1]))

    def test_compact_lossless_summary_content_and_restore(self):
        rel, meta, context = self.task(count=13)
        before = {path.relative_to(self.root / rel).as_posix(): path.read_bytes()
                  for path in (self.root / rel).rglob("*") if path.is_file()}
        initial = H.report(self.api)["total_bytes"]
        plan = R._task_plan(self.api, meta["id"], "compact-plan")
        self.assertEqual(plan["summary"]["verbatim_context_prefix"], context)
        results = self.apply("compact", plan)
        self.assertGreater(len(results), 1)
        self.assertLess(H.report(self.api)["total_bytes"], initial // 4)
        self.assertEqual(json.loads((self.root / rel / "meta.json").read_text()), meta)
        self.assertEqual(R.load_content(self.api, self.root / rel, meta)[0], context)
        with H._lock(self.api, self.root):
            restored = R.restore_for_reopen(self.api, self.root / rel, meta)
        after = {path.relative_to(restored).as_posix(): path.read_bytes()
                 for path in restored.rglob("*") if path.is_file()}
        self.assertEqual(before, after)
        self.assertEqual(self.api.locks, [])

    def test_retire_batches_atomic_and_restore(self):
        rel, meta, _ = self.task(count=20)
        plan = R._task_plan(self.api, meta["id"], "retire-plan")
        with H._lock(self.api, self.root):
            first = R._retire(self.api, plan)
        self.assertEqual(first["state"], "in_progress")
        self.assertTrue((self.root / rel / "meta.json").exists())
        results = self.apply("retire", plan)
        self.assertFalse((self.root / rel).exists())
        self.assertEqual(R._inventory(self.api).summary()["archived_tasks"], 0)
        self.assertTrue(all(result["physical_bytes_freed"] == 0 for result in results))
        code, result, err = self.cli("restore", "--ticket", plan["token"])
        self.assertEqual(code, 0, err)
        self.assertTrue((self.root / rel / "meta.json").exists())
        self.assertEqual(result["task_id"], meta["id"])

    def test_purge_double_confirmation_batches_and_persistent_summary(self):
        rel, meta, _ = self.task(count=16)
        retire = R._task_plan(self.api, meta["id"], "retire-plan")
        self.apply("retire", retire)
        plan = R._recovery_plan(self.api, retire["token"])
        path = self.base / "purge-plan.json"
        path.write_text(json.dumps(plan), encoding="utf-8")
        for extra in ([], ["--confirm-data-loss", "wrong"]):
            code, _, _ = self.cli("purge", "--plan", str(path), "--confirm", plan["token"], *extra)
            self.assertEqual(code, 1)
            self.assertTrue((self.root / plan["source"] / "meta.json").exists())
        before = H.report(self.api)["total_bytes"]
        results = self.apply("purge", plan)
        self.assertGreater(len(results), 1)
        self.assertFalse((self.root / plan["source"]).exists())
        self.assertFalse((self.root / plan["backup_path"]).exists())
        receipt = json.loads((self.root / plan["receipt_path"]).read_text())
        self.assertEqual(receipt["state"], "purged")
        self.assertEqual(receipt["summary"], plan["summary"])
        self.assertLess(H.report(self.api)["total_bytes"], before // 4)
        code, _, _ = self.cli("restore", "--ticket", retire["token"])
        self.assertEqual(code, 1)

    def test_plan_tamper_hash_refs_config_and_links_fail_closed(self):
        rel, meta, _ = self.task()
        plan = R._task_plan(self.api, meta["id"], "compact-plan")
        modified = copy.deepcopy(plan)
        modified["files"][0]["sha256"] = "0" * 64
        with self.assertRaisesRegex(RuntimeError, "令牌"):
            R._compact(self.api, modified)
        selected = self.root / rel / plan["files"][0]["path"]
        original = selected.read_bytes()
        selected.write_bytes(b"changed")
        with self.assertRaises(RuntimeError):
            R._compact(self.api, plan)
        selected.write_bytes(original)
        plan = R._task_plan(self.api, meta["id"], "compact-plan")
        self.config(history_max_tasks=1)
        with self.assertRaisesRegex(RuntimeError, "配置"):
            R._compact(self.api, plan)
        (self.root / "RETENTION.md").unlink()
        self.task(references=[meta["id"]])
        with self.assertRaisesRegex(RuntimeError, "元数据|引用"):
            R._compact(self.api, plan)
        for kind in ("symlink", "hardlink"):
            extra = self.root / rel / "unsafe"
            if kind == "symlink":
                extra.symlink_to(selected)
            else:
                os.link(selected, extra)
            with self.assertRaises(RuntimeError):
                R._task_plan(self.api, meta["id"], "retire-plan")
            extra.unlink()

    def test_selection_does_not_read_other_payload(self):
        rel, meta, _ = self.task()
        other, _, _ = self.task()
        original = H._open_file
        @contextlib.contextmanager
        def guarded(root, path, expected=None):
            if path.startswith(other + "/") and not path.endswith("meta.json"):
                raise AssertionError("不得读取未选中的 payload")
            with original(root, path, expected) as stream:
                yield stream
        with mock.patch.object(H, "_open_file", guarded):
            plan = R._task_plan(self.api, meta["id"], "compact-plan")
            self.apply("compact", plan)

    def test_compact_interruption_after_unlink_resumes(self):
        rel, meta, context = self.task(count=12)
        plan = R._task_plan(self.api, meta["id"], "compact-plan")
        original = R._unlink
        called = []
        def interrupted(root, path, digest=None):
            original(root, path, digest)
            called.append(path)
            if len(called) == 1:
                raise OSError("注入删除后崩溃")
        with mock.patch.object(R, "_unlink", interrupted):
            with self.assertRaises(OSError):
                R._compact(self.api, plan)
        self.assertEqual(R.load_content(self.api, self.root / rel, meta)[0], context)
        self.apply("compact", plan)
        self.assertEqual(R.load_content(self.api, self.root / rel, meta)[0], context)

    def test_zip_build_interruption_preserves_original_and_resumes(self):
        rel, meta, _ = self.task()
        plan = R._task_plan(self.api, meta["id"], "compact-plan")
        original = R._LimitedWriter.write
        count = []
        def broken(writer, data):
            count.append(1)
            if len(count) == 3:
                raise OSError("注入 ZIP 写入故障")
            return original(writer, data)
        with mock.patch.object(R._LimitedWriter, "write", broken):
            with self.assertRaises(OSError):
                R._compact(self.api, plan)
        self.assertTrue(all((self.root / rel / row["path"]).exists() for row in plan["files"]))
        self.apply("compact", plan)

    def test_retire_rename_failure_resumes(self):
        rel, meta, _ = self.task()
        plan = R._task_plan(self.api, meta["id"], "retire-plan")
        original = os.rename
        def broken(source, target):
            original(source, target)
            raise OSError("注入 rename 后崩溃")
        with mock.patch.object(os, "rename", broken):
            with self.assertRaises(OSError):
                R._retire(self.api, plan)
        self.apply("retire", plan)
        code, _, err = self.cli("restore", "--id", meta["id"])
        self.assertEqual(code, 0, err)

    def test_purge_interruption_after_delete_resumes_with_backup(self):
        _, meta, _ = self.task(count=12)
        retire = R._task_plan(self.api, meta["id"], "retire-plan")
        self.apply("retire", retire)
        plan = R._recovery_plan(self.api, retire["token"])
        original = R._unlink
        calls = []
        def interrupted(root, path, digest=None):
            original(root, path, digest)
            calls.append(path)
            if len(calls) == 1:
                raise OSError("注入清空故障")
        with mock.patch.object(R, "_unlink", interrupted):
            with self.assertRaises(OSError):
                R._purge(self.api, plan)
        self.assertTrue((self.root / plan["backup_path"]).exists())
        self.apply("purge", plan)

    def test_purge_permission_and_new_reference_do_not_delete(self):
        _, meta, _ = self.task(count=1)
        retire = R._task_plan(self.api, meta["id"], "retire-plan")
        self.apply("retire", retire)
        plan = R._recovery_plan(self.api, retire["token"])
        source = self.root / plan["source"]
        before = {path: path.read_bytes() for path in source.rglob("*") if path.is_file()}
        source.chmod(0o500)
        try:
            with self.assertRaises(RuntimeError):
                R._purge(self.api, plan)
            self.assertTrue(all(path.read_bytes() == data for path, data in before.items()))
        finally:
            source.chmod(0o700)
        self.task(references=[meta["id"]])
        with self.assertRaisesRegex(RuntimeError, "引用|元数据"):
            R._purge(self.api, plan)

    def test_legacy_backup_and_quarantine_can_be_purged(self):
        data = b"old-verified-history" * 10000
        path = self.file("log/archive/history.txt", data)
        old = (self.api.now - timedelta(days=300)).timestamp()
        os.utime(path, (old, old))
        with H._lock(self.api, self.root):
            plan = H._plan(H._Inventory(self.api))
            self.assertTrue(plan["files"])
        H._write_plan(self.api, H.PLAN_PATH)
        result = H._apply(self.api, H.PLAN_PATH)
        ticket = result["backup_root"].split("/")[-1]
        purge = R._recovery_plan(self.api, ticket)
        self.apply("purge", purge)
        self.assertFalse((self.root / result["backup_root"]).exists())
        self.assertFalse((self.root / result["quarantine_root"]).exists())
        self.assertTrue((self.root / purge["preserved_receipt"]).exists())

    def test_cycle_compacts_retires_purges_to_low_watermark(self):
        self.task(count=6, size=1024 * 1024)
        self.task(age=100, count=6, size=1024 * 1024)
        self.config(history_max_bytes=15000000, history_target_bytes=600000, history_max_tasks=1)
        before = H.report(self.api)["total_bytes"]
        plan = R._cycle_plan(self.api)
        self.assertEqual(plan["actions"][0]["plan"]["task_id"], "20260101-000000000001")
        self.assertTrue((self.root / "handoff/archive").exists())
        results = self.apply("cycle", plan)
        self.assertGreater(len(results), 2)
        final = results[-1]
        self.assertLess(final["total_bytes"], before)
        self.assertLessEqual(final["total_bytes"], 600000)
        self.assertFalse(any(final["needs"].values()))

    def test_full_budget_plan_and_reserve_are_bounded(self):
        _, meta, _ = self.task(count=2, size=1024 * 1024)
        self.config(history_max_bytes=100000, history_target_bytes=80000)
        code, plan, err = self.cli("compact-plan", "--id", meta["id"])
        self.assertEqual(code, 0, err)
        self.apply("compact", plan)
        self.assertLess(H.report(self.api)["total_bytes"], 100000)
        self.file("history/blocker", b"x" * 1024)
        with mock.patch.object(R, "MAINTENANCE_RESERVE_BYTES", 1):
            self.config(history_max_bytes=1, history_target_bytes=0)
            with self.assertRaisesRegex(RuntimeError, "峰值"):
                R._capacity(self.api, 10)

    def test_protected_cycle_is_bounded_and_needs_confirmation_is_readonly(self):
        rel, meta, _ = self.task(pin=True)
        self.config(history_max_bytes=500000, history_target_bytes=1)
        plan = R._cycle_plan(self.api)
        self.assertFalse(plan["actions"])
        with H._lock(self.api, self.root):
            result = R._cycle(self.api, plan, False)
        self.assertEqual(result["state"], "blocked")
        self.assertTrue((self.root / rel / "meta.json").exists())

    def test_zip_traversal_and_bomb_rejected(self):
        rel, meta, _ = self.task()
        plan = R._task_plan(self.api, meta["id"], "compact-plan")
        self.apply("compact", plan)
        path = self.root / rel / R.PAYLOAD
        original = path.read_bytes()
        with zipfile.ZipFile(path, "a") as archive:
            archive.writestr("../outside", "evil")
        pack_path = self.root / rel / R.PACK
        pack = json.loads(pack_path.read_text())
        pack["zip"]["size"] = path.stat().st_size
        pack["zip"]["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
        pack_path.write_text(json.dumps(pack), encoding="utf-8")
        with self.assertRaises(RuntimeError):
            R.load_content(self.api, self.root / rel, meta)
        self.assertFalse((self.root / "outside").exists())
        path.write_bytes(original)
        pack["zip"]["size"] = len(original)
        pack["zip"]["sha256"] = hashlib.sha256(original).hexdigest()
        pack["files"][0]["size"] = R.MAX_MEMBER_BYTES + 1
        pack_path.write_text(json.dumps(pack), encoding="utf-8")
        with self.assertRaises(RuntimeError):
            R.restore_for_reopen(self.api, self.root / rel, meta)

    def test_restore_extraction_failure_and_rename_failure_resume(self):
        rel, meta, context = self.task(count=3)
        plan = R._task_plan(self.api, meta["id"], "compact-plan")
        self.apply("compact", plan)
        original = os.rename
        failures = []
        def interrupted(source, target):
            if Path(source).name == R.RESTORE_TMP and not failures:
                original(source, target)
                failures.append(1)
                raise OSError("恢复 rename 后崩溃")
            return original(source, target)
        with mock.patch.object(os, "rename", interrupted):
            with self.assertRaises(OSError):
                R.restore_for_reopen(self.api, self.root / rel, meta)
        self.assertTrue((self.root / rel / R.PAYLOAD).exists())
        R.restore_for_reopen(self.api, self.root / rel, meta)
        self.assertEqual(R._raw_content(self.root, rel, meta)[0], context)
        self.assertFalse((self.root / rel / R.PACK).exists())
        retire = R._task_plan(self.api, meta["id"], "retire-plan")
        self.apply("retire", retire)
        def restore_crash(source, target):
            original(source, target)
            raise OSError("整包恢复 rename 后崩溃")
        with mock.patch.object(os, "rename", restore_crash):
            with self.assertRaises(OSError):
                R._restore(self.api, retire["token"])
        R._restore(self.api, retire["token"])
        self.assertTrue((self.root / rel / "meta.json").exists())

    def test_forged_resealed_purge_cannot_escape_managed_scope(self):
        _, meta, _ = self.task()
        retire = R._task_plan(self.api, meta["id"], "retire-plan")
        self.apply("retire", retire)
        plan = R._recovery_plan(self.api, retire["token"])
        protected = self.file("memory/shared/fact.txt", "必须保留")
        altered = copy.deepcopy(plan)
        altered["source"] = "memory/shared"
        altered["files"] = [{"path": "fact.txt", "sha256": hashlib.sha256(protected.read_bytes()).hexdigest(),
                             "size": protected.stat().st_size, "stat": H._stamp(protected.stat())}]
        altered = R._seal(altered)
        with self.assertRaisesRegex(RuntimeError, "登记退役包"):
            R._purge(self.api, altered)
        self.assertEqual(protected.read_text(), "必须保留")

    def test_permanent_last_backup_delete_failure_resume(self):
        _, meta, _ = self.task()
        retire = R._task_plan(self.api, meta["id"], "retire-plan")
        self.apply("retire", retire)
        plan = R._recovery_plan(self.api, retire["token"])
        original = R._unlink
        def interrupted(root, path, digest=None):
            original(root, path, digest)
            if path == plan["backup_path"]:
                raise OSError("最后备份删除后崩溃")
        with mock.patch.object(R, "_unlink", interrupted):
            with self.assertRaises(OSError):
                R._purge(self.api, plan)
        self.apply("purge", plan)
        self.assertFalse((self.root / plan["source"]).exists())

    def test_summary_includes_end_of_document_decision_with_markers(self):
        rel, meta, _ = self.task(count=0)
        decision = "# 文末决定\n最终决定：证据链保持只读，执行有界清理。\n"
        body = "# 过程\n" + "中间过程逐条记录，不推断结论。\n" * 6000 + decision
        snapshot = self.root / rel / "snapshots" / meta["snapshot"]
        (snapshot / "context.md").write_text(body, encoding="utf-8")
        manifest = json.loads((snapshot / "manifest.json").read_text(encoding="utf-8"))
        manifest["context"] = T._hash(body.encode("utf-8"))
        (snapshot / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
        plan = R._task_plan(self.api, meta["id"], "retire-plan")
        summary = plan["summary"]
        self.assertTrue(summary["truncated"])
        self.assertGreater(summary["truncated_bytes"], 0)
        self.assertNotIn("最终决定", summary["verbatim_context_prefix"])
        self.assertIn("最终决定：证据链保持只读", summary["verbatim_context_suffix"])
        self.assertEqual(summary["suffix_offset"], len(body.encode("utf-8")) - R.SUMMARY_BYTES // 2)
        self.assertEqual(summary["source"]["context_size"], len(body.encode("utf-8")))

    def test_purged_receipt_bounded_cleanup_requires_double_confirmation(self):
        _, meta, _ = self.task(count=1)
        retire = R._task_plan(self.api, meta["id"], "retire-plan")
        self.apply("retire", retire)
        purge = R._recovery_plan(self.api, retire["token"])
        self.apply("purge", purge)
        before = H.report(self.api)["total_bytes"]
        preview = R.preview_cycle(self.api)
        self.assertEqual(preview["counts"]["receipt_cleanup"], 1)
        self.assertFalse(preview["applied"])
        plan = R._cycle_plan(self.api)
        self.assertEqual([action["kind"] for action in plan["actions"]], ["receipt-cleanup"])
        self.assertTrue(plan["irreversible"])
        path = self.base / (plan["token"] + ".json")
        path.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
        code, result, err = self.cli("cycle", "--plan", str(path), "--confirm", plan["token"])
        self.assertEqual(code, 2, err or result)
        self.assertEqual(result["state"], "needs_confirmation")
        self.assertTrue((self.root / "history/retired" / retire["token"] / "receipt.json").exists())
        code, _, _ = self.cli("cycle", "--plan", str(path), "--confirm", plan["token"],
                              "--confirm-data-loss", "wrong")
        self.assertEqual(code, 1)
        results = self.apply("cycle", plan)
        self.assertEqual(results[-1]["state"], "complete")
        self.assertFalse((self.root / "history/retired" / retire["token"]).exists())
        self.assertLess(H.report(self.api)["total_bytes"], before)
        self.assertTrue(H.report(self.api)["complete"])
        self.assertEqual(R.preview_cycle(self.api)["counts"]["receipt_cleanup"], 0)

    def test_restored_receipt_cleanup_in_cycle_after_restore(self):
        self.config(history_full_days=170, history_retention_days=180)
        rel, meta, _ = self.task(age=150, count=1)
        retire = R._task_plan(self.api, meta["id"], "retire-plan")
        self.apply("retire", retire)
        code, _, err = self.cli("restore", "--ticket", retire["token"])
        self.assertEqual(code, 0, err)
        self.assertTrue((self.root / rel / "meta.json").exists())
        before = H.report(self.api)["total_bytes"]
        plan = R._cycle_plan(self.api)
        self.assertEqual([action["kind"] for action in plan["actions"]], ["receipt-cleanup"])
        self.assertTrue(plan["irreversible"])
        results = self.apply("cycle", plan)
        self.assertEqual(results[-1]["state"], "complete")
        self.assertFalse((self.root / "history/retired" / retire["token"]).exists())
        self.assertTrue((self.root / rel / "meta.json").exists())
        self.assertLess(H.report(self.api)["total_bytes"], before)
        cleanup = R._receipt_cleanup(self.api, plan["actions"][0]["plan"])
        self.assertEqual(cleanup["state"], "complete")
        self.assertEqual(cleanup["unlinked_files"], 0)

    def test_metadata_preview_never_reads_payload(self):
        rel, _, _ = self.task()
        original = H._open_file
        @contextlib.contextmanager
        def guarded(root, path, expected=None):
            if path.startswith(rel + "/") and not path.endswith("meta.json"):
                raise AssertionError("维护预览不能读正文")
            with original(root, path, expected) as stream:
                yield stream
        with mock.patch.object(H, "_open_file", guarded):
            result = R.preview_cycle(self.api)
        self.assertFalse(result["applied"])
        self.assertFalse((self.root / "history").exists())

    def test_uncompressible_cycle_falls_back_without_loop(self):
        rel, meta, _ = self.task(count=0)
        self.config(history_max_bytes=2000000, history_target_bytes=1000000)
        plan = R._cycle_plan(self.api)
        results = self.apply("cycle", plan)
        self.assertLess(len(results), 8)
        self.assertFalse((self.root / rel).exists())

    def test_cli_integrated_compact_list_and_reopen(self):
        rel, meta, context = self.task()
        plan = R._task_plan(self.api, meta["id"], "compact-plan")
        self.apply("compact", plan)
        script = Path(__file__).with_name("ag.py")
        def command(*args):
            return subprocess.run([sys.executable, str(script), *args], env=dict(os.environ), text=True,
                                  capture_output=True, timeout=30)
        listing = command("task", "list", "--archive", "--session", "new-session", "--agent", "coder")
        self.assertEqual(listing.returncode, 0, listing.stderr)
        self.assertEqual(json.loads(listing.stdout)["items"][0]["task_id"], meta["id"])
        reopened = command("task", "reopen", "--id", meta["id"], "--session", "new-session", "--agent", "coder",
                           "--expected-revision", "2")
        self.assertEqual(reopened.returncode, 0, reopened.stderr + reopened.stdout)
        resumed = command("task", "resume", "--id", meta["id"], "--session", "new-session", "--agent", "coder")
        self.assertEqual(resumed.returncode, 0, resumed.stderr)
        self.assertEqual(json.loads(resumed.stdout)["context"], context)
        status = command("history", "status")
        self.assertEqual(status.returncode, 0, status.stderr)
        self.assertTrue(json.loads(status.stdout)["complete"])


if __name__ == "__main__":
    unittest.main()
