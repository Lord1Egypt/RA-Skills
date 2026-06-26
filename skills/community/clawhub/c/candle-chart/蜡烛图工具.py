#!/usr/bin/env python3
"""蜡烛图工具 - 文字标注版"""
import akshare as ak
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# 设置字体
for f in matplotlib.font_manager.fontManager.ttflist:
    if 'Noto Sans CJK' in f.name:
        plt.rcParams['font.family'] = f.name
        break
    elif 'UMing' in f.name:
        plt.rcParams['font.family'] = f.name
        break
plt.rcParams['axes.unicode_minus'] = False

# 配色 - 与压力支撑技能统一
BG = '#1A1A2E'  # 深蓝黑背景
COLORS = {
    'up': '#FF6B6B',        # 珊瑚红 - 上涨
    'down': '#4ECDC4',     # 青绿色 - 下跌
    'ma5': '#FF6B6B',     # 珊瑚红
    'ma10': '#FFE66D',    # 明黄色
    'ma20': '#4ECDC4',    # 青绿色
    
    # 信号颜色
    'morning': '#4ECDC4',   # 青绿色 - 早晨星
    'evening': '#FF6B6B',   # 珊瑚红 - 黄昏星
    'bull_eng': '#4ECDC4',  # 青绿色 - 看涨吞没
    'darkcloud': '#FF6B6B', # 珊瑚红 - 乌云盖顶
    'hammer': '#FFE66D',    # 明黄色 - 锤子线
    'shooting': '#FF6B6B',  # 珊瑚红 - 流星线
    'piercing': '#4ECDC4',  # 青绿色 - 刺透
    'grid': '#3D3D5C',     # 网格线
    'spine': '#5C5C7A',    # 边框
}

# 信号文字
SIGNALS = {
    'morning': '早',
    'evening': '昏',
    'bull_eng': '吞↑',
    'darkcloud': '乌',
    'piercing': '刺',
    'hammer': '锤',
    'shooting': '流',
}

def judge_hammer(o, c, h, l, scale=0.03):
    body = abs(c - o)
    full = h - l
    full = np.where(full == 0, 1e-6, full)
    lower_shadow = np.where(o > c, o - l, c - l)
    return (body < scale * full) & (lower_shadow > body * 2.5)

def judge_shooting_star(o, c, h, l, scale=0.03):
    body = abs(c - o)
    full = h - l
    full = np.where(full == 0, 1e-6, full)
    upper_shadow = np.where(o > c, h - o, h - c)
    return (body < scale * full) & (upper_shadow > body * 2.5)

def judge_engulfing(o, c, h, l):
    """吞没形态 - 与原版一致，有前一天实体>16%限制"""
    p = np.roll(c, 1)
    po = np.roll(o, 1)
    prev_h = np.roll(h, 1)
    prev_l = np.roll(l, 1)
    
    # 颜色相反
    curr_red = c > o
    prev_red = p > po
    cond_color = curr_red != prev_red
    cond_color[0] = False
    
    # 完全包覆
    curr_max = np.maximum(o, c)
    curr_min = np.minimum(o, c)
    prev_max = np.maximum(po, p)
    prev_min = np.minimum(po, p)
    cond_engulf = (curr_max > prev_max) & (curr_min < prev_min)
    
    # 前一天实体>16%（防误判）
    body = abs(po - p)
    full = prev_h - prev_l
    full = np.where(full == 0, 1e-6, full)
    cond_prev = body > 0.16 * full
    
    # 返回合并结果，颜色在调用处判断
    return cond_color & cond_engulf & cond_prev

def judge_darkcloud(o, c, h, l):
    """乌云盖顶 - 与原版一致"""
    prev_s = np.roll(c, 1)
    prev_k = np.roll(o, 1)
    prev_h = np.roll(h, 1)
    prev_l = np.roll(l, 1)
    
    prev_body = prev_s - prev_k
    cond1 = o > prev_s  # 高开
    cond2 = c < prev_s - 0.5 * prev_body  # 收盘深入实体一半以下
    cond3 = prev_s > prev_k  # 前一天阳线
    
    # 前一天实体>16%（防误判）
    body = abs(prev_k - prev_s)
    full = prev_h - prev_l
    full = np.where(full == 0, 1e-6, full)
    cond4 = body > 0.16 * full
    
    result = cond1 & cond2 & cond3 & cond4
    result[0] = False
    return result

def judge_piercing(o, c, h, l):
    """刺透形态 - 与原版一致"""
    prev_s = np.roll(c, 1)
    prev_k = np.roll(o, 1)
    prev_h = np.roll(h, 1)
    prev_l = np.roll(l, 1)
    
    prev_body = prev_s - prev_k
    cond1 = o < prev_s  # 低开
    cond2 = c > prev_s - 0.5 * prev_body  # 收盘进入实体一半以上
    cond3 = prev_s < prev_k  # 前一天阴线
    
    # 前一天实体>16%（防误判）
    body = abs(prev_k - prev_s)
    full = prev_h - prev_l
    full = np.where(full == 0, 1e-6, full)
    cond4 = body > 0.16 * full
    
    result = cond1 & cond2 & cond3 & cond4
    result[0] = False
    return result

def judge_morning_star(o, c, h, l):
    """早晨之星 - 加入第一天实体>16%防误判"""
    n = len(o)
    bull = np.zeros(n, dtype=bool)
    for i in range(2, n):
        body2 = abs(o[i-1] - c[i-1])
        full2 = h[i-1] - l[i-1]
        
        # 第一天实体>16%（防误判）
        body1 = abs(o[i-2] - c[i-2])
        full1 = h[i-2] - l[i-2]
        if full1 > 0 and body1 < 0.16 * full1:
            continue
            
        if full2 > 0 and c[i-2] < o[i-2] and body2 < 0.3 * full2 and c[i] > o[i] and c[i] > (o[i-2] + c[i-2]) / 2:
            bull[i] = True
    return bull

def judge_evening_star(o, c, h, l):
    """黄昏之星 - 加入第一天实体>16%防误判"""
    n = len(o)
    bear = np.zeros(n, dtype=bool)
    for i in range(2, n):
        body2 = abs(o[i-1] - c[i-1])
        full2 = h[i-1] - l[i-1]
        
        # 第一天实体>16%（防误判）
        body1 = abs(o[i-2] - c[i-2])
        full1 = h[i-2] - l[i-2]
        if full1 > 0 and body1 < 0.16 * full1:
            continue
            
        if full2 > 0 and c[i-2] > o[i-2] and body2 < 0.3 * full2 and c[i] < o[i] and c[i] < (o[i-2] + c[i-2]) / 2:
            bear[i] = True
    return bear

STOCK_NAMES = {
    '600585': '海螺水泥',
    '600989': '宝丰能源',
    '600987': '航民股份',
    '600519': '贵州茅台',
    '000001': '平安银行',
}

def get_stock_name(code):
    try:
        df = ak.stock_individual_info_em(symbol='sh'+code.replace('.XSHG', '').replace('.XSHE', ''))
        for _, row in df.iterrows():
            if row.get('item') == '股票简称':
                return row.get('value', code)
    except:
        pass
    return STOCK_NAMES.get(code.replace('.XSHG', '').replace('.XSHE', ''), code)

def plot(code, days=90):
    stock_name = get_stock_name(code)
    
    # 动态计算日期
    import datetime
    end_date = datetime.datetime.now().strftime('%Y%m%d')
    start_date = (datetime.datetime.now() - datetime.timedelta(days=180)).strftime('%Y%m%d')
    
    df = ak.stock_zh_a_hist_tx(symbol='sh'+code, start_date=start_date, end_date=end_date)
    df = df.rename(columns={'开盘': 'open', '收盘': 'close', '最高': 'high', '最低': 'low', '成交量': 'amount'})
    df = df.tail(days).reset_index(drop=True)

    o = df['open'].values
    c = df['close'].values
    h = df['high'].values
    l = df['low'].values
    v = df['amount'].values

    # 形态判断
    Jhammer = judge_hammer(o, c, h, l)
    Jshooting = judge_shooting_star(o, c, h, l)
    engulf = judge_engulfing(o, c, h, l)
    bull_eng = engulf & (c > o)  # 上涨吞没
    bear_eng = engulf & (c < o)  # 下跌吞没
    Jdark = judge_darkcloud(o, c, h, l)
    Jpierce = judge_piercing(o, c, h, l)
    Jmorning = judge_morning_star(o, c, h, l)
    Jevening = judge_evening_star(o, c, h, l)

    # 绘图 - 信号带加宽
    fig = plt.figure(figsize=(16, 9))
    gs = fig.add_gridspec(3, 1, height_ratios=[3, 0.35, 1], hspace=0.08)
    
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1])
    ax3 = fig.add_subplot(gs[2])
    
    fig.patch.set_facecolor(BG)
    ax1.set_facecolor(BG)
    ax2.set_facecolor(BG)
    ax3.set_facecolor(BG)

    # K线
    width = 0.7
    for i in range(len(c)):
        if c[i] >= o[i]:
            ax1.add_patch(plt.Rectangle((i - width/2, o[i]), width, c[i] - o[i], 
                                         color=COLORS['up'], edgecolor=COLORS['up'], linewidth=0.3))
            ax1.plot([i, i], [c[i], h[i]], color=COLORS['up'], lw=0.8)
            ax1.plot([i, i], [l[i], o[i]], color=COLORS['up'], lw=0.8)
        else:
            ax1.add_patch(plt.Rectangle((i - width/2, c[i]), width, o[i] - c[i], 
                                         color=COLORS['down'], edgecolor=COLORS['down'], linewidth=0.3))
            ax1.plot([i, i], [o[i], h[i]], color=COLORS['down'], lw=0.8)
            ax1.plot([i, i], [l[i], c[i]], color=COLORS['down'], lw=0.8)

    # 均线 - 调细调透明
    ma5 = pd.Series(c).rolling(5).mean()
    ma10 = pd.Series(c).rolling(10).mean()
    ma20 = pd.Series(c).rolling(20).mean()
    ax1.plot(range(len(c)), ma5, color=COLORS['ma5'], lw=1.2, alpha=0.5, label='MA5')
    ax1.plot(range(len(c)), ma10, color=COLORS['ma10'], lw=1.2, alpha=0.5, label='MA10')
    ax1.plot(range(len(c)), ma20, color=COLORS['ma20'], lw=1.2, alpha=0.5, label='MA20')

    # 早晨/黄昏/吞没特殊标注 - 三天横线+方向指示
    for i in range(2, len(c)):
        # 早晨之星：三天横线+上方五角星
        if Jmorning[i]:
            y_mid = (h[i-2] + l[i-1]) / 2
            ax1.plot([i-2, i], [y_mid, y_mid], color=COLORS['morning'], lw=2, alpha=0.8)
            ax1.scatter([i-1], [h[i-1] + (h[i-1]-l[i-1])*0.3], s=150, c=COLORS['morning'], marker='*', zorder=25, edgecolors='white', linewidths=0.5)
        
        # 黄昏之星：三天横线+下方五角星
        if Jevening[i]:
            y_mid = (l[i-2] + h[i-1]) / 2
            ax1.plot([i-2, i], [y_mid, y_mid], color=COLORS['evening'], lw=2, alpha=0.8)
            ax1.scatter([i-1], [l[i-1] - (h[i-1]-l[i-1])*0.3], s=150, c=COLORS['evening'], marker='*', zorder=25, edgecolors='white', linewidths=0.5)
        
        # 看涨吞没：三天横线+向上箭头
        if bull_eng[i]:
            y_mid = (min(l[i-2], l[i-1], l[i]) + max(h[i-2], h[i-1], h[i])) / 2
            ax1.plot([i-1, i], [y_mid, y_mid], color=COLORS['bull_eng'], lw=2, alpha=0.8)
            ax1.scatter([i-0.5], [y_mid + (h[i-1]-l[i-1])*0.4], s=120, c=COLORS['bull_eng'], marker='^', zorder=25, edgecolors='white', linewidths=0.5)
        
        # 看跌吞没：三天横线+向下箭头
        if bear_eng[i]:
            y_mid = (min(l[i-2], l[i-1], l[i]) + max(h[i-2], h[i-1], h[i])) / 2
            ax1.plot([i-1, i], [y_mid, y_mid], color=COLORS['darkcloud'], lw=2, alpha=0.8)
            ax1.scatter([i-0.5], [y_mid - (h[i-1]-l[i-1])*0.4], s=120, c=COLORS['darkcloud'], marker='v', zorder=25, edgecolors='white', linewidths=0.5)

    # 信号带 - 文字标注，错位避免重叠
    ax2.set_xlim(-1, len(c))
    ax2.set_ylim(0, 1)
    ax2.set_yticks([])
    
    # 添加垂直分割线（每10天）
    for i in range(0, len(c), 10):
        ax2.axvline(x=i, color='#ccc', lw=0.5, alpha=0.5)
    
    # 信号位置映射 - 避免重叠
    # 早晨/黄昏在第二天(idx-1)标注
    
    for idx in range(len(c)):
        signals_at_idx = []
        
        # 早晨之星：判断在第3天(idx)，标注在第2天(idx-1)
        if idx > 0 and Jmorning[idx]:
            signals_at_idx.append(('早', COLORS['morning']))
        # 黄昏之星：判断在第3天(idx)，标注在第2天(idx-1)
        if idx > 0 and Jevening[idx]:
            signals_at_idx.append(('昏', COLORS['evening']))
        # 其他形态在当天标注
        if idx > 0 and bull_eng[idx-1]:
            signals_at_idx.append(('吞↑', COLORS['bull_eng']))
        if idx > 0 and Jdark[idx-1]:
            signals_at_idx.append(('乌', COLORS['darkcloud']))
        if idx > 0 and Jpierce[idx-1]:
            signals_at_idx.append(('刺', COLORS['piercing']))
        if idx > 0 and Jhammer[idx-1]:
            signals_at_idx.append(('锤', COLORS['hammer']))
        if idx > 0 and Jshooting[idx-1]:
            signals_at_idx.append(('流', COLORS['shooting']))
        if idx > 0 and bear_eng[idx-1]:
            signals_at_idx.append(('吞↓', COLORS['darkcloud']))
        
        # 多个信号时上下错开排列
        if len(signals_at_idx) > 0:
            # 早晨/黄昏标注在第二天(idx-1)，其他在当天
            draw_idx = idx - 1 if (len(signals_at_idx) == 1 and 
                                (signals_at_idx[0][0] in ['早', '昏'])) else idx
            for j, (text, color) in enumerate(signals_at_idx):
                if len(signals_at_idx) == 1:
                    ax2.text(draw_idx, 0.5, text, fontsize=8, ha='center', va='center',
                            color=color, fontweight='bold', alpha=0.9)
                else:
                    # 上下错开
                    y_offset = (j - (len(signals_at_idx)-1)/2) * 0.25
                    ax2.text(draw_idx, 0.5 + y_offset, text, fontsize=8, ha='center', va='center',
                            color=color, fontweight='bold', alpha=0.9)

    # 最后一天形态预测
    last_idx = len(c) - 1
    predictions = []
    if bull_eng[last_idx]: predictions.append(("吞↑", COLORS["bull_eng"]))
    if bear_eng[last_idx]: predictions.append(("吞↓", COLORS["darkcloud"]))
    if Jdark[last_idx]: predictions.append(("乌", COLORS["darkcloud"]))
    if Jpierce[last_idx]: predictions.append(("刺", COLORS["piercing"]))
    if Jhammer[last_idx]: predictions.append(("锤", COLORS["hammer"]))
    if Jshooting[last_idx]: predictions.append(("流", COLORS["shooting"]))
    if Jmorning[last_idx]: predictions.append(("早", COLORS["morning"]))
    if Jevening[last_idx]: predictions.append(("昏", COLORS["evening"]))
    
    if predictions:
        pred_text = " ".join([p[0] for p in predictions])
        ax2.text(len(c)-1, 0.9, f"({pred_text})", fontsize=7, ha="right", va="top",
                color="#666", fontweight="normal", alpha=0.8)

    # 成交量
    ax3.set_xlim(-1, len(c))
    ax3.set_ylabel('成交量', color='white', fontsize=9)
    ax3.tick_params(colors='white', labelsize=8)
    ax3.set_xticks([])
    v_colors = [COLORS['up'] if c[i] >= o[i] else COLORS['down'] for i in range(len(c))]
    ax3.bar(range(len(c)), v / 10000, color=v_colors, alpha=0.5, width=0.75)
    ax3.grid(True, alpha=0.3, color=COLORS['grid'])

    # 统计
    total = sum([np.sum(Jhammer), np.sum(Jshooting), np.sum(bull_eng), np.sum(bear_eng),
                np.sum(Jdark), np.sum(Jpierce), np.sum(Jmorning), np.sum(Jevening)])

    # 坐标轴 - 集中到价格区间
    ax1.set_xlim(-1, len(c))
    price_min = min(l)
    price_max = max(h)
    price_range = price_max - price_min
    ax1.set_ylim(price_min - price_range * 0.08, price_max + price_range * 0.08)
    ax1.set_ylabel('价格 (CNY)', color='white', fontsize=11)
    ax1.tick_params(colors='white', labelsize=9)
    ax1.set_xticks([])
    
    # 标题
    ax1.set_title(f'{stock_name} ({code}) — 蜡烛图形态分析 | {days}个交易日 | 信号数: {total}', 
                  color='white', fontsize=14, pad=10, fontweight='bold')
    
    # 图例 - 只保留均线
    from matplotlib.patches import Patch
    legend_elements = [
        plt.Line2D([0], [0], color=COLORS['ma5'], lw=1.5, alpha=0.6, label='MA5'),
        plt.Line2D([0], [0], color=COLORS['ma10'], lw=1.5, alpha=0.6, label='MA10'),
        plt.Line2D([0], [0], color=COLORS['ma20'], lw=1.5, alpha=0.6, label='MA20'),
    ]
    ax1.legend(handles=legend_elements, loc='upper left', fontsize=9, facecolor=BG, 
               edgecolor=COLORS['grid'], labelcolor='white', ncol=1, framealpha=0.95)
    
    ax1.grid(True, alpha=0.3, color=COLORS['grid'])

    for ax in [ax1, ax2, ax3]:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_color(COLORS['spine'])
        ax.spines['left'].set_color(COLORS['spine'])

    plt.tight_layout()
    import os
    desktop = os.path.expanduser("~/Desktop")
    plt.savefig(f'{desktop}/{code}_蜡烛图.png', facecolor=BG, dpi=150, bbox_inches='tight')
    print(f"📊 图片已保存到: {desktop}/{code}_蜡烛图.png")
    
    print(f"✅ {stock_name} ({code}) - {total} signals")

if __name__ == '__main__':
    import sys
    code = sys.argv[1] if len(sys.argv) > 1 else '600585'
    days = int(sys.argv[2]) if len(sys.argv) > 2 else 60
    plot(code, days)
