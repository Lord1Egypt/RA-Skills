#!/usr/bin/env python3
"""
FocusMind 缓存模块
提供结果缓存以提高性能
"""

import time
import hashlib
import json
from typing import Any, Dict, Optional, Tuple
from dataclasses import dataclass


@dataclass
class CacheEntry:
    """缓存条目"""
    result: Any
    timestamp: float
    ttl: int  # 生存时间(秒)


class ResultCache:
    """
    简单的结果缓存
    
    用于缓存分析结果，避免重复计算
    """
    
    def __init__(self, default_ttl: int = 300, max_size: int = 100):
        """
        Args:
            default_ttl: 默认缓存时间(秒)
            max_size: 最大缓存条目数
        """
        self._cache: Dict[str, CacheEntry] = {}
        self.default_ttl = default_ttl
        self.max_size = max_size
        self.hits = 0
        self.misses = 0
    
    def _make_key(self, context: Any, operation: str) -> str:
        """生成缓存键"""
        # 简单处理：根据内容哈希 + 操作名
        content = str(context)[:1000]  # 限制长度
        raw = f"{operation}:{content}"
        return hashlib.md5(raw.encode()).hexdigest()
    
    def get(self, context: Any, operation: str) -> Optional[Any]:
        """获取缓存结果"""
        key = self._make_key(context, operation)
        
        if key in self._cache:
            entry = self._cache[key]
            # 检查是否过期
            if time.time() - entry.timestamp < entry.ttl:
                self.hits += 1
                return entry.result
            else:
                # 过期删除
                del self._cache[key]
        
        self.misses += 1
        return None
    
    def set(self, context: Any, operation: str, result: Any, ttl: Optional[int] = None):
        """设置缓存"""
        # 超过最大容量时删除最老的
        if len(self._cache) >= self.max_size:
            oldest_key = min(self._cache.keys(), key=lambda k: self._cache[k].timestamp)
            del self._cache[oldest_key]
        
        key = self._make_key(context, operation)
        self._cache[key] = CacheEntry(
            result=result,
            timestamp=time.time(),
            ttl=ttl or self.default_ttl
        )
    
    def clear(self):
        """清空缓存"""
        self._cache.clear()
        self.hits = 0
        self.misses = 0
    
    def get_stats(self) -> Dict[str, Any]:
        """获取缓存统计"""
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0
        
        return {
            "size": len(self._cache),
            "max_size": self.max_size,
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": f"{hit_rate:.1f}%",
            "total_requests": total
        }


# 全局缓存实例
_global_cache = ResultCache()


def get_cache() -> ResultCache:
    """获取全局缓存"""
    return _global_cache


def cached_analysis(func):
    """缓存装饰器"""
    def wrapper(context, *args, **kwargs):
        cache = get_cache()
        operation = func.__name__
        
        # 尝试获取缓存
        cached_result = cache.get(context, operation)
        if cached_result is not None:
            return cached_result
        
        # 执行并缓存
        result = func(context, *args, **kwargs)
        cache.set(context, operation, result)
        return result
    
    return wrapper


# 导出
__all__ = ["ResultCache", "get_cache", "cached_analysis"]
