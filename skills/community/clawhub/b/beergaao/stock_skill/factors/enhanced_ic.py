"""增强因子分析 - 滚动IC、IC衰减、因子收益归因"""
from __future__ import annotations
import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


@dataclass
class FactorICResult:
    """因子IC分析结果"""
    factor_name: str
    ic_mean: float
    ic_std: float
    ic_ir: float
    ic_series: pd.Series = None
    rolling_ic: pd.Series = None
    ic_decay: List[float] = field(default_factory=list)
    turnover: float = 0.0
    t_stat: float = 0.0
    p_value: float = 0.0

    def summary(self) -> str:
        significance = "***" if abs(self.t_stat) > 2.58 else "**" if abs(self.t_stat) > 1.96 else "*" if abs(self.t_stat) > 1.65 else ""
        return (
            f"{self.factor_name}: IC={self.ic_mean:.4f}±{self.ic_std:.4f}, "
            f"ICIR={self.ic_ir:.2f}, t={self.t_stat:.2f}{significance}, "
            f"Turnover={self.turnover:.2%}"
        )


@dataclass
class FactorDecayResult:
    """因子IC衰减分析"""
    factor_name: str
    decay_periods: List[int]
    decay_values: List[float]
    half_life: Optional[int] = None
    persistence: float = 0.0


class EnhancedFactorAnalyzer:
    """增强因子分析器"""

    def __init__(self, periods: List[int] = None):
        self.periods = periods or [1, 5, 10, 20]

    def calculate_ic(self, factor_values: pd.Series, forward_returns: pd.Series,
                     method: str = "rank") -> pd.Series:
        """计算IC序列"""
        aligned = pd.DataFrame({
            "factor": factor_values,
            "returns": forward_returns
        }).dropna()

        if len(aligned) < 10:
            return pd.Series(dtype=float)

        if method == "rank":
            ic = aligned["factor"].corr(aligned["returns"], method="spearman")
        else:
            ic = aligned["factor"].corr(aligned["returns"], method="pearson")

        return ic

    def calculate_rolling_ic(self, factor_values: pd.Series, forward_returns: pd.Series,
                             window: int = 60, method: str = "rank") -> pd.Series:
        """计算滚动IC"""
        aligned = pd.DataFrame({
            "factor": factor_values,
            "returns": forward_returns
        }).dropna()

        if len(aligned) < window:
            return pd.Series(dtype=float)

        rolling_ic = pd.Series(index=aligned.index, dtype=float)

        for i in range(window, len(aligned)):
            window_data = aligned.iloc[i - window:i]
            if method == "rank":
                ic = window_data["factor"].corr(window_data["returns"], method="spearman")
            else:
                ic = window_data["factor"].corr(window_data["returns"], method="pearson")
            rolling_ic.iloc[i] = ic

        return rolling_ic

    def calculate_ic_decay(self, factor_df: pd.DataFrame, returns_df: pd.DataFrame,
                           factor_name: str, max_lag: int = 20) -> FactorDecayResult:
        """计算IC衰减（因子预测能力随时间的衰减）"""
        decay_values = []
        decay_periods = list(range(1, max_lag + 1))

        close = returns_df["close"].astype(float)

        for lag in decay_periods:
            forward_returns = close.shift(-lag) / close - 1
            aligned = pd.DataFrame({
                "factor": factor_df[factor_name],
                "returns": forward_returns
            }).dropna()

            if len(aligned) >= 10:
                ic = aligned["factor"].corr(aligned["returns"], method="spearman")
                decay_values.append(ic if np.isfinite(ic) else 0)
            else:
                decay_values.append(0)

        half_life = None
        if decay_values and abs(decay_values[0]) > 0.01:
            initial_ic = abs(decay_values[0])
            for i, ic in enumerate(decay_values):
                if abs(ic) < initial_ic / 2:
                    half_life = decay_periods[i]
                    break

        persistence = 0.0
        if decay_values:
            positive_count = sum(1 for ic in decay_values[:5] if ic * decay_values[0] > 0)
            persistence = positive_count / min(5, len(decay_values))

        return FactorDecayResult(
            factor_name=factor_name,
            decay_periods=decay_periods,
            decay_values=decay_values,
            half_life=half_life,
            persistence=persistence
        )

    def calculate_factor_turnover(self, factor_values: pd.Series,
                                  quantile_pct: float = 0.2) -> float:
        """计算因子换手率"""
        if len(factor_values) < 2:
            return 0.0

        n = len(factor_values)
        top_n = max(1, int(n * quantile_pct))

        turnovers = []
        for i in range(1, len(factor_values)):
            prev_top = set(factor_values.iloc[:i].nlargest(top_n).index)
            curr_top = set(factor_values.iloc[:i + 1].nlargest(top_n).index)

            if prev_top:
                overlap = len(prev_top & curr_top)
                turnover = 1 - overlap / len(prev_top)
                turnovers.append(turnover)

        return np.mean(turnovers) if turnovers else 0.0

    def analyze_factor(self, factor_values: pd.Series, price_df: pd.DataFrame,
                       factor_name: str, forward_period: int = 5,
                       rolling_window: int = 60) -> FactorICResult:
        """完整因子分析"""
        close = price_df["close"].astype(float)
        forward_returns = close.shift(-forward_period) / close - 1

        aligned = pd.DataFrame({
            "factor": factor_values,
            "returns": forward_returns
        }).dropna()

        if len(aligned) < 20:
            return FactorICResult(
                factor_name=factor_name,
                ic_mean=0, ic_std=0, ic_ir=0
            )

        ic_series = pd.Series(index=aligned.index, dtype=float)
        for i in range(60, len(aligned)):
            window = aligned.iloc[i - 60:i]
            ic = window["factor"].corr(window["returns"], method="spearman")
            ic_series.iloc[i] = ic

        ic_series = ic_series.dropna()

        if len(ic_series) == 0:
            return FactorICResult(
                factor_name=factor_name,
                ic_mean=0, ic_std=0, ic_ir=0
            )

        ic_mean = float(ic_series.mean())
        ic_std = float(ic_series.std())
        ic_ir = ic_mean / ic_std if ic_std > 0 else 0

        t_stat = ic_mean / (ic_std / np.sqrt(len(ic_series))) if ic_std > 0 else 0
        from scipy import stats
        p_value = 2 * (1 - stats.t.cdf(abs(t_stat), df=len(ic_series) - 1)) if len(ic_series) > 1 else 1.0

        rolling_ic = self.calculate_rolling_ic(
            factor_values, forward_returns, rolling_window
        )

        turnover = self.calculate_factor_turnover(factor_values)

        return FactorICResult(
            factor_name=factor_name,
            ic_mean=ic_mean,
            ic_std=ic_std,
            ic_ir=ic_ir,
            ic_series=ic_series,
            rolling_ic=rolling_ic,
            turnover=turnover,
            t_stat=t_stat,
            p_value=p_value
        )


class MultiFactorICAnalyzer:
    """多因子IC分析器"""

    def __init__(self):
        self.analyzer = EnhancedFactorAnalyzer()

    def analyze_all_factors(self, factor_data: Dict[str, pd.Series],
                            price_df: pd.DataFrame,
                            forward_period: int = 5) -> Dict[str, FactorICResult]:
        """分析所有因子"""
        results = {}

        for factor_name, factor_values in factor_data.items():
            try:
                result = self.analyzer.analyze_factor(
                    factor_values, price_df, factor_name, forward_period
                )
                results[factor_name] = result
                logger.info(result.summary())
            except Exception as e:
                logger.error(f"因子 {factor_name} 分析失败: {e}")

        return results

    def calculate_factor_correlation(self, factor_data: Dict[str, pd.Series]) -> pd.DataFrame:
        """计算因子间相关性"""
        factor_df = pd.DataFrame(factor_data)
        return factor_df.corr(method="spearman")

    def select_factors_by_ic(self, results: Dict[str, FactorICResult],
                             min_ic: float = 0.02,
                             min_icir: float = 0.3) -> List[str]:
        """根据IC筛选因子"""
        selected = []
        for name, result in results.items():
            if abs(result.ic_mean) >= min_ic and abs(result.ic_ir) >= min_icir:
                selected.append(name)
        return selected

    def calculate_ic_weighted_returns(self, factor_data: Dict[str, pd.Series],
                                      price_df: pd.DataFrame,
                                      forward_period: int = 5) -> pd.Series:
        """计算IC加权收益"""
        results = self.analyze_all_factors(factor_data, price_df, forward_period)

        weights = {}
        total_abs_ic = 0
        for name, result in results.items():
            abs_ic = abs(result.ic_mean)
            weights[name] = abs_ic
            total_abs_ic += abs_ic

        if total_abs_ic == 0:
            return pd.Series(0, index=price_df.index)

        for name in weights:
            weights[name] /= total_abs_ic

        close = price_df["close"].astype(float)
        forward_returns = close.shift(-forward_period) / close - 1

        weighted_returns = pd.Series(0, index=price_df.index, dtype=float)
        for name, weight in weights.items():
            if name in factor_data:
                factor = factor_data[name]
                aligned = pd.DataFrame({
                    "factor": factor,
                    "returns": forward_returns
                }).dropna()

                if len(aligned) > 0:
                    factor_returns = aligned["factor"] * aligned["returns"]
                    weighted_returns = weighted_returns.add(factor_returns * weight, fill_value=0)

        return weighted_returns


class FactorPerformanceTracker:
    """因子绩效跟踪器"""

    def __init__(self, lookback_periods: List[int] = None):
        self.lookback_periods = lookback_periods or [20, 60, 120]
        self.history: Dict[str, List[FactorICResult]] = {}

    def update(self, factor_name: str, result: FactorICResult):
        """更新因子绩效"""
        if factor_name not in self.history:
            self.history[factor_name] = []
        self.history[factor_name].append(result)

    def get_trend(self, factor_name: str) -> Dict[str, float]:
        """获取因子绩效趋势"""
        if factor_name not in self.history or len(self.history[factor_name]) < 2:
            return {"trend": 0, "stability": 0}

        recent = self.history[factor_name][-10:]
        ics = [r.ic_mean for r in recent]

        if len(ics) < 2:
            return {"trend": 0, "stability": 0}

        trend = ics[-1] - ics[0]
        stability = 1 - np.std(ics) / (abs(np.mean(ics)) + 1e-6)

        return {"trend": trend, "stability": stability}

    def detect_factor_decay(self, factor_name: str, threshold: float = 0.5) -> bool:
        """检测因子衰减"""
        if factor_name not in self.history or len(self.history[factor_name]) < 10:
            return False

        recent = self.history[factor_name][-20:]
        ics = [abs(r.ic_mean) for r in recent]

        if len(ics) < 10:
            return False

        first_half = np.mean(ics[:len(ics) // 2])
        second_half = np.mean(ics[len(ics) // 2:])

        if first_half > 0 and second_half / first_half < threshold:
            return True

        return False

    def get_factor_score(self, factor_name: str) -> float:
        """获取因子综合评分"""
        if factor_name not in self.history or not self.history[factor_name]:
            return 0.0

        latest = self.history[factor_name][-1]
        trend_info = self.get_trend(factor_name)

        score = 0.0
        score += min(abs(latest.ic_mean) * 10, 3)
        score += min(abs(latest.ic_ir) * 2, 3)
        score += min(trend_info["stability"] * 2, 2)
        score += 1 if not self.detect_factor_decay(factor_name) else 0
        score += min(abs(latest.t_stat) / 2, 2)

        return min(score, 10)
