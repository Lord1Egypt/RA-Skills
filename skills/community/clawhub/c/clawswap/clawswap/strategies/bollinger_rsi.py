"""
Bollinger Band + RSI Mean Reversion
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Buy when price touches lower Bollinger Band AND RSI < 30 (oversold).
Sell when price reaches middle band OR RSI > 70.
Trailing stop for risk management.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
import numpy as np


@dataclass
class BollingerRsiConfig:
    ticker: str = "BTC"
    leverage: float = 1.0           # Matches Rust engine default
    position_size_pct: float = 0.2
    bb_period: int = 240            # 4-hour BB (Rust bb_period=240 for range_scalper)
    bb_std: float = 3.0             # Wider bands (Rust bb_std=3.0)
    rsi_period: int = 84            # ~1.4h RSI
    rsi_oversold: float = 30.0
    rsi_overbought: float = 70.0
    stop_loss_pct: float = 5.0      # Rust stop_loss=0.05
    take_profit_pct: float = 8.0    # Rust take_profit=0.08
    max_hold_candles: int = 360     # Max hold 6 hours
    cooldown_candles: int = 120     # Rust cooldown_bars=120


class BollingerRsiStrategy:
    def __init__(self, cfg=None):
        self.cfg = cfg or BollingerRsiConfig()
        self.closes = []
        self.in_position = False
        self.entry_price = 0.0
        self.highest_since_entry = 0.0
        self.candles_in_position = 0
        self.cooldown = 0

    def on_candle(self, candle: dict):
        self.closes.append(candle["close"])
        if len(self.closes) > self.cfg.bb_period * 3:
            self.closes = self.closes[-self.cfg.bb_period * 3:]
        if self.in_position:
            self.candles_in_position += 1
            self.highest_since_entry = max(self.highest_since_entry, candle["close"])
        if self.cooldown > 0:
            self.cooldown -= 1

    def _rsi(self) -> float:
        if len(self.closes) < self.cfg.rsi_period + 1:
            return 50.0
        prices = np.array(self.closes[-(self.cfg.rsi_period + 1):])
        deltas = np.diff(prices)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        avg_gain = np.mean(gains)
        avg_loss = np.mean(losses)
        if avg_loss == 0:
            return 100.0
        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))

    def _bollinger(self):
        if len(self.closes) < self.cfg.bb_period:
            return None, None, None
        window = np.array(self.closes[-self.cfg.bb_period:])
        mid = np.mean(window)
        std = np.std(window)
        return mid - self.cfg.bb_std * std, mid, mid + self.cfg.bb_std * std

    def get_signal(self) -> Optional[str]:
        if self.in_position or self.cooldown > 0:
            return None
        lower, mid, upper = self._bollinger()
        if lower is None:
            return None
        rsi = self._rsi()
        price = self.closes[-1]
        if price <= lower and rsi < self.cfg.rsi_oversold:
            return "buy"
        return None

    def get_exit_signal(self, current_price: float) -> Optional[str]:
        if not self.in_position:
            return None
        _, mid, _ = self._bollinger()
        rsi = self._rsi()

        # Trailing stop
        drawdown = (self.highest_since_entry - current_price) / self.highest_since_entry * 100
        if drawdown >= self.cfg.trailing_stop_pct:
            return "trailing_stop"

        # Take profit at middle band or RSI overbought
        if mid and current_price >= mid:
            return "take_profit"
        if rsi > self.cfg.rsi_overbought:
            return "take_profit"

        # Max hold time
        if self.candles_in_position >= self.cfg.max_hold_candles:
            return "timeout"

        return None

    def on_fill(self, side, price, position_id):
        if side == "buy":
            self.in_position = True
            self.entry_price = price
            self.highest_since_entry = price
            self.candles_in_position = 0
        elif side == "sell":
            self.in_position = False
            self.entry_price = 0.0
            self.cooldown = self.cfg.cooldown_candles
