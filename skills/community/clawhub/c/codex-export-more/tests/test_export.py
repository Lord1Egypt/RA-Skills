"""Regression tests for scripts/export.py.

Run from the repository root:
    python -m unittest discover -s tests -v
"""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import export as ex

SESSION_ID = "019f-test-0000-0000-000000000001"
SESSION_ID2 = "019f-test-0000-0000-000000000002"


def meta(ts="2026-08-10T09:00:00.000Z"):
    return {
        "timestamp": ts,
        "type": "session_meta",
        "payload": {
            "session_id": SESSION_ID,
            "id": SESSION_ID,
            "timestamp": ts,
            "cwd": "/tmp/work",
            "originator": "Codex Desktop",
            "model_provider": "custom",
            "first_user_message": "测试会话",
        },
    }


def msg(role, text, ts, mid):
    ctype = "input_text" if role == "user" else "output_text"
    return {
        "timestamp": ts,
        "type": "response_item",
        "payload": {
            "type": "message",
            "role": role,
            "id": mid,
            "content": [{"type": ctype, "text": text}],
        },
    }


def tool_call(ts, mid, name="shell_command", args='{"cmd":"dir"}'):
    return {
        "timestamp": ts,
        "type": "response_item",
        "payload": {
            "type": "function_call",
            "role": "assistant",
            "id": mid,
            "name": name,
            "arguments": args,
        },
    }


def tool_output(ts, mid, output="ok"):
    return {
        "timestamp": ts,
        "type": "response_item",
        "payload": {
            "type": "function_call_output",
            "role": "tool",
            "id": mid,
            "output": output,
        },
    }


BASE_ENTRIES = [
    meta(),
    msg("user", "如何发布文章？", "2026-08-10T09:12:40.234Z", "m1"),
    msg("assistant", "我来处理发布流程。", "2026-08-10T09:12:42.362Z", "m2"),
    tool_call("2026-08-10T09:12:43.000Z", "t1"),
    tool_output("2026-08-10T09:12:44.000Z", "t1o"),
    msg("user", "再讲一下编码问题", "2026-08-10T09:12:45.000Z", "m3"),
    msg("assistant", "编码问题已经修复。", "2026-08-10T09:12:46.000Z", "m4"),
]


class ExportTestCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.codex_home = Path(self._tmp.name) / "codex_home"
        self.sessions_dir = self.codex_home / "sessions" / "2026" / "08" / "10"
        self.sessions_dir.mkdir(parents=True, exist_ok=True)
        self._old_home = os.environ.get("CODEX_HOME")
        os.environ["CODEX_HOME"] = str(self.codex_home)

    def tearDown(self):
        if self._old_home is None:
            os.environ.pop("CODEX_HOME", None)
        else:
            os.environ["CODEX_HOME"] = self._old_home
        self._tmp.cleanup()

    def write_rollout(self, entries, name=None, session_id=SESSION_ID):
        path = self.sessions_dir / (
            name or f"rollout-2026-08-10T00-00-00-{session_id}.jsonl"
        )
        with open(path, "w", encoding="utf-8") as f:
            f.writelines(json.dumps(entry, ensure_ascii=False) + "\n" for entry in entries)
        return path

    def export_text(self, out_path, **kwargs):
        ex.export(SESSION_ID, str(out_path), **kwargs)
        return Path(out_path).read_text(encoding="utf-8")

    def test_full_export_and_brief_mode(self):
        self.write_rollout(BASE_ENTRIES)
        out = Path(self._tmp.name) / "full.md"
        text = self.export_text(out)
        self.assertIn("如何发布文章？", text)
        self.assertIn("我来处理发布流程。", text)
        self.assertIn("### 🔧 Tool Call", text)
        self.assertIn(SESSION_ID, text)

        brief = self.export_text(out, brief=True)
        self.assertNotIn("### 🔧 Tool Call", brief)
        self.assertIn("如何发布文章？", brief)

    def test_output_dir_is_auto_created(self):
        self.write_rollout(BASE_ENTRIES)
        out = Path(self._tmp.name) / "a" / "b" / "c" / "session.md"
        self.assertFalse(out.parent.exists())
        text = self.export_text(out)
        self.assertIn("如何发布文章？", text)
        self.assertTrue(out.exists())

    def test_since_until_window(self):
        self.write_rollout(BASE_ENTRIES)
        since = ex.parse_dt("2026-08-10T09:12:44.500Z")
        until = ex.parse_dt("2026-08-10T09:12:45.500Z")
        out = Path(self._tmp.name) / "window.md"
        text = self.export_text(out, brief=True, since=since, until=until)
        self.assertNotIn("如何发布文章？", text)      # before since
        self.assertNotIn("我来处理发布流程。", text)  # before since
        self.assertIn("再讲一下编码问题", text)       # inside window
        self.assertNotIn("编码问题已经修复。", text)  # after until

    def test_grep_pulls_full_turn(self):
        self.write_rollout(BASE_ENTRIES)
        out = Path(self._tmp.name) / "grep.md"
        text = self.export_text(out, brief=False, grep="编码")
        self.assertNotIn("如何发布文章？", text)
        self.assertNotIn("我来处理发布流程。", text)
        self.assertIn("再讲一下编码问题", text)
        self.assertIn("编码问题已经修复。", text)

    def test_grep_matches_question_and_turn(self):
        self.write_rollout(BASE_ENTRIES)
        out = Path(self._tmp.name) / "grep2.md"
        text = self.export_text(out, brief=False, grep="发布")
        self.assertIn("如何发布文章？", text)
        self.assertIn("我来处理发布流程。", text)
        self.assertNotIn("再讲一下编码问题", text)

    def test_incremental_append(self):
        self.write_rollout(BASE_ENTRIES[:4])
        out = Path(self._tmp.name) / "inc.md"
        first = self.export_text(out, brief=True, append=True)
        self.assertIn("如何发布文章？", first)
        self.assertNotIn("再讲一下编码问题", first)

        # conversation continues: append new entries to the same rollout file
        self.write_rollout(BASE_ENTRIES)
        second = self.export_text(out, brief=True, append=True)
        self.assertEqual(second.count("如何发布文章？"), 1)
        self.assertIn("再讲一下编码问题", second)
        self.assertIn("编码问题已经修复。", second)

        state = json.loads(
            Path(str(out) + ".state.json").read_text(encoding="utf-8")
        )
        self.assertEqual(state["session_id"], SESSION_ID)
        self.assertEqual(state["last_timestamp"], "2026-08-10T09:12:46.000Z")

        # third run is a no-op
        before = out.read_text(encoding="utf-8")
        self.export_text(out, brief=True, append=True)
        self.assertEqual(out.read_text(encoding="utf-8"), before)

    def test_append_with_since_as_initial_checkpoint(self):
        self.write_rollout(BASE_ENTRIES)
        out = Path(self._tmp.name) / "old.md"
        # simulate an older full export (no checkpoint)
        self.export_text(out, brief=True)
        self.assertEqual(out.read_text(encoding="utf-8").count("如何发布文章？"), 1)

        # continue chatting
        extra = [
            msg("user", "新增问题：如何导出？", "2026-08-10T10:00:00.000Z", "m5"),
            msg("assistant", "用 --append 即可。", "2026-08-10T10:00:05.000Z", "m6"),
        ]
        self.write_rollout(BASE_ENTRIES + extra)

        since = ex.parse_dt("2026-08-10T09:30:00.000Z")
        self.export_text(out, brief=True, append=True, since=since)
        text = out.read_text(encoding="utf-8")
        self.assertEqual(text.count("如何发布文章？"), 1)  # no duplication
        self.assertIn("新增问题：如何导出？", text)
        self.assertIn("用 --append 即可。", text)

    def test_multi_rollout_merge_and_dedup(self):
        self.write_rollout(BASE_ENTRIES[:3], name=f"rollout-A-{SESSION_ID}.jsonl")
        self.write_rollout(BASE_ENTRIES, name=f"rollout-B-{SESSION_ID}.jsonl")
        out = Path(self._tmp.name) / "multi.md"
        text = self.export_text(out, brief=True)
        self.assertEqual(text.count("如何发布文章？"), 1)
        self.assertEqual(text.count("我来处理发布流程。"), 1)
        self.assertIn("再讲一下编码问题", text)
        self.assertIn("编码问题已经修复。", text)

    def test_archived_sessions_fallback(self):
        path = self.write_rollout(BASE_ENTRIES)
        archived = self.codex_home / "archived_sessions" / "2026" / "08" / "10"
        archived.mkdir(parents=True, exist_ok=True)
        target = archived / path.name
        path.replace(target)
        out = Path(self._tmp.name) / "archived.md"
        text = self.export_text(out, brief=True)
        self.assertIn("如何发布文章？", text)

    def test_injected_blocks_are_stripped(self):
        noisy = [
            meta(),
            msg(
                "user",
                '<app-context>\n# Codex desktop context\n- some injected text\n</app-context>\n\n'
                '<in-app-browser-context source="ambient-ui-state">\nambient junk\n</in-app-browser-context>\n\n'
                "真实提问：如何保存对话？",
                "2026-08-10T09:12:40.234Z",
                "n1",
            ),
            msg("assistant", "用导出工具即可。", "2026-08-10T09:12:42.362Z", "n2"),
            msg(
                "user",
                "<environment_context>\n一些环境噪音\n</environment_context>",
                "2026-08-10T09:12:45.000Z",
                "n3",
            ),
        ]
        self.write_rollout(noisy)
        out = Path(self._tmp.name) / "noise.md"
        text = self.export_text(out, brief=True)
        self.assertIn("真实提问：如何保存对话？", text)
        self.assertNotIn("Codex desktop context", text)
        self.assertNotIn("ambient junk", text)
        self.assertNotIn("环境噪音", text)
        self.assertIn("用导出工具即可。", text)
        # the message that was only an injected block must not appear as blank section
        self.assertNotIn("## 👤 User\n\n##", text)

    def test_redact_masks_sensitive_content(self):
        sensitive = [
            meta(),
            msg(
                "user",
                "邮箱 user@example.com token sk-abc123456789 "
                "路径 D:\\Users\\EDY\\secret\\file.py 和 /home/edy/secret/file.py",
                "2026-08-10T09:12:40.234Z",
                "r1",
            ),
            msg("assistant", "你的 token 是 sk-xyz987654321，别外发。", "2026-08-10T09:12:42.362Z", "r2"),
        ]
        self.write_rollout(sensitive)

        plain = self.export_text(Path(self._tmp.name) / "plain.md", brief=True)
        self.assertIn("user@example.com", plain)
        self.assertIn("sk-abc123456789", plain)
        self.assertIn("D:\\Users\\EDY\\secret\\file.py", plain)

        redacted = self.export_text(Path(self._tmp.name) / "redacted.md", brief=True, redact=True)
        self.assertNotIn("user@example.com", redacted)
        self.assertNotIn("sk-abc123456789", redacted)
        self.assertNotIn("sk-xyz987654321", redacted)
        self.assertNotIn("Users\\EDY", redacted)
        self.assertNotIn("/home/edy/", redacted)
        self.assertIn("D:\\***\\file.py", redacted)
        self.assertIn("/***/file.py", redacted)

    def test_html_format(self):
        self.write_rollout(BASE_ENTRIES)
        out = Path(self._tmp.name) / "session.html"
        text = self.export_text(out, brief=True, fmt="html")
        self.assertTrue(text.startswith("<!doctype html>"))
        self.assertIn('<h2 class="role user">', text)
        self.assertIn('<h2 class="role assistant">', text)
        self.assertIn(SESSION_ID, text)
        self.assertIn("如何发布文章？", text)

    def test_html_escapes_content(self):
        evil = [
            meta(),
            msg("user", "<script>alert(1)</script> 提问 & 回答", "2026-08-10T09:12:40.234Z", "h1"),
            msg("assistant", "安全导出。", "2026-08-10T09:12:42.362Z", "h2"),
        ]
        self.write_rollout(evil)
        out = Path(self._tmp.name) / "evil.html"
        text = self.export_text(out, brief=True, fmt="html")
        self.assertNotIn("<script>alert(1)</script>", text)
        self.assertIn("&lt;script&gt;", text)

    def test_obsidian_format(self):
        self.write_rollout(BASE_ENTRIES)
        out = Path(self._tmp.name) / "session.md"
        text = self.export_text(out, brief=True, fmt="obsidian")
        self.assertTrue(text.startswith("---\n"))
        self.assertIn(f'session_id: "{SESSION_ID}"', text)
        self.assertIn("- codex", text)
        self.assertIn("如何发布文章？", text)

    def test_obsidian_append_keeps_frontmatter_once(self):
        self.write_rollout(BASE_ENTRIES[:2])
        out = Path(self._tmp.name) / "obs.md"
        first = self.export_text(out, brief=True, fmt="obsidian", append=True)
        self.assertTrue(first.startswith("---\n"))
        self.assertEqual(first.count("session_id:"), 1)
        self.write_rollout(BASE_ENTRIES)
        second = self.export_text(out, brief=True, fmt="obsidian", append=True)
        self.assertEqual(second.count("session_id:"), 1)
        self.assertIn("再讲一下编码问题", second)

    def test_html_append_rejected(self):
        self.write_rollout(BASE_ENTRIES)
        out = Path(self._tmp.name) / "session.html"
        self.export_text(out, brief=True, fmt="html")
        with self.assertRaises(SystemExit):
            self.export_text(out, brief=True, fmt="html", append=True)

    def test_interactive_select_picks_entries(self):
        self.write_rollout(BASE_ENTRIES)
        entries = ex.load_entries(ex.find_rollouts(SESSION_ID))
        answers = iter(["1", "3", "d"])
        selected = ex.interactive_select(
            entries, input_fn=lambda prompt: next(answers)
        )
        payloads = [(e.get("payload") or {}).get("type") for e in selected]
        texts = [
            ex.get_text((e.get("payload") or {}).get("content"))
            for e in selected
            if (e.get("payload") or {}).get("type") == "message"
        ]
        self.assertIn("如何发布文章？", texts)
        self.assertIn("function_call", payloads)
        self.assertNotIn("再讲一下编码问题", texts)

    def test_interactive_select_toggle_and_all(self):
        self.write_rollout(BASE_ENTRIES)
        entries = ex.load_entries(ex.find_rollouts(SESSION_ID))
        answers = iter(["1", "1", "d"])
        selected = ex.interactive_select(
            entries, input_fn=lambda prompt: next(answers)
        )
        self.assertEqual(selected, [])

        answers = iter(["a", "d"])
        selected = ex.interactive_select(
            entries, input_fn=lambda prompt: next(answers)
        )
        self.assertGreaterEqual(len(selected), 6)

    def test_interactive_export_end_to_end(self):
        self.write_rollout(BASE_ENTRIES)
        out = Path(self._tmp.name) / "picked.md"
        answers = iter(["1", "d"])
        ex.export(
            SESSION_ID, str(out), interactive=True,
            input_fn=lambda prompt: next(answers),
        )
        text = out.read_text(encoding="utf-8")
        self.assertIn("如何发布文章？", text)
        self.assertNotIn("我来处理发布流程。", text)

    def build_second_session(self):
        return [
            {
                "timestamp": "2026-08-10T10:00:00.000Z",
                "type": "session_meta",
                "payload": {
                    "session_id": SESSION_ID2,
                    "id": SESSION_ID2,
                    "timestamp": "2026-08-10T10:00:00.000Z",
                    "cwd": "/tmp/other",
                    "originator": "Codex CLI",
                    "model_provider": "gpt-5",
                    "first_user_message": "第二会话",
                },
            },
            msg("user", "第二个会话的问题", "2026-08-10T10:00:05.000Z", "o1"),
            msg("assistant", "第二个会话的回答", "2026-08-10T10:00:06.000Z", "o2"),
        ]

    def test_merged_export_md(self):
        self.write_rollout(BASE_ENTRIES)
        self.write_rollout(self.build_second_session(), session_id=SESSION_ID2)
        out = Path(self._tmp.name) / "merged.md"
        ex.export_merged([SESSION_ID, SESSION_ID2], str(out), brief=True)
        text = out.read_text(encoding="utf-8")
        self.assertIn("## 📁 Session", text)
        self.assertIn(SESSION_ID, text)
        self.assertIn(SESSION_ID2, text)
        self.assertIn("如何发布文章？", text)
        self.assertIn("第二个会话的问题", text)
        self.assertIn("**Sessions:** 2", text)

    def test_merged_export_html(self):
        self.write_rollout(BASE_ENTRIES)
        self.write_rollout(self.build_second_session(), session_id=SESSION_ID2)
        out = Path(self._tmp.name) / "merged.html"
        ex.export_merged([SESSION_ID, SESSION_ID2], str(out), brief=True, fmt="html")
        text = out.read_text(encoding="utf-8")
        self.assertIn(SESSION_ID, text)
        self.assertIn(SESSION_ID2, text)
        self.assertIn('<h3 class="role user">', text)

    def test_merged_export_grep(self):
        self.write_rollout(BASE_ENTRIES)
        self.write_rollout(self.build_second_session(), session_id=SESSION_ID2)
        out = Path(self._tmp.name) / "merged_grep.md"
        ex.export_merged([SESSION_ID, SESSION_ID2], str(out), brief=True, grep="第二个")
        text = out.read_text(encoding="utf-8")
        self.assertIn("第二个会话的问题", text)
        self.assertNotIn("如何发布文章？", text)

    def test_watch_loop_runs_once_then_stops(self):
        self.write_rollout(BASE_ENTRIES[:2])
        out = Path(self._tmp.name) / "watch.md"

        def boom(seconds):
            raise KeyboardInterrupt

        ex.watch_loop(SESSION_ID, str(out), interval=1, brief=True, sleep_fn=boom)
        text = out.read_text(encoding="utf-8")
        self.assertIn("如何发布文章？", text)

    def test_header_contains_statistics(self):
        self.write_rollout(BASE_ENTRIES)
        out = Path(self._tmp.name) / "stats.md"
        text = self.export_text(out, brief=True)
        self.assertIn("- **Messages:** 2 用户 / 2 助手", text)
        self.assertIn("- **Tool calls:** 1", text)
        self.assertIn("- **Duration:**", text)

    def test_append_records_file_offsets(self):
        path = self.write_rollout(BASE_ENTRIES[:4])
        out = Path(self._tmp.name) / "inc2.md"
        self.export_text(out, brief=True, append=True)
        state = json.loads(
            Path(str(out) + ".state.json").read_text(encoding="utf-8")
        )
        self.assertIn(str(path), state["file_offsets"])
        self.assertEqual(state["file_offsets"][str(path)], path.stat().st_size)

    def test_append_fallback_when_file_shrunk(self):
        path = self.write_rollout(BASE_ENTRIES)
        out = Path(self._tmp.name) / "shrunk.md"
        self.export_text(out, brief=True, append=True)
        # simulate a replaced/truncated rollout file
        path.write_text("", encoding="utf-8")
        self.write_rollout(BASE_ENTRIES[:2])
        self.export_text(out, brief=True, append=True)  # must not crash
        state = json.loads(
            Path(str(out) + ".state.json").read_text(encoding="utf-8")
        )
        self.assertEqual(state["file_offsets"][str(path)], path.stat().st_size)


if __name__ == "__main__":
    unittest.main()
