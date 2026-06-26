#!/usr/bin/env python3
"""
Skill Evaluator P1 集成测试

测试 P1 新增功能:
1. Assertion System
2. Critic Engine V2
3. Real Skill Evaluator
4. scripts/ 与 interfaces/ 整合

运行方式:
    pytest tests/test_p1_integration.py -v
    python3 tests/test_p1_integration.py
"""

import sys
import tempfile
import json
from pathlib import Path

# 添加 interfaces 到 path
interfaces_dir = str(Path(__file__).parent.parent / "interfaces")
if interfaces_dir not in sys.path:
    sys.path.insert(0, interfaces_dir)


def test_assertion_system():
    """测试断言系统"""
    print("\n" + "=" * 60)
    print("Test 1: Assertion System")
    print("=" * 60)

    from assertions import (
        AssertionRunner,
        AssertionExecutor,
        create_check,
        create_assertion,
        AssertionType,
    )

    # 测试 contains 断言
    check = create_check(
        name="Basic Contains Test",
        assertions=[
            {"type": "contains", "value": "success", "description": "Contains 'success'"},
            {"type": "contains", "value": "completed", "description": "Contains 'completed'"},
        ],
    )

    runner = AssertionRunner()
    result = runner.run(check, {"output": "Operation success - task completed"})

    assert result.passed, f"Expected check to pass, got: {result.message}"
    assert result.score > 0.8, f"Expected high score, got: {result.score}"

    print(f"✅ Contains test passed: {result.message}")
    print(f"   Score: {result.score:.2%}")

    # 测试 regex 断言
    regex_check = create_check(
        name="Regex Test",
        assertions=[
            {"type": "regex", "value": r"\d+", "description": "Contains digits"},
        ],
    )

    regex_result = runner.run(regex_check, "Result: 42 items found")
    assert regex_result.passed, f"Expected regex to match, got: {regex_result.message}"

    print(f"✅ Regex test passed: {regex_result.message}")

    # 测试 threshold 断言
    threshold_check = create_check(
        name="Threshold Test",
        assertions=[
            {"type": "threshold", "value": 0.8, "description": "Score >= 0.8"},
        ],
    )

    threshold_result = runner.run(threshold_check, 0.85)
    assert threshold_result.passed, f"Expected threshold to pass, got: {threshold_result.message}"

    print(f"✅ Threshold test passed: {threshold_result.message}")

    print("\n✅ Assertion System tests passed!")


def test_critic_engine_v2():
    """测试 Critic Engine V2"""
    print("\n" + "=" * 60)
    print("Test 2: Critic Engine V2")
    print("=" * 60)

    from critic_engine import CriticEngineV2, CriticConfig

    # 创建配置
    config = CriticConfig(
        enable_frozen_benchmark=True,
        enable_hidden_tests=True,
        enable_assertions=True,
        benchmark_weight=0.35,
        hidden_test_weight=0.25,
        assertion_weight=0.20,
        regression_weight=0.10,
        human_review_weight=0.10,
        verbose=False,
        use_mock_evaluator=True,  # 测试使用 mock
    )

    # 创建引擎
    engine = CriticEngineV2(config)

    # 加载测试套件
    engine.load_benchmark_suite()
    engine.load_hidden_tests(password="DEMO_ONLY_NOT_FOR_PRODUCTION")
    engine.load_standard_assertions()

    # 运行评估
    score = engine.evaluate()

    # 验证结果
    assert score.overall >= 0.0, "Overall score should be non-negative"
    assert score.overall <= 1.0, "Overall score should be <= 1.0"
    assert score.level in [1, 2, 3], "Level should be 1, 2, or 3"
    assert hasattr(score, 'assertion_score'), "Score should have assertion_score (P1)"

    print(f"✅ Critic V2 evaluation completed")
    print(f"   Overall: {score.overall:.4f}")
    print(f"   Benchmark: {score.benchmark_score:.4f}")
    print(f"   Hidden: {score.hidden_test_score:.4f}")
    print(f"   Assertion: {score.assertion_score:.4f} (P1)")
    print(f"   Level: {score.level}")

    # 验证报告生成
    report = engine.generate_report("/tmp/test_critic_v2_report.md")
    assert "Critic V2" in report or "P1" in report, "Report should mention V2/P1"
    assert "断言检查" in report or "Assertion" in report, "Report should include assertion section"

    print(f"✅ Report generated successfully")

    # 验证 JSON 导出
    json_path = engine.export_results("/tmp/test_critic_v2_results.json")
    with open(json_path, 'r') as f:
        results = json.load(f)

    assert "score" in results, "Results should contain score"
    assert "assertions" in results, "Results should contain assertions (P1)"

    print(f"✅ JSON results exported successfully")
    print("\n✅ Critic Engine V2 tests passed!")


def test_real_skill_evaluator():
    """测试真实 Skill 评估器"""
    print("\n" + "=" * 60)
    print("Test 3: Real Skill Evaluator")
    print("=" * 60)

    from critic_engine import RealSkillEvaluator
    from frozen_benchmark import BenchmarkCase

    # 创建临时 Skill 文件
    with tempfile.TemporaryDirectory() as tmpdir:
        skill_dir = Path(tmpdir)
        skill_file = skill_dir / "main.py"

        # 编写一个简单的 Skill
        skill_code = '''
def evaluate(input_data):
    """简单的 Skill 实现"""
    if isinstance(input_data, dict):
        task = input_data.get("task", "unknown")
        return {
            "status": "success",
            "result": f"Processed: {task}",
            "score": 0.85,
        }
    return {"status": "error", "result": "Invalid input"}
'''
        skill_file.write_text(skill_code)

        # 加载 Skill 评估器
        evaluator = RealSkillEvaluator(str(skill_dir))

        # 验证模块已加载
        assert evaluator.skill_module is not None, "Skill module should be loaded"
        assert evaluator.skill_func is not None, "Skill function should be found"

        print(f"✅ Real Skill loaded from: {skill_file}")

        # 创建测试用例
        test_case = BenchmarkCase(
            id="test-001",
            name="Real Skill Test",
            input_data={"task": "test_operation"},
            expected_output={"status": "success"},
            category="test",
            difficulty=1,
        )

        # 运行评估
        result = evaluator.evaluate(test_case)

        # 验证结果
        assert result.passed, f"Expected test to pass, got: {result.error_message}"
        assert result.score > 0.5, f"Expected reasonable score, got: {result.score}"
        assert result.actual_output is not None, "Should have actual output"

        print(f"✅ Real Skill evaluation completed")
        print(f"   Passed: {result.passed}")
        print(f"   Score: {result.score:.4f}")
        print(f"   Output: {result.actual_output}")

    print("\n✅ Real Skill Evaluator tests passed!")


def test_scripts_interfaces_integration():
    """测试 scripts/ 与 interfaces/ 的整合"""
    print("\n" + "=" * 60)
    print("Test 4: Scripts/Interfaces Integration")
    print("=" * 60)

    # 测试 score.py 存在且 critic_engine 可导入
    scripts_dir = Path(__file__).parent.parent / "scripts"
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))

    score_script = scripts_dir / "score.py"
    assert score_script.exists(), "score.py should exist"
    print(f"✅ score.py exists")

    from critic_engine import CriticEngineV2, CriticConfig
    print(f"✅ critic_engine can be imported")

    # 测试能否运行简单评估
    config = CriticConfig(
        enable_frozen_benchmark=False,  # 简化测试
        enable_hidden_tests=False,
        enable_assertions=True,
        benchmark_weight=0.0,
        hidden_test_weight=0.0,
        assertion_weight=0.80,
        regression_weight=0.10,
        human_review_weight=0.10,
        verbose=False,
    )

    engine = CriticEngineV2(config)
    engine.load_standard_assertions()

    # 运行仅断言评估
    score = engine.evaluate()

    assert score.overall >= 0.0, "Should have valid score"
    assert score.assertion_score > 0.0, "Should have assertion score"

    print(f"✅ Scripts/Interfaces integration test passed")
    print(f"   Assertion-only score: {score.assertion_score:.4f}")

    print("\n✅ Scripts/Interfaces Integration tests passed!")


def test_mock_reduction():
    """测试 MockSkillEvaluator 权重降低"""
    print("\n" + "=" * 60)
    print("Test 5: Mock Reduction Verification")
    print("=" * 60)

    from critic_engine import CriticConfig, CriticEngineV2

    # 验证默认配置不使用 mock
    default_config = CriticConfig()
    assert default_config.use_mock_evaluator == False, "Default should not use mock"

    print(f"✅ Default config: use_mock_evaluator = {default_config.use_mock_evaluator}")

    # 验证可以显式启用 mock
    mock_config = CriticConfig(use_mock_evaluator=True)
    assert mock_config.use_mock_evaluator == True, "Should be able to enable mock"

    print(f"✅ Can explicitly enable mock when needed")

    # 验证权重配置
    total = (default_config.benchmark_weight + default_config.hidden_test_weight
             + default_config.assertion_weight + default_config.regression_weight
             + default_config.human_review_weight)
    assert abs(total - 1.0) < 0.001
    print(f"✅ Weights sum to 1.0: {total}")

    print("\n✅ Mock Reduction verification passed!")


def run_all_tests():
    """运行所有 P1 集成测试"""
    print("=" * 60)
    print("Skill Evaluator P1 Integration Tests")
    print("=" * 60)

    tests = [
        ("Assertion System", test_assertion_system),
        ("Critic Engine V2", test_critic_engine_v2),
        ("Real Skill Evaluator", test_real_skill_evaluator),
        ("Scripts/Interfaces Integration", test_scripts_interfaces_integration),
        ("Mock Reduction", test_mock_reduction),
    ]

    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed, None))
        except Exception as e:
            results.append((name, False, str(e)))
            print(f"\n❌ {name} FAILED: {e}")
            import traceback
            traceback.print_exc()

    # 汇总结果
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    passed_count = sum(1 for _, passed, _ in results if passed)
    total_count = len(results)

    for name, passed, error in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {name}")
        if error:
            print(f"       Error: {error}")

    print(f"\nTotal: {passed_count}/{total_count} tests passed")

    if passed_count == total_count:
        print("\n🎉 All P1 integration tests passed!")
        return True
    else:
        print(f"\n⚠️ {total_count - passed_count} test(s) failed")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
