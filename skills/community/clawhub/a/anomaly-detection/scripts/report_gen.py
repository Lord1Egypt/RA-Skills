#!/usr/bin/env python3
"""
异常检测报告生成器
Usage: python report_gen.py --data anomaly_data.json --output report.html

从 anomaly_detect.py 输出的 JSON 数据生成交互式 HTML 可视化报告。
包含：异常概览、时序图标注、残差分析、异常类型分布、热力图、详细列表。
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path


def install_plotly():
    try:
        import plotly  # noqa
    except ImportError:
        import subprocess
        print("[INFO] 安装 plotly...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "plotly", "-q"])


install_plotly()

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def load_data(data_path: str) -> dict:
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)


def create_main_chart(data: dict) -> str:
    """创建主时序图：历史数据 + 预测值 + 异常标注"""
    ts = data["time_series"]
    anomalies = data["anomalies"]
    summary = data["summary"]

    df = pd.DataFrame(ts)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    anomaly_indices = set(a["index"] for a in anomalies)
    df_anomaly = df[df.index.isin(anomaly_indices)].copy()
    df_normal = df[~df.index.isin(anomaly_indices)].copy()

    fig = go.Figure()

    # 正常点
    fig.add_trace(go.Scatter(
        x=df_normal["timestamp"], y=df_normal["actual"],
        mode="lines", name="实际值",
        line=dict(color="#2C3E50", width=1.5),
        hovertemplate="%{x}<br>实际: %{y:,.2f}<extra></extra>",
    ))

    # 预测线
    fig.add_trace(go.Scatter(
        x=df["timestamp"], y=df["predicted"],
        mode="lines", name="Chronos-2 预测值",
        line=dict(color="#3498DB", width=1.2, dash="dash"),
        hovertemplate="%{x}<br>预测: %{y:,.2f}<extra></extra>",
    ))

    # 异常点 - 按严重级别分色
    severity_colors = {"P0_严重": "#E74C3C", "P1_警告": "#F39C12", "P2_轻微": "#3498DB"}
    severity_symbols = {"P0_严重": "x", "P1_警告": "diamond", "P2_轻微": "circle"}

    for sev in ["P0_严重", "P1_警告", "P2_轻微"]:
        sev_anomalies = [a for a in anomalies if a["severity"] == sev]
        if not sev_anomalies:
            continue
        sev_indices = set(a["index"] for a in sev_anomalies)
        sev_df = df[df.index.isin(sev_indices)]
        sev_label = {"P0_严重": "严重异常", "P1_警告": "警告异常", "P2_轻微": "轻微异常"}[sev]
        fig.add_trace(go.Scatter(
            x=sev_df["timestamp"], y=sev_df["actual"],
            mode="markers", name=sev_label,
            marker=dict(
                color=severity_colors[sev],
                size=10,
                symbol=severity_symbols[sev],
                line=dict(width=1.5, color="white"),
            ),
            hovertemplate=(
                "%{x}<br>实际: %{y:,.2f}<br>预测: %{customdata[0]:,.2f}"
                "<br>偏离: %{customdata[1]:.1f}%<br>Z-score: %{customdata[2]:.2f}"
                "<extra></extra>"
            ),
            customdata=[
                (sev_df["predicted"].values, 
                 (sev_df["actual"] / (sev_df["predicted"] + 1e-10) - 1) * 100,
                 df.loc[sev_df.index, "z_score"].values)
            ],
        ))

    fig.update_layout(
        title=dict(
            text="🔍 时序异常检测总览",
            font=dict(size=22, color="#2C3E50", family="Microsoft YaHei, sans-serif"),
        ),
        xaxis_title="时间",
        yaxis_title="数值",
        hovermode="closest",
        template="plotly_white",
        font=dict(family="Microsoft YaHei, sans-serif", size=13),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=60, r=30, t=80, b=60),
        height=500,
    )

    return fig.to_html(full_html=False, include_plotlyjs="cdn")


def create_residual_chart(data: dict) -> str:
    """创建残差分析图"""
    ts = data["time_series"]
    anomalies = data["anomalies"]

    df = pd.DataFrame(ts)
    anomaly_indices = set(a["index"] for a in anomalies)
    df["is_anomaly"] = df.index.isin(anomaly_indices)

    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.08,
        row_heights=[0.6, 0.4],
        subplot_titles=("残差时序", "残差分布直方图"),
    )

    # 残差时序
    normal_df = df[~df["is_anomaly"]]
    anomaly_df = df[df["is_anomaly"]]

    fig.add_trace(go.Scatter(
        x=normal_df["timestamp"], y=normal_df["residual"],
        mode="lines", name="正常残差",
        line=dict(color="#95A5A6", width=1),
    ), row=1, col=1)

    fig.add_trace(go.Scatter(
        x=anomaly_df["timestamp"], y=anomaly_df["residual"],
        mode="markers", name="异常残差",
        marker=dict(color="#E74C3C", size=8, symbol="x"),
    ), row=1, col=1)

    # 零线
    fig.add_hline(y=0, line_dash="dash", line_color="#BDC3C7", row=1, col=1)

    # 残差分布
    fig.add_trace(go.Histogram(
        x=df["residual"], nbinsx=min(50, len(df) // 2),
        name="残差分布",
        marker=dict(color="#3498DB", line=dict(color="white", width=1)),
    ), row=2, col=1)

    # 标注异常区域
    residuals = np.array(df["residual"])
    mean_r = np.mean(residuals)
    std_r = np.std(residuals)
    for level, color, label in [(2, "#F39C12", "±2σ"), (3, "#E74C3C", "±3σ")]:
        fig.add_vline(x=mean_r + level * std_r, line_dash="dot",
                      line_color=color, row=2, col=1, opacity=0.5)
        fig.add_vline(x=mean_r - level * std_r, line_dash="dot",
                      line_color=color, row=2, col=1, opacity=0.5)

    fig.update_layout(
        template="plotly_white",
        font=dict(family="Microsoft YaHei, sans-serif", size=12),
        showlegend=False,
        height=500,
        margin=dict(l=60, r=30, t=70, b=60),
    )
    fig.update_xaxes(title_text="时间", row=1, col=1)
    fig.update_yaxes(title_text="残差", row=1, col=1)
    fig.update_xaxes(title_text="残差值", row=2, col=1)
    fig.update_yaxes(title_text="频次", row=2, col=1)

    return fig.to_html(full_html=False, include_plotlyjs=False)


def create_type_distribution_chart(data: dict) -> str:
    """创建异常类型分布图"""
    anomalies = data["anomalies"]
    if not anomalies:
        return ""

    df_a = pd.DataFrame(anomalies)

    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{"type": "pie"}, {"type": "bar"}]],
        subplot_titles=("异常严重度分布", "异常类型分布"),
    )

    # 严重度饼图
    sev_counts = df_a["severity"].value_counts()
    sev_labels_map = {"P0_严重": "严重(P0)", "P1_警告": "警告(P1)", "P2_轻微": "轻微(P2)"}
    sev_colors = {"P0_严重": "#E74C3C", "P1_警告": "#F39C12", "P2_轻微": "#3498DB"}
    
    fig.add_trace(go.Pie(
        labels=[sev_labels_map.get(k, k) for k in sev_counts.index],
        values=sev_counts.values,
        marker=dict(colors=[sev_colors.get(k, "#95A5A6") for k in sev_counts.index]),
        hole=0.4,
        textinfo="label+percent",
    ), row=1, col=1)

    # 类型柱状图
    type_counts = df_a["type"].value_counts()
    type_names = {"point": "点异常", "contextual": "上下文异常", "collective": "集体异常", "level_shift": "水平偏移"}
    type_colors = {"point": "#3498DB", "contextual": "#9B59B6", "collective": "#E74C3C", "level_shift": "#F39C12"}

    fig.add_trace(go.Bar(
        x=[type_names.get(k, k) for k in type_counts.index],
        y=type_counts.values,
        marker=dict(color=[type_colors.get(k, "#95A5A6") for k in type_counts.index]),
        text=type_counts.values,
        textposition="outside",
    ), row=1, col=2)

    fig.update_layout(
        template="plotly_white",
        font=dict(family="Microsoft YaHei, sans-serif", size=12),
        height=400,
        margin=dict(l=60, r=30, t=70, b=60),
    )

    return fig.to_html(full_html=False, include_plotlyjs=False)


def create_anomaly_heatmap(data: dict) -> str:
    """创建异常时段热力图"""
    anomalies = data["anomalies"]
    if not anomalies:
        return ""

    df_a = pd.DataFrame(anomalies)
    df_a["timestamp"] = pd.to_datetime(df_a["timestamp"])
    df_a["hour"] = df_a["timestamp"].dt.hour
    df_a["date"] = df_a["timestamp"].dt.date.astype(str)

    # 按日期和小时聚合
    pivot = df_a.pivot_table(
        index="hour", columns="date", values="index",
        aggfunc="count", fill_value=0
    )

    if pivot.empty:
        return ""

    fig = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=list(pivot.columns),
        y=list(pivot.index),
        colorscale=[
            [0, "#FFFFFF"], [0.25, "#3498DB"], [0.5, "#F39C12"],
            [0.75, "#E67E22"], [1, "#E74C3C"]
        ],
        hovertemplate="日期: %{x}<br>时段: %{y}时<br>异常数: %{z}<extra></extra>",
    ))

    fig.update_layout(
        title=dict(
            text="📅 异常时段热力图",
            font=dict(size=16, color="#2C3E50", family="Microsoft YaHei, sans-serif"),
        ),
        xaxis_title="日期",
        yaxis_title="小时",
        template="plotly_white",
        font=dict(family="Microsoft YaHei, sans-serif", size=12),
        height=350,
        margin=dict(l=60, r=30, t=60, b=60),
    )

    return fig.to_html(full_html=False, include_plotlyjs=False)


def generate_html(data: dict, output_path: str):
    """生成完整的交互式 HTML 报告"""
    summary = data["summary"]
    anomalies = data["anomalies"]
    metadata = data.get("metadata", {})

    # 生成各图表
    main_chart_html = create_main_chart(data)
    residual_chart_html = create_residual_chart(data)
    type_chart_html = create_type_distribution_chart(data)
    heatmap_html = create_anomaly_heatmap(data)

    # 计算统计摘要
    s = summary
    sev = s["severity_breakdown"]
    rs = s["residual_stats"]

    # 异常详情表
    anomaly_rows = ""
    if anomalies:
        for a in anomalies[:100]:  # 限制显示前100条
            sev_badge_class = {"P0_严重": "badge-danger", "P1_警告": "badge-warning", "P2_轻微": "badge-info"}
            type_name = {"point": "点", "contextual": "上下文", "collective": "集体", "level_shift": "水平偏移"}
            direct_icon = "↑" if a["direction"] == "偏高" else "↓"
            direct_class = "up" if a["direction"] == "偏高" else "down"
            anomaly_rows += f"""
            <tr>
                <td>{a["timestamp"][:19]}</td>
                <td>{a["actual"]:,.2f}</td>
                <td>{a["predicted"]:,.2f}</td>
                <td class="direction-{direct_class}">{direct_icon} {abs(a["residual_pct"]):.1f}%</td>
                <td>{a["z_score"]:.1f}σ</td>
                <td><span class="badge {sev_badge_class.get(a['severity'], 'badge-info')}">{a["severity"]}</span></td>
                <td>{type_name.get(a["type"], a["type"])}</td>
                <td>{a["vote_count"]}/4 方法确认</td>
            </tr>"""

    if len(anomalies) > 100:
        anomaly_rows += f'<tr><td colspan="8" style="text-align:center;color:#7F8C8D">... 还有 {len(anomalies) - 100} 条异常，完整数据见 anomalies.csv</td></tr>'

    no_anomaly_row = ""
    if not anomalies:
        no_anomaly_row = '<tr><td colspan="8" style="text-align:center;color:#27AE60;padding:40px">✅ 未检测到异常，数据表现正常</td></tr>'

    # 严重度卡 CSS class
    sev_status = "danger" if sev["P0_严重"] > 0 else ("warning" if sev["P1_警告"] > 0 else "success")
    overall_status = {"danger": "⚠️ 存在严重异常", "warning": "⚡ 存在警告异常", "success": "✅ 数据表现正常"}[sev_status]

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>时序异常检测报告 - Chronos-2</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Microsoft YaHei", "PingFang SC", sans-serif;
            background: #F0F2F5;
            min-height: 100vh;
            color: #2C3E50;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 24px 20px;
        }}

        /* Header */
        .header {{
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            border-radius: 20px;
            padding: 40px 36px;
            margin-bottom: 24px;
            color: white;
            position: relative;
            overflow: hidden;
        }}
        .header::before {{
            content: "";
            position: absolute;
            top: -50%;
            right: -20%;
            width: 60%;
            height: 200%;
            background: radial-gradient(circle, rgba(231,76,60,0.08) 0%, transparent 70%);
        }}
        .header h1 {{
            font-size: 2.2em;
            font-weight: 800;
            margin-bottom: 6px;
            position: relative;
        }}
        .header .subtitle {{
            font-size: 1.05em;
            opacity: 0.8;
            position: relative;
        }}
        .header-meta {{
            display: flex;
            gap: 16px;
            flex-wrap: wrap;
            margin-top: 16px;
            position: relative;
        }}
        .header-badge {{
            background: rgba(255,255,255,0.12);
            border: 1px solid rgba(255,255,255,0.2);
            padding: 5px 14px;
            border-radius: 20px;
            font-size: 0.85em;
        }}

        /* Status Banner */
        .status-banner {{
            padding: 20px 28px;
            border-radius: 16px;
            margin-bottom: 24px;
            font-size: 1.1em;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        .status-banner.danger {{ background: #FDF0ED; color: #C0392B; border: 1px solid #F5C6CB; }}
        .status-banner.warning {{ background: #FFF8E1; color: #E67E22; border: 1px solid #FFE082; }}
        .status-banner.success {{ background: #E8F8F5; color: #27AE60; border: 1px solid #A3E4D7; }}

        /* Stats Grid */
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(145px, 1fr));
            gap: 14px;
            margin-bottom: 24px;
        }}
        .stat-card {{
            background: white;
            border-radius: 14px;
            padding: 20px 22px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.06);
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .stat-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }}
        .stat-card .label {{
            font-size: 0.82em;
            color: #7F8C8D;
            margin-bottom: 6px;
            font-weight: 500;
        }}
        .stat-card .value {{
            font-size: 1.7em;
            font-weight: 800;
            color: #2C3E50;
        }}
        .stat-card .value.danger {{ color: #E74C3C; }}
        .stat-card .value.warning {{ color: #F39C12; }}
        .stat-card .value.success {{ color: #27AE60; }}

        /* Chart Container */
        .chart-container {{
            background: white;
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        }}
        .chart-container .section-title {{
            font-size: 1.1em;
            font-weight: 700;
            color: #2C3E50;
            margin-bottom: 8px;
            padding-bottom: 12px;
            border-bottom: 2px solid #F0F2F5;
        }}

        /* Anomaly Table */
        .anomaly-table-wrap {{
            overflow-x: auto;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.92em;
        }}
        thead th {{
            background: #F8F9FA;
            padding: 12px 14px;
            text-align: left;
            font-weight: 700;
            color: #555;
            border-bottom: 2px solid #E9ECEF;
            white-space: nowrap;
            position: sticky;
            top: 0;
        }}
        tbody td {{
            padding: 10px 14px;
            border-bottom: 1px solid #F0F2F5;
            white-space: nowrap;
        }}
        tbody tr:hover {{
            background: #F8F9FF;
        }}

        .badge {{
            display: inline-block;
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 0.82em;
            font-weight: 600;
        }}
        .badge-danger {{ background: #FDF0ED; color: #C0392B; }}
        .badge-warning {{ background: #FFF8E1; color: #E67E22; }}
        .badge-info {{ background: #EBF5FB; color: #2980B9; }}

        .direction-up {{ color: #E74C3C; font-weight: 600; }}
        .direction-down {{ color: #27AE60; font-weight: 600; }}

        /* Method Cards */
        .method-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 14px;
            margin-bottom: 20px;
        }}
        .method-card {{
            background: white;
            border-radius: 12px;
            padding: 16px 18px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            border-left: 4px solid #3498DB;
        }}
        .method-card h4 {{
            font-size: 0.95em;
            color: #2C3E50;
            margin-bottom: 6px;
        }}
        .method-card p {{
            font-size: 0.82em;
            color: #7F8C8D;
            line-height: 1.5;
        }}

        /* Section */
        .section-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 16px;
        }}
        .section-header h2 {{
            font-size: 1.3em;
            color: #2C3E50;
        }}
        .section-count {{
            font-size: 0.9em;
            color: #7F8C8D;
        }}

        /* Footer */
        .footer {{
            text-align: center;
            padding: 30px;
            color: #95A5A6;
            font-size: 0.85em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>🔍 时序异常检测报告</h1>
            <p class="subtitle">基于 Amazon Chronos-2 零样本时序大模型 + 多方法融合检测</p>
            <div class="header-meta">
                <span class="header-badge">模型: {metadata.get("model", "amazon/chronos-2")}</span>
                <span class="header-badge">数据点: {s["total_points"]}</span>
                <span class="header-badge">异常点: {s["anomaly_count"]} ({s["anomaly_rate"]}%)</span>
                <span class="header-badge">检测时间: {s["detection_time"]}</span>
            </div>
        </div>

        <!-- Status Banner -->
        <div class="status-banner {sev_status}">
            <span style="font-size:1.5em">{overall_status.split(' ')[0]}</span>
            <span>{overall_status}</span>
        </div>

        <!-- Key Stats -->
        <div class="stats-grid">
            <div class="stat-card">
                <div class="label">📊 总数据点</div>
                <div class="value">{s["total_points"]}</div>
            </div>
            <div class="stat-card">
                <div class="label">🚨 异常点数</div>
                <div class="value {'danger' if s['anomaly_count'] > s['total_points'] * 0.1 else 'warning' if s['anomaly_count'] > 0 else 'success'}">{s["anomaly_count"]}</div>
            </div>
            <div class="stat-card">
                <div class="label">📈 异常率</div>
                <div class="value {'danger' if s['anomaly_rate'] > 10 else 'warning' if s['anomaly_rate'] > 5 else ''}">{s["anomaly_rate"]}%</div>
            </div>
            <div class="stat-card">
                <div class="label">🔴 严重(P0)</div>
                <div class="value {'danger' if sev['P0_严重'] > 0 else ''}">{sev["P0_严重"]}</div>
            </div>
            <div class="stat-card">
                <div class="label">🟡 警告(P1)</div>
                <div class="value {'warning' if sev['P1_警告'] > 0 else ''}">{sev["P1_警告"]}</div>
            </div>
            <div class="stat-card">
                <div class="label">🔵 轻微(P2)</div>
                <div class="value">{sev["P2_轻微"]}</div>
            </div>
            <div class="stat-card">
                <div class="label">📐 残差 MAE</div>
                <div class="value">{rs["mae"]:.3f}</div>
            </div>
            <div class="stat-card">
                <div class="label">📏 残差 RMSE</div>
                <div class="value">{rs["rmse"]:.3f}</div>
            </div>
        </div>

        <!-- Detection Methods -->
        <div class="method-grid">
            <div class="method-card" style="border-left-color:#3498DB">
                <h4>📏 Z-Score 检测</h4>
                <p>基于均值与标准差，检测偏离 &gt;{s["methods_used"]["zscore_threshold"]}σ 的数据点</p>
            </div>
            <div class="method-card" style="border-left-color:#9B59B6">
                <h4>📐 改进 Z-Score (MAD)</h4>
                <p>基于中位数绝对偏差，对离群值更鲁棒，阈值 {s["methods_used"]["mad_threshold"]}</p>
            </div>
            <div class="method-card" style="border-left-color:#27AE60">
                <h4>📦 IQR 四分位距</h4>
                <p>检测超出 Q1-{s["methods_used"]["iqr_multiplier"]}×IQR ~ Q3+{s["methods_used"]["iqr_multiplier"]}×IQR 范围的点</p>
            </div>
            <div class="method-card" style="border-left-color:#F39C12">
                <h4>📈 移动平均偏离</h4>
                <p>检测偏离局部移动平均窗口的数据点，识别趋势突变</p>
            </div>
        </div>

        <!-- Main Chart -->
        <div class="chart-container">
            <div class="section-header">
                <h2>📈 时序异常检测总览</h2>
                <span class="section-count">异常点已用标记高亮</span>
            </div>
            {main_chart_html}
        </div>

        <!-- Residual Analysis -->
        <div class="chart-container">
            <div class="section-header">
                <h2>📉 残差分析</h2>
                <span class="section-count">实际值 - Chronos-2预测值</span>
            </div>
            {residual_chart_html}
        </div>

        <!-- Type Distribution -->
        <div class="chart-container">
            <div class="section-header">
                <h2>📊 异常分类分布</h2>
                <span class="section-count">严重度 & 类型统计</span>
            </div>
            {type_chart_html}
        </div>

        <!-- Heatmap -->
        {f'<div class="chart-container"><div class="section-header"><h2>🗺️ 异常时段热力图</h2><span class="section-count">按日期×时段聚合</span></div>{heatmap_html}</div>' if heatmap_html else ''}

        <!-- Anomaly Detail Table -->
        <div class="chart-container">
            <div class="section-header">
                <h2>📋 异常明细列表</h2>
                <span class="section-count">共 {s["anomaly_count"]} 条异常记录</span>
            </div>
            <div class="anomaly-table-wrap">
                <table>
                    <thead>
                        <tr>
                            <th>时间</th>
                            <th>实际值</th>
                            <th>预测值</th>
                            <th>偏离度</th>
                            <th>Z-Score</th>
                            <th>严重级别</th>
                            <th>异常类型</th>
                            <th>确认方法</th>
                        </tr>
                    </thead>
                    <tbody>
                        {anomaly_rows}
                        {no_anomaly_row}
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Footer -->
        <div class="footer">
            <p>Powered by Amazon Chronos-2 · Multi-Method Anomaly Detection Engine</p>
            <p>检测方法: Z-Score | 改进Z-Score(MAD) | IQR | 移动平均偏离 | 融合策略: 4选2多数投票</p>
            <p>Generated at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        </div>
    </div>
</body>
</html>"""

    output = Path(output_path)
    output.write_text(html, encoding="utf-8")
    print(f"[INFO] HTML 报告已生成: {output}")
    return str(output)


def main():
    parser = argparse.ArgumentParser(description="异常检测报告生成器")
    parser.add_argument("--data", "-d", required=True, help="anomaly_data.json 路径")
    parser.add_argument("--output", "-o", required=True, help="输出 HTML 文件路径")
    args = parser.parse_args()

    data = load_data(args.data)
    report_path = generate_html(data, args.output)
    print(f"\n✅ 报告已生成: {report_path}")


if __name__ == "__main__":
    main()
