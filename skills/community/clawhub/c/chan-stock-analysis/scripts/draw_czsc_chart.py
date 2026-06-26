#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
draw_czsc_chart.py - 基于czsc框架的缠论可视化绘图
"""
import os
import sys
import json
import argparse
from datetime import datetime

# ============ 从 config.py 读取配置（支持环境变量覆盖） ============
import importlib.util as _ilu
_script_dir_early = os.path.dirname(os.path.abspath(__file__))
_cfg_spec = _ilu.spec_from_file_location(
    "chan_config",
    os.path.join(_script_dir_early, "config.py"),
)
_cfg = _ilu.module_from_spec(_cfg_spec)
_cfg_spec.loader.exec_module(_cfg)

# 强制使用Python实现
os.environ['CZSC_USE_PYTHON'] = '1'
sys.path.insert(0, _cfg.CZSC_PATH)

# 清理缓存
for m in list(sys.modules.keys()):
    if 'czsc' in m or 'rs_czsc' in m:
        del sys.modules[m]

from czsc import CZSC, Freq, format_standard_kline, ZS
from czsc.py.enum import Direction

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle

# ============ 配置 ============
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
CACHE_DIR = os.path.join(SCRIPT_DIR, 'cache')
OBSIDIAN_DIR = str(_cfg.OBSIDIAN_STOCK_DIR)  # 从配置读取，支持 OBSIDIAN_STOCK_DIR 环境变量

# 中文支持
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

LEVELS = [
    ('daily', 'Daily', Freq.D, 365),
    ('30',    '30min', Freq.F30, 253),
    ('5',     '5min', Freq.F5, 500),
    ('1',     '1min', Freq.F1, 500),
]

# ============ 数据加载 ============
def load_cache_bars(code: str, period: str):
    """从缓存加载K线"""
    cache_path = os.path.join(CACHE_DIR, f"{code}_{period}.json")
    if not os.path.exists(cache_path):
        return None
    
    with open(cache_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    klines = data.get('klines', [])
    if not klines:
        return None
    
    df = pd.DataFrame(klines)
    df['dt'] = pd.to_datetime(df['datetime'])
    df['symbol'] = code
    df['vol'] = df.get('volume', df.get('vol', 0))
    if 'amount' not in df.columns:
        df['amount'] = df['vol'] * df['close']
    
    freq_map = {'daily': Freq.D, '30': Freq.F30, '5': Freq.F5, '1': Freq.F1}
    freq = freq_map.get(period, Freq.D)
    
    bars = format_standard_kline(df[['symbol', 'dt', 'open', 'high', 'low', 'close', 'vol', 'amount']], freq=freq)
    return bars

def calc_macd(closes):
    """计算MACD"""
    if len(closes) < 34:
        return [], [], []
    
    ema_f = [sum(closes[:12]) / 12]
    for i in range(12, len(closes)):
        ema_f.append((closes[i] - ema_f[-1]) * 2 / 13 + ema_f[-1])
    
    ema_s = [sum(closes[:26]) / 26]
    for i in range(26, len(closes)):
        ema_s.append((closes[i] - ema_s[-1]) * 2 / 27 + ema_s[-1])
    
    ml = min(len(ema_f), len(ema_s))
    dif = [ema_f[i] - ema_s[i] for i in range(ml)]
    
    dea = [sum(dif[:9]) / 9]
    for i in range(9, len(dif)):
        dea.append((dif[i] - dea[-1]) * 2 / 10 + dea[-1])
    
    md = len(dea)
    hist = [(dif[i] - dea[i - md]) * 2 for i in range(md, len(dif))]
    
    return dif, dea, hist

def calc_ma(closes, period):
    """计算均线"""
    if len(closes) < period:
        return [None] * len(closes)
    ma = [None] * (period - 1)
    for i in range(period - 1, len(closes)):
        ma.append(sum(closes[i - period + 1:i + 1]) / period)
    return ma

# ============ 绘图函数 ============
def draw_level(ax, bars, czsc_obj, level_name, show_bi=True):
    """绘制单个级别的K线图"""
    n = len(bars)
    if n == 0:
        return
    
    # 提取数据
    dates = [b.dt for b in bars]
    opens = [b.open for b in bars]
    highs = [b.high for b in bars]
    lows = [b.low for b in bars]
    closes = [b.close for b in bars]
    
    # 计算指标
    dif, dea, hist = calc_macd(closes)
    ma5 = calc_ma(closes, 5)
    ma13 = calc_ma(closes, 13)
    ma34 = calc_ma(closes, 34)
    
    # 调整x轴范围
    x = range(n)
    
    # 绘制K线
    for i in range(n):
        color = '#DC143C' if closes[i] >= opens[i] else '#00CED1'
        # 实体
        body_bottom = min(opens[i], closes[i])
        body_height = abs(closes[i] - opens[i])
        if body_height < 0.01:
            body_height = 0.01
        rect = Rectangle((i - 0.3, body_bottom), 0.6, body_height,
                         facecolor=color, edgecolor=color, alpha=0.8)
        ax.add_patch(rect)
        # 上影线
        ax.plot([i, i], [highs[i], body_bottom + body_height], color=color, linewidth=0.5)
        # 下影线
        ax.plot([i, i], [lows[i], body_bottom], color=color, linewidth=0.5)
    
    # 绘制均线
    if ma5[-1] is not None:
        ma5_valid = [(i, v) for i, v in enumerate(ma5) if v is not None]
        if ma5_valid:
            ax.plot([x[0] for x in ma5_valid], [x[1] for x in ma5_valid], 
                   color='#FF6B6B', linewidth=1, label='MA5', alpha=0.8)
    
    if ma13[-1] is not None:
        ma13_valid = [(i, v) for i, v in enumerate(ma13) if v is not None]
        if ma13_valid:
            ax.plot([x[0] for x in ma13_valid], [x[1] for x in ma13_valid], 
                   color='#4ECDC4', linewidth=1, label='MA13', alpha=0.8)
    
    if ma34[-1] is not None:
        ma34_valid = [(i, v) for i, v in enumerate(ma34) if v is not None]
        if ma34_valid:
            ax.plot([x[0] for x in ma34_valid], [x[1] for x in ma34_valid], 
                   color='#FFE66D', linewidth=1, label='MA34', alpha=0.8)
    
    # 绘制笔
    if show_bi and czsc_obj and len(czsc_obj.bi_list) > 0:
        for bi in czsc_obj.bi_list[-20:]:  # 只画最近20笔
            # 找到对应的x坐标
            start_x = next((i for i, b in enumerate(bars) if b.dt >= bi.sdt), None)
            end_x = next((i for i, b in enumerate(bars) if b.dt >= bi.edt), None)
            if start_x is not None and end_x is not None:
                color = '#FF6B6B' if bi.direction == Direction.Up else '#4ECDC4'
                # 用分型的高低点画笔
                ax.plot([start_x, end_x], [bi.fx_a.fx, bi.fx_b.fx],
                       color=color, linewidth=2, alpha=0.7)
                # 标记端点
                ax.scatter([start_x], [bi.fx_a.fx], color=color, s=30, zorder=5)
                ax.scatter([end_x], [bi.fx_b.fx], color=color, s=30, zorder=5)
    
    # 绘制中枢
    if czsc_obj and len(czsc_obj.bi_list) >= 3:
        try:
            zs = ZS(bis=czsc_obj.bi_list[-3:])
            if zs.is_valid:
                # 中枢矩形
                zx = n - 50  # 画在中枢周期的中间位置
                if zx < 0:
                    zx = n // 4
                zw = 40
                rect = Rectangle((zx, zs.zd), zw, zs.zg - zs.zd,
                                facecolor='yellow', edgecolor='orange', 
                                linewidth=2, alpha=0.3)
                ax.add_patch(rect)
                ax.text(zx + zw/2, (zs.zd + zs.zg)/2, f'ZS\n{zs.zd:.1f}-{zs.zg:.1f}',
                       ha='center', va='center', fontsize=8, color='orange',
                       bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        except:
            pass
    
    # 设置标题
    cur_price = closes[-1]
    ax.set_title(f'{level_name} ({n} bars) | {cur_price:.2f}', 
                fontsize=12, fontweight='bold', loc='left')
    
    # 设置x轴
    tick_step = max(1, n // 10)
    tick_positions = list(range(0, n, tick_step))
    tick_labels = [dates[i].strftime('%m-%d') for i in tick_positions]
    ax.set_xticks(tick_positions)
    ax.set_xticklabels(tick_labels, rotation=45, fontsize=8)
    
    ax.set_xlim(-1, n)
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper right', fontsize=8)

def draw_macd(ax, bars):
    """绘制MACD"""
    closes = [b.close for b in bars]
    dif, dea, hist = calc_macd(closes)
    
    n = len(bars)
    offset = n - len(dif)
    m = len(hist)
    
    x = list(range(offset, offset + m))
    
    # 柱状图
    colors = ['#DC143C' if h >= 0 else '#00CED1' for h in hist]
    ax.bar(x, hist, color=colors, width=0.8, alpha=0.7)
    
    # DIF和DEA线
    dif_x = list(range(offset, offset + len(dif)))
    dea_x = list(range(offset, offset + len(dea)))
    ax.plot(dif_x, dif, color='#FF6B6B', linewidth=1, label='DIF')
    ax.plot(dea_x, dea, color='#4ECDC4', linewidth=1, label='DEA')
    
    ax.axhline(y=0, color='gray', linewidth=0.5)
    ax.set_title('MACD (12,26,9)', fontsize=10)
    ax.legend(loc='upper right', fontsize=8)
    ax.grid(True, alpha=0.3)

# ============ 主绘图函数 ============
def draw_chart(code: str, output_path: str):
    """绘制完整图表"""
    print(f"\nDrawing chart for {code}...")
    
    # 创建图形
    fig = plt.figure(figsize=(20, 16))
    
    # 子图布局: 4个级别K线 + 4个级别MACD
    gs = fig.add_gridspec(8, 1, height_ratios=[2,2,2,2, 0.5,0.5,0.5,0.5], hspace=0.3)
    
    level_axes = []
    macd_axes = []
    
    for i, (period, name, freq, expected) in enumerate(LEVELS):
        ax_k = fig.add_subplot(gs[i])
        ax_m = fig.add_subplot(gs[i + 4])
        level_axes.append(ax_k)
        macd_axes.append(ax_m)
    
    # 加载数据并绘制
    for i, (period, name, freq, expected) in enumerate(LEVELS):
        bars = load_cache_bars(code, period)
        if bars is None or len(bars) < 20:
            level_axes[i].text(0.5, 0.5, f'No data for {name}', 
                             ha='center', va='center', fontsize=14)
            continue
        
        czsc_obj = CZSC(bars)
        draw_level(level_axes[i], bars, czsc_obj, name)
        draw_macd(macd_axes[i], bars)
        
        print(f"  {name}: {len(bars)} bars, {len(czsc_obj.bi_list)} strokes")
    
    # 总标题
    fig.suptitle(f'CZSC Multi-Level Chan Theory Analysis\n{code} | {datetime.now().strftime("%Y-%m-%d %H:%M")}',
                fontsize=16, fontweight='bold', y=0.98)
    
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    
    # 保存
    plt.savefig(output_path, dpi=150, bbox_inches='tight', 
               facecolor='white', edgecolor='none')
    plt.close()
    
    print(f"\nChart saved: {output_path}")
    
    # 保存到Obsidian
    save_chart_to_obsidian(code, output_path)
    
    return output_path

def save_chart_to_obsidian(code: str, chart_path: str):
    """将图表保存到Obsidian仓库并上传到百度云"""
    from datetime import datetime
    import shutil
    import subprocess
    
    date_str = datetime.now().strftime('%Y-%m-%d')
    time_str = datetime.now().strftime('%H-%M-%S')
    # OBSIDIAN_DIR 已经是 D:\knowledge\stock，直接在下面创建日期目录
    obsidian_date_dir = os.path.join(OBSIDIAN_DIR, date_str)
    
    if not os.path.exists(obsidian_date_dir):
        os.makedirs(obsidian_date_dir, exist_ok=True)
    
    # 复制图表到Obsidian
    obsidian_chart = os.path.join(obsidian_date_dir, f"{date_str}_{time_str}_{code}_czsc_chart.png")
    shutil.copy(chart_path, obsidian_chart)
    
    print(f"Chart copied to Obsidian: {obsidian_chart}")
    
    # 上传到百度云
    try:
        remote_chart = f"/knowledge/{date_str}/{date_str}_{time_str}_{code}_czsc_chart.png"
        result = subprocess.run(
            ['bypy', 'upload', obsidian_chart, remote_chart],
            capture_output=True,
            timeout=60
        )
        if result.returncode == 0:
            print(f"Chart uploaded to Baidu Cloud: {remote_chart}")
        else:
            print(f"Upload failed: {result.stderr.decode('utf-8', errors='ignore')[:100]}")
    except Exception as e:
        print(f"Upload error: {e}")

# ============ 主函数 ============
def main(code: str, output_dir: str = None):
    """主函数"""
    if output_dir is None:
        output_dir = SKILL_DIR
    
    output_path = os.path.join(output_dir, f"output_{code}_czsc.png")
    draw_chart(code, output_path)
    return output_path

# ============ 命令行入口 ============
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CZSC-based Chan Theory Chart Drawing')
    parser.add_argument('--code', default='399006', help='Stock/Index code')
    parser.add_argument('--output', default=None, help='Output path')
    args = parser.parse_args()
    
    output = main(args.code, args.output)
    print(f"\nDone: {output}")
