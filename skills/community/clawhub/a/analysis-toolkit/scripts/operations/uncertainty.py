"""
不确定度偏倚计算算子 — 测量不确定度评定（GUM 法 / JJF 1059.1）

包含因子对照：
  ┌─────────────┬──────┬──────────────────┐
  │ 分布类型     │  k   │ 适用场景          │
  ├─────────────┼──────┼──────────────────┤
  │ 正态分布     │  2   │ A类评定，大自由度  │
  │ 矩形分布     │ √3   │ B类评定，均匀分布  │
  │ 三角分布     │ √6   │ B类评定，三角分布  │
  │ U形分布      │ √2   │ B类评定，正弦分布  │
  │ t分布        │ t(df)│ A类评定，小自由度  │
  └─────────────┴──────┴──────────────────┘
"""
import numpy as np
import math
from typing import Union, List


# ═══════════════════════════════════════════════════════
# 包含因子
# ═══════════════════════════════════════════════════════

DISTRIBUTION_FACTORS = {
    "normal": 2.0,          # 正态分布（95%置信概率）
    "rectangular": math.sqrt(3),   # 矩形/均匀分布
    "triangular": math.sqrt(6),    # 三角分布
    "u_shape": math.sqrt(2),       # U形分布（正弦分布）
    "arcsine": math.sqrt(2),       # 反正弦分布（同U形）
}


def get_coverage_factor(distribution: str = "normal") -> float:
    """
    获取指定分布类型的包含因子 k。

    Parameters
    ----------
    distribution : str — 分布类型
        "normal" | "rectangular" | "triangular" | "u_shape" | "arcsine"

    Returns
    -------
    float — 包含因子 k
    """
    factor = DISTRIBUTION_FACTORS.get(distribution)
    if factor is None:
        raise ValueError(
            f"不支持的分布类型: '{distribution}'。"
            f"可用: {', '.join(DISTRIBUTION_FACTORS.keys())}"
        )
    return factor


def list_distribution_factors() -> dict:
    """列出所有分布类型及其包含因子。"""
    return dict(DISTRIBUTION_FACTORS)


# ═══════════════════════════════════════════════════════
# 偏倚不确定度
# ═══════════════════════════════════════════════════════

def calc_ubias(bias: float, k: float = 2.0) -> float:
    """
    偏倚引入的标准不确定度。
    u(bias) = |bias| / k

    Parameters
    ----------
    bias : float — 偏倚值
    k : float — 包含因子，默认 2（正态分布95%置信）

    Returns
    -------
    float — 标准不确定度
    """
    if k <= 0:
        raise ValueError("包含因子 k 必须大于 0")
    return abs(bias) / k


def calc_ubias_by_distribution(
        bias: float, distribution: str = "normal") -> float:
    """
    根据分布类型自动选择包含因子计算偏倚不确定度。

    Parameters
    ----------
    bias : float — 偏倚值
    distribution : str — 分布类型

    Returns
    -------
    float
    """
    k = get_coverage_factor(distribution)
    return calc_ubias(bias, k)


# ═══════════════════════════════════════════════════════
# A 类标准不确定度
# ═══════════════════════════════════════════════════════

def calc_ua(values: Union[List[float], np.ndarray]) -> float:
    """
    A 类标准不确定度 = SD / sqrt(n)
    对同一被测量做 n 次独立重复观测。
    """
    arr = np.array(values, dtype=float)
    n = len(arr)
    if n < 2:
        raise ValueError(f"A类评定需要至少2个数据点 (n={n})")
    sd = np.std(arr, ddof=1)
    return float(sd / np.sqrt(n))


# ═══════════════════════════════════════════════════════
# 合成不确定度
# ═══════════════════════════════════════════════════════

def calc_u_combined(components: Union[List[float], np.ndarray]) -> float:
    """
    合成标准不确定度 u_c = sqrt(Σ u_i²)
    各分量互不相关时适用。

    Parameters
    ----------
    components : list[float] — 各分量标准不确定度列表

    Returns
    -------
    float
    """
    comp = np.array(components, dtype=float)
    return float(np.sqrt(np.sum(comp ** 2)))


def calc_u_combined_weighted(
        components: List[dict]) -> float:
    """
    合成不确定度（加权敏感系数版）。
    当每个分量有自己的灵敏系数时使用。

    Parameters
    ----------
    components : list[dict]
        每个元素 {"u": float, "c": float}，c 为灵敏系数
        u_c = sqrt(Σ (c_i × u_i)²)

    Returns
    -------
    float
    """
    weighted = sum((c["c"] * c["u"]) ** 2 for c in components)
    return float(np.sqrt(weighted))


# ═══════════════════════════════════════════════════════
# 扩展不确定度
# ═══════════════════════════════════════════════════════

def calc_expanded_u(uc: float, k: float = 2.0) -> float:
    """
    扩展不确定度 U = k × u_c

    Parameters
    ----------
    uc : float — 合成标准不确定度
    k : float — 包含因子，默认 2（95%置信概率）

    Returns
    -------
    float
    """
    return uc * k


def calc_expanded_u_by_distribution(
        uc: float, distribution: str = "normal") -> float:
    """根据分布类型计算扩展不确定度。"""
    k = get_coverage_factor(distribution)
    return calc_expanded_u(uc, k)


# ═══════════════════════════════════════════════════════
# B 类评定
# ═══════════════════════════════════════════════════════

def calc_ub_type_b(half_width: float, distribution: str = "rectangular") -> float:
    """
    B 类标准不确定度评定。
    根据半宽信息和分布类型计算。

    Parameters
    ----------
    half_width : float — 区间半宽度（允差、最大允许误差等）
    distribution : str — 分布类型假设

    Returns
    -------
    float
    """
    k = get_coverage_factor(distribution)
    return half_width / k


# ═══════════════════════════════════════════════════════
# 相对不确定度
# ═══════════════════════════════════════════════════════

def calc_u_relative(u: float, value: float) -> float:
    """
    相对标准不确定度 = u / |value|
    """
    if value == 0:
        raise ValueError("不能计算相对不确定度: value = 0")
    return u / abs(value)


__all__ = [
    # 包含因子
    "get_coverage_factor", "list_distribution_factors",
    # 偏倚不确定度
    "calc_ubias", "calc_ubias_by_distribution",
    # A 类
    "calc_ua",
    # 合成
    "calc_u_combined", "calc_u_combined_weighted",
    # 扩展
    "calc_expanded_u", "calc_expanded_u_by_distribution",
    # B 类
    "calc_ub_type_b",
    # 相对
    "calc_u_relative",
]
