"""
collectors/ - 数据采集模块

核心组件:
- base.py: 数据结构定义（StructuredItem, StockQuote, Discussion等）
- registry.py: 采集器注册表
- cli.py: 命令行入口

采集器:
- builtin/browser_collector.py: 通用浏览器采集器
- builtin/eastmoney.py: 东方财富采集器
- builtin/xueqiu.py: 雪球采集器

辅助模块:
- stealth.py: 反检测
- proxy_pool.py: 代理池
- cookie_db.py: Cookie持久化
- captcha_solver.py: 验证码识别
- batch_collector.py: 批量采集
- tesseract_ocr.py: OCR优化
"""

from collectors.base import (
    StructuredItem,
    StockQuote,
    Discussion,
    DocItem,
    CollectionStats,
    BaseCollector,
    items_to_dict_list,
    merge_items,
    filter_low_quality,
    sort_by_quality,
    group_by_platform,
)

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