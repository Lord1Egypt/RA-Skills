"""Baseline AutoTradeResearch strategy for backtesting.py."""

from __future__ import annotations

import pandas as pd
from backtesting import Strategy


def sma(values, window: int):
    """Return a simple moving average as a numpy-compatible sequence."""

    return pd.Series(values).rolling(window=window, min_periods=window).mean()


class AutoTradeStrategy(Strategy):
    """Readable long-only SMA crossover baseline."""

    fast_window = 20
    slow_window = 50

    def init(self) -> None:
        close = self.data.Close
        self.fast_sma = self.I(sma, close, self.fast_window)
        self.slow_sma = self.I(sma, close, self.slow_window)

    def next(self) -> None:
        if len(self.data.Close) < self.slow_window:
            return

        crossed_up = self.fast_sma[-1] > self.slow_sma[-1] and self.fast_sma[-2] <= self.slow_sma[-2]
        crossed_down = self.fast_sma[-1] < self.slow_sma[-1] and self.fast_sma[-2] >= self.slow_sma[-2]

        if crossed_up:
            if not self.position:
                self.buy()
            return

        if crossed_down and self.position:
            self.position.close()
