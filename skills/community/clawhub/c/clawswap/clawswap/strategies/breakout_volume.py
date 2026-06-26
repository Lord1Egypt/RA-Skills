"""
Volume Breakout — Momentum with Confirmation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Enter on price breakout above N-period high WITH volume spike.
Volume must be 2x+ average — confirms institutional participation.
Trailing stop locks in gains. Time stop prevents holding losers.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
import numpy as np


@dataclass
class BreakoutVolumeConfig:
    ticker: str = "BTC"
    leverage: float = 1.0           # Matches Rust engine default
    position_size_pct: float = 0.2
    breakout_period: int = 480      # Rust lookback_bars=480
    volume_lookback: int = 120      # 2h volume average
    volume_mult: float = 2.0        # Volume must be 2x average
    stop_loss_pct: float = 5.0      # Rust stop_loss=0.05
    take_profit_pct: float = 8.0    # Rust take_profit=0.08
    max_hold_candles: int = 480     # Max 8 hours
    cooldown_candles: int = 120     # Rust cooldown_bars=120
    min_breakout_pct: float = 0.2   # Rust entry_threshold ~0.04 but ATR filtered


class BreakoutVolumeStrategy:
    def __init__(self, cfg=None):
        self.cfg = cfg or BreakoutVolumeConfig()
        self.highs = []
        self.closes = []
        self.volumes = []
        self.in_position = False
        self.entry_price = 0.0
        self.highest_since_entry = 0.0
        self.candles_held = 0
        self.cooldown = 0

    def on_candle(self, candle: dict):
        self.highs.append(candle["high"])
        self.closes.append(candle["close"])
        self.volumes.append(candle.get("volume", 0))

        max_len = max(self.cfg.breakout_period, self.cfg.volume_lookback) * 2
        if len(self.closes) > max_len:
            self.highs = self.highs[-max_len:]
            self.closes = self.closes[-max_len:]
            self.volumes = self.volumes[-max_len:]

        if self.in_position:
            self.candles_held += 1
            self.highest_since_entry = max(self.highest_since_entry, candle["high"])
        if self.cooldown > 0:
            self.cooldown -= 1

    def get_signal(self) -> Optional[str]:
        if self.in_position or self.cooldown > 0:
            return None
        if len(self.highs) < self.cfg.breakout_period + 1:
            return None
        if len(self.volumes) < self.cfg.volume_lookback + 1:
            return None

        price = self.closes[-1]
        prev_high = max(self.highs[-(self.cfg.breakout_period + 1):-1])
        min_break = prev_high * (1 + self.cfg.min_breakout_pct / 100)

        if price <= min_break:
            return None

        # Volume confirmation
        current_vol = self.volumes[-1]
        avg_vol = np.mean(self.volumes[-(self.cfg.volume_lookback + 1):-1])
        if avg_vol > 0 and current_vol >= avg_vol * self.cfg.volume_mult:
            return "buy"

        return None

    def get_exit_signal(self, current_price: float) -> Optional[str]:
        if not self.in_position:
            return None

        # Trailing stop
        drawdown = (self.highest_since_entry - current_price) / self.highest_since_entry * 100
        if drawdown >= self.cfg.trailing_stop_pct:
            return "trailing_stop"

        # Time stop
        if self.candles_held >= self.cfg.max_hold_candles:
            return "timeout"

        return None

    def on_fill(self, side, price, position_id):
        if side == "buy":
            self.in_position = True
            self.entry_price = price
            self.highest_since_entry = price
            self.candles_held = 0
        elif side == "sell":
            self.in_position = False
            self.cooldown = self.cfg.cooldown_candles
