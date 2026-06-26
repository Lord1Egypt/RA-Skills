#!/usr/bin/env python3
"""生成美联储缩表周期分析图表"""

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path
import sys
from datetime import datetime

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei', 'SimHei', 'Noto Sans CJK SC', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def load_indicator_data(filepath):
    """加载指标数据"""
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    df = pd.DataFrame(data['data'])
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    df.sort_index(inplace=True)
    
    return df

def generate_comparison_chart(df_primary, df_related, events, primary_name, related_name, output_path):
    """生成时序对比图（含事件区间标记）"""
    fig, ax1 = plt.subplots(figsize=(16, 8))
    
    # 绘制主指标
    ax1.plot(df_primary.index, df_primary['close'], 'b-', linewidth=1.5, label=primary_name, alpha=0.8)
    ax1.set_xlabel('时间', fontsize=12)
    ax1.set_ylabel(primary_name, color='b', fontsize=12)
    ax1.tick_params(axis='y', labelcolor='b')
    
    # 绘制相关指标（双Y轴）
    ax2 = ax1.twinx()
    ax2.plot(df_related.index, df_related['close'], 'r-', linewidth=1.5, label=related_name, alpha=0.8)
    ax2.set_ylabel(related_name, color='r', fontsize=12)
    ax2.tick_params(axis='y', labelcolor='r')
    
    # 标记缩表事件区间（红色虚线框）
    for event in events['historical_events']:
        start = pd.to_datetime(event['start_date'])
        end = pd.to_datetime(event['end_date'])
        
        # 添加红色虚线矩形框
        rect = mpatches.Rectangle(
            (start, ax1.get_ylim()[0]),
            end - start,
            ax1.get_ylim()[1] - ax1.get_ylim()[0],
            linewidth=2,
            edgecolor='red',
            facecolor='lightyellow',
            alpha=0.3,
            linestyle='--',
            zorder=0
        )
        ax1.add_patch(rect)
        
        # 添加事件标签
        mid_date = start + (end - start) / 2
        ax1.annotate(
            f'缩表周期{event["event_id"]}',
            xy=(mid_date, ax1.get_ylim()[1] * 0.95),
            fontsize=10,
            ha='center',
            color='red',
            weight='bold'
        )
    
    # 设置标题
    title = f'{primary_name} vs {related_name} 历史走势对比\n（红色虚线框标记缩表周期）'
    plt.title(title, fontsize=14, weight='bold')
    
    # 合并图例
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=10)
    
    # 格式化X轴
    plt.gcf().autofmt_xdate()
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"图表保存: {output_path}")

def generate_summary_chart(performance, output_path):
    """生成表现汇总图"""
    indicator_names = {
        'sp500': '标普500',
        'nasdaq': '纳斯达克',
        'usd_index': '美元指数',
        'xlf': '金融ETF',
        'tlt': '长债ETF',
        'xlk': '科技ETF',
        'xle': '能源ETF',
        'us_10y_treasury': '10年美债收益率'
    }
    
    # 提取汇总数据
    summary = performance['summary']
    indicators = list(summary.keys())
    names = [indicator_names.get(i, i) for i in indicators]
    avg_changes = [summary[i]['avg_change'] for i in indicators]
    win_rates = [summary[i]['win_rate'] for i in indicators]
    
    # 创建图表
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # 颜色：正收益红色，负收益绿色（中国习惯）
    colors = ['#ff4444' if c > 0 else '#44ff44' for c in avg_changes]
    
    # 绘制柱状图
    bars = ax.bar(names, avg_changes, color=colors, alpha=0.8, edgecolor='black')
    
    # 添加数值标签
    for bar, change, win_rate in zip(bars, avg_changes, win_rates):
        height = bar.get_height()
        sign = '+' if change > 0 else ''
        ax.annotate(
            f'{sign}{change:.2f}%\n胜率{win_rate:.0f}%',
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 5),
            textcoords='offset points',
            ha='center',
            va='bottom',
            fontsize=10,
            weight='bold'
        )
    
    ax.set_ylabel('平均涨跌幅 (%)', fontsize=12)
    ax.set_xlabel('资产类别', fontsize=12)
    ax.set_title('美联储缩表周期内各类资产平均表现\n（🔴红涨 🟢绿跌）', fontsize=14, weight='bold')
    
    # 添加0线
    ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    
    plt.xticks(rotation=30, ha='right')
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"图表保存: {output_path}")

def generate_event_comparison_chart(performance, output_path):
    """生成事件对比图"""
    indicator_names = {
        'sp500': '标普500',
        'nasdaq': '纳斯达克',
        'usd_index': '美元指数',
        'xlf': '金融ETF',
        'tlt': '长债ETF',
        'xlk': '科技ETF',
        'xle': '能源ETF',
        'us_10y_treasury': '10年美债收益率'
    }
    
    # 提取事件数据
    events_data = performance['events']
    
    # 创建图表
    fig, axes = plt.subplots(1, 2, figsize=(16, 8))
    
    for ax, event in zip(axes, events_data):
        assets = event['assets']
        indicators = list(assets.keys())
        names = [indicator_names.get(i, i) for i in indicators]
        changes = [assets[i]['pct_change'] for i in indicators]
        
        colors = ['#ff4444' if c > 0 else '#44ff44' for c in changes]
        bars = ax.bar(names, changes, color=colors, alpha=0.8, edgecolor='black')
        
        for bar, change in zip(bars, changes):
            height = bar.get_height()
            sign = '+' if change > 0 else ''
            ax.annotate(
                f'{sign}{change:.2f}%',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 5),
                textcoords='offset points',
                ha='center',
                va='bottom',
                fontsize=9,
                weight='bold'
            )
        
        ax.set_ylabel('涨跌幅 (%)', fontsize=10)
        ax.set_title(f'【{event["name"]}】\n{event["start_date"]} ~ {event["end_date"]}', fontsize=12, weight='bold')
        ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        ax.tick_params(axis='x', rotation=30)
    
    plt.suptitle('美联储缩表周期各资产表现对比\n（🔴红涨 🟢绿跌）', fontsize=14, weight='bold')
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"图表保存: {output_path}")

def main():
    output_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.home() / '.openclaw/workspace/memory/reports/fed_qt_20260328'
    data_dir = output_dir / 'data'
    charts_dir = output_dir / 'charts'
    
    # 加载数据
    with open(output_dir / 'events.json', 'r') as f:
        events = json.load(f)
    
    with open(output_dir / 'performance.json', 'r') as f:
        performance = json.load(f)
    
    # 加载指标数据
    indicators_data = {}
    for indicator in ['sp500', 'nasdaq', 'usd_index', 'xlf', 'tlt', 'xlk', 'xle', 'us_10y_treasury']:
        filepath = data_dir / f'{indicator}.json'
        if filepath.exists():
            indicators_data[indicator] = load_indicator_data(filepath)
    
    indicator_names = {
        'sp500': '标普500指数',
        'nasdaq': '纳斯达克指数',
        'usd_index': '美元指数',
        'xlf': '金融ETF',
        'tlt': '长债ETF',
        'xlk': '科技ETF',
        'xle': '能源ETF',
        'us_10y_treasury': '10年美债收益率'
    }
    
    # 生成时序对比图
    comparison_pairs = [
        ('us_10y_treasury', 'sp500'),
        ('us_10y_treasury', 'nasdaq'),
        ('us_10y_treasury', 'tlt'),
        ('us_10y_treasury', 'xlf'),
        ('us_10y_treasury', 'usd_index'),
    ]
    
    for primary, related in comparison_pairs:
        if primary in indicators_data and related in indicators_data:
            output_path = charts_dir / f'{primary}_vs_{related}.png'
            generate_comparison_chart(
                indicators_data[primary],
                indicators_data[related],
                events,
                indicator_names[primary],
                indicator_names[related],
                output_path
            )
    
    # 生成汇总图
    generate_summary_chart(performance, charts_dir / 'performance_summary.png')
    
    # 生成事件对比图
    generate_event_comparison_chart(performance, charts_dir / 'event_comparison.png')
    
    # 保存图表清单
    manifest = {
        'charts': [
            {'file': 'us_10y_treasury_vs_sp500.png', 'title': '10年美债收益率 vs 标普500'},
            {'file': 'us_10y_treasury_vs_nasdaq.png', 'title': '10年美债收益率 vs 纳斯达克'},
            {'file': 'us_10y_treasury_vs_tlt.png', 'title': '10年美债收益率 vs 长债ETF'},
            {'file': 'us_10y_treasury_vs_xlf.png', 'title': '10年美债收益率 vs 金融ETF'},
            {'file': 'us_10y_treasury_vs_usd_index.png', 'title': '10年美债收益率 vs 美元指数'},
            {'file': 'performance_summary.png', 'title': '资产表现汇总'},
            {'file': 'event_comparison.png', 'title': '缩表周期对比'},
        ],
        'generated_at': datetime.now().isoformat()
    }
    
    with open(charts_dir / 'charts_manifest.json', 'w') as f:
        json.dump(manifest, f, indent=2)
    
    print(f"\n所有图表生成完成！保存目录: {charts_dir}")

if __name__ == '__main__':
    main()