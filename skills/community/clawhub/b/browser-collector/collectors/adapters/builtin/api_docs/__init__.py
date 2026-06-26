#!/usr/bin/env python3
"""
collectors/adapters/builtin/api_docs - API文档适配器

提供各类API文档站点的专用适配器。

当前支持:
- Kimi API文档 (platform.kimi.com)
- MiniMax API文档 (platform.minimaxi.com)

Usage:
    from collectors.adapters.builtin.api_docs import KimiApiAdapter, MiniMaxApiAdapter
"""

from .kimi import (
    KimiApiAdapter,
    KimiApiEndpoint,
    KimiApiDoc,
    ApiParameter,
    ApiExample,
)

from .minimax import (
    MiniMaxApiAdapter,
    MiniMaxApiEndpoint,
    MiniMaxApiDoc,
    MiniMaxParameter,
)

__all__ = [
    # Kimi
    'KimiApiAdapter',
    'KimiApiEndpoint',
    'KimiApiDoc',
    'ApiParameter',
    'ApiExample',
    # MiniMax
    'MiniMaxApiAdapter',
    'MiniMaxApiEndpoint',
    'MiniMaxApiDoc',
    'MiniMaxParameter',
]
