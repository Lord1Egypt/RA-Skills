#!/usr/bin/env python3
"""Draw stock price chart for 601390"""
import akshare as ak
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import pandas as pd

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 获取历史数据（最近 30 个交易日）
print("获取历史数据...")
df = ak.stock_zh_a_hist(
    symbol='601390',
    period='daily',
    start_date='20260101',
    end_date='20260303',
    adjust='qfq'  # 前复权
)

if df.empty:
    print("未获取到数据")
    exit(1)

# 转换日期格式
df['日期'] = pd.to_datetime(df['日期'])
df = df.sort_values('日期')

# 创建图表
fig = plt.figure(figsize=(14, 8))

# 子图1：价格走势图
ax1 = plt.subplot(2, 1, 1)
ax1.plot(df['日期'], df['收盘'], linewidth=2, label='收盘价', color='#1f77b4')
ax1.fill_between(df['日期'], df['收盘'], alpha=0.3, color='#1f77b4')

# 标记最高价和最低价
max_price = df['收盘'].max()
min_price = df['收盘'].min()
max_date = df[df['收盘'] == max_price]['日期'].iloc[0]
min_date = df[df['收盘'] == min_price]['日期'].iloc[0]

ax1.scatter([max_date], [max_price], color='red', s=100, zorder=5, label=f'最高价 ¥{max_price:.2f}')
ax1.scatter([min_date], [min_price], color='green', s=100, zorder=5, label=f'最低价 ¥{min_price:.2f}')

ax1.set_ylabel('价格 (元)', fontsize=12)
ax1.set_title('中国中铁 (601390) 股价走势图', fontsize=16, fontweight='bold')
ax1.legend(loc='upper left', fontsize=10)
ax1.grid(True, alpha=0.3)

# 格式化x轴
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
ax1.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO))

# 子图2：成交量柱状图
ax2 = plt.subplot(2, 1, 2)
colors = ['#d62728' if df['涨跌幅'].iloc[i] < 0 else '#2ca02c' for i in range(len(df))]
ax2.bar(df['日期'], df['成交量'] / 10000, color=colors, alpha=0.6)
ax2.set_ylabel('成交量 (万手)', fontsize=12)
ax2.set_xlabel('日期', fontsize=12)
ax2.grid(True, alpha=0.3)
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
ax2.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO))

plt.tight_layout()

# 保存图表
output_file = r'C:\Users\Administrator\.openclaw\workspace\601390_chart.png'
plt.savefig(output_file, dpi=150, bbox_inches='tight')
print(f"图表已保存到: {output_file}")

# 显示当前信息
latest = df.iloc[-1]
print(f"\n最新行情 ({latest['日期'].strftime('%Y-%m-%d')}):")
print(f"收盘价: ¥{latest['收盘']:.2f}")
print(f"涨跌幅: {latest['涨跌幅']:.2f}%")
print(f"成交量: {latest['成交量']/10000:.2f}万手")
