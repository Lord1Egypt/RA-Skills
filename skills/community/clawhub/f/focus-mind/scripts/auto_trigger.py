#!/usr/bin/env python3
"""
FocusMind 自动触发器
用于在特定条件下自动触发脑雾清除
"""

import os
import sys
import time
import json
from typing import Callable, Optional, Dict, Any
from dataclasses import dataclass, field

# 添加当前目录到路径
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from scripts.check_context import analyze_context_health
from scripts.summarize import generate_summary
from scripts.extract_goals import extract_goals


@dataclass
class TriggerConfig:
    """触发配置"""
    threshold_tokens: int = 10000
    check_interval_seconds: int = 1800  # 30分钟
    min_score_to_trigger: int = 70  # 分数低于此值时触发
    auto_summarize: bool = True
    notify_only: bool = False  # True=只通知, False=执行清理


class AutoTrigger:
    """
    自动触发器
    
    在 Agent 运行过程中自动检查上下文状态，
    当超过阈值时自动触发清理建议或执行清理
    """
    
    def __init__(self, config: Optional[TriggerConfig] = None):
        self.config = config or TriggerConfig()
        self.last_check_time = 0
        self.check_count = 0
        self.trigger_count = 0
        self.history = []
    
    def should_check(self) -> bool:
        """判断是否应该执行检查"""
        now = time.time()
        if now - self.last_check_time >= self.config.check_interval_seconds:
            self.last_check_time = now
            return True
        return False
    
    def check(self, context: Any, callback: Optional[Callable] = None) -> Dict[str, Any]:
        """
        执行检查
        
        Args:
            context: 上下文内容
            callback: 触发时的回调函数 (health, summary, goals) => None
        
        Returns:
            检查结果
        """
        self.check_count += 1
        
        # 分析健康度
        health = analyze_context_health(context, self.config.threshold_tokens)
        
        result = {
            "timestamp": now(),
            "check_number": self.check_count,
            "health": health,
            "triggered": False,
            "actions": []
        }
        
        # 判断是否需要触发
        need_trigger = (
            health["level"] in ["yellow", "red"] or
            health["score"] < self.config.min_score_to_trigger
        )
        
        if need_trigger:
            self.trigger_count += 1
            result["triggered"] = True
            
            # 生成摘要和目标
            if self.config.auto_summarize:
                summary = generate_summary(context)
                goals = extract_goals(context)
                result["summary"] = summary
                result["goals"] = goals
            
            # 执行回调或记录
            if callback:
                callback(health, result.get("summary"), result.get("goals"))
            
            if not self.config.notify_only:
                result["actions"].append("auto_cleanup_triggered")
        
        # 记录历史
        self.history.append(result)
        
        # 只保留最近100条
        if len(self.history) > 100:
            self.history = self.history[-100:]
        
        return result
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            "total_checks": self.check_count,
            "total_triggers": self.trigger_count,
            "trigger_rate": f"{self.trigger_count / max(1, self.check_count) * 100:.1f}%",
            "config": {
                "threshold": self.config.threshold_tokens,
                "interval": self.config.check_interval_seconds,
                "auto_summarize": self.config.auto_summarize
            }
        }


def now():
    """获取当前时间戳"""
    return int(time.time())


# ===== 便捷函数 =====

def quick_check(context: Any, threshold: int = 10000) -> Dict[str, Any]:
    """快速检查上下文健康度"""
    return analyze_context_health(context, threshold)


def quick_summary(context: Any) -> str:
    """快速生成摘要"""
    result = generate_summary(context)
    return result["summary"]


def quick_goals(context: Any) -> Dict[str, Any]:
    """快速提取目标"""
    return extract_goals(context)


# ===== Heartbeat 集成 =====

def on_heartbeat(context: Any, config: Optional[TriggerConfig] = None) -> Optional[str]:
    """
    Heartbeat 钩子函数
    
    在 Agent 的 heartbeat 中调用此函数
    
    Args:
        context: 上下文内容
        config: 触发配置
    
    Returns:
        如果需要清理返回提示信息，否则返回 None
    """
    trigger = AutoTrigger(config)
    
    if not trigger.should_check():
        return None
    
    health = analyze_context_health(context, config.threshold_tokens if config else 10000)
    
    if health["level"] in ["yellow", "red"]:
        summary = generate_summary(context)
        return f"🧠 脑雾警告: {health['emoji']} {health['label']}\n{health['recommendations'][0]}\n建议: 运行 focus-mind 完整分析"
    
    return None


# ===== 测试 =====

if __name__ == "__main__":
    # 测试
    test_context = """
    用户: 请帮我开发一个博客网站
    Agent: 好的，我来帮你开发博客网站。
    用户: 需要用户登录、文章发布、评论功能
    Agent: 明白了。我们需要实现这些功能。
    """ * 20
    
    print("=== 快速检查 ===")
    health = quick_check(test_context, threshold=5000)
    print(f"健康度: {health['score']}/100 ({health['label']})")
    
    print("\n=== 自动触发器 ===")
    config = TriggerConfig(threshold_tokens=3000, check_interval_seconds=1)
    trigger = AutoTrigger(config)
    
    for i in range(3):
        print(f"\n检查 {i+1}:")
        result = trigger.check(test_context)
        print(f"  触发: {result['triggered']}")
        if result['triggered']:
            print(f"  建议: {result['health']['recommendations'][:2]}")
    
    print(f"\n统计: {trigger.get_statistics()}")
