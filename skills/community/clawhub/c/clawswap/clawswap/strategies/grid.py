"""
Grid Trading Strategy — ClawSwap Agent Template
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Place buy/sell orders at fixed price intervals above/below current price.
Low-risk, profits from sideways oscillation.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class GridConfig:
    ticker: str = "BTC"
    leverage: float = 1.0
    grid_count: int = 3                 # Grids above + below (Rust grid_levels=3)
    grid_spacing_pct: float = 2.0       # 2% spacing (Rust grid_spacing=0.02)
    size_per_grid: float = 100.0        # USD per grid order
    stop_loss_pct: float = 5.0          # Rust stop_loss=0.05
    grid_reset_bars: int = 480          # Reset grid every 8h (Rust grid_reset_bars=480)
    reinvest_profit: bool = True        # Add profits back to grid


@dataclass
class GridLevel:
    price: float
    side: str                           # 'buy' or 'sell'
    filled: bool = False
    order_id: Optional[str] = None


@dataclass
class GridState:
    initialized: bool = False
    center_price: float = 0.0
    levels: list = field(default_factory=list)
    total_profit: float = 0.0


class GridStrategy:
    def __init__(self, cfg=None):
        self.cfg = cfg or GridConfig()
        self.state = GridState()

    def initialize(self, current_price: float) -> list[GridLevel]:
        """Create grid levels centered at current_price. Returns list of levels to place."""
        self.state.center_price = current_price
        self.state.initialized = True
        levels = []
        for i in range(1, self.cfg.grid_count + 1):
            buy_price = current_price * (1 - i * self.cfg.grid_spacing_pct / 100)
            sell_price = current_price * (1 + i * self.cfg.grid_spacing_pct / 100)
            levels.append(GridLevel(price=buy_price, side="buy"))
            levels.append(GridLevel(price=sell_price, side="sell"))
        self.state.levels = sorted(levels, key=lambda l: l.price)
        return self.state.levels

    def on_fill(self, filled_level: GridLevel, current_price: float) -> Optional[GridLevel]:
        """
        When a grid level fills:
        - Buy filled → place sell one level up
        - Sell filled → place buy one level down
        Returns new counter-level to place, or None.
        """
        filled_level.filled = True
        spacing = self.state.center_price * self.cfg.grid_spacing_pct / 100

        if filled_level.side == "buy":
            new_sell_price = filled_level.price + spacing
            profit = spacing  # simplified
            if self.cfg.reinvest_profit:
                self.state.total_profit += profit
            return GridLevel(price=new_sell_price, side="sell")
        else:  # sell
            new_buy_price = filled_level.price - spacing
            return GridLevel(price=new_buy_price, side="buy")

    def get_unfilled_levels(self) -> list[GridLevel]:
        return [l for l in self.state.levels if not l.filled]
