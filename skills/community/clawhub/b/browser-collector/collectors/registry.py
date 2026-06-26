#!/usr/bin/env python3
"""
collectors/registry.py - 采集器注册表

提供全局采集器注册、查询和管理功能。

Usage:
    from collectors.registry import CollectorRegistry, get_registry

    registry = get_registry()
    collector = registry.get('browser')
    registry.register('custom', my_collector)
"""

from typing import Dict, List, Optional, Any
from urllib.parse import urlparse


class CollectorRegistry:
    """
    采集器注册表

    提供:
    - register(name, collector): 注册采集器
    - get(name): 获取采集器
    - list_all(): 列出所有采集器
    - detect_for_url(url): 根据URL检测适用的采集器
    """

    def __init__(self):
        self._collectors: Dict[str, Any] = {}
        self._url_mappings: Dict[str, str] = {}  # domain -> collector_name

    def register(self, name: str, collector: Any):
        """注册采集器"""
        self._collectors[name] = collector

        # 如果采集器有supported_domains，自动建立映射
        if hasattr(collector, 'supported_domains'):
            for domain in collector.supported_domains:
                self._url_mappings[domain] = name

    def register_domain_mapping(self, domain: str, collector_name: str):
        """手动注册域名到采集器的映射"""
        self._url_mappings[domain] = collector_name

    def get(self, name: str) -> Optional[Any]:
        """获取采集器"""
        return self._collectors.get(name)

    def get_or_raise(self, name: str) -> Any:
        """获取采集器，不存在则抛异常"""
        collector = self._collectors.get(name)
        if collector is None:
            available = ', '.join(self._collectors.keys()) or 'none'
            raise ValueError(f"采集器 '{name}' 不存在。可用: {available}")
        return collector

    def list_all(self) -> List[str]:
        """列出所有采集器名称"""
        return list(self._collectors.keys())

    def detect_for_url(self, url: str) -> Optional[str]:
        """
        根据URL检测适用的采集器名称

        Args:
            url: 目标URL

        Returns:
            采集器名称，或None（未找到）
        """
        parsed = urlparse(url)
        domain = parsed.netloc.lower()

        # 精确匹配
        if domain in self._url_mappings:
            return self._url_mappings[domain]

        # 部分匹配（如 www.github.com → github.com）
        for mapped_domain, collector_name in self._url_mappings.items():
            if mapped_domain in domain or domain in mapped_domain:
                return collector_name

        return None

    def get_for_url(self, url: str) -> Optional[Any]:
        """根据URL获取采集器实例"""
        name = self.detect_for_url(url)
        if name:
            return self.get(name)
        return None

    def unregister(self, name: str) -> bool:
        """注销采集器"""
        if name in self._collectors:
            del self._collectors[name]
            # 清理域名映射
            self._url_mappings = {
                d: n for d, n in self._url_mappings.items() if n != name
            }
            return True
        return False

    def clear(self):
        """清空注册表"""
        self._collectors.clear()
        self._url_mappings.clear()

    def get_stats(self) -> Dict[str, Any]:
        """获取注册表统计"""
        return {
            'total_collectors': len(self._collectors),
            'total_domains': len(self._url_mappings),
            'collectors': self.list_all(),
            'domain_mappings': dict(self._url_mappings),
        }


# 全局注册表实例
_global_registry = CollectorRegistry()


def get_registry() -> CollectorRegistry:
    """获取全局注册表"""
    return _global_registry


def register_collector(name: str, collector: Any):
    """快捷注册到全局注册表"""
    get_registry().register(name, collector)


def get_collector(name: str) -> Optional[Any]:
    """从全局注册表获取采集器"""
    return get_registry().get(name)


def detect_collector_for_url(url: str) -> Optional[str]:
    """从全局注册表检测采集器"""
    return get_registry().detect_for_url(url)