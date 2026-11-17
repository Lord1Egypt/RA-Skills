"""Module H FYP Scaffolding Tests.

6 tests verifying FYP I/II AI scaffolding:
1. FYP I has 8 weeks of structured tasks
2. FYP II has 16 weeks (or 6 phase groups)
3. Each FYP week has task + ai_tools + output
4. AI role boundary (what AI can/cannot do)
5. Tracking metrics defined
6. Cross-disciplinary examples have primary + secondary major
"""
import json
import os
import pathlib
import sys
import unittest

SKILL_DIR = pathlib.Path(__file__).resolve().parent.parent
DATA_DIR = SKILL_DIR / "data"

os.environ["PYTHONIOENCODING"] = "utf-8"
sys.stdout.reconfigure(encoding="utf-8")


class TestModuleHFYP(unittest.TestCase):
    """V8.2-AIPC Module H · FYP Scaffolding (6 tests)."""

    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((DATA_DIR / "fyp_templates.json").read_text(encoding="utf-8"))

    def test_01_fyp_i_8_weeks(self):
        """[F1] FYP I has 8 weeks of structured tasks (W1-W8)."""
        fyp_i = self.data["fyp_i_templates"]["weeks_1_to_8"]
        self.assertEqual(len(fyp_i), 8, f"FYP I should have 8 weeks, got {len(fyp_i)}")
        # Verify W1-W8 are present
        for i in range(1, 9):
            self.assertIn(f"W{i}", fyp_i, f"FYP I missing W{i}")

    def test_02_fyp_ii_phase_groups(self):
        """[F2] FYP II has 6+ phase groups covering W1-W16."""
        fyp_ii = self.data["fyp_ii_templates"]["weeks_1_to_16"]
        self.assertGreaterEqual(len(fyp_ii), 6, f"FYP II should have >= 6 phase groups, got {len(fyp_ii)}")
        # Verify key phases present
        for phase in ["W1-4", "W5-8", "W9-12", "W14"]:
            self.assertIn(phase, fyp_ii, f"FYP II missing phase {phase}")

    def test_03_each_week_has_required_fields(self):
        """[F3] Each FYP week has task + ai_tools + output + duration_hours."""
        fyp_i = self.data["fyp_i_templates"]["weeks_1_to_8"]
        for week_id, week in fyp_i.items():
            for key in ("task", "ai_tools", "output", "duration_hours"):
                self.assertIn(key, week, f"FYP I {week_id} missing {key}")
            self.assertIsInstance(week["ai_tools"], list, f"FYP I {week_id} ai_tools should be a list")
            self.assertGreater(len(week["ai_tools"]), 0, f"FYP I {week_id} ai_tools empty")
        fyp_ii = self.data["fyp_ii_templates"]["weeks_1_to_16"]
        for week_id, week in fyp_ii.items():
            for key in ("task", "ai_tools", "output", "duration_hours"):
                self.assertIn(key, week, f"FYP II {week_id} missing {key}")

    def test_04_ai_role_boundary(self):
        """[F4] AI role boundary defines can_ai_do and need_human lists."""
        boundary = self.data["ai_role_boundary"]
        self.assertIn("can_ai_do", boundary, "Missing can_ai_do in ai_role_boundary")
        self.assertIn("need_human", boundary, "Missing need_human in ai_role_boundary")
        self.assertGreater(len(boundary["can_ai_do"]), 0, "can_ai_do list empty")
        self.assertGreater(len(boundary["need_human"]), 0, "need_human list empty")
        # Verify ethics red line: 学术诚信 must be in need_human
        all_human = " ".join(boundary["need_human"])
        self.assertIn("学术诚信", all_human, "need_human should include 学术诚信 (academic integrity)")

    def test_05_tracking_metrics_defined(self):
        """[F5] Tracking metrics for FYP completion, cross-disciplinary ratio, etc."""
        metrics = self.data["tracking_metrics"]
        expected_keys = ["fyp_completion_rate", "cross_disciplinary_fyp_ratio", "bozhifang_attendance", "student_initiated_cross_disciplinary_projects"]
        for key in expected_keys:
            self.assertIn(key, metrics, f"Missing tracking metric: {key}")
            self.assertIn("baseline", metrics[key], f"{key} missing baseline")
            self.assertIn("target", metrics[key], f"{key} missing target")

    def test_06_cross_disciplinary_examples(self):
        """[F6] Cross-disciplinary FYP examples have primary + secondary major + tools."""
        examples = self.data["cross_disciplinary_fyp_examples"]
        self.assertGreaterEqual(len(examples), 3, f"Should have >= 3 cross-disciplinary FYP examples, got {len(examples)}")
        for ex in examples:
            self.assertIn("title", ex, f"Example missing title")
            self.assertIn("primary_major", ex, f"Example '{ex.get('title')}' missing primary_major")
            self.assertIn("secondary_major", ex, f"Example '{ex.get('title')}' missing secondary_major")
            # Primary and secondary majors should be different
            self.assertNotEqual(ex["primary_major"], ex["secondary_major"], f"Example '{ex['title']}' has same primary and secondary")
            # Innovation and tools required
            self.assertIn("innovation", ex, f"Example '{ex['title']}' missing innovation")
            self.assertIn("tools", ex, f"Example '{ex['title']}' missing tools")


if __name__ == "__main__":
    unittest.main(verbosity=2)
