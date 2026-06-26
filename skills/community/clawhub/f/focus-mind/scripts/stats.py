#!/usr/bin/env python3
"""
FocusMind 性能统计模块
跟踪和分析技能使用情况
"""

import time
import json
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class OperationStats:
    """操作统计"""
    operation: str
    count: int = 0
    total_time: float = 0.0
    min_time: float = float('inf')
    max_time: float = 0.0
    errors: int = 0


@dataclass
class SessionStats:
    """会话统计"""
    session_id: str
    start_time: float = field(default_factory=time.time)
    operations: Dict[str, OperationStats] = field(default_factory=dict)
    cleanup_triggered: int = 0
    summaries_generated: int = 0
    goals_extracted: int = 0


class PerformanceTracker:
    """
    性能跟踪器
    
    记录 FocusMind 的使用统计
    """
    
    def __init__(self, session_id: Optional[str] = None):
        self.session_id = session_id or f"session_{int(time.time())}"
        self.stats = SessionStats(session_id=self.session_id)
    
    def record_operation(self, operation: str, duration: float, error: bool = False):
        """记录操作"""
        if operation not in self.stats.operations:
            self.stats.operations[operation] = OperationStats(operation=operation)
        
        stats = self.stats.operations[operation]
        stats.count += 1
        stats.total_time += duration
        stats.min_time = min(stats.min_time, duration)
        stats.max_time = max(stats.max_time, duration)
        if error:
            stats.errors += 1
    
    def record_cleanup(self):
        """记录清理触发"""
        self.stats.cleanup_triggered += 1
    
    def record_summary(self):
        """记录摘要生成"""
        self.stats.summaries_generated += 1
    
    def record_goals(self):
        """记录目标提取"""
        self.stats.goals_extracted += 1
    
    def get_summary(self) -> Dict[str, Any]:
        """获取统计摘要"""
        total_ops = sum(s.count for s in self.stats.operations.values())
        total_time = sum(s.total_time for s in self.stats.operations.values())
        
        return {
            "session_id": self.session_id,
            "duration_seconds": time.time() - self.stats.start_time,
            "total_operations": total_ops,
            "total_time": f"{total_time:.3f}s",
            "operations": {
                op: {
                    "count": s.count,
                    "avg_time": f"{s.total_time / max(1, s.count):.3f}s",
                    "min_time": f"{s.min_time:.3f}s",
                    "max_time": f"{s.max_time:.3f}s",
                    "errors": s.errors
                }
                for op, s in self.stats.operations.items()
            },
            "cleanup_triggered": self.stats.cleanup_triggered,
            "summaries_generated": self.stats.summaries_generated,
            "goals_extracted": self.stats.goals_extracted
        }
    
    def print_report(self):
        """打印报告"""
        summary = self.get_summary()
        
        print(f"""
╔══════════════════════════════════════╗
║     FocusMind 性能报告                ║
╠══════════════════════════════════════╣
║ 会话ID: {summary['session_id']:<26} ║
║ 运行时间: {summary['duration_seconds']:<23.1f}s ║
║ 总操作数: {summary['total_operations']:<26} ║
║ 总耗时: {summary['total_time']:<28} ║
╠══════════════════════════════════════╣
║ 功能使用统计:                          ║""")
        
        for op, stats in summary["operations"].items():
            print(f"║   {op}: {stats['count']}次, 平均{stats['avg_time']:<18} ║")
        
        print(f"""╠══════════════════════════════════════╣
║ 清理触发: {summary['cleanup_triggered']:<28} ║
║ 摘要生成: {summary['summaries_generated']:<28} ║
║ 目标提取: {summary['goals_extracted']:<28} ║
╚══════════════════════════════════════╝
        """)


# 上下文管理器版本
class Timer:
    """计时器上下文管理器"""
    
    def __init__(self, tracker: PerformanceTracker, operation: str):
        self.tracker = tracker
        self.operation = operation
        self.start_time = 0
        self.error = False
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = time.time() - self.start_time
        self.error = exc_type is not None
        self.tracker.record_operation(self.operation, duration, self.error)


def timer(tracker: PerformanceTracker, operation: str):
    """创建计时器"""
    return Timer(tracker, operation)


# 全局跟踪器
_global_tracker = PerformanceTracker()


def get_tracker() -> PerformanceTracker:
    """获取全局跟踪器"""
    return _global_tracker


# 导出
__all__ = ["PerformanceTracker", "Timer", "get_tracker"]
