"""Tests for journal_collect.py — offline, stdlib only.

Builds a throwaway state.db with the columns the collector reads, so window math,
session attribution and digest shape are all exercised without touching real data.

Run: python -m unittest discover -s tests -v
"""

from __future__ import annotations

import contextlib
import datetime as dt
import io
import json
import os
import pathlib
import sqlite3
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import journal_collect as collect  # noqa: E402

SCHEMA_SESSIONS = """
CREATE TABLE sessions (
    id TEXT PRIMARY KEY, title TEXT, display_name TEXT, source TEXT, model TEXT,
    started_at REAL, last_activity_at REAL, message_count INTEGER, tool_call_count INTEGER,
    cwd TEXT, hidden INTEGER DEFAULT 0
)
"""
SCHEMA_MESSAGES = """
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT, session_id TEXT, role TEXT, content TEXT,
    tool_name TEXT, timestamp REAL, active INTEGER DEFAULT 1
)
"""


class SandboxTestCase(unittest.TestCase):
    """Temp state.db + temp journal + a config pointing at both, no Ollama."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = pathlib.Path(self._tmp.name)
        self.db = self.root / "state.db"
        self.journal = self.root / "memory" / "journal" / "journal.md"
        self.journal.parent.mkdir(parents=True, exist_ok=True)
        con = sqlite3.connect(self.db)
        con.execute(SCHEMA_SESSIONS)
        con.execute(SCHEMA_MESSAGES)
        con.commit()
        con.close()
        self.cfg = collect.load_config(None)
        self.cfg.update({
            "state_db": self.db,
            "journal": self.journal,
            "workspace": self.root,
            "day_start_hour": 4,
            "max_windows": 4,
            "local_mode": "off",          # no Ollama in tests
            "labels": collect.DEFAULTS["labels"],
        })

    # -- helpers ---------------------------------------------------------
    def add_session(self, sid, title, prompt, when: dt.datetime, outcome="done",
                    tools=("read_file",), source="telegram"):
        con = sqlite3.connect(self.db)
        ts = when.timestamp()
        con.execute(
            "INSERT INTO sessions (id, title, display_name, source, model, started_at,"
            " last_activity_at, message_count, tool_call_count, cwd, hidden)"
            " VALUES (?,?,?,?,?,?,?,?,?,?,0)",
            (sid, title, title, source, "test-model", ts, ts + 60, 4, len(tools), str(self.root)),
        )
        con.execute("INSERT INTO messages (session_id, role, content, timestamp) VALUES (?,?,?,?)",
                    (sid, "user", prompt, ts))
        for tool in tools:
            con.execute("INSERT INTO messages (session_id, role, content, tool_name, timestamp)"
                        " VALUES (?,?,?,?,?)", (sid, "tool", '{"ok": true}', tool, ts + 10))
        con.execute("INSERT INTO messages (session_id, role, content, timestamp) VALUES (?,?,?,?)",
                    (sid, "assistant", outcome, ts + 20))
        con.commit()
        con.close()

    def write_config(self) -> pathlib.Path:
        path = self.root / "journal.json"
        path.write_text(json.dumps({
            "state_db": str(self.db),
            "journal": str(self.journal),
            "workspace": str(self.root),
            "local_mode": "off",
        }), encoding="utf-8")
        return path

    def run_cli(self, argv: list[str]) -> tuple[int, str]:
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            code = collect.main(argv)
        return code, buffer.getvalue()


class WindowMathTests(SandboxTestCase):
    def test_window_bounds_respect_day_start_hour(self):
        start, end = collect.window_bounds(dt.date(2026, 10, 25), self.cfg)
        self.assertEqual(dt.datetime.fromtimestamp(start), dt.datetime(2026, 10, 25, 4, 0))
        self.assertEqual(dt.datetime.fromtimestamp(end), dt.datetime(2026, 10, 26, 4, 0))

    def test_latest_complete_day_excludes_the_open_window(self):
        self.assertEqual(collect.latest_complete_day(dt.datetime(2026, 10, 26, 19, 0), self.cfg),
                         dt.date(2026, 10, 25))
        self.assertEqual(collect.latest_complete_day(dt.datetime(2026, 10, 26, 3, 0), self.cfg),
                         dt.date(2026, 10, 24))

    def test_missing_days_only_reports_owed_windows(self):
        self.journal.write_text("## 2026-10-23 x\n\nbody\n\n<!-- window:2026-10-23 -->\n",
                                encoding="utf-8")
        missing = collect.missing_days(dt.datetime(2026, 10, 26, 19, 0), self.cfg)
        self.assertEqual([d.isoformat() for d in missing], ["2026-10-24", "2026-10-25"])

    def test_marked_window_is_not_owed(self):
        self.journal.write_text("<!-- window:2026-10-24 -->\n<!-- window:2026-10-25 -->\n",
                                encoding="utf-8")
        self.assertEqual(collect.missing_days(dt.datetime(2026, 10, 26, 19, 0), self.cfg), [])


class DigestTests(SandboxTestCase):
    def test_sessions_inside_window_become_one_block_each(self):
        self.add_session("s1", "fix the build", "the build is broken", dt.datetime(2026, 10, 25, 9, 0))
        self.add_session("s2", "write docs", "write the docs for it", dt.datetime(2026, 10, 25, 14, 0))
        self.add_session("s3", "yesterday", "old work", dt.datetime(2026, 10, 24, 9, 0))
        digest = collect.build_digest(dt.date(2026, 10, 25), False, False, set(), self.cfg)
        events = collect.window_events(digest)
        self.assertEqual(len(events), 2, "only in-window sessions, one heading each")
        self.assertIn("fix the build", events[0])
        self.assertIn("write docs", events[1])
        self.assertNotIn("yesterday", digest)

    def test_cron_sessions_are_excluded(self):
        self.add_session("s1", "real work", "do it", dt.datetime(2026, 10, 25, 9, 0))
        self.add_session("c1", "cron job", "x", dt.datetime(2026, 10, 25, 10, 0), source="cron")
        digest = collect.build_digest(dt.date(2026, 10, 25), False, False, set(), self.cfg)
        self.assertNotIn("cron job", digest)
        self.assertIn("real work", digest)

    def test_files_section_is_not_counted_as_an_event(self):
        when = dt.datetime(2026, 10, 25, 9, 0)
        self.add_session("s1", "fix the build", "the build is broken", when)
        touched = self.root / "note.txt"
        touched.write_text("x", encoding="utf-8")
        stamp = when.timestamp() + 30
        os.utime(touched, (stamp, stamp))
        digest = collect.build_digest(dt.date(2026, 10, 25), False, False, set(), self.cfg)
        self.assertIn(self.cfg["labels"]["files"], digest)
        self.assertEqual(len(collect.window_events(digest, self.cfg)), 1)

    def test_empty_window_says_so(self):
        digest = collect.build_digest(dt.date(2026, 10, 25), False, False, set(), self.cfg)
        self.assertEqual(collect.window_events(digest), [])
        self.assertIn(self.cfg["labels"]["empty_window"], digest)

    def test_json_mode_lists_windows_and_events(self):
        self.add_session("s1", "fix the build", "the build is broken", dt.datetime(2026, 10, 25, 9, 0))
        code, out = self.run_cli(["--config", str(self.write_config()),
                                  "--only", "2026-10-25", "--json"])
        self.assertEqual(code, 0)
        payload = json.loads(out)
        self.assertEqual(payload["windows"][0]["day"], "2026-10-25")
        self.assertEqual(len(payload["windows"][0]["events"]), 1)
        self.assertIn("fix the build", payload["windows"][0]["events"][0])

    def test_markdown_mode_ends_with_the_marker_instruction(self):
        self.add_session("s1", "fix the build", "the build is broken", dt.datetime(2026, 10, 25, 9, 0))
        code, out = self.run_cli(["--config", str(self.write_config()), "--only", "2026-10-25"])
        self.assertEqual(code, 0)
        self.assertIn("window:YYYY-MM-DD", out)


class ConfigTests(unittest.TestCase):
    def test_language_zh_switches_the_labels(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "journal.json"
            path.write_text(json.dumps({"language": "zh"}), encoding="utf-8")
            cfg = collect.load_config(str(path))
            self.assertIn("待写日记窗口", cfg["labels"]["header"])
            self.assertEqual(cfg["labels"]["weekdays"][0], "周一")

    def test_env_overrides_beat_the_config_file(self):
        os.environ["JOURNAL_DAY_START_HOUR"] = "6"
        try:
            self.assertEqual(collect.load_config(None)["day_start_hour"], 6)
        finally:
            del os.environ["JOURNAL_DAY_START_HOUR"]

    def test_every_label_exists_in_both_languages(self):
        self.assertEqual(set(collect.DEFAULTS["labels"]), set(collect.CN_LABELS))


if __name__ == "__main__":
    unittest.main()
