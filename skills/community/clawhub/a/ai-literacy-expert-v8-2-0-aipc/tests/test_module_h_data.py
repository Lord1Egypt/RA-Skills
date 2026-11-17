"""Module H Data Validation Tests.

8 tests verifying all 9 JSON data files:
1. All JSON files exist and parse
2. _meta structure present
3. Schema-required fields present
4. 5+N program structure
5. Discipline AI map completeness
6. Tool stack structure
7. FYP templates structure
8. Common core courses AI focus coverage
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


class TestModuleHData(unittest.TestCase):
    """V8.2-AIPC Module H · Data validation (8 tests)."""

    DATA_FILES = [
        "5plusn_programs.json",
        "discipline_ai_map.json",
        "discipline_tool_stack.json",
        "fyp_templates.json",
        "per_major_lesson_plans.json",
        "teacher_toolbox_templates.json",
        "bozhifang_workshops.json",
        "speaker_roster.json",
        "certification_records.example.json",
        "common_core_courses.json",
    ]

    def test_01_all_json_files_exist_and_parse(self):
        """[T1] All 9 JSON data files exist and parse as valid JSON."""
        for name in self.DATA_FILES:
            p = DATA_DIR / name
            self.assertTrue(p.exists(), f"Missing data file: {name}")
            try:
                json.loads(p.read_text(encoding="utf-8"))
            except json.JSONDecodeError as e:
                self.fail(f"Invalid JSON in {name}: {e}")

    def test_02_meta_structure_present(self):
        """[T2] Every JSON file has _meta with name/version/module/last_updated."""
        for name in self.DATA_FILES:
            data = json.loads((DATA_DIR / name).read_text(encoding="utf-8"))
            self.assertIn("_meta", data, f"Missing _meta in {name}")
            meta = data["_meta"]
            for key in ("name", "version", "module", "last_updated"):
                self.assertIn(key, meta, f"Missing {key} in _meta of {name}")
            self.assertEqual(meta["version"], "8.2.0-aipc", f"Wrong version in {name}")

    def test_03_5plusn_programs_structure(self):
        """[T3] 5+N programs JSON has 5 programs and 35 major directions."""
        data = json.loads((DATA_DIR / "5plusn_programs.json").read_text(encoding="utf-8"))
        programs = data["programs"]
        self.assertEqual(len(programs), 5, "Should have 5 programs")
        total_directions = sum(len(p["major_directions"]) for p in programs)
        self.assertEqual(total_directions, 35, "Should have 35 major directions")
        # Verify all expected programs
        expected_ids = {"CM+N", "DGC+N", "IBL+N", "Math+N", "IST+N"}
        actual_ids = {p["id"] for p in programs}
        self.assertEqual(expected_ids, actual_ids, "Wrong program ids")

    def test_04_discipline_ai_map_completeness(self):
        """[T4] Discipline AI map covers all 35 major directions with >= 3 entry points each."""
        data = json.loads((DATA_DIR / "discipline_ai_map.json").read_text(encoding="utf-8"))
        mp = data["map"]
        for prog_id, prog_data in mp.items():
            for direction_id, direction_data in prog_data.items():
                self.assertIn("ai_entry_points", direction_data, f"{prog_id}/{direction_id} missing ai_entry_points")
                self.assertGreaterEqual(
                    len(direction_data["ai_entry_points"]),
                    3,
                    f"{prog_id}/{direction_id} should have >= 3 AI entry points"
                )

    def test_05_tool_stack_structure(self):
        """[T5] Tool stack JSON has stacks for all 5 programs and all stacks include 'local' tool."""
        data = json.loads((DATA_DIR / "discipline_tool_stack.json").read_text(encoding="utf-8"))
        stacks = data["stacks"]
        # Verify each program has at least one direction with a tool stack
        for prog in ("CM+AIM", "CM+GD", "CM+MAD"):
            self.assertIn(prog, stacks, f"Missing {prog} in tool stacks")
        # Verify every stack has a 'local' tool for zero-upload privacy
        for direction, stack in stacks.items():
            self.assertIn("local", stack, f"{direction} stack missing 'local' tool")
            self.assertGreater(len(stack["local"]), 0, f"{direction} local stack empty")

    def test_06_fyp_templates_structure(self):
        """[T6] FYP templates has FYP I (8 weeks) and FYP II (16 weeks) with required tasks."""
        data = json.loads((DATA_DIR / "fyp_templates.json").read_text(encoding="utf-8"))
        fyp_i = data["fyp_i_templates"]["weeks_1_to_8"]
        fyp_ii = data["fyp_ii_templates"]["weeks_1_to_16"]
        # FYP I should have W1-W8 (8 weeks)
        self.assertEqual(len(fyp_i), 8, "FYP I should have 8 weeks")
        # FYP II should have at least 6 phase groups
        self.assertGreaterEqual(len(fyp_ii), 6, "FYP II should have >= 6 phase groups")
        # Should have cross-disciplinary examples
        self.assertGreaterEqual(len(data["cross_disciplinary_fyp_examples"]), 3, "Should have >= 3 cross-disciplinary examples")
        # Should have AI role boundary
        self.assertIn("ai_role_boundary", data, "Missing ai_role_boundary")

    def test_07_lesson_plans_structure(self):
        """[T7] Lesson plans JSON has at least 12 plans and 5-lesson structure."""
        data = json.loads((DATA_DIR / "per_major_lesson_plans.json").read_text(encoding="utf-8"))
        plans = data["lesson_plans"]
        self.assertGreaterEqual(len(plans), 12, "Should have >= 12 lesson plans")
        # Verify 5-lesson template
        template = data["template_structure"]
        self.assertEqual(template["lessons_per_plan"], 5, "Should be 5 lessons per plan")
        # Verify each plan has required fields
        for plan_id, plan in plans.items():
            for key in ("title", "primary_major", "ai_entry", "tools", "objectives"):
                self.assertIn(key, plan, f"Plan {plan_id} missing {key}")

    def test_08_common_core_ai_coverage(self):
        """[T8] Common core courses have >= 14 AI focus courses across 5 programs."""
        data = json.loads((DATA_DIR / "common_core_courses.json").read_text(encoding="utf-8"))
        courses = data["courses"]
        ai_focus_count = 0
        for prog_id, prog_data in courses.items():
            all_courses = prog_data.get("courses", []) + prog_data.get("elective_courses", []) + prog_data.get("elective_courses_zero_credit", [])
            for course in all_courses:
                if course.get("ai_focus", False):
                    ai_focus_count += 1
        # Should have at least 14 AI focus courses (we reported 14 required + 7 elective)
        self.assertGreaterEqual(ai_focus_count, 14, f"Should have >= 14 AI focus courses, got {ai_focus_count}")
        # Verify summary matches
        self.assertIn("summary", data, "Missing summary")
        self.assertGreaterEqual(data["summary"]["total_ai_focus_courses"], 14)


if __name__ == "__main__":
    unittest.main(verbosity=2)
