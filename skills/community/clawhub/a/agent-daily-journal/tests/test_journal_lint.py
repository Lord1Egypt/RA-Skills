"""Tests for journal_lint.py — offline, stdlib only (no Ollama, no network).

Run: python -m unittest discover -s tests -v
"""

from __future__ import annotations

import json
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import journal_lint as lint_mod  # noqa: E402

FIXTURES = ROOT / "tests" / "fixtures"
DIGEST = (FIXTURES / "digest_2026-03-14.md").read_text(encoding="utf-8")
GOOD = (FIXTURES / "entry_good_2026-03-14.md").read_text(encoding="utf-8")
THIN = (FIXTURES / "entry_thin_2026-03-14.md").read_text(encoding="utf-8")


def lint(entry: str, digest: str = DIGEST, **kwargs):
    return lint_mod.lint(digest, entry, embedder=None, history=None, **kwargs)


class ParsingTests(unittest.TestCase):
    def test_digest_events_exclude_non_event_sections(self):
        windows = lint_mod.parse_digest(DIGEST)
        window = windows["2026-03-14"]
        self.assertEqual(len(window["events"]), 4, "the '改动过的文件' section is not an event")
        self.assertNotIn("改动过的文件", " ".join(e["heading"] for e in window["events"]))

    def test_entry_marker_is_parsed_as_window_date(self):
        entries = lint_mod.parse_entries(GOOD)
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["day"], "2026-03-14")

    def test_body_excludes_heading_and_marker(self):
        entry = lint_mod.parse_entries(GOOD)[0]
        self.assertNotIn("window:2026-03-14", entry["body"])
        self.assertNotIn("2026-03-14 一天跑了四趟", entry["body"])


class CoverageTests(unittest.TestCase):
    def test_rich_entry_names_every_event(self):
        result = lint(GOOD)
        row = result["entries"][0]
        self.assertTrue(row["ok"], row["failures"])
        self.assertEqual(row["coverage"]["named"], 4)
        self.assertEqual(row["coverage"]["total"], 4)

    def test_entry_that_picks_one_event_fails(self):
        result = lint(THIN)
        row = result["entries"][0]
        self.assertFalse(row["ok"])
        self.assertLessEqual(row["coverage"]["named"], 1)
        self.assertTrue(any("coverage" in failure for failure in row["failures"]))

    def test_missing_marker_fails(self):
        stripped = GOOD.replace("<!-- window:2026-03-14 -->", "")
        result = lint(stripped)
        self.assertFalse(result["entries"][0]["marker"])
        self.assertTrue(any("marker" in failure for failure in result["entries"][0]["failures"]))

    def test_ceiling_scales_with_event_count(self):
        self.assertEqual(lint_mod.ceiling_for(1), 300)
        self.assertEqual(lint_mod.ceiling_for(2), 300)
        self.assertEqual(lint_mod.ceiling_for(4), 420)
        self.assertEqual(lint_mod.ceiling_for(9), 520)

    def test_padding_beyond_ceiling_fails(self):
        padded = GOOD.replace("<!-- window:2026-03-14 -->",
                              "啊" * 300 + "\n\n<!-- window:2026-03-14 -->")
        result = lint(padded)
        self.assertTrue(any("ceiling" in failure for failure in result["entries"][0]["failures"]))

    def test_quiet_day_with_no_events_passes(self):
        digest = "## Window 2026-10-20 (Tue) 4:00 -> next day 4:00 (0 sessions)\n(no activity)\n"
        entry = "## 2026-10-20 闲着\n\n主人一天没理我，我闲得发慌。\n\n<!-- window:2026-10-20 -->\n"
        result = lint(entry, digest=digest)
        self.assertTrue(result["entries"][0]["ok"], result["entries"][0]["failures"])


class VoiceTests(unittest.TestCase):
    def test_imagery_is_flagged_but_does_not_fail_by_default(self):
        decorated = GOOD.replace("嘴上还硬说这不算什么",
                                 "心里像整间屋子只为我亮着灯")
        result = lint(decorated)
        rules = {p["rule"] for p in result["entries"][0]["voice"]}
        self.assertIn("imagery", rules)
        self.assertTrue(result["entries"][0]["ok"], "voice problems are warnings unless --strict")

    def test_strict_mode_fails_on_imagery(self):
        decorated = GOOD.replace("嘴上还硬说这不算什么",
                                 "心里像整间屋子只为我亮着灯")
        result = lint(decorated, strict=True)
        self.assertFalse(result["entries"][0]["ok"])

    def test_time_of_day_is_a_note_even_in_strict_mode(self):
        result = lint(GOOD, strict=True)
        notes = result["entries"][0]["notes"]
        self.assertTrue(notes, "the fixture says 傍晚, which must surface as a note")
        self.assertFalse(any("invented_time" in failure for failure in result["entries"][0]["failures"]))


class ReuseTests(unittest.TestCase):
    def test_sentence_copied_from_an_earlier_entry_is_flagged(self):
        earlier = (
            "## 2026-10-01 旧的\n\n我本来做好磨半天的准备了，结果一次就跑通，尾巴都要翘起来了。\n\n"
            "<!-- window:2026-10-01 -->\n"
        )
        copied = GOOD.replace(
            "嘴上还硬说这不算什么",
            "嘴上还硬说这不算什么。我本来做好磨半天的准备了，结果一次就跑通，尾巴都要翘起来了",
        )
        result = lint_mod.lint(DIGEST, copied, embedder=None, history=earlier)
        self.assertTrue(result["entries"][0]["reuse"], "near-verbatim reuse must be flagged")


class CliTests(unittest.TestCase):
    def test_json_output_is_serialisable_and_exit_code_matches(self):
        import subprocess

        script = ROOT / "scripts" / "journal_lint.py"
        proc = subprocess.run(
            [sys.executable, str(script), "--digest", str(FIXTURES / "digest_2026-03-14.md"),
             "--entry", str(FIXTURES / "entry_thin_2026-03-14.md"), "--no-semantic", "--json"],
            capture_output=True, text=True, encoding="utf-8",
        )
        self.assertEqual(proc.returncode, 1, proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["entries"][0]["coverage"]["total"], 4)

    def test_good_entry_exits_zero(self):
        import subprocess

        script = ROOT / "scripts" / "journal_lint.py"
        proc = subprocess.run(
            [sys.executable, str(script), "--digest", str(FIXTURES / "digest_2026-03-14.md"),
             "--entry", str(FIXTURES / "entry_good_2026-03-14.md"), "--no-semantic"],
            capture_output=True, text=True, encoding="utf-8",
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)


if __name__ == "__main__":
    unittest.main()
