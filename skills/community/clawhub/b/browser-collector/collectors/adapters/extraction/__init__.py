#!/usr/bin/env python3
"""
collectors/adapters.extraction - 文档提取能力模块

提供文档结构化提取的核心能力:
- structure.py: 结构化数据模型
- spawait.py: SPA动态等待策略
- apiparser.py: API端点解析

Usage:
    from collectors.adapters.extraction.structure import DocumentItem, CodeBlock
    from collectors.adapters.extraction.spawait import SPAWaitStrategy
"""

from .structure import (
    DocumentItem,
    HeadingItem,
    CodeBlock,
    TableItem,
    ImageItem,
    ApiEndpoint,
    ModelInfo,
)
from .spawait import (
    SPAWaitStrategy,
    SPAConfig,
    WaitResult,
    wait_for_page_ready,
)

__all__ = [
    # structure
    'DocumentItem',
    'HeadingItem',
    'CodeBlock',
    'TableItem',
    'ImageItem',
    'ApiEndpoint',
    'ModelInfo',
    # spawait
    'SPAWaitStrategy',
    'SPAConfig',
    'WaitResult',
    'wait_for_page_ready',
]