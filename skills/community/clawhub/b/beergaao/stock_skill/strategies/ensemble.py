"""策略集成引擎 - 多策略组合、自适应选择、动态权重"""
from __future__ import annotations
import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
import numpy as np
import pandas as pd
from enum import Enum

logger = logging.getLogger(__name__)


class MarketRegime(Enum):
    """市场状态"""
    TREND_UP = "trend_up"
    TREND_DOWN = "trend_down"
    RANGE = "range"
    VOLATILE = "volatile"
    UNKNOWN = "unknown"


@dataclass
class StrategySignal:
    """策略信号"""
    strategy_name: str
    direction: str
    confidence: float
    weight: float = 1.0
    regime: MarketRegime = MarketRegime.UNKNOWN
    metadata: Dict = field(default_factory=dict)


@dataclass
class EnsembleSignal:
    """集成信号"""
    direction: str
    confidence: float
    consensus_score: float
    strategies_agreed: int
    total_strategies: int
    regime: MarketRegime
    details: List[StrategySignal] = field(default_factory=list)

    def summary(self) -> str:
        return (
            f"方向={self.direction}, 置信={self.confidence:.2f}, "
            f"共识={self.consensus_score:.2f}, "
            f"策略={self.strategies_agreed}/{self.total_strategies}, "
            f"市场={self.regime.value}"
        )


class MarketRegimeDetector:
    """市场状态检测器"""

    def __init__(self, lookback: int = 60):
        self.lookback = lookback

    def detect(self, df: pd.DataFrame) -> MarketRegime:
        """检测市场状态"""
        if len(df) < self.lookback:
            return MarketRegime.UNKNOWN

        close = df["close"].astype(float)
        returns = close.pct_change().dropna()

        if len(returns) < 20:
            return MarketRegime.UNKNOWN

        recent_returns = returns.iloc[-20:]
        volatility = recent_returns.std()
        mean_return = recent_returns.mean()

        ma20 = close.rolling(20).mean().iloc[-1]
        ma60 = close.rolling(60).mean().iloc[-1] if len(close) >= 60 else ma20
        current_price = float(close.iloc[-1])

        adx = self._calculate_adx(df)

        if volatility > 0.03:
            return MarketRegime.VOLATILE

        if adx > 25:
            if current_price > ma20 > ma60:
                return MarketRegime.TREND_UP
            elif current_price < ma20 < ma60:
                return MarketRegime.TREND_DOWN

        return MarketRegime.RANGE

    def _calculate_adx(self, df: pd.DataFrame, period: int = 14) -> float:
        """计算ADX（平均趋向指数）"""
        try:
            high = df["high"].astype(float)
            low = df["low"].astype(float)
            close = df["close"].astype(float)

            plus_dm = high.diff()
            minus_dm = -low.diff()

            plus_dm[plus_dm < 0] = 0
            minus_dm[minus_dm < 0] = 0

            tr = pd.concat([
                high - low,
                (high - close.shift(1)).abs(),
                (low - close.shift(1)).abs()
            ], axis=1).max(axis=1)

            atr = tr.rolling(period).mean()
            plus_di = 100 * (plus_dm.rolling(period).mean() / atr)
            minus_di = 100 * (minus_dm.rolling(period).mean() / atr)

            dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
            adx = dx.rolling(period).mean()

            return float(adx.iloc[-1]) if not np.isnan(adx.iloc[-1]) else 0
        except Exception:
            return 0


class StrategyWeightOptimizer:
    """策略权重优化器"""

    def __init__(self, lookback: int = 60):
        self.lookback = lookback
        self.performance_history: Dict[str, List[float]] = {}

    def update_performance(self, strategy_name: str, return_value: float):
        """更新策略绩效"""
        if strategy_name not in self.performance_history:
            self.performance_history[strategy_name] = []
        self.performance_history[strategy_name].append(return_value)

        if len(self.performance_history[strategy_name]) > self.lookback:
            self.performance_history[strategy_name] = self.performance_history[strategy_name][-self.lookback:]

    def calculate_weights(self, strategies: List[str],
                          method: str = "sharpe") -> Dict[str, float]:
        """计算策略权重"""
        if not strategies:
            return {}

        if method == "equal":
            return {s: 1.0 / len(strategies) for s in strategies}

        weights = {}
        for strategy in strategies:
            if strategy in self.performance_history and len(self.performance_history[strategy]) > 5:
                returns = np.array(self.performance_history[strategy])

                if method == "sharpe":
                    rf = 0.03 / 252
                    excess = returns - rf
                    score = np.mean(excess) / (np.std(excess) + 1e-6)
                elif method == "sortino":
                    rf = 0.03 / 252
                    excess = returns - rf
                    downside = returns[returns < 0]
                    downside_std = np.std(downside) if len(downside) > 0 else 1e-6
                    score = np.mean(excess) / downside_std
                elif method == "calmar":
                    cumulative = np.cumsum(returns)
                    peak = np.maximum.accumulate(cumulative)
                    drawdown = peak - cumulative
                    max_dd = np.max(drawdown) if len(drawdown) > 0 else 1e-6
                    score = np.mean(returns) / max_dd
                else:
                    score = np.mean(returns)

                weights[strategy] = max(0, score)
            else:
                weights[strategy] = 1.0

        total = sum(weights.values())
        if total > 0:
            weights = {k: v / total for k, v in weights.items()}
        else:
            weights = {s: 1.0 / len(strategies) for s in strategies}

        return weights

    def get_regime_weights(self, strategies: List[str],
                           regime: MarketRegime) -> Dict[str, float]:
        """根据市场状态调整权重"""
        base_weights = self.calculate_weights(strategies)

        regime_adjustments = {
            MarketRegime.TREND_UP: {
                "ma_breakout": 1.5,
                "macd_cross": 1.3,
                "double_ma": 1.4,
                "obv_trend": 1.2,
                "rsi_oversold": 0.7,
                "kdj_cross": 0.8,
            },
            MarketRegime.TREND_DOWN: {
                "ma_breakout": 0.6,
                "macd_cross": 0.8,
                "rsi_oversold": 1.3,
                "kdj_cross": 1.2,
                "support_bounce": 1.1,
            },
            MarketRegime.RANGE: {
                "boll_squeeze": 1.4,
                "rsi_oversold": 1.3,
                "kdj_cross": 1.2,
                "vol_price_divergence": 1.1,
                "ma_breakout": 0.7,
            },
            MarketRegime.VOLATILE: {
                "boll_squeeze": 1.2,
                "vol_price_divergence": 1.3,
                "support_bounce": 1.1,
                "ma_breakout": 0.6,
                "macd_cross": 0.8,
            }
        }

        adjustments = regime_adjustments.get(regime, {})
        adjusted = {}
        for strategy in strategies:
            base = base_weights.get(strategy, 1.0 / len(strategies))
            multiplier = adjustments.get(strategy, 1.0)
            adjusted[strategy] = base * multiplier

        total = sum(adjusted.values())
        if total > 0:
            adjusted = {k: v / total for k, v in adjusted.items()}

        return adjusted


class EnsembleStrategyEngine:
    """集成策略引擎"""

    def __init__(self, strategies: List[Any] = None):
        from .strategies import get_all_strategies
        self.strategies = strategies or get_all_strategies()
        self.regime_detector = MarketRegimeDetector()
        self.weight_optimizer = StrategyWeightOptimizer()
        self.strategy_names = [s.name for s in self.strategies]

    def evaluate(self, df: pd.DataFrame,
                 min_consensus: float = 0.3) -> Optional[EnsembleSignal]:
        """评估所有策略并生成集成信号"""
        regime = self.regime_detector.detect(df)
        weights = self.weight_optimizer.get_regime_weights(self.strategy_names, regime)

        signals = []
        for strategy in self.strategies:
            try:
                signal = strategy.evaluate(df)
                if signal:
                    weight = weights.get(strategy.name, 0.1)
                    signals.append(StrategySignal(
                        strategy_name=strategy.name,
                        direction=signal.direction,
                        confidence=signal.confidence,
                        weight=weight,
                        regime=regime,
                        metadata=signal.metadata or {}
                    ))
            except Exception as e:
                logger.debug(f"策略 {strategy.name} 评估失败: {e}")

        if not signals:
            return None

        buy_score = sum(s.confidence * s.weight for s in signals if s.direction == "BUY")
        sell_score = sum(s.confidence * s.weight for s in signals if s.direction == "SELL")

        buy_count = sum(1 for s in signals if s.direction == "BUY")
        sell_count = sum(1 for s in signals if s.direction == "SELL")

        total_weight = sum(s.weight for s in signals)
        consensus = max(buy_score, sell_score) / total_weight if total_weight > 0 else 0

        if consensus < min_consensus:
            return None

        if buy_score > sell_score:
            direction = "BUY"
            confidence = buy_score / total_weight if total_weight > 0 else 0
            agreed = buy_count
        else:
            direction = "SELL"
            confidence = sell_score / total_weight if total_weight > 0 else 0
            agreed = sell_count

        return EnsembleSignal(
            direction=direction,
            confidence=min(confidence, 0.95),
            consensus_score=consensus,
            strategies_agreed=agreed,
            total_strategies=len(signals),
            regime=regime,
            details=signals
        )

    def update_performance(self, strategy_name: str, return_value: float):
        """更新策略绩效"""
        self.weight_optimizer.update_performance(strategy_name, return_value)

    def get_strategy_rankings(self) -> Dict[str, float]:
        """获取策略排名"""
        rankings = {}
        for strategy in self.strategies:
            weights = self.weight_optimizer.calculate_weights([strategy.name])
            rankings[strategy.name] = weights.get(strategy.name, 0)
        return dict(sorted(rankings.items(), key=lambda x: x[1], reverse=True))


class AdaptiveStrategySelector:
    """自适应策略选择器"""

    def __init__(self):
        self.regime_strategies: Dict[MarketRegime, List[str]] = {
            MarketRegime.TREND_UP: ["ma_breakout", "macd_cross", "double_ma", "obv_trend"],
            MarketRegime.TREND_DOWN: ["rsi_oversold", "kdj_cross", "support_bounce"],
            MarketRegime.RANGE: ["boll_squeeze", "rsi_oversold", "kdj_cross", "vol_price_divergence"],
            MarketRegime.VOLATILE: ["boll_squeeze", "vol_price_divergence", "support_bounce"],
        }
        self.performance_history: Dict[str, Dict[MarketRegime, List[float]]] = {}

    def select_strategies(self, regime: MarketRegime,
                          available_strategies: List[str]) -> List[str]:
        """根据市场状态选择策略"""
        preferred = self.regime_strategies.get(regime, [])
        selected = [s for s in preferred if s in available_strategies]

        if not selected:
            selected = available_strategies[:3]

        return selected

    def update_performance(self, strategy_name: str, regime: MarketRegime,
                           return_value: float):
        """更新策略绩效"""
        if strategy_name not in self.performance_history:
            self.performance_history[strategy_name] = {}
        if regime not in self.performance_history[strategy_name]:
            self.performance_history[strategy_name][regime] = []

        self.performance_history[strategy_name][regime].append(return_value)

        if len(self.performance_history[strategy_name][regime]) > 100:
            self.performance_history[strategy_name][regime] = \
                self.performance_history[strategy_name][regime][-100:]

    def get_best_strategies(self, regime: MarketRegime,
                            top_n: int = 3) -> List[Tuple[str, float]]:
        """获取当前市场状态下表现最好的策略"""
        strategy_scores = {}

        for strategy_name, regime_perf in self.performance_history.items():
            if regime in regime_perf and len(regime_perf[regime]) >= 5:
                returns = np.array(regime_perf[regime])
                sharpe = np.mean(returns) / (np.std(returns) + 1e-6)
                strategy_scores[strategy_name] = sharpe

        sorted_strategies = sorted(strategy_scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_strategies[:top_n]


class StrategyCombinationOptimizer:
    """策略组合优化器"""

    def __init__(self, max_strategies: int = 5):
        self.max_strategies = max_strategies

    def optimize_combination(self, strategy_signals: Dict[str, StrategySignal],
                             df: pd.DataFrame) -> List[str]:
        """优化策略组合"""
        if len(strategy_signals) <= self.max_strategies:
            return list(strategy_signals.keys())

        scored = []
        for name, signal in strategy_signals.items():
            score = self._calculate_strategy_score(signal, df)
            scored.append((name, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        return [name for name, _ in scored[:self.max_strategies]]

    def _calculate_strategy_score(self, signal: StrategySignal,
                                  df: pd.DataFrame) -> float:
        """计算策略得分"""
        score = signal.confidence * signal.weight

        if signal.direction == "BUY":
            close = df["close"].astype(float)
            if len(close) >= 5:
                recent_return = (close.iloc[-1] - close.iloc[-5]) / close.iloc[-5]
                if recent_return < 0:
                    score *= 1.2

        return score

    def calculate_dynamic_weights(self, signals: List[StrategySignal],
                                  regime: MarketRegime) -> Dict[str, float]:
        """计算动态权重"""
        weights = {}

        for signal in signals:
            base_weight = signal.confidence * signal.weight

            regime_multiplier = self._get_regime_multiplier(signal.strategy_name, regime)
            adjusted_weight = base_weight * regime_multiplier

            weights[signal.strategy_name] = adjusted_weight

        total = sum(weights.values())
        if total > 0:
            weights = {k: v / total for k, v in weights.items()}

        return weights

    def _get_regime_multiplier(self, strategy_name: str,
                               regime: MarketRegime) -> float:
        """获取市场状态乘数"""
        multipliers = {
            MarketRegime.TREND_UP: {
                "ma_breakout": 1.5, "macd_cross": 1.3, "double_ma": 1.4,
                "rsi_oversold": 0.7, "boll_squeeze": 0.8,
            },
            MarketRegime.TREND_DOWN: {
                "rsi_oversold": 1.3, "kdj_cross": 1.2, "support_bounce": 1.1,
                "ma_breakout": 0.6, "macd_cross": 0.8,
            },
            MarketRegime.RANGE: {
                "boll_squeeze": 1.4, "rsi_oversold": 1.2, "kdj_cross": 1.1,
                "vol_price_divergence": 1.1, "ma_breakout": 0.7,
            },
            MarketRegime.VOLATILE: {
                "boll_squeeze": 1.2, "vol_price_divergence": 1.3,
                "support_bounce": 1.1, "ma_breakout": 0.6,
            }
        }

        regime_map = multipliers.get(regime, {})
        return regime_map.get(strategy_name, 1.0)
