#!/usr/bin/env python3
"""
福彩全玩法号码走势图生成工具
用法:
  python scripts/chart_generator.py --type <玩法> --hot-cold
  python scripts/chart_generator.py --type <玩法> --trend
  python scripts/chart_generator.py --type <玩法> --all
  python scripts/chart_generator.py --type <玩法> --output <dir>

玩法: ssq(双色球) fc3d(福彩3D) qlc(七乐彩) kl8(快乐8) 15x5(15选5)
"""

import csv
import os
import sys
from collections import Counter

import warnings
warnings.filterwarnings('ignore', message='Glyph.*missing from font')

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.font_manager as fm
import numpy as np

_FONT_PATH = '/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf'
if os.path.exists(_FONT_PATH):
    fm.fontManager.addfont(_FONT_PATH)
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Droid Sans Fallback']
plt.rcParams['axes.unicode_minus'] = False

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'references')

GAMES = {
    'ssq': {
        'name': '双色球', 'file': 'ssq-history.csv', 'pools': {'红球': 33, '蓝球': 16},
    },
    'fc3d': {
        'name': '福彩3D', 'file': 'fc3d-history.csv', 'pools': {'数字': 10},
    },
    'qlc': {
        'name': '七乐彩', 'file': 'qlc-history.csv', 'pools': {'号码': 30, '特别号': 1},
    },
    'kl8': {
        'name': '快乐8', 'file': 'kl8-history.csv', 'pools': {'号码': 80},
    },
    '15x5': {
        'name': '15选5', 'file': '15x5-history.csv', 'pools': {'号码': 15},
    },
}

REDS = list(range(1, 34))
BLUES = list(range(1, 17))
RED_LABELS = [f'{i:02d}' for i in REDS]
BLUE_LABELS = [f'{i:02d}' for i in BLUES]


def load_history(gtype='ssq'):
    game = GAMES.get(gtype, GAMES['ssq'])
    path = os.path.join(DATA_DIR, game['file'])
    if not os.path.exists(path):
        print(f"⚠️ 数据文件不存在: {path}")
        return []
    rows = []
    with open(path, 'r') as f:
        reader = csv.DictReader(f)
        for r in reader:
            row = {'phase': r['期号'], 'date': r.get('日期', '')}
            if gtype == 'ssq':
                row['reds'] = sorted([int(r[f'红球{i}']) for i in range(1, 7)])
                row['blue'] = int(r['蓝球'])
            elif gtype == 'fc3d':
                row['digits'] = [int(r['百位']), int(r['十位']), int(r['个位'])]
            elif gtype == 'qlc':
                row['numbers'] = sorted([int(r[f'号码{i}']) for i in range(1, 8)])
            elif gtype == 'kl8':
                row['numbers'] = sorted([int(r[f'号码{i}']) for i in range(1, 21)])
            elif gtype == '15x5':
                row['numbers'] = sorted([int(r[f'号码{i}']) for i in range(1, 6)])
            rows.append(row)
    return rows


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def autolabel_bars(ax, rects):
    for rect in rects:
        h = rect.get_height()
        if h > 0:
            ax.annotate(f'{int(h)}', xy=(rect.get_x() + rect.get_width() / 2, h),
                        xytext=(0, 2), textcoords="offset points", ha='center', fontsize=6)


def chart_hot_cold(data, output_dir, gtype='ssq'):
    game_name = GAMES[gtype]['name']

    if gtype == 'ssq':
        _chart_ssq_hot_cold(data, output_dir, game_name)
    elif gtype == 'fc3d':
        _chart_fc3d_hot_cold(data, output_dir, game_name)
    elif gtype == 'qlc' or gtype == '15x5':
        _chart_pool_hot_cold(data, output_dir, game_name, gtype)
    elif gtype == 'kl8':
        _chart_kl8_hot_cold(data, output_dir, game_name)
    else:
        print(f"⚠️ {game_name}暂不支持冷热号图表")


def _chart_ssq_hot_cold(data, output_dir, game_name):
    red_all, blue_all = [], []
    for r in data:
        red_all.extend(r['reds'])
        blue_all.append(r['blue'])
    red_counter = Counter(red_all)
    blue_counter = Counter(blue_all)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 5))
    fig.suptitle(f'{game_name}号码频率分布', fontsize=16, fontweight='bold')

    red_freq = [red_counter.get(i, 0) for i in REDS]
    colors_red = ['#E74C3C' if f >= sorted(red_freq, reverse=True)[10] else
                  '#95A5A6' if f == 0 else '#3498DB' for f in red_freq]
    bars1 = ax1.bar(RED_LABELS, red_freq, color=colors_red, edgecolor='white', linewidth=0.5)
    ax1.set_title('红球频率', fontsize=13)
    ax1.set_xlabel('红球号码')
    ax1.set_ylabel('出现次数')
    ax1.tick_params(axis='x', rotation=90, labelsize=6)
    ax1.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    autolabel_bars(ax1, bars1)

    blue_freq = [blue_counter.get(i, 0) for i in BLUES]
    colors_blue = ['#E74C3C' if f >= sorted(blue_freq, reverse=True)[3] else
                   '#95A5A6' if f == 0 else '#2ECC71' for f in blue_freq]
    bars2 = ax2.bar(BLUE_LABELS, blue_freq, color=colors_blue, edgecolor='white', linewidth=0.5)
    ax2.set_title('蓝球频率', fontsize=13)
    ax2.set_xlabel('蓝球号码')
    ax2.set_ylabel('出现次数')
    ax2.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    autolabel_bars(ax2, bars2)

    plt.tight_layout()
    _save_chart(output_dir, 'hot-cold.png')


def _chart_fc3d_hot_cold(data, output_dir, game_name):
    fig, axes = plt.subplots(1, 4, figsize=(18, 5))
    fig.suptitle(f'{game_name}位选频率分布', fontsize=16, fontweight='bold')

    positions = [('百位', 0), ('十位', 1), ('个位', 2)]
    for label, pos in positions:
        counter = Counter(r['digits'][pos] for r in data)
        freq = [counter.get(i, 0) for i in range(10)]
        colors = ['#E74C3C' if f >= sorted(freq, reverse=True)[2] else '#3498DB' for f in freq]
        bars = axes[pos].bar(range(10), freq, color=colors, edgecolor='white', linewidth=0.5)
        axes[pos].set_title(f'{label}频率', fontsize=11)
        axes[pos].set_xticks(range(10))
        axes[pos].set_ylabel('出现次数')
        axes[pos].tick_params(labelsize=8)
        autolabel_bars(axes[pos], bars)

    all_digits = []
    for r in data:
        all_digits.extend(r['digits'])
    counter = Counter(all_digits)
    freq = [counter.get(i, 0) for i in range(10)]
    colors = ['#E74C3C' if f >= sorted(freq, reverse=True)[3] else '#8E44AD' for f in freq]
    bars = axes[3].bar(range(10), freq, color=colors, edgecolor='white', linewidth=0.5)
    axes[3].set_title('综合频率', fontsize=11)
    axes[3].set_xticks(range(10))
    axes[3].set_ylabel('出现次数')
    axes[3].tick_params(labelsize=8)
    autolabel_bars(axes[3], bars)

    plt.tight_layout()
    _save_chart(output_dir, 'hot-cold.png')


def _chart_pool_hot_cold(data, output_dir, game_name, gtype):
    if gtype == 'qlc':
        pool_size = 30
        name = '号码'
    else:
        pool_size = 15
        name = '号码'
    all_nums = []
    for r in data:
        all_nums.extend(r['numbers'])
    counter = Counter(all_nums)
    freq = [counter.get(i, 0) for i in range(1, pool_size + 1)]

    fig, ax = plt.subplots(figsize=(14, 5))
    fig.suptitle(f'{game_name}号码频率分布', fontsize=16, fontweight='bold')

    top_n = min(8, pool_size)
    colors = ['#E74C3C' if f >= sorted(freq, reverse=True)[top_n] else
              '#95A5A6' if f == 0 else '#3498DB' for f in freq]
    labels = [f'{i:02d}' for i in range(1, pool_size + 1)]
    bars = ax.bar(labels, freq, color=colors, edgecolor='white', linewidth=0.5)
    ax.set_xlabel(f'{name}')
    ax.set_ylabel('出现次数')
    ax.tick_params(axis='x', rotation=90, labelsize=7)
    ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    autolabel_bars(ax, bars)

    plt.tight_layout()
    _save_chart(output_dir, 'hot-cold.png')


def _chart_kl8_hot_cold(data, output_dir, game_name):
    all_nums = []
    for r in data:
        all_nums.extend(r['numbers'])
    counter = Counter(all_nums)
    freq = [counter.get(i, 0) for i in range(1, 81)]
    sections = [freq[0:20], freq[20:40], freq[40:60], freq[60:80]]
    section_names = ['一区(01-20)', '二区(21-40)', '三区(41-60)', '四区(61-80)']

    fig, axes = plt.subplots(2, 2, figsize=(18, 10))
    fig.suptitle(f'{game_name}四分区频率分布', fontsize=16, fontweight='bold')

    for idx, (sec, name) in enumerate(zip(sections, section_names)):
        ax = axes[idx // 2][idx % 2]
        start = idx * 20 + 1
        labels = [f'{start+i:02d}' for i in range(20)]
        top_n = min(6, 20)
        colors = ['#E74C3C' if f >= sorted(sec, reverse=True)[top_n] else
                  '#95A5A6' if f == 0 else '#3498DB' for f in sec]
        bars = ax.bar(labels, sec, color=colors, edgecolor='white', linewidth=0.3)
        ax.set_title(name, fontsize=11)
        ax.tick_params(axis='x', rotation=90, labelsize=5)
        ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        autolabel_bars(ax, bars)

    plt.tight_layout()
    _save_chart(output_dir, 'hot-cold.png')


def _save_chart(output_dir, filename):
    path = os.path.join(output_dir, filename)
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"✅ 图表: {path}")


def chart_trend(data, output_dir, gtype='ssq'):
    if len(data) < 2:
        print("⚠️ 数据不足，无法绘制走势图")
        return
    game_name = GAMES[gtype]['name']

    if gtype == 'ssq':
        _chart_ssq_trend(data, output_dir, game_name)
    elif gtype == 'fc3d':
        _chart_fc3d_trend(data, output_dir, game_name)
    elif gtype == 'qlc' or gtype == '15x5':
        _chart_pool_trend(data, output_dir, game_name, gtype)
    elif gtype == 'kl8':
        _chart_kl8_trend(data, output_dir, game_name)
    else:
        print(f"⚠️ {game_name}暂不支持走势图表")


def _chart_ssq_trend(data, output_dir, game_name):
    phases = [r['phase'][-3:] for r in data]
    sums = [sum(r['reds']) for r in data]
    spans = [max(r['reds']) - min(r['reds']) for r in data]
    odds = [sum(1 for n in r['reds'] if n % 2 == 1) for r in data]

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 9))
    fig.suptitle(f'{game_name}走势图', fontsize=16, fontweight='bold')

    ax1.plot(phases, sums, color='#E74C3C', linewidth=1.5, marker='o', markersize=3)
    ax1.axhline(y=105, color='gray', linestyle='--', alpha=0.4)
    ax1.axhline(y=130, color='gray', linestyle='--', alpha=0.4)
    ax1.fill_between(range(len(phases)), sums, 105, alpha=0.1, color='#E74C3C')
    ax1.set_title('和值走势', fontsize=12)
    ax1.set_ylabel('和值')
    ax1.tick_params(axis='x', rotation=90, labelsize=6)
    ax1.set_ylim(min(sums) - 10, max(sums) + 10)

    ax2.plot(phases, spans, color='#3498DB', linewidth=1.5, marker='s', markersize=3)
    ax2.axhline(y=22, color='gray', linestyle='--', alpha=0.4)
    ax2.axhline(y=28, color='gray', linestyle='--', alpha=0.4)
    ax2.fill_between(range(len(phases)), spans, 22, alpha=0.1, color='#3498DB')
    ax2.set_title('跨度走势', fontsize=12)
    ax2.set_ylabel('跨度')
    ax2.tick_params(axis='x', rotation=90, labelsize=6)
    ax2.set_ylim(min(spans) - 3, max(spans) + 3)

    odd_labels = ['全偶', '1奇5偶', '2奇4偶', '3奇3偶', '4奇2偶', '5奇1偶', '全奇']
    odd_indices = [6 - o for o in odds]
    ax3.plot(phases, odd_indices, color='#9B59B6', linewidth=1.5, marker='^', markersize=3)
    ax3.set_title('奇偶走势', fontsize=12)
    ax3.set_ylabel('奇偶比')
    ax3.set_yticks(range(7))
    ax3.set_yticklabels(odd_labels, fontsize=8)
    ax3.tick_params(axis='x', rotation=90, labelsize=6)
    ax3.set_ylim(-0.5, 6.5)

    plt.tight_layout()
    _save_chart(output_dir, 'trend.png')


def _chart_fc3d_trend(data, output_dir, game_name):
    phases = [r['phase'][-3:] for r in data]
    nums = [int(''.join(str(d) for d in r['digits'])) for r in data]
    andzhi = [sum(r['digits']) for r in data]
    kuadu = [max(r['digits']) - min(r['digits']) for r in data]

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 9))
    fig.suptitle(f'{game_name}走势图', fontsize=16, fontweight='bold')

    ax1.plot(phases, nums, color='#E74C3C', linewidth=1, marker='o', markersize=3)
    ax1.set_title('直选号码走势', fontsize=12)
    ax1.set_ylabel('号码')
    ax1.tick_params(axis='x', rotation=90, labelsize=6)

    ax2.plot(phases, andzhi, color='#F39C12', linewidth=1.5, marker='s', markersize=4)
    ax2.axhline(y=13.5, color='gray', linestyle='--', alpha=0.4)
    ax2.fill_between(range(len(phases)), 8, 18, alpha=0.1, color='#F39C12')
    ax2.set_title('和值走势', fontsize=12)
    ax2.set_ylabel('和值')
    ax2.tick_params(axis='x', rotation=90, labelsize=6)
    ax2.set_ylim(0, 27)

    ax3.plot(phases, kuadu, color='#2ECC71', linewidth=1.5, marker='^', markersize=4)
    ax3.axhline(y=4.5, color='gray', linestyle='--', alpha=0.4)
    ax3.set_title('跨度走势', fontsize=12)
    ax3.set_ylabel('跨度')
    ax3.tick_params(axis='x', rotation=90, labelsize=6)
    ax3.set_ylim(0, 9)

    plt.tight_layout()
    _save_chart(output_dir, 'trend.png')


def _chart_pool_trend(data, output_dir, game_name, gtype):
    phases = [r['phase'][-3:] for r in data]
    sums = [sum(r['numbers']) for r in data]
    spans = [max(r['numbers']) - min(r['numbers']) for r in data]
    odds = [sum(1 for n in r['numbers'] if n % 2 == 1) for r in data]
    pick_count = len(data[0]['numbers']) if data else 1

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 9))
    fig.suptitle(f'{game_name}走势图', fontsize=16, fontweight='bold')

    if gtype == 'qlc':
        avg_sum, min_v, max_v = 100, 28, 189
    else:
        avg_sum, min_v, max_v = 40, 15, 65
    ax1.plot(phases, sums, color='#E74C3C', linewidth=1.5, marker='o', markersize=3)
    ax1.axhline(y=avg_sum, color='gray', linestyle='--', alpha=0.4)
    ax1.fill_between(range(len(phases)), sums, avg_sum, alpha=0.1, color='#E74C3C')
    ax1.set_title('和值走势', fontsize=12)
    ax1.set_ylabel('和值')
    ax1.tick_params(axis='x', rotation=90, labelsize=6)

    ax2.plot(phases, spans, color='#3498DB', linewidth=1.5, marker='s', markersize=3)
    ax2.set_title('跨度走势', fontsize=12)
    ax2.set_ylabel('跨度')
    ax2.tick_params(axis='x', rotation=90, labelsize=6)

    odd_labels = ['全偶'] + [f'{i}奇{pick_count-i}偶' for i in range(1, pick_count)] + ['全奇']
    ax3.plot(phases, odds, color='#9B59B6', linewidth=1.5, marker='^', markersize=3)
    ax3.set_title('奇偶走势', fontsize=12)
    ax3.set_ylabel('奇数个数')
    ax3.tick_params(axis='x', rotation=90, labelsize=6)
    ax3.set_ylim(0, pick_count)

    plt.tight_layout()
    _save_chart(output_dir, 'trend.png')


def _chart_kl8_trend(data, output_dir, game_name):
    phases = [r['phase'][-3:] for r in data]
    sect1 = [sum(1 for n in r['numbers'] if 1 <= n <= 20) for r in data]
    sect2 = [sum(1 for n in r['numbers'] if 21 <= n <= 40) for r in data]
    sect3 = [sum(1 for n in r['numbers'] if 41 <= n <= 60) for r in data]
    sect4 = [sum(1 for n in r['numbers'] if 61 <= n <= 80) for r in data]
    span = [max(r['numbers']) - min(r['numbers']) for r in data]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8))
    fig.suptitle(f'{game_name}走势图', fontsize=16, fontweight='bold')

    x = range(len(phases))
    ax1.plot(phases, sect1, color='#E74C3C', linewidth=1, marker='o', markersize=2, label='一区(01-20)')
    ax1.plot(phases, sect2, color='#3498DB', linewidth=1, marker='s', markersize=2, label='二区(21-40)')
    ax1.plot(phases, sect3, color='#2ECC71', linewidth=1, marker='^', markersize=2, label='三区(41-60)')
    ax1.plot(phases, sect4, color='#F39C12', linewidth=1, marker='D', markersize=2, label='四区(61-80)')
    ax1.legend(loc='upper right', fontsize=8)
    ax1.set_title('四分区出号数走势', fontsize=12)
    ax1.set_ylabel('出号数')
    ax1.tick_params(axis='x', rotation=90, labelsize=6)

    ax2.plot(phases, span, color='#9B59B6', linewidth=1.5, marker='o', markersize=3)
    ax2.axhline(y=75, color='gray', linestyle='--', alpha=0.4)
    ax2.fill_between(x, span, alpha=0.1, color='#9B59B6')
    ax2.set_title('跨度走势', fontsize=12)
    ax2.set_ylabel('跨度')
    ax2.tick_params(axis='x', rotation=90, labelsize=6)
    ax2.set_ylim(min(span) - 5, 79)

    plt.tight_layout()
    _save_chart(output_dir, 'trend.png')


def chart_distribution(data, output_dir, gtype='ssq'):
    game_name = GAMES[gtype]['name']

    if gtype == 'ssq':
        _chart_ssq_distribution(data, output_dir, game_name)
    elif gtype == 'fc3d':
        _chart_fc3d_distribution(data, output_dir, game_name)
    elif gtype == 'qlc':
        _chart_qlc_distribution(data, output_dir, game_name)
    elif gtype == 'kl8':
        _chart_kl8_distribution(data, output_dir, game_name)
    elif gtype == '15x5':
        _chart_15x5_distribution(data, output_dir, game_name)
    else:
        print(f"⚠️ {game_name}暂不支持分布图表")


def _chart_ssq_distribution(data, output_dir, game_name):
    for d in data:
        d['section'] = (sum(1 for n in d['reds'] if 1 <= n <= 11),
                        sum(1 for n in d['reds'] if 12 <= n <= 22),
                        sum(1 for n in d['reds'] if 23 <= n <= 33))
    sections = [r['section'] for r in data]
    sec_labels = [f'{s[0]}:{s[1]}:{s[2]}' for s in sections]
    sec_counter = Counter(sec_labels)
    top_sec = sec_counter.most_common(8)
    big_small = [(sum(1 for n in r['reds'] if n <= 16),
                  sum(1 for n in r['reds'] if n >= 17)) for r in data]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle(f'{game_name}分布分析', fontsize=16, fontweight='bold')

    labels = [s[0] for s in top_sec]
    values = [s[1] for s in top_sec]
    colors_pie = plt.cm.Set3(np.linspace(0, 1, len(labels)))
    wedges, texts, autotexts = ax1.pie(
        values, labels=labels, autopct='%1.0f%%', colors=colors_pie,
        startangle=90, pctdistance=0.75
    )
    for t in autotexts:
        t.set_fontsize(9)
    ax1.set_title('区间比分布', fontsize=12)

    bs_counter = Counter(bs for bs in big_small)
    bs_labels = [f'{b}:{s}' for b, s in bs_counter.keys()]
    bs_values = list(bs_counter.values())
    bars = ax2.barh(bs_labels, bs_values, color=['#3498DB', '#2ECC71', '#F39C12', '#9B59B6', '#E74C3C'][:len(bs_labels)])
    ax2.set_title('大小比分布', fontsize=12)
    ax2.set_xlabel('出现次数')
    for bar, v in zip(bars, bs_values):
        ax2.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height() / 2,
                 str(v), va='center', fontsize=10)

    plt.tight_layout()
    _save_chart(output_dir, 'distribution.png')


def _chart_fc3d_distribution(data, output_dir, game_name):
    andzhi_counter = Counter(sum(r['digits']) for r in data)
    kuadu_counter = Counter(max(r['digits']) - min(r['digits']) for r in data)

    def type_of(row):
        d = row['digits']
        if d[0] == d[1] == d[2]:
            return '豹子'
        elif d[0] == d[1] or d[1] == d[2] or d[0] == d[2]:
            return '组三'
        else:
            return '组六'
    type_counter = Counter(type_of(r) for r in data)
    def road(row):
        return ''.join(str(n % 3) for n in row['digits'])
    road_counter = Counter(road(r) for r in data)

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle(f'{game_name}分布分析', fontsize=16, fontweight='bold')

    labels = ['组六', '组三', '豹子']
    values = [type_counter.get(t, 0) for t in labels]
    colors_pie = ['#3498DB', '#F39C12', '#E74C3C']
    ax1.pie(values, labels=labels, autopct='%1.0f%%', colors=colors_pie, startangle=90)
    ax1.set_title('形态分布', fontsize=12)

    top_roads = road_counter.most_common(10)
    bars = ax2.barh([r[0] for r in top_roads], [r[1] for r in top_roads],
                    color='#2ECC71', edgecolor='white')
    ax2.set_title('012路分布 TOP10', fontsize=12)
    ax2.set_xlabel('次数')
    for bar, v in zip(bars, [r[1] for r in top_roads]):
        ax2.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height() / 2,
                 str(v), va='center', fontsize=10)

    andzhi_vals = [andzhi_counter.get(i, 0) for i in range(28)]
    bars3 = ax3.bar(range(28), andzhi_vals, color='#9B59B6', edgecolor='white', width=0.8)
    ax3.set_title('和值分布', fontsize=12)
    ax3.set_xlabel('和值')
    ax3.set_xticks(range(0, 28, 3))
    ax3.tick_params(labelsize=8)

    kuadu_vals = [kuadu_counter.get(i, 0) for i in range(10)]
    bars4 = ax4.bar(range(10), kuadu_vals, color='#E67E22', edgecolor='white', width=0.8)
    ax4.set_title('跨度分布', fontsize=12)
    ax4.set_xlabel('跨度')
    ax4.tick_params(labelsize=8)

    plt.tight_layout()
    _save_chart(output_dir, 'distribution.png')


def _chart_qlc_distribution(data, output_dir, game_name):
    for d in data:
        d['section'] = (sum(1 for n in d['numbers'] if 1 <= n <= 10),
                        sum(1 for n in d['numbers'] if 11 <= n <= 20),
                        sum(1 for n in d['numbers'] if 21 <= n <= 30))
    sections = [r['section'] for r in data]
    sec_labels = [f'{s[0]}:{s[1]}:{s[2]}' for s in sections]
    sec_counter = Counter(sec_labels)
    big_small = [(sum(1 for n in r['numbers'] if n <= 15),
                  sum(1 for n in r['numbers'] if n >= 16)) for r in data]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle(f'{game_name}分布分析', fontsize=16, fontweight='bold')

    top_sec = sec_counter.most_common(8)
    labels = [s[0] for s in top_sec]
    values = [s[1] for s in top_sec]
    colors_pie = plt.cm.Set3(np.linspace(0, 1, len(labels)))
    ax1.pie(values, labels=labels, autopct='%1.0f%%', colors=colors_pie, startangle=90, pctdistance=0.75)
    ax1.set_title('区间比分布', fontsize=12)

    bs_counter = Counter(bs for bs in big_small)
    bs_labels = [f'{b}:{s}' for b, s in bs_counter.keys()]
    bs_values = list(bs_counter.values())
    bars = ax2.barh(bs_labels, bs_values, color=['#3498DB', '#2ECC71', '#F39C12', '#9B59B6', '#E74C3C'][:len(bs_labels)])
    ax2.set_title('大小比分布', fontsize=12)
    ax2.set_xlabel('出现次数')
    for bar, v in zip(bars, bs_values):
        ax2.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height() / 2,
                 str(v), va='center', fontsize=10)

    plt.tight_layout()
    _save_chart(output_dir, 'distribution.png')


def _chart_kl8_distribution(data, output_dir, game_name):
    sections = [(sum(1 for n in r['numbers'] if 1 <= n <= 20),
                 sum(1 for n in r['numbers'] if 21 <= n <= 40),
                 sum(1 for n in r['numbers'] if 41 <= n <= 60),
                 sum(1 for n in r['numbers'] if 61 <= n <= 80)) for r in data]

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(f'{game_name}四分区出号统计', fontsize=16, fontweight='bold')

    zone_names = ['一区(01-20)', '二区(21-40)', '三区(41-60)', '四区(61-80)']
    for idx, name in enumerate(zone_names):
        ax = axes[idx // 2][idx % 2]
        counter = Counter(s[idx] for s in sections)
        vals = [counter.get(i, 0) for i in range(11)]
        colors = ['#E74C3C' if i in [4, 5, 6] else '#3498DB' for i in range(11)]
        bars = ax.bar(range(11), vals, color=colors, edgecolor='white', width=0.8)
        ax.axhline(y=sorted(vals, reverse=True)[1] if sum(vals) > 0 else 0,
                   color='gray', linestyle='--', alpha=0.3)
        ax.set_title(name, fontsize=11)
        ax.set_xlabel('出号数')
        ax.set_xticks(range(11))
        ax.tick_params(labelsize=8)
        for bar, v in zip(bars, vals):
            if v > 0:
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
                        str(v), ha='center', fontsize=7)

    plt.tight_layout()
    _save_chart(output_dir, 'distribution.png')


def _chart_15x5_distribution(data, output_dir, game_name):
    big_small = [(sum(1 for n in r['numbers'] if n <= 8),
                  sum(1 for n in r['numbers'] if n >= 9)) for r in data]
    prime_count = [(sum(1 for n in r['numbers'] if n in (2, 3, 5, 7, 11, 13))) for r in data]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle(f'{game_name}分布分析', fontsize=16, fontweight='bold')

    bs_counter = Counter(bs for bs in big_small)
    bs_labels = [f'{b}:{s}' for b, s in bs_counter.keys()]
    bs_values = list(bs_counter.values())
    bars = ax1.barh(bs_labels, bs_values, color=['#3498DB', '#2ECC71', '#F39C12', '#9B59B6', '#E74C3C'][:len(bs_labels)])
    ax1.set_title('大小比分布', fontsize=12)
    ax1.set_xlabel('出现次数')
    for bar, v in zip(bars, bs_values):
        ax1.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height() / 2,
                 str(v), va='center', fontsize=10)

    pc_counter = Counter(prime_count)
    pc_vals = [pc_counter.get(i, 0) for i in range(6)]
    colors_pc = ['#3498DB', '#2ECC71', '#F39C12', '#9B59B6', '#E74C3C', '#E67E22']
    bars2 = ax2.bar(range(6), pc_vals, color=colors_pc, edgecolor='white', width=0.7)
    ax2.set_title('质数个数分布', fontsize=12)
    ax2.set_xticks(range(6))
    ax2.set_xticklabels([f'{i}个' for i in range(6)])
    ax2.tick_params(labelsize=9)
    for bar, v in zip(bars2, pc_vals):
        if v > 0:
            ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
                     str(v), ha='center', fontsize=9)

    plt.tight_layout()
    _save_chart(output_dir, 'distribution.png')


if __name__ == '__main__':
    gtype = 'ssq'
    if '--type' in sys.argv:
        idx = sys.argv.index('--type')
        if idx + 1 < len(sys.argv):
            gtype = sys.argv[idx + 1]
    if gtype not in GAMES:
        print(f"❌ 未知玩法: {gtype}")
        sys.exit(1)

    output_dir = os.path.join(os.path.dirname(__file__), '..', 'assets', 'charts', gtype)

    if '--output' in sys.argv:
        idx = sys.argv.index('--output')
        if idx + 1 < len(sys.argv):
            output_dir = sys.argv[idx + 1]

    data = load_history(gtype)
    if not data:
        sys.exit(1)

    game_name = GAMES[gtype]['name']
    ensure_dir(output_dir)
    print(f"📊 {game_name}走势图 -> {output_dir}")
    print(f"📈 数据期数: {len(data)}")

    if '--hot-cold' in sys.argv:
        chart_hot_cold(data, output_dir, gtype)
    elif '--trend' in sys.argv:
        chart_trend(data, output_dir, gtype)
    elif '--distribution' in sys.argv:
        chart_distribution(data, output_dir, gtype)
    elif '--all' in sys.argv or len(sys.argv) <= 3:
        chart_hot_cold(data, output_dir, gtype)
        chart_trend(data, output_dir, gtype)
        chart_distribution(data, output_dir, gtype)
        print(f"\n📁 所有图表已保存至: {output_dir}")
    else:
        print(f"用法: python scripts/chart_generator.py --type {gtype} [--hot-cold|--trend|--distribution|--all]")
