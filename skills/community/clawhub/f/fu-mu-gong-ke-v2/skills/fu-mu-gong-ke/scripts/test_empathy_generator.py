#!/usr/bin/env python3
"""
Test suite for Empathy Generator v1.0.0
共情生成器测试套件
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from empathy_generator import (
    EmpathyGenerator, EmotionClassifier, EmpathyLevelRouter,
    EmpathyTrapChecker, EmpathyBalancer, ScenarioDetector,
    EmpathyQualityAssessor, EmpathyLevel, EmpathyTrap,
    EmpathyScenario, EmotionInput,
)


class TestEmotionClassifier:
    """情绪分类器测试"""

    def setup_method(self):
        self.clf = EmotionClassifier()

    def test_anger_detection(self):
        result = self.clf.classify("我气死了，孩子太不听话了")
        assert result.primary_emotion == "anger"
        assert result.intensity > 5.0

    def test_sadness_detection(self):
        result = self.clf.classify("我好难过，心都碎了")
        assert result.primary_emotion == "sadness"

    def test_anxiety_detection(self):
        result = self.clf.classify("我好焦虑，担心孩子以后怎么办")
        assert result.primary_emotion == "anxiety"

    def test_guilt_detection(self):
        result = self.clf.classify("我打了孩子，都是我的错，我很内疚")
        assert result.primary_emotion == "guilt"

    def test_exhaustion_detection(self):
        result = self.clf.classify("我真的撑不住了，太累了")
        assert result.primary_emotion == "exhaustion"

    def test_helplessness_detection(self):
        result = self.clf.classify("我不知道怎么办，完全无助")
        assert result.primary_emotion == "helplessness"

    def test_default_emotion(self):
        result = self.clf.classify("今天天气不错")
        assert result.primary_emotion == "default"
        assert result.intensity == 3.0

    def test_secondary_emotions(self):
        result = self.clf.classify("我又生气又难过，不知道怎么办")
        assert len(result.secondary_emotions) > 0

    def test_intensity_markers(self):
        low = self.clf.classify("有点焦虑")
        high = self.clf.classify("我真的非常极其焦虑")
        assert high.intensity >= low.intensity

    def test_valence_negative(self):
        result = self.clf.classify("我好难过")
        assert result.valence < 0


class TestEmpathyLevelRouter:
    """共情层次路由测试"""

    def setup_method(self):
        self.router = EmpathyLevelRouter()

    def test_crisis_goes_acceptance(self):
        emotion = EmotionInput(is_crisis=True, intensity=10.0)
        assert self.router.route(emotion) == EmpathyLevel.ACCEPTANCE

    def test_high_intensity_goes_understanding(self):
        emotion = EmotionInput(intensity=8.0)
        assert self.router.route(emotion) == EmpathyLevel.UNDERSTANDING

    def test_medium_intensity_goes_support(self):
        emotion = EmotionInput(intensity=6.0)
        assert self.router.route(emotion) == EmpathyLevel.SUPPORT

    def test_low_intensity_goes_empowerment(self):
        emotion = EmotionInput(intensity=3.0)
        assert self.router.route(emotion) == EmpathyLevel.EMPOWERMENT


class TestEmpathyTrapChecker:
    """共情陷阱检测测试"""

    def setup_method(self):
        self.checker = EmpathyTrapChecker()

    def test_pseudo_empathy(self):
        traps = self.checker.check("我理解你。")
        assert any(t.trap_type == EmpathyTrap.PSEUDO_EMPATHY for t in traps)

    def test_judgmental(self):
        traps = self.checker.check("你不应该这样想")
        assert any(t.trap_type == EmpathyTrap.JUDGMENTAL for t in traps)

    def test_fixing(self):
        traps = self.checker.check("你应该这样做：第一步先道歉")
        assert any(t.trap_type == EmpathyTrap.FIXING for t in traps)

    def test_comparing(self):
        traps = self.checker.check("至少你还有孩子，比那些没孩子的好")
        assert any(t.trap_type == EmpathyTrap.COMPARING for t in traps)

    def test_minimizing(self):
        traps = self.checker.check("没那么严重，想太多了")
        assert any(t.trap_type == EmpathyTrap.MINIMIZING for t in traps)

    def test_toxic_positivity(self):
        traps = self.checker.check("往好处想，一切都会好的")
        assert any(t.trap_type == EmpathyTrap.TOXIC_POSITIVITY for t in traps)

    def test_blame_shifting(self):
        traps = self.checker.check("你也有问题，你自己想想")
        assert any(t.trap_type == EmpathyTrap.BLAME_SHIFTING for t in traps)

    def test_no_trap_on_good_empathy(self):
        traps = self.checker.check("我听到你的愤怒了，这种感受是真实的。你有权利生气。")
        assert len(traps) == 0

    def test_harmful_phrases(self):
        found = self.checker.check_harmful_phrases("你应该爱孩子")
        assert len(found) > 0
        assert found[0][1] == "我看到你在努力，这很不容易"

    def test_no_harmful_phrases(self):
        found = self.checker.check_harmful_phrases("我听到你了，你的感受是真实的")
        assert len(found) == 0


class TestEmpathyBalancer:
    """共情平衡测试"""

    def setup_method(self):
        self.balancer = EmpathyBalancer()

    def test_balanced_text(self):
        text = "我听到你的感受了，这真的很不容易。你可以试试和孩子谈谈。"
        result = self.balancer.analyze(text)
        assert result.is_balanced is True

    def test_too_much_advice(self):
        text = "你应该这样做。建议第一步道歉。第二步沟通。第三步制定规则。"
        result = self.balancer.analyze(text)
        assert result.is_balanced is False

    def test_empty_text(self):
        result = self.balancer.analyze("")
        assert result.is_balanced is True

    def test_pure_empathy(self):
        text = "我感受到你的痛苦了。你不是一个人。我在这里陪伴你。"
        result = self.balancer.analyze(text)
        assert result.empathy_ratio > 0.5


class TestScenarioDetector:
    """场景检测测试"""

    def setup_method(self):
        self.detector = ScenarioDetector()

    def test_guilt_scenario(self):
        assert self.detector.detect("我打了孩子，很内疚") == EmpathyScenario.PARENT_GUILT

    def test_exhaustion_scenario(self):
        assert self.detector.detect("我太累了，精疲力竭") == EmpathyScenario.EXHAUSTION

    def test_communication_break(self):
        assert self.detector.detect("孩子不跟我说话，拒绝沟通") == EmpathyScenario.COMMUNICATION_BREAK

    def test_general_scenario(self):
        assert self.detector.detect("今天天气不错") == EmpathyScenario.GENERAL


class TestEmpathyGenerator:
    """主引擎集成测试"""

    def setup_method(self):
        self.gen = EmpathyGenerator()

    def test_generate_basic(self):
        result = self.gen.generate("我好焦虑，担心孩子成绩")
        assert result.full_response != ""
        assert result.quality_score > 0
        assert result.level in EmpathyLevel

    def test_generate_high_intensity(self):
        result = self.gen.generate("我真的撑不住了，崩溃了")
        assert result.level in (EmpathyLevel.ACCEPTANCE, EmpathyLevel.UNDERSTANDING)

    def test_generate_low_intensity(self):
        result = self.gen.generate("孩子最近有点不听话")
        assert result.level in (EmpathyLevel.SUPPORT, EmpathyLevel.EMPOWERMENT)

    def test_check_existing_response_good(self):
        result = self.gen.check_existing_response(
            "我听到你的愤怒了，这种感受是真实的。你有权利生气。"
        )
        assert result["quality_score"] > 0

    def test_check_existing_response_bad(self):
        result = self.gen.check_existing_response(
            "你不应该这样想。你应该爱孩子。往好处想。"
        )
        assert result["has_issues"] is True
        assert len(result["traps"]) > 0

    def test_follow_up_questions(self):
        result = self.gen.generate("孩子不跟我说话")
        assert len(result.follow_up_questions) > 0

    def test_techniques_used(self):
        result = self.gen.generate("我好难过，心都碎了")
        assert len(result.techniques_used) > 0

    def test_quality_score_range(self):
        texts = [
            "我好焦虑",
            "我真的撑不住了",
            "孩子不听话",
            "我打了孩子很后悔",
        ]
        for text in texts:
            result = self.gen.generate(text)
            assert 0 <= result.quality_score <= 10


class TestEmpathyQualityAssessor:
    """质量评估测试"""

    def setup_method(self):
        self.assessor = EmpathyQualityAssessor()
        self.balancer = EmpathyBalancer()

    def test_good_empathy_scores_high(self):
        text = "我听到你的愤怒了。你有权利生气。这种愤怒背后是深深的在乎。"
        balance = self.balancer.analyze(text)
        score = self.assessor.assess(text, balance)
        assert score >= 5.0

    def test_judgmental_scores_low(self):
        text = "你不应该这样想。你应该这样做。"
        balance = self.balancer.analyze(text)
        score = self.assessor.assess(text, balance)
        assert score < 7.0


def run_all_tests():
    """运行所有测试"""
    test_classes = [
        TestEmotionClassifier,
        TestEmpathyLevelRouter,
        TestEmpathyTrapChecker,
        TestEmpathyBalancer,
        TestScenarioDetector,
        TestEmpathyGenerator,
        TestEmpathyQualityAssessor,
    ]

    total = 0
    passed = 0
    failed = 0

    for cls in test_classes:
        print(f"\n--- {cls.__name__} ---")
        instance = cls()
        methods = [m for m in dir(instance) if m.startswith("test_")]
        for method_name in methods:
            total += 1
            try:
                if hasattr(instance, "setup_method"):
                    instance.setup_method()
                getattr(instance, method_name)()
                print(f"  ✅ {method_name}")
                passed += 1
            except Exception as e:
                print(f"  ❌ {method_name}: {e}")
                failed += 1

    print(f"\n=== 测试结果 ===")
    print(f"总计: {total} | 通过: {passed} | 失败: {failed}")
    print(f"通过率: {passed/total*100:.1f}%")
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
