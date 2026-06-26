#!/usr/bin/env python3
"""性能监控模块 - v2.7.0"""

import time
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, field
from functools import wraps
from contextlib import contextmanager
import threading

logger = logging.getLogger(__name__)

@dataclass
class OperationStats:
    operation: str
    count: int = 0
    total_time: float = 0.0
    min_time: float = float('inf')
    max_time: float = 0.0
    last_time: float = 0.0
    
    @property
    def avg_time(self) -> float:
        return self.total_time / self.count if self.count > 0 else 0
    
    def to_dict(self) -> Dict:
        return {'operation': self.operation, 'count': self.count, 'total_ms': self.total_time * 1000, 'avg_ms': self.avg_time * 1000, 'min_ms': self.min_time * 1000 if self.min_time != float('inf') else 0, 'max_ms': self.max_time * 1000, 'last_ms': self.last_time * 1000}

class PerformanceMonitor:
    def __init__(self, enabled: bool = True):
        self._stats: Dict[str, OperationStats] = {}
        self._lock = threading.RLock()
        self.enabled = enabled
        self._start_time = time.time()
        self.slow_threshold = 1.0
        self._slow_callback: Optional[Callable] = None
    
    @contextmanager
    def track_operation(self, operation_name: str):
        if not self.enabled:
            yield
            return
        start = time.time()
        try:
            yield
        finally:
            elapsed = time.time() - start
            self._record(operation_name, elapsed)
            if elapsed > self.slow_threshold:
                logger.warning(f"慢操作：{operation_name} 耗时 {elapsed*1000:.2f}ms")
    
    def _record(self, operation: str, elapsed: float):
        with self._lock:
            if operation not in self._stats:
                self._stats[operation] = OperationStats(operation=operation)
            stats = self._stats[operation]
            stats.count += 1
            stats.total_time += elapsed
            stats.min_time = min(stats.min_time, elapsed)
            stats.max_time = max(stats.max_time, elapsed)
            stats.last_time = elapsed
    
    def get_stats(self) -> Dict[str, OperationStats]:
        with self._lock:
            return dict(self._stats)
    
    def print_report(self):
        report = self.generate_report()
        print("\n" + "="*70)
        print("性能报告")
        print("="*70)
        print(f"运行时间：{report['summary']['elapsed_seconds']:.2f}秒")
        print(f"总操作数：{report['summary']['total_operations']}")
        print(f"操作/秒：{report['summary']['ops_per_second']:.1f}")
        print()
        print("操作统计 (按总耗时排序):")
        print("-"*70)
        print(f"{'操作':<30} {'次数':>8} {'平均 (ms)':>12} {'总计 (ms)':>12}")
        print("-"*70)
        sorted_ops = sorted(report['operations'].values(), key=lambda x: x['total_ms'], reverse=True)
        for op in sorted_ops:
            print(f"{op['operation']:<30} {op['count']:>8} {op['avg_ms']:>12.2f} {op['total_ms']:>12.2f}")
        print("-"*70)
        if report['bottlenecks']:
            print("\n性能瓶颈 (Top 5):")
            for i, b in enumerate(report['bottlenecks'], 1):
                print(f"  {i}. {b['operation']}: {b['total_ms']:.2f}ms ({b['count']}次)")
        print("="*70 + "\n")
    
    def generate_report(self) -> Dict:
        with self._lock:
            elapsed = time.time() - self._start_time
            total_ops = sum(s.count for s in self._stats.values())
            total_time = sum(s.total_time for s in self._stats.values())
            bottlenecks = sorted(self._stats.values(), key=lambda x: x.total_time, reverse=True)[:5]
            return {
                'summary': {'elapsed_seconds': elapsed, 'total_operations': total_ops, 'total_time_seconds': total_time, 'ops_per_second': total_ops / elapsed if elapsed > 0 else 0, 'unique_operations': len(self._stats)},
                'operations': {name: stats.to_dict() for name, stats in self._stats.items()},
                'bottlenecks': [b.to_dict() for b in bottlenecks],
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }

_global_monitor: Optional[PerformanceMonitor] = None

def get_monitor() -> PerformanceMonitor:
    global _global_monitor
    if _global_monitor is None:
        _global_monitor = PerformanceMonitor(enabled=True)
    return _global_monitor
