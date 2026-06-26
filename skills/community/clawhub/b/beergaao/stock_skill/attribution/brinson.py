"""绩效归因 - Brinson 归因 + 因子暴露分析 + 基准对比"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import numpy as np

logger = logging.getLogger(__name__)


# ===================== Brinson 归因 =====================

@dataclass
class BrinsonAttribution:
    """Brinson 单期归因结果"""
    allocation_effect: float    # 配置效应
    selection_effect: float     # 选择效应
    interaction_effect: float   # 交互效应
    total_active_return: float  # 总主动收益

    def summary(self) -> str:
        return (
            f"配置效应: {self.allocation_effect:+.4f} | "
            f"选择效应: {self.selection_effect:+.4f} | "
            f"交互效应: {self.interaction_effect:+.4f} | "
            f"总主动收益: {self.total_active_return:+.4f}"
        )


@dataclass
class MultiPeriodBrinson:
    """多期 Brinson 归因"""
    periods: List[BrinsonAttribution]
    cumulative_allocation: float
    cumulative_selection: float
    cumulative_interaction: float
    cumulative_total: float

    def summary(self) -> str:
        return (
            f"累计配置效应: {self.cumulative_allocation:+.4f}\n"
            f"累计选择效应: {self.cumulative_selection:+.4f}\n"
            f"累计交互效应: {self.cumulative_interaction:+.4f}\n"
            f"累计总主动收益: {self.cumulative_total:+.4f}"
        )


class BrinsonModel:
    """Brinson 归因模型

    BHB 模型：
    - 配置效应 (AE): Σ(wp - wb) × (Rb_i - Rb)
    - 选择效应 (SE): Σ wb × (Rp_i - Rb_i)
    - 交互效应 (IE): Σ(wp - wb) × (Rp_i - Rb_i)
    """

    @staticmethod
    def single_period(
        portfolio_weights: Dict[str, float],
        benchmark_weights: Dict[str, float],
        portfolio_returns: Dict[str, float],
        benchmark_returns: Dict[str, float],
    ) -> BrinsonAttribution:
        """单期 Brinson 归因"""
        all_sectors = set(list(portfolio_weights.keys()) + list(benchmark_weights.keys()))

        # 基准总收益
        bm_total = sum(benchmark_weights.get(s, 0) * benchmark_returns.get(s, 0) for s in all_sectors)

        allocation = 0.0
        selection = 0.0
        interaction = 0.0

        for sector in all_sectors:
            wp = portfolio_weights.get(sector, 0)
            wb = benchmark_weights.get(sector, 0)
            rp = portfolio_returns.get(sector, 0)
            rb = benchmark_returns.get(sector, 0)

            allocation += (wp - wb) * (rb - bm_total)
            selection += wb * (rp - rb)
            interaction += (wp - wb) * (rp - rb)

        total = allocation + selection + interaction

        return BrinsonAttribution(
            allocation_effect=allocation,
            selection_effect=selection,
            interaction_effect=interaction,
            total_active_return=total,
        )

    @staticmethod
    def multi_period(
        period_data: List[Tuple[Dict, Dict, Dict, Dict]],
    ) -> MultiPeriodBrinson:
        """多期 Brinson 归因（链式分解）"""
        periods = []
        cum_alloc = 0.0
        cum_select = 0.0
        cum_interact = 0.0

        for pw, bw, pr, br in period_data:
            result = BrinsonModel.single_period(pw, bw, pr, br)
            periods.append(result)
            cum_alloc += result.allocation_effect
            cum_select += result.selection_effect
            cum_interact += result.interaction_effect

        return MultiPeriodBrinson(
            periods=periods,
            cumulative_allocation=cum_alloc,
            cumulative_selection=cum_select,
            cumulative_interaction=cum_interact,
            cumulative_total=cum_alloc + cum_select + cum_interact,
        )


# ===================== 因子暴露分析 =====================

@dataclass
class FactorExposure:
    """因子暴露分析结果"""
    factor_name: str
    portfolio_exposure: float    # 组合因子暴露
    benchmark_exposure: float    # 基准因子暴露
    active_exposure: float       # 主动暴露
    factor_return: float         # 因子收益率
    contribution: float          # 因子贡献

    def summary(self) -> str:
        return (
            f"{self.factor_name}: "
            f"组合={self.portfolio_exposure:.3f} | "
            f"基准={self.benchmark_exposure:.3f} | "
            f"主动={self.active_exposure:.3f} | "
            f"贡献={self.contribution:+.4f}"
        )


class FactorExposureAnalyzer:
    """因子暴露分析器"""

    @staticmethod
    def analyze(
        portfolio_weights: Dict[str, float],
        benchmark_weights: Dict[str, float],
        factor_values: Dict[str, Dict[str, float]],
    ) -> List[FactorExposure]:
        """分析因子暴露

        Args:
            portfolio_weights: {code: weight}
            benchmark_weights: {code: weight}
            factor_values: {factor_name: {code: value}}

        Returns:
            各因子的暴露分析
        """
        results = []

        for factor_name, values in factor_values.items():
            # 组合因子暴露 = Σ(wp × factor_value)
            port_exp = sum(
                portfolio_weights.get(c, 0) * values.get(c, 0)
                for c in portfolio_weights
            )

            # 基准因子暴露
            bm_exp = sum(
                benchmark_weights.get(c, 0) * values.get(c, 0)
                for c in benchmark_weights
            )

            active_exp = port_exp - bm_exp

            results.append(FactorExposure(
                factor_name=factor_name,
                portfolio_exposure=port_exp,
                benchmark_exposure=bm_exp,
                active_exposure=active_exp,
                factor_return=0,
                contribution=0,
            ))

        return results

    @staticmethod
    def factor_contribution(
        exposures: List[FactorExposure],
        factor_returns: Dict[str, float],
    ) -> List[FactorExposure]:
        """计算因子贡献"""
        for exp in exposures:
            fr = factor_returns.get(exp.factor_name, 0)
            exp.factor_return = fr
            exp.contribution = exp.active_exposure * fr
        return exposures


# ===================== 风险归因 =====================

@dataclass
class RiskAttribution:
    """风险归因"""
    total_risk: float
    systematic_risk: float
    specific_risk: float
    factor_risks: Dict[str, float]

    def summary(self) -> str:
        lines = [
            f"总风险: {self.total_risk:.4f}",
            f"系统性风险: {self.systematic_risk:.4f} ({self.systematic_risk/self.total_risk*100:.1f}%)",
            f"特异性风险: {self.specific_risk:.4f} ({self.specific_risk/self.total_risk*100:.1f}%)",
        ]
        for name, risk in sorted(self.factor_risks.items(), key=lambda x: -abs(x[1])):
            lines.append(f"  {name}: {risk:.4f}")
        return "\n".join(lines)


class RiskAttributionModel:
    """风险归因模型"""

    @staticmethod
    def decompose(
        portfolio_returns: np.ndarray,
        factor_returns: Dict[str, np.ndarray],
    ) -> RiskAttribution:
        """分解风险为系统性风险和特异性风险"""
        total_risk = float(np.var(portfolio_returns))

        if not factor_returns:
            return RiskAttribution(
                total_risk=total_risk,
                systematic_risk=0,
                specific_risk=total_risk,
                factor_risks={},
            )

        # 多因子回归
        factor_names = list(factor_returns.keys())
        X = np.column_stack([factor_returns[f] for f in factor_names])
        X = np.column_stack([np.ones(len(X)), X])  # 加截距

        y = portfolio_returns
        min_len = min(len(y), X.shape[0])
        y = y[:min_len]
        X = X[:min_len]

        try:
            betas = np.linalg.lstsq(X, y, rcond=None)[0]
            predicted = X @ betas
            residual = y - predicted

            systematic = float(np.var(predicted))
            specific = float(np.var(residual))

            factor_risks = {}
            for i, name in enumerate(factor_names):
                factor_risks[name] = float(betas[i + 1] ** 2 * np.var(X[:, i + 1]))

            return RiskAttribution(
                total_risk=total_risk,
                systematic_risk=systematic,
                specific_risk=specific,
                factor_risks=factor_risks,
            )
        except Exception as e:
            logger.warning(f"风险归因失败: {e}")
            return RiskAttribution(total_risk=total_risk, systematic_risk=0, specific_risk=total_risk, factor_risks={})
