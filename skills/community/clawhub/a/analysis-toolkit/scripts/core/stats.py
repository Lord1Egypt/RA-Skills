"""
基础统计方法模块

重构说明（v2）：
  细粒度算子已拆分到 scripts/operations/ 下。
  本模块保留高层聚合函数，内部调用 operations 层的原子算子。
"""
import numpy as np
from scripts.operations.operators import (
    calc_mean, calc_median, calc_sd, calc_rsd, calc_min, calc_max,
    calc_count, calc_pooled_sd, calc_pooled_rsd, calc_robust_sd,
)


def calc_precision_stats(values):
    """
    精密度统计：SD, RSD, 平均值, 中位数。

    内部使用 operations 层的细粒度算子。
    """
    arr = np.array(values, dtype=float)
    n = len(arr)
    if n < 2:
        raise ValueError(f"数据点不足 (n={n})，至少需要2个数据点计算标准差")
    if np.any(np.isnan(arr)):
        raise ValueError("数据包含 NaN")

    try:
        mean = calc_mean(arr)
        sd = calc_sd(arr)
    except (ZeroDivisionError, FloatingPointError) as e:
        raise ValueError(f"精密度计算失败: {e}")

    return {
        "mean": mean,
        "median": calc_median(arr),
        "sd": sd,
        "rsd": calc_rsd(arr),
        "count": calc_count(arr),
        "min": calc_min(arr),
        "max": calc_max(arr),
    }


def calc_synthetic_std(groups, method="standard"):
    """
    合成标准差。

    内部使用 operations 层的 calc_pooled_sd 算子。

    Parameters
    ----------
    groups : list of array-like
        每个组的数值列表
    method : str
        "standard" — 正规算法（加权合并）
        "simple" — 简单算法（SQRT((SD1²+SD2²+...+SDk²)/k)）

    Returns
    -------
    dict
        {"synthetic_std", "synthetic_rsd", "overall_mean", "group_stats"}
    """
    if not groups or all(len(g) < 2 for g in groups):
        raise ValueError("各组数据不足，至少有一组需要 ≥2 个数据点")

    try:
        group_stats = []
        total_n = 0
        weighted_sum = 0
        sd_squares = 0
        k = len(groups)

        for g in groups:
            arr = np.array(g, dtype=float)
            n = len(arr)
            mean = calc_mean(arr)
            sd = calc_sd(arr)

            group_stats.append({"n": n, "mean": mean, "sd": sd})
            total_n += n
            weighted_sum += mean * n
            sd_squares += sd ** 2

        if method == "simple":
            synthetic_std = np.sqrt(sd_squares / k) if k > 0 else 0
        else:
            synthetic_std = calc_pooled_sd(groups)

        overall_mean = weighted_sum / total_n if total_n > 0 else 0

        return {
            "synthetic_std": synthetic_std,
            "synthetic_rsd": synthetic_std / overall_mean * 100 if overall_mean != 0 else 0,
            "overall_mean": overall_mean,
            "group_count": k,
            "total_n": total_n,
            "method": method,
            "group_stats": group_stats,
        }
    except (ZeroDivisionError, FloatingPointError) as e:
        raise ValueError(f"合成标准差计算失败: {e}")


def calc_precision(values):
    """calc_precision_stats 的简写别名。"""
    return calc_precision_stats(values)
