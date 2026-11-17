from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class Stock:
    market: int
    code: str
    name: str = ""

    @property
    def key(self) -> tuple[int, str]:
        return (self.market, self.code)

    @property
    def market_prefix(self) -> str:
        if self.market == 1:
            return "SH"
        if self.market == 0:
            return "SZ"
        return ""

    @property
    def display_code(self) -> str:
        prefix = self.market_prefix
        return f"{prefix}{self.code}" if prefix else self.code


@dataclass(frozen=True, slots=True)
class Quote:
    stock: Stock
    price: float
    open: float
    last_close: float
    volume: float
    amount: float | None = None


@dataclass(frozen=True, slots=True)
class HistoryBaseline:
    stock: Stock
    avg_volume: float
    sample_days: int

    @property
    def ready(self) -> bool:
        return self.avg_volume > 0 and self.sample_days > 0


@dataclass(frozen=True, slots=True)
class Signal:
    stock: Stock
    timestamp: datetime
    price: float
    last_close: float
    open: float
    change_pct: float
    current_volume: float
    avg_volume: float
    expected_volume: float
    volume_ratio: float
    interval_volume: float | None
    interval_spike_ratio: float | None
    server: str

