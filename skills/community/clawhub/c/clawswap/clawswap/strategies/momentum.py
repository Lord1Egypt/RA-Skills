"""
Momentum Strategy — ClawSwap Agent Template
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Bidirectional trend-following:
- LONG when price breaks above recent high
- SHORT when price breaks below recent low
Trailing stop loss to lock in profits.

Also used as `short_momentum` (short-only variant via alias).
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class MomentumConfig:
    ticker: str = "BTC"
    leverage: float = 1.0               # Matches Rust engine default
    position_size_pct: float = 0.2
    breakout_lookback: int = 480        # Lookback bars (Rust lookback_bars=480)
    entry_threshold_pct: float = 4.0    # Price must move 4% (Rust entry_threshold=0.04)
    take_profit_pct: float = 8.0        # Rust take_profit=0.08
    stop_loss_pct: float = 5.0          # Rust stop_loss=0.05
    trailing_stop_pct: float = 3.0      # Trailing stop (Rust exit_threshold=0.03)
    max_open_positions: int = 1
    direction: str = "both"             # "both", "long", "short"
    cooldown_candles: int = 120         # Rust cooldown_bars=120


@dataclass
class MomentumState:
    in_position: bool = False
    entry_price: float = 0.0
    peak_price: float = 0.0
    trough_price: float = float('inf')
    is_long: bool = True
    position_id: Optional[str] = None
    candle_buffer: list = field(default_factory=list)
    bars_since_exit: int = 999


class MomentumStrategy:
    def __init__(self, cfg=None):
        self.cfg = cfg or MomentumConfig()
        self.state = MomentumState()

    def _open_position(self, is_long: bool, price: float, position_id: str) -> None:
        self.state.in_position = True
        self.state.entry_price = price
        self.state.is_long = is_long
        self.state.peak_price = price
        self.state.trough_price = price
        self.state.position_id = position_id

    def _close_position(self) -> None:
        self.state.in_position = False
        self.state.entry_price = 0.0
        self.state.peak_price = 0.0
        self.state.trough_price = float('inf')
        self.state.position_id = None
        self.state.bars_since_exit = 0

    def on_candle(self, candle: dict) -> None:
        self.state.candle_buffer.append(candle["close"])
        if len(self.state.candle_buffer) > self.cfg.breakout_lookback * 3:
            self.state.candle_buffer.pop(0)
        if not self.state.in_position:
            self.state.bars_since_exit += 1

    def get_signal(self) -> Optional[str]:
        if self.state.in_position:
            return None
        if self.state.bars_since_exit < self.cfg.cooldown_candles:
            return None

        buf = self.state.candle_buffer
        if len(buf) < self.cfg.breakout_lookback + 1:
            return None

        window = buf[-(self.cfg.breakout_lookback + 1):-1]
        window_high = max(window)
        window_low = min(window)
        current = buf[-1]
        threshold = self.cfg.entry_threshold_pct / 100

        # Long signal: price rises from window low
        if self.cfg.direction in ("both", "long"):
            if window_low > 0 and (current - window_low) / window_low >= threshold:
                return "buy"

        # Short signal: price drops from window high
        if self.cfg.direction in ("both", "short"):
            if window_high > 0 and (window_high - current) / window_high >= threshold:
                return "short"

        return None

    def get_exit_signal(self, current_price: float) -> Optional[str]:
        if not self.state.in_position:
            return None

        if self.state.is_long:
            # Update peak for trailing stop
            if current_price > self.state.peak_price:
                self.state.peak_price = current_price
            # Trailing stop
            trail_stop = self.state.peak_price * (1 - self.cfg.trailing_stop_pct / 100)
            if current_price <= trail_stop:
                return "trailing_stop"
            # PnL-based exits
            pnl_pct = (current_price - self.state.entry_price) / self.state.entry_price * 100
        else:
            # Update trough for trailing stop (short)
            if current_price < self.state.trough_price:
                self.state.trough_price = current_price
            trail_stop = self.state.trough_price * (1 + self.cfg.trailing_stop_pct / 100)
            if current_price >= trail_stop:
                return "trailing_stop"
            pnl_pct = (self.state.entry_price - current_price) / self.state.entry_price * 100

        leveraged_pnl = pnl_pct * self.cfg.leverage / 100
        if leveraged_pnl <= -self.cfg.stop_loss_pct / 100:
            return "stop_loss"
        if leveraged_pnl >= self.cfg.take_profit_pct / 100:
            return "take_profit"

        return None

    def on_fill(self, side: str, price: float, position_id: str) -> None:
        if side == "buy":
            self._open_position(is_long=True, price=price, position_id=position_id)
        elif side == "short":
            self._open_position(is_long=False, price=price, position_id=position_id)
        elif side == "sell":
            if self.state.in_position and self.state.is_long:
                self._close_position()
            elif not self.state.in_position and self.cfg.direction == "short":
                self._open_position(is_long=False, price=price, position_id=position_id)
        elif side == "cover":
            if self.state.in_position and not self.state.is_long:
                self._close_position()
        elif side in ("close_long", "close_short", "close"):
            self._close_position()
