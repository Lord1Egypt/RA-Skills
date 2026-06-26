"""情绪因子 - 涨跌停/换手率/波动率/赚钱效应/新闻情绪"""
from __future__ import annotations

import logging
import re
from typing import Dict, Optional

import numpy as np
import pandas as pd
import requests

from .base import Factor, FactorResult, register_factor

logger = logging.getLogger(__name__)


@register_factor
class TurnoverFactor(Factor):
    """换手率因子"""
    name = "turnover"
    category = "sentiment"
    description = "近5日平均换手率"

    def compute(self, df: pd.DataFrame, **kwargs) -> Optional[float]:
        if len(df) < 5:
            return None
        # 换手率 = 成交量 / 流通股本，这里用相对换手率近似
        vol = df["volume"].astype(float).tail(5)
        vol_ma20 = df["volume"].astype(float).rolling(20).mean().iloc[-1]
        if vol_ma20 > 0:
            return float(vol.mean() / vol_ma20)
        return None


@register_factor
class VolatilityFactor(Factor):
    """波动率因子"""
    name = "volatility"
    category = "sentiment"
    description = "20日年化波动率"

    def compute(self, df: pd.DataFrame, **kwargs) -> Optional[float]:
        if len(df) < 20:
            return None
        returns = df["close"].astype(float).pct_change().tail(20)
        vol = returns.std() * np.sqrt(252)
        return float(vol) if np.isfinite(vol) else None


@register_factor
class LimitUpMomentum(Factor):
    """涨停动量因子"""
    name = "limit_up_momentum"
    category = "sentiment"
    description = "近10日涨停次数"

    def compute(self, df: pd.DataFrame, **kwargs) -> Optional[float]:
        if len(df) < 10:
            return None
        pct = df["close"].astype(float).pct_change().tail(10) * 100
        limit_ups = (pct >= 9.5).sum()
        return float(limit_ups)


@register_factor
class PriceStrengthFactor(Factor):
    """价格强度因子"""
    name = "price_strength"
    category = "sentiment"
    description = "收盘价在N日高低价区间的位置"

    def compute(self, df: pd.DataFrame, **kwargs) -> Optional[float]:
        n = kwargs.get("lookback", 60)
        if len(df) < n:
            return None

        recent = df.tail(n)
        high = recent["high"].astype(float).max()
        low = recent["low"].astype(float).min()
        close = float(df.iloc[-1]["close"])

        if high == low:
            return 0.5
        return (close - low) / (high - low)


@register_factor
class ConsecutiveUpFactor(Factor):
    """连涨因子"""
    name = "consecutive_up"
    category = "sentiment"
    description = "连续上涨天数"

    def compute(self, df: pd.DataFrame, **kwargs) -> Optional[float]:
        if len(df) < 2:
            return None

        closes = df["close"].astype(float).values
        count = 0
        for i in range(len(closes) - 1, 0, -1):
            if closes[i] > closes[i - 1]:
                count += 1
            else:
                break
        return float(count)


@register_factor
class NewsSentimentFactor(Factor):
    """新闻情绪因子"""
    name = "news_sentiment"
    category = "sentiment"
    description = "东方财富股吧情绪得分"

    def compute(self, df: pd.DataFrame, **kwargs) -> Optional[float]:
        sentiment = kwargs.get("news_sentiment")
        if sentiment is not None:
            return sentiment
        return None

    @staticmethod
    def fetch_sentiment(code: str) -> Optional[float]:
        """获取股吧情绪"""
        try:
            stock_code = code.split(".")[0]
            url = f"https://guba.eastmoney.com/list,{stock_code}.html"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            }
            resp = requests.get(url, headers=headers, timeout=5)
            if resp.status_code == 200:
                text = resp.text
                # 简化情绪分析：统计正面/负面关键词
                positive = len(re.findall(r"涨|利好|突破|新高|放量|金叉|牛市", text))
                negative = len(re.findall(r"跌|利空|破位|新低|缩量|死叉|熊市", text))
                total = positive + negative
                if total > 0:
                    return (positive - negative) / total
        except Exception:
            pass
        return None


class SentimentFactorSet:
    """情绪因子集合"""

    @staticmethod
    def get_factors() -> list:
        return [
            TurnoverFactor(), VolatilityFactor(), LimitUpMomentum(),
            PriceStrengthFactor(), ConsecutiveUpFactor(), NewsSentimentFactor(),
        ]
