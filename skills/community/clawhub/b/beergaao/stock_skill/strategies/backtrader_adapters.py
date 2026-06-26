"""Backtrader 策略适配器 - 将 BeerGaao 策略包装为 Backtrader 策略"""
from __future__ import annotations

import logging
from typing import Optional

import backtrader as bt
import numpy as np

logger = logging.getLogger(__name__)


# ===================== 移动平均线策略 =====================

class BTMAStrategy(bt.Strategy):
    """双均线策略的 Backtrader 适配"""

    params = (
        ('short_period', 5),
        ('long_period', 20),
        ('stop_loss_pct', 0.04),
        ('take_profit_pct', 0.06),
    )

    def __init__(self):
        self.short_ma = bt.indicators.SimpleMovingAverage(
            self.data.close, period=self.params.short_period
        )
        self.long_ma = bt.indicators.SimpleMovingAverage(
            self.data.close, period=self.params.long_period
        )
        self.crossover = bt.indicators.CrossOver(self.short_ma, self.long_ma)
        self.order = None
        self.buy_price = None

    def notify_order(self, order):
        if order.status in [order.Completed]:
            if order.isbuy():
                self.buy_price = order.executed.price
        self.order = None

    def next(self):
        if self.order:
            return

        if not self.position:
            if self.crossover > 0:  # 金叉
                size = self._calculate_size()
                if size > 0:
                    self.order = self.buy(size=size)
        else:
            # 止损止盈检查
            if self.buy_price:
                pnl_pct = (self.data.close[0] - self.buy_price) / self.buy_price
                if pnl_pct <= -self.params.stop_loss_pct:
                    self.order = self.sell(size=self.position.size)
                elif pnl_pct >= self.params.take_profit_pct:
                    self.order = self.sell(size=self.position.size)
                elif self.crossover < 0:  # 死叉
                    self.order = self.sell(size=self.position.size)

    def _calculate_size(self) -> int:
        cash = self.broker.getcash()
        price = self.data.close[0]
        if price <= 0:
            return 0
        size = int(cash * 0.95 / price)
        return (size // 100) * 100


# ===================== MACD 策略 =====================

class BTMACDStrategy(bt.Strategy):
    """MACD 策略的 Backtrader 适配"""

    params = (
        ('fast_period', 12),
        ('slow_period', 26),
        ('signal_period', 9),
        ('stop_loss_pct', 0.04),
        ('take_profit_pct', 0.06),
    )

    def __init__(self):
        self.macd = bt.indicators.MACD(
            self.data.close,
            period_me1=self.params.fast_period,
            period_me2=self.params.slow_period,
            period_signal=self.params.signal_period
        )
        self.crossover = bt.indicators.CrossOver(self.macd.macd, self.macd.signal)
        self.order = None
        self.buy_price = None

    def notify_order(self, order):
        if order.status in [order.Completed]:
            if order.isbuy():
                self.buy_price = order.executed.price
        self.order = None

    def next(self):
        if self.order:
            return

        if not self.position:
            if self.crossover > 0 and self.macd.macd[0] > 0:  # 金叉且 MACD > 0
                size = self._calculate_size()
                if size > 0:
                    self.order = self.buy(size=size)
        else:
            if self.buy_price:
                pnl_pct = (self.data.close[0] - self.buy_price) / self.buy_price
                if pnl_pct <= -self.params.stop_loss_pct:
                    self.order = self.sell(size=self.position.size)
                elif pnl_pct >= self.params.take_profit_pct:
                    self.order = self.sell(size=self.position.size)
                elif self.crossover < 0:  # 死叉
                    self.order = self.sell(size=self.position.size)

    def _calculate_size(self) -> int:
        cash = self.broker.getcash()
        price = self.data.close[0]
        if price <= 0:
            return 0
        size = int(cash * 0.95 / price)
        return (size // 100) * 100


# ===================== RSI 策略 =====================

class BTRSIMeanReversionStrategy(bt.Strategy):
    """RSI 均值回归策略的 Backtrader 适配"""

    params = (
        ('rsi_period', 14),
        ('oversold', 30),
        ('overbought', 70),
        ('stop_loss_pct', 0.04),
        ('take_profit_pct', 0.06),
    )

    def __init__(self):
        self.rsi = bt.indicators.RSI(self.data.close, period=self.params.rsi_period)
        self.order = None
        self.buy_price = None

    def notify_order(self, order):
        if order.status in [order.Completed]:
            if order.isbuy():
                self.buy_price = order.executed.price
        self.order = None

    def next(self):
        if self.order:
            return

        if not self.position:
            if self.rsi[0] < self.params.oversold:  # 超卖
                size = self._calculate_size()
                if size > 0:
                    self.order = self.buy(size=size)
        else:
            if self.buy_price:
                pnl_pct = (self.data.close[0] - self.buy_price) / self.buy_price
                if pnl_pct <= -self.params.stop_loss_pct:
                    self.order = self.sell(size=self.position.size)
                elif pnl_pct >= self.params.take_profit_pct:
                    self.order = self.sell(size=self.position.size)
                elif self.rsi[0] > self.params.overbought:  # 超买
                    self.order = self.sell(size=self.position.size)

    def _calculate_size(self) -> int:
        cash = self.broker.getcash()
        price = self.data.close[0]
        if price <= 0:
            return 0
        size = int(cash * 0.95 / price)
        return (size // 100) * 100


# ===================== 布林带策略 =====================

class BTBollingerStrategy(bt.Strategy):
    """布林带策略的 Backtrader 适配"""

    params = (
        ('period', 20),
        ('devfactor', 2.0),
        ('stop_loss_pct', 0.04),
        ('take_profit_pct', 0.06),
    )

    def __init__(self):
        self.boll = bt.indicators.BollingerBands(
            self.data.close,
            period=self.params.period,
            devfactor=self.params.devfactor
        )
        self.order = None
        self.buy_price = None

    def notify_order(self, order):
        if order.status in [order.Completed]:
            if order.isbuy():
                self.buy_price = order.executed.price
        self.order = None

    def next(self):
        if self.order:
            return

        if not self.position:
            # 触及下轨买入
            if self.data.close[0] < self.boll.bot[0]:
                size = self._calculate_size()
                if size > 0:
                    self.order = self.buy(size=size)
        else:
            if self.buy_price:
                pnl_pct = (self.data.close[0] - self.buy_price) / self.buy_price
                if pnl_pct <= -self.params.stop_loss_pct:
                    self.order = self.sell(size=self.position.size)
                elif pnl_pct >= self.params.take_profit_pct:
                    self.order = self.sell(size=self.position.size)
                elif self.data.close[0] > self.boll.top[0]:  # 触及上轨卖出
                    self.order = self.sell(size=self.position.size)

    def _calculate_size(self) -> int:
        cash = self.broker.getcash()
        price = self.data.close[0]
        if price <= 0:
            return 0
        size = int(cash * 0.95 / price)
        return (size // 100) * 100


# ===================== KDJ 策略 =====================

class BTKDJStrategy(bt.Strategy):
    """KDJ 策略的 Backtrader 适配"""

    params = (
        ('period', 9),
        ('oversold', 20),
        ('overbought', 80),
        ('stop_loss_pct', 0.04),
        ('take_profit_pct', 0.06),
    )

    def __init__(self):
        self.stochastic = bt.indicators.Stochastic(
            self.data,
            period=self.params.period,
            period_dfast=3,
            period_dslow=3
        )
        self.order = None
        self.buy_price = None

    def notify_order(self, order):
        if order.status in [order.Completed]:
            if order.isbuy():
                self.buy_price = order.executed.price
        self.order = None

    def next(self):
        if self.order:
            return

        if not self.position:
            # KDJ 超卖区金叉
            if (self.stochastic.percK[0] < self.params.oversold and
                self.stochastic.percK[0] > self.stochastic.percD[0] and
                self.stochastic.percK[-1] <= self.stochastic.percD[-1]):
                size = self._calculate_size()
                if size > 0:
                    self.order = self.buy(size=size)
        else:
            if self.buy_price:
                pnl_pct = (self.data.close[0] - self.buy_price) / self.buy_price
                if pnl_pct <= -self.params.stop_loss_pct:
                    self.order = self.sell(size=self.position.size)
                elif pnl_pct >= self.params.take_profit_pct:
                    self.order = self.sell(size=self.position.size)
                elif (self.stochastic.percK[0] > self.params.overbought and
                      self.stochastic.percK[0] < self.stochastic.percD[0]):  # 超买区死叉
                    self.order = self.sell(size=self.position.size)

    def _calculate_size(self) -> int:
        cash = self.broker.getcash()
        price = self.data.close[0]
        if price <= 0:
            return 0
        size = int(cash * 0.95 / price)
        return (size // 100) * 100


# ===================== 策略注册表 =====================

BT_STRATEGY_REGISTRY = {
    'MAStrategy': BTMAStrategy,
    'MACDStrategy': BTMACDStrategy,
    'RSIMeanReversionStrategy': BTRSIMeanReversionStrategy,
    'BollingerStrategy': BTBollingerStrategy,
    'KDJStrategy': BTKDJStrategy,
}


def get_bt_strategy(name: str) -> Optional[type]:
    """获取 Backtrader 策略类"""
    return BT_STRATEGY_REGISTRY.get(name)


def list_bt_strategies() -> list:
    """列出所有可用的 Backtrader 策略"""
    return list(BT_STRATEGY_REGISTRY.keys())
