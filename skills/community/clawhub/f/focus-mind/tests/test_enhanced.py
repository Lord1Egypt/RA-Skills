#!/usr/bin/env python3
"""
FocusMind 增强测试套件
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from focusmind import (
    FocusMind,
    FocusMindConfig,
    analyze_context_health,
    generate_summary,
    extract_goals,
    need_cleanup
)

# 从子模块导入
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.check_context import HealthChecker
from scripts.auto_trigger import AutoTrigger, TriggerConfig
from scripts.cache import get_cache
from scripts.stats import get_tracker


def test_config():
    """测试配置"""
    print("=== 测试: 配置 ===")
    
    config = FocusMindConfig(
        threshold_tokens=5000,
        summary_style="bullet",
        auto_cleanup=True,
        preserve_recent=10
    )
    
    assert config.threshold_tokens == 5000
    assert config.summary_style == "bullet"
    assert config.auto_cleanup == True
    assert config.preserve_recent == 10
    
    print("  配置测试通过!")


def test_health_checker_class():
    """测试 HealthChecker 类"""
    print("=== 测试: HealthChecker 类 ===")
    
    checker = HealthChecker(threshold=5000)
    
    # 测试检查
    result = checker.check("test context")
    assert "score" in result
    
    # 测试趋势
    checker.check("more context " * 10)
    checker.check("more context " * 20)
    
    trend = checker.get_trend()
    assert trend in ["declining", "improving", "stable"]
    
    stats = checker.get_statistics()
    assert "checks" in stats
    
    print(f"  检查次数: {stats['checks']}")
    print(f"  平均分数: {stats['avg_score']:.1f}")
    print("  HealthChecker 测试通过!")


def test_auto_trigger():
    """测试自动触发器"""
    print("=== 测试: 自动触发器 ===")
    
    config = TriggerConfig(
        threshold_tokens=1000,
        check_interval_seconds=0,  # 立即可检查
        auto_summarize=True
    )
    
    trigger = AutoTrigger(config)
    
    # 第一次检查 - 应该触发
    context = "test " * 500
    result = trigger.check(context)
    
    print(f"  触发: {result['triggered']}")
    print(f"  健康度: {result['health']['score']}")
    
    stats = trigger.get_statistics()
    assert stats["total_checks"] >= 1
    
    print("  自动触发器测试通过!")


def test_cache():
    """测试缓存"""
    print("=== 测试: 缓存 ===")
    
    cache = get_cache()
    cache.clear()  # 清空缓存
    
    # 第一次请求
    context = "test context for caching"
    result1 = analyze_context_health(context)
    
    stats = cache.get_stats()
    print(f"  缓存命中率: {stats['hit_rate']}")
    
    print("  缓存测试通过!")


def test_tracker():
    """测试跟踪器"""
    print("=== 测试: 性能跟踪 ===")
    
    tracker = get_tracker()
    
    # 记录一些操作
    tracker.record_operation("test_op", 0.1)
    tracker.record_operation("test_op", 0.2)
    tracker.record_cleanup()
    tracker.record_summary()
    
    summary = tracker.get_summary()
    assert summary["total_operations"] >= 1
    
    print(f"  总操作数: {summary['total_operations']}")
    print("  性能跟踪测试通过!")


def test_summary_styles():
    """测试所有摘要风格"""
    print("=== 测试: 摘要风格 ===")
    
    messages = [
        {"role": "user", "content": "开发一个博客系统"},
        {"role": "assistant", "content": "好的"},
        {"role": "user", "content": "需要用户登录"},
    ] * 5
    
    styles = ["structured", "concise", "bullet", "executive"]
    
    for style in styles:
        result = generate_summary(messages, style=style)
        assert "summary" in result
        assert result["style"] == style
        print(f"  {style}: ✓")
    
    print("  摘要风格测试通过!")


def test_goal_extraction():
    """测试目标提取的各个阶段"""
    print("=== 测试: 目标提取阶段 ===")
    
    # 规划阶段
    planning_msgs = [
        {"role": "user", "content": "帮我设计一个系统"},
        {"role": "assistant", "content": "好的，我们先来做规划"},
    ]
    goals = extract_goals(planning_msgs)
    print(f"  规划阶段: {goals['current_phase_label']}")
    
    # 实现阶段
    implementing_msgs = [
        {"role": "user", "content": "开始写代码"},
        {"role": "assistant", "content": "正在编写代码"},
    ] * 10
    goals = extract_goals(implementing_msgs)
    print(f"  实现阶段: {goals['current_phase_label']}")
    
    # 测试阶段
    testing_msgs = [
        {"role": "user", "content": "开始测试"},
        {"role": "assistant", "content": "正在运行测试用例"},
    ] * 10
    goals = extract_goals(testing_msgs)
    print(f"  测试阶段: {goals['current_phase_label']}")
    
    print("  目标提取阶段测试通过!")


def test_edge_cases():
    """测试边界情况"""
    print("=== 测试: 边界情况 ===")
    
    # 空上下文
    health = analyze_context_health("")
    assert health["score"] >= 0
    print("  空上下文: ✓")
    
    # None
    health = analyze_context_health(None)
    assert health["score"] >= 0
    print("  None 上下文: ✓")
    
    # 纯数字
    health = analyze_context_health("123 456 789")
    assert health["score"] >= 0
    print("  纯数字: ✓")
    
    # 纯代码
    code = "def foo():\n    return 1\n" * 50
    health = analyze_context_health(code)
    assert health["score"] >= 0
    print("  纯代码: ✓")
    
    print("  边界情况测试通过!")


def test_full_workflow():
    """测试完整工作流"""
    print("=== 测试: 完整工作流 ===")
    
    # 创建 FocusMind 实例
    fm = FocusMind(config=FocusMindConfig(threshold_tokens=3000))
    
    # 模拟上下文
    messages = [
        {"role": "user", "content": "请帮我开发一个 Python 博客系统"},
        {"role": "assistant", "content": "好的，我来帮你开发"},
        {"role": "user", "content": "需要用户登录、文章发布、评论功能"},
        {"role": "assistant", "content": "明白了，我来实现这些功能"},
        {"role": "user", "content": "使用 Flask 框架"},
        {"role": "assistant", "content": "Flask 很好，我已经创建了项目结构"},
    ] * 10  # 重复以增加长度
    
    # 检查是否需要清理
    needs = fm.need_cleanup(messages)
    print(f"  需要清理: {needs}")
    
    # 完整分析
    result = fm.full_analysis(messages)
    assert "health" in result
    assert "summary" in result
    assert "goals" in result
    
    print(f"  健康度: {result['health']['score']}/100")
    print(f"  摘要长度: {len(result['summary']['summary'])} 字符")
    print(f"  子目标数: {len(result['goals']['sub_goals'])}")
    
    # 格式化报告
    report = fm.format_report(messages)
    assert len(report) > 0
    
    print("  完整工作流测试通过!")


def run_all_tests():
    """运行所有测试"""
    print("\n" + "="*50)
    print("🧪 FocusMind 增强测试套件")
    print("="*50 + "\n")
    
    try:
        test_config()
        test_health_checker_class()
        test_auto_trigger()
        test_cache()
        test_tracker()
        test_summary_styles()
        test_goal_extraction()
        test_edge_cases()
        test_full_workflow()
        
        print("\n" + "="*50)
        print("✅ 所有增强测试通过!")
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
