"""风控模块 - 动态止损/止盈、仓位管理、相关性风控、黑天鹅熔断"""
from __future__ import annotations
import logging
from dataclasses import dataclass
from typing import Dict, List, Tuple
import numpy as np
import pandas as pd
from .config import get_config
from .models import MarketAnalysis, MarketTrend, TradeSignal

logger = logging.getLogger(__name__)

@dataclass
class PositionResult:
    position_pct: float
    reason: str

@dataclass
class TrailingStop:
    code: str
    entry_price: float
    highest_price: float
    current_stop: float
    atr: float
    def update(self, current_price: float) -> float:
        if current_price > self.highest_price:
            self.highest_price = current_price
            new_stop = self.highest_price - 2 * self.atr
            if new_stop > self.current_stop:
                self.current_stop = new_stop
        return self.current_stop
    def is_triggered(self, current_price: float) -> bool:
        return current_price <= self.current_stop

class RiskManager:
    def __init__(self):
        cfg = get_config()
        self.max_single = cfg.max_single_position
        self.max_total = cfg.max_total_position
        self.min_market_score = cfg.min_market_score
        self.target_rate = cfg.target_rate
        self.stop_loss_rate = cfg.stop_loss_rate
        self.hold_days = cfg.hold_days
        self.circuit_breaker_drop = cfg.circuit_breaker_drop
        self.correlation_threshold = cfg.correlation_threshold
        self._trailing_stops: Dict[str, TrailingStop] = {}

    def calculate_position(self, confidence, market_score, signal_count, atr=0.0, current_price=0.0) -> PositionResult:
        base = self.max_single / max(signal_count, 1)
        market_factor = 1.3 if market_score >= 8 else 1.1 if market_score >= 6 else 0.8 if market_score >= 4 else 0.5 if market_score >= 2 else 0.2
        conf_factor = min(confidence / 0.6, 1.5)
        atr_factor = 1.0
        if atr > 0 and current_price > 0:
            atr_pct = atr / current_price
            if atr_pct > 0.04: atr_factor = 0.7
            elif atr_pct > 0.03: atr_factor = 0.85
        position = max(0.05, min(base * market_factor * conf_factor * atr_factor, self.max_single))
        return PositionResult(round(position, 2), f"基础{base:.0%} | 市场×{market_factor:.1f} | 置信×{conf_factor:.2f}")

    def calculate_stop_loss(self, price, atr=0.0, support=0.0) -> float:
        stops = [price * (1 + self.stop_loss_rate)]
        if atr > 0: stops.append(price - 2 * atr)
        if support > 0 and support < price: stops.append(support * 0.98)
        return round(max(stops), 2)

    def calculate_target(self, price, resistance=0.0, atr=0.0) -> float:
        targets = [price * (1 + self.target_rate)]
        if atr > 0: targets.append(price + 3 * atr)
        if resistance > price: targets.append(resistance)
        return round(min(targets), 2)

    def init_trailing_stop(self, code, entry, atr) -> TrailingStop:
        ts = TrailingStop(code=code, entry_price=entry, highest_price=entry, current_stop=self.calculate_stop_loss(entry, atr), atr=atr)
        self._trailing_stops[code] = ts
        return ts

    def update_trailing_stop(self, code, current_price):
        ts = self._trailing_stops.get(code)
        if not ts: return None
        stop = ts.update(current_price)
        if ts.is_triggered(current_price): return stop
        return None

    def remove_trailing_stop(self, code): self._trailing_stops.pop(code, None)

    def circuit_breaker(self, market: MarketAnalysis) -> Tuple[bool, List[str]]:
        triggers = []
        if market.limit_down > 30: triggers.append(f"跌停潮: {market.limit_down}只跌停")
        if market.score < 2: triggers.append(f"极端弱势: 情绪分 {market.score}/10")
        if market.total_count > 0 and market.down_count / market.total_count > 0.9:
            triggers.append(f"普跌: {market.down_count/market.total_count:.0%} 个股下跌")
        return len(triggers) > 0, triggers

    def check_portfolio_correlation(self, returns_dict: Dict[str, np.ndarray]):
        codes = list(returns_dict.keys())
        if len(codes) < 2: return [], []
        min_len = min(len(v) for v in returns_dict.values())
        aligned = np.array([returns_dict[c][-min_len:] for c in codes])
        corr = np.corrcoef(aligned)
        warnings = []
        for i in range(len(codes)):
            for j in range(i+1, len(codes)):
                if corr[i][j] > self.correlation_threshold:
                    warnings.append(f"{codes[i]} 与 {codes[j]} 相关性 {corr[i][j]:.2f}")
        return warnings, corr.tolist()

    def should_open(self, market): return market.score >= self.min_market_score
    def adjust_confidence(self, raw, bt_wr, n_strats):
        bt_factor = bt_wr / 0.5 if bt_wr > 0 else 0.5
        resonance = min(0.1 * (n_strats - 1), 0.2)
        return round(max(0.0, min(1.0, raw * bt_factor + resonance)), 2)
    def risk_check(self, signals: List[TradeSignal]):
        warnings = []
        total = sum(s.position_pct for s in signals)
        if total > self.max_total: warnings.append(f"总仓位 {total:.0%} 超过上限")
        return warnings
