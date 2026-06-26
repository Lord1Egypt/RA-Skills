"""
Test suite for Parenting Psychology Reasoning Engine
育儿心理学推理引擎测试 - 50+ 测试用例

运行: python3 -m pytest scripts/test_reasoning_engine.py -v
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from reasoning_engine import (
    CrisisDetector, UserIdentifier, EmotionAssessor, ScenarioMatcher,
    DefenseSignalDetector, DisplacementAnalyzer, ErrorPurposeDetector,
    ReasoningChainGenerator, ResponseGenerator, ExitDetector,
    ParentingReasoningEngine, create_engine, quick_analyze,
    CrisisLevel, UserRole, EmotionLevel, ResponseDepth, DefenseType, ErrorPurpose,
    CrisisResult, UserIdentity, EmotionState, ScenarioMatch,
    DefenseSignal, DisplacementAnalysis, ReasoningStep, ErrorPurposeResult, ReasoningResult,
)


class TestCrisisDetector(unittest.TestCase):
    def setUp(self):
        self.detector = CrisisDetector()

    def test_direct_suicide_keyword(self):
        result = self.detector.detect("孩子说他想死")
        self.assertEqual(result.level, CrisisLevel.DIRECT)
        self.assertIn("想死", result.matched_keywords)

    def test_direct_self_harm_keyword(self):
        result = self.detector.detect("她割腕了")
        self.assertEqual(result.level, CrisisLevel.DIRECT)

    def test_imminent_with_signal(self):
        result = self.detector.detect("她现在正在割腕")
        self.assertEqual(result.level, CrisisLevel.IMMINENT)
        self.assertTrue(result.has_imminent_signal)

    def test_imminent_prepared(self):
        result = self.detector.detect("他说准备好了要去死")
        self.assertEqual(result.level, CrisisLevel.IMMINENT)

    def test_single_metaphor(self):
        result = self.detector.detect("如果我不在了，大家会不会更好")
        self.assertEqual(result.level, CrisisLevel.METAPHOR)

    def test_two_metaphors_escalate(self):
        result = self.detector.detect("真的累了，如果我消失了也没人在乎")
        self.assertEqual(result.level, CrisisLevel.DIRECT)

    def test_no_crisis(self):
        result = self.detector.detect("今天天气不错")
        self.assertEqual(result.level, CrisisLevel.NONE)

    def test_empty_input(self):
        result = self.detector.detect("")
        self.assertEqual(result.level, CrisisLevel.NONE)

    def test_despair_keywords(self):
        result = self.detector.detect("活着没意思，想解脱")
        self.assertEqual(result.level, CrisisLevel.DIRECT)

    def test_exhaustion_keywords(self):
        result = self.detector.detect("撑不下去了，看不到尽头")
        self.assertEqual(result.level, CrisisLevel.DIRECT)


class TestUserIdentifier(unittest.TestCase):
    def setUp(self):
        self.identifier = UserIdentifier()

    def test_parent_signals(self):
        result = self.identifier.identify("我儿子最近不听话")
        self.assertEqual(result.role, UserRole.PARENT)

    def test_child_signals(self):
        result = self.identifier.identify("我爸总是骂我")
        self.assertEqual(result.role, UserRole.CHILD)

    def test_intermediary_signals(self):
        result = self.identifier.identify("我朋友的孩子不上学了")
        self.assertEqual(result.role, UserRole.INTERMEDIARY)

    def test_parent_multiple_signals(self):
        result = self.identifier.identify("我女儿不听话，我打了孩子")
        self.assertEqual(result.role, UserRole.PARENT)
        self.assertGreater(result.confidence, 0.7)

    def test_child_parent_keyword(self):
        result = self.identifier.identify("我家长不理解我")
        self.assertEqual(result.role, UserRole.CHILD)

    def test_unknown_role(self):
        result = self.identifier.identify("今天天气好")
        self.assertEqual(result.role, UserRole.UNKNOWN)

    def test_empty_input(self):
        result = self.identifier.identify("")
        self.assertEqual(result.role, UserRole.UNKNOWN)

    def test_intermediary_neighborhood(self):
        result = self.identifier.identify("邻居家小孩天天打游戏")
        self.assertEqual(result.role, UserRole.INTERMEDIARY)


class TestEmotionAssessor(unittest.TestCase):
    def setUp(self):
        self.assessor = EmotionAssessor()

    def test_high_distress_red(self):
        result = self.assessor.assess("我快崩溃了，受不了了")
        self.assertEqual(result.level, EmotionLevel.RED)

    def test_moderate_distress_yellow(self):
        # 注意: "怎么办" 属于 high_distress，用"迷茫"替代以测试纯 moderate_distress
        result = self.assessor.assess("我很焦虑，很迷茫")
        self.assertEqual(result.level, EmotionLevel.YELLOW)

    def test_anger_red(self):
        result = self.assessor.assess("气死了，发火吼了孩子")
        self.assertEqual(result.level, EmotionLevel.RED)

    def test_self_doubt_yellow(self):
        result = self.assessor.assess("我是不是做错了，我不是好妈妈")
        self.assertEqual(result.level, EmotionLevel.YELLOW)

    def test_green_calm(self):
        result = self.assessor.assess("我想了解一下育儿方法")
        self.assertEqual(result.level, EmotionLevel.GREEN)

    def test_empty_input(self):
        result = self.assessor.assess("")
        self.assertEqual(result.level, EmotionLevel.GREEN)

    def test_crisis_override_black(self):
        crisis = CrisisResult(level=CrisisLevel.DIRECT)
        result = self.assessor.assess("我很焦虑", crisis)
        self.assertEqual(result.level, EmotionLevel.BLACK)

    def test_response_depth_mapping(self):
        result = self.assessor.assess("崩溃了")
        self.assertEqual(result.response_depth, ResponseDepth.CRISIS)


class TestScenarioMatcher(unittest.TestCase):
    def setUp(self):
        self.matcher = ScenarioMatcher()

    def test_score_drop(self):
        result = self.matcher.match("孩子成绩下降了，考试不及格")
        self.assertIsNotNone(result)
        self.assertEqual(result.name, "孩子成绩下降")

    def test_school_refusal(self):
        result = self.matcher.match("孩子不想去学校，厌学")
        self.assertIsNotNone(result)
        self.assertEqual(result.name, "孩子不想上学")

    def test_phone_addiction(self):
        result = self.matcher.match("孩子沉迷游戏，天天玩手机")
        self.assertIsNotNone(result)
        self.assertEqual(result.name, "孩子沉迷手机游戏")

    def test_bullying(self):
        result = self.matcher.match("孩子在学校被欺负了")
        self.assertIsNotNone(result)
        self.assertEqual(result.name, "孩子被欺负霸凌")

    def test_crisis_scenario_priority_boost(self):
        result = self.matcher.match("孩子说想死")
        self.assertIsNotNone(result)
        self.assertEqual(result.priority, "crisis")
        self.assertGreater(result.confidence, 0.5)

    def test_no_match(self):
        result = self.matcher.match("今天天气很好")
        self.assertIsNone(result)

    def test_empty_input(self):
        result = self.matcher.match("")
        self.assertIsNone(result)

    def test_comparison_scenario(self):
        result = self.matcher.match("总是拿别人家孩子比较")
        self.assertIsNotNone(result)
        self.assertEqual(result.name, "比较")

    def test_self_harm_scenario(self):
        result = self.matcher.match("发现孩子划手腕")
        self.assertIsNotNone(result)
        self.assertEqual(result.name, "孩子自伤")

    def test_parent_burnout(self):
        result = self.matcher.match("当父母太累了，精疲力竭")
        self.assertIsNotNone(result)
        self.assertEqual(result.name, "父母倦怠")


class TestDefenseSignalDetector(unittest.TestCase):
    def setUp(self):
        self.detector = DefenseSignalDetector()

    def test_shame_defense(self):
        result = self.detector.detect("太丢人了，别人怎么看我们")
        self.assertTrue(any(d.defense_type == DefenseType.SHAME for d in result))

    def test_anxiety_defense(self):
        result = self.detector.detect("万一以后怎么办，来不及了")
        self.assertTrue(any(d.defense_type == DefenseType.ANXIETY for d in result))

    def test_control_defense(self):
        result = self.detector.detect("必须听我的，不准反驳")
        self.assertTrue(any(d.defense_type == DefenseType.CONTROL for d in result))

    def test_guilt_defense(self):
        result = self.detector.detect("都是我的错，我害了孩子")
        self.assertTrue(any(d.defense_type == DefenseType.GUILT for d in result))

    def test_no_defense(self):
        result = self.detector.detect("孩子最近学习有点吃力")
        self.assertEqual(len(result), 0)

    def test_multiple_defenses(self):
        result = self.detector.detect("都是我的错，太丢人了，万一以后怎么办")
        types = {d.defense_type for d in result}
        self.assertIn(DefenseType.GUILT, types)
        self.assertIn(DefenseType.SHAME, types)
        self.assertIn(DefenseType.ANXIETY, types)


class TestDisplacementAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = DisplacementAnalyzer()

    def test_score_scenario_template(self):
        scenario = ScenarioMatch(scenario_id="01", name="孩子成绩下降")
        result = self.analyzer.analyze("成绩下降", scenario, [], None)
        self.assertIn("不用功", result.parent_sees)
        self.assertIn("做不到", result.child_feels)

    def test_default_template(self):
        result = self.analyzer.analyze("有问题", None, [], None)
        self.assertIn("纠正", result.parent_sees)

    def test_defense_adjusted_gap(self):
        defenses = [DefenseSignal(defense_type=DefenseType.SHAME)]
        result = self.analyzer.analyze("丢人", None, defenses, None)
        self.assertIn("shame", result.gap_description)

    def test_phone_addiction_template(self):
        scenario = ScenarioMatch(scenario_id="10", name="孩子沉迷手机游戏")
        result = self.analyzer.analyze("沉迷游戏", scenario, [], None)
        self.assertIn("避难所", result.gap_description)


class TestErrorPurposeDetector(unittest.TestCase):
    def setUp(self):
        self.detector = ErrorPurposeDetector()

    def test_attention_purpose(self):
        result = self.detector.detect("孩子总是捣乱，故意引起注意")
        self.assertIsNotNone(result)
        self.assertEqual(result.purpose, ErrorPurpose.ATTENTION)

    def test_power_purpose(self):
        result = self.detector.detect("孩子顶嘴反抗，说什么都不听")
        self.assertIsNotNone(result)
        self.assertEqual(result.purpose, ErrorPurpose.POWER)

    def test_give_up_purpose(self):
        result = self.detector.detect("孩子说反正我不行，无所谓了")
        self.assertIsNotNone(result)
        self.assertEqual(result.purpose, ErrorPurpose.GIVE_UP)

    def test_no_purpose(self):
        result = self.detector.detect("孩子今天很开心")
        self.assertIsNone(result)


class TestExitDetector(unittest.TestCase):
    def setUp(self):
        self.detector = ExitDetector()

    def test_direct_exit(self):
        self.assertTrue(self.detector.detect("好了，不想聊了"))

    def test_thanks_exit(self):
        self.assertTrue(self.detector.detect("谢谢你的帮助"))

    def test_short_messages_exit(self):
        self.assertTrue(self.detector.detect("嗯", ["好的", "哦"]))

    def test_no_exit(self):
        self.assertFalse(self.detector.detect("我想聊聊孩子的问题"))


class TestFullPipeline(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine()

    def test_crisis_short_circuit(self):
        result = self.engine.process("我想自杀")
        self.assertEqual(result.crisis.level, CrisisLevel.DIRECT)
        self.assertIn("担心", result.response)

    def test_parent_score_scenario(self):
        result = self.engine.process("我儿子成绩下降了，考试不及格，我很焦虑")
        self.assertEqual(result.identity.role, UserRole.PARENT)
        self.assertIsNotNone(result.scenario)
        self.assertEqual(result.scenario.name, "孩子成绩下降")
        self.assertEqual(result.emotion.level, EmotionLevel.YELLOW)

    def test_child_role_pipeline(self):
        result = self.engine.process("我被打了，我爸总是发火吼我")
        self.assertEqual(result.identity.role, UserRole.CHILD)

    def test_defense_in_pipeline(self):
        result = self.engine.process("孩子考了60分，太丢人了，别人怎么看")
        self.assertTrue(any(d.defense_type == DefenseType.SHAME for d in result.defenses))

    def test_phone_scenario_with_displacement(self):
        result = self.engine.process("我女儿沉迷游戏，不自律")
        self.assertIsNotNone(result.scenario)
        self.assertIsNotNone(result.displacement)
        self.assertIn("避难所", result.displacement.gap_description)

    def test_imminent_crisis(self):
        result = self.engine.process("她现在正在割腕")
        self.assertEqual(result.crisis.level, CrisisLevel.IMMINENT)

    def test_reasoning_steps_generated(self):
        result = self.engine.process("孩子成绩下降了")
        self.assertGreater(len(result.reasoning_steps), 0)

    def test_follow_up_questions(self):
        result = self.engine.process("我女儿不想上学")
        self.assertGreater(len(result.follow_up_questions), 0)


class TestConversationProcessing(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine()

    def test_multi_message_conversation(self):
        messages = ["我儿子成绩下降了", "他以前成绩很好的", "现在天天玩游戏"]
        results = self.engine.process_conversation(messages)
        self.assertEqual(len(results), 3)
        self.assertIsNotNone(results[2].scenario)

    def test_empty_conversation(self):
        results = self.engine.process_conversation([])
        self.assertEqual(len(results), 0)


class TestEdgeCases(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine()

    def test_very_long_input(self):
        long_text = "孩子成绩下降了" * 100
        result = self.engine.process(long_text)
        self.assertIsNotNone(result)
        self.assertIsNotNone(result.response)

    def test_mixed_signals_crisis_and_parent(self):
        result = self.engine.process("我儿子说他想死，我快崩溃了")
        self.assertEqual(result.crisis.level, CrisisLevel.DIRECT)
        self.assertIn("担心", result.response)

    def test_only_whitespace(self):
        result = self.engine.process("   ")
        self.assertIsNotNone(result)

    def test_special_characters(self):
        result = self.engine.process("孩子成绩下降了！！！？？？")
        self.assertIsNotNone(result.scenario)

    def test_quick_analyze_function(self):
        result = quick_analyze("孩子沉迷游戏怎么办")
        self.assertIn("crisis_level", result)
        self.assertIn("response", result)
        self.assertEqual(result["scenario"], "孩子沉迷手机游戏")

    def test_all_defense_types_detected(self):
        texts = {
            DefenseType.SHAME: "太丢人了",
            DefenseType.ANXIETY: "万一以后怎么办",
            DefenseType.CONTROL: "必须听我的",
            DefenseType.PROJECTION: "我小时候也是这样",
            DefenseType.DENIAL: "没问题，挺好的",
            DefenseType.GUILT: "都是我的错",
        }
        for expected_type, text in texts.items():
            signals = DefenseSignalDetector().detect(text)
            self.assertTrue(
                any(d.defense_type == expected_type for d in signals),
                f"Failed to detect {expected_type} in '{text}'"
            )


class TestReasoningChainGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = ReasoningChainGenerator()

    def test_steps_include_crisis(self):
        crisis = CrisisResult(level=CrisisLevel.NONE, confidence=0.9)
        identity = UserIdentity(role=UserRole.PARENT, confidence=0.8)
        emotion = EmotionState(level=EmotionLevel.GREEN)
        steps = self.generator.generate(crisis, identity, emotion, None, [], None)
        self.assertTrue(any(s.step_name == "危机评估" for s in steps))

    def test_steps_include_defense_when_present(self):
        crisis = CrisisResult(level=CrisisLevel.NONE)
        identity = UserIdentity(role=UserRole.PARENT)
        emotion = EmotionState(level=EmotionLevel.GREEN)
        defenses = [DefenseSignal(defense_type=DefenseType.SHAME, confidence=0.8)]
        steps = self.generator.generate(crisis, identity, emotion, None, defenses, None)
        self.assertTrue(any(s.step_name == "防御分析" for s in steps))


class TestResponseGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = ResponseGenerator()

    def test_crisis_response_contains_resources(self):
        crisis = CrisisResult(level=CrisisLevel.DIRECT)
        response = self.generator.generate_crisis_response(crisis)
        self.assertIn("心理援助热线", response)

    def test_imminent_response_uses_worried_tone(self):
        crisis = CrisisResult(level=CrisisLevel.IMMINENT)
        response = self.generator.generate_crisis_response(crisis)
        self.assertIn("担心", response)


if __name__ == "__main__":
    unittest.main()
