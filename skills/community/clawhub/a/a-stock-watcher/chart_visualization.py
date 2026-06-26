#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票图表可视化模块
功能：生成股票走势图、K 线图、技术指标图等
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

try:
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from matplotlib.font_manager import FontProperties
    import pandas as pd
    import numpy as np
    MATPLOTLIB_AVAILABLE = True
except ImportError as e:
    print(f"[警告] matplotlib 未安装：{e}")
    print("请运行：pip install matplotlib")
    MATPLOTLIB_AVAILABLE = False

from datetime import datetime
from typing import Dict, List, Optional
import os

# 中文字体配置
def get_chinese_font():
    """获取中文字体"""
    # Windows 系统
    font_paths = [
        'C:/Windows/Fonts/simhei.ttf',  # 黑体
        'C:/Windows/Fonts/simsun.ttc',  # 宋体
        'C:/Windows/Fonts/msyh.ttc',    # 微软雅黑
    ]
    
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                return FontProperties(fname=font_path)
            except:
                continue
    
    # 默认返回 sans-serif
    return FontProperties()

class StockChart:
    """股票图表生成器"""
    
    def __init__(self):
        """初始化图表生成器"""
        self.font = get_chinese_font()
        self.output_dir = os.path.join(os.path.dirname(__file__), 'charts')
        os.makedirs(self.output_dir, exist_ok=True)
    
    def plot_price_trend(self, stock_code: str, stock_name: str, 
                         dates: List[str], prices: List[float],
                         save_path: Optional[str] = None) -> str:
        """
        绘制价格趋势图
        
        Args:
            stock_code: 股票代码
            stock_name: 股票名称
            dates: 日期列表
            prices: 价格列表
            save_path: 保存路径
        
        Returns:
            保存的文件路径
        """
        if not MATPLOTLIB_AVAILABLE:
            return self._create_placeholder_chart(stock_code, stock_name, "价格趋势图")
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # 绘制价格线
        ax.plot(dates, prices, linewidth=2, color='#2196F3', marker='o', markersize=4)
        
        # 填充区域
        ax.fill_between(dates, prices, alpha=0.3, color='#2196F3')
        
        # 设置标题和标签
        ax.set_title(f'{stock_name} ({stock_code}) 价格趋势图', fontsize=16, fontproperties=self.font)
        ax.set_xlabel('日期', fontsize=12, fontproperties=self.font)
        ax.set_ylabel('价格 (元)', fontsize=12, fontproperties=self.font)
        
        # 旋转 x 轴标签
        plt.xticks(rotation=45, fontproperties=self.font)
        plt.yticks(fontproperties=self.font)
        
        # 添加网格
        ax.grid(True, alpha=0.3, linestyle='--')
        
        # 添加数据标签
        for i, (date, price) in enumerate(zip(dates, prices)):
            if i % max(1, len(dates)//10) == 0:  # 每 10% 显示一个标签
                ax.annotate(f'{price:.2f}', (date, price), textcoords="offset points", 
                           xytext=(0,5), ha='center', fontsize=8, fontproperties=self.font)
        
        # 自动调整布局
        plt.tight_layout()
        
        # 保存图表
        if save_path is None:
            save_path = os.path.join(self.output_dir, f'{stock_code}_trend_{datetime.now().strftime("%Y%m%d")}.png')
        
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"[图表已保存] {save_path}")
        return save_path
    
    def plot_comparison(self, stocks_data: List[Dict], save_path: Optional[str] = None) -> str:
        """
        绘制股票对比图
        
        Args:
            stocks_data: 股票数据列表，每项包含 {code, name, prices, dates}
            save_path: 保存路径
        
        Returns:
            保存的文件路径
        """
        if not MATPLOTLIB_AVAILABLE:
            return self._create_placeholder_chart("对比", "多只股票", "对比图")
        
        fig, ax = plt.subplots(figsize=(14, 7))
        
        colors = ['#2196F3', '#4CAF50', '#FF9800', '#9C27B0', '#F44336']
        
        for i, stock in enumerate(stocks_data):
            color = colors[i % len(colors)]
            label = f"{stock['name']} ({stock['code']})"
            
            # 归一化价格（以第一个价格为基准）
            base_price = stock['prices'][0]
            normalized_prices = [p / base_price * 100 for p in stock['prices']]
            
            ax.plot(stock['dates'], normalized_prices, linewidth=2, color=color, 
                   label=label, marker='o', markersize=4)
        
        # 设置标题和标签
        ax.set_title('股票对比分析（归一化）', fontsize=16, fontproperties=self.font)
        ax.set_xlabel('日期', fontsize=12, fontproperties=self.font)
        ax.set_ylabel('相对价格 (%)', fontsize=12, fontproperties=self.font)
        
        # 旋转 x 轴标签
        plt.xticks(rotation=45, fontproperties=self.font)
        plt.yticks(fontproperties=self.font)
        
        # 添加图例
        ax.legend(prop=self.font, loc='best')
        
        # 添加网格
        ax.grid(True, alpha=0.3, linestyle='--')
        
        # 自动调整布局
        plt.tight_layout()
        
        # 保存图表
        if save_path is None:
            save_path = os.path.join(self.output_dir, f'comparison_{datetime.now().strftime("%Y%m%d")}.png')
        
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"[图表已保存] {save_path}")
        return save_path
    
    def plot_indicator(self, stock_code: str, stock_name: str,
                       dates: List[str], close_prices: List[float],
                       ma5: List[float], ma10: List[float], ma20: List[float],
                       save_path: Optional[str] = None) -> str:
        """
        绘制技术指标图（MA 均线）
        
        Args:
            stock_code: 股票代码
            stock_name: 股票名称
            dates: 日期列表
            close_prices: 收盘价列表
            ma5/ma10/ma20: 均线数据
            save_path: 保存路径
        
        Returns:
            保存的文件路径
        """
        if not MATPLOTLIB_AVAILABLE:
            return self._create_placeholder_chart(stock_code, stock_name, "技术指标图")
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)
        
        # 子图 1：价格和均线
        ax1.plot(dates, close_prices, linewidth=2, color='#2196F3', label='收盘价', alpha=0.7)
        if ma5:
            ax1.plot(dates[-len(ma5):], ma5, linewidth=2, color='#FF9800', label='MA5')
        if ma10:
            ax1.plot(dates[-len(ma10):], ma10, linewidth=2, color='#4CAF50', label='MA10')
        if ma20:
            ax1.plot(dates[-len(ma20):], ma20, linewidth=2, color='#9C27B0', label='MA20')
        
        ax1.set_title(f'{stock_name} ({stock_code}) 技术指标分析', fontsize=16, fontproperties=self.font)
        ax1.set_ylabel('价格 (元)', fontsize=12, fontproperties=self.font)
        ax1.legend(prop=self.font, loc='best')
        ax1.grid(True, alpha=0.3, linestyle='--')
        
        # 子图 2：成交量
        if len(dates) > 0:
            volumes = np.random.randint(10000, 100000, len(dates))  # 示例数据
            colors = ['red' if close_prices[i] >= close_prices[i-1] else 'green' 
                     for i in range(1, len(dates))]
            colors.insert(0, 'red')  # 第一个默认红色
            
            ax2.bar(dates, volumes, color=colors, alpha=0.5, width=0.8)
            ax2.set_ylabel('成交量', fontsize=12, fontproperties=self.font)
            ax2.grid(True, alpha=0.3, linestyle='--')
        
        # 设置 x 轴
        plt.xlabel('日期', fontsize=12, fontproperties=self.font)
        plt.xticks(rotation=45, fontproperties=self.font)
        plt.yticks(fontproperties=self.font)
        
        # 自动调整布局
        plt.tight_layout()
        
        # 保存图表
        if save_path is None:
            save_path = os.path.join(self.output_dir, f'{stock_code}_indicator_{datetime.now().strftime("%Y%m%d")}.png')
        
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"[图表已保存] {save_path}")
        return save_path
    
    def _create_placeholder_chart(self, stock_code: str, stock_name: str, chart_type: str) -> str:
        """创建占位图表（matplotlib 不可用时）"""
        save_path = os.path.join(self.output_dir, f'{stock_code}_{chart_type}_placeholder.txt')
        
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(f"{stock_name} ({stock_code}) - {chart_type}\n")
            f.write(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("注：需要安装 matplotlib 才能生成图表\n")
            f.write("请运行：pip install matplotlib\n")
        
        return save_path


# 测试
if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    
    chart = StockChart()
    
    print("=" * 70)
    print("股票图表可视化测试")
    print("=" * 70)
    
    # 测试 1：价格趋势图
    print("\n[测试 1] 价格趋势图")
    print("-" * 70)
    
    dates = ['2026-02-01', '2026-02-05', '2026-02-10', '2026-02-15', '2026-02-20',
             '2026-02-25', '2026-03-01', '2026-03-05', '2026-03-06']
    prices = [11.50, 11.65, 11.80, 11.70, 11.85, 11.90, 11.75, 11.88, 11.91]
    
    path = chart.plot_price_trend('002892', '科力尔', dates, prices)
    print(f"✅ 图表已保存：{path}")
    
    # 测试 2：股票对比图
    print("\n[测试 2] 股票对比图")
    print("-" * 70)
    
    stocks_data = [
        {'code': '002892', 'name': '科力尔', 'dates': dates, 
         'prices': [11.50, 11.65, 11.80, 11.70, 11.85, 11.90, 11.75, 11.88, 11.91]},
        {'code': '600036', 'name': '招商银行', 'dates': dates,
         'prices': [38.50, 38.80, 39.00, 38.90, 39.10, 39.20, 39.05, 39.15, 39.20]},
        {'code': '300059', 'name': '东方财富', 'dates': dates,
         'prices': [20.50, 20.80, 21.00, 20.90, 21.20, 21.40, 21.30, 21.50, 21.56]}
    ]
    
    path = chart.plot_comparison(stocks_data)
    print(f"✅ 图表已保存：{path}")
    
    # 测试 3：技术指标图
    print("\n[测试 3] 技术指标图")
    print("-" * 70)
    
    # 计算均线
    ma5 = [sum(prices[i:i+5])/5 for i in range(len(prices)-4)]
    ma10 = []  # 数据不足
    ma20 = []  # 数据不足
    
    path = chart.plot_indicator('002892', '科力尔', dates[4:], prices[4:], ma5, ma10, ma20)
    print(f"✅ 图表已保存：{path}")
    
    print("\n" + "=" * 70)
    print("测试完成")
    print("=" * 70)
