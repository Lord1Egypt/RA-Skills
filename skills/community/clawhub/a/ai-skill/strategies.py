"""
ClawMarkets 交易策略库
实现动量策略、价值策略、套利策略
"""

import asyncio
from typing import Optional, Dict, Any, List, Tuple
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
import numpy as np
import pandas as pd


class SignalType(Enum):
    """交易信号类型"""
    STRONG_BUY = "strong_buy"
    BUY = "buy"
    HOLD = "hold"
    SELL = "sell"
    STRONG_SELL = "strong_sell"


@dataclass
class TradingSignal:
    """交易信号"""
    market_id: str
    signal: SignalType
    confidence: float  # 0.0 - 1.0
    reason: str
    target_shares: int = 0
    target_price: Optional[float] = None


class BaseStrategy(ABC):
    """策略基类"""

    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description

    @abstractmethod
    async def analyze(self, market_data: Dict[str, Any]) -> TradingSignal:
        """分析市场并生成交易信号"""
        pass

    @abstractmethod
    def get_parameters(self) -> Dict[str, Any]:
        """获取策略参数"""
        pass


class MomentumStrategy(BaseStrategy):
    """
    动量策略
    基于价格趋势和动量指标进行交易
    - 上涨趋势时买入
    - 下跌趋势时卖出
    """

    def __init__(
        self,
        lookback_period: int = 20,
        momentum_threshold: float = 0.05,
        ma_period: int = 10
    ):
        super().__init__(
            name="动量策略",
            description="基于价格动量和趋势进行交易"
        )
        self.lookback_period = lookback_period
        self.momentum_threshold = momentum_threshold
        self.ma_period = ma_period

    def get_parameters(self) -> Dict[str, Any]:
        return {
            "lookback_period": self.lookback_period,
            "momentum_threshold": self.momentum_threshold,
            "ma_period": self.ma_period
        }

    async def analyze(self, market_data: Dict[str, Any]) -> TradingSignal:
        """
        分析动量信号

        Args:
            market_data: 包含 price_history, current_price 等字段

        Returns:
            TradingSignal: 交易信号
        """
        price_history = market_data.get('price_history', [])
        current_price = market_data.get('current_price', 0)

        if len(price_history) < self.lookback_period:
            return TradingSignal(
                market_id=market_data.get('market_id', 'unknown'),
                signal=SignalType.HOLD,
                confidence=0.0,
                reason="历史数据不足"
            )

        # 计算动量
        prices = np.array(price_history[-self.lookback_period:])
        momentum = (prices[-1] - prices[0]) / prices[0]

        # 计算移动平均
        ma = np.mean(prices[-self.ma_period:])
        price_vs_ma = (current_price - ma) / ma

        # 生成信号
        if momentum > self.momentum_threshold and price_vs_ma > 0.02:
            confidence = min(1.0, momentum / 0.1)
            return TradingSignal(
                market_id=market_data.get('market_id', 'unknown'),
                signal=SignalType.BUY,
                confidence=confidence,
                reason=f"动量强劲：{momentum:.2%}, 价格高于 MA: {price_vs_ma:.2%}",
                target_shares=int(100 * confidence)
            )
        elif momentum < -self.momentum_threshold and price_vs_ma < -0.02:
            confidence = min(1.0, abs(momentum) / 0.1)
            return TradingSignal(
                market_id=market_data.get('market_id', 'unknown'),
                signal=SignalType.SELL,
                confidence=confidence,
                reason=f"动量疲弱：{momentum:.2%}, 价格低于 MA: {price_vs_ma:.2%}",
                target_shares=int(100 * confidence)
            )
        else:
            return TradingSignal(
                market_id=market_data.get('market_id', 'unknown'),
                signal=SignalType.HOLD,
                confidence=0.5,
                reason=f"动量中性：{momentum:.2%}"
            )


class ValueStrategy(BaseStrategy):
    """
    价值策略
    基于内在价值评估进行交易
    - 价格低于价值时买入
    - 价格高于价值时卖出
    """

    def __init__(
        self,
        fair_value_method: str = "average",
        margin_of_safety: float = 0.1,
        overvaluation_threshold: float = 0.15
    ):
        super().__init__(
            name="价值策略",
            description="基于内在价值和安全边际进行交易"
        )
        self.fair_value_method = fair_value_method
        self.margin_of_safety = margin_of_safety
        self.overvaluation_threshold = overvaluation_threshold

    def get_parameters(self) -> Dict[str, Any]:
        return {
            "fair_value_method": self.fair_value_method,
            "margin_of_safety": self.margin_of_safety,
            "overvaluation_threshold": self.overvaluation_threshold
        }

    def _calculate_fair_value(self, market_data: Dict[str, Any]) -> float:
        """计算内在价值"""
        price_history = market_data.get('price_history', [])

        if not price_history:
            return market_data.get('current_price', 0)

        if self.fair_value_method == "average":
            return np.mean(price_history)
        elif self.fair_value_method == "median":
            return np.median(price_history)
        elif self.fair_value_method == "min":
            return np.min(price_history)
        else:
            return np.mean(price_history)

    async def analyze(self, market_data: Dict[str, Any]) -> TradingSignal:
        """
        分析价值信号

        Args:
            market_data: 包含 current_price, price_history, fundamentals 等

        Returns:
            TradingSignal: 交易信号
        """
        current_price = market_data.get('current_price', 0)
        fair_value = self._calculate_fair_value(market_data)

        if fair_value == 0:
            return TradingSignal(
                market_id=market_data.get('market_id', 'unknown'),
                signal=SignalType.HOLD,
                confidence=0.0,
                reason="无法计算内在价值"
            )

        # 计算折价/溢价率
        discount_rate = (fair_value - current_price) / fair_value

        # 生成信号
        if discount_rate > self.margin_of_safety:
            confidence = min(1.0, discount_rate / 0.2)
            return TradingSignal(
                market_id=market_data.get('market_id', 'unknown'),
                signal=SignalType.BUY,
                confidence=confidence,
                reason=f"低估：折价 {discount_rate:.2%}, 内在价值 {fair_value:.2f}",
                target_shares=int(100 * confidence),
                target_price=fair_value
            )
        elif discount_rate < -self.overvaluation_threshold:
            confidence = min(1.0, abs(discount_rate) / 0.2)
            return TradingSignal(
                market_id=market_data.get('market_id', 'unknown'),
                signal=SignalType.SELL,
                confidence=confidence,
                reason=f"高估：溢价 {abs(discount_rate):.2%}, 内在价值 {fair_value:.2f}",
                target_shares=int(100 * confidence)
            )
        else:
            return TradingSignal(
                market_id=market_data.get('market_id', 'unknown'),
                signal=SignalType.HOLD,
                confidence=0.5,
                reason=f"合理估值：折价 {discount_rate:.2%}"
            )


class ArbitrageStrategy(BaseStrategy):
    """
    套利策略
    寻找市场间的价格差异进行套利
    - 跨市场价差套利
    - 时间套利
    """

    def __init__(
        self,
        min_spread: float = 0.03,
        max_position: int = 1000
    ):
        super().__init__(
            name="套利策略",
            description="寻找价格差异进行无风险套利"
        )
        self.min_spread = min_spread
        self.max_position = max_position

    def get_parameters(self) -> Dict[str, Any]:
        return {
            "min_spread": self.min_spread,
            "max_position": self.max_position
        }

    async def analyze(
        self,
        market_data: Dict[str, Any],
        reference_market_data: Optional[Dict[str, Any]] = None
    ) -> TradingSignal:
        """
        分析套利机会

        Args:
            market_data: 当前市场数据
            reference_market_data: 参考市场数据（用于跨市场套利）

        Returns:
            TradingSignal: 交易信号
        """
        current_price = market_data.get('current_price', 0)

        # 跨市场套利
        if reference_market_data is not None:
            ref_price = reference_market_data.get('current_price', 0)
            if ref_price == 0:
                return TradingSignal(
                    market_id=market_data.get('market_id', 'unknown'),
                    signal=SignalType.HOLD,
                    confidence=0.0,
                    reason="参考价格无效"
                )

            spread = (current_price - ref_price) / ref_price

            if spread < -self.min_spread:
                confidence = min(1.0, abs(spread) / 0.05)
                return TradingSignal(
                    market_id=market_data.get('market_id', 'unknown'),
                    signal=SignalType.BUY,
                    confidence=confidence,
                    reason=f"跨市场套利：价差 {spread:.2%}, 参考价格 {ref_price:.2f}",
                    target_shares=min(self.max_position, int(100 * confidence))
                )
            elif spread > self.min_spread:
                confidence = min(1.0, spread / 0.05)
                return TradingSignal(
                    market_id=market_data.get('market_id', 'unknown'),
                    signal=SignalType.SELL,
                    confidence=confidence,
                    reason=f"跨市场套利：价差 {spread:.2%}, 参考价格 {ref_price:.2f}",
                    target_shares=min(self.max_position, int(100 * confidence))
                )

        # 时间套利（基于价格回归）
        price_history = market_data.get('price_history', [])
        if len(price_history) >= 5:
            recent_avg = np.mean(price_history[-5:])
            deviation = (current_price - recent_avg) / recent_avg

            if deviation < -self.min_spread:
                confidence = min(1.0, abs(deviation) / 0.05)
                return TradingSignal(
                    market_id=market_data.get('market_id', 'unknown'),
                    signal=SignalType.BUY,
                    confidence=confidence,
                    reason=f"时间套利：价格偏离 {deviation:.2%}, 预期回归",
                    target_shares=min(self.max_position, int(100 * confidence))
                )
            elif deviation > self.min_spread:
                confidence = min(1.0, deviation / 0.05)
                return TradingSignal(
                    market_id=market_data.get('market_id', 'unknown'),
                    signal=SignalType.SELL,
                    confidence=confidence,
                    reason=f"时间套利：价格偏离 {deviation:.2%}, 预期回归",
                    target_shares=min(self.max_position, int(100 * confidence))
                )

        return TradingSignal(
            market_id=market_data.get('market_id', 'unknown'),
            signal=SignalType.HOLD,
            confidence=0.5,
            reason="无套利机会"
        )


class StrategyExecutor:
    """策略执行器 - 组合多个策略"""

    def __init__(self, strategies: List[BaseStrategy]):
        self.strategies = strategies
        self.results: Dict[str, List[TradingSignal]] = {}

    async def execute_all(self, market_data: Dict[str, Any]) -> Dict[str, TradingSignal]:
        """
        执行所有策略并返回信号

        Args:
            market_data: 市场数据

        Returns:
            Dict[str, TradingSignal]: 每个策略的信号
        """
        results = {}
        for strategy in self.strategies:
            signal = await strategy.analyze(market_data)
            results[strategy.name] = signal
            self.results[strategy.name] = self.results.get(strategy.name, []) + [signal]
        return results

    def get_consensus_signal(self, signals: Dict[str, TradingSignal]) -> TradingSignal:
        """
        获取策略共识信号

        Args:
            signals: 各策略的信号

        Returns:
            TradingSignal: 共识信号
        """
        if not signals:
            return TradingSignal(
                market_id="unknown",
                signal=SignalType.HOLD,
                confidence=0.0,
                reason="无策略信号"
            )

        # 加权投票
        signal_scores = {
            SignalType.STRONG_BUY: 2,
            SignalType.BUY: 1,
            SignalType.HOLD: 0,
            SignalType.SELL: -1,
            SignalType.STRONG_SELL: -2
        }

        weighted_score = 0
        total_confidence = 0

        for signal in signals.values():
            score = signal_scores.get(signal.signal, 0)
            weighted_score += score * signal.confidence
            total_confidence += signal.confidence

        avg_score = weighted_score / total_confidence if total_confidence > 0 else 0

        # 转换为共识信号
        if avg_score >= 1.5:
            consensus = SignalType.STRONG_BUY
        elif avg_score >= 0.5:
            consensus = SignalType.BUY
        elif avg_score <= -1.5:
            consensus = SignalType.STRONG_SELL
        elif avg_score <= -0.5:
            consensus = SignalType.SELL
        else:
            consensus = SignalType.HOLD

        return TradingSignal(
            market_id=next(iter(signals.values())).market_id,
            signal=consensus,
            confidence=total_confidence / len(signals),
            reason=f"共识：{len(signals)} 个策略，加权得分 {avg_score:.2f}"
        )


# 策略工厂
def create_momentum_strategy(**kwargs) -> MomentumStrategy:
    """创建动量策略"""
    return MomentumStrategy(**kwargs)


def create_value_strategy(**kwargs) -> ValueStrategy:
    """创建价值策略"""
    return ValueStrategy(**kwargs)


def create_arbitrage_strategy(**kwargs) -> ArbitrageStrategy:
    """创建套利策略"""
    return ArbitrageStrategy(**kwargs)


def create_default_executor() -> StrategyExecutor:
    """创建默认策略执行器（包含所有策略）"""
    strategies = [
        MomentumStrategy(),
        ValueStrategy(),
        ArbitrageStrategy()
    ]
    return StrategyExecutor(strategies)
