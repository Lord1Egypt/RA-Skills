#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图表生成模块

生成情感趋势图、行业分布图等可视化图表

用法:
    python charts.py trend --input analyzed.json --output trend.png
    python charts.py pie --input analyzed.json --output pie.png
    python charts.py industry --input analyzed.json --output industry.png
"""

import argparse
import json
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime


def check_matplotlib():
    """检查 matplotlib 是否安装"""
    try:
        import matplotlib
        return True
    except ImportError:
        print("⚠️  请安装 matplotlib: pip install matplotlib")
        print("   或使用 --no-chart 参数跳过图表生成")
        return False


def create_sentiment_trend(data: List[Dict[str, Any]], output_file: str):
    """生成情感趋势图"""
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from collections import defaultdict
    
    # 按日期分组统计
    daily_stats = defaultdict(lambda: {'positive': 0, 'negative': 0, 'neutral': 0})
    
    for item in data:
        # 尝试从不同字段获取日期
        date_str = item.get('analyzed_at', item.get('time', item.get('publish_time', '')))
        if not date_str:
            continue
        
        # 简化日期（取前 10 位）
        date_str = date_str[:10]
        
        sentiment = item.get('sentiment', 'neutral')
        if sentiment in daily_stats[date_str]:
            daily_stats[date_str][sentiment] += 1
    
    # 准备绘图数据
    dates = sorted(daily_stats.keys())
    positive = [daily_stats[d]['positive'] for d in dates]
    negative = [daily_stats[d]['negative'] for d in dates]
    neutral = [daily_stats[d]['neutral'] for d in dates]
    
    # 创建图表
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.plot(dates, positive, 'o-', color='#22c55e', label='利好 🟢', linewidth=2, markersize=6)
    ax.plot(dates, negative, 's-', color='#ef4444', label='利空 🔴', linewidth=2, markersize=6)
    ax.plot(dates, neutral, '^-', color='#9ca3af', label='中性 ⚪', linewidth=2, markersize=6)
    
    # 填充区域
    ax.fill_between(dates, positive, alpha=0.3, color='#22c55e')
    ax.fill_between(dates, negative, alpha=0.3, color='#ef4444')
    ax.fill_between(dates, neutral, alpha=0.3, color='#9ca3af')
    
    # 设置标题和标签
    ax.set_title('财经新闻情感趋势', fontsize=16, fontweight='bold')
    ax.set_xlabel('日期', fontsize=12)
    ax.set_ylabel('新闻数量', fontsize=12)
    
    # 旋转日期标签
    plt.xticks(rotation=45)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    
    # 添加图例
    ax.legend(loc='upper left', fontsize=10)
    
    # 添加网格
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # 调整布局
    plt.tight_layout()
    
    # 保存图表
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"✅ 情感趋势图已保存：{output_file}")


def create_sentiment_pie(data: List[Dict[str, Any]], output_file: str):
    """生成情感分布饼图"""
    import matplotlib.pyplot as plt
    
    # 统计情感分布
    sentiment_count = {'positive': 0, 'negative': 0, 'neutral': 0}
    
    for item in data:
        sentiment = item.get('sentiment', 'neutral')
        if sentiment in sentiment_count:
            sentiment_count[sentiment] += 1
    
    # 准备数据
    labels = ['利好 🟢', '利空 🔴', '中性 ⚪']
    sizes = [sentiment_count['positive'], sentiment_count['negative'], sentiment_count['neutral']]
    colors = ['#22c55e', '#ef4444', '#9ca3af']
    
    # 创建图表
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # 绘制饼图
    wedges, texts, autotexts = ax.pie(
        sizes, 
        labels=labels, 
        colors=colors,
        autopct='%1.1f%%',
        startangle=90,
        explode=(0.05, 0.05, 0.05),
        textprops={'fontsize': 12}
    )
    
    # 设置百分比格式
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    # 添加标题
    ax.set_title('新闻情感分布', fontsize=16, fontweight='bold')
    
    # 确保饼图是圆形
    ax.axis('equal')
    
    # 保存图表
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"✅ 情感分布饼图已保存：{output_file}")


def create_industry_chart(data: List[Dict[str, Any]], output_file: str):
    """生成行业分布图"""
    import matplotlib.pyplot as plt
    from collections import defaultdict
    
    # 统计行业分布
    industry_count = defaultdict(lambda: {'positive': 0, 'negative': 0, 'neutral': 0})
    
    for item in data:
        # 获取行业信息
        sectors = item.get('affected_sectors', [])
        sentiment = item.get('sentiment', 'neutral')
        
        for sector in sectors:
            if sector and sentiment in industry_count[sector]:
                industry_count[sector][sentiment] += 1
    
    # 按新闻总数排序，取前 10 个行业
    industry_totals = [(k, sum(v.values())) for k, v in industry_count.items()]
    industry_totals.sort(key=lambda x: x[1], reverse=True)
    top_industries = [x[0] for x in industry_totals[:10]]
    
    if not top_industries:
        print("⚠️  没有行业数据，跳过图表生成")
        return
    
    # 准备数据
    x = range(len(top_industries))
    positive = [industry_count[ind]['positive'] for ind in top_industries]
    negative = [industry_count[ind]['negative'] for ind in top_industries]
    neutral = [industry_count[ind]['neutral'] for ind in top_industries]
    
    # 创建图表
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # 堆叠柱状图
    p1 = ax.bar(x, positive, color='#22c55e', label='利好 🟢')
    p2 = ax.bar(x, negative, bottom=positive, color='#ef4444', label='利空 🔴')
    p3 = ax.bar(x, neutral, bottom=[p+n for p,n in zip(positive, negative)], 
                color='#9ca3af', label='中性 ⚪')
    
    # 设置标题和标签
    ax.set_title('行业新闻分布 Top 10', fontsize=16, fontweight='bold')
    ax.set_xlabel('行业', fontsize=12)
    ax.set_ylabel('新闻数量', fontsize=12)
    
    # 设置 x 轴标签
    ax.set_xticks(x)
    ax.set_xticklabels(top_industries, rotation=45, ha='right')
    
    # 添加图例
    ax.legend(loc='upper left', fontsize=10)
    
    # 添加网格
    ax.grid(True, alpha=0.3, axis='y', linestyle='--')
    
    # 调整布局
    plt.tight_layout()
    
    # 保存图表
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"✅ 行业分布图已保存：{output_file}")


def create_stock_heatmap(data: List[Dict[str, Any]], output_file: str):
    """生成股票情感热力图"""
    import matplotlib.pyplot as plt
    from collections import defaultdict
    
    # 统计股票情感
    stock_sentiment = defaultdict(lambda: {'positive': 0, 'negative': 0, 'neutral': 0})
    
    for item in data:
        affected_stocks = item.get('affected_stocks', [])
        sentiment = item.get('sentiment', 'neutral')
        
        for stock in affected_stocks:
            if isinstance(stock, dict):
                ticker = stock.get('ticker', '')
                impact = stock.get('impact', 'neutral')
                if ticker:
                    stock_sentiment[ticker][impact] += 1
    
    if not stock_sentiment:
        print("⚠️  没有股票数据，跳过图表生成")
        return
    
    # 按总提及次数排序，取前 15 只股票
    stock_totals = [(k, sum(v.values())) for k, v in stock_sentiment.items()]
    stock_totals.sort(key=lambda x: x[1], reverse=True)
    top_stocks = [x[0] for x in stock_totals[:15]]
    
    # 准备热力图数据
    positive_ratio = []
    for stock in top_stocks:
        total = sum(stock_sentiment[stock].values())
        if total > 0:
            ratio = stock_sentiment[stock]['positive'] / total * 100
        else:
            ratio = 50
        positive_ratio.append(ratio)
    
    # 创建图表
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # 绘制热力图
    im = ax.barh(top_stocks, positive_ratio, color=plt.cm.RdYlGn([r/100 for r in positive_ratio]))
    
    # 设置标题和标签
    ax.set_title('股票情感热力图（绿色=利好占比高，红色=利空占比高）', fontsize=14, fontweight='bold')
    ax.set_xlabel('利好消息占比 (%)', fontsize=12)
    ax.set_ylabel('股票代码', fontsize=12)
    
    # 设置 x 轴范围
    ax.set_xlim([0, 100])
    
    # 添加颜色条
    sm = plt.cm.ScalarMappable(cmap=plt.cm.RdYlGn, norm=plt.Normalize(vmin=0, vmax=100))
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax)
    cbar.set_label('利好消息占比 (%)', fontsize=10)
    
    # 添加网格
    ax.grid(True, alpha=0.3, axis='x', linestyle='--')
    
    # 调整布局
    plt.tight_layout()
    
    # 保存图表
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"✅ 股票情感热力图已保存：{output_file}")


def main():
    parser = argparse.ArgumentParser(description='财经新闻图表生成')
    
    parser.add_argument('chart_type', type=str,
                        choices=['trend', 'pie', 'industry', 'heatmap', 'all'],
                        help='图表类型')
    parser.add_argument('--input', type=str, required=True,
                        help='输入 JSON 文件路径')
    parser.add_argument('--output', type=str, default=None,
                        help='输出文件路径')
    parser.add_argument('--no-show', action='store_true',
                        help='不显示图表，仅保存文件')
    
    args = parser.parse_args()
    
    # 检查 matplotlib
    if not check_matplotlib():
        return
    
    # 加载数据
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"❌ 文件不存在：{input_path}")
        return
    
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if not isinstance(data, list):
        data = [data]
    
    print(f"📊 加载数据：{len(data)} 条")
    
    # 确定输出目录
    output_dir = input_path.parent
    base_name = input_path.stem
    
    # 生成图表
    if args.chart_type == 'trend' or args.chart_type == 'all':
        output = args.output or str(output_dir / f'{base_name}_trend.png')
        create_sentiment_trend(data, output)
    
    if args.chart_type == 'pie' or args.chart_type == 'all':
        output = args.output or str(output_dir / f'{base_name}_pie.png')
        create_sentiment_pie(data, output)
    
    if args.chart_type == 'industry' or args.chart_type == 'all':
        output = args.output or str(output_dir / f'{base_name}_industry.png')
        create_industry_chart(data, output)
    
    if args.chart_type == 'heatmap' or args.chart_type == 'all':
        output = args.output or str(output_dir / f'{base_name}_heatmap.png')
        create_stock_heatmap(data, output)
    
    print("\n✅ 图表生成完成！")


if __name__ == '__main__':
    main()
