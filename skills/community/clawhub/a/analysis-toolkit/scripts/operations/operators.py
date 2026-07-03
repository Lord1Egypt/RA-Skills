"""
细粒度算子层 — 原子级统计计算函数

每个函数做且只做一件事，参数签名明确，可单独导入使用。
上层场景函数（scenarios/）和模板（pipeline/）均组合这些算子。
"""
import numpy as np
from typing import Union, List


# 空值守卫 — 提升基础算子的错误信息可读性
def _check_non_empty(values, func_name="该算子"):
    """检查输入序列是否为空，为空时抛出清晰异常。"""
    if len(values) == 0:
        raise ValueError(
            f"{func_name}: 输入数据为空列表（length=0），无法计算。\n"
            f"建议：检查传递给该函数的数据源，确认 DataFrame 包含有效行且列名正确。"
        )


# ═══════════════════════════════════════════════════════
# 基础描述统计
# ═══════════════════════════════════════════════════════

def calc_mean(values: Union[List[float], np.ndarray]) -> float:
    """算术均值。"""
    _check_non_empty(values, "calc_mean")
    return float(np.mean(values))


def calc_median(values: Union[List[float], np.ndarray]) -> float:
    """中位数。"""
    _check_non_empty(values, "calc_median")
    return float(np.median(values))


def calc_sd(values: Union[List[float], np.ndarray], ddof: int = 1) -> float:
    """
    标准偏差。

    Parameters
    ----------
    values : array-like
    ddof : int — 自由度修正，默认 1（样本标准差）
    """
    _check_non_empty(values, "calc_sd")
    return float(np.std(values, ddof=ddof))


def calc_var(values: Union[List[float], np.ndarray], ddof: int = 1) -> float:
    """方差。"""
    _check_non_empty(values, "calc_var")
    return float(np.var(values, ddof=ddof))


def calc_rsd(values: Union[List[float], np.ndarray]) -> float:
    """
    相对标准偏差（RSD%）。
    RSD = SD / mean * 100
    """
    _check_non_empty(values, "calc_rsd")
    mean = np.mean(values)
    if mean == 0:
        return 0.0
    return float(np.std(values, ddof=1) / mean * 100)


def calc_cv(values: Union[List[float], np.ndarray]) -> float:
    """变异系数（CV），即 RSD。"""
    return calc_rsd(values)


def calc_count(values: Union[List[float], np.ndarray]) -> int:
    """有效数据点数（非 NaN）。"""
    arr = np.asarray(values, dtype=float)
    return int(np.sum(~np.isnan(arr)))


def calc_min(values: Union[List[float], np.ndarray]) -> float:
    """最小值。"""
    _check_non_empty(values, "calc_min")
    return float(np.min(values))


def calc_max(values: Union[List[float], np.ndarray]) -> float:
    """最大值。"""
    _check_non_empty(values, "calc_max")
    return float(np.max(values))


def calc_range(values: Union[List[float], np.ndarray]) -> float:
    """极差。"""
    _check_non_empty(values, "calc_range")
    return float(np.ptp(values))


def calc_sum(values: Union[List[float], np.ndarray]) -> float:
    """求和。"""
    _check_non_empty(values, "calc_sum")
    return float(np.sum(values))


# ═══════════════════════════════════════════════════════
# 合并与合成统计
# ═══════════════════════════════════════════════════════

def calc_pooled_sd(groups: List[Union[List[float], np.ndarray]]) -> float:
    """
    合并标准差（加权合并）。
    pooled_sd = sqrt( Σ((n_i-1) * s_i²) / Σ(n_i - k) )
    """
    k = 0
    total_ss = 0
    total_df = 0
    for g in groups:
        arr = np.array(g, dtype=float)
        n = len(arr)
        if n < 2:
            continue
        sd = np.std(arr, ddof=1)
        total_ss += (n - 1) * sd ** 2
        total_df += n - 1
        k += 1
    if total_df == 0 or k < 2:
        raise ValueError("合并标准差需要至少2组且每组≥2个数据点")
    return float(np.sqrt(total_ss / total_df))


def calc_pooled_rsd(groups: List[Union[List[float], np.ndarray]]) -> float:
    """合并 RSD% = pooled_sd / grand_mean * 100"""
    pooled = calc_pooled_sd(groups)
    all_vals = np.concatenate([np.array(g, dtype=float) for g in groups])
    grand_mean = np.mean(all_vals)
    if grand_mean == 0:
        return 0.0
    return pooled / grand_mean * 100


def calc_robust_sd(values: Union[List[float], np.ndarray]) -> float:
    """
    稳健标准差（MAD 法）。
    robust_sd = 1.4826 * median(|xi - median(x)|)
    """
    _check_non_empty(values, "calc_robust_sd")
    arr = np.array(values, dtype=float)
    med = np.median(arr)
    mad = np.median(np.abs(arr - med))
    return float(1.4826 * mad)


# ═══════════════════════════════════════════════════════
# 偏倚计算
# ═══════════════════════════════════════════════════════

def calc_bias(mean: float, reference: float) -> float:
    """
    偏倚 = 均值 - 参考值
    """
    return mean - reference


def calc_bias_relative(mean: float, reference: float) -> float:
    """
    相对偏倚(%) = (均值 - 参考值) / 参考值 * 100
    """
    if reference == 0:
        return 0.0
    return (mean - reference) / reference * 100


def calc_bias_from_values(values: Union[List[float], np.ndarray],
                           reference: float) -> float:
    """从原始数据直接计算偏倚。"""
    return calc_bias(calc_mean(values), reference)


# ═══════════════════════════════════════════════════════
# SSE 和回归相关
# ═══════════════════════════════════════════════════════

def calc_sse(residuals: Union[List[float], np.ndarray]) -> float:
    """
    残差平方和 SSE = Σ(residuals²)
    """
    return float(np.sum(np.array(residuals, dtype=float) ** 2))


def calc_syx(residuals: Union[List[float], np.ndarray], n: int, n_params: int = 2) -> float:
    """
    剩余标准偏差 Sy/x = sqrt(SSE / (n - n_params))
    """
    resid = np.array(residuals, dtype=float)
    df = n - n_params
    if df <= 0:
        raise ValueError(f"自由度不足: n={n}, n_params={n_params}")
    return float(np.sqrt(np.sum(resid ** 2) / df))


def calc_ssr(predicted: Union[List[float], np.ndarray],
             observed: Union[List[float], np.ndarray]) -> float:
    """
    回归平方和 SSR = Σ(y_pred - y_mean)²
    """
    pred = np.array(predicted, dtype=float)
    y_mean = np.mean(observed)
    return float(np.sum((pred - y_mean) ** 2))


def calc_sst(observed: Union[List[float], np.ndarray]) -> float:
    """
    总平方和 SST = Σ(y_i - y_mean)²
    """
    arr = np.array(observed, dtype=float)
    y_mean = np.mean(arr)
    return float(np.sum((arr - y_mean) ** 2))


def calc_r2(sse: float, sst: float) -> float:
    """
    决定系数 R² = 1 - SSE/SST
    """
    if sst == 0:
        return 0.0
    return 1 - sse / sst


def calc_r2_adjusted(r2: float, n: int, k: int) -> float:
    """
    调整 R² = 1 - (1-R²)(n-1)/(n-k-1)
    n: 样本量, k: 自变量数
    """
    if n <= k + 1:
        return r2
    return 1 - (1 - r2) * (n - 1) / (n - k - 1)


# ═══════════════════════════════════════════════════════
# 置信区间
# ═══════════════════════════════════════════════════════

def calc_ci_mean(mean: float, sd: float, n: int, t_crit: float) -> tuple:
    """
    均值的置信区间。

    Parameters
    ----------
    mean : float — 样本均值
    sd : float — 样本标准差
    n : int — 样本量
    t_crit : float — t 临界值

    Returns
    -------
    (lower, upper)
    """
    margin = t_crit * sd / np.sqrt(n)
    return (mean - margin, mean + margin)


def calc_ci_bias(mean: float, reference: float, sd: float, n: int,
                 t_crit: float) -> tuple:
    """
    偏倚的置信区间。
    CI_bias = (mean - ref) ± t_crit × sd / sqrt(n)
    """
    bias = mean - reference
    margin = t_crit * sd / np.sqrt(n)
    return (bias - margin, bias + margin)


# ═══════════════════════════════════════════════════════
# Z 值计算
# ═══════════════════════════════════════════════════════

def calc_z_score(x: float, assigned_value: float, std_dev: float) -> float:
    """Z 值 = (x - assigned_value) / std_dev"""
    if std_dev <= 0:
        raise ValueError("标准偏差必须大于 0")
    return (x - assigned_value) / std_dev


def calc_z_judgment(z: float) -> str:
    """Z 值判定（ISO 13528 / CNAS-GL002）"""
    if abs(z) <= 2:
        return "满意"
    elif abs(z) <= 3:
        return "可疑"
    return "不满意"


# ═══════════════════════════════════════════════════════
# ANOVA 相关
# ═══════════════════════════════════════════════════════

def calc_msb(ssb: float, dfb: int) -> float:
    """组间均方 MSB = SSB / dfb"""
    return ssb / dfb if dfb > 0 else 0.0


def calc_msw(ssw: float, dfw: int) -> float:
    """组内均方 MSW = SSW / dfw"""
    return ssw / dfw if dfw > 0 else 0.0


def calc_f_value(msb: float, msw: float) -> float:
    """F 值 = MSB / MSW"""
    return msb / msw if msw > 0 else 0.0


# ═══════════════════════════════════════════════════════
# 临界值查表（t_distribution / F 分布）
# ═══════════════════════════════════════════════════════

def calc_tcrit(df: int, alpha: float = 0.05, two_tailed: bool = True) -> float:
    """
    t 分布临界值查表。

    委托到 core.qc_tables.t_critical。

    Parameters
    ----------
    df : int — 自由度
    alpha : float — 显著性水平，默认 0.05
    two_tailed : bool — 是否双尾，默认 True
        双尾时直接用 alpha 查表（如 α=0.05 时每尾 2.5%）
        单尾时查 alpha=alpha×2（如 α=0.05 单尾 → 查 α=0.10 双尾）

    Returns
    -------
    float
    """
    from scripts.core.qc_tables import t_critical
    # t 表存储的是双尾值，单尾需要将 α×2 传入
    table_alpha = alpha if two_tailed else alpha * 2
    return t_critical(df, table_alpha)


def calc_fcrit(df1: int, df2: int, alpha: float = 0.05) -> float:
    """
    F 分布临界值查表（α=0.05）。

    委托到 core.qc_tables.f_critical。

    Parameters
    ----------
    df1 : int — 分子自由度（组间）
    df2 : int — 分母自由度（组内）
    alpha : float — 显著性水平（当前仅支持 0.05）

    Returns
    -------
    float
    """
    from scripts.core.qc_tables import f_critical
    return f_critical(df1, df2, alpha)


# ═══════════════════════════════════════════════════════
# Z 表 / P 表分布算子
# ═══════════════════════════════════════════════════════

def calc_z_to_p(z: float) -> float:
    """Z 值转累积概率 Φ(z)。"""
    from scripts.core.qc_tables import z_to_p
    return z_to_p(z)


def calc_z_to_p_two_tailed(z: float) -> float:
    """Z 值转双尾 p 值。"""
    from scripts.core.qc_tables import z_to_p_two_tailed
    return z_to_p_two_tailed(z)


def calc_z_critical(alpha: float = 0.05, two_tailed: bool = True) -> float:
    """给定 α 查临界 Z 值。"""
    from scripts.core.qc_tables import z_critical
    return z_critical(alpha, two_tailed)


def calc_p_from_t(t_stat: float, df: int) -> dict:
    """t 检验 p 值计算（含显著性判定）。"""
    from scripts.core.qc_tables import p_from_t
    return p_from_t(t_stat, df)


def calc_p_from_f(f_stat: float, df1: int, df2: int) -> dict:
    """F 检验 p 值计算（含显著性判定）。"""
    from scripts.core.qc_tables import p_from_f
    return p_from_f(f_stat, df1, df2)


# ═══════════════════════════════════════════════════════
# 辅助
# ═══════════════════════════════════════════════════════

def calc_tolerance(magnitude_order: int) -> float:
    """根据数量级获取允许偏差(%)。"""
    TOLERANCE_MAP = {
        4: 1.0, 5: 2.5, 6: 6.0, 7: 10.0, 8: 20.0, 9: 30.0, 10: 50.0,
    }
    return TOLERANCE_MAP.get(magnitude_order, min(magnitude_order * 5.0, 100.0) if magnitude_order > 10 else 1.0)


def calc_magnitude_order(value: float) -> int:
    """根据数值估算数量级指数。"""
    if value <= 0:
        return 6
    return int(np.floor(np.abs(np.log10(abs(value)))))


# ═══════════════════════════════════════════════════════
# 秩和计算（非参数检验）
# ═══════════════════════════════════════════════════════

def calc_rank_sum(values: Union[List[float], np.ndarray]) -> dict:
    """
    秩和计算 — 对数值序列排序并赋予秩次（等值取平均秩）。

    Parameters
    ----------
    values : array-like — 原始数值

    Returns
    -------
    dict — {"ranks": list, "n": int, "sorted": list}
    """
    arr = np.array(values, dtype=float)
    n = len(arr)
    # 排序并计算秩次（等值取平均秩）
    sorted_idx = np.argsort(arr)
    ranks = np.zeros(n)
    i = 0
    while i < n:
        j = i
        while j < n and arr[sorted_idx[j]] == arr[sorted_idx[i]]:
            j += 1
        # 等值组赋予平均秩
        avg_rank = (i + j + 1) / 2.0  # 秩从1开始
        for k in range(i, j):
            ranks[sorted_idx[k]] = avg_rank
        i = j
    return {
        "ranks": ranks.tolist(),
        "n": n,
        "sorted": np.sort(arr).tolist(),
    }


def calc_mann_whitney_u(x: Union[List[float], np.ndarray],
                         y: Union[List[float], np.ndarray]) -> dict:
    """
    Mann-Whitney U 检验（Wilcoxon 秩和检验）— 两组独立样本的非参数比较。

    适用于 t 检验的正态性假设不满足时。

    Parameters
    ----------
    x : array-like — 第一组样本
    y : array-like — 第二组样本

    Returns
    -------
    dict
        {"u_statistic": float, "n1": int, "n2": int,
         "mean_u": float, "sd_u": float, "z_value": float,
         "p_value": float, "p_two_tailed": float, "significant_005": bool,
         "rank_sum_x": float, "rank_sum_y": float, "summary": str}
    """
    x_arr = np.array(x, dtype=float)
    y_arr = np.array(y, dtype=float)
    n1, n2 = len(x_arr), len(y_arr)

    # 合并排序并赋秩
    combined = np.concatenate([x_arr, y_arr])
    sorted_idx = np.argsort(combined)

    # 赋予秩次（平均秩处理等值）
    ranks = np.zeros(len(combined))
    i = 0
    total_n = len(combined)
    while i < total_n:
        j = i
        while j < total_n and combined[sorted_idx[j]] == combined[sorted_idx[i]]:
            j += 1
        avg_rank = (i + j + 1) / 2.0
        for k in range(i, j):
            ranks[sorted_idx[k]] = avg_rank
        i = j

    # 计算 U 统计量
    rank_sum_x = np.sum(ranks[:n1])
    rank_sum_y = np.sum(ranks[n1:])
    u1 = rank_sum_x - n1 * (n1 + 1) / 2.0
    u2 = rank_sum_y - n2 * (n2 + 1) / 2.0
    u_stat = min(u1, u2)

    # 正态近似（n1,n2 > 10 时成立，小样本用精确表）
    mean_u = n1 * n2 / 2.0
    # 标准误差（含等值校正）
    tie_groups = {}
    for v in combined:
        key = f"{v:.10f}"
        tie_groups[key] = tie_groups.get(key, 0) + 1
    tie_correction = sum(t ** 3 - t for t in tie_groups.values() if t > 1)
    total_n_sq = total_n * (total_n ** 2 - 1)
    sd_u = np.sqrt((n1 * n2 / 12.0) * (total_n_sq - tie_correction) / (total_n_sq - 1)) if total_n > 1 else 1.0
    if sd_u == 0:
        sd_u = 1.0

    z_val = (u_stat - mean_u) / sd_u

    # 用 Z 表算 p 值
    from scripts.core.qc_tables import z_to_p_two_tailed
    p_val = z_to_p_two_tailed(z_val)

    return {
        "u_statistic": float(u_stat),
        "u1": float(u1),
        "u2": float(u2),
        "n1": n1,
        "n2": n2,
        "rank_sum_x": float(rank_sum_x),
        "rank_sum_y": float(rank_sum_y),
        "mean_u": float(mean_u),
        "sd_u": float(sd_u),
        "z_value": float(z_val),
        "p_value": float(p_val),
        "p_two_tailed": float(p_val),
        "significant_005": p_val < 0.05,
        "summary": (
            f"Mann-Whitney U = {u_stat:.2f}, "
            f"n1={n1}, n2={n2}, "
            f"z = {z_val:.4f}, "
            f"p = {p_val:.4f}"
            f"{' *' if p_val < 0.05 else ''}"
        ),
    }


def calc_wilcoxon_signed_rank(x: Union[List[float], np.ndarray],
                                y: Union[List[float], np.ndarray] = None,
                                mu: float = 0) -> dict:
    """
    Wilcoxon 符号秩检验 — 配对样本或单样本中位数检验。

    Parameters
    ----------
    x : array-like — 第一组（或差值）
    y : array-like, optional — 第二组（提供时计算 x-y）
    mu : float — 中位数假设值（单样本时），默认 0

    Returns
    -------
    dict
        {"w_statistic": float, "n": int, "z_value": float, "p_value": float, ...}
    """
    if y is not None:
        diff = np.array(x, dtype=float) - np.array(y, dtype=float)
    else:
        diff = np.array(x, dtype=float) - mu

    # 排除差值为 0 的样本
    diff = diff[diff != 0]
    n = len(diff)
    if n == 0:
        return {"w_statistic": 0, "n": 0, "p_value": 1.0,
                "significant_005": False, "summary": "无有效配对"}

    # 对绝对值排序赋秩
    abs_diff = np.abs(diff)
    sorted_idx = np.argsort(abs_diff)
    ranks = np.zeros(n)
    i = 0
    while i < n:
        j = i
        while j < n and abs_diff[sorted_idx[j]] == abs_diff[sorted_idx[i]]:
            j += 1
        avg_rank = (i + j + 1) / 2.0
        for k in range(i, j):
            ranks[sorted_idx[k]] = avg_rank
        i = j

    # W+ 和 W-
    w_plus = np.sum(ranks[diff > 0])
    w_minus = np.sum(ranks[diff < 0])
    w_stat = min(w_plus, w_minus)

    # 正态近似
    mean_w = n * (n + 1) / 4.0
    sd_w = np.sqrt(n * (n + 1) * (2 * n + 1) / 24.0)
    z_val = (w_stat - mean_w) / sd_w if sd_w > 0 else 0

    from scripts.core.qc_tables import z_to_p_two_tailed
    p_val = z_to_p_two_tailed(z_val)

    return {
        "w_statistic": float(w_stat),
        "w_plus": float(w_plus),
        "w_minus": float(w_minus),
        "n": n,
        "z_value": float(z_val),
        "p_value": float(p_val),
        "p_two_tailed": float(p_val),
        "significant_005": p_val < 0.05,
        "summary": (
            f"Wilcoxon W = {w_stat:.2f}, "
            f"n = {n}, "
            f"z = {z_val:.4f}, "
            f"p = {p_val:.4f}"
            f"{' *' if p_val < 0.05 else ''}"
        ),
    }


# ═══════════════════════════════════════════════════════
# 归一化 / 标准化
# ═══════════════════════════════════════════════════════

def normalize_z_score(values: Union[List[float], np.ndarray]) -> np.ndarray:
    """
    Z 归一法（Z-score normalization）。
    z = (x - mean) / sd
    处理后均值为 0，标准差为 1。
    """
    arr = np.array(values, dtype=float)
    mean = np.mean(arr)
    sd = np.std(arr, ddof=0)
    if sd == 0:
        return np.zeros_like(arr)
    return (arr - mean) / sd


def normalize_minmax(values: Union[List[float], np.ndarray],
                     a: float = 0, b: float = 1) -> np.ndarray:
    """
    极差归一法（Min-Max normalization）。
    x' = a + (x - min) / (max - min) × (b - a)
    处理后范围 [a, b]，默认 [0, 1]。
    """
    arr = np.array(values, dtype=float)
    vmin, vmax = np.min(arr), np.max(arr)
    if vmax == vmin:
        return np.full_like(arr, (a + b) / 2.0)
    return a + (arr - vmin) / (vmax - vmin) * (b - a)


def normalize_robust(values: Union[List[float], np.ndarray]) -> np.ndarray:
    """
    稳健归一法（Robust normalization）。
    x' = (x - median) / MAD
    使用中位数和绝对中位差，抗异常值。
    """
    arr = np.array(values, dtype=float)
    med = np.median(arr)
    mad = np.median(np.abs(arr - med))
    if mad == 0:
        return arr - med
    return (arr - med) / (1.4826 * mad)


def normalize_decimal(values: Union[List[float], np.ndarray]) -> np.ndarray:
    """
    小数定标归一法（Decimal scaling normalization）。
    x' = x / 10^k，其中 k 为使 max(|x'|) < 1 的最小整数。
    """
    arr = np.array(values, dtype=float)
    max_abs = np.max(np.abs(arr))
    if max_abs == 0:
        return np.zeros_like(arr)
    k = int(np.ceil(np.log10(max_abs + 1e-15)))
    if k <= 0:
        return arr
    return arr / (10 ** k)


# ═══════════════════════════════════════════════════════
# 修约 / 数值舍入（QC 专用）
# ═══════════════════════════════════════════════════════

def round_ceil(value: float, decimals: int = 0) -> float:
    """向上修约（向正无穷方向）。"""
    import math
    factor = 10 ** decimals
    return math.ceil(value * factor) / factor


def round_floor(value: float, decimals: int = 0) -> float:
    """向下修约（向负无穷方向）。"""
    import math
    factor = 10 ** decimals
    return math.floor(value * factor) / factor


def round_half_up(value: float, decimals: int = 0) -> float:
    """
    四舍五入（远离零方向）。
    0.5 → 1, -0.5 → -1
    """
    import math
    factor = 10 ** decimals
    if value >= 0:
        return math.floor(value * factor + 0.5) / factor
    else:
        return math.ceil(value * factor - 0.5) / factor


def round_half_even(value: float, decimals: int = 0) -> float:
    """
    四舍六入五成双（银行家舍入）。
    2.5 → 2, 3.5 → 4, 1.5 → 2
    符合 GB/T 8170-2008 数值修约规则。
    """
    import math
    factor = 10 ** decimals
    scaled = value * factor
    # 使用 Python 内置的 round（银行家舍入）
    return round(scaled) / factor


def round_significant(value: float, sig_figs: int = 4) -> float:
    """
    有效数字修约。

    Parameters
    ----------
    value : float — 待修约数值
    sig_figs : int — 有效数字位数，默认 4 位

    Returns
    -------
    float
    """
    if value == 0:
        return 0.0
    import math
    # 确定数量级
    magnitude = int(math.floor(math.log10(abs(value))))
    # 计算修约到 sig_figs 位有效数字的量级
    factor = 10 ** (sig_figs - magnitude - 1)
    return round(value * factor) / factor


def round_to_decimals(value: float, decimals: int = 4) -> float:
    """指定小数位数修约（四舍六入五成双）。"""
    return round_half_even(value, decimals)


def round_format(value: float, decimals: int = 4,
                 method: str = "half_even") -> float:
    """
    统一修约接口 — 用指定方法修约。

    Parameters
    ----------
    value : float
    decimals : int — 小数位数
    method : str — "half_up"|"half_even"|"ceil"|"floor"|"significant"

    Returns
    -------
    float
    """
    METHOD_MAP = {
        "half_up": round_half_up,
        "half_even": round_half_even,
        "ceil": round_ceil,
        "floor": round_floor,
        "significant": lambda v, d: round_significant(v, sig_figs=d),
    }
    func = METHOD_MAP.get(method, round_half_even)
    return func(value, decimals)


# ═══════════════════════════════════════════════════════
# 导出清单（用于注册表自动发现）
# ═══════════════════════════════════════════════════════

__all__ = [
    # 基础描述统计
    "calc_mean", "calc_median", "calc_sd", "calc_var", "calc_rsd", "calc_cv",
    "calc_count", "calc_min", "calc_max", "calc_range", "calc_sum",
    # 合并与合成统计
    "calc_pooled_sd", "calc_pooled_rsd", "calc_robust_sd",
    # 偏倚
    "calc_bias", "calc_bias_relative", "calc_bias_from_values",
    # 回归相关
    "calc_sse", "calc_syx", "calc_ssr", "calc_sst", "calc_r2", "calc_r2_adjusted",
    # 置信区间
    "calc_ci_mean", "calc_ci_bias",
    # Z 值
    "calc_z_score", "calc_z_judgment",
    # 临界值
    "calc_tcrit", "calc_fcrit",
    # Z表 / P表
    "calc_z_to_p", "calc_z_to_p_two_tailed", "calc_z_critical",
    "calc_p_from_t", "calc_p_from_f",
    # ANOVA
    "calc_msb", "calc_msw", "calc_f_value",
    # 辅助
    "calc_tolerance", "calc_magnitude_order",
    # 秩和（非参数检验）
    "calc_rank_sum", "calc_mann_whitney_u", "calc_wilcoxon_signed_rank",
    # 归一化 / 标准化
    "normalize_z_score", "normalize_minmax", "normalize_robust", "normalize_decimal",
    # 修约
    "round_ceil", "round_floor", "round_half_up", "round_half_even",
    "round_significant", "round_to_decimals", "round_format",
]
