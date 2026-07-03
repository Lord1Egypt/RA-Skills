"""
趋势监控（Trend Monitoring）

场景：对检测数据做长期趋势跟踪和风险预警。

核心流程：
1. 时间序列聚合与趋势分析
2. 滚动统计量与变动监测
3. Prophet时序预测（多品类/整体）
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from ..analysis.time_series import time_trend_analyze, trend_plot
from ..analysis.time_series import prophet_forecast, prophet_plot
from ..reporting import publish


def _warn_on_data_quality(data, date_col, value_col, min_rows=5):
    """数据质量前置校验：不阻断执行，只输出警告。"""
    warnings = []
    if data is None or data.empty:
        warnings.append("数据为空，无法分析。")
        return warnings
    if value_col not in data.columns:
        warnings.append(f"数值列 '{value_col}' 不存在。")
        return warnings
    if date_col not in data.columns:
        warnings.append(f"日期列 '{date_col}' 不存在。")
        return warnings
    vals = data[value_col].dropna()
    if len(vals) < min_rows:
        warnings.append(f"有效数据仅 {len(vals)} 行（建议至少 {min_rows} 行用于趋势分析）。")
    if len(vals) < len(data):
        warnings.append(f"数值列包含 {len(data) - len(vals)} 个空值，已自动跳过。")
    if vals.std() == 0:
        warnings.append("数值列所有值相同，趋势分析无意义。")
    # 检查日期范围
    try:
        dates = pd.to_datetime(data[date_col])
        if dates.nunique() < 3:
            warnings.append(f"日期列仅有 {dates.nunique()} 个不同日期，需要至少 3 个。")
    except Exception:
        warnings.append(f"日期列 '{date_col}' 无法解析为日期格式。")
    return warnings


def monitoring_dashboard(data, date_col="日期", value_col="值",
                         group_col=None, freq="W", window=7):
    """
    综合监控看板 —— 趋势、滚动统计、变化点检测。

    Parameters
    ----------
    data : pd.DataFrame
    date_col : str
    value_col : str
    group_col : str, optional
    freq : str — 聚合频率
    window : int — 滚动窗口大小

    Returns
    -------
    dict
        {
            "trend": 时序聚合结果,
            "trend_fig": 趋势图,
            "rolling_stats": 滚动统计,
            "stats_summary": 总体摘要,
        }
    """
    # 数据质量前置校验
    quality_warnings = _warn_on_data_quality(data, date_col, value_col)
    if quality_warnings:
        import warnings as _warn
        for w in quality_warnings:
            _warn.warn(f"[数据质量] {w}")
        print("⚠️  数据质量警告：")
        for w in quality_warnings:
            print(f"   • {w}")

    df = data.copy()
    df[date_col] = pd.to_datetime(df[date_col])

    # 时序聚合
    trend_result = time_trend_analyze(df, date_col, value_col, freq=freq)

    # 趋势图
    trend_fig = trend_plot(df, date_col, value_col, title="检测趋势监控")

    # 滚动统计
    df_sorted = df.sort_values(date_col)
    df_sorted["rolling_mean"] = df_sorted[value_col].rolling(window=window, min_periods=1).mean()
    df_sorted["rolling_std"] = df_sorted[value_col].rolling(window=window, min_periods=1).std()
    df_sorted["rolling_upper"] = df_sorted["rolling_mean"] + 2 * df_sorted["rolling_std"]
    df_sorted["rolling_lower"] = df_sorted["rolling_mean"] - 2 * df_sorted["rolling_std"]

    # 变化点检测：当前值超出±2σ范围
    recent = df_sorted.iloc[-1]
    alert = False
    if not pd.isna(recent["rolling_upper"]) and not pd.isna(recent["rolling_lower"]):
        alert = recent[value_col] > recent["rolling_upper"] or recent[value_col] < recent["rolling_lower"]

    summary = {
        "总记录数": len(df),
        "时间跨度": f"{df[date_col].min().date()} ~ {df[date_col].max().date()}",
        "总均值": df[value_col].mean(),
        "总标准差": df[value_col].std(ddof=1),
        "当前值": recent[value_col],
        "滚动均值": recent["rolling_mean"],
        "超出警戒": alert,
    }

    result = {
        "trend": trend_result,
        "trend_fig": trend_fig,
        "rolling_data": df_sorted,
        "stats_summary": summary,
        "warnings": quality_warnings,
    }
    publish(result, title="监控看板", figure=trend_fig, html_filename="monitoring_dashboard.html")
    return result


def forecast_alert(data, date_col="日期", value_col="值",
                   group_col=None, freq="W", periods=4, alert_threshold=0.2):
    """
    预测预警 —— 基于Prophet模型预测未来趋势并发出预警。

    Parameters
    ----------
    data : pd.DataFrame
    date_col : str
    value_col : str
    group_col : str, optional
    freq : str
    periods : int
    alert_threshold : float — 预警阈值（预测增长百分比）

    Returns
    -------
    dict
        {
            "forecast": 预测结果DataFrame,
            "forecast_fig": 预测图,
            "alerts": list — 预警信息
        }
    """
    if group_col:
        forecast_df, forecast_fig = prophet_forecast(data, date_col, value_col, group_col=group_col,
                                  periods=periods, freq=freq)
    else:
        forecast_df, forecast_fig = prophet_forecast(data, date_col, value_col, periods=periods, freq=freq)

    alerts = []
    if "组别" in forecast_df.columns:
        for group in forecast_df["组别"].unique():
            g = forecast_df[forecast_df["组别"] == group]
            recent = g[g["ds"] >= pd.Timestamp.today() - pd.Timedelta(days=30)]
            if len(recent) > 1:
                growth = (recent["yhat"].iloc[-1] - recent["yhat"].iloc[0]) / abs(recent["yhat"].iloc[0])
                if growth > alert_threshold:
                    alerts.append({
                        "组别": group,
                        "增长率": f"{growth:.1%}",
                        "预警": "上升过快，建议关注"
                    })
    else:
        recent = forecast_df[forecast_df["ds"] >= pd.Timestamp.today() - pd.Timedelta(days=30)]
        if len(recent) > 1:
            growth = (recent["yhat"].iloc[-1] - recent["yhat"].iloc[0]) / abs(recent["yhat"].iloc[0])
            if growth > alert_threshold:
                alerts.append({
                    "组别": "整体",
                    "增长率": f"{growth:.1%}",
                    "预警": "上升过快，建议关注"
                })

    result = {
        "forecast": forecast_df,
        "forecast_fig": forecast_fig,
        "alerts": alerts,
    }
    publish(result, title="预测预警", figure=forecast_fig, html_filename="forecast_alert.html")
    return result


def trend_report(trend_result, alert_result=None):
    """
    趋势监控报告文本。

    Parameters
    ----------
    trend_result : dict
    alert_result : dict, optional

    Returns
    -------
    str
    """
    lines = [
        "=" * 60,
        "  趋势监控报告",
        "=" * 60,
    ]

    summary = trend_result.get("stats_summary", {})
    if summary:
        for k, v in summary.items():
            lines.append(f"  {k}: {v}")

    if alert_result:
        alerts = alert_result.get("alerts", [])
        if alerts:
            lines.append("\n⚠️ 预警信息：")
            for a in alerts:
                lines.append(f"  [{a.get('组别', '')}] {a.get('预警', '')} (增长率: {a.get('增长率', '')})")
        else:
            lines.append("\n✅ 无预警，趋势正常。")

    report = "\n".join(lines)
    publish({}, title="趋势监控报告", md_extra=report)
    return report
