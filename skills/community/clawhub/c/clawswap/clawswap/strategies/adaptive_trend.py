"""
Adaptive Trend Following — Multi-Timeframe with ATR Stops
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Uses EMA crossover on aggregated (15m) bars for trend direction.
Enters on 1m pullbacks within the trend.
ATR-based trailing stop adapts to volatility.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
import numpy as np


@dataclass
class AdaptiveTrendConfig:
    ticker: str = "BTC"
    leverage: float = 1.0           # Matches Rust engine default
    position_size_pct: float = 0.2
    fast_ema: int = 50              # Fast period (Rust fast_period=50 for dual_ma)
    slow_ema: int = 150             # Slow period (Rust slow_period=150)
    atr_period: int = 14            # ATR/ADX period
    adx_threshold: float = 25.0     # Rust adx_threshold=25
    stop_loss_pct: float = 5.0      # Rust stop_loss=0.05
    take_profit_pct: float = 8.0    # Rust take_profit=0.08
    entry_threshold_pct: float = 4.0  # Rust entry_threshold=0.04
    agg_period: int = 1             # 1-min bars (no aggregation to match Rust)
    max_hold_candles: int = 720     # Max 12 hours
    cooldown_candles: int = 240     # Rust adaptive cooldown=240


class AdaptiveTrendStrategy:
    def __init__(self, cfg=None):
        self.cfg = cfg or AdaptiveTrendConfig()
        self.candle_buffer = []  # 1m candles
        self.agg_highs = []
        self.agg_lows = []
        self.agg_closes = []
        self.fast_ema_val = None
        self.slow_ema_val = None
        self.trend_bars = 0  # consecutive bars of trend
        self.trend_dir = 0   # 1 = up, -1 = down, 0 = none
        self.in_position = False
        self.entry_price = 0.0
        self.trail_stop = 0.0
        self.candles_held = 0
        self.cooldown = 0
        self.atr_val = 0.0
        self.current_close = 0.0
        self.recent_high = 0.0

    def _ema_update(self, prev, val, period):
        if prev is None:
            return val
        alpha = 2 / (period + 1)
        return alpha * val + (1 - alpha) * prev

    def on_candle(self, candle: dict):
        self.current_close = candle["close"]
        self.candle_buffer.append(candle)

        if self.in_position:
            self.candles_held += 1
            self.recent_high = max(self.recent_high, candle["high"])
        if self.cooldown > 0:
            self.cooldown -= 1

        # Aggregate to higher timeframe
        if len(self.candle_buffer) >= self.cfg.agg_period:
            bars = self.candle_buffer[-self.cfg.agg_period:]
            agg_h = max(b["high"] for b in bars)
            agg_l = min(b["low"] for b in bars)
            agg_c = bars[-1]["close"]

            self.agg_highs.append(agg_h)
            self.agg_lows.append(agg_l)
            self.agg_closes.append(agg_c)

            # Keep bounded
            if len(self.agg_closes) > 200:
                self.agg_highs = self.agg_highs[-100:]
                self.agg_lows = self.agg_lows[-100:]
                self.agg_closes = self.agg_closes[-100:]

            # Update EMAs
            self.fast_ema_val = self._ema_update(self.fast_ema_val, agg_c, self.cfg.fast_ema)
            self.slow_ema_val = self._ema_update(self.slow_ema_val, agg_c, self.cfg.slow_ema)

            # ATR
            if len(self.agg_highs) >= 2:
                tr = max(
                    agg_h - agg_l,
                    abs(agg_h - self.agg_closes[-2]),
                    abs(agg_l - self.agg_closes[-2])
                )
                if self.atr_val == 0:
                    self.atr_val = tr
                else:
                    self.atr_val = self._ema_update(self.atr_val, tr, self.cfg.atr_period)

            # Update trend
            if self.fast_ema_val and self.slow_ema_val:
                if self.fast_ema_val > self.slow_ema_val:
                    if self.trend_dir == 1:
                        self.trend_bars += 1
                    else:
                        self.trend_dir = 1
                        self.trend_bars = 1
                elif self.fast_ema_val < self.slow_ema_val:
                    if self.trend_dir == -1:
                        self.trend_bars += 1
                    else:
                        self.trend_dir = -1
                        self.trend_bars = 1
                else:
                    self.trend_dir = 0
                    self.trend_bars = 0

            self.candle_buffer = []

    def get_signal(self) -> Optional[str]:
        if self.in_position or self.cooldown > 0:
            return None
        if self.trend_dir != 1 or self.trend_bars < self.cfg.min_trend_bars:
            return None  # Only long in uptrend
        if self.fast_ema_val is None:
            return None

        # Enter on pullback toward fast EMA
        price = self.current_close
        if price <= self.fast_ema_val * (1 + self.cfg.pullback_pct / 100):
            if price > self.slow_ema_val:  # Still above slow EMA
                return "buy"
        return None

    def get_exit_signal(self, current_price: float) -> Optional[str]:
        if not self.in_position:
            return None

        # ATR trailing stop
        if self.atr_val > 0:
            stop = self.recent_high - self.cfg.atr_stop_mult * self.atr_val
            self.trail_stop = max(self.trail_stop, stop)
            if current_price <= self.trail_stop:
                return "trailing_stop"

        # Trend reversal
        if self.trend_dir == -1:
            return "trend_reversal"

        # Timeout
        if self.candles_held >= self.cfg.max_hold_candles:
            return "timeout"

        return None

    def on_fill(self, side, price, position_id):
        if side == "buy":
            self.in_position = True
            self.entry_price = price
            self.recent_high = price
            self.trail_stop = price - self.cfg.atr_stop_mult * self.atr_val if self.atr_val > 0 else price * 0.98
            self.candles_held = 0
        elif side == "sell":
            self.in_position = False
            self.cooldown = self.cfg.cooldown_candles
