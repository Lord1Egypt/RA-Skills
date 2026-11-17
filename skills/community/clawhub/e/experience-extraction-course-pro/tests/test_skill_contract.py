import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
FRAMEWORK = ROOT / "references" / "course-development-framework.md"
FORMAT_SPEC = ROOT / "references" / "course-format-spec.md"


class SkillContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.skill_text = SKILL.read_text(encoding="utf-8")
        cls.framework_text = FRAMEWORK.read_text(encoding="utf-8")
        cls.format_text = FORMAT_SPEC.read_text(encoding="utf-8")
        cls.all_text = "\n".join(
            [cls.skill_text, cls.framework_text, cls.format_text]
        )

    def test_default_first_round_is_lightweight(self) -> None:
        self.assertIn("普通任务首轮默认不联网", self.skill_text)
        self.assertIn("最多 3 个关键问题", self.skill_text)
        self.assertIn("首轮不生成完整课件", self.skill_text)

    def test_models_are_conditionally_applied(self) -> None:
        self.assertIn("STAR 仅用于事件型资料", self.skill_text)
        self.assertIn("PRM 只深挖核心能力", self.skill_text)
        self.assertIn("不得为了套模型补造事实", self.skill_text)

    def test_depth_and_teaching_quality_chains_exist(self) -> None:
        self.assertIn("条件—判断—动作—结果—边界", self.all_text)
        self.assertIn("目标—方法—案例—练习—点评—应用", self.all_text)
        self.assertIn("合格标准", self.all_text)
        self.assertIn("优秀标准", self.all_text)

    def test_full_deliverables_are_on_demand(self) -> None:
        self.assertIn("完整交付物仅在用户明确要求后生成", self.skill_text)
        self.assertIn("题库数量按课程时长和用户要求确定", self.skill_text)

    def test_reference_loading_is_conditional(self) -> None:
        self.assertIn("按任务需要读取参考文件", self.skill_text)
        self.assertNotIn("开始任务前必须读取全部参考文件", self.skill_text)

    def test_long_material_is_fully_covered(self) -> None:
        self.assertIn("不得限页、限字或截断用户资料", self.skill_text)
        self.assertIn("分段只改变分析顺序，不减少资料范围", self.skill_text)
        self.assertIn("章节或页段", self.skill_text)
        self.assertIn("处理状态", self.skill_text)

    def test_user_facing_template_labels_are_chinese(self) -> None:
        forbidden_labels = (
            "**Title**",
            "**Subtitle**",
            "**Knowledge Points**",
            "**Key Takeaway**",
            "**Teaching Note**",
            "**Case**",
            "**Activity**",
        )
        for label in forbidden_labels:
            with self.subTest(label=label):
                self.assertNotIn(label, self.all_text)

    def test_main_instruction_is_compact(self) -> None:
        line_count = len(self.skill_text.splitlines())
        self.assertLessEqual(line_count, 420)


if __name__ == "__main__":
    unittest.main()
