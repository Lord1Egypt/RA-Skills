#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DLP 单机轻量级客户端
高性能、低资源占用、自动优化
"""

import os
import sys
import time
import hashlib
from functools import lru_cache
from threading import Lock

# 路径
DLP_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(DLP_PATH, 'lib'))

from agent_dlp import AgentDLP


class DLPCache:
    """轻量级缓存"""
    
    def __init__(self, max_size=1000, ttl=300):
        self.cache = {}
        self.timestamps = {}
        self.max_size = max_size
        self.ttl = ttl
        self.lock = Lock()
        self.hits = 0
        self.misses = 0
    
    def get(self, key):
        with self.lock:
            if key in self.cache:
                if time.time() - self.timestamps[key] < self.ttl:
                    self.hits += 1
                    return self.cache[key]
                else:
                    del self.cache[key]
                    del self.timestamps[key]
            self.misses += 1
            return None
    
    def set(self, key, value):
        with self.lock:
            if len(self.cache) >= self.max_size:
                # 删除最老的
                oldest = min(self.timestamps, key=self.timestamps.get)
                del self.cache[oldest]
                del self.timestamps[oldest]
            self.cache[key] = value
            self.timestamps[key] = time.time()
    
    def stats(self):
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0
        return {"hits": self.hits, "misses": self.misses, "hit_rate": hit_rate}


class LightweightDLP:
    """轻量级 DLP 客户端"""
    
    _instance = None
    _lock = Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        self._initialized = True
        
        # 核心组件
        self.dlp = AgentDLP()
        self.cache = DLPCache(max_size=1000, ttl=300)
        
        # 配置
        self.config = {
            "cache_enabled": True,
            "short_text_skip": True,
            "min_text_length": 3,
            "timeout_ms": 100,
        }
        
        # 统计
        self.stats = {
            "total_checks": 0,
            "blocked": 0,
            "cache_hits": 0,
            "total_time_ms": 0,
        }
    
    def _hash(self, text):
        """快速 hash"""
        return hashlib.md5(text.encode()).hexdigest()
    
    def check(self, text, use_cache=True):
        """检查文本 - 高性能版本"""
        start = time.perf_counter()
        
        # 1. 短文本跳过
        if self.config["short_text_skip"] and len(text) < self.config["min_text_length"]:
            return {
                "blocked": False,
                "result": text,
                "findings": [],
                "cached": False,
                "time_ms": 0,
                "skipped": True
            }
        
        # 2. 缓存检查
        if use_cache and self.config["cache_enabled"]:
            cache_key = self._hash(text)
            cached = self.cache.get(cache_key)
            if cached:
                self.stats["cache_hits"] += 1
                return cached
        
        # 3. 实际检查
        blocked, result, details = self.dlp.check_output(text)
        
        # 修正: findings 存在就算 blocked
        findings = details.get("findings", [])
        is_blocked = len(findings) > 0
        
        # 4. 构建结果
        output = {
            "blocked": is_blocked,
            "result": result if not is_blocked else text,
            "findings": findings,
            "cached": False,
            "time_ms": (time.perf_counter() - start) * 1000,
            "skipped": False
        }
        
        # 5. 缓存结果
        if use_cache and self.config["cache_enabled"]:
            self.cache.set(cache_key, output)
        
        # 6. 更新统计
        self.stats["total_checks"] += 1
        if blocked:
            self.stats["blocked"] += 1
        self.stats["total_time_ms"] += output["time_ms"]
        
        return output
    
    def check_input(self, text):
        """检查输入"""
        return self.check(text)
    
    def check_output(self, text):
        """检查输出"""
        return self.check(text)
    
    def get_stats(self):
        """获取统计信息"""
        cache_stats = self.cache.stats()
        avg_time = (self.stats["total_time_ms"] / self.stats["total_checks"] * 1000) if self.stats["total_checks"] > 0 else 0
        
        return {
            "total_checks": self.stats["total_checks"],
            "blocked": self.stats["blocked"],
            "cache_hit_rate": cache_stats["hit_rate"],
            "avg_time_ms": avg_time,
            "cache_enabled": self.config["cache_enabled"],
        }
    
    def reset_stats(self):
        """重置统计"""
        self.stats = {
            "total_checks": 0,
            "blocked": 0,
            "cache_hits": 0,
            "total_time_ms": 0,
        }
    
    def clear_cache(self):
        """清空缓存"""
        self.cache.cache.clear()
        self.cache.timestamps.clear()


# 全局实例
_dlp_instance = None

def get_dlp():
    """获取 DLP 实例 (单例)"""
    global _dlp_instance
    if _dlp_instance is None:
        _dlp_instance = LightweightDLP()
    return _dlp_instance


# CLI
def main():
    if len(sys.argv) < 2:
        print("""DLP Lightweight Client
    
Usage:
    python dlp_client.py <command> [args]
    
Commands:
    check <text>       Check text for sensitive data
    stats              Show statistics
    clear              Clear cache
    reset              Reset statistics
    status             Show DLP status
""")
        sys.exit(1)
    
    cmd = sys.argv[1]
    dlp = get_dlp()
    
    if cmd == "check":
        if len(sys.argv) < 3:
            print("Usage: python dlp_client.py check <text>")
            sys.exit(1)
        text = " ".join(sys.argv[2:])
        result = dlp.check(text)
        
        print("\n=== DLP Check Result ===")
        print("Blocked: {}".format(result["blocked"]))
        print("Time: {:.2f} ms".format(result["time_ms"]))
        print("Cached: {}".format(result["cached"]))
        if result["findings"]:
            print("Findings:")
            for f in result["findings"]:
                print("  - {} ({})".format(f["description"], f["severity"]))
        else:
            print("No sensitive data found")
    
    elif cmd == "stats":
        stats = dlp.get_stats()
        print("\n=== DLP Statistics ===")
        print("Total checks: {}".format(stats["total_checks"]))
        print("Blocked: {}".format(stats["blocked"]))
        print("Cache hit rate: {:.1f}%".format(stats["cache_hit_rate"]))
        print("Avg time: {:.2f} ms".format(stats["avg_time_ms"]))
        print("Cache enabled: {}".format(stats["cache_enabled"]))
    
    elif cmd == "clear":
        dlp.clear_cache()
        print("Cache cleared")
    
    elif cmd == "reset":
        dlp.reset_stats()
        print("Statistics reset")
    
    elif cmd == "status":
        stats = dlp.get_stats()
        print("DLP Status: Running")
        print("Rules: 166")
        print("Checks: {} | Blocked: {} | Cache: {:.1f}%".format(
            stats["total_checks"], 
            stats["blocked"],
            stats["cache_hit_rate"]
        ))
    
    else:
        print("Unknown command: {}".format(cmd))
        sys.exit(1)


if __name__ == "__main__":
    main()
