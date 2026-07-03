"""
室内质控（Internal QC）

场景：同一实验室内部，评估方法精密度、重复性、稳定性。

核心流程：
1. 多水平精密度分析（SD、RSD、均值、中位数、合成标准差）
2. 重复限性检查（r值、相对误差）
3. 允许值分级判定
4. 质控图（Levey-Jennings）
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from ..core.stats import calc_precision, calc_synthetic_std
from ..core.qc_tables import get_tolerance, get_magnitude_order
from ..reporting import publish


def _warn_on_data_quality(data, value_col, level_col=None, min_rows=3):
    """数据质量前置校验：不阻断执行，只输出警告。"""
    warnings = []
    if data.empty:
        warnings.append("数据为空，计算结果可能无意义。")
    if value_col not in data.columns:
        warnings.append(f"数值列 '{value_col}' 不存在于数据中。")
        return warnings
    vals = data[value_col].dropna()
    if len(vals) < min_rows:
        warnings.append(f"有效数据仅 {len(vals)} 行（建议至少 {min_rows} 行）。")
    if len(vals) < len(data):
        warnings.append(f"数值列 '{value_col}' 包含 {len(data) - len(vals)} 个空值，已自动跳过。")
    if pd.api.types.is_numeric_dtype(data[value_col]):
        if vals.std() == 0:
            warnings.append(f"数值列 '{value_col}' 所有值相同（标准差为0），精密度分析无意义。")
    else:
        warnings.append(f"数值列 '{value_col}' 不是数值类型，请检查数据格式。")
    if level_col and level_col in data.columns:
        n_levels = data[level_col].nunique()
        if n_levels < 2:
            warnings.append(f"水平列 '{level_col}' 仅有 {n_levels} 个水平，多水平分析至少需要 2 个。")
    return warnings


def internal_precision_analysis(data, level_col="水平", value_col="结果", n_replicates=3):
    """
    室内精密度分析 — 多水平精密度统计与合成标准差。

    对应原始Excel「方法正确度和精密度」模块。

    Parameters
    ----------
    data : pd.DataFrame
        需包含水平列和结果列，每水平n_replicates行
    level_col : str
        水平标识列名
    value_col : str
        结果数值列名
    n_replicates : int
        每水平重复次数（默认3）

    Returns
    -------
    dict
        {
            "per_level": pd.DataFrame,   # 每水平统计
            "synthetic_std": float,       # 合成标准偏差（正规算法）
            "synthetic_std_simple": float # 合成标准偏差（简单算法）
            "synthetic_rsd": float,       # 合成RSD（正规算法）
            "synthetic_rsd_simple": float # 合成RSD（简单算法）
        }
    """
    # 数据质量前置校验
    quality_warnings = _warn_on_data_quality(data, value_col, level_col)
    if quality_warnings:
        import warnings as _warn
        for w in quality_warnings:
            _warn.warn(f"[数据质量] {w}")
        # 同步输出到 stdout，避免 stderr 被忽略
        print("⚠️  数据质量警告：")
        for w in quality_warnings:
            print(f"   • {w}")

    levels = data[level_col].unique()
    summaries = []

    groups = []
    for level in sorted(levels):
        vals = data[data[level_col] == level][value_col].dropna().values
        if len(vals) < 2:
            continue

        stats = calc_precision(vals)
        stats[level_col] = level
        summaries.append(stats)
        groups.append(vals)

    per_level = pd.DataFrame(summaries)

    # 合成标准差
    k = len(groups)
    syn_result = calc_synthetic_std(groups, method="standard") if groups else {"synthetic_std": 0, "overall_mean": 0}
    syn_simple_result = calc_synthetic_std(groups, method="simple") if groups else {"synthetic_std": 0, "overall_mean": 0}
    syn_std = syn_result["synthetic_std"] if isinstance(syn_result, dict) else syn_result
    syn_std_simple = syn_simple_result["synthetic_std"] if isinstance(syn_simple_result, dict) else syn_simple_result

    # 合成RSD
    all_means = [np.mean(g) for g in groups]
    grand_mean = np.average(all_means) if all_means else 0

    syn_rsd = (syn_std / grand_mean * 100) if grand_mean != 0 else 0
    syn_rsd_simple = (syn_std_simple / grand_mean * 100) if grand_mean != 0 else 0

    result = {
        "per_level": per_level,
        "synthetic_std": syn_std,
        "synthetic_std_simple": syn_std_simple,
        "synthetic_rsd": syn_rsd,
        "synthetic_rsd_simple": syn_rsd_simple,
        "grand_mean": grand_mean,
        "warnings": quality_warnings,
    }
    publish(per_level, title="室内精密度分析 — 各水平统计")
    publish(result, title="合成标准差")
    return result


def repeatability_check(results, tolerance_pct=None):
    """
    重复限性检查 — 检查平行样结果的差异是否在允许范围内。

    对应原始Excel「重复限性」模块。

    Parameters
    ----------
    results : list of float
        平行样结果列表
    tolerance_pct : float, optional
        允许偏差百分比。若为None，根据结果数量级自动查找。

    Returns
    -------
    dict
        {
            "max_min_diff": float,
            "mean": float,
            "relative_error_pct": float,
            "tolerance_pct": float,
            "range_ok": bool,
            "relative_ok": bool,
            "judgment": str  # "合格" / "不合格"
        }
    """
    arr = np.array(results)
    mean_val = np.mean(arr)
    max_min_diff = np.max(arr) - np.min(arr)
    relative_error = abs(max_min_diff) / mean_val * 100 if mean_val != 0 else 0

    if tolerance_pct is None:
        mag = get_magnitude_order(mean_val)
        tolerance_pct = get_tolerance(mag)

    range_ok = max_min_diff <= tolerance_pct / 100 * mean_val
    relative_ok = relative_error <= tolerance_pct

    result = {
        "max_min_diff": max_min_diff,
        "mean": mean_val,
        "relative_error_pct": relative_error,
        "tolerance_pct": tolerance_pct,
        "range_ok": range_ok,
        "relative_ok": relative_ok,
        "judgment": "合格" if (range_ok and relative_ok) else "不合格",
    }
    publish(result, title="重复限性检查")
    return result


def control_chart(data, value_col="结果", date_col=None,
                  method="mean_std", target=None, sigma_limits=3):
    """
    质控图（Levey-Jennings）。

    绘制单个质控物多次测定结果的质控图，标注±1σ、±2σ、±3σ限。

    Parameters
    ----------
    data : pd.DataFrame — 质控数据
    value_col : str — 测量值列名
    date_col : str, optional — 日期列（用于X轴标签）
    method : str — "mean_std"（基于均值和标准差）
    target : float, optional — 目标值（默认用数据均值）
    sigma_limits : int — 标准差倍数（默认3）

    Returns
    -------
    matplotlib.figure.Figure
    dict — 质控统计量
    """
    values = data[value_col].dropna().values
    mean_val = target if target is not None else np.mean(values)
    std_val = np.std(values, ddof=1)

    fig, ax = plt.subplots(figsize=(12, 5))

    x_labels = data[date_col] if date_col else range(len(values))
    x = range(len(values))

    ax.plot(x, values, 'o-', color='#2c3e50', markersize=6, linewidth=1.5, label="测量值")
    ax.axhline(mean_val, color='#27ae60', linewidth=2, label=f"均值 ({mean_val:.3f})")
    ax.axhline(mean_val + std_val, color='#f39c12', linestyle='--', linewidth=1, label=f"+1σ")
    ax.axhline(mean_val - std_val, color='#f39c12', linestyle='--', linewidth=1, label=f"-1σ")
    ax.axhline(mean_val + 2 * std_val, color='#e67e22', linestyle='--', linewidth=1, label=f"+2σ")
    ax.axhline(mean_val - 2 * std_val, color='#e67e22', linestyle='--', linewidth=1, label=f"-2σ")
    ax.axhline(mean_val + sigma_limits * std_val, color='#e74c3c', linestyle=':', linewidth=1.5, label=f"+{sigma_limits}σ")
    ax.axhline(mean_val - sigma_limits * std_val, color='#e74c3c', linestyle=':', linewidth=1.5, label=f"-{sigma_limits}σ")

    # 标注失控点
    for i, v in enumerate(values):
        if abs(v - mean_val) > sigma_limits * std_val:
            ax.annotate(f"⚠ {v:.3f}", (i, v), textcoords="offset points",
                        xytext=(0, 10), ha='center', fontsize=8, color='red')

    if date_col:
        ax.set_xticks(x)
        ax.set_xticklabels([str(d)[:10] for d in x_labels], rotation=45, ha='right')

    ax.set_title("Levey-Jennings 质控图", fontsize=14)
    ax.set_ylabel("测量值")
    ax.legend(loc='best', ncol=3, fontsize=8)
    ax.grid(alpha=0.3)
    plt.tight_layout()

    stats = {
        "mean": mean_val,
        "std": std_val,
        "rsd": std_val / mean_val * 100 if mean_val != 0 else 0,
        "n": len(values),
        "out_of_control": sum(abs(v - mean_val) > sigma_limits * std_val for v in values),
    }

    publish(stats, title="Levey-Jennings 质控图", figure=fig, html_filename="qc_chart.html")
    return fig, stats


def precision_report(result):
    """
    将室内精密度分析结果格式化为可读报告文本。

    Parameters
    ----------
    result : dict — internal_precision_analysis的返回值

    Returns
    -------
    str
    """
    lines = [
        "=" * 60,
        "  室内精密度分析报告",
        "=" * 60,
    ]

    per_level = result.get("per_level")
    if per_level is not None and not per_level.empty:
        lines.append("\n各水平精密度：")
        lines.append(f"{'水平':<10} {'均值':<10} {'SD':<10} {'RSD(%)':<10} {'中位数':<10}")
        lines.append("-" * 50)
        for _, row in per_level.iterrows():
            lines.append(
                f"{str(row.get('水平', '')):<10} "
                f"{row.get('mean', 0):<10.4f} "
                f"{row.get('std', 0):<10.4f} "
                f"{row.get('rsd', 0):<10.2f} "
                f"{row.get('median', 0):<10.4f}"
            )

    lines.append(f"\n合成标准偏差（正规算法）：{result.get('synthetic_std', 0):.4f}")
    lines.append(f"合成标准偏差（简单算法）：{result.get('synthetic_std_simple', 0):.4f}")
    lines.append(f"合成RSD（正规算法）：{result.get('synthetic_rsd', 0):.2f}%")
    lines.append(f"合成RSD（简单算法）：{result.get('synthetic_rsd_simple', 0):.2f}%")
    lines.append(f"整体均值：{result.get('grand_mean', 0):.4f}")

    return "\n".join(lines)
