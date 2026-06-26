#!/usr/bin/env python3
"""
pytest 配置文件

提供测试夹具和共享配置。
"""

import sys
import os
import pytest

# 添加父目录到 sys.path，以便导入 crypto_advisor
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture
def sample_screenshot_data():
    """示例截图数据"""
    return {
        "price": 594.82,
        "timeframe": "4h",
        "clarity": "clear",
        "confidence": "high",
        "missing_elements": []
    }


@pytest.fixture
def sample_search_data():
    """示例搜索数据"""
    return {
        "min": 595.68,
        "max": 598.79,
        "source": "web_search"
    }


@pytest.fixture
def stablecoin_symbols():
    """稳定币符号列表"""
    return ["USDT", "USDC", "DAI", "FDUSD", "TUSD", "BUSD"]


@pytest.fixture
def meme_symbols():
    """Meme币符号列表"""
    return ["DOGE", "SHIB", "PEPE", "WIF", "MEME", "FLOKI", "BONK"]


@pytest.fixture
def mainstream_symbols():
    """主流币符号列表"""
    return ["BTC", "ETH", "SOL", "BNB", "XRP", "ADA", "AVAX", "DOT", "MATIC", "LINK"]
