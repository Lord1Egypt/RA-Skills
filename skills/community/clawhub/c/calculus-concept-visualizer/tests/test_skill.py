#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Calculus Concept Visualizer - 测试套件
作者: 代国兴
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tools'))

import json
from generate_geogebra import generate_geogebra, GeoGebraGenerator
from diagnose_misconception import diagnose_misconception, MisconceptionDetector
from generate_quiz import generate_quiz, QuizGenerator
from step_builder import step_builder, StepBuilder

def test_geogebra_generator():
    """测试 GeoGebra 生成器"""
    print("=" * 50)
    print("测试 1: GeoGebra 生成器")
    print("=" * 50)

    generator = GeoGebraGenerator()

    # 测试极限 ε-δ
    config = generator.generate("limit_epsilon_delta", {
        "function": "sin(x)/x",
        "point": 0,
        "limit": 1
    })

    assert config["type"] == "geogebra"
    assert "parameters" in config
    assert "epsilon" in config["parameters"]
    print("✅ ε-δ 极限配置生成成功")

    # 测试导数定义
    config = generator.generate("derivative_definition", {
        "function": "x^2",
        "point": 1
    })
    assert "animation" in config
    print("✅ 导数定义动画配置生成成功")

    # 测试黎曼和
    config = generator.generate("integral_riemann", {
        "function": "x^2",
        "a": 0,
        "b": 2
    })
    assert "parameters" in config
    print("✅ 黎曼和配置生成成功")

    print("✅ GeoGebra 生成器测试通过\n")

def test_misconception_detector():
    """测试误区检测器"""
    print("=" * 50)
    print("测试 2: 误区检测器")
    print("=" * 50)

    detector = MisconceptionDetector()

    # 测试误区识别
    response = "我觉得极限就是直接把 x=0 代入函数计算的值"
    result = detector.analyze(response, "limit")

    assert result["has_misconception"] == True
    assert result["risk_level"] in ["low", "medium", "high"]
    assert len(result["detected"]) > 0
    print(f"✅ 检测到 {len(result['detected'])} 个潜在误区")
    print(f"   风险等级: {result['risk_level']}")

    # 测试无误区情况
    response = "ε-δ 定义说的是对于任意给定的 ε，存在一个 δ"
    result = detector.analyze(response, "limit")
    print(f"✅ 正确表述检测: 发现 {len(result['detected'])} 个误区")

    print("✅ 误区检测器测试通过\n")

def test_quiz_generator():
    """测试检测题生成器"""
    print("=" * 50)
    print("测试 3: 检测题生成器")
    print("=" * 50)

    generator = QuizGenerator()

    # 测试极限题目生成
    quiz_set = generator.generate_quiz("limit", 0.6)

    assert len(quiz_set) == 3
    levels = [q["level"] for q in quiz_set]
    assert "recognition" in levels
    assert "application" in levels
    assert "transfer" in levels
    print(f"✅ 生成 {len(quiz_set)} 道渐进式检测题")

    total_score = sum(q["scoring"] for q in quiz_set)
    assert total_score == 100
    print(f"✅ 总分验证: {total_score} 分")

    print("✅ 检测题生成器测试通过\n")

def test_step_builder():
    """测试分步推导构建器"""
    print("=" * 50)
    print("测试 4: 分步推导构建器")
    print("=" * 50)

    builder = StepBuilder()

    # 测试 ε-δ 证明步骤
    result = builder.build("epsilon_delta_proof", {
        "function": "3x-1",
        "a": 2,
        "L": 5
    })

    assert result["type"] == "step_by_step_derivation"
    assert result["total_steps"] > 0
    print(f"✅ 生成 {result['total_steps']} 步推导")

    # 测试链式法则
    result = builder.build("derivative_chain_rule", {})
    assert result["total_steps"] > 0
    print(f"✅ 链式法则推导: {result['total_steps']} 步")

    print("✅ 分步推导构建器测试通过\n")

def run_all_tests():
    """运行所有测试"""
    print("\n" + "=" * 50)
    print("Calculus Concept Visualizer - 测试套件")
    print("作者: 代国兴")
    print("=" * 50 + "\n")

    try:
        test_geogebra_generator()
        test_misconception_detector()
        test_quiz_generator()
        test_step_builder()

        print("=" * 50)
        print("✅ 所有测试通过!")
        print("=" * 50)
        return 0

    except Exception as e:
        print("\n" + "=" * 50)
        print(f"❌ 测试失败: {str(e)}")
        print("=" * 50)
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(run_all_tests())
