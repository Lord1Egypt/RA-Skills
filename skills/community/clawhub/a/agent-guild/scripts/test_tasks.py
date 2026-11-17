#!/usr/bin/env python3
"""任务包隔离回归；所有运行时数据只写入临时目录。"""

import copy
import hashlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
import types
import unittest
from contextlib import contextmanager, redirect_stderr, redirect_stdout
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
from unittest import mock

import ag_tasks


SCRIPTS = Path(__file__).resolve().parent


class TaskTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="ag-task-test-")
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name).resolve()
        self.root = self.base / "guild"
        self.root.mkdir()
        self.environment = mock.patch.dict(os.environ, {
            "AGENT_GUILD_DIR": str(self.root), "AG_HOST_ID": "test-host", "PYTHONDONTWRITEBYTECODE": "1",
        })
        self.environment.start()
        self.addCleanup(self.environment.stop)
        spec = importlib.util.spec_from_file_location("ag_task_test_api", str(SCRIPTS / "ag.py"))
        self.api = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.api)
        self.capacity = mock.Mock()
        self.history = mock.patch.dict(sys.modules, {
            "ag_history": types.SimpleNamespace(ensure_capacity=self.capacity,
                                                budget_lock=lambda api: api._append_lock(api.CENTRAL / "history-budget")),
        })
        self.history.start()
        self.addCleanup(self.history.stop)

    def invoke(self, command, *options, session="session-one", agent="alpha", context="", expected=0):
        output = io.StringIO()
        errors = io.StringIO()
        with mock.patch.object(sys, "stdin", io.StringIO(context)), redirect_stdout(output), redirect_stderr(errors):
            code = ag_tasks.run([command, "--session", session, "--agent", agent, *map(str, options)], self.api)
        self.assertEqual(code, expected, output.getvalue() + errors.getvalue())
        value = json.loads(output.getvalue())
        self.assertEqual(value["ok"], expected == 0)
        self.assertEqual(bool(errors.getvalue()), expected != 0)
        return value

    def create(self, title="中文任务一", context="仅此任务完整私有上下文", **kwargs):
        return self.invoke("create", "--title", title, "--project", "项目甲", context=context, **kwargs)

    def task_options(self, value):
        return ["--id", value["task"]["task_id"], "--expected-revision", value["task"]["revision"]]

    def tree(self):
        return {str(path.relative_to(self.root)): path.read_bytes()
                for path in self.root.rglob("*") if path.is_file()}

    def meta(self, result):
        return json.loads((Path(result["package"]) / "meta.json").read_text(encoding="utf-8"))

    def rewrite_meta(self, result, data):
        (Path(result["package"]) / "meta.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    def test_two_sessions_explicit_selection_and_many_tasks(self):
        first = self.create(context="上下文A")
        second = self.create(title="任务二", context="上下文B")
        listing = self.invoke("list")
        self.assertEqual(len(listing["items"]), 2)
        number = next(item["number"] for item in listing["items"] if item["task_id"] == first["task"]["task_id"])
        resumed = self.invoke("resume", "--list", listing["list_id"], "--number", number)
        self.assertEqual(resumed["context"], "上下文A")
        self.assertNotIn("上下文B", json.dumps(resumed, ensure_ascii=False))
        released = self.invoke("release", *self.task_options(first))
        other = self.invoke("resume", "--id", first["task"]["task_id"], session="session-two", agent="beta")
        self.assertEqual(other["context"], "上下文A")
        self.assertEqual(other["task"]["revision"], released["task"]["revision"] + 1)
        self.assertEqual(len(other["task"]["sessions"]), 2)
        self.assertEqual(self.meta(second)["owners"][0]["session"], "session-one")

    def test_list_reads_only_metadata_even_if_bodies_unreadable(self):
        first = self.create()
        self.create(title="另一个任务", context="禁止偷读的正文")
        original = ag_tasks._read_bytes
        opened = []

        def guarded(path, limit=None):
            opened.append(str(path))
            if path.name in ("context.md", "manifest.json") or "artifacts" in path.parts:
                raise AssertionError("list 不得读取上下文或附件")
            return original(path, limit)

        with mock.patch.object(ag_tasks, "_read_bytes", side_effect=guarded):
            listing = self.invoke("list", session="browser-session", agent="browser")
        self.assertEqual(len(listing["items"]), 2)
        self.assertNotIn("完整私有上下文", json.dumps(listing, ensure_ascii=False))
        self.assertNotIn("禁止偷读", json.dumps(listing, ensure_ascii=False))
        self.assertEqual(listing["items"][0]["summary"], "")
        self.assertTrue(any(path.endswith("meta.json") for path in opened))
        self.assertNotIn("context.md", str(listing))
        self.assertTrue(Path(first["package"]).is_dir())

    def test_list_replaced_and_selected_revision_changed(self):
        first = self.create()
        old = self.invoke("list")
        latest = self.invoke("list")
        error = self.invoke("resume", "--list", old["list_id"], "--number", 1, expected=1)
        self.assertEqual(error["error"], "stale_list")
        changed = self.invoke("checkpoint", *self.task_options(first), context="新的完整上下文")
        error = self.invoke("resume", "--list", latest["list_id"], "--number", 1, expected=1)
        self.assertEqual(error["error"], "stale_list")
        self.assertNotIn("context", error)
        current = self.invoke("resume", "--id", first["task"]["task_id"])
        self.assertEqual(current["context"], "新的完整上下文")
        self.assertEqual(current["task"]["revision"], changed["task"]["revision"])
        self.assertIsNotNone(json.loads((self.root / "hosts/test-host/task-sessions/session-one.json").read_text())["list"])
        self.assertEqual(len(list((self.root / "hosts/test-host/task-sessions").iterdir())), 1)

    def test_busy_handover_and_collaboration_cas(self):
        first = self.create()
        error = self.invoke("resume", "--id", first["task"]["task_id"], session="session-two", agent="beta", expected=1)
        self.assertEqual(error["error"], "busy")
        self.assertNotIn("context", error)
        joined = self.invoke("resume", "--id", first["task"]["task_id"], "--collaborate", session="session-two", agent="beta")
        self.assertEqual(len(joined["task"]["owners"]), 2)
        updated = self.invoke("checkpoint", *self.task_options(joined), context="甲的协作上下文")
        conflict = self.invoke("checkpoint", *self.task_options(joined), session="session-two", agent="beta", context="过期写入", expected=1)
        self.assertEqual(conflict["error"], "revision_conflict")
        taken = self.invoke("resume", "--id", first["task"]["task_id"], "--handover", session="session-two", agent="beta")
        self.assertEqual(taken["context"], "甲的协作上下文")
        self.assertEqual(len(taken["task"]["owners"]), 1)
        denied = self.invoke("checkpoint", *self.task_options(taken), context="被接管的旧主人", expected=1)
        self.assertEqual(denied["error"], "not_owner")
        self.assertGreater(taken["task"]["revision"], updated["task"]["revision"])

    def test_close_reopen_whole_package_and_evidence(self):
        first = self.create()
        attachment = self.base / "中文结果.txt"
        attachment.write_text("证据内容", encoding="utf-8")
        attached = self.invoke("attach", *self.task_options(first), "--file", attachment)
        source_bytes = attachment.read_bytes()
        closed = self.invoke("close", *self.task_options(attached), "--evidence", "已通过验收")
        self.assertEqual(closed["task"]["location"], "archive")
        self.assertFalse(Path(first["package"]).exists())
        self.assertEqual(self.invoke("list")["items"], [])
        self.assertEqual(len(self.invoke("list", "--archive")["items"]), 1)
        self.assertEqual(self.meta(closed)["closure"]["evidence"], "已通过验收")
        reopened = self.invoke("reopen", *self.task_options(closed), session="session-two", agent="beta")
        self.assertEqual(Path(reopened["package"]).name, Path(first["package"]).name)
        resumed = self.invoke("resume", "--id", first["task"]["task_id"], session="session-two", agent="beta")
        self.assertEqual(len(resumed["artifacts"]), 1)
        self.assertEqual(attachment.read_bytes(), source_bytes)
        self.assertEqual(resumed["context"], "仅此任务完整私有上下文")

    def test_checkpoint_retitle_preserves_id_directory_and_snapshots(self):
        first = self.create(title="中文 名称 / 二十字以上的字符绝对不能成为路径穿越..")
        package = Path(first["package"])
        self.assertLessEqual(len(package.name.split("-", 2)[2]), 20)
        self.assertTrue(first["task"]["task_id"].startswith(datetime.now().strftime("%Y%m%d") + "-"))
        old = self.meta(first)
        changed = self.invoke("checkpoint", *self.task_options(first), "--title", "已经改名", "--summary", "显式摘要", "--status", "waiting", context="当前完整上下文")
        self.assertEqual(changed["package"], first["package"])
        self.assertEqual(changed["task"]["task_id"], first["task"]["task_id"])
        self.assertEqual(changed["task"]["status"], "waiting")
        self.assertEqual((package / "snapshots" / old["snapshot"] / "context.md").read_text(), "仅此任务完整私有上下文")
        self.assertEqual(len(list((package / "snapshots").iterdir())), 2)
        self.assertFalse((package / "context.md").exists())
        self.assertEqual(self.invoke("list")["items"][0]["summary"], "显式摘要")

    def test_attachment_copy_hash_no_source_path_and_never_execute(self):
        first = self.create()
        marker = self.base / "must-not-exist"
        script = self.base / "payload.py"
        script.write_text("from pathlib import Path\nPath(" + repr(str(marker)) + ").write_text('bad')\n", encoding="utf-8")
        script.chmod(0o755)
        before = script.read_bytes()
        attached = self.invoke("attach", *self.task_options(first), "--file", script)
        resumed = self.invoke("resume", "--id", first["task"]["task_id"])
        item = resumed["artifacts"][0]
        self.assertEqual(item["sha256"], hashlib.sha256(before).hexdigest())
        self.assertEqual(item["size"], len(before))
        self.assertEqual((Path(attached["package"]) / item["path"]).read_bytes(), before)
        self.assertEqual((Path(attached["package"]) / item["path"]).stat().st_mode & 0o111, 0)
        for path in Path(attached["package"]).rglob("*.json"):
            self.assertNotIn(str(script), path.read_text())
        self.assertFalse(marker.exists())
        self.assertEqual(script.read_bytes(), before)

    def test_invalid_ids_session_agent_arguments_and_empty_context(self):
        first = self.create()
        for task_id in ("../escape", first["task"]["task_id"] + "/context.md", "20261350-0123456789ab", "", "abcdef"):
            with self.subTest(task_id=task_id):
                self.invoke("resume", "--id", task_id, expected=1)
        for session, agent in (("../escape", "alpha"), ("", "alpha"), ("alpha", "alpha"), ("safe", "a/b"), ("safe", "")):
            with self.subTest(session=session, agent=agent):
                self.invoke("list", session=session, agent=agent, expected=1)
        self.invoke("resume", expected=2)
        self.invoke("resume", "--id", first["task"]["task_id"], "--number", 1, expected=1)
        self.invoke("create", "--title", "空", "--project", "项目", expected=1)
        self.invoke("list", agent="other-agent", expected=1)
        self.invoke("checkpoint", *self.task_options(first), "--expected-revision", 0, context="新", expected=1)

    def test_symlink_and_hardlink_sources_rejected(self):
        first = self.create()
        source = self.base / "source.txt"
        source.write_text("不可通过链接复制")
        link = self.base / "link.txt"
        link.symlink_to(source)
        self.invoke("attach", *self.task_options(first), "--file", link, expected=1)
        hard = self.base / "hard.txt"
        os.link(str(source), str(hard))
        self.invoke("attach", *self.task_options(first), "--file", hard, expected=1)
        self.invoke("attach", *self.task_options(first), "--file", "relative.txt", expected=1)
        self.invoke("attach", *self.task_options(first), "--file", source, "--name", "../bad", expected=1)
        directory_link = self.base / "linked-dir"
        directory_link.symlink_to(self.base, target_is_directory=True)
        self.invoke("attach", *self.task_options(first), "--file", directory_link / "source.txt", expected=1)

    def test_symlink_metadata_package_session_lock_and_context(self):
        first = self.create()
        package = Path(first["package"])
        meta = self.meta(first)
        context = package / "snapshots" / meta["snapshot"] / "context.md"
        external = self.base / "outside.txt"
        external.write_text("外部内容")
        context.unlink()
        context.symlink_to(external)
        self.invoke("list")
        self.invoke("resume", "--id", first["task"]["task_id"], expected=1)
        context.unlink()
        context.write_text("仅此任务完整私有上下文")
        metadata = package / "meta.json"
        saved = metadata.read_bytes()
        metadata.unlink()
        metadata.symlink_to(external)
        self.invoke("list", expected=1)
        metadata.unlink()
        metadata.write_bytes(saved)
        bogus = self.root / "handoff/active" / ("20261019-aaaaaaaaaaaa-外链")
        bogus.symlink_to(package, target_is_directory=True)
        self.invoke("list", expected=1)
        bogus.unlink()
        session = self.root / "hosts/test-host/task-sessions/session-two.json"
        session.symlink_to(external)
        self.invoke("list", session="session-two", agent="beta", expected=1)
        session.unlink()
        lock = self.root / ".handoff.ag-lock"
        lock.unlink()
        lock.symlink_to(external)
        self.invoke("list", expected=1)
        self.assertEqual(external.read_text(), "外部内容")

    def test_corrupt_metadata_fail_closed_and_no_context_leak(self):
        first = self.create()
        original = self.meta(first)
        variants = []
        for key, value in (("revision", True), ("schema_version", True), ("snapshot", "../outside"),
                           ("sessions", {}), ("owners", ["bad"]), ("title", 123),
                           ("closure", {"evidence": "forged"}), ("status", "unknown")):
            data = copy.deepcopy(original)
            data[key] = value
            variants.append(data)
        extra = copy.deepcopy(original)
        extra["unexpected"] = "bad"
        variants.append(extra)
        for data in variants:
            with self.subTest(data=data):
                self.rewrite_meta(first, data)
                error = self.invoke("resume", "--id", first["task"]["task_id"], expected=1)
                self.assertNotIn("context", error)
                self.invoke("list", expected=1)
        path = Path(first["package"]) / "meta.json"
        path.write_text('{"schema_version": 1, "schema_version": 1}')
        self.invoke("list", expected=1)
        path.write_text("{")
        self.invoke("list", expected=1)
        self.rewrite_meta(first, original)
        self.invoke("list")

    def test_corrupt_context_manifest_attachment_fail_closed(self):
        first = self.create()
        package = Path(first["package"])
        metadata = self.meta(first)
        context = package / "snapshots" / metadata["snapshot"] / "context.md"
        context.write_text("损坏的正文")
        error = self.invoke("resume", "--id", first["task"]["task_id"], expected=1)
        self.assertEqual(error["error"], "integrity_error")
        self.assertNotIn("损坏的正文", str(error))
        context.write_text("仅此任务完整私有上下文")
        manifest_path = context.parent / "manifest.json"
        manifest = json.loads(manifest_path.read_text())
        bad = copy.deepcopy(manifest)
        bad["artifacts"] = [{"name": "x", "path": "../../escape", "size": 1, "sha256": "a" * 64}]
        manifest_path.write_text(json.dumps(bad))
        self.invoke("resume", "--id", first["task"]["task_id"], expected=1)
        manifest_path.write_text(json.dumps(manifest))
        self.invoke("resume", "--id", first["task"]["task_id"])

    def test_cas_rejection_does_not_change_any_bytes(self):
        first = self.create()
        changed = self.invoke("checkpoint", *self.task_options(first), context="第二版")
        original = self.tree()
        for command, extra in (("checkpoint", []), ("attach", ["--file", self.base / "not-there"]),
                               ("release", []), ("close", ["--evidence", "过期关闭"]), ("reopen", [])):
            with self.subTest(command=command):
                error = self.invoke(command, *self.task_options(first), *extra, context="失败的写入", expected=1)
                self.assertEqual(error["error"], "revision_conflict")
                self.assertEqual(original, self.tree())
        self.assertEqual(self.meta(changed)["revision"], 2)

    def test_capacity_checks_are_before_writes(self):
        first = self.create()
        self.assertGreater(self.capacity.call_args.kwargs["additional_bytes"], 0)
        before = self.tree()
        self.capacity.side_effect = ValueError("容量不足")
        for command, options, context in (("checkpoint", self.task_options(first), "新上下文"),
                                          ("close", self.task_options(first) + ["--evidence", "已完成"], ""),
                                          ("create", ["--title", "未创建", "--project", "项目"], "新任务")):
            with self.subTest(command=command):
                error = self.invoke(command, *options, context=context, expected=1)
                self.assertEqual(error["error"], "capacity_exceeded")
                self.assertEqual(self.tree(), before)

    def test_snapshot_publish_failure_keeps_old_context_authoritative(self):
        first = self.create(context="提交前")
        original = self.api.atomic_write_json

        def fail_meta(path, value):
            if path.name == "meta.json":
                raise OSError("模拟原子发布失败")
            return original(path, value)

        with mock.patch.object(self.api, "atomic_write_json", side_effect=fail_meta):
            self.invoke("checkpoint", *self.task_options(first), context="尚未发布", expected=1)
        resumed = self.invoke("resume", "--id", first["task"]["task_id"])
        self.assertEqual(resumed["context"], "提交前")
        self.assertEqual(resumed["task"]["revision"], 1)
        successful = self.invoke("checkpoint", *self.task_options(first), context="成功的新版本")
        self.assertEqual(successful["task"]["revision"], 2)
        self.assertEqual(self.invoke("resume", "--id", first["task"]["task_id"])["context"], "成功的新版本")

    def test_archive_metadata_failure_recovered_on_next_command(self):
        first = self.create()
        original = self.api.atomic_write_json

        def fail_archive_meta(path, value):
            if path.name == "meta.json" and "archive" in path.parts:
                raise OSError("模拟移动后元数据发布失败")
            return original(path, value)

        with mock.patch.object(self.api, "atomic_write_json", side_effect=fail_archive_meta):
            error = self.invoke("close", *self.task_options(first), "--evidence", "验证完成", expected=1)
        self.assertEqual(error["error"], "transaction_pending")
        self.assertFalse(Path(first["package"]).exists())
        listing = self.invoke("list", "--archive")
        self.assertEqual(listing["items"][0]["status"], "closed")
        self.assertEqual(listing["recovered"], [first["task"]["task_id"]])
        package = self.root / "handoff/archive" / Path(first["package"]).name
        self.assertFalse((package / ".transition.json").exists())
        self.invoke("reopen", "--id", first["task"]["task_id"], "--expected-revision", 2)

    def test_reopen_rename_failure_recovers_with_owner(self):
        first = self.create()
        closed = self.invoke("close", *self.task_options(first), "--evidence", "验收完成")
        with mock.patch.object(ag_tasks.os, "rename", side_effect=OSError("模拟移动失败")):
            error = self.invoke("reopen", *self.task_options(closed), session="session-two", agent="beta", expected=1)
        self.assertEqual(error["error"], "transaction_pending")
        listing = self.invoke("list", session="session-two", agent="beta")
        self.assertEqual(listing["items"][0]["owners"][0]["session"], "session-two")
        self.assertEqual(listing["recovered"], [first["task"]["task_id"]])
        self.assertFalse(Path(closed["package"]).exists())

    def test_parallel_checkpoint_exactly_one_cas_winner(self):
        first = self.create()
        worker = (
            "import sys; "
            "sys.path.insert(0, sys.argv.pop(1)); "
            "import ag, ag_tasks; "
            "raise SystemExit(ag_tasks.run(sys.argv[1:], ag))"
        )
        arguments = [sys.executable, "-c", worker, str(SCRIPTS), "checkpoint",
                     "--session", "session-one", "--agent", "alpha", *map(str, self.task_options(first))]
        processes = [subprocess.Popen(arguments, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                      text=True, env=dict(os.environ)) for _ in range(2)]
        results = []
        with ThreadPoolExecutor(max_workers=2) as workers:
            pending = [workers.submit(process.communicate, "并发上下文" + str(number), timeout=30)
                       for number, process in enumerate(processes)]
            for process, future in zip(processes, pending):
                out, err = future.result()
                results.append((process.returncode, json.loads(out), err))
        self.assertEqual(sorted(item[0] for item in results), [0, 1])
        loser = next(item[1] for item in results if item[0] == 1)
        self.assertEqual(loser["error"], "revision_conflict")
        resumed = self.invoke("resume", "--id", first["task"]["task_id"])
        self.assertEqual(resumed["task"]["revision"], 2)
        self.assertIn(resumed["context"], ("并发上下文0", "并发上下文1"))
        self.assertEqual(len(list((Path(first["package"]) / "snapshots").iterdir())), 2)

    def test_id_collision_checks_active_and_archive(self):
        with mock.patch.object(ag_tasks.secrets, "token_hex", return_value="a" * 12):
            first = self.create()
        closed = self.invoke("close", *self.task_options(first), "--evidence", "已完成")
        with mock.patch.object(ag_tasks.secrets, "token_hex", return_value="a" * 12):
            error = self.create(title="不同标题", expected=1)
        self.assertEqual(error["error"], "id_collision")
        self.assertTrue(Path(closed["package"]).is_dir())

    def test_references_pin_hold_update_preserve_and_clear(self):
        first = self.create()
        second = self.create(title="被引用任务")
        third = self.create(title="新增引用任务")
        self.assertEqual(self.meta(first)["references"], [])
        self.assertIs(self.meta(first)["pin"], False)
        self.assertIs(self.meta(first)["hold"], False)
        updated = self.invoke("checkpoint", *self.task_options(first), "--ref", second["task"]["task_id"],
                              "--ref", second["task"]["task_id"], "--pin", "--hold", context="包含显式引用")
        self.assertEqual(updated["task"]["references"], [second["task"]["task_id"]])
        self.assertTrue(updated["task"]["pin"])
        self.assertTrue(updated["task"]["hold"])
        preserved = self.invoke("checkpoint", *self.task_options(updated), context="正文并不自动改引用")
        self.assertEqual(preserved["task"]["references"], updated["task"]["references"])
        self.assertTrue(preserved["task"]["hold"])
        appended = self.invoke("checkpoint", *self.task_options(preserved), "--ref", third["task"]["task_id"], context="两个引用")
        self.assertEqual(appended["task"]["references"], [second["task"]["task_id"], third["task"]["task_id"]])
        replaced = self.invoke("checkpoint", *self.task_options(appended), "--clear-refs", "--ref", third["task"]["task_id"],
                               "--unpin", "--unhold", context="明确替换")
        self.assertEqual(replaced["task"]["references"], [third["task"]["task_id"]])
        self.assertFalse(replaced["task"]["pin"])
        self.assertFalse(replaced["task"]["hold"])
        cleared = self.invoke("checkpoint", *self.task_options(replaced), "--clear-refs", context="明确清空")
        self.assertEqual(cleared["task"]["references"], [])

    def test_invalid_references_flags_and_metadata_fail_closed(self):
        first = self.create()
        before = self.tree()
        for reference in (first["task"]["task_id"], "../../escape", "20260101-000000000000"):
            self.invoke("checkpoint", *self.task_options(first), "--ref", reference, context="不应提交", expected=1)
            self.assertEqual(self.tree(), before)
        self.invoke("checkpoint", *self.task_options(first), "--pin", "--unpin", context="不应提交", expected=2)
        self.invoke("checkpoint", *self.task_options(first), "--hold", "--unhold", context="不应提交", expected=2)
        original = self.meta(first)
        for key, value in (("references", {}), ("references", ["../escape"]), ("pin", 1), ("hold", "false")):
            corrupted = copy.deepcopy(original)
            corrupted[key] = value
            self.rewrite_meta(first, corrupted)
            self.invoke("list", expected=1)
        self.rewrite_meta(first, original)

    def test_all_bookkeeping_writes_obey_capacity_before_mutation(self):
        first = self.create()
        before = self.tree()
        self.capacity.side_effect = ValueError("容量已满")
        self.invoke("list", expected=1)
        self.assertEqual(self.tree(), before)
        self.invoke("resume", "--id", first["task"]["task_id"], "--handover", session="session-two", agent="beta", expected=1)
        self.assertEqual(self.tree(), before)
        self.invoke("release", *self.task_options(first), expected=1)
        self.assertEqual(self.tree(), before)
        self.invoke("resume", "--id", first["task"]["task_id"])
        self.capacity.side_effect = None
        closed = self.invoke("close", *self.task_options(first), "--evidence", "完成")
        before = self.tree()
        self.capacity.side_effect = RuntimeError("容量已满")
        self.invoke("reopen", *self.task_options(closed), session="session-two", agent="beta", expected=1)
        self.assertEqual(self.tree(), before)

    def test_task_then_budget_lock_covers_capacity_and_writes(self):
        events = []
        held = []
        original_lock = self.api._append_lock
        original_write = self.api.atomic_write_json

        @contextmanager
        def tracked_lock(path):
            events.append(("enter", path.name))
            with original_lock(path):
                held.append(path.name)
                try:
                    yield
                finally:
                    held.pop()
                    events.append(("exit", path.name))

        def guarded_capacity(api, additional_bytes):
            self.assertEqual(held, ["handoff", "history-budget"])
            self.assertGreater(additional_bytes, 0)
            events.append(("capacity", additional_bytes))

        def guarded_write(path, data):
            self.assertEqual(held, ["handoff", "history-budget"])
            events.append(("write", path.name))
            return original_write(path, data)

        self.capacity.side_effect = guarded_capacity
        with mock.patch.object(self.api, "_append_lock", side_effect=tracked_lock), \
                mock.patch.object(self.api, "atomic_write_json", side_effect=guarded_write):
            first = self.create()
            self.invoke("list")
            self.invoke("checkpoint", *self.task_options(first), context="双锁覆盖检查点")
        self.assertEqual(events[:2], [("enter", "handoff"), ("enter", "history-budget")])
        self.assertEqual(events[-2:], [("exit", "history-budget"), ("exit", "handoff")])
        self.assertLess(next(i for i, event in enumerate(events) if event[0] == "capacity"),
                        next(i for i, event in enumerate(events) if event[0] == "write"))

    def test_real_history_full_lifecycle_and_session_accounting(self):
        self.history.stop()
        import ag_history
        first = self.create(context="真实历史联调初始上下文")
        listing = self.invoke("list")
        resumed = self.invoke("resume", "--list", listing["list_id"], "--number", 1)
        self.assertEqual(resumed["context"], "真实历史联调初始上下文")
        taken = self.invoke("resume", "--id", first["task"]["task_id"], "--handover", session="session-two", agent="beta")
        checkpoint = self.invoke("checkpoint", *self.task_options(taken), "--pin", "--hold", context="真实历史联调新版上下文", session="session-two", agent="beta")
        source = self.base / "report.txt"
        source.write_text("完整附件")
        attached = self.invoke("attach", *self.task_options(checkpoint), "--file", source, session="session-two", agent="beta")
        report = ag_history.report(self.api)
        self.assertTrue(report["complete"], report)
        self.assertTrue(report["references_complete"], report)
        self.assertGreater(report["total_bytes"], 0)
        session_bytes = sum(path.stat().st_size for path in (self.root / "hosts").rglob("task-sessions/*.json"))
        self.assertGreater(session_bytes, 0)
        closed = self.invoke("close", *self.task_options(attached), "--evidence", "真实模块验证完成", session="session-two", agent="beta")
        closed_report = ag_history.report(self.api)
        self.assertTrue(closed_report["complete"], closed_report)
        self.assertTrue(closed_report["references_complete"], closed_report)
        self.assertGreater(closed_report["total_bytes"], report["total_bytes"])
        reopened = self.invoke("reopen", *self.task_options(closed), session="session-two", agent="beta")
        final = self.invoke("resume", "--id", first["task"]["task_id"], session="session-two", agent="beta")
        self.assertEqual(final["context"], "真实历史联调新版上下文")
        self.assertEqual((Path(final["package"]) / final["artifacts"][0]["path"]).read_text(), "完整附件")
        self.assertEqual(final["task"]["revision"], reopened["task"]["revision"])
        self.assertGreaterEqual(report["total_bytes"], session_bytes)

    def test_real_history_budget_blocks_sessions_and_all_changes(self):
        self.history.stop()
        import ag_history
        first = self.create()
        current = ag_history.report(self.api)["total_bytes"]
        (self.root / "RETENTION.md").write_text(
            "history_max_bytes = " + str(max(current, 1)) + "\nhistory_target_bytes = 0\n", encoding="utf-8")
        before = self.tree()
        for command, options, context in (
                ("list", [], ""),
                ("release", self.task_options(first), ""),
                ("checkpoint", self.task_options(first), "无法写入的新上下文"),
                ("close", self.task_options(first) + ["--evidence", "无法归档"], "")):
            error = self.invoke(command, *options, context=context, expected=1)
            self.assertEqual(error["error"], "capacity_exceeded")
            self.assertEqual(self.tree(), before)
        error = self.invoke("list", session="new-session", agent="new-agent", expected=1)
        self.assertEqual(error["error"], "capacity_exceeded")
        self.assertEqual(self.tree(), before)
        self.assertFalse((Path(first["package"]) / ".transition.json").exists())

    def test_real_history_reference_and_retention_flags_are_recognized(self):
        self.history.stop()
        import ag_history
        first = self.create(title="引用任务")
        second = self.create(title="保留任务")
        protected = self.invoke("checkpoint", *self.task_options(second), "--hold", "--pin", context="应保留历史")
        referenced = self.invoke("checkpoint", *self.task_options(first), "--ref", second["task"]["task_id"], context="显式引用另一任务")
        closed = self.invoke("close", *self.task_options(protected), "--evidence", "封闭但保留")
        inventory = ag_history._Inventory(self.api)
        self.assertEqual(inventory.reference_error_count, 0)
        task = inventory.tasks[second["task"]["task_id"]]
        self.assertTrue(task["held"])
        self.assertTrue(inventory.task_referenced(task))
        self.assertTrue(all(inventory.protected(row) for row in inventory.files if row["task_id"] == task["id"]))
        self.assertEqual(self.meta(referenced)["references"], [closed["task"]["task_id"]])

    def test_recovery_rechecks_budget_after_interrupted_close(self):
        self.history.stop()
        import ag_history
        first = self.create()
        with mock.patch.object(ag_tasks.os, "rename", side_effect=OSError("模拟归档前崩溃")):
            pending = self.invoke("close", *self.task_options(first), "--evidence", "已完成", expected=1)
        self.assertEqual(pending["error"], "transaction_pending")
        package = Path(first["package"])
        self.assertTrue((package / ".transition.json").exists())
        used = ag_history.report(self.api)["total_bytes"]
        config = self.root / "RETENTION.md"
        config.write_text("history_max_bytes = " + str(max(used, 1)) + "\nhistory_target_bytes = 0\n")
        before = self.tree()
        error = self.invoke("list", expected=1)
        self.assertEqual(error["error"], "capacity_exceeded")
        self.assertEqual(self.tree(), before)
        self.assertTrue(package.is_dir())
        config.write_text("history_max_bytes = 1073741824\nhistory_target_bytes = 0\n")
        recovered = self.invoke("list", "--archive")
        self.assertEqual(recovered["recovered"], [first["task"]["task_id"]])
        self.assertEqual(recovered["items"][0]["status"], "closed")

    def test_real_reopen_metadata_failure_recovers_without_budget_deadlock(self):
        self.history.stop()
        first = self.create()
        closed = self.invoke("close", *self.task_options(first), "--evidence", "已封闭")
        original_write = self.api.atomic_write_json

        def fail_reopened_meta(path, data):
            if path.name == "meta.json" and "active" in path.parts:
                raise OSError("模拟重开移动后元数据发布失败")
            return original_write(path, data)

        with mock.patch.object(self.api, "atomic_write_json", side_effect=fail_reopened_meta):
            pending = self.invoke("reopen", *self.task_options(closed), expected=1)
        self.assertEqual(pending["error"], "transaction_pending")
        listed = self.invoke("list")
        self.assertEqual(listed["recovered"], [first["task"]["task_id"]])
        self.assertEqual(listed["items"][0]["status"], "active")
        resumed = self.invoke("resume", "--list", listed["list_id"], "--number", 1)
        self.assertEqual(resumed["context"], "仅此任务完整私有上下文")

    def test_real_budget_list_never_opens_context_or_attachment_bodies(self):
        self.history.stop()
        import ag_history
        first = self.create(context="任务一正文不可列单读取")
        second = self.create(title="另一个任务", context="任务二正文不可列单读取")
        source = self.base / "attachment.txt"
        source.write_text("附件内容不可列单读取")
        attached = self.invoke("attach", *self.task_options(first), "--file", source)
        original_read = ag_tasks._read_bytes
        original_open = ag_history._open_file

        def guard_task(path, limit=None):
            self.assertNotEqual(path.name, "context.md")
            self.assertNotIn("artifacts", path.parts)
            return original_read(path, limit)

        @contextmanager
        def guard_history(root, rel, expected=None):
            self.assertNotEqual(Path(rel).name, "context.md")
            self.assertNotIn("artifacts", Path(rel).parts)
            with original_open(root, rel, expected) as stream:
                yield stream

        with mock.patch.object(ag_tasks, "_read_bytes", side_effect=guard_task), \
                mock.patch.object(ag_history, "_open_file", side_effect=guard_history):
            listed = self.invoke("list")
        self.assertEqual(len(listed["items"]), 2)
        self.assertNotIn("不可列单读取", json.dumps(listed, ensure_ascii=False))
        self.assertEqual(self.meta(attached)["revision"], 2)
        self.assertEqual(self.meta(second)["revision"], 1)

    def test_independent_processes_cannot_overcommit_shared_budget(self):
        self.history.stop()
        import ag_history
        first = self.create(context="a" * 10000)
        second = self.create(title="并行的另一任务", context="b" * 10000, session="session-two", agent="beta")
        size = 20000
        snapshot = self.meta(first)["snapshot"]
        manifest = json.loads((Path(first["package"]) / "snapshots" / snapshot / "manifest.json").read_text())
        reserve = 10000 + size + 2 * ag_tasks._json_size(manifest) + ag_tasks._json_size(self.meta(first))
        maximum = ag_history.report(self.api)["total_bytes"] + reserve + 2000
        (self.root / "RETENTION.md").write_text(
            "history_max_bytes = " + str(maximum) + "\nhistory_target_bytes = 0\n")
        worker = "import sys; sys.path.insert(0, sys.argv.pop(1)); import ag, ag_tasks; raise SystemExit(ag_tasks.run(sys.argv[1:], ag))"
        processes = []
        for task, session, agent in ((first, "session-one", "alpha"), (second, "session-two", "beta")):
            arguments = [sys.executable, "-c", worker, str(SCRIPTS), "checkpoint", "--session", session,
                         "--agent", agent, *map(str, self.task_options(task))]
            processes.append(subprocess.Popen(arguments, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                               stderr=subprocess.PIPE, text=True, env=dict(os.environ)))
        results = []
        with ThreadPoolExecutor(max_workers=2) as workers:
            pending = [workers.submit(process.communicate, "x" * size, timeout=30) for process in processes]
            for process, future in zip(processes, pending):
                out, err = future.result()
                results.append((process.returncode, json.loads(out), err))
        self.assertEqual(sorted(item[0] for item in results), [0, 1], results)
        self.assertEqual(next(item[1] for item in results if item[0] == 1)["error"], "capacity_exceeded")
        self.assertLessEqual(ag_history.report(self.api)["total_bytes"], maximum)
        self.assertEqual(sorted([self.meta(first)["revision"], self.meta(second)["revision"]]), [1, 2])

    def test_different_hosts_with_same_session_are_distinct_owners(self):
        first = self.create()
        with mock.patch.object(self.api, "host_id", return_value="other-host"):
            error = self.invoke("resume", "--id", first["task"]["task_id"], expected=1)
            self.assertEqual(error["error"], "busy")
            resumed = self.invoke("resume", "--id", first["task"]["task_id"], "--collaborate")
            self.assertEqual({item["host"] for item in resumed["task"]["owners"]}, {"test-host", "other-host"})
            self.assertTrue((self.root / "hosts/other-host/task-sessions/session-one.json").is_file())

    def test_attachment_corruption_and_duplicate_name_are_rejected(self):
        first = self.create()
        source = self.base / "evidence.txt"
        source.write_text("内容")
        attached = self.invoke("attach", *self.task_options(first), "--file", source)
        error = self.invoke("attach", *self.task_options(attached), "--file", source, expected=1)
        self.assertEqual(error["error"], "attachment_exists")
        self.invoke("attach", *self.task_options(attached), "--file", source, "--name", "EVIDENCE.TXT", expected=1)
        artifact = next((Path(first["package"]) / "artifacts").iterdir())
        artifact.write_text("篡改")
        error = self.invoke("resume", "--id", first["task"]["task_id"], expected=1)
        self.assertEqual(error["error"], "integrity_error")
        self.assertNotIn("context", error)

    def test_failed_snapshot_is_safe_during_an_unfinished_revision(self):
        first = self.create(context="稳定的上下文")
        original = ag_tasks._write_bytes

        def fail_snapshot(path, value):
            if path.name == "context.md":
                raise OSError("模拟正文落盘失败")
            return original(path, value)

        with mock.patch.object(ag_tasks, "_write_bytes", side_effect=fail_snapshot):
            self.invoke("checkpoint", *self.task_options(first), context="未落盘上下文", expected=1)
        resumed = self.invoke("resume", "--id", first["task"]["task_id"])
        self.assertEqual(resumed["context"], "稳定的上下文")
        self.assertEqual(resumed["task"]["revision"], 1)

    def test_session_snapshot_and_metadata_paths_cannot_escape(self):
        first = self.create()
        listing = self.invoke("list")
        state = self.root / "hosts/test-host/task-sessions/session-one.json"
        value = json.loads(state.read_text())
        value["list"]["items"][0]["task_id"] = "../../outside"
        state.write_text(json.dumps(value))
        error = self.invoke("resume", "--list", listing["list_id"], "--number", 1, expected=1)
        self.assertNotIn("context", error)
        self.assertEqual(self.meta(first)["revision"], 1)

    def test_unreadable_metadata_is_not_treated_as_empty(self):
        first = self.create()
        metadata = Path(first["package"]) / "meta.json"
        metadata.chmod(0)
        try:
            error = self.invoke("list", expected=1)
            self.assertEqual(error["error"], "permission_denied")
        finally:
            metadata.chmod(0o600)


if __name__ == "__main__":
    unittest.main(verbosity=2)
