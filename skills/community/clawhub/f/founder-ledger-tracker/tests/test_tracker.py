"""Tests for skill-tracker/tracker.py — the founder-ledger-tracker skill.

Covers the worker acceptance contract from docs/NEW-SKILL-IDEAS-founder-ledger-tracker.md:
C1 unittest green + exit codes 0/1/2 demonstrated, C2 SKILL.md frontmatter
valid (incl. invalid-name rejection), C3 pricing-grep clean, C4 clean-room
(no reuse of mission pack text — verified by this file containing none).
"""
import json
import re
import subprocess
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL_DIR = HERE.parent
TRACKER = SKILL_DIR / "tracker.py"
SKILL_MD = SKILL_DIR / "SKILL.md"

sys.path.insert(0, str(SKILL_DIR))
import tracker  # noqa: E402


class EvaluateTests(unittest.TestCase):
    def test_no_triggers_is_exit_0(self):
        state = {"goal_name": "g", "goal_target": 100, "goal_current": 0}
        code, reasons = tracker._evaluate(state, date(2026, 1, 1))
        self.assertEqual(code, 0)
        self.assertEqual(reasons, [])

    def test_deadline_soft_trigger_within_3_days(self):
        state = {"goal_name": "g", "deadline": "2026-01-04"}
        code, reasons = tracker._evaluate(state, date(2026, 1, 1))
        self.assertEqual(code, 1)
        self.assertTrue(any("deadline" in r for r in reasons))

    def test_deadline_hard_trigger_when_passed(self):
        state = {"goal_name": "g", "deadline": "2025-12-31"}
        code, reasons = tracker._evaluate(state, date(2026, 1, 1))
        self.assertEqual(code, 2)
        self.assertTrue(any("passed" in r for r in reasons))

    def test_deadline_no_trigger_when_far_out(self):
        state = {"goal_name": "g", "deadline": "2026-06-01"}
        code, reasons = tracker._evaluate(state, date(2026, 1, 1))
        self.assertEqual(code, 0)
        self.assertEqual(reasons, [])

    def test_cap_soft_trigger_at_80_percent(self):
        state = {"goal_name": "g", "daily_cap": 100, "spent_today": 80}
        code, reasons = tracker._evaluate(state, date(2026, 1, 1))
        self.assertEqual(code, 1)

    def test_cap_no_trigger_below_80_percent(self):
        state = {"goal_name": "g", "daily_cap": 100, "spent_today": 79.99}
        code, reasons = tracker._evaluate(state, date(2026, 1, 1))
        self.assertEqual(code, 0)

    def test_cap_hard_trigger_at_cap(self):
        state = {"goal_name": "g", "daily_cap": 100, "spent_today": 100}
        code, reasons = tracker._evaluate(state, date(2026, 1, 1))
        self.assertEqual(code, 2)

    def test_cap_hard_trigger_over_cap(self):
        state = {"goal_name": "g", "daily_cap": 100, "spent_today": 150}
        code, reasons = tracker._evaluate(state, date(2026, 1, 1))
        self.assertEqual(code, 2)

    def test_combined_triggers_take_worst_code(self):
        # soft deadline + hard cap -> hard (2) wins
        state = {
            "goal_name": "g",
            "deadline": "2026-01-02",
            "daily_cap": 100,
            "spent_today": 100,
        }
        code, reasons = tracker._evaluate(state, date(2026, 1, 1))
        self.assertEqual(code, 2)
        self.assertEqual(len(reasons), 2)

    def test_goal_reached_recorded_as_reason_without_forcing_a_code(self):
        state = {"goal_name": "first dollar", "goal_target": 1, "goal_current": 1}
        code, reasons = tracker._evaluate(state, date(2026, 1, 1))
        self.assertEqual(code, 0)
        self.assertTrue(any("goal 'first dollar' reached" in r for r in reasons))


class CliIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.state = str(Path(self.tmp.name) / "state.json")

    def tearDown(self):
        self.tmp.cleanup()

    def _run(self, *args):
        return subprocess.run(
            [sys.executable, str(TRACKER), *args],
            capture_output=True,
            text=True,
        )

    def test_init_creates_state_file(self):
        r = self._run(
            "init", "--state", self.state, "--goal-name", "first $1", "--goal-target", "1"
        )
        self.assertEqual(r.returncode, 0)
        self.assertTrue(Path(self.state).exists())
        data = json.loads(Path(self.state).read_text())
        self.assertEqual(data["goal_name"], "first $1")

    def test_init_refuses_to_overwrite_without_force(self):
        self._run("init", "--state", self.state, "--goal-name", "g", "--goal-target", "1")
        r = self._run("init", "--state", self.state, "--goal-name", "g2", "--goal-target", "2")
        self.assertEqual(r.returncode, 1)
        data = json.loads(Path(self.state).read_text())
        self.assertEqual(data["goal_name"], "g")  # untouched

    def test_init_force_overwrites(self):
        self._run("init", "--state", self.state, "--goal-name", "g", "--goal-target", "1")
        r = self._run(
            "init", "--state", self.state, "--goal-name", "g2", "--goal-target", "2", "--force"
        )
        self.assertEqual(r.returncode, 0)
        data = json.loads(Path(self.state).read_text())
        self.assertEqual(data["goal_name"], "g2")

    def test_check_missing_state_exits_2(self):
        r = self._run("check", "--state", self.state)
        self.assertEqual(r.returncode, 2)
        self.assertIn("not found", r.stderr)

    def test_check_exit_code_0_1_2_end_to_end(self):
        self._run(
            "init",
            "--state",
            self.state,
            "--goal-name",
            "milestone",
            "--goal-target",
            "1000",
            "--deadline",
            "2026-09-10",
        )
        r0 = self._run("check", "--state", self.state, "--today", "2026-08-01")
        self.assertEqual(r0.returncode, 0)
        r1 = self._run("check", "--state", self.state, "--today", "2026-09-08")
        self.assertEqual(r1.returncode, 1)
        r2 = self._run("check", "--state", self.state, "--today", "2026-09-11")
        self.assertEqual(r2.returncode, 2)

    def test_check_spent_flag_persists_to_state(self):
        self._run(
            "init", "--state", self.state, "--goal-name", "g", "--goal-target", "1",
            "--daily-cap", "100",
        )
        self._run("check", "--state", self.state, "--spent", "90")
        data = json.loads(Path(self.state).read_text())
        self.assertEqual(data["spent_today"], 90)

    def test_reminder_text_does_not_mutate_state_and_exits_0(self):
        self._run(
            "init", "--state", self.state, "--goal-name", "g", "--goal-target", "1",
            "--daily-cap", "100", "--spent-today", "150",
        )
        before = Path(self.state).read_text()
        r = self._run("reminder-text", "--state", self.state, "--today", "2026-01-01")
        after = Path(self.state).read_text()
        self.assertEqual(r.returncode, 0)
        self.assertEqual(before, after)
        self.assertIn("alert", r.stdout)


class SkillMdFrontmatterTests(unittest.TestCase):
    """C2: validate SKILL.md frontmatter without a YAML dependency (stdlib-only)."""

    NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")

    @staticmethod
    def _frontmatter_field(text, field):
        m = re.search(rf"^{field}:\s*(.+)$", text, re.M)
        return m.group(1).strip() if m else None

    def test_skill_md_exists_with_frontmatter_block(self):
        self.assertTrue(SKILL_MD.exists())
        text = SKILL_MD.read_text()
        self.assertTrue(text.startswith("---\n"))
        self.assertGreaterEqual(text.count("---\n"), 2)

    def test_name_field_passes_clawhub_slug_pattern(self):
        text = SKILL_MD.read_text()
        name = self._frontmatter_field(text, "name")
        self.assertIsNotNone(name)
        self.assertRegex(name, self.NAME_RE)

    def test_description_field_present_and_nonempty(self):
        text = SKILL_MD.read_text()
        desc = self._frontmatter_field(text, "description")
        self.assertTrue(desc)

    def test_invalid_names_are_rejected_by_the_slug_pattern(self):
        for bad in ["Invalid Name!", "UPPERCASE", "-leading-hyphen", "has space", "trailing-!"]:
            self.assertNotRegex(bad, self.NAME_RE, msg=f"{bad!r} should be rejected")

    def test_no_pricing_or_payment_wording(self):
        text = SKILL_MD.read_text()
        self.assertNotRegex(text, re.compile(r"price|pricing|tip|donate|payment", re.I))


if __name__ == "__main__":
    unittest.main()
