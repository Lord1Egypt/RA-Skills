"""因子基类 - 注册表模式，统一接口"""
from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Type

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


@dataclass
class FactorValue:
    """单只股票的因子值"""
    code: str
    factor_name: str
    value: float
    z_score: float = 0.0
    percentile: float = 0.0
    weight: float = 1.0


@dataclass
class FactorResult:
    """因子计算结果"""
    name: str
    category: str  # fundamental / capital / technical / sentiment
    description: str
    values: Dict[str, float]  # code -> value
    ic: float = 0.0           # Information Coefficient
    ic_ir: float = 0.0        # IC Information Ratio
    turnover: float = 0.0     # 因子换手率

    def to_rank(self) -> Dict[str, float]:
        """转换为排名百分位"""
        if not self.values:
            return {}
        codes = list(self.values.keys())
        vals = np.array(list(self.values.values()))
        ranks = pd.Series(vals).rank(pct=True).values
        return dict(zip(codes, ranks))


# ===================== 因子注册表 =====================

_FACTOR_REGISTRY: Dict[str, Type["Factor"]] = {}


def register_factor(cls: Type["Factor"]) -> Type["Factor"]:
    _FACTOR_REGISTRY[cls.name] = cls
    return cls


def get_all_factors() -> List["Factor"]:
    return [cls() for cls in _FACTOR_REGISTRY.values()]


def get_factors_by_category(category: str) -> List["Factor"]:
    return [cls() for cls in _FACTOR_REGISTRY.values() if cls.category == category]


def get_factor(name: str) -> Optional["Factor"]:
    cls = _FACTOR_REGISTRY.get(name)
    return cls() if cls else None


# ===================== 因子基类 =====================

class Factor(ABC):
    """因子基类"""

    name: str = "base"
    category: str = "unknown"
    description: str = ""

    @abstractmethod
    def compute(self, df: pd.DataFrame, **kwargs) -> Optional[float]:
        """计算单只股票的因子值

        Args:
            df: K线数据（已含技术指标）
            kwargs: 额外数据（基本面、资金面等）

        Returns:
            因子值或 None
        """
        ...

    def compute_batch(self, data: Dict[str, pd.DataFrame], **kwargs) -> FactorResult:
        """批量计算因子"""
        values = {}
        for code, df in data.items():
            try:
                val = self.compute(df, **kwargs)
                if val is not None and np.isfinite(val):
                    values[code] = val
            except Exception as e:
                logger.debug(f"因子 {self.name} 计算 {code} 失败: {e}")

        return FactorResult(
            name=self.name,
            category=self.category,
            description=self.description,
            values=values,
        )


# ===================== 因子合成引擎 =====================

class FactorCombiner:
    """多因子合成"""

    @staticmethod
    def equal_weight(factors: List[FactorResult]) -> Dict[str, float]:
        """等权合成"""
        if not factors:
            return {}

        all_codes = set()
        for f in factors:
            all_codes.update(f.values.keys())

        scores = {}
        for code in all_codes:
            vals = []
            for f in factors:
                ranks = f.to_rank()
                if code in ranks:
                    vals.append(ranks[code])
            scores[code] = np.mean(vals) if vals else 0.0

        return scores

    @staticmethod
    def ic_weight(factors: List[FactorResult], ic_data: Dict[str, float]) -> Dict[str, float]:
        """IC 加权合成"""
        if not factors:
            return {}

        # 归一化 IC 权重
        total_ic = sum(abs(ic_data.get(f.name, 0)) for f in factors)
        if total_ic == 0:
            return FactorCombiner.equal_weight(factors)

        weights = {f.name: abs(ic_data.get(f.name, 0)) / total_ic for f in factors}

        all_codes = set()
        for f in factors:
            all_codes.update(f.values.keys())

        scores = {}
        for code in all_codes:
            weighted_sum = 0.0
            weight_sum = 0.0
            for f in factors:
                ranks = f.to_rank()
                if code in ranks:
                    w = weights.get(f.name, 0)
                    weighted_sum += ranks[code] * w
                    weight_sum += w
            scores[code] = weighted_sum / weight_sum if weight_sum > 0 else 0.0

        return scores

    @staticmethod
    def maximize_ic_ir(
        factors: List[FactorResult],
        returns: Dict[str, float],
    ) -> Dict[str, float]:
        """最大化 IC_IR 合成（二次规划优化权重）

        通过求解优化问题：max w'*IC / sqrt(w'*Cov*w)
        其中 IC 为各因子的截面IC，Cov为因子IC的协方差矩阵
        """
        if len(factors) < 2:
            return FactorCombiner.equal_weight(factors)

        all_codes = set()
        for f in factors:
            all_codes.update(f.values.keys())
        if len(all_codes) < 3:
            return FactorCombiner.equal_weight(factors)

        code_list = sorted(all_codes)
        ret_arr = np.array([returns.get(c, 0) for c in code_list])

        factor_ranks = []
        for f in factors:
            ranks = f.to_rank()
            factor_ranks.append([ranks.get(c, 0.5) for c in code_list])
        rank_matrix = np.array(factor_ranks)
        n_factors = len(factors)

        ic_values = []
        for i in range(n_factors):
            if np.std(rank_matrix[i]) > 0 and np.std(ret_arr) > 0:
                corr = np.corrcoef(rank_matrix[i], ret_arr)[0, 1]
                ic_values.append(corr if np.isfinite(corr) else 0)
            else:
                ic_values.append(0)
        ic_vec = np.array(ic_values)

        if np.all(ic_vec == 0):
            return FactorCombiner.equal_weight(factors)

        cov_matrix = np.cov(rank_matrix)
        if cov_matrix.ndim == 1:
            cov_matrix = cov_matrix.reshape(1, 1)

        try:
            from scipy.optimize import minimize

            def neg_ic_ir(w):
                port_ic = np.dot(w, ic_vec)
                port_var = np.dot(w, np.dot(cov_matrix, w))
                port_std = np.sqrt(max(port_var, 1e-10))
                return -port_ic / port_std

            constraints = {"type": "eq", "fun": lambda w: np.sum(w) - 1}
            bounds = [(0, 1)] * n_factors
            w0 = np.ones(n_factors) / n_factors

            result = minimize(
                neg_ic_ir, w0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
            )
            if result.success:
                opt_weights = np.abs(result.x)
                total = np.sum(opt_weights)
                if total > 0:
                    opt_weights = opt_weights / total
                else:
                    opt_weights = np.ones(n_factors) / n_factors
            else:
                opt_weights = np.abs(ic_vec)
                total = np.sum(opt_weights)
                opt_weights = opt_weights / total if total > 0 else np.ones(n_factors) / n_factors
        except ImportError:
            opt_weights = np.abs(ic_vec)
            total = np.sum(opt_weights)
            opt_weights = opt_weights / total if total > 0 else np.ones(n_factors) / n_factors

        scores = {}
        for idx, code in enumerate(code_list):
            score = sum(opt_weights[i] * factor_ranks[i][idx] for i in range(n_factors))
            scores[code] = float(score)

        for f in factors:
            f.ic = ic_values[factors.index(f)] if factors.index(f) < len(ic_values) else 0

        return scores
