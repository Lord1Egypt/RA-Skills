"""
分组统计分析模块

通用功能：按类别分组 → 计算指标 → 可视化 → 结论生成。
不绑定任何特定领域。
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io


def group_analyze(df, group_col, metric_col=None, agg_funcs=None):
    """
    通用分组分析。
    
    Parameters
    ----------
    df : pd.DataFrame
    group_col : str
        分组列名（如品种、批次、地区等任何类别字段）
    metric_col : str, optional
        计算指标使用的列
    agg_funcs : dict or list, optional
        聚合函数，默认 {"count", "mean", "std", "min", "max"}
    
    Returns
    -------
    pd.DataFrame
        分组统计结果
    """
    if agg_funcs is None:
        if metric_col:
            agg_funcs = {metric_col: ["count", "mean", "std", "min", "max"]}
        else:
            # 默认统计每组数量
            result = df.groupby(group_col, as_index=False).size().rename(columns={"size": "计数"})
            return result

    result = df.groupby(group_col, as_index=False).agg(agg_funcs)

    # 摊平多层列名
    if isinstance(result.columns, pd.MultiIndex):
        result.columns = [f"{col[0]}_{col[1]}" if col[1] else col[0] for col in result.columns]
        # 重命名为更直观的名字
        rename_map = {}
        for c in result.columns:
            if c.endswith("_count"):
                rename_map[c] = "计数"
            elif c.endswith("_mean"):
                rename_map[c] = "均值"
            elif c.endswith("_std"):
                rename_map[c] = "标准差"
            elif c.endswith("_min"):
                rename_map[c] = "最小值"
            elif c.endswith("_max"):
                rename_map[c] = "最大值"
        result = result.rename(columns=rename_map)
    
    return result


def group_rate_analysis(df, group_col, result_col, positive_val, value_col=None):
    """
    率指标分析（如阳性率、合格率、通过率等）。
    
    Parameters
    ----------
    df : pd.DataFrame
    group_col : str
        分组列
    result_col : str
        结果列（二分类）
    positive_val : str or int or float
        视为"正例"的值
    value_col : str, optional
        用于聚合的数值列
    
    Returns
    -------
    pd.DataFrame
        含阳性数、总数、阳性率等指标
    """
    analysis = df.groupby(group_col).agg(
        总数=(result_col, "count"),
        正例数=(result_col, lambda x: (x == positive_val).sum())
    ).reset_index()
    
    analysis["率"] = analysis["正例数"] / analysis["总数"]
    
    if value_col:
        value_stats = df.groupby(group_col)[value_col].agg(["mean", "std", "min", "max"]).reset_index()
        analysis = analysis.merge(value_stats, on=group_col)
    
    return analysis


def group_compare_plot(result_df, group_col, value_col, title="分组对比", plot_type="bar"):
    """
    分组对比可视化。
    
    Parameters
    ----------
    result_df : pd.DataFrame
    group_col : str
        分组列名
    value_col : str
        数值列名
    title : str
        图表标题
    plot_type : str
        "bar" | "pie"
    
    Returns
    -------
    matplotlib.figure.Figure
    """
    fig, ax = plt.subplots(figsize=(10, 5))
    
    if plot_type == "bar":
        colors = plt.cm.Set2(np.linspace(0, 1, len(result_df)))
        bars = ax.bar(result_df[group_col], result_df[value_col], color=colors, edgecolor='gray')
        ax.set_ylabel(value_col)
        
        # 数据标签
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.2%}' if height <= 1 else f'{height:.2f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        ha='center', va='bottom', fontsize=9)
        
    elif plot_type == "pie":
        colors = plt.cm.Pastel1(np.linspace(0, 1, len(result_df)))
        ax.pie(result_df[value_col], labels=result_df[group_col], autopct='%1.1f%%',
               colors=colors, startangle=90)
    
    ax.set_title(title, pad=15)
    plt.tight_layout()
    return fig


def generate_conclusion(result_df, group_col, value_col, higher_is_riskier=True):
    """
    自动生成分析结论文本。
    
    Parameters
    ----------
    result_df : pd.DataFrame
    group_col : str
    value_col : str
    higher_is_riskier : bool
        True=值越高越需要关注, False=值越低越需要关注
    
    Returns
    -------
    str
    """
    max_row = result_df.loc[result_df[value_col].idxmax()]
    min_row = result_df.loc[result_df[value_col].idxmin()]
    avg_val = result_df[value_col].mean()
    
    top = max_row[group_col] if higher_is_riskier else min_row[group_col]
    bottom = min_row[group_col] if higher_is_riskier else max_row[group_col]
    
    lines = [
        "【分组分析结论】",
        f"• 最高组: {top} ({max_row[value_col]:.2% if max_row[value_col] <= 1 else max_row[value_col]:.2f}), "
        f"偏离均值 {(max_row[value_col] - avg_val) / avg_val * 100:+.1f}%",
        f"• 最低组: {bottom} ({min_row[value_col]:.2% if min_row[value_col] <= 1 else min_row[value_col]:.2f}), "
        f"偏离均值 {(min_row[value_col] - avg_val) / avg_val * 100:+.1f}%",
        f"• 整体均值: {avg_val:.4f}, 标准差: {result_df[value_col].std():.4f}",
        f"• 离散系数: {result_df[value_col].std() / avg_val:.2f} — {'差异显著' if result_df[value_col].std() / avg_val > 0.5 else '差异一般'}",
    ]
    return "\n".join(lines)
