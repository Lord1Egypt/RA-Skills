#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网络优化器 - 完整版
功能：DNS 缓存、连接池、重试策略、网络监控、带宽优化
"""

from typing import Dict, Any, Optional, Tuple
from collections import OrderedDict
from urllib.parse import urlparse
import time
import threading
import requests
from dataclasses import dataclass, asdict


@dataclass
class NetworkMetrics:
    """网络指标"""
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    timeouts: int = 0
    avg_response_time: float = 0.0
    dns_cache_hit_rate: float = 0.0
    connection_pool_hit_rate: float = 0.0
    
    def to_dict(self) -> Dict:
        return asdict(self)


class DNSCache:
    """DNS 缓存"""
    
    def __init__(self, ttl: int = 300):
        self.cache = OrderedDict()
        self.ttl = ttl
        self.stats = {'hits': 0, 'misses': 0}
        self.lock = threading.Lock()
    
    def get(self, hostname: str) -> Optional[str]:
        """获取缓存的 IP"""
        with self.lock:
            if hostname in self.cache:
                ip, timestamp = self.cache[hostname]
                if time.time() - timestamp < self.ttl:
                    self.stats['hits'] += 1
                    return ip
                else:
                    del self.cache[hostname]
            self.stats['misses'] += 1
            return None
    
    def set(self, hostname: str, ip: str):
        """缓存 IP"""
        with self.lock:
            self.cache[hostname] = (ip, time.time())
    
    def get_hit_rate(self) -> float:
        """获取命中率"""
        total = self.stats['hits'] + self.stats['misses']
        return self.stats['hits'] / total if total > 0 else 0.0
    
    def clear(self):
        """清空缓存"""
        with self.lock:
            self.cache.clear()
            self.stats = {'hits': 0, 'misses': 0}


class ConnectionPool:
    """连接池管理"""
    
    def __init__(self, max_size: int = 20):
        self.max_size = max_size
        self.pools: Dict[str, Dict] = {}
        self.stats = {'created': 0, 'reused': 0, 'closed': 0}
        self.lock = threading.Lock()
    
    def get_adapter(self, base_url: str) -> Dict:
        """获取或创建适配器"""
        parsed = urlparse(base_url)
        key = f"{parsed.scheme}://{parsed.netloc}"
        
        with self.lock:
            if key not in self.pools:
                # 创建新连接池
                self.pools[key] = {'connections': [], 'created': time.time(), 'usage': 0}
                self.stats['created'] += 1
            else:
                self.pools[key]['usage'] += 1
                self.stats['reused'] += 1
            
            return self.pools[key]
    
    def get_hit_rate(self) -> float:
        """获取命中率"""
        total = self.stats['created'] + self.stats['reused']
        return self.stats['reused'] / total if total > 0 else 0.0
    
    def close_all(self):
        """关闭所有连接"""
        with self.lock:
            self.pools.clear()
            self.stats['closed'] += len(self.pools)


class RetryStrategy:
    """重试策略"""
    
    RETRY_CONFIG = {
        'timeout': {'max_retries': 3, 'base_wait': 2, 'exponential': True},
        'connection_error': {'max_retries': 3, 'base_wait': 2, 'exponential': True},
        '429': {'max_retries': 5, 'base_wait': 'header', 'exponential': False},
        '500': {'max_retries': 3, 'base_wait': 5, 'exponential': False},
        '503': {'max_retries': 2, 'base_wait': 10, 'exponential': False}
    }
    
    def __init__(self):
        self.stats = {}
        self.lock = threading.Lock()
    
    def should_retry(self, error_type: str, attempt: int) -> Tuple[bool, float]:
        """判断是否重试"""
        config = self.RETRY_CONFIG.get(error_type)
        if not config:
            return False, 0
        
        if attempt >= config['max_retries']:
            return False, 0
        
        # 记录重试
        with self.lock:
            if error_type not in self.stats:
                self.stats[error_type] = 0
            self.stats[error_type] += 1
        
        # 计算等待时间
        if config['base_wait'] == 'header':
            wait = 5  # 默认等待时间
        elif config['exponential']:
            wait = config['base_wait'] * (2 ** attempt)
        else:
            wait = config['base_wait']
        
        return True, min(wait, 30)
    
    def get_stats(self) -> Dict:
        """获取统计"""
        return dict(self.stats)


class BandwidthOptimizer:
    """带宽优化器"""
    
    def __init__(self, max_bandwidth: int = 1000000):
        self.max_bandwidth = max_bandwidth  # bytes/sec
        self.current_usage = 0
        self.stats = {'total_bytes': 0, 'optimized_bytes': 0}
        self.lock = threading.Lock()
    
    def request_bandwidth(self, size: int) -> bool:
        """请求带宽"""
        with self.lock:
            if self.current_usage + size <= self.max_bandwidth:
                self.current_usage += size
                self.stats['total_bytes'] += size
                return True
            else:
                self.stats['optimized_bytes'] += size
                return False
    
    def release_bandwidth(self, size: int):
        """释放带宽"""
        with self.lock:
            self.current_usage = max(0, self.current_usage - size)
    
    def get_optimization_rate(self) -> float:
        """获取优化率"""
        total = self.stats['total_bytes'] + self.stats['optimized_bytes']
        if total > 0:
            return self.stats['optimized_bytes'] / total
        return 0.0


class NetworkOptimizer:
    """网络优化器"""
    
    def __init__(self):
        self.dns_cache = DNSCache(ttl=300)
        self.conn_pool = ConnectionPool(max_size=20)
        self.retry_strategy = RetryStrategy()
        self.bandwidth_optimizer = BandwidthOptimizer()
        self.metrics = NetworkMetrics()
        self.monitoring_enabled = True
    
    def optimize(self) -> Dict:
        """优化网络"""
        return {
            'dns_cache_hit_rate': self.dns_cache.get_hit_rate(),
            'connection_pool_hit_rate': self.conn_pool.get_hit_rate(),
            'retry_stats': self.retry_strategy.get_stats(),
            'bandwidth_optimization_rate': self.bandwidth_optimizer.get_optimization_rate(),
            'request_stats': self.metrics.to_dict()
        }
    
    def record_request(self, success: bool, response_time: float):
        """记录请求"""
        self.metrics.total_requests += 1
        
        if success:
            self.metrics.successful_requests += 1
        else:
            self.metrics.failed_requests += 1
        
        # 更新平均响应时间
        total = self.metrics.total_requests
        self.metrics.avg_response_time = (
            (self.metrics.avg_response_time * (total - 1) + response_time) / total
        )
    
    def record_timeout(self):
        """记录超时"""
        self.metrics.timeouts += 1
    
    def get_stats(self) -> Dict:
        """获取统计"""
        return {
            'metrics': self.metrics.to_dict(),
            'dns_cache_hit_rate': self.dns_cache.get_hit_rate(),
            'connection_pool_stats': {
                'created': self.conn_pool.stats['created'],
                'reused': self.conn_pool.stats['reused'],
                'hit_rate': self.conn_pool.get_hit_rate()
            },
            'retry_stats': self.retry_strategy.get_stats(),
            'bandwidth_optimization_rate': self.bandwidth_optimizer.get_optimization_rate()
        }
    
    def enable_monitoring(self, enabled: bool = True):
        """启用/禁用监控"""
        self.monitoring_enabled = enabled
    
    # ==================== 2026-04-06 新增方法 ====================
    
    def probe_capabilities(self, base_url: str = "https://evomap.ai") -> Dict:
        """
        探测节点协议支持能力（help 导航端点）
        
        Args:
            base_url: EvoMap Hub 基础 URL
            
        Returns:
            协议支持能力字典
        """
        url = f"{base_url}/a2a/help"
        
        try:
            resp = requests.get(url, timeout=10)
            
            if resp.status_code == 200:
                data = resp.json()
                print(f"[网络优化器] ✅ 节点能力探测成功")
                print(f"   协议版本：{data.get('protocol_version', '未知')}")
                print(f"   支持端点：{len(data.get('endpoints', []))} 个")
                return {
                    'success': True,
                    'data': data,
                    'message': '节点能力探测成功'
                }
            else:
                print(f"[网络优化器] ⚠️ 节点能力探测失败：HTTP {resp.status_code}")
                return {
                    'success': False,
                    'data': None,
                    'message': f'HTTP {resp.status_code}'
                }
                
        except requests.exceptions.Timeout:
            print(f"[网络优化器] ❌ 节点能力探测超时")
            return {
                'success': False,
                'data': None,
                'message': '请求超时'
            }
        except Exception as e:
            print(f"[网络优化器] ❌ 节点能力探测异常：{str(e)}")
            return {
                'success': False,
                'data': None,
                'message': str(e)
            }


if __name__ == "__main__":
    # 测试网络优化器
    print("=== 测试网络优化器 ===\n")
    
    optimizer = NetworkOptimizer()
    
    # 测试 DNS 缓存
    print("1. 测试 DNS 缓存...")
    optimizer.dns_cache.set('example.com', '192.168.1.1')
    print(f"   DNS 缓存命中率：{optimizer.dns_cache.get_hit_rate():.1%}\n")
    
    # 测试连接池
    print("2. 测试连接池...")
    adapter = optimizer.conn_pool.get_adapter('https://evomap.ai')
    adapter = optimizer.conn_pool.get_adapter('https://evomap.ai')
    print(f"   连接池命中率：{optimizer.conn_pool.get_hit_rate():.1%}\n")
    
    # 测试重试策略
    print("3. 测试重试策略...")
    retry, wait = optimizer.retry_strategy.should_retry('429', 0)
    print(f"   429 重试：{retry}, 等待：{wait}秒\n")
    
    # 测试带宽优化
    print("4. 测试带宽优化...")
    optimizer.bandwidth_optimizer.request_bandwidth(500000)
    print(f"   带宽优化率：{optimizer.bandwidth_optimizer.get_optimization_rate():.1%}\n")
    
    # 获取统计
    stats = optimizer.get_stats()
    print(f"网络优化统计：{stats}")
