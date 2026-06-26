import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "run_flow.py"
SPEC = importlib.util.spec_from_file_location("run_flow_module", MODULE_PATH)
run_flow = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(run_flow)


class RunFlowTests(unittest.TestCase):
    def test_resolve_flow_name(self):
        self.assertEqual(run_flow.resolve_flow_name("流转"), "handoff-review")
        self.assertEqual(run_flow.resolve_flow_name("fanout"), "fanout-synthesis")

    def test_render_template_supports_nested_paths(self):
        context = {
            "input": {"title": "测试", "description": "描述"},
            "steps": {
                "plan": {
                    "content": "先拆解任务",
                    "summary": "拆解完成",
                }
            }
        }
        rendered = run_flow.render_template(
            "标题={{input.title}}; 内容={{steps.plan.content}}",
            context,
        )
        self.assertEqual(rendered, "标题=测试; 内容=先拆解任务")

    def test_parse_slot_assignments(self):
        slots = run_flow.parse_slot_assignments(["planner=产品", "executor=前端"])
        self.assertEqual(slots["planner"], "产品")
        self.assertEqual(slots["executor"], "前端")

    def test_build_combined_content(self):
        combined = run_flow.build_combined_content(
            [
                {"worker_name": "A", "worker_id": "a", "status": "done", "summary": "ok", "content": "内容1"},
                {"worker_name": "B", "worker_id": "b", "status": "done", "summary": "ok2", "content": "内容2"},
            ]
        )
        self.assertIn("[A/a]", combined)
        self.assertIn("内容2", combined)


if __name__ == "__main__":
    unittest.main()
