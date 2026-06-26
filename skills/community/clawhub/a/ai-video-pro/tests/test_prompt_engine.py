"""提示词引擎测试"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from prompt_engine import (
    detect_scene_type,
    analyze_scene,
    format_for_provider,
    SCENE_TYPE_KEYWORDS,
    REQUIRED_ELEMENTS,
)


def test_detect_scene_type():
    """测试场景类型检测。"""
    cases = [
        ("两个武士在雨中决斗", "action"),
        ("巨型机甲从海里走出来", "mecha"),
        ("一个女孩从难过变成开心", "emotional"),
        ("父亲送女儿上大学的离别", "character"),
        ("夕阳下的城市天际线", "landscape"),
        ("一只猫在阳光下睡觉", "general"),
        ("机器人互相战斗", "mecha"),  # mecha + action, mecha 优先（更具体）
        ("Two robots fighting in a city", "mecha"),  # robot 触发 mecha
    ]

    passed = 0
    for description, expected in cases:
        result = detect_scene_type(description)
        status = "PASS" if result == expected else "FAIL"
        if status == "FAIL":
            print(f"  {status}: '{description}' → 期望 '{expected}', 得到 '{result}'")
        else:
            passed += 1

    print(f"场景类型检测: {passed}/{len(cases)} 通过")
    return passed == len(cases)


def test_analyze_scene_action():
    """测试动作场景分析。"""
    analysis = analyze_scene("两个忍者在屋顶上打斗")

    assert analysis.scene_type == "action", f"期望 action, 得到 {analysis.scene_type}"
    assert analysis.user_input == "两个忍者在屋顶上打斗"
    assert len(analysis.questions_for_user) > 0, "应该有需要询问的问题"

    # 检查动作场景特有的问题
    question_fields = [q["field"] for q in analysis.questions_for_user]
    assert "impact_level" in question_fields, "缺少打击力度问题"
    assert "impact_reaction" in question_fields, "缺少受击反应问题"

    # 检查通用问题
    assert "aspect_ratio" in question_fields, "缺少画面比例问题"
    assert "duration_seconds" in question_fields, "缺少时长问题"
    assert "visual_style" in question_fields, "缺少风格问题"

    print("动作场景分析: PASS")
    return True


def test_analyze_scene_mecha():
    """测试机甲场景分析。"""
    analysis = analyze_scene("巨型机甲在城市中行走")

    assert analysis.scene_type == "mecha", f"期望 mecha, 得到 {analysis.scene_type}"

    question_fields = [q["field"] for q in analysis.questions_for_user]
    assert "mecha_motion_style" in question_fields, "缺少运动风格问题"

    print("机甲场景分析: PASS")
    return True


def test_format_for_providers():
    """测试各 Provider 的 prompt 格式化。"""
    analysis = analyze_scene("一条龙在城堡上空飞翔")

    providers = ["lumaai", "runway", "replicate", "comfyui", "dalle"]
    all_passed = True

    for provider in providers:
        prompt = format_for_provider(analysis, provider)
        assert isinstance(prompt, str), f"{provider}: 输出不是字符串"
        assert len(prompt) > 10, f"{provider}: prompt 太短"

        # 检查关键内容是否存在
        if provider == "comfyui":
            assert "positive" in prompt, f"{provider}: 缺少 positive 字段"
            assert "negative" in prompt, f"{provider}: 缺少 negative 字段"
        elif provider == "runway":
            assert "Subject:" in prompt, f"{provider}: 缺少 Subject 字段"

    print(f"Provider 格式化: {'PASS' if all_passed else 'FAIL'}")
    return all_passed


def test_format_with_answers():
    """测试带用户回答的格式化。"""
    analysis = analyze_scene("两个武士决斗")
    answers = {
        "impact_level": "heavy cinematic impact",
        "impact_effects": "sparks and debris",
        "expression_start": "calm determination",
        "expression_end": "fierce battle cry",
    }

    prompt = format_for_provider(analysis, "lumaai", answers)
    assert "heavy cinematic impact" in prompt, "用户回答未包含在 prompt 中"
    assert "sparks and debris" in prompt, "特效描述未包含在 prompt 中"

    print("带回答格式化: PASS")
    return True


def test_required_elements_coverage():
    """测试必需元素覆盖完整性。"""
    # 确保所有定义的场景类型都有对应的必需元素
    for scene_type in ["action", "mecha", "emotional", "character"]:
        assert scene_type in REQUIRED_ELEMENTS, f"缺少 {scene_type} 的必需元素定义"
        elements = REQUIRED_ELEMENTS[scene_type]
        assert len(elements) >= 3, f"{scene_type} 的必需元素太少 ({len(elements)})"

    print("必需元素覆盖: PASS")
    return True


if __name__ == "__main__":
    print("=== 提示词引擎测试 ===\n")

    tests = [
        test_detect_scene_type,
        test_analyze_scene_action,
        test_analyze_scene_mecha,
        test_format_for_providers,
        test_format_with_answers,
        test_required_elements_coverage,
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
