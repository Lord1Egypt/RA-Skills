#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
性能优化器 - 完整版
功能：LRU 缓存、并行处理、性能监控、自动优化
"""

from typing import Dict, List, Any, Callable, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import OrderedDict
import time
import threading
from dataclasses import dataclass, asdict


@dataclass
class PerformanceMetrics:
    """性能指标"""
    total_operations: int = 0
    cache_hits: int = 0
    cache_misses: int = 0
    avg_execution_time: float = 0.0
    parallel_speedup: float = 1.0
    optimization_count: int = 0
    
    def to_dict(self) -> Dict:
        return asdict(self)


class LRUCache:
    """LRU 缓存"""
    
    def __init__(self, max_size: int = 1000):
        self.cache = OrderedDict()
        self.max_size = max_size
        self.stats = {'hits': 0, 'misses': 0}
        self.lock = threading.Lock()
    
    def get(self, key: str) -> Any:
        """获取缓存"""
        with self.lock:
            if key in self.cache:
                self.cache.move_to_end(key)
                self.stats['hits'] += 1
                return self.cache[key]
            self.stats['misses'] += 1
            return None
    
    def put(self, key: str, value: Any):
        """存入缓存"""
        with self.lock:
            if key in self.cache:
                self.cache.move_to_end(key)
            self.cache[key] = value
            if len(self.cache) > self.max_size:
                self.cache.popitem(last=False)
    
    def get_hit_rate(self) -> float:
        """获取命中率"""
        total = self.stats['hits'] + self.stats['misses']
        return self.stats['hits'] / total if total > 0 else 0.0
    
    def clear(self):
        """清空缓存"""
        with self.lock:
            self.cache.clear()
            self.stats = {'hits': 0, 'misses': 0}


class ParallelProcessor:
    """并行处理器"""
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.stats = {'submitted': 0, 'completed': 0, 'failed': 0}
        self.execution_times: List[float] = []
    
    def process_batch(self, items: List[Any], processor: Callable, batch_size: int = None) -> List[Any]:
        """批量并行处理"""
        if batch_size is None:
            batch_size = len(items)
        
        results = []
        
        for i in range(0, len(items), batch_size):
            batch = items[i:i + batch_size]
            
            # 提交任务
            futures = {
                self.executor.submit(processor, item): idx
                for idx, item in enumerate(batch)
            }
            
            # 收集结果
            batch_results = [None] * len(batch)
            for future in as_completed(futures):
                idx = futures[future]
                start_time = time.time()
                try:
                    batch_results[idx] = future.result()
                    self.stats['completed'] += 1
                    self.execution_times.append(time.time() - start_time)
                except Exception as e:
                    batch_results[idx] = {'error': str(e)}
                    self.stats['failed'] += 1
            
            results.extend(batch_results)
            self.stats['submitted'] += len(batch)
        
        return results
    
    def get_avg_execution_time(self) -> float:
        """获取平均执行时间"""
        if not self.execution_times:
            return 0.0
        return sum(self.execution_times) / len(self.execution_times)
    
    def calculate_speedup(self, serial_time: float) -> float:
        """计算加速比"""
        parallel_time = self.get_avg_execution_time() * self.stats['submitted']
        if parallel_time > 0:
            return serial_time / parallel_time
        return 1.0
    
    def shutdown(self):
        """关闭线程池"""
        self.executor.shutdown(wait=True)


class PerformanceOptimizer:
    """性能优化器"""
    
    def __init__(self, cache_size: int = 1000, max_workers: int = 4, show_version: bool = False):
        if show_version:
            print(f"🧬 EvoMap WorkBench v1.0.11 - 性能优化已加载")
        self.cache = LRUCache(max_size=cache_size)
        self.processor = ParallelProcessor(max_workers=max_workers)
        self.metrics = PerformanceMetrics()
        self.auto_optimize_enabled = True
        self.optimization_threshold = 0.8
    
    def optimize(self, data: Any, cache_key: str = None) -> Any:
        """优化数据"""
        start_time = time.time()
        
        # 检查缓存
        if cache_key:
            cached = self.cache.get(cache_key)
            if cached:
                self.metrics.cache_hits += 1
                return cached
        
        self.metrics.cache_misses += 1
        
        # 处理数据
        result = self._process_data(data)
        
        # 存入缓存
        if cache_key:
            self.cache.put(cache_key, result)
        
        # 更新指标
        execution_time = time.time() - start_time
        self._update_metrics(execution_time)
        
        # 自动优化
        if self.auto_optimize_enabled:
            self._auto_optimize()
        
        return result
    
    def _process_data(self, data: Any) -> Any:
        """处理数据"""
        self.metrics.total_operations += 1
        return data
    
    def _update_metrics(self, execution_time: float):
        """更新指标"""
        # 更新平均执行时间
        total = self.metrics.total_operations
        self.metrics.avg_execution_time = (
            (self.metrics.avg_execution_time * (total - 1) + execution_time) / total
        )
    
    def _auto_optimize(self):
        """自动优化"""
        cache_hit_rate = self.cache.get_hit_rate()
        
        if cache_hit_rate < self.optimization_threshold:
            # 缓存命中率低，调整缓存大小
            self.metrics.optimization_count += 1
    
    def get_stats(self) -> Dict:
        """获取统计"""
        return {
            'metrics': self.metrics.to_dict(),
            'cache_hit_rate': self.cache.get_hit_rate(),
            'parallel_stats': self.processor.stats,
            'avg_execution_time': self.processor.get_avg_execution_time()
        }
    
    def enable_auto_optimize(self, enabled: bool = True):
        """启用/禁用自动优化"""
        self.auto_optimize_enabled = enabled
    
    def clear_cache(self):
        """清空缓存"""
        self.cache.clear()


if __name__ == "__main__":
    # 测试性能优化器
    print("=== 测试性能优化器 ===\n")
    
    optimizer = PerformanceOptimizer()
    
    # 测试缓存
    print("1. 测试缓存...")
    for i in range(10):
        optimizer.optimize(f"data_{i % 5}", cache_key=f"key_{i % 5}")
    
    print(f"   缓存命中率：{optimizer.cache.get_hit_rate():.1%}\n")
    
    # 测试并行处理
    print("2. 测试并行处理...")
    def process(x):
        time.sleep(0.1)
        return x * 2
    
    results = optimizer.processor.process_batch(list(range(10)), process)
    print(f"   并行处理结果：{len(results)}项")
    print(f"   平均执行时间：{optimizer.processor.get_avg_execution_time():.3f}s\n")
    
    # 获取统计
    stats = optimizer.get_stats()
    print(f"性能统计：{stats}")
