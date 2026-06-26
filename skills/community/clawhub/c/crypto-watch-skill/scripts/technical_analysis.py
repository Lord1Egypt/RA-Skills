#!/usr/bin/env python3
"""
Technical analysis module - pure computation, no network access.

Data must be provided externally (e.g., from MCP tools).
This module does NOT fetch data from any API.
"""

import json
import os
import logging
from datetime import datetime
from typing import Dict, List, Optional
import pandas as pd
import numpy as np

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


class TechnicalAnalysis:
    def __init__(
        self,
        kline_data: List[Dict],
        inst_id: Optional[str] = None,
        bar: Optional[str] = None,
    ):
        """
        Initialize with pre-fetched kline data.

        Args:
            kline_data: List of candle dicts, must contain keys:
                        datetime, open, high, low, close, vol
            inst_id:    Optional label for reference (no network use)
            bar:        Optional label for reference (no network use)
        """
        self.inst_id = inst_id
        self.bar = bar
        self.data = pd.DataFrame(kline_data)
        if not self.data.empty:
            self._process_dataframe()

    def _process_dataframe(self):
        if self.data is not None and not self.data.empty:
            if "datetime" in self.data.columns:
                self.data["datetime"] = pd.to_datetime(self.data["datetime"])
            self.data = (
                self.data.sort_values("datetime").reset_index(drop=True)
                if "datetime" in self.data.columns
                else self.data
            )
            for col in ["open", "high", "low", "close", "vol"]:
                if col in self.data.columns:
                    self.data[col] = pd.to_numeric(self.data[col], errors="coerce")

    def get_all_indicators(self) -> pd.DataFrame:
        if self.data is None or self.data.empty:
            return pd.DataFrame()
        df = self.data.copy()
        close = df["close"] if "close" in df else pd.Series(dtype=float)
        indicators = pd.DataFrame(index=df.index)
        indicators["datetime"] = df.get("datetime")
        indicators["open"] = df.get("open")
        indicators["high"] = df.get("high")
        indicators["low"] = df.get("low")
        indicators["close"] = close
        vol = df.get("vol")
        indicators["volume"] = vol
        # Simple indicators
        indicators["ma5"] = close.rolling(window=5).mean()
        indicators["ma10"] = close.rolling(window=10).mean()
        delta = close.diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.ewm(alpha=1 / 14, adjust=False).mean()
        avg_loss = loss.ewm(alpha=1 / 14, adjust=False).mean()
        rs = avg_gain / avg_loss
        indicators["rsi14"] = 100 - (100 / (1 + rs))
        ema12 = close.ewm(span=12, adjust=False).mean()
        ema26 = close.ewm(span=26, adjust=False).mean()
        dif = ema12 - ema26
        dea = dif.ewm(span=9, adjust=False).mean()
        indicators["macd_dif"] = dif
        indicators["macd_dea"] = dea
        indicators["macd_hist"] = (dif - dea) * 2
        return indicators

    def calculate_fibonacci_retracement(
        self, high: float, low: float
    ) -> Dict[str, float]:
        """Calculate Fibonacci retracement levels."""
        diff = high - low
        levels = {
            "0.0": low,
            "0.236": low + diff * 0.236,
            "0.382": low + diff * 0.382,
            "0.5": low + diff * 0.5,
            "0.618": low + diff * 0.618,
            "0.786": low + diff * 0.786,
            "1.0": high,
        }
        return levels

    def find_support_resistance(
        self, window: int = 5
    ) -> tuple[list[float], list[float]]:
        """Find support and resistance levels using local extrema."""
        if self.data is None or self.data.empty:
            return [], []

        highs = self.data["high"].values
        lows = self.data["low"].values

        supports = []
        resistances = []

        for i in range(window, len(highs) - window):
            # Check for local high (resistance)
            is_high = True
            for j in range(-window, window + 1):
                if j != 0 and highs[i] < highs[i + j]:
                    is_high = False
                    break
            if is_high:
                resistances.append(float(highs[i]))

            # Check for local low (support)
            is_low = True
            for j in range(-window, window + 1):
                if j != 0 and lows[i] > lows[i + j]:
                    is_low = False
                    break
            if is_low:
                supports.append(float(lows[i]))

        return supports, resistances


def analyze_all_assets(
    data_file: Optional[str] = None,
    kline_map: Optional[Dict[str, List[Dict]]] = None,
):
    """
    Analyze multiple assets.

    Args:
        data_file:  Path to a JSON file mapping asset -> {"kline_1d": [...]}
                    (for local/offline use)
        kline_map:  Dict mapping inst_id -> list of candle dicts
                    (for use when data is already fetched via MCP)
    """
    results = {}
    if data_file:
        try:
            with open(data_file, "r", encoding="utf-8") as f:
                all_data = json.load(f)
        except FileNotFoundError:
            logger.info("data_file not found")
            return {}
        for asset, data in all_data.items():
            kline_data = data.get("kline_1d", [])
            ta = TechnicalAnalysis(kline_data)
            result = _analyze_single_asset(ta, asset)
            if result:
                results[asset] = result
    elif kline_map:
        for inst_id, kline_data in kline_map.items():
            ta = TechnicalAnalysis(kline_data, inst_id=inst_id)
            if ta.data.empty:
                continue
            result = _analyze_single_asset(ta, inst_id)
            if result:
                results[inst_id] = result
    else:
        return {}
    result_dir = "result"
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(result_dir, f"technical_analysis_{timestamp}.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False, default=str)
    return results


def _analyze_single_asset(ta: TechnicalAnalysis, asset: str) -> Optional[Dict]:
    if ta.data is None or ta.data.empty:  # type: ignore
        return None
    indicators = (
        ta.get_all_indicators().iloc[-1].to_dict()
        if hasattr(ta, "get_all_indicators")
        else {}
    )
    data_summary = {
        "total_candles": len(ta.data)  # type: ignore
    }
    return {"asset": asset, "indicators": indicators, "data_summary": data_summary}
