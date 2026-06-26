"""图表生成模块 - 支持多种图表类型"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
import pandas as pd
import numpy as np
from pathlib import Path
import uuid

# 中文字体配置
plt.rcParams['font.sans-serif'] = ['SimHei', 'WenQuanYi Micro Hei', 'Heiti TC', 'Arial Unicode MS', 'Noto Sans CJK SC']
plt.rcParams['axes.unicode_minus'] = False

CHART_COLORS = ['#4A90E2', '#50C878', '#FF6B6B', '#FFD93D', '#6BCB77', '#4D96FF', '#FF922B']


def _ensure_font():
    """确保中文字体可用"""
    fonts = font_manager.findSystemFonts()
    if not fonts:
        matplotlib.rcParams['font.family'] = 'DejaVu Sans'
    else:
        matplotlib.rcParams['font.family'] = 'sans-serif'


def generate_chart(df: pd.DataFrame, column: str, chart_type: str, output_dir: str = None) -> str:
    """生成图表并保存为图片

    Args:
        df: 数据框
        column: 列名（用于图表数据）
        chart_type: 图表类型 ('line', 'bar', 'pie', 'scatter')
        output_dir: 输出目录，默认为 None（使用系统临时目录）

    Returns:
        str: 保存的图片路径
    """
    _ensure_font()

    if output_dir is None:
        output_dir = Path('/tmp/auto_report_charts')
    else:
        output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if column not in df.columns:
        raise ValueError(f"列 '{column}' 不存在于数据框中")

    fig, ax = plt.subplots(figsize=(10, 6))

    if chart_type == 'line':
        _plot_line(df, column, ax)
    elif chart_type == 'bar':
        _plot_bar(df, column, ax)
    elif chart_type == 'pie':
        _plot_pie(df, column, ax)
    elif chart_type == 'scatter':
        _plot_scatter(df, column, ax)
    else:
        raise ValueError(f"不支持的图表类型: {chart_type}，支持: line, bar, pie, scatter")

    plt.tight_layout()

    filename = f"{chart_type}_{column}_{uuid.uuid4().hex[:8]}.png"
    filepath = output_dir / filename
    plt.savefig(filepath, dpi=150, bbox_inches='tight')
    plt.close()

    return str(filepath)


def _plot_line(df: pd.DataFrame, column: str, ax):
    """绘制折线图"""
    numeric_data = df[column].dropna()
    ax.plot(numeric_data.reset_index(drop=True), color=CHART_COLORS[0], linewidth=2, marker='o', markersize=4)
    ax.set_title(f'{column} 趋势图', fontsize=14, fontweight='bold')
    ax.set_xlabel('序号', fontsize=11)
    ax.set_ylabel(column, fontsize=11)
    ax.grid(True, alpha=0.3)


def _plot_bar(df: pd.DataFrame, column: str, ax):
    """绘制柱状图"""
    value_counts = df[column].value_counts().head(20)
    colors = CHART_COLORS[:len(value_counts)]
    bars = ax.bar(range(len(value_counts)), value_counts.values, color=colors)
    ax.set_xticks(range(len(value_counts)))
    ax.set_xticklabels(value_counts.index, rotation=45, ha='right', fontsize=9)
    ax.set_title(f'{column} 分布图', fontsize=14, fontweight='bold')
    ax.set_ylabel('数量', fontsize=11)
    ax.grid(axis='y', alpha=0.3)


def _plot_pie(df: pd.DataFrame, column: str, ax):
    """绘制饼图"""
    value_counts = df[column].value_counts().head(8)
    colors = CHART_COLORS[:len(value_counts)]
    wedges, texts, autotexts = ax.pie(
        value_counts.values,
        labels=value_counts.index,
        colors=colors,
        autopct='%1.1f%%',
        startangle=90
    )
    ax.set_title(f'{column} 占比图', fontsize=14, fontweight='bold')


def _plot_scatter(df: pd.DataFrame, column: str, ax):
    """绘制散点图"""
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if len(numeric_cols) < 2:
        raise ValueError("散点图需要至少两个数值列")

    other_col = numeric_cols[0] if numeric_cols[0] != column else numeric_cols[1]
    ax.scatter(df[other_col], df[column], alpha=0.6, color=CHART_COLORS[0], s=30)
    ax.set_title(f'{column} vs {other_col}', fontsize=14, fontweight='bold')
    ax.set_xlabel(other_col, fontsize=11)
    ax.set_ylabel(column, fontsize=11)
    ax.grid(True, alpha=0.3)


def generate_histogram(df: pd.DataFrame, column: str, bins: int = 30, output_dir: str = None) -> str:
    """生成直方图"""
    _ensure_font()

    if output_dir is None:
        output_dir = Path('/tmp/auto_report_charts')
    else:
        output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    series = df[column].dropna()

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(series, bins=bins, color=CHART_COLORS[0], edgecolor='white', alpha=0.8)
    ax.set_title(f'{column} 直方图', fontsize=14, fontweight='bold')
    ax.set_xlabel(column, fontsize=11)
    ax.set_ylabel('频数', fontsize=11)
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()

    filename = f"histogram_{column}_{uuid.uuid4().hex[:8]}.png"
    filepath = output_dir / filename
    plt.savefig(filepath, dpi=150, bbox_inches='tight')
    plt.close()

    return str(filepath)
