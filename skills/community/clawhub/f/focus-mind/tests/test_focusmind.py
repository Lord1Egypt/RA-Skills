#!/usr/bin/env python3 测试套件

"""
FocusMind"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from focusmind import (
    FocusMind,
    analyze_context_health,
    generate_summary,
    extract_goals,
    need_cleanup
)


def test_health_check():
    """测试健康度检查"""
    print("=== 测试: 健康度检查 ===")
    
    # 测试短上下文
    short_ctx = "用户: 你好"
    health = analyze_context_health(short_ctx)
    assert health["score"] > 80, "短上下文应该是健康的"
    assert health["level"] == "green", "短上下文应该是绿色"
    print(f"  短上下文: {health['score']}/100 ({health['label']}) ✓")
    
    # 测试长上下文
    long_ctx = "用户: 你好，这是一个很长的对话内容我们需要测试上下文健康度 " * 500
    health = analyze_context_health(long_ctx, threshold=5000)
    assert health["level"] in ["yellow", "red"], "长上下文应该触发警告"
    print(f"  长上下文: {health['score']}/100 ({health['label']}) ✓")
    
    # 测试高重复上下文
    repeat_ctx = "用户: 开发一个博客网站 " * 50
    health = analyze_context_health(repeat_ctx)
    print(f"  高重复上下文: {health['score']}/100, 重复率 {health['details']['repetition_ratio']}% ✓")
    
    print("  健康度检查测试通过!\n")


def test_summarize():
    """测试摘要生成"""
    print("=== 测试: 摘要生成 ===")
    
    messages = [
        {"role": "user", "content": "请帮我开发一个 Python 博客网站"},
        {"role": "assistant", "content": "好的，我来帮你开发博客网站。"},
        {"role": "user", "content": "需要用户登录、文章发布、评论功能"},
        {"role": "assistant", "content": "明白了。我们需要实现这些功能。"},
    ] * 3
    
    # 测试不同风格
    for style in ["structured", "concise", "bullet", "executive"]:
        result = generate_summary(messages, style=style)
        assert "summary" in result, f"{style} 风格应该返回 summary"
        print(f"  {style} 风格: ✓")
    
    print("  摘要生成测试通过!\n")


def test_extract_goals():
    """测试目标提取"""
    print("=== 测试: 目标提取 ===")
    
    messages = [
        {"role": "user", "content": "请帮我开发一个 Python 博客网站"},
        {"role": "assistant", "content": "好的，我来帮你开发博客网站。"},
        {"role": "user", "content": "需要用户登录、文章发布、评论功能"},
        {"role": "assistant", "content": "明白了。我们需要：1) 用户系统 2) 文章CRUD 3) 评论系统"},
        {"role": "user", "content": "使用 Flask 框架"},
        {"role": "assistant", "content": "好的，已创建项目结构，实现了用户认证。"},
    ]
    
    goals = extract_goals(messages)
    
    assert "main_goal" in goals, "应该返回 main_goal"
    assert "sub_goals" in goals, "应该返回 sub_goals"
    assert "current_phase" in goals, "应该返回 current_phase"
    
    print(f"  主目标: {goals['main_goal'][:30]}...")
    print(f"  当前阶段: {goals['current_phase_label']}")
    print(f"  子目标数: {len(goals['sub_goals'])}")
    print("  目标提取测试通过!\n")


def test_focusmind_class():
    """测试 FocusMind 类"""
    print("=== 测试: FocusMind 类 ===")
    
    fm = FocusMind()
    
    messages = [
        {"role": "user", "content": "开发一个博客"},
        {"role": "assistant", "content": "好的"},
    ] * 10
    
    # test analyze
    health = fm.analyze(messages)
    assert "score" in health
    
    # test need_cleanup
    needs = fm.need_cleanup(messages)
    assert isinstance(needs, bool)
    
    # test summarize
    summary = fm.summarize(messages)
    assert "summary" in summary
    
    # test extract_goals
    goals = fm.extract_goals(messages)
    assert "main_goal" in goals
    
    # test full_analysis
    full = fm.full_analysis(messages)
    assert "health" in full
    assert "summary" in full
    assert "goals" in full
    assert "need_cleanup" in full
    
    print("  FocusMind 类测试通过!\n")


def test_need_cleanup():
    """测试 need_cleanup 函数"""
    print("=== 测试: need_cleanup ===")
    
    # 短上下文
    assert not need_cleanup("hi", threshold=1000), "短上下文不需要清理"
    
    # 长上下文 - 使用更长的文本来确保超过阈值
    long = "用户: 你好，这是一个很长的对话内容我们需要测试上下文健康度 " * 500
    assert need_cleanup(long, threshold=100), "长上下文需要清理"
    
    print("  need_cleanup 测试通过!\n")


def run_all_tests():
    """运行所有测试"""
    print("\n" + "="*50)
    print("🧪 FocusMind 测试套件")
    print("="*50 + "\n")
    
    try:
        test_health_check()
        test_summarize()
        test_extract_goals()
        test_focusmind_class()
        test_need_cleanup()
        
        print("="*50)
        print("✅ 所有测试通过!")
        print("="*50 + "\n")
        return 0
    except AssertionError as e:
        print(f"\n❌ 测试失败: {e}\n")
        return 1
    except Exception as e:
        print(f"\n❌ 错误: {e}\n")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
