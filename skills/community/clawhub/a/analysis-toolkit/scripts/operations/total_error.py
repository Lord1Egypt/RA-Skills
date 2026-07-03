"""
总误差计算算子 — 临床检验/质量控制领域的 Total Error 评估

公式：TE = Bias + t(α, df) × SD

其中：
  - Bias = |mean - reference|（偏倚绝对值）
  - t(α, df) = 给定置信水平和自由度下的 t 临界值
  - SD = 样本标准偏差

总误差衡量测量结果的准确度，是方法性能评价的核心指标。
"""
import numpy as np
from typing import Union, List, Optional
from scripts.operations.operators import calc_mean, calc_sd, calc_bias
from scripts.operations.operators import calc_ci_mean


# ═══════════════════════════════════════════════════════
# 核心函数
# ═══════════════════════════════════════════════════════

def calc_te(mean: float, reference: float, sd: float, df: int,
            t_crit: float) -> float:
    """
    总误差计算（核心公式）。

    TE = |mean - reference| + t_crit × sd

    Parameters
    ----------
    mean : float — 样本均值
    reference : float — 参考值/指定值/真值
    sd : float — 样本标准偏差
    df : int — 自由度（决定 t 临界值查表）
    t_crit : float — t 临界值（由 df 和置信水平查表获得）

    Returns
    -------
    float — 总误差
    """
    bias = calc_bias(mean, reference)
    return abs(bias) + t_crit * sd


def calc_te_relative(mean: float, reference: float, sd: float,
                     df: int, t_crit: float) -> float:
    """
    相对总误差(%) = TE / reference × 100

    Parameters 同 calc_te
    """
    te = calc_te(mean, reference, sd, df, t_crit)
    if reference == 0:
        return 0.0
    return te / abs(reference) * 100


def calc_te_from_values(values: Union[List[float], np.ndarray],
                         reference: float, t_crit: float) -> dict:
    """
    从原始数据直接计算总误差及所有分量。

    Parameters
    ----------
    values : array-like — 测量值列表
    reference : float — 参考值
    t_crit : float — t 临界值

    Returns
    -------
    dict
        {
            "te": 总误差,
            "te_relative": 相对总误差(%),
            "bias": 偏倚,
            "bias_abs": 偏倚绝对值,
            "mean": 均值,
            "sd": 标准偏差,
            "n": 样本量,
            "df": 自由度,
            "t_crit": t 临界值,
            "random_error": t_crit × sd,
            "reference": 参考值,
            "formula": "TE = |mean-ref| + t_crit × SD",
            "expression": "TE = |{mean} - {ref}| + {t_crit} × {sd} = {te}"
        }
    """
    arr = np.array(values, dtype=float)
    n = len(arr)
    if n < 2:
        raise ValueError(f"数据点不足 (n={n})，至少需要2个数据点")
    mean = calc_mean(arr)
    sd_val = calc_sd(arr)
    df = n - 1
    bias_val = calc_bias(mean, reference)
    random_error = t_crit * sd_val
    te_value = abs(bias_val) + random_error
    te_rel = te_value / abs(reference) * 100 if reference != 0 else 0.0

    return {
        "te": te_value,
        "te_relative": te_rel,
        "bias": bias_val,
        "bias_abs": abs(bias_val),
        "mean": mean,
        "sd": sd_val,
        "n": n,
        "df": df,
        "t_crit": t_crit,
        "random_error": random_error,
        "reference": reference,
        "formula": "TE = |mean - reference| + t_crit × SD",
        "expression": (
            f"TE = |{mean:.4f} - {reference}| + {t_crit:.4f} × {sd_val:.4f} = {te_value:.4f}"
        ),
    }


def calc_te_with_components(values: Union[List[float], np.ndarray],
                             reference: float, t_crit: float) -> dict:
    """calc_te_from_values 的完整别名，包含分量分解。"""
    return calc_te_from_values(values, reference, t_crit)


# ═══════════════════════════════════════════════════════
# 总误差判定
# ═══════════════════════════════════════════════════════

def calc_te_judgment(te_relative: float, te_allowable: float) -> dict:
    """
    总误差判定（CLIA'88 / RiliBÄK 等常用准则）。

    ┌─────────────────┬────────────────────────┐
    │ TE% / TEa%      │ 判定                    │
    ├─────────────────┼────────────────────────┤
    │ ≤ 1/3 TEa%      │ 优秀 (excellent)        │
    │ ≤ 2/3 TEa%      │ 良好 (good)             │
    │ ≤ TEa%          │ 可接受 (acceptable)      │
    │ > TEa%          │ 不可接受 (unacceptable)  │
    └─────────────────┴────────────────────────┘

    Parameters
    ----------
    te_relative : float — 相对总误差(%)
    te_allowable : float — 允许总误差 TEa(%)

    Returns
    -------
    dict — {"level": str, "acceptable": bool, "ratio": float}
    """
    ratio = te_relative / te_allowable if te_allowable > 0 else float('inf')

    if ratio <= 1 / 3:
        level = "excellent"
        acceptable = True
    elif ratio <= 2 / 3:
        level = "good"
        acceptable = True
    elif ratio <= 1.0:
        level = "acceptable"
        acceptable = True
    else:
        level = "unacceptable"
        acceptable = False

    return {
        "level": level,
        "acceptable": acceptable,
        "ratio": ratio,
        "te_relative": te_relative,
        "te_allowable": te_allowable,
        "summary": (
            f"TE% = {te_relative:.2f}%, TEa% = {te_allowable:.2f}%, "
            f"ratio = {ratio:.2f}, 判定: {level}"
        ),
    }


__all__ = [
    "calc_te", "calc_te_relative",
    "calc_te_from_values", "calc_te_with_components",
    "calc_te_judgment",
]
