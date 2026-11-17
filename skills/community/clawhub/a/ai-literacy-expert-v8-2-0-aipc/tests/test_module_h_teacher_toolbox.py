"""Module H Teacher Toolbox Tests.

6 tests verifying T2/T3/T4 teacher tools:
1. T2 4-piece suite (lesson prep / question gen / assessment / QA)
2. Each tool has time_savings metric
3. T2.3 has privacy protection
4. T2.1 integrates with V8.1-AIPC compose_lesson.py
5. T3 cross-disciplinary collaboration has 5 schools
6. T4 innovation has 4 categories and approval workflow
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


class TestModuleHTeacherToolbox(unittest.TestCase):
    """V8.2-AIPC Module H · Teacher Toolbox (6 tests)."""

    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((DATA_DIR / "teacher_toolbox_templates.json").read_text(encoding="utf-8"))

    def test_01_4_piece_suite_complete(self):
        """[TT1] T2 4-piece suite (lesson prep / question gen / assessment / QA) all present."""
        self.assertIn("t2_1_lesson_prep_assistant", self.data, "Missing T2.1 lesson prep")
        self.assertIn("t2_2_question_generation_assistant", self.data, "Missing T2.2 question gen")
        self.assertIn("t2_3_assessment_assistant", self.data, "Missing T2.3 assessment")
        self.assertIn("t2_4_qa_assistant", self.data, "Missing T2.4 QA")

    def test_02_time_savings_metrics(self):
        """[TT2] Each T2 tool has time_savings (savings_percent >= 50%)."""
        tools = [
            "t2_1_lesson_prep_assistant",
            "t2_2_question_generation_assistant",
            "t2_3_assessment_assistant",
            "t2_4_qa_assistant",
        ]
        for tool_key in tools:
            tool = self.data[tool_key]
            self.assertIn("time_savings", tool, f"{tool_key} missing time_savings")
            ts = tool["time_savings"]
            self.assertIn("savings_percent", ts, f"{tool_key} time_savings missing savings_percent")
            self.assertGreaterEqual(ts["savings_percent"], 50, f"{tool_key} savings should be >= 50%")

    def test_03_privacy_protection(self):
        """[TT3] T2.3 assessment has privacy protection (pii_redactor, no cloud upload)."""
        t23 = self.data["t2_3_assessment_assistant"]
        self.assertIn("privacy_protection", t23, "T2.3 missing privacy_protection")
        pp = t23["privacy_protection"]
        self.assertIn("student_answers", pp, "T2.3 privacy missing student_answers")
        self.assertIn("pii_redactor", pp["student_answers"], "T2.3 privacy should use pii_redactor")
        # Cloud policy must say no upload
        self.assertIn("cloud_policy", pp, "T2.3 privacy missing cloud_policy")
        self.assertIn("不上传", pp["cloud_policy"], "T2.3 cloud policy should state no upload")

    def test_04_lesson_prep_integrates_with_compose_lesson(self):
        """[TT4] T2.1 lesson prep integrates with V8.1-AIPC compose_lesson.py."""
        t21 = self.data["t2_1_lesson_prep_assistant"]
        self.assertIn("integration", t21, "T2.1 missing integration")
        self.assertIn("compose_lesson", t21["integration"], "T2.1 should integrate with compose_lesson")
        # Verify output format includes p5.js HTML
        self.assertIn("p5js_html", t21["output_format"], "T2.1 output should include p5js_html")

    def test_05_cross_disciplinary_5_schools(self):
        """[TT5] T3 has coordination_mechanism covering all 5 SAI programs."""
        t3 = self.data["t3_cross_disciplinary_collaboration"]
        self.assertIn("coordination_mechanism", t3, "T3 missing coordination_mechanism")
        meetings = t3["coordination_mechanism"]["monthly_meetings"]
        self.assertEqual(len(meetings), 5, f"T3 should have 5 program meetings, got {len(meetings)}")
        # Verify all 5 programs represented
        program_codes = {m["program"] for m in meetings}
        expected = {"CM+N", "DGC+N", "IBL+N", "Math+N", "IST+N"}
        self.assertEqual(program_codes, expected, f"T3 meetings should cover 5 programs, got {program_codes}")

    def test_06_innovation_categories_and_workflow(self):
        """[TT6] T4 has 4 innovation categories and 5-step approval workflow."""
        t4 = self.data["t4_teaching_innovation_support"]
        self.assertIn("innovation_categories", t4, "T4 missing innovation_categories")
        self.assertEqual(len(t4["innovation_categories"]), 4, f"T4 should have 4 innovation categories, got {len(t4['innovation_categories'])}")
        # Verify approval workflow has 5 steps
        self.assertIn("approval_workflow", t4, "T4 missing approval_workflow")
        self.assertEqual(len(t4["approval_workflow"]), 5, f"T4 approval should have 5 steps, got {len(t4['approval_workflow'])}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
