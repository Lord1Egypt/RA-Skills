"""AI 内容分析测试（无 API 调用，测试降级行为）"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from content_analyzer import (
    call_ai, list_available_providers,
    analyze_plagiarism_context,
    analyze_age_rating_context,
    extract_plot_and_characters,
    analyze_adaptation_significance,
    generate_risk_assessment,
)


def test_call_ai_no_key():
    """测试无 API 密钥时的降级。"""
    # 确保无 API 密钥
    orig_openai = os.environ.pop("OPENAI_API_KEY", None)
    orig_anthropic = os.environ.pop("ANTHROPIC_API_KEY", None)

    try:
        result = call_ai("测试 prompt")
        assert result is None, "无 API 密钥时应返回 None"
        print("无密钥降级: PASS")
        return True
    finally:
        if orig_openai:
            os.environ["OPENAI_API_KEY"] = orig_openai
        if orig_anthropic:
            os.environ["ANTHROPIC_API_KEY"] = orig_anthropic


def test_list_providers_empty():
    """测试无密钥时的 provider 列表。"""
    orig_openai = os.environ.pop("OPENAI_API_KEY", None)
    orig_anthropic = os.environ.pop("ANTHROPIC_API_KEY", None)

    try:
        providers = list_available_providers()
        assert isinstance(providers, list)
        assert len(providers) == 0, "无密钥时应无可用 provider"
        print("空 provider 列表: PASS")
        return True
    finally:
        if orig_openai:
            os.environ["OPENAI_API_KEY"] = orig_openai
        if orig_anthropic:
            os.environ["ANTHROPIC_API_KEY"] = orig_anthropic


def test_analyze_plagiarism_empty():
    """测试空输入的版权分析。"""
    result = analyze_plagiarism_context([])
    assert result is None, "空列表应返回 None"
    print("空版权分析: PASS")
    return True


def test_analyze_age_rating_empty():
    """测试空输入的分级分析。"""
    result = analyze_age_rating_context([], "all_ages")
    assert result is None, "空列表应返回 None"
    print("空分级分析: PASS")
    return True


def test_analyze_adaptation_empty():
    """测试空输入的改编分析。"""
    result = analyze_adaptation_significance([])
    assert result is None, "空列表应返回 None"
    print("空改编分析: PASS")
    return True


def test_extract_plot_no_api():
    """测试无 API 时的情节提取。"""
    orig_openai = os.environ.pop("OPENAI_API_KEY", None)
    orig_anthropic = os.environ.pop("ANTHROPIC_API_KEY", None)

    try:
        result = extract_plot_and_characters("测试文本")
        assert result is None, "无 API 时应返回 None"
        print("无API情节提取: PASS")
        return True
    finally:
        if orig_openai:
            os.environ["OPENAI_API_KEY"] = orig_openai
        if orig_anthropic:
            os.environ["ANTHROPIC_API_KEY"] = orig_anthropic


def test_risk_assessment_no_api():
    """测试无 API 时的风险评估。"""
    orig_openai = os.environ.pop("OPENAI_API_KEY", None)
    orig_anthropic = os.environ.pop("ANTHROPIC_API_KEY", None)

    try:
        result = generate_risk_assessment({"test": "data"})
        assert result is None, "无 API 时应返回 None"
        print("无API风险评估: PASS")
        return True
    finally:
        if orig_openai:
            os.environ["OPENAI_API_KEY"] = orig_openai
        if orig_anthropic:
            os.environ["ANTHROPIC_API_KEY"] = orig_anthropic


if __name__ == "__main__":
    print("=== AI 内容分析测试 ===\n")

    tests = [
        test_call_ai_no_key,
        test_list_providers_empty,
        test_analyze_plagiarism_empty,
        test_analyze_age_rating_empty,
        test_analyze_adaptation_empty,
        test_extract_plot_no_api,
        test_risk_assessment_no_api,
    ]

    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"  FAIL: {test.__name__}: {e}")
            results.append(False)

    passed = sum(results)
    total = len(results)
    print(f"\n总计: {passed}/{total} 通过")
    sys.exit(0 if passed == total else 1)
