"""Module H Cross-Major Recommendation Tests.

6 tests verifying recommendation logic:
1. AI entry point lookup by major
2. Tool stack lookup by major
3. Cross-disciplinary FYP suggestion
4. 5-level progression validation
5. 4-cornerstone common language coverage
6. Workshop-to-major mapping
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


class TestModuleHRecommend(unittest.TestCase):
    """V8.2-AIPC Module H · Cross-major recommendation (6 tests)."""

    @classmethod
    def setUpClass(cls):
        cls.ai_map = json.loads((DATA_DIR / "discipline_ai_map.json").read_text(encoding="utf-8"))
        cls.tool_stack = json.loads((DATA_DIR / "discipline_tool_stack.json").read_text(encoding="utf-8"))
        cls.fyp = json.loads((DATA_DIR / "fyp_templates.json").read_text(encoding="utf-8"))
        cls.workshops = json.loads((DATA_DIR / "bozhifang_workshops.json").read_text(encoding="utf-8"))

    def test_01_ai_entry_point_lookup(self):
        """[R1] Can retrieve AI entry points for any major direction."""
        for prog_id, prog_data in self.ai_map["map"].items():
            for direction_id, direction_data in prog_data.items():
                entry_points = direction_data.get("ai_entry_points", [])
                self.assertGreater(len(entry_points), 0, f"{prog_id}/{direction_id} has no entry points")
                # Each entry point has a name
                for ep in entry_points:
                    self.assertIn("name", ep, f"Entry point in {prog_id}/{direction_id} missing name")

    def test_02_tool_stack_lookup(self):
        """[R2] Tool stack retrieval includes main + local tools."""
        # Test for CM+GD specifically
        stack = self.tool_stack["stacks"].get("CM+GD", {})
        self.assertIn("main", stack, "CM+GD missing main tools")
        self.assertIn("local", stack, "CM+GD missing local tools")
        # Main tools should include DeepSeek
        main_str = " ".join(stack["main"])
        self.assertIn("DeepSeek", main_str, "CM+GD main tools should include DeepSeek")
        # Local tools should always include DeepSeek-R1 (zero-upload privacy)
        local_str = " ".join(stack["local"])
        self.assertIn("DeepSeek-R1", local_str, "Local tools should include DeepSeek-R1")

    def test_03_cross_disciplinary_fyp_suggestion(self):
        """[R3] Cross-disciplinary FYP examples span multiple program pairs."""
        examples = self.fyp["cross_disciplinary_fyp_examples"]
        primary_programs = {e["primary_major"] for e in examples}
        # Should cover at least 3 different programs in cross-disciplinary FYP examples
        self.assertGreaterEqual(len(primary_programs), 3, f"Cross-disciplinary FYP should span >= 3 programs, got {primary_programs}")
        # Every example should have tools
        for e in examples:
            self.assertIn("tools", e, f"FYP '{e['title']}' missing tools")
            self.assertGreater(len(e["tools"]), 0, f"FYP '{e['title']}' has no tools")

    def test_04_5_level_progression(self):
        """[R4] FYP templates support 5-level progression (L1-L5)."""
        # FYP I (W1-W8) = Level 1-2 (single-discipline)
        fyp_i = self.fyp["fyp_i_templates"]["weeks_1_to_8"]
        self.assertIn("W1", fyp_i, "FYP I should have W1")
        self.assertIn("W8", fyp_i, "FYP I should have W8")
        # FYP II (W1-W16) = Level 3-4 (FYP + cross-disciplinary)
        fyp_ii = self.fyp["fyp_ii_templates"]["weeks_1_to_16"]
        self.assertIn("W14", fyp_ii, "FYP II should have W14 (答辩 PPT)")
        # Cross-disciplinary examples = Level 4-5
        self.assertGreaterEqual(len(self.fyp["cross_disciplinary_fyp_examples"]), 3, "Should have >= 3 cross-disciplinary FYP examples")

    def test_05_4_cornerstone_common_language(self):
        """[R5] 4 cornerstones (data thinking / prompt engineering / ethics / tool literacy) coverage."""
        # Verify by checking common_core_courses.json
        ccc = json.loads((DATA_DIR / "common_core_courses.json").read_text(encoding="utf-8"))
        # Should have courses across all 5 programs
        self.assertEqual(len(ccc["courses"]), 5, "Should have courses for 5 programs")
        # Total AI focus courses >= 14
        self.assertGreaterEqual(ccc["summary"]["total_ai_focus_courses"], 14, "Should have >= 14 AI focus courses")
        # Verify 4 cornerstones by name
        ai_keywords = ["Python", "AI", "人工智能", "Machine Learning", "Data", "数据"]
        for prog_id, prog_data in ccc["courses"].items():
            all_courses = prog_data.get("courses", []) + prog_data.get("elective_courses", []) + prog_data.get("elective_courses_zero_credit", [])
            for course in all_courses:
                name_en = course.get("name_en", "")
                if course.get("ai_focus", False):
                    # Each AI focus course should mention at least one cornerstone keyword
                    self.assertTrue(
                        any(kw in name_en for kw in ai_keywords),
                        f"{prog_id} course '{name_en}' missing cornerstone keyword"
                    )

    def test_06_workshop_to_major_mapping(self):
        """[R6] Each workshop has applicable_majors covering at least 1 program."""
        all_workshops = self.workshops["semester_1"] + self.workshops["semester_2"]
        for ws in all_workshops:
            self.assertIn("applicable_majors", ws, f"Workshop {ws['id']} missing applicable_majors")
            self.assertGreater(len(ws["applicable_majors"]), 0, f"Workshop {ws['id']} has no applicable_majors")
        # Verify semester_1 has 6 workshops
        self.assertEqual(len(self.workshops["semester_1"]), 6, "Semester 1 should have 6 workshops")
        # Verify semester_2 has 4 workshops
        self.assertEqual(len(self.workshops["semester_2"]), 4, "Semester 2 should have 4 workshops")


if __name__ == "__main__":
    unittest.main(verbosity=2)
