#!/usr/bin/env python3
"""
生成近10年月K线图（价格 + 成交额 + Zigzag趋势线）
"""

import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from typing import List, Dict, Any, Optional
import os

# 设置中文字体（使用系统可用的字体）
plt.rcParams['font.family'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def zigzag_indicator(prices: List[float], threshold: float = 0.08) -> List[int]:
    """
    Zigzag趋势线算法
    找出价格转折点（超过threshold百分比的变化）
    返回转折点的索引列表
    """
    if len(prices) < 3:
        return []
    
    zigzag_points = [0]  # 第一个点
    pivot_idx = 0
    pivot_price = prices[0]
    direction = 0  # 0: 未确定, 1: 上涨, -1: 下跌
    
    for i in range(1, len(prices)):
        price = prices[i]
        
        if pivot_price == 0:
            continue
        
        change = (price - pivot_price) / pivot_price
        
        if direction == 0:
            # 确定初始方向
            if change >= threshold:
                direction = 1
                pivot_idx = i
                pivot_price = price
                zigzag_points.append(i)
            elif change <= -threshold:
                direction = -1
                pivot_idx = i
                pivot_price = price
                zigzag_points.append(i)
        elif direction == 1:
            # 上升趋势
            if price > pivot_price:
                pivot_idx = i
                pivot_price = price
            elif change <= -threshold:
                # 转折点
                zigzag_points.append(pivot_idx)
                direction = -1
                pivot_idx = i
                pivot_price = price
        elif direction == -1:
            # 下降趋势
            if price < pivot_price:
                pivot_idx = i
                pivot_price = price
            elif change >= threshold:
                # 转折点
                zigzag_points.append(pivot_idx)
                direction = 1
                pivot_idx = i
                pivot_price = price
    
    # 添加最后一个点
    if pivot_idx not in zigzag_points:
        zigzag_points.append(pivot_idx)
    
    return sorted(zigzag_points)

def parse_date(date_str: str) -> datetime:
    """解析日期字符串"""
    try:
        if len(date_str) == 8:  # YYYYMMDD
            return datetime.strptime(date_str, '%Y%m%d')
        elif len(date_str) == 10:  # YYYY-MM-DD
            return datetime.strptime(date_str, '%Y-%m-%d')
        else:
            return datetime.strptime(date_str[:10], '%Y-%m-%d')
    except:
        return datetime.now()

def generate_kline_chart(
    kline_data: Dict[str, Any],
    output_path: str,
    title: str = "近10年月K线图",
    threshold: float = 0.08
) -> str:
    """
    生成月K线图（价格 + 成交额 + Zigzag）
    """
    if not kline_data or not kline_data.get('dates'):
        print("No kline data available")
        return ""
    
    # 解析日期
    dates = [parse_date(d) for d in kline_data['dates']]
    dates.reverse()  # 从旧到新
    
    # 价格数据
    closes = kline_data.get('close', [])
    highs = kline_data.get('high', [])
    lows = kline_data.get('low', [])
    amounts = kline_data.get('amount', [])
    
    if closes:
        closes = closes[::-1]
    if highs:
        highs = highs[::-1]
    if lows:
        lows = lows[::-1]
    if amounts:
        amounts = amounts[::-1]
    
    # 计算zigzag
    zigzag_idx = zigzag_indicator(closes, threshold) if closes else []
    
    # 创建图表
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 10),
                                    gridspec_kw={'height_ratios': [3, 1]},
                                    sharex=True)
    
    # 顶部：价格K线
    ax1.set_title(title, fontsize=14, fontweight='bold')
    
    # 绘制收盘价
    ax1.plot(dates, closes, 'b-', linewidth=1.5, label='Close Price', alpha=0.8)
    
    # 绘制价格区间
    if highs and lows:
        ax1.fill_between(dates, lows, highs, alpha=0.2, color='gray', label='Price Range')
    
    # 绘制zigzag趋势线
    if zigzag_idx and len(zigzag_idx) > 1:
        zig_dates = [dates[i] for i in zigzag_idx]
        zig_prices = [closes[i] for i in zigzag_idx]
        ax1.plot(zig_dates, zig_prices, 'r-', linewidth=2.5,
                 marker='o', markersize=5, label='Zigzag Trend', alpha=0.7)
    
    ax1.set_ylabel('Price (CNY)', fontsize=12)
    ax1.legend(loc='upper left')
    ax1.grid(True, alpha=0.3)
    
    # 标注最高最低点
    if closes:
        max_idx = np.argmax(closes)
        min_idx = np.argmin(closes)
        ax1.annotate(f'H: {closes[max_idx]:.2f}',
                     xy=(dates[max_idx], closes[max_idx]),
                     xytext=(10, 10), textcoords='offset points',
                     fontsize=10, color='green')
        ax1.annotate(f'L: {closes[min_idx]:.2f}',
                     xy=(dates[min_idx], closes[min_idx]),
                     xytext=(10, -15), textcoords='offset points',
                     fontsize=10, color='red')
    
    # 底部：成交额
    if amounts:
        # 转换为亿元
        amounts_bn = [a / 1e7 for a in amounts]  # 千元转亿元
        ax2.bar(dates, amounts_bn, width=25,
                color='steelblue', alpha=0.6, label='Turnover (Billion CNY)')
        ax2.set_ylabel('Turnover (Billion)', fontsize=12)
        ax2.legend(loc='upper left')
        ax2.grid(True, alpha=0.3)
    
    # X轴格式
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax2.xaxis.set_major_locator(mdates.MonthLocator(interval=12))  # 每年一个刻度
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    
    # 保存图片
    plt.savefig(output_path, dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    
    print(f"Chart saved: {output_path}")
    return output_path

def main():
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python generate_chart.py <kline_json_file> <output_image_path>")
        print("Example: python generate_chart.py kline.json chart.png")
        sys.exit(1)
    
    kline_file = sys.argv[1]
    output_path = sys.argv[2]
    
    with open(kline_file, 'r') as f:
        kline_data = json.load(f)
    
    generate_kline_chart(kline_data, output_path)

if __name__ == "__main__":
    main()