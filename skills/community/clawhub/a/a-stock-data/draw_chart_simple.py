#!/usr/bin/env python3
"""Draw stock price chart based on known data"""
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import pandas as pd

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 已知的近期数据
data = {
    '日期': [
        '2026-02-25', '2026-02-26', '2026-02-27',
        '2026-03-02', '2026-03-03'
    ],
    '收盘': [6.19, 6.15, 6.30, 6.23, 6.01],
    '涨跌幅': [2.31, -0.65, 2.44, -1.11, -3.53],
    '成交量': [7.93, 3.23, 3.74, 2.70, 4.17],  # 换手率作为成交量参考
    '最高': [6.47, 6.30, 6.36, 6.29, 6.23],
    '最低': [6.05, 6.14, 6.15, 6.17, 5.97]
}

df = pd.DataFrame(data)
df['日期'] = pd.to_datetime(df['日期'])

# 创建图表
fig = plt.figure(figsize=(14, 10))

# 子图1：价格走势图（带K线）
ax1 = plt.subplot(3, 1, 1)
ax1.plot(df['日期'], df['收盘'], linewidth=2.5, label='收盘价', color='#1f77b4', marker='o', markersize=8)
ax1.fill_between(df['日期'], df['收盘'], alpha=0.3, color='#1f77b4')

# 绘制最高最低价范围
ax1.fill_between(df['日期'], df['最低'], df['最高'], alpha=0.2, color='gray', label='日内波动区间')

# 标记最高价和最低价
max_price = df['收盘'].max()
min_price = df['收盘'].min()
max_date = df[df['收盘'] == max_price]['日期'].iloc[0]
min_date = df[df['收盘'] == min_price]['日期'].iloc[0]

ax1.scatter([max_date], [max_price], color='red', s=150, zorder=5, 
            label=f'最高 ¥{max_price:.2f}', edgecolors='darkred', linewidths=2)
ax1.scatter([min_date], [min_price], color='green', s=150, zorder=5,
            label=f'最低 ¥{min_price:.2f}', edgecolors='darkgreen', linewidths=2)

# 添加价格标签
for i, row in df.iterrows():
    ax1.annotate(f'{row["收盘"]:.2f}', 
                xy=(row['日期'], row['收盘']), 
                xytext=(0, 10), 
                textcoords='offset points',
                ha='center', va='bottom', fontsize=9,
                color='red' if row['涨跌幅'] < 0 else 'green')

ax1.set_ylabel('价格 (元)', fontsize=12, fontweight='bold')
ax1.set_title('中国中铁 (601390) 近期股价走势', fontsize=18, fontweight='bold')
ax1.legend(loc='upper left', fontsize=10, framealpha=0.9)
ax1.grid(True, alpha=0.3, linestyle='--')
ax1.set_ylim(5.8, 6.5)

# 子图2：涨跌幅柱状图
ax2 = plt.subplot(3, 1, 2)
colors = ['#d62728' if x < 0 else '#2ca02c' for x in df['涨跌幅']]
bars = ax2.bar(df['日期'], df['涨跌幅'], color=colors, alpha=0.7, edgecolor='black', linewidth=1)

# 添加涨跌幅标签
for bar, pct in zip(bars, df['涨跌幅']):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height,
            f'{pct:+.2f}%',
            ha='center', va='bottom' if height > 0 else 'top',
            fontweight='bold')

ax2.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
ax2.set_ylabel('涨跌幅 (%)', fontsize=12, fontweight='bold')
ax2.grid(True, alpha=0.3, linestyle='--', axis='y')

# 子图3：成交量/换手率
ax3 = plt.subplot(3, 1, 3)
ax3.bar(df['日期'], df['成交量'], color='#ff7f0e', alpha=0.7, edgecolor='black', linewidth=1)
ax3.set_ylabel('换手率 (%)', fontsize=12, fontweight='bold')
ax3.set_xlabel('日期', fontsize=12, fontweight='bold')
ax3.grid(True, alpha=0.3, linestyle='--')

# 格式化x轴
for ax in [ax1, ax2, ax3]:
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))

plt.tight_layout(pad=3.0)

# 保存图表
output_file = r'C:\Users\Administrator\.openclaw\workspace\601390_chart.png'
plt.savefig(output_file, dpi=150, bbox_inches='tight')
print(f"图表已保存到: {output_file}")

# 显示统计信息
print(f"\n中国中铁 (601390) 统计信息:")
print(f"数据周期: {df['日期'].min().strftime('%Y-%m-%d')} 至 {df['日期'].max().strftime('%Y-%m-%d')}")
print(f"期间涨跌: {df['收盘'].iloc[-1] - df['收盘'].iloc[0]:+.2f} 元 ({((df['收盘'].iloc[-1] / df['收盘'].iloc[0]) - 1) * 100:+.2f}%)")
print(f"最高价: ¥{df['最高'].max():.2f} ({df[df['最高']==df['最高'].max()]['日期'].iloc[0].strftime('%Y-%m-%d')})")
print(f"最低价: ¥{df['最低'].min():.2f} ({df[df['最低']==df['最低'].min()]['日期'].iloc[0].strftime('%Y-%m-%d')})")
print(f"平均换手率: {df['成交量'].mean():.2f}%")
