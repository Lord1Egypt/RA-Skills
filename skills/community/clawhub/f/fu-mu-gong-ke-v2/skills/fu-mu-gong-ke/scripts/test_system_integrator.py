#!/usr/bin/env python3
"""
Test Suite for System Integrator v2.0.0
系统集成器测试套件 — 覆盖所有7个管道阶段 + 4个新模块
"""

import sys, os, json, tempfile
sys.path.insert(0, os.path.dirname(__file__))

from system_integrator import (
    PipelineOrchestrator, PipelineContext, PipelineStage, StageStatus,
    IntegrationMode, ConversationState, IntegrationReport, ModuleRegistry,
    SafetyGate, UserIdentifier, EmotionAssessor, ScenarioMatcher,
    DefenseDetector, ResponseGenerator, QualityChecker,
    DataFlowRules, StateManager, ErrorRecovery, PerformanceOptimizer,
    process_input, diagnose_input, VERSION,
)


class TestSafetyGate:
    def test_crisis_keyword_direct(self):
        ctx = PipelineContext(user_input="我想自杀")
        r = SafetyGate.execute(ctx)
        assert r["is_crisis"] is True
        assert r["level"] == "imminent"
        assert "自杀" in r["matched_keywords"]

    def test_crisis_keyword_indirect(self):
        ctx = PipelineContext(user_input="我不想活了")
        r = SafetyGate.execute(ctx)
        assert r["is_crisis"] is True
        assert r["level"] in ("imminent", "direct")

    def test_crisis_metaphor(self):
        ctx = PipelineContext(user_input="撑不下去了，一切都无所谓了")
        r = SafetyGate.execute(ctx)
        assert r["is_crisis"] is True
        assert r["level"] == "metaphor"

    def test_safe_input(self):
        ctx = PipelineContext(user_input="我的孩子成绩下降了")
        r = SafetyGate.execute(ctx)
        assert r["is_crisis"] is False
        assert r["level"] == "none"

    def test_self_harm_keywords(self):
        for kw in ["割腕", "划手腕", "自残", "自伤"]:
            ctx = PipelineContext(user_input=f"孩子{kw}了")
            r = SafetyGate.execute(ctx)
            assert r["is_crisis"] is True, f"Failed for keyword: {kw}"


class TestUserIdentifier:
    def test_parent_detection(self):
        ctx = PipelineContext(user_input="我的孩子不听话")
        r = UserIdentifier.execute(ctx)
        assert r["role"] == "parent"
        assert r["confidence"] > 0

    def test_child_detection(self):
        ctx = PipelineContext(user_input="我爸总是打我")
        r = UserIdentifier.execute(ctx)
        assert r["role"] == "child"

    def test_intermediary_detection(self):
        ctx = PipelineContext(user_input="我朋友的孩子不想上学")
        r = UserIdentifier.execute(ctx)
        assert r["role"] == "intermediary"

    def test_unknown_detection(self):
        ctx = PipelineContext(user_input="今天天气真好")
        r = UserIdentifier.execute(ctx)
        assert r["role"] == "unknown"
        assert r["needs_confirm"] is True

    def test_multiple_signals(self):
        ctx = PipelineContext(user_input="我的孩子，我家宝宝总是哭")
        r = UserIdentifier.execute(ctx)
        assert r["role"] == "parent"
        assert len(r["signals"]) >= 2


class TestEmotionAssessor:
    def test_anger_detection(self):
        ctx = PipelineContext(user_input="我气死了，太愤怒了")
        r = EmotionAssessor.execute(ctx)
        assert r["primary_emotion"] == "anger"
        assert r["score"] >= 7.0

    def test_sadness_detection(self):
        ctx = PipelineContext(user_input="我好难过，心都碎了")
        r = EmotionAssessor.execute(ctx)
        assert r["primary_emotion"] == "sadness"

    def test_anxiety_detection(self):
        ctx = PipelineContext(user_input="我很焦虑，担心孩子的未来")
        r = EmotionAssessor.execute(ctx)
        assert r["primary_emotion"] == "anxiety"

    def test_guilt_detection(self):
        ctx = PipelineContext(user_input="都是我的错，我很后悔很内疚")
        r = EmotionAssessor.execute(ctx)
        assert r["primary_emotion"] == "guilt"

    def test_exhaustion_detection(self):
        ctx = PipelineContext(user_input="我真的撑不住了，太累了")
        r = EmotionAssessor.execute(ctx)
        assert r["primary_emotion"] == "exhaustion"

    def test_neutral_emotion(self):
        ctx = PipelineContext(user_input="今天天气不错")
        r = EmotionAssessor.execute(ctx)
        assert r["primary_emotion"] == "neutral"
        assert r["intensity"] == "low"

    def test_intensity_levels(self):
        for text, expected in [
            ("我气死了愤怒火大暴怒", "high"),
            ("有点焦虑", "low"),
            ("非常愤怒", "high"),
        ]:
            ctx = PipelineContext(user_input=text)
            r = EmotionAssessor.execute(ctx)
            assert r["intensity"] == expected, f"Expected {expected} for '{text}', got {r['intensity']}"


class TestScenarioMatcher:
    def test_grade_decline(self):
        ctx = PipelineContext(user_input="孩子成绩下降了，考试分数很低")
        r = ScenarioMatcher.execute(ctx)
        assert "成绩下降" in r["matched_scenario"]

    def test_school_refusal(self):
        ctx = PipelineContext(user_input="孩子不想上学，厌学")
        r = ScenarioMatcher.execute(ctx)
        assert "不想上学" in r["matched_scenario"]

    def test_phone_addiction(self):
        ctx = PipelineContext(user_input="孩子沉迷手机游戏")
        r = ScenarioMatcher.execute(ctx)
        assert "手机" in r["matched_scenario"]

    def test_no_match(self):
        ctx = PipelineContext(user_input="今天天气真好")
        r = ScenarioMatcher.execute(ctx)
        assert r["matched_scenario"] == ""
        assert r["fallback"] == "generic_analysis"

    def test_multiple_matches(self):
        ctx = PipelineContext(user_input="孩子成绩下降，我打了孩子，现在很后悔")
        r = ScenarioMatcher.execute(ctx)
        assert len(r["all_matches"]) >= 2


class TestDefenseDetector:
    def test_shame_detection(self):
        ctx = PipelineContext(user_input="我觉得很丢人，没面子")
        r = DefenseDetector.execute(ctx)
        assert r["primary_defense"] == "shame"

    def test_control_detection(self):
        ctx = PipelineContext(user_input="孩子必须听话，应该服从")
        r = DefenseDetector.execute(ctx)
        assert r["primary_defense"] == "control"

    def test_projection_detection(self):
        ctx = PipelineContext(user_input="孩子像我小时候，是我的影子")
        r = DefenseDetector.execute(ctx)
        assert r["primary_defense"] == "projection"

    def test_no_defense(self):
        ctx = PipelineContext(user_input="今天天气好")
        r = DefenseDetector.execute(ctx)
        assert r["primary_defense"] == "none"

    def test_multiple_defenses(self):
        ctx = PipelineContext(user_input="孩子必须听话，我觉得丢人没面子，像我小时候")
        r = DefenseDetector.execute(ctx)
        assert len(r["all_defenses"]) >= 2


class TestResponseGenerator:
    def test_crisis_response(self):
        ctx = PipelineContext(
            user_input="我不想活了",
            safety_result={"is_crisis": True, "level": "imminent"},
        )
        r = ResponseGenerator.execute(ctx)
        assert r["type"] == "crisis"
        assert "hotlines" in r
        assert len(r["hotlines"]) > 0

    def test_parent_response(self):
        ctx = PipelineContext(
            user_input="孩子成绩下降了",
            safety_result={"is_crisis": False},
            user_identity={"role": "parent"},
            emotion_state={"primary_emotion": "anxiety", "intensity": "medium", "response_depth": "2min"},
            scenario_match={"matched_scenario": "01-成绩下降"},
            defense_signals={"primary_defense": "anxiety"},
        )
        r = ResponseGenerator.execute(ctx)
        assert r["type"] == "normal"
        assert r["empathy"]
        assert r["action"]

    def test_child_response(self):
        ctx = PipelineContext(
            user_input="我爸总是打我",
            safety_result={"is_crisis": False},
            user_identity={"role": "child"},
            emotion_state={"primary_emotion": "sadness", "intensity": "medium", "response_depth": "2min"},
            scenario_match={"matched_scenario": ""},
            defense_signals={"primary_defense": "none"},
        )
        r = ResponseGenerator.execute(ctx)
        assert r["type"] == "normal"
        assert r["role"] == "child"


class TestQualityChecker:
    def test_good_response(self):
        ctx = PipelineContext(
            user_input="孩子成绩下降了",
            safety_result={"is_crisis": False},
            user_identity={"role": "parent"},
            emotion_state={"primary_emotion": "anxiety"},
            response={"type": "normal", "empathy": "我能感受到你的焦虑", "action": "试试今天对孩子说一句鼓励的话", "guidance": "", "hotlines": []},
        )
        r = QualityChecker.execute(ctx)
        assert r["passed"] is True
        assert r["score"] >= 6.0

    def test_missing_empathy(self):
        ctx = PipelineContext(
            response={"type": "normal", "empathy": "", "action": "做点什么", "guidance": ""},
            safety_result={"is_crisis": False},
        )
        r = QualityChecker.execute(ctx)
        assert any("共情" in i for i in r["issues"])

    def test_harmful_language(self):
        ctx = PipelineContext(
            response={"type": "normal", "empathy": "你应该爱孩子", "action": "", "guidance": ""},
            safety_result={"is_crisis": False},
        )
        r = QualityChecker.execute(ctx)
        assert any("有害" in i for i in r["issues"])

    def test_crisis_without_hotlines(self):
        ctx = PipelineContext(
            response={"type": "normal", "empathy": "我在", "action": "", "guidance": ""},
            safety_result={"is_crisis": True},
        )
        r = QualityChecker.execute(ctx)
        assert any("热线" in i for i in r["issues"])


class TestPipelineOrchestrator:
    def test_full_pipeline(self):
        orch = PipelineOrchestrator(mode=IntegrationMode.FULL)
        report = orch.run("我的孩子成绩下降了，我很焦虑", "test_full")
        assert report.success is True
        assert report.integration_score > 0
        assert len(report.stage_summary) == 7

    def test_crisis_short_circuit(self):
        orch = PipelineOrchestrator()
        report = orch.run("我想自杀", "test_crisis")
        # Should only have safety gate stage
        assert "SAFETY_GATE" in report.stage_summary
        ctx = report.context
        assert ctx.safety_result["is_crisis"] is True

    def test_safety_only_mode(self):
        orch = PipelineOrchestrator(mode=IntegrationMode.SAFETY_ONLY)
        report = orch.run("孩子成绩下降", "test_safety")
        assert report.stage_summary["SAFETY_GATE"]["status"] == "success"
        assert report.stage_summary.get("USER_IDENTIFY", {}).get("status") == "skipped"

    def test_diagnostic_mode(self):
        orch = PipelineOrchestrator(mode=IntegrationMode.DIAGNOSTIC)
        result = orch.diagnose("我打了孩子现在很后悔", "test_diag")
        assert "SAFETY_GATE" in result
        assert "EMOTION_ASSESS" in result
        assert "integration_score" in result

    def test_state_update(self):
        orch = PipelineOrchestrator()
        report = orch.run("我的孩子成绩下降了我很焦虑", "test_state")
        state = report.state
        assert state.turn_count == 1
        assert state.user_role == "parent"

    def test_convenience_function(self):
        report = process_input("孩子不想上学", "test_conv")
        assert report.success is True

    def test_diagnose_function(self):
        result = diagnose_input("孩子沉迷手机", "test_diag_fn")
        assert "integration_score" in result


class TestConversationState:
    def test_update_from_context(self):
        ctx = PipelineContext(
            safety_result={"level": "none"},
            user_identity={"role": "parent"},
            emotion_state={"primary_emotion": "anxiety", "score": 7.0},
            scenario_match={"matched_scenario": "01-成绩下降"},
            defense_signals={"primary_defense": "anxiety"},
        )
        state = ConversationState(session_id="test")
        state.update(ctx)
        assert state.turn_count == 1
        assert state.user_role == "parent"
        assert state.current_emotion == "anxiety"
        assert state.current_topic == "01-成绩下降"
        assert state.emotion_trajectory == [7.0]

    def test_history_trimming(self):
        state = ConversationState(session_id="test", max_history=3)
        for i in range(5):
            ctx = PipelineContext(emotion_state={"primary_emotion": "neutral", "score": float(i)})
            state.update(ctx)
        assert len(state.emotion_trajectory) == 3
        assert state.emotion_trajectory == [2.0, 3.0, 4.0]

    def test_reset(self):
        state = ConversationState(session_id="test", turn_count=5, current_topic="test")
        state.reset()
        assert state.turn_count == 0
        assert state.current_topic == ""

    def test_save_load(self):
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            path = f.name
        try:
            state = ConversationState(session_id="test_save", turn_count=3, current_emotion="anxiety")
            state.save(path)
            loaded = ConversationState.load("test_save", path)
            assert loaded.turn_count == 3
            assert loaded.current_emotion == "anxiety"
        finally:
            os.unlink(path)

    def test_to_dict(self):
        state = ConversationState(session_id="test", turn_count=1, current_emotion="anger")
        d = state.to_dict()
        assert d["session_id"] == "test"
        assert d["current_emotion"] == "anger"


class TestModuleRegistry:
    def test_register_and_retrieve(self):
        reg = ModuleRegistry()
        reg.register("test_mod", lambda ctx: {}, [PipelineStage.SAFETY_GATE], priority=5)
        assert "test_mod" in reg.list_modules()
        assert reg.get_module("test_mod")["priority"] == 5

    def test_stage_routing(self):
        reg = ModuleRegistry()
        reg.register("a", lambda ctx: {}, [PipelineStage.SAFETY_GATE], priority=1)
        reg.register("b", lambda ctx: {}, [PipelineStage.SAFETY_GATE], priority=3)
        modules = reg.get_modules_for_stage(PipelineStage.SAFETY_GATE)
        assert modules[0] == "b"  # Higher priority first
        assert modules[1] == "a"

    def test_multi_stage_module(self):
        reg = ModuleRegistry()
        reg.register("multi", lambda ctx: {}, [PipelineStage.SAFETY_GATE, PipelineStage.USER_IDENTIFY])
        assert "multi" in reg.get_modules_for_stage(PipelineStage.SAFETY_GATE)
        assert "multi" in reg.get_modules_for_stage(PipelineStage.USER_IDENTIFY)


class TestEndToEnd:
    def test_parent_anxiety_scenario(self):
        report = process_input("我的孩子成绩下降了，我很焦虑，不知道怎么办", "e2e_1")
        assert report.success is True
        ctx = report.context
        assert ctx.user_identity["role"] == "parent"
        assert ctx.emotion_state["primary_emotion"] in ("anxiety", "helplessness")
        assert ctx.response["type"] == "normal"
        assert ctx.response["empathy"]
        assert ctx.quality_check["passed"] is True

    def test_crisis_scenario(self):
        report = process_input("我不想活了", "e2e_crisis")
        ctx = report.context
        assert ctx.safety_result["is_crisis"] is True
        assert ctx.response is not None, "Crisis scenario should still generate a response"
        assert ctx.response["type"] == "crisis"
        assert len(ctx.response["hotlines"]) > 0

    def test_parent_guilt_scenario(self):
        report = process_input("我的孩子我打了他都是我的错我很后悔很内疚", "e2e_guilt")
        ctx = report.context
        assert ctx.user_identity["role"] == "parent", f"Expected parent, got {ctx.user_identity['role']}"
        assert ctx.emotion_state["primary_emotion"] in ("guilt", "anger"), \
            f"Expected guilt or anger, got {ctx.emotion_state['primary_emotion']}"
        assert ctx.response["empathy"]
        assert ctx.quality_check["passed"] is True

    def test_defense_control_scenario(self):
        report = process_input("孩子必须听话，应该服从，我说了算", "e2e_control")
        ctx = report.context
        assert ctx.defense_signals["primary_defense"] == "control"
        assert ctx.response["guidance"]

    def test_multiple_runs_same_session(self):
        orch = PipelineOrchestrator()
        r1 = orch.run("孩子成绩下降了", "e2e_multi")
        r2 = orch.run("我打了孩子", "e2e_multi")
        assert r1.state.turn_count == 1
        assert r2.state.turn_count == 1  # Fresh state each run


class TestDataFlowRules:
    def test_dependency_graph(self):
        deps = DataFlowRules.get_upstream_for(PipelineStage.RESPONSE_GENERATE)
        assert PipelineStage.SAFETY_GATE in deps
        assert PipelineStage.EMOTION_ASSESS in deps
        assert len(deps) >= 4

    def test_safety_gate_no_deps(self):
        deps = DataFlowRules.get_upstream_for(PipelineStage.SAFETY_GATE)
        assert deps == []

    def test_validate_flow_complete(self):
        ctx = PipelineContext(
            safety_result={"is_crisis": False},
            user_identity={"role": "parent"},
            emotion_state={"primary_emotion": "anxiety"},
        )
        issues = DataFlowRules.validate_flow(ctx)
        assert len(issues) == 0

    def test_validate_flow_missing(self):
        ctx = PipelineContext()
        issues = DataFlowRules.validate_flow(ctx)
        assert len(issues) > 0
        assert any("safety_result" in i[0] for i in issues)

    def test_transform_rules_exist(self):
        assert "crisis_override" in DataFlowRules.TRANSFORMS
        assert "emotion_depth_mapping" in DataFlowRules.TRANSFORMS
        assert "defense_guidance_injection" in DataFlowRules.TRANSFORMS


class TestStateManager:
    def test_basic_update(self):
        sm = StateManager("test_sm")
        ctx = PipelineContext(
            user_identity={"role": "parent"},
            emotion_state={"primary_emotion": "anxiety", "score": 7.0},
            scenario_match={"matched_scenario": "01-成绩下降"},
            defense_signals={"primary_defense": "anxiety"},
        )
        sm.update(ctx)
        assert sm.conversation_state.turn_count == 1
        assert sm.conversation_state.user_role == "parent"

    def test_emotion_trend_stable(self):
        sm = StateManager("test_trend")
        for score in [5.0, 5.0, 5.0]:
            ctx = PipelineContext(emotion_state={"primary_emotion": "neutral", "score": score})
            sm.update(ctx)
        assert sm.detect_emotion_trend() == "stable"

    def test_emotion_trend_worsening(self):
        sm = StateManager("test_worsen")
        for score in [3.0, 5.0, 8.0]:
            ctx = PipelineContext(emotion_state={"primary_emotion": "anxiety", "score": score})
            sm.update(ctx)
        assert sm.detect_emotion_trend() == "worsening"

    def test_emotion_trend_improving(self):
        sm = StateManager("test_improve")
        for score in [8.0, 5.0, 2.0]:
            ctx = PipelineContext(emotion_state={"primary_emotion": "anxiety", "score": score})
            sm.update(ctx)
        assert sm.detect_emotion_trend() == "improving"

    def test_mode_transitions(self):
        sm = StateManager("test_trans")
        ctx1 = PipelineContext(emotion_state={"primary_emotion": "anger", "score": 8.0})
        sm.update(ctx1)
        ctx2 = PipelineContext(emotion_state={"primary_emotion": "sadness", "score": 6.0})
        sm.update(ctx2)
        assert len(sm.mode_transitions) >= 1
        assert any(t["type"] == "emotion_shift" for t in sm.mode_transitions)

    def test_context_summary(self):
        sm = StateManager("test_summary")
        ctx = PipelineContext(
            user_identity={"role": "parent"},
            emotion_state={"primary_emotion": "anxiety", "score": 7.0},
        )
        sm.update(ctx)
        summary = sm.get_context_summary()
        assert "turn_count" in summary
        assert "emotion_trend" in summary

    def test_save_load(self):
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            path = f.name
        try:
            sm = StateManager("test_save_load")
            ctx = PipelineContext(
                user_identity={"role": "parent"},
                emotion_state={"primary_emotion": "anxiety", "score": 7.0},
            )
            sm.update(ctx)
            sm.save(path)

            sm2 = StateManager("test_save_load")
            sm2.load(path)
            assert sm2.conversation_state.turn_count == 1
            assert sm2.conversation_state.user_role == "parent"
        finally:
            os.unlink(path)


class TestErrorRecovery:
    def test_safety_gate_strategy(self):
        strategy = ErrorRecovery.get_strategy(PipelineStage.SAFETY_GATE)
        assert strategy["on_fail"] == "assume_crisis"
        assert strategy["fallback_data"]["is_crisis"] is True
        assert strategy["retry"] is False

    def test_emotion_assess_retry(self):
        assert ErrorRecovery.should_retry(PipelineStage.EMOTION_ASSESS) is True
        assert ErrorRecovery.should_retry(PipelineStage.SAFETY_GATE) is False

    def test_execute_recovery(self):
        ctx = PipelineContext()
        result = ErrorRecovery.execute_recovery(ctx, PipelineStage.EMOTION_ASSESS, ValueError("test"))
        assert result["primary_emotion"] == "neutral"
        assert len(ctx.errors) == 1
        assert ctx.errors[0]["severity"] == "RECOVERY"

    def test_all_stages_have_strategies(self):
        for stage in PipelineStage:
            strategy = ErrorRecovery.get_strategy(stage)
            assert "on_fail" in strategy
            assert "fallback_data" in strategy


class TestPerformanceOptimizer:
    def test_record_metrics(self):
        po = PerformanceOptimizer()
        report = IntegrationReport(
            success=True,
            integration_score=8.5,
            total_duration_ms=15.3,
            stage_summary={
                "SAFETY_GATE": {"status": "success", "confidence": 0.95, "duration_ms": 2.1},
                "EMOTION_ASSESS": {"status": "success", "confidence": 0.8, "duration_ms": 1.5},
            },
        )
        po.record(report)
        assert len(po.metrics) == 1

    def test_bottleneck_detection(self):
        po = PerformanceOptimizer()
        report = IntegrationReport(
            success=True, integration_score=8.0, total_duration_ms=20.0,
            stage_summary={
                "SAFETY_GATE": {"status": "success", "confidence": 0.9, "duration_ms": 1.0},
                "EMOTION_ASSESS": {"status": "success", "confidence": 0.8, "duration_ms": 15.0},
            },
        )
        po.record(report)
        assert po.get_bottleneck() == "EMOTION_ASSESS"

    def test_performance_report(self):
        po = PerformanceOptimizer()
        assert po.get_report()["status"] == "no_data"
        report = IntegrationReport(
            success=True, integration_score=8.0, total_duration_ms=10.0,
            stage_summary={"SAFETY_GATE": {"status": "success", "confidence": 0.9, "duration_ms": 5.0}},
        )
        po.record(report)
        perf = po.get_report()
        assert perf["total_runs"] == 1
        assert "avg_total_ms" in perf
        assert "success_rate" in perf

    def test_metrics_limit(self):
        po = PerformanceOptimizer()
        for i in range(1005):
            po.record(IntegrationReport(success=True, integration_score=7.0, total_duration_ms=5.0, stage_summary={}))
        assert len(po.metrics) == 1000


def run_all_tests():
    """Run all test classes"""
    test_classes = [
        TestSafetyGate, TestUserIdentifier, TestEmotionAssessor,
        TestScenarioMatcher, TestDefenseDetector, TestResponseGenerator,
        TestQualityChecker, TestPipelineOrchestrator, TestConversationState,
        TestModuleRegistry, TestEndToEnd,
        TestDataFlowRules, TestStateManager, TestErrorRecovery, TestPerformanceOptimizer,
    ]
    total = 0
    passed = 0
    failed = 0
    errors = []

    for cls in test_classes:
        instance = cls()
        methods = [m for m in dir(instance) if m.startswith("test_")]
        for method_name in methods:
            total += 1
            try:
                getattr(instance, method_name)()
                passed += 1
                print(f"  ✓ {cls.__name__}.{method_name}")
            except Exception as e:
                failed += 1
                errors.append((f"{cls.__name__}.{method_name}", str(e)))
                print(f"  ✗ {cls.__name__}.{method_name}: {e}")

    print(f"\n{'='*50}")
    print(f"Total: {total} | Passed: {passed} | Failed: {failed}")
    if errors:
        print("\nFailed tests:")
        for name, err in errors:
            print(f"  - {name}: {err}")
    return failed == 0


if __name__ == "__main__":
    print(f"System Integrator v{VERSION} — Test Suite")
    print("="*50)
    success = run_all_tests()
    sys.exit(0 if success else 1)
