#!/usr/bin/env python3
"""
Chart Toolkit - 使用示例
"""

from chart_generator import ChartGenerator, plot_heatmap, plot_histogram, plot_corr_matrix, plot_timeline
from chart_generator import plot_gauge, plot_funnel, batch_charts, get_color_scheme, PlotlyChart
import pandas as pd
import matplotlib.pyplot as plt


def example_line_chart():
    """示例1: 折线图"""
    data = {
        'date': ['2026-01', '2026-02', '2026-03', '2026-04'],
        'sales': [10000, 15000, 12000, 18000],
        'profit': [2000, 3500, 2800, 4200]
    }
    
    chart = ChartGenerator()
    chart.line_chart(data, 'date', ['sales', 'profit'], title='Sales & Profit')
    chart.save('examples/line_chart.png')
    print("✓ 折线图已保存")


def example_bar_chart():
    """示例2: 柱状图"""
    data = {
        'date': ['2026-01', '2026-02', '2026-03', '2026-04'],
        'sales': [10000, 15000, 12000, 18000]
    }
    
    chart = ChartGenerator()
    chart.bar_chart(data, 'date', 'sales', title='Monthly Sales')
    chart.save('examples/bar_chart.png')
    print("✓ 柱状图已保存")


def example_pie_chart():
    """示例3: 饼图"""
    data = {
        'category': ['手机', '电脑', '平板', '配件'],
        'sales': [3500, 3000, 2000, 1500]
    }
    
    chart = ChartGenerator()
    chart.pie_chart(data, 'category', 'sales', title='Sales by Category')
    chart.save('examples/pie_chart.png')
    print("✓ 饼图已保存")


def example_scatter_chart():
    """示例4: 散点图"""
    data = {
        'advertising': [100, 200, 300, 400, 500],
        'sales': [1200, 1800, 2400, 2900, 3800]
    }
    
    chart = ChartGenerator()
    chart.scatter_chart(data, 'advertising', 'sales', title='Advertising vs Sales')
    chart.save('examples/scatter_chart.png')
    print("✓ 散点图已保存")


def example_heatmap():
    """示例5: 热力图"""
    import numpy as np
    data = pd.DataFrame(
        np.random.rand(10, 10),
        columns=[f'Col{i}' for i in range(10)],
        index=[f'Row{i}' for i in range(10)]
    )
    
    fig = plot_heatmap(data, 'Col0', 'Row0', title='Heatmap')
    if fig:
        plt.savefig('examples/heatmap.png')
        print("✓ 热力图已保存")


def example_corr_matrix():
    """示例6: 相关性矩阵"""
    data = pd.DataFrame({
        'A': [1, 2, 3, 4, 5],
        'B': [2, 4, 6, 8, 10],
        'C': [1, 3, 5, 7, 9],
        'D': [5, 4, 3, 2, 1]
    })
    
    fig = plot_corr_matrix(data, title='Correlation')
    if fig:
        plt.savefig('examples/corr_matrix.png')
        print("✓ 相关性矩阵已保存")


def example_timeline():
    """示例7: 时间线"""
    data = {
        'date': ['2026-01', '2026-02', '2026-03', '2026-04'],
        'visitors': [1000, 1500, 1800, 2200],
        'orders': [100, 150, 180, 220]
    }
    
    fig = plot_timeline(data, 'date', ['visitors', 'orders'], title='Timeline')
    if fig:
        plt.savefig('examples/timeline.png')
        print("✓ 时间线已保存")


def example_gauge():
    """示例8: 仪表盘"""
    fig = plot_gauge(75, title='Performance', max_value=100)
    if fig:
        plt.savefig('examples/gauge.png')
        print("✓ 仪表盘已保存")


def example_funnel():
    """示例9: 漏斗图"""
    data = pd.DataFrame({
        'stage': ['访问', '注册', '浏览', '购买'],
        'users': [10000, 5000, 3000, 1000]
    })
    
    fig = plot_funnel(data, 'stage', 'users', title='Funnel')
    if fig:
        plt.savefig('examples/funnel.png')
        print("✓ 漏斗图已保存")


def example_batch():
    """示例10: 批量图表"""
    data = pd.DataFrame({
        'A': [1, 2, 3, 4, 5],
        'B': [5, 4, 3, 2, 1],
        'C': [2, 3, 4, 5, 6]
    })
    
    results = batch_charts(data, output_dir='examples/batch')
    print(f"✓ 已生成 {len(results)} 个批量图表")


def example_color_scheme():
    """示例11: 颜色方案"""
    colors = get_color_scheme('neon')
    print(f"Neon颜色: {colors}")
    
    colors = get_color_scheme('pastel')
    print(f"Pastel颜色: {colors}")


def example_plotly():
    """示例12: Plotly交互图表"""
    data = {
        'date': ['2026-01', '2026-02', '2026-03', '2026-04'],
        'sales': [10000, 15000, 12000, 18000]
    }
    
    df = pd.DataFrame(data)
    fig = PlotlyChart.line(df, 'date', 'sales', title='Interactive')
    html = PlotlyChart.to_html(fig)
    
    with open('examples/interactive.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("✓ 交互图表已保存")


def run_all_examples():
    """运行所有示例"""
    import os
    os.makedirs('examples', exist_ok=True)
    
    print("开始运行示例...")
    print()
    
    example_line_chart()
    example_bar_chart()
    example_pie_chart()
    example_scatter_chart()
    example_heatmap()
    example_corr_matrix()
    example_timeline()
    example_gauge()
    example_funnel()
    example_batch()
    example_color_scheme()
    example_plotly()
    
    print()
    print("所有示例完成!")


if __name__ == '__main__':
    run_all_examples()