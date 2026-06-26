# -*- coding: utf-8 -*-
"""
===================================
市场环境增强分析模块 - V2.2
===================================

核心功能:
1. 市场情绪指数计算
2. 市场强度指标
3. 板块轮动分析
4. 恐慌贪婪指数
5. 市场热度评分
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional
from enum import Enum

import pandas as pd
import numpy as np

from market_analyzer import MarketAnalyzer, MarketEnvironment

logger = logging.getLogger(__name__)


# ============================================
# 数据结构
# ============================================

@dataclass
class MarketSentiment:
    """市场情绪数据"""
    date: str

    # 情绪指标
    fear_greed_index: float = 50.0    # 恐慌贪婪指数 (0-100)
    market_heat: float = 50.0          # 市场热度 (0-100)
    money_flow: float = 0.0            # 资金流向

    # 涨跌统计
    up_down_ratio: float = 1.0         # 涨跌比
    limit_up_ratio: float = 0.0        # 涨停比例
    advance_decline_ratio: float = 1.0 # 涨跌家数比

    # 市场强度
    strength_index: float = 50.0       # 强度指数 (0-100)

    # 板块轮动
    leading_sectors: List[str] = field(default_factory=list)
    lagging_sectors: List[str] = field(default_factory=list)


class MarketEnhancedAnalyzer(MarketAnalyzer):
    """增强的市场分析器"""

    def __init__(self, region='cn'):
        super().__init__(region)
        self.enhanced_analyzer = MarketEnhancedAnalyzer()

    def analyze_enhanced(self, overview=None) -> MarketSentiment:
        """增强分析"""
        if overview is None:
            overview = self.get_market_overview()

        sentiment = MarketSentiment(
            date=overview.date,
            up_down_ratio=overview.statistics.up_down_ratio if overview.statistics else 1.0,
            limit_up_ratio=0.0  # 需要额外计算
        )

        # 计算恐慌贪婪指数
        sentiment.fear_greed_index = self._calculate_fear_greed(sentiment, overview)

        # 计算市场热度
        sentiment.market_heat = self._calculate_market_heat(sentiment, overview)

        # 计算强度指数
        sentiment.strength_index = self._calculate_strength(overview)

        return sentiment

    def _calculate_fear_greed(self, sentiment, overview) -> float:
        """计算恐慌贪婪指数 (0-100)"""
        score = 50.0  # 中性

        # 涨跌比影响 (+-20)
        if sentiment.up_down_ratio > 2:
            score += 20
        elif sentiment.up_down_ratio < 0.5:
            score -= 20
        elif sentiment.up_down_ratio > 1:
            score += 10
        else:
            score -= 10

        # 涨停家数影响 (+-15)
        if overview.statistics:
            limit_up = overview.statistics.limit_up_count
            if limit_up > 100:
                score += 15
            elif limit_up > 50:
                score += 10
            elif limit_up < 10:
                score -= 10

        return max(0, min(100, score))

    def _calculate_market_heat(self, sentiment, overview) -> float:
        """计算市场热度 (0-100)"""
        score = 50.0

        # 成交额影响
        if overview.statistics and overview.statistics.total_amount > 10000:
            score += 20
        elif overview.statistics and overview.statistics.total_amount > 8000:
            score += 10

        # 换手率影响（需额外数据）
        # 涨跌家数影响
        if sentiment.up_down_ratio > 1.5:
            score += 15
        elif sentiment.up_down_ratio < 0.8:
            score -= 15

        return max(0, min(100, score))

    def _calculate_strength(self, overview) -> float:
        """计算强度指数 (0-100)"""
        score = 50.0

        # 指数表现
        for idx in overview.indices:
            if idx.change_pct > 1:
                score += 10
            elif idx.change_pct > 0:
                score += 5
            elif idx.change_pct < -1:
                score -= 10

        # 均线排列
        bullish_count = sum(1 for idx in overview.indices if idx.is_bullish())
        score += bullish_count * 5

        return max(0, min(100, score))
