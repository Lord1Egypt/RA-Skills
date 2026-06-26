#!/usr/bin/env python3
"""
collectors/base.py - 数据结构定义

定义所有采集器的核心数据结构:
- StructuredItem: 结构化采集结果（统一输出格式）
- StockQuote: 股票行情数据
- Discussion: 讨论/帖子数据
- 辅助函数

Usage:
    from collectors.base import StructuredItem, StockQuote, items_to_dict_list
"""

import hashlib
import time
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any
from datetime import datetime


# ==================== 数据结构 ====================

@dataclass
class StructuredItem:
    """
    结构化采集结果 - 所有采集器的统一输出格式

    字段说明:
    - title: 标题
    - url: 原始URL
    - platform: 平台名称
    - content: 正文内容（支持长文本）
    - quality_score: 质量评分 (0.0-1.0)
    - metadata: 扩展元数据

    可选字段（部分平台使用）:
    - author: 作者
    - tags: 标签列表
    - published_at: 发布时间
    - raw_id: 平台原始ID

    方法:
    - to_dict(): 转为dict（用于JSON序列化）
    - checksum: 内容MD5校验和
    """
    title: str
    url: str
    platform: str
    content: str = ''
    author: str = ''
    tags: List[str] = field(default_factory=list)
    quality_score: float = 0.5
    metadata: Dict[str, Any] = field(default_factory=dict)
    published_at: str = ''
    raw_id: str = ''
    checksum: str = ''

    def __post_init__(self):
        if not self.checksum and self.content:
            self.checksum = hashlib.md5(self.content[:5000].encode()).hexdigest()[:12]

    def to_dict(self) -> Dict[str, Any]:
        """转为dict（用于JSON序列化）"""
        d = asdict(self)
        # 截断长字段以便展示
        if 'content' in d and len(d['content']) > 500:
            d['content_preview'] = d['content'][:500]
        return d

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'StructuredItem':
        """从dict恢复"""
        allowed = {f.name for f in cls.__dataclass_fields__.values()}
        return cls(**{k: v for k, v in data.items() if k in allowed})

    def __str__(self):
        preview = self.content[:100].replace('\n', ' ')
        return f"<StructuredItem [{self.platform}] '{self.title[:50]}...' score={self.quality_score:.2f}>"


@dataclass
class StockQuote:
    """股票行情数据"""
    symbol: str           # 股票代码
    name: str             # 股票名称
    price: float          # 当前价格
    change_pct: float     # 涨跌幅%
    volume: int           # 成交量
    turnover: float       # 成交额
    open: float           # 开盘价
    high: float           # 最高价
    low: float            # 最低价
    prev_close: float     # 昨收价
    timestamp: str        # 数据时间
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class Discussion:
    """讨论/帖子数据"""
    title: str
    author: str
    content: str
    url: str
    platform: str
    reply_count: int = 0
    like_count: int = 0
    published_at: str = ''
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class DocItem:
    """技术文档条目"""
    title: str
    url: str
    platform: str
    section: str = ''       # 所属章节/分类
    content: str = ''       # 正文
    code_snippets: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    quality_score: float = 0.5
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return asdict(self)


# ==================== 辅助函数 ====================

def items_to_dict_list(items: List[StructuredItem]) -> List[Dict[str, Any]]:
    """将StructuredItem列表转为dict列表（用于JSON序列化）"""
    return [item.to_dict() for item in items]


def merge_items(items: List[StructuredItem], dedup_key: str = 'checksum') -> List[StructuredItem]:
    """
    合并去重StructuredItem列表

    Args:
        items: StructuredItem列表
        dedup_key: 去重依据字段（默认checksum）

    Returns:
        去重后的列表（保留最新）
    """
    seen = {}
    result = []
    for item in items:
        key = getattr(item, dedup_key, None) or item.url
        if key not in seen:
            seen[key] = True
            result.append(item)
    return result


def filter_low_quality(items: List[StructuredItem], threshold: float = 0.5) -> List[StructuredItem]:
    """过滤低质量条目"""
    return [item for item in items if item.quality_score >= threshold]


def sort_by_quality(items: List[StructuredItem], descending: bool = True) -> List[StructuredItem]:
    """按质量评分排序"""
    return sorted(items, key=lambda x: x.quality_score, reverse=descending)


def group_by_platform(items: List[StructuredItem]) -> Dict[str, List[StructuredItem]]:
    """按平台分组"""
    groups = {}
    for item in items:
        if item.platform not in groups:
            groups[item.platform] = []
        groups[item.platform].append(item)
    return groups


# ==================== 采集结果统计 ====================

@dataclass
class CollectionStats:
    """采集统计"""
    total: int = 0
    success: int = 0
    failed: int = 0
    by_platform: Dict[str, int] = field(default_factory=dict)
    avg_quality: float = 0.0
    duration_seconds: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_items(cls, items: List[StructuredItem], duration: float = 0.0) -> 'CollectionStats':
        """从采集结果生成统计"""
        stats = cls(total=len(items), duration_seconds=duration)
        if not items:
            return stats

        stats.success = len(items)
        quality_sum = 0.0
        for item in items:
            quality_sum += item.quality_score
            platform = item.platform
            stats.by_platform[platform] = stats.by_platform.get(platform, 0) + 1

        stats.avg_quality = quality_sum / len(items) if items else 0.0
        return stats


# ==================== BaseCollector ====================

class BaseCollector:
    """
    采集器基类

    提供通用采集逻辑，子类只需实现具体extract方法。
    """

    name: str = 'base'
    platform: str = 'unknown'

    def __init__(self, headless: bool = True):
        self.headless = headless

    def collect(self, url: str, **kwargs) -> StructuredItem:
        """采集单个URL"""
        raise NotImplementedError("子类必须实现collect方法")

    def collect_batch(self, urls: List[str], **kwargs) -> List[StructuredItem]:
        """批量采集"""
        results = []
        for url in urls:
            try:
                item = self.collect(url, **kwargs)
                results.append(item)
            except Exception as e:
                print(f"[{self.name}] 采集失败 {url}: {e}")
        return results

    def _default_extract(self, page, url: str) -> StructuredItem:
        """默认提取逻辑（Playwright Page对象）"""
        from urllib.parse import urlparse
        return StructuredItem(
            title=page.title(),
            url=url,
            platform=self.platform,
            content=page.locator('body').inner_text()[:10000],
            checksum=hashlib.md5(page.content()[:5000].encode()).hexdigest()[:12],
        )


# ==================== 导出 ====================

__all__ = [
    'StructuredItem',
    'StockQuote',
    'Discussion',
    'DocItem',
    'CollectionStats',
    'BaseCollector',
    'items_to_dict_list',
    'merge_items',
    'filter_low_quality',
    'sort_by_quality',
    'group_by_platform',
]