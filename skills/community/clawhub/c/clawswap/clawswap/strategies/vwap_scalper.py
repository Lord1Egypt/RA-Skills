"""
VWAP Scalper — Intraday Mean Reversion
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Trades around Volume-Weighted Average Price.
Buy below VWAP - 1σ, sell at VWAP.
Resets VWAP calculation every session (1440 candles = 1 day).
Tight stops, high win rate, small gains.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
import numpy as np


@dataclass
class VwapScalperConfig:
    ticker: str = "BTC"
    leverage: float = 3.0
    position_size_pct: float = 0.10
    session_length: int = 1440       # Reset VWAP every 24h
    entry_sigma: float = 1.2         # Buy below VWAP - N*sigma
    take_profit_sigma: float = 0.0   # Sell at VWAP (0 sigma)
    stop_loss_pct: float = 0.8       # Tight stop
    min_volume_ratio: float = 0.8    # Volume must be > 80% of avg
    max_hold_candles: int = 120      # Max 2 hours
    cooldown_candles: int = 15       # 15min cooldown


class VwapScalperStrategy:
    def __init__(self, cfg=None):
        self.cfg = cfg or VwapScalperConfig()
        self.session_prices = []
        self.session_volumes = []
        self.all_volumes = []
        self.candle_count = 0
        self.in_position = False
        self.entry_price = 0.0
        self.candles_held = 0
        self.cooldown = 0
        self.current_volume = 0.0

    def on_candle(self, candle: dict):
        self.candle_count += 1
        vol = candle.get("volume", 0)
        self.current_volume = vol
        self.all_volumes.append(vol)
        if len(self.all_volumes) > 10000:
            self.all_volumes = self.all_volumes[-5000:]

        # Reset session every N candles
        if len(self.session_prices) >= self.cfg.session_length:
            self.session_prices = []
            self.session_volumes = []

        self.session_prices.append(candle["close"])
        self.session_volumes.append(vol)

        if self.in_position:
            self.candles_held += 1
        if self.cooldown > 0:
            self.cooldown -= 1

    def _vwap_and_std(self):
        if len(self.session_prices) < 60:  # Need at least 1h
            return None, None
        prices = np.array(self.session_prices)
        volumes = np.array(self.session_volumes)
        total_vol = np.sum(volumes)
        if total_vol == 0:
            return np.mean(prices), np.std(prices)
        vwap = np.sum(prices * volumes) / total_vol
        # Volume-weighted standard deviation
        variance = np.sum(volumes * (prices - vwap) ** 2) / total_vol
        std = np.sqrt(variance)
        return vwap, std

    def _volume_ok(self) -> bool:
        if len(self.all_volumes) < 100:
            return True
        avg_vol = np.mean(self.all_volumes[-1000:]) if len(self.all_volumes) >= 1000 else np.mean(self.all_volumes)
        return self.current_volume >= avg_vol * self.cfg.min_volume_ratio

    def get_signal(self) -> Optional[str]:
        if self.in_position or self.cooldown > 0:
            return None
        vwap, std = self._vwap_and_std()
        if vwap is None or std <= 0:
            return None
        price = self.session_prices[-1]
        entry_level = vwap - self.cfg.entry_sigma * std

        if price <= entry_level and self._volume_ok():
            return "buy"
        return None

    def get_exit_signal(self, current_price: float) -> Optional[str]:
        if not self.in_position:
            return None

        # Stop loss
        pnl_pct = (current_price - self.entry_price) / self.entry_price * 100
        if pnl_pct <= -self.cfg.stop_loss_pct:
            return "stop_loss"

        # Take profit at VWAP
        vwap, std = self._vwap_and_std()
        if vwap is not None:
            target = vwap + self.cfg.take_profit_sigma * std
            if current_price >= target:
                return "take_profit"

        # Timeout
        if self.candles_held >= self.cfg.max_hold_candles:
            return "timeout"

        return None

    def on_fill(self, side, price, position_id):
        if side == "buy":
            self.in_position = True
            self.entry_price = price
            self.candles_held = 0
        elif side == "sell":
            self.in_position = False
            self.cooldown = self.cfg.cooldown_candles
