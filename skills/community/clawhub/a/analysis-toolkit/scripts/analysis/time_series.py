"""
时序趋势分析与预测模块

通用功能：时间序列聚合 → 趋势图 → 滚动统计 → Prophet预测。
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def time_trend_analyze(df, date_col, value_col, freq="D"):
    """
    时序聚合统计。
    
    Parameters
    ----------
    df : pd.DataFrame
    date_col : str
        日期列
    value_col : str
        待聚合的数值列
    freq : str
        频率: "D"=日, "W"=周, "M"=月, "Q"=季度
    
    Returns
    -------
    pd.DataFrame
        聚合后的时序数据
    """
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    
    ts = df.set_index(date_col).resample(freq)[value_col].agg(["sum", "mean", "std", "count"]).reset_index()
    ts.columns = [date_col, "总值", "均值", "标准差", "计数"]
    ts = ts.dropna(subset=["总值"])
    
    return ts


def trend_plot(ts_data, date_col, value_col, title="时序趋势图"):
    """
    绘制趋势线。
    
    Parameters
    ----------
    ts_data : pd.DataFrame
    date_col : str
    value_col : str
    title : str
    
    Returns
    -------
    matplotlib.figure.Figure
    """
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(ts_data[date_col], ts_data[value_col], marker='o', 
            color='#2c3e50', linewidth=2, markersize=6, markerfacecolor='#e74c3c')
    ax.set_title(title, fontsize=14)
    ax.set_xlabel("时间")
    ax.set_ylabel(value_col)
    ax.grid(linestyle='--', alpha=0.6)
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig


def rolling_stats(ts_data, date_col, value_col, window=7):
    """
    滚动统计量（滚动均值、标准差）。
    
    Parameters
    ----------
    ts_data : pd.DataFrame
    date_col : str
    value_col : str
    window : int
        滚动窗口大小
    
    Returns
    -------
    pd.DataFrame
        含滚动统计列的DataFrame
    """
    df = ts_data.sort_values(date_col).copy()
    df["滚动均值"] = df[value_col].rolling(window=window, min_periods=1).mean()
    df["滚动标准差"] = df[value_col].rolling(window=window, min_periods=1).std()
    df["上限"] = df["滚动均值"] + 1.96 * df["滚动标准差"]
    df["下限"] = df["滚动均值"] - 1.96 * df["滚动标准差"]
    return df


def trend_conclusion(ts_data, value_col, recent_n=7):
    """
    自动生成趋势解读。
    
    Parameters
    ----------
    ts_data : pd.DataFrame
    value_col : str
    recent_n : int
        近期窗口
    
    Returns
    -------
    str
    """
    recent = ts_data.iloc[-recent_n:]
    avg = recent[value_col].mean()
    change = recent[value_col].diff().mean()
    cv = recent[value_col].std() / avg if avg != 0 else 0
    
    status = "预警" if avg > ts_data[value_col].mean() * 1.2 else "正常"
    suggestion = "提高监测频率" if avg > ts_data[value_col].mean() * 1.2 else "保持现有频率"
    
    return (
        "【趋势解读】\n"
        f"• 近{recent_n}期均值: {avg:.2f}, 环比变化: {change:+.2f}/期\n"
        f"• 波动率: {cv:.1%}\n"
        f"• 当前趋势: {status}, 建议: {suggestion}"
    )


def prophet_forecast(df, date_col, value_col, group_col=None, periods=4, freq="W"):
    """
    基于Prophet的时序预测。
    
    Parameters
    ----------
    df : pd.DataFrame
    date_col : str
    value_col : str
    group_col : str, optional
        分组列（如品种、项目），不指定则做整体预测
    periods : int
        预测期数
    freq : str
        "W"=周, "M"=月, "Q"=季度
    
    Returns
    -------
    pd.DataFrame
        预测结果（含ds, yhat, yhat_lower, yhat_upper）
    matplotlib.figure.Figure or None
    """
    try:
        from prophet import Prophet
    except ImportError:
        raise ImportError("需要安装 prophet: pip install prophet")
    
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    
    if group_col and group_col in df.columns:
        forecasts = []
        fig = plt.figure(figsize=(12, 3 * df[group_col].nunique()))
        colors = plt.cm.Set3(np.linspace(0, 1, df[group_col].nunique()))
        
        for idx, (group_name, group) in enumerate(df.groupby(group_col)):
            ts = group.set_index(date_col).resample(freq)[value_col].mean().reset_index()
            ts.columns = ["ds", "y"]
            ts = ts.dropna()
            
            if len(ts) < 3:
                continue
            
            model = Prophet(interval_width=0.95, yearly_seasonality=True,
                            weekly_seasonality=(freq == "W"), daily_seasonality=False)
            
            if freq == "Q":
                model.add_seasonality(name="quarterly", period=91.25, fourier_order=5)
            
            model.fit(ts)
            future = model.make_future_dataframe(periods=periods, freq=freq)
            forecast = model.predict(future)
            forecast[group_col] = group_name
            
            forecasts.append(forecast[["ds", "yhat", "yhat_lower", "yhat_upper", group_col]])
            
            # 子图
            ax = fig.add_subplot(df[group_col].nunique(), 1, idx + 1)
            ax.plot(forecast["ds"], forecast["yhat"], color=colors[idx], linestyle='--', label="预测值")
            ax.fill_between(forecast["ds"], forecast["yhat_lower"], forecast["yhat_upper"],
                            color=colors[idx], alpha=0.2)
            ax.scatter(ts["ds"], ts["y"], color=colors[idx], label="历史数据", s=20)
            ax.set_title(f"{group_name} 预测")
            ax.legend()
            ax.grid(alpha=0.3)
        
        plt.tight_layout()
        return pd.concat(forecasts) if forecasts else pd.DataFrame(), fig if forecasts else None
    
    else:
        # 整体预测
        ts = df.set_index(date_col).resample(freq)[value_col].mean().reset_index()
        ts.columns = ["ds", "y"]
        ts = ts.dropna()
        
        if len(ts) < 3:
            raise ValueError(
                f"数据不足，无法进行 Prophet 预测。\n"
                f"当前有效时间点: {len(ts)} 个（至少需要 3 个）\n"
                "可能原因：① 数据量不够，历史记录太少\n"
                "         ② 按所选频率聚合后有效数据不足\n"
                "         ③ 数据中有过多的空值（NaN）被过滤掉了\n"
                "建议：① 补充更多历史数据\n"
                "      ② 换用更粗的频率（如从'日'改为'周'）\n"
                "      ③ 检查数据是否包含有效日期列"
            )
        
        model = Prophet(interval_width=0.95, yearly_seasonality=True,
                        weekly_seasonality=(freq == "W"), daily_seasonality=False)
        
        if freq == "Q":
            model.add_seasonality(name="quarterly", period=91.25, fourier_order=5)
        
        model.fit(ts)
        future = model.make_future_dataframe(periods=periods, freq=freq)
        forecast = model.predict(future)
        
        fig, ax = plt.subplots(figsize=(12, 5))
        model.plot(forecast, ax=ax)
        ax.set_title("时序预测")
        ax.fill_between(forecast["ds"], forecast["yhat_lower"], forecast["yhat_upper"],
                        alpha=0.2, color="#3498db")
        
        return forecast, fig


def prophet_plot(forecast, history=None, title=""):
    """
    预测结果可视化。
    
    Parameters
    ----------
    forecast : pd.DataFrame
        预测结果（含ds, yhat, yhat_lower, yhat_upper）
    history : pd.DataFrame, optional
        历史数据（含ds, y）
    title : str
    
    Returns
    -------
    matplotlib.figure.Figure
    """
    fig, ax = plt.subplots(figsize=(12, 5))
    
    ax.plot(forecast["ds"], forecast["yhat"], color="#e74c3c", linewidth=2, label="预测值")
    ax.fill_between(forecast["ds"], forecast["yhat_lower"], forecast["yhat_upper"],
                    color="#e74c3c", alpha=0.15, label="95%置信区间")
    
    if history is not None:
        ax.scatter(history["ds"], history["y"], color="#2c3e50", s=30, label="历史数据", zorder=5)
    
    ax.set_title(title or "预测结果")
    ax.legend()
    ax.grid(alpha=0.3)
    plt.tight_layout()
    return fig
