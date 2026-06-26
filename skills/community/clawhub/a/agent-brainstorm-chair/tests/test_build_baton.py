import importlib.util
import pathlib
import sys
import unittest

MODULE_PATH = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "build_baton.py"
SPEC = importlib.util.spec_from_file_location("build_baton", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class BuildBatonTests(unittest.TestCase):
    def test_middle_round_baton_keeps_facilitator_moving(self) -> None:
        spec = MODULE.BatonSpec(
            round_no=1,
            round_total=3,
            speaker="executor",
            next_speaker="facilitator",
            final_speaker="executor",
            facilitator="facilitator",
            topic="主体债券库审批边界",
            mode="discussion",
            focus="rebuttal",
            custom_ask="请承接上一棒补充限制条件。",
        )

        output = MODULE.build_baton(spec)

        self.assertIn("第 1/3 轮", output)
        self.assertIn("本轮顺序：executor -> facilitator", output)
        self.assertIn("回收主持：facilitator", output)
        self.assertIn("当前还未到最终轮次时，只允许主持人开启下一轮", output)
        self.assertIn("[[mention:executor]]", output)
        self.assertIn("[[next:facilitator]]", output)
        self.assertNotIn("答完后交回facilitator", output)
        self.assertNotIn("是否有下一步议题", output)

    def test_custom_mention_template(self) -> None:
        spec = MODULE.BatonSpec(
            round_no=1,
            round_total=2,
            speaker="alice",
            next_speaker="bob",
            final_speaker="bob",
            facilitator="facilitator",
            topic="test topic",
            mode="discussion",
            focus="auto",
            custom_ask="",
        )
        output = MODULE.build_baton(spec, mention_tpl="<@{{speaker}}>", next_tpl="→ {{speaker}}")
        self.assertIn("<@alice>", output)
        self.assertIn("→ bob", output)
        self.assertNotIn("[[mention:", output)

    def test_facilitator_as_next_speaker_is_final_baton(self) -> None:
        spec = MODULE.BatonSpec(
            round_no=2,
            round_total=3,
            speaker="strategist",
            next_speaker="facilitator",
            final_speaker="strategist",
            facilitator="facilitator",
            topic="test",
            mode="discussion",
            focus="auto",
            custom_ask="",
        )
        output = MODULE.build_baton(spec)
        self.assertIn("回收主持", output)
        self.assertIn("不要自行总结整轮或开启下一轮", output)


if __name__ == "__main__":
    unittest.main()
