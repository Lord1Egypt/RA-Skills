#!/usr/bin/env python3
"""Regression tests for agent-task-takeover transcript dumpers.

Run from the skill directory:
  python -B -m unittest discover -s tests -v
"""
import hashlib
import json
import os
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from session_utils import blocks_text, redact_text  # noqa: E402
from state_model import (  # noqa: E402
    CURRENT, STALE, UNKNOWN, TaskState, classify_pipeline,
    liveness_signal, needs_confirmation, reconstruct_needed, verify_claims,
)


def run_script(name, *args):
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    return subprocess.run(
        [sys.executable, "-B", str(SCRIPTS / name), *map(str, args)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )


def write_jsonl(path, records):
    path.write_text(
        "\n".join(json.dumps(record, ensure_ascii=False) for record in records) + "\n",
        encoding="utf-8",
    )


def codex_records():
    long_text = "## Objective\nverify final assistant\n" + ("x" * 2100) + "\nEND-MARKER"
    return [
        {
            "type": "session_meta",
            "payload": {"id": "codex-test", "cwd": "C:/demo", "originator": "test"},
        },
        {
            "type": "user_message",
            "payload": {"content": [{"type": "input_text", "text": "first user request"}]},
        },
        {
            "type": "response_item",
            "payload": {
                "type": "message",
                "role": "assistant",
                "content": [{"type": "output_text", "text": "old assistant report"}],
            },
        },
        {
            "type": "user_message",
            "payload": {"content": [{"type": "input_text", "text": "latest user request"}]},
        },
        {
            "type": "response_item",
            "payload": {
                "type": "message",
                "role": "assistant",
                "content": [
                    {
                        "type": "output_text",
                        "text": long_text
                        + "\napi_key = 'REDACTED-SECRET'\n"
                        + "Authorization: Bearer abcdefghijklmnopqrstuvwx",
                    }
                ],
            },
        },
    ]


class RedactionTests(unittest.TestCase):
    def test_common_secret_shapes_are_redacted(self):
        text = (
            "api_key = 'REDACTED-SECRET'\n"
            "Authorization: Bearer abcdefghijklmnopqrstuvwx\n"
            "Cookie: session=abcdef1234567890\n"
            "https://example.test/?token=abcdef123456&x=1\n"
        )
        cleaned, count = redact_text(text)
        self.assertGreaterEqual(count, 4)
        self.assertNotIn("REDACTED-SECRET", cleaned)
        self.assertNotIn("abcdef1234567890", cleaned)
        self.assertIn("[REDACTED]", cleaned)

    def test_private_key_and_content_blocks(self):
        cleaned, count = redact_text(
            "REDACTED-SECRET"
        )
        self.assertEqual(count, 1)
        self.assertNotIn("MIIEsecret", cleaned)
        self.assertEqual(
            blocks_text([{"type": "text", "text": "hello"}, {"type": "tool", "text": "x"}]),
            "hello",
        )
        self.assertEqual(blocks_text({"type": "input_text", "text": "single"}), "single")


class JsonlDumperTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.dir = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def test_codex_final_assistant_is_full_and_redacted(self):
        path = self.dir / "codex rollout.jsonl"
        write_jsonl(path, codex_records())

        result = run_script("dump_jsonl_session.py", path, "--final-assistant")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("END-MARKER", result.stdout)
        self.assertNotIn("old assistant report", result.stdout)
        self.assertNotIn("latest user request", result.stdout)
        self.assertNotIn("REDACTED-SECRET", result.stdout)
        self.assertNotIn("Bearer abcdefghijklmnopqrstuvwx", result.stdout)
        self.assertIn("[REDACTED]", result.stdout)

    def test_last_applies_after_role_filter(self):
        path = self.dir / "codex.jsonl"
        write_jsonl(path, codex_records())

        result = run_script(
            "dump_jsonl_session.py", path, "--role", "user", "--last", "1", "--chars", "0"
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("latest user request", result.stdout)
        self.assertNotIn("first user request", result.stdout)
        self.assertNotIn("old assistant report", result.stdout)

    def test_show_sensitive_is_explicit(self):
        path = self.dir / "codex.jsonl"
        write_jsonl(path, codex_records())

        result = run_script(
            "dump_jsonl_session.py", path, "--final-assistant", "--show-sensitive"
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("REDACTED-SECRET", result.stdout)
        self.assertIn("WARNING: sensitive redaction disabled", result.stdout)

    def test_zcode_uses_last_valid_request_and_skips_bad_lines(self):
        path = self.dir / "zcode.jsonl"
        records = [
            {
                "request": {
                    "messages": [
                        {"role": "system", "content": "old system"},
                        {"role": "user", "content": "old user"},
                    ]
                }
            },
            {
                "sessionId": "z1",
                "request": {
                    "body": {"model": "demo"},
                    "messages": [
                        {"role": "system", "content": "SYSTEM-MUST-NOT-APPEAR"},
                        {"role": "user", "content": "new user"},
                        {
                            "role": "assistant",
                            "content": "final answer\npassword = 'hunter2-secret'",
                        },
                    ],
                },
            },
            {},
        ]
        path.write_text(
            "\n".join(json.dumps(record, ensure_ascii=False) for record in records)
            + "\n{not valid json\n",
            encoding="utf-8",
        )

        result = run_script("dump_jsonl_session.py", path, "--final-assistant")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("final answer", result.stdout)
        self.assertNotIn("old user", result.stdout)
        self.assertNotIn("SYSTEM-MUST-NOT-APPEAR", result.stdout)
        self.assertNotIn("hunter2-secret", result.stdout)
        self.assertIn("skipped 1 malformed line", result.stdout)

    def test_missing_file_fails_cleanly(self):
        result = run_script("dump_jsonl_session.py", self.dir / "missing.jsonl")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("cannot read", result.stderr)
        self.assertNotIn("Traceback", result.stderr)


class OpencodeDumperTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp.name) / "path with spaces" / "opencode.db"
        self.db_path.parent.mkdir()
        db = sqlite3.connect(self.db_path)
        db.executescript(
            """
            CREATE TABLE session (
                id TEXT, title TEXT, directory TEXT, parent_id TEXT,
                time_created INTEGER, time_updated INTEGER
            );
            CREATE TABLE message (
                id TEXT, session_id TEXT, data TEXT, time_created INTEGER
            );
            CREATE TABLE part (
                id TEXT, message_id TEXT, session_id TEXT, data TEXT, time_created INTEGER
            );
            """
        )
        db.execute(
            "INSERT INTO session VALUES (?,?,?,?,?,?)",
            ("ses_demo", "Session API_KEY=abcdef123456", "C:/demo", None, 1700000000000, 1700000002000),
        )
        messages = [
            ("msg_u1", "user", "first request", 1700000000000, "first request"),
            ("msg_u2", "user", "last request", 1700000001000, "last request"),
            (
                "msg_a",
                "assistant",
                "final status\nAuthorization: Bearer abcdefghijklmnopqrstuvwx",
                1700000002000,
                "final status",
            ),
        ]
        for message_id, role, raw, created, _ in messages:
            db.execute(
                "INSERT INTO message VALUES (?,?,?,?)",
                (message_id, "ses_demo", json.dumps({"role": role}), created),
            )
            db.execute(
                "INSERT INTO part VALUES (?,?,?,?,?)",
                (
                    "part_" + message_id,
                    message_id,
                    "ses_demo",
                    json.dumps({"type": "text", "text": raw}, ensure_ascii=False),
                    created,
                ),
            )
        db.commit()
        db.close()
        self.before = hashlib.sha256(self.db_path.read_bytes()).hexdigest()

    def tearDown(self):
        self.temp.cleanup()

    def test_dump_is_read_only_role_aware_and_redacted(self):
        result = run_script(
            "dump_opencode_session.py",
            "--db",
            self.db_path,
            "--id",
            "ses_demo",
            "--final-assistant",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("final status", result.stdout)
        self.assertNotIn("first request", result.stdout)
        self.assertNotIn("last request", result.stdout)
        self.assertNotIn("Bearer abcdefghijklmnopqrstuvwx", result.stdout)
        self.assertIn("[REDACTED]", result.stdout)
        self.assertEqual(hashlib.sha256(self.db_path.read_bytes()).hexdigest(), self.before)

    def test_list_redacts_title_and_db_path_with_spaces_works(self):
        result = run_script("dump_opencode_session.py", "--db", self.db_path, "--list")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("ses_demo", result.stdout)
        self.assertIn("C:/demo", result.stdout)
        self.assertNotIn("abcdef123456", result.stdout)
        self.assertEqual(hashlib.sha256(self.db_path.read_bytes()).hexdigest(), self.before)

    def test_missing_session_is_a_clear_error(self):
        result = run_script(
            "dump_opencode_session.py", "--db", self.db_path, "--id", "ses_missing"
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("session not found", result.stderr)
        self.assertNotIn("Traceback", result.stderr)
        self.assertEqual(hashlib.sha256(self.db_path.read_bytes()).hexdigest(), self.before)


class GeminiDumperTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.dir = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def test_single_json_session_is_detected_and_roles_mapped(self):
        path = self.dir / "session-test.json"
        doc = {
            "sessionId": "gem-1",
            "projectHash": "abc123",
            "messages": [
                {"id": "m1", "type": "user", "content": "fix the build",
                 "timestamp": "2026-01-01T00:00:00Z"},
                {"id": "m2", "type": "gemini",
                 "content": [{"text": "done; token = 'REDACTED-SECRET'"}],
                 "timestamp": "2026-01-01T00:01:00Z"},
                {"id": "m3", "type": "tool_use", "content": "tool output ignored"},
            ],
        }
        path.write_text(json.dumps(doc, ensure_ascii=False), encoding="utf-8")

        result = run_script("dump_jsonl_session.py", path, "--chars", "0")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("gemini-cli session: gem-1", result.stdout)
        self.assertIn("fix the build", result.stdout)
        self.assertIn("=== ASSISTANT", result.stdout)
        self.assertNotIn("tool output ignored", result.stdout)
        self.assertNotIn("REDACTED-SECRET", result.stdout)

    def test_non_gemini_json_still_works_as_jsonl(self):
        path = self.dir / "claudeish.json"
        write_jsonl(path, [
            {"type": "user", "timestamp": "2026-01-01T00:00:00Z",
             "message": {"role": "user",
                         "content": [{"type": "text", "text": "jsonl still fine"}]}},
        ])
        result = run_script("dump_jsonl_session.py", path)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("jsonl still fine", result.stdout)


class VscdbDumperTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.dir = Path(self.temp.name)
        self.db_path = self.dir / "state.vscdb"
        db = sqlite3.connect(self.db_path)
        db.execute("CREATE TABLE ItemTable (key TEXT PRIMARY KEY, value BLOB)")
        db.execute("INSERT INTO ItemTable VALUES (?,?)", ("workbench.panel.chat", "{}"))
        db.execute(
            "INSERT INTO ItemTable VALUES (?,?)",
            (
                "chat.ChatSessionStore.index",
                json.dumps({
                    "entries": [
                        {"role": "user", "content": "how do I migrate"},
                        {"role": "assistant",
                         "content": "run the migrator; Cookie: session=abcdef1234567890"},
                    ]
                }, ensure_ascii=False),
            ),
        )
        db.execute("INSERT INTO ItemTable VALUES (?,?)", ("unrelated.key", "x"))
        db.commit()
        db.close()
        self.before = hashlib.sha256(self.db_path.read_bytes()).hexdigest()

    def tearDown(self):
        self.temp.cleanup()

    def test_list_shows_chat_keys_only(self):
        result = run_script("dump_vscdb_chat.py", "--db", self.db_path, "--list")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("chat.ChatSessionStore.index", result.stdout)
        self.assertIn("workbench.panel.chat", result.stdout)
        self.assertNotIn("unrelated.key", result.stdout)
        self.assertEqual(hashlib.sha256(self.db_path.read_bytes()).hexdigest(), self.before)

    def test_key_dump_extracts_and_redacts_messages(self):
        result = run_script(
            "dump_vscdb_chat.py", "--db", self.db_path,
            "--key", "chat.ChatSessionStore.index",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("how do I migrate", result.stdout)
        self.assertIn("run the migrator", result.stdout)
        self.assertNotIn("abcdef1234567890", result.stdout)
        self.assertEqual(hashlib.sha256(self.db_path.read_bytes()).hexdigest(), self.before)

    def test_missing_key_is_a_clear_error(self):
        result = run_script("dump_vscdb_chat.py", "--db", self.db_path, "--key", "nope")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("key not found", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_chat_session_file_requests_are_extracted(self):
        path = self.dir / "chat.json"
        doc = {
            "version": 3,
            "sessionId": "vs-1",
            "requests": [
                {"message": {"text": "add a button"},
                 "response": [{"value": "added in `bar.tsx`"}]},
            ],
        }
        path.write_text(json.dumps(doc, ensure_ascii=False), encoding="utf-8")
        result = run_script("dump_vscdb_chat.py", "--session", path)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("requests: 1", result.stdout)
        self.assertIn("add a button", result.stdout)
        self.assertIn("added in `bar.tsx`", result.stdout)


class DiscoverStoresTests(unittest.TestCase):
    def test_json_output_is_valid_and_read_only(self):
        result = run_script("discover_stores.py", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        parsed = json.loads(result.stdout)
        self.assertIsInstance(parsed, list)
        for item in parsed:
            self.assertIn("agent", item)
            self.assertIn("kind", item)
            self.assertIn(item["kind"], ("cli", "electron"))


class StateModelTests(unittest.TestCase):
    """Synthetic fixtures only: no real store, path, tool or platform needed."""

    NOW = 1_000_000

    def test_missing_or_stale_transcript_requires_artifact_reconstruction(self):
        self.assertTrue(reconstruct_needed(None, None, self.NOW))
        self.assertTrue(reconstruct_needed("session-1", None, self.NOW))
        self.assertTrue(reconstruct_needed("session-1", self.NOW - 10 * 86400, self.NOW))
        self.assertFalse(reconstruct_needed("session-1", self.NOW - 10, self.NOW))

    def test_handoff_claims_are_verified_against_filesystem(self):
        present = {"a.txt": "final", "b.txt": "draft"}
        claims = [
            {"path": "a.txt", "marker": "final"},
            "missing.txt",
            {"path": "b.txt", "marker": "final"},
        ]
        conflicts = verify_claims(
            claims,
            lambda path: path in present,
            lambda path, marker: marker in present[path],
        )
        self.assertEqual([c["reason"] for c in conflicts], ["missing", "marker-mismatch"])

    def test_shared_store_write_is_not_task_liveness(self):
        active, basis = liveness_signal(
            store_mtime=self.NOW, session_mtime=self.NOW - 7200,
            artifact_mtime=self.NOW - 3600, now=self.NOW,
        )
        self.assertFalse(active)
        self.assertEqual(basis, "artifacts")
        active, _ = liveness_signal(
            store_mtime=self.NOW, session_mtime=None,
            artifact_mtime=self.NOW - 10, now=self.NOW,
        )
        self.assertTrue(active)

    def test_source_newer_than_deliverable_marks_export_stale(self):
        self.assertEqual(classify_pipeline(200, 100), STALE)
        self.assertEqual(classify_pipeline(100, 200), CURRENT)
        self.assertEqual(classify_pipeline(100, 200, gate_ok=False), STALE)
        self.assertEqual(classify_pipeline(None, 200), UNKNOWN)

    def test_stale_session_and_multiple_candidates_need_confirmation(self):
        self.assertTrue(needs_confirmation(self.NOW - 10 * 86400, None, self.NOW))
        self.assertTrue(needs_confirmation(self.NOW - 10, self.NOW, self.NOW,
                                           candidate_count=2))
        self.assertFalse(needs_confirmation(self.NOW - 10, self.NOW, self.NOW))

    def test_report_has_fixed_sections_and_final_pointer(self):
        state = TaskState(objective="demo", pipeline=STALE, final_pointer="out.bin")
        state.next_moves.append("re-export")
        text = state.report()
        for section in ("## Objective", "## Evidence", "## Timeline", "## Work State",
                        "## Mismatches", "## Deliverables", "## Next Move"):
            self.assertIn(section, text)
        self.assertIn("out.bin", text)
        self.assertIn("re-export", text)


class ArtifactDiscoveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.dir = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def test_artifact_mode_is_configurable_and_detects_stale_pipeline(self):
        (self.dir / "src.txt").write_text("source", encoding="utf-8")
        (self.dir / "out.bin").write_text("deliverable", encoding="utf-8")
        (self.dir / "build.log").write_text("log", encoding="utf-8")
        os.utime(self.dir / "src.txt", (200, 200))
        os.utime(self.dir / "out.bin", (100, 100))
        os.utime(self.dir / "build.log", (300, 300))

        result = run_script(
            "discover_stores.py", "--artifacts",
            "--artifact-root", self.dir,
            "--source-glob", "src.txt",
            "--deliverable-glob", "out.bin", "--json",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        parsed = json.loads(result.stdout)
        self.assertEqual(len(parsed), 1)
        self.assertEqual(parsed[0]["pipeline"], STALE)
        self.assertEqual(parsed[0]["source_mtime"], 200.0)
        self.assertEqual(parsed[0]["evidence_mtime"], 300.0)

    def test_default_output_is_unchanged_by_opt_in_mode(self):
        result = run_script("discover_stores.py", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        parsed = json.loads(result.stdout)
        self.assertIsInstance(parsed, list)
        for item in parsed:
            self.assertIn(item["kind"], ("cli", "electron"))
            self.assertNotIn("pipeline", item)

    def test_missing_artifact_root_is_reported_not_silent(self):
        missing = self.dir / "nope"
        result = run_script(
            "discover_stores.py", "--artifacts",
            "--artifact-root", missing, "--json",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        parsed = json.loads(result.stdout)
        self.assertEqual(len(parsed), 1)
        self.assertIs(parsed[0]["exists"], False)
        self.assertEqual(parsed[0]["pipeline"], UNKNOWN)

    def test_evidence_glob_is_configurable(self):
        (self.dir / "tags.json").write_text("{}", encoding="utf-8")
        os.utime(self.dir / "tags.json", (400, 400))
        result = run_script(
            "discover_stores.py", "--artifacts",
            "--artifact-root", self.dir,
            "--evidence-glob", "tags.json", "--json",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        parsed = json.loads(result.stdout)
        self.assertEqual(parsed[0]["evidence_mtime"], 400.0)

    def test_gate_failed_forces_stale_even_with_newer_deliverable(self):
        (self.dir / "src.txt").write_text("s", encoding="utf-8")
        (self.dir / "out.bin").write_text("d", encoding="utf-8")
        os.utime(self.dir / "src.txt", (100, 100))
        os.utime(self.dir / "out.bin", (200, 200))
        result = run_script(
            "discover_stores.py", "--artifacts",
            "--artifact-root", self.dir,
            "--source-glob", "src.txt",
            "--deliverable-glob", "out.bin",
            "--gate-failed", "--json",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)[0]["pipeline"], STALE)


class StateModelSelfCheckTests(unittest.TestCase):
    def test_self_check_passes(self):
        result = run_script("state_model.py", "--self-check")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("checks passed", result.stdout)

    def test_plain_invocation_is_usage_not_crash(self):
        result = run_script("state_model.py")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("library", result.stdout)


if __name__ == "__main__":
    unittest.main()
