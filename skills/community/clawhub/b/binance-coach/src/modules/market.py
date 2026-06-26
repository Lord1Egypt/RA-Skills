"""
market.py — Binance market data fetcher
Handles price data, RSI, moving averages, Fear & Greed index
"""

import time
import requests
import pandas as pd
from binance.spot import Spot
from rich.console import Console
from modules.i18n import t

console = Console()


class MarketData:
    """Fetches and processes market data from Binance and external sources."""

    FEAR_GREED_URL = "https://api.alternative.me/fng/?limit=1"
    KLINE_INTERVALS = {"1h": "1h", "4h": "4h", "1d": "1d", "1w": "1w"}

    def __init__(self, client: Spot):
        self.client = client
        self._price_cache: dict[str, tuple[float, float]] = {}  # symbol -> (price, timestamp)
        self._cache_ttl = 30  # seconds

    def get_price(self, symbol: str) -> float:
        """Get current price for a symbol, with 30s cache to reduce API calls."""
        cached = self._price_cache.get(symbol)
        if cached and (time.time() - cached[1]) < self._cache_ttl:
            return cached[0]
        data = self.client.ticker_price(symbol=symbol)
        price = float(data["price"])
        self._price_cache[symbol] = (price, time.time())
        return price

    def get_klines(self, symbol: str, interval: str = "1d", limit: int = 100) -> pd.DataFrame:
        """Fetch OHLCV kline data as a DataFrame."""
        raw = self.client.klines(symbol=symbol, interval=interval, limit=limit)
        df = pd.DataFrame(raw, columns=[
            "open_time", "open", "high", "low", "close", "volume",
            "close_time", "quote_volume", "trades", "taker_buy_base",
            "taker_buy_quote", "ignore"
        ])
        for col in ["open", "high", "low", "close", "volume"]:
            df[col] = pd.to_numeric(df[col])
        df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
        df.set_index("open_time", inplace=True)
        return df

    def get_rsi(self, symbol: str, period: int = 14, interval: str = "1d") -> float:
        """Calculate RSI for a symbol."""
        df = self.get_klines(symbol, interval=interval, limit=period + 20)
        delta = df["close"].diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)
        avg_gain = gain.ewm(span=period, adjust=False).mean()
        avg_loss = loss.ewm(span=period, adjust=False).mean()
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return round(float(rsi.iloc[-1]), 2)

    def get_moving_averages(self, symbol: str, interval: str = "1d") -> dict:
        """Get SMA 50, SMA 200, EMA 21 for a symbol."""
        df = self.get_klines(symbol, interval=interval, limit=210)
        close = df["close"]
        def safe(val):
            import math
            f = float(val)
            return round(f, 4) if not math.isnan(f) else 0.0

        return {
            "sma_50": safe(close.rolling(50).mean().iloc[-1]),
            "sma_200": safe(close.rolling(200).mean().iloc[-1]),
            "ema_21": safe(close.ewm(span=21, adjust=False).mean().iloc[-1]),
            "current": safe(close.iloc[-1]),
        }

    def get_fear_greed(self) -> dict:
        """Fetch the Crypto Fear & Greed Index."""
        try:
            resp = requests.get(self.FEAR_GREED_URL, timeout=5)
            data = resp.json()["data"][0]
            return {
                "value": int(data["value"]),
                "classification": data["value_classification"],
                "timestamp": data["timestamp"],
            }
        except Exception:
            return {"value": 50, "classification": "Neutral", "timestamp": None}

    def get_market_context(self, symbol: str) -> dict:
        """
        Aggregate all market context for a symbol.
        Returns a rich dict with price, RSI, MAs, F&G, and interpretations.
        Fetches klines once and computes RSI + MAs from the same dataset.
        """
        price = self.get_price(symbol)
        # Fetch klines once (limit=210 covers both RSI(14) and SMA(200))
        df = self.get_klines(symbol, interval="1d", limit=210)
        # Compute RSI from shared klines
        delta = df["close"].diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)
        avg_gain = gain.ewm(span=14, adjust=False).mean()
        avg_loss = loss.ewm(span=14, adjust=False).mean()
        rs = avg_gain / avg_loss
        rsi_series = 100 - (100 / (1 + rs))
        rsi = round(float(rsi_series.iloc[-1]), 2)
        # Compute MAs from same klines
        import math
        def safe(val):
            f = float(val)
            return round(f, 4) if not math.isnan(f) else 0.0
        close = df["close"]
        mas = {
            "sma_50":  safe(close.rolling(50).mean().iloc[-1]),
            "sma_200": safe(close.rolling(200).mean().iloc[-1]),
            "ema_21":  safe(close.ewm(span=21, adjust=False).mean().iloc[-1]),
            "current": safe(close.iloc[-1]),
        }
        fg = self.get_fear_greed()

        # Price vs MAs interpretation
        above_sma50 = price > mas["sma_50"] if mas["sma_50"] else False
        above_sma200 = price > mas["sma_200"] if mas["sma_200"] else False
        trend = t("market.trend.strong_up") if (above_sma50 and above_sma200) else \
                t("market.trend.recovering") if above_sma50 else \
                t("market.trend.downtrend") if not above_sma200 else \
                t("market.trend.mixed")

        # RSI zone (internal key, not translated — used as dict key in DCA_MULTIPLIERS)
        rsi_zone = "overbought" if rsi > 70 else "oversold" if rsi < 30 else \
                   "neutral-high" if rsi > 55 else "neutral-low" if rsi < 45 else "neutral"

        # RSI zone translated label (for display only)
        rsi_zone_label = t(f"market.rsi.{rsi_zone.replace('-', '_')}")

        # Price relative to SMA200 (discount/premium)
        discount_pct = round(((price - mas["sma_200"]) / mas["sma_200"]) * 100, 2) if mas["sma_200"] else 0.0

        return {
            "symbol": symbol,
            "price": price,
            "rsi": rsi,
            "rsi_zone": rsi_zone,           # internal key for DCA logic
            "rsi_zone_label": rsi_zone_label, # translated for display
            "trend": trend,                 # already translated
            "above_sma50": above_sma50,
            "above_sma200": above_sma200,
            "sma_50": mas["sma_50"],
            "sma_200": mas["sma_200"],
            "ema_21": mas["ema_21"],
            "vs_sma200_pct": discount_pct,
            "fear_greed": fg,
        }
