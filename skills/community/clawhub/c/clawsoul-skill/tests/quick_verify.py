#!/usr/bin/env python3
"""
ClawSoul 快速验证脚本
运行: python3 ~/Desktop/八哥/clawsoul-skill/tests/quick_verify.py
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_memory_manager():
    """测试存储模块"""
    print("\n📦 测试: Memory Manager")
    from lib.memory_manager import MemoryManager
    
    # 使用临时文件
    mm = MemoryManager("~/.clawsoul/test_state.json")
    
    # 测试状态
    assert mm.get_evolution_stage() == 0, "初始阶段应为0"
    mm.complete_awaken("INTJ")
    assert mm.get_mbti() == "INTJ", "MBTI 应为 INTJ"
    assert mm.get_evolution_stage() == 1, "阶段应为1"
    assert mm.is_awaken_completed() == True, "觉醒应完成"
    
    # 测试偏好
    mm.add_user_preference("喜欢简洁")
    prefs = mm.get_user_preferences()
    assert "喜欢简洁" in prefs, "偏好应保存"
    
    # 清理
    mm.reset()
    print("  ✅ 存储模块正常")
    return True


def test_frustration_detector():
    """测试痛点检测"""
    print("\n😤 测试: Frustration Detector")
    from lib.frustration_detector import FrustrationDetector
    
    detector = FrustrationDetector()
    
    # 测试用例
    tests = [
        ("太笨了", True),
        ("不对，不是这个意思", True),
        ("重做", True),
        ("抓不住重点", True),
        ("很好", False),
        ("谢谢", False),
    ]
    
    for text, expected in tests:
        result, _ = detector.detect(text)
        # result 可能是 'strong', 'mild', 'none', '' 字符串
        actual = result in ('strong', 'mild')
        assert actual == expected, f"检测 '{text}' 失败: {result}"
    
    print("  ✅ 痛点检测正常")
    return True


def test_prompt_builder():
    """测试 Prompt 构建"""
    print("\n🎭 测试: Prompt Builder")
    from lib.prompt_builder import PromptBuilder
    
    # 重置状态
    from lib.memory_manager import MemoryManager
    mm = MemoryManager("~/.clawsoul/test_state.json")
    mm.reset()
    mm.complete_awaken("INTJ")
    
    builder = PromptBuilder()
    prompt = builder.build_persona_prompt()
    
    assert "INTJ" in prompt, "Prompt 应包含 MBTI"
    assert len(prompt) > 0, "Prompt 不应为空"
    
    # 清理
    mm.reset()
    print("  ✅ Prompt 构建正常")
    return True


def test_awaken_hook():
    """测试觉醒流程"""
    print("\n⚡ 测试: Awaken Hook")
    try:
        from hooks.awaken import AwakenHook
        print("  ✅ 觉醒模块导入成功")
        return True
    except ImportError as e:
        print(f"  ⚠️ 觉醒模块未就绪: {e}")
        return False


def main():
    print("=" * 50)
    print("🧪 ClawSoul 快速验证")
    print("=" * 50)
    
    results = []
    
    try:
        results.append(("存储模块", test_memory_manager()))
    except Exception as e:
        print(f"  ❌ 存储模块失败: {e}")
        results.append(("存储模块", False))
    
    try:
        results.append(("痛点检测", test_frustration_detector()))
    except Exception as e:
        print(f"  ❌ 痛点检测失败: {e}")
        results.append(("痛点检测", False))
    
    try:
        results.append(("Prompt构建", test_prompt_builder()))
    except Exception as e:
        print(f"  ❌ Prompt构建失败: {e}")
        results.append(("Prompt构建", False))
    
    try:
        results.append(("觉醒模块", test_awaken_hook()))
    except Exception as e:
        print(f"  ❌ 觉醒模块失败: {e}")
        results.append(("觉醒模块", False))
    
    # 汇总
    print("\n" + "=" * 50)
    print("📊 测试结果汇总")
    print("=" * 50)
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = "✅" if result else "❌"
        print(f"  {status} {name}")
    
    print(f"\n总计: {passed}/{total} 通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！")
        return 0
    else:
        print(f"\n⚠️ {total - passed} 项待完善")
        return 1


if __name__ == "__main__":
    sys.exit(main())
