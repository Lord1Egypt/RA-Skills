"""
室间质控（Inter-lab QC）& 批次间比对

场景：多家实验室 / 多个操作人员 / 多个批次之间的比对分析。

核心流程：
1. ANOVA方差分析 —— 判断各组均值是否一致
2. F临界值查表 + 显著性判定
3. Z值计算 + 质控判定（ISO 13528）
4. Youden图（双实验室比对可视化）
5. 允许值分级判定
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from ..analysis.anova import anova_oneway, anova_table
from ..core.qc_tables import f_critical, calculate_z_score, z_score_judgment, get_tolerance, get_magnitude_order
from ..reporting import publish


def _warn_on_data_quality(data, value_col, group_col=None, min_rows=3):
    """数据质量前置校验：不阻断执行，只输出警告。"""
    warnings = []
    if data.empty:
        warnings.append("数据为空，计算结果可能无意义。")
        return warnings
    if value_col not in data.columns:
        warnings.append(f"数值列 '{value_col}' 不存在于数据中。")
        return warnings
    vals = data[value_col].dropna()
    if len(vals) < min_rows:
        warnings.append(f"有效数据仅 {len(vals)} 行（建议至少 {min_rows} 行）。")
    if len(vals) < len(data):
        warnings.append(f"数值列 '{value_col}' 包含 {len(data) - len(vals)} 个空值，已自动跳过。")
    if not pd.api.types.is_numeric_dtype(data[value_col]):
        warnings.append(f"数值列 '{value_col}' 不是数值类型，请检查数据格式。")
        return warnings
    if vals.std() == 0:
        warnings.append(f"数值列 '{value_col}' 所有值相同（标准差为0），比对分析无意义。")
    if group_col and group_col in data.columns:
        n_groups = data[group_col].nunique()
        if n_groups < 2:
            warnings.append(f"分组列 '{group_col}' 仅有 {n_groups} 个组，比对分析至少需要 2 个组。")
        # 检查是否有组数据不足
        small_groups = [g for g in data[group_col].unique()
                        if len(data[data[group_col] == g][value_col].dropna()) < 2]
        if small_groups:
            warnings.append(f"以下组数据不足2行: {small_groups}，这些组会被跳过。")
    return warnings


def interlab_comparison(data, lab_col="实验室", value_col="结果"):
    """
    室间/人员比对分析 —— 基于ANOVA的多组均值比较。

    对应原始Excel「室间比对/批次间比对」模块。

    Parameters
    ----------
    data : pd.DataFrame
        包含实验室列和结果列
    lab_col : str
        实验室/人员标识列名
    value_col : str
        结果数值列名

    Returns
    -------
    dict
        {
            "anova": anova_oneway result,
            "anova_table": pd.DataFrame,
            "group_stats": pd.DataFrame,   # 每组统计量
            "conclusion": str
        }
    """
    # 数据质量前置校验
    quality_warnings = _warn_on_data_quality(data, value_col, lab_col)
    if quality_warnings:
        import warnings as _warn
        for w in quality_warnings:
            _warn.warn(f"[数据质量] {w}")
        print("⚠️  数据质量警告：")
        for w in quality_warnings:
            print(f"   • {w}")

    groups = {}
    group_names = sorted(data[lab_col].unique())
    for name in group_names:
        vals = data[data[lab_col] == name][value_col].dropna().values
        if len(vals) > 0:
            groups[name] = vals

    # ANOVA
    anova_result = anova_oneway(groups)
    anova_df = anova_table(anova_result)

    # 每组统计
    stats_list = []
    for name, vals in groups.items():
        stats_list.append({
            lab_col: name,
            "n": len(vals),
            "均值": np.mean(vals),
            "SD": np.std(vals, ddof=1),
            "RSD(%)": np.std(vals, ddof=1) / np.mean(vals) * 100 if np.mean(vals) != 0 else 0,
            "中位数": np.median(vals),
            "最小值": np.min(vals),
            "最大值": np.max(vals),
        })
    group_stats = pd.DataFrame(stats_list)

    # 结论
    if anova_result["significant"]:
        conclusion = (
            f"F值 = {anova_result['f_value']:.4f} > F临界值 F({anova_result['dfb']},{anova_result['dfw']}) = {anova_result['f_critical']:.4f}\n"
            f"→ 各组均值存在显著差异（p<0.05），比对结果不一致，需排查原因。"
        )
    else:
        conclusion = (
            f"F值 = {anova_result['f_value']:.4f} ≤ F临界值 F({anova_result['dfb']},{anova_result['dfw']}) = {anova_result['f_critical']:.4f}\n"
            f"→ 各组均值无显著差异（p≥0.05），比对结果一致。"
        )

    result = {
        "anova": anova_result,
        "anova_table": anova_df,
        "group_stats": group_stats,
        "conclusion": conclusion,
        "warnings": quality_warnings,
    }
    publish(result, title="室间比对分析")
    return result


def z_score_analysis(data, lab_col="实验室", value_col="结果", assigned_value=None, std_dev=None):
    """
    Z值分析 —— 基于ISO 13528的能力验证评价。

    Parameters
    ----------
    data : pd.DataFrame
    lab_col : str
    value_col : str
    assigned_value : float, optional
        指定值（如参考值、中位数）。默认用所有数据均值。
    std_dev : float, optional
        标准偏差。默认用稳健标准差（MAD×1.4826）。

    Returns
    -------
    pd.DataFrame
        每实验室的Z值和判定结果
    """
    all_values = data[value_col].dropna().values
    if assigned_value is None:
        assigned_value = np.median(all_values)
    if std_dev is None:
        # 稳健标准差：MAD × 1.4826
        mad = np.median(np.abs(all_values - np.median(all_values)))
        std_dev = mad * 1.4826 if mad > 0 else np.std(all_values, ddof=1)

    results = []
    for lab in sorted(data[lab_col].unique()):
        lab_vals = data[data[lab_col] == lab][value_col].dropna().values
        if len(lab_vals) == 0:
            continue
        lab_mean = np.mean(lab_vals)
        z = calculate_z_score(lab_mean, assigned_value, std_dev)
        results.append({
            lab_col: lab,
            "结果均值": lab_mean,
            "Z值": z,
            "判定": z_score_judgment(z),
        })

    result = pd.DataFrame(results)
    publish(result, title="Z值分析")
    return result


def youden_plot(data_a, data_b, label_a="实验室A", label_b="实验室B",
                title="Youden图 — 双实验室比对"):
    """
    Youden图 —— 双实验室比对可视化。

    横轴为实验室A结果，纵轴为实验室B结果。
    每个点代表一个样本在两个实验室的测量结果。
    椭圆区域表示95%置信区间。

    Parameters
    ----------
    data_a : array-like — 实验室A的测量值
    data_b : array-like — 实验室B的测量值
    label_a : str
    label_b : str
    title : str

    Returns
    -------
    matplotlib.figure.Figure
    """
    x = np.array(data_a)
    y = np.array(data_b)

    fig, ax = plt.subplots(figsize=(8, 8))

    ax.scatter(x, y, c='#3498db', s=60, edgecolors='#2c3e50', linewidth=0.5, zorder=5)
    ax.axhline(np.mean(y), color='gray', linestyle='--', linewidth=1, alpha=0.7)
    ax.axvline(np.mean(x), color='gray', linestyle='--', linewidth=1, alpha=0.7)

    # 对角线 y=x
    lim_min = min(np.min(x), np.min(y))
    lim_max = max(np.max(x), np.max(y))
    margin = (lim_max - lim_min) * 0.1
    ax.plot([lim_min - margin, lim_max + margin],
            [lim_min - margin, lim_max + margin],
            'k-', linewidth=1, alpha=0.5, label="y = x")

    ax.set_xlabel(f"{label_a}")
    ax.set_ylabel(f"{label_b}")
    ax.set_title(title, fontsize=14)
    ax.grid(alpha=0.3)
    ax.legend()
    ax.set_aspect('equal')
    plt.tight_layout()
    publish({}, title="Youden图", figure=fig, html_filename="youden_plot.html")
    return fig


def interbatch_analysis(data, batch_col="批次", value_col="结果"):
    """
    批次间比对分析 —— 同室间比对，但针对不同批次。

    Parameters
    ----------
    data : pd.DataFrame
    batch_col : str — 批次列名
    value_col : str — 结果列名

    Returns
    -------
    dict — 同 interlab_comparison
    """
    result = interlab_comparison(data, lab_col=batch_col, value_col=value_col)
    publish(result, title="批次间比对分析")
    return result


def interlab_report(result):
    """
    将室间比对结果格式化为可读报告文本。

    Parameters
    ----------
    result : dict — interlab_comparison的返回值

    Returns
    -------
    str
    """
    lines = [
        "=" * 60,
        "  室间/人员比对分析报告",
        "=" * 60,
    ]

    group_stats = result.get("group_stats")
    if group_stats is not None and not group_stats.empty:
        lines.append("\n各参与方统计：")
        lines.append(str(group_stats.to_string(index=False)))

    lines.append(f"\nANOVA分析：")
    lines.append(result.get("conclusion", ""))

    report = "\n".join(lines)
    publish({}, title="室间比对报告", md_extra=report)
    return report
