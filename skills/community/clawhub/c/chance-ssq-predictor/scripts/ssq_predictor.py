# -*- coding: utf-8 -*-
"""
双色球分析预测工具 (SSQ Predictor)
提供遗漏值分析、频率统计、和值分析、号码生成等功能

使用方法:
    python ssq_predictor.py --analysis --recent 50 --generate 5
    python ssq_predictor.py --missing
    python ssq_predictor.py --frequency --recent 30
    python ssq_predictor.py --generate 10

免责声明: 彩票开奖是完全随机的独立事件，本工具仅供娱乐参考。
"""

import random
import argparse
import sys

# Windows 控制台 UTF-8 编码修复
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from datetime import datetime, timedelta
from collections import Counter

# ============================================================================
# 历史数据（最近100期模拟数据，用于统计分析）
# ============================================================================

HISTORY_DATA = [
    {"period": "2025030", "red": [3, 8, 12, 18, 22, 33], "blue": 11},
    {"period": "2025029", "red": [1, 9, 15, 19, 26, 30], "blue": 7},
    {"period": "2025028", "red": [4, 7, 14, 20, 25, 31], "blue": 14},
    {"period": "2025027", "red": [2, 11, 17, 23, 28, 32], "blue": 5},
    {"period": "2025026", "red": [5, 9, 13, 16, 27, 33], "blue": 9},
    {"period": "2025025", "red": [1, 6, 10, 19, 24, 29], "blue": 3},
    {"period": "2025024", "red": [3, 8, 15, 21, 26, 30], "blue": 12},
    {"period": "2025023", "red": [2, 7, 11, 18, 25, 31], "blue": 8},
    {"period": "2025022", "red": [4, 9, 14, 20, 27, 32], "blue": 6},
    {"period": "2025021", "red": [1, 5, 12, 17, 23, 28], "blue": 15},
    {"period": "2025020", "red": [6, 10, 16, 22, 26, 33], "blue": 4},
    {"period": "2025019", "red": [2, 8, 13, 19, 25, 30], "blue": 10},
    {"period": "2025018", "red": [3, 7, 11, 15, 24, 29], "blue": 2},
    {"period": "2025017", "red": [5, 9, 14, 18, 21, 31], "blue": 13},
    {"period": "2025016", "red": [1, 6, 12, 20, 27, 32], "blue": 7},
    {"period": "2025015", "red": [4, 8, 17, 22, 26, 30], "blue": 11},
    {"period": "2025014", "red": [2, 10, 15, 19, 23, 28], "blue": 5},
    {"period": "2025013", "red": [3, 7, 13, 16, 25, 33], "blue": 9},
    {"period": "2025012", "red": [5, 11, 18, 21, 29, 31], "blue": 3},
    {"period": "2025011", "red": [1, 6, 14, 20, 24, 32], "blue": 14},
    {"period": "2025010", "red": [4, 9, 12, 17, 22, 27], "blue": 6},
    {"period": "2025009", "red": [2, 8, 15, 19, 26, 30], "blue": 12},
    {"period": "2025008", "red": [3, 7, 11, 16, 23, 28], "blue": 8},
    {"period": "2025007", "red": [5, 10, 13, 18, 25, 31], "blue": 1},
    {"period": "2025006", "red": [1, 6, 14, 21, 29, 33], "blue": 15},
    {"period": "2025005", "red": [4, 9, 17, 20, 24, 32], "blue": 4},
    {"period": "2025004", "red": [2, 8, 12, 15, 22, 27], "blue": 10},
    {"period": "2025003", "red": [3, 7, 11, 19, 26, 30], "blue": 2},
    {"period": "2025002", "red": [5, 10, 14, 23, 28, 31], "blue": 13},
    {"period": "2025001", "red": [1, 6, 13, 18, 25, 29], "blue": 7},
    {"period": "2024150", "red": [4, 9, 16, 20, 27, 32], "blue": 11},
    {"period": "2024149", "red": [2, 8, 11, 17, 24, 30], "blue": 5},
    {"period": "2024148", "red": [3, 7, 15, 19, 22, 33], "blue": 9},
    {"period": "2024147", "red": [5, 10, 14, 21, 26, 31], "blue": 3},
    {"period": "2024146", "red": [1, 6, 12, 18, 23, 28], "blue": 14},
    {"period": "2024145", "red": [4, 9, 13, 16, 25, 32], "blue": 6},
    {"period": "2024144", "red": [2, 8, 17, 20, 27, 30], "blue": 12},
    {"period": "2024143", "red": [3, 7, 11, 15, 24, 29], "blue": 8},
    {"period": "2024142", "red": [5, 10, 14, 19, 22, 33], "blue": 1},
    {"period": "2024141", "red": [1, 6, 16, 21, 26, 31], "blue": 15},
    {"period": "2024140", "red": [4, 9, 12, 18, 23, 28], "blue": 4},
    {"period": "2024139", "red": [2, 8, 15, 20, 25, 30], "blue": 10},
    {"period": "2024138", "red": [3, 7, 11, 17, 22, 27], "blue": 2},
    {"period": "2024137", "red": [5, 10, 13, 19, 24, 32], "blue": 13},
    {"period": "2024136", "red": [1, 6, 14, 21, 29, 33], "blue": 7},
    {"period": "2024135", "red": [4, 9, 16, 18, 26, 31], "blue": 5},
    {"period": "2024134", "red": [2, 8, 12, 15, 23, 28], "blue": 11},
    {"period": "2024133", "red": [3, 7, 17, 20, 25, 30], "blue": 9},
    {"period": "2024132", "red": [5, 11, 14, 19, 22, 27], "blue": 3},
    {"period": "2024131", "red": [1, 6, 13, 16, 24, 32], "blue": 14},
    {"period": "2024130", "red": [4, 9, 15, 21, 26, 29], "blue": 6},
    {"period": "2024129", "red": [2, 8, 11, 18, 23, 31], "blue": 12},
    {"period": "2024128", "red": [3, 7, 14, 19, 25, 33], "blue": 8},
    {"period": "2024127", "red": [5, 10, 16, 20, 28, 30], "blue": 1},
    {"period": "2024126", "red": [1, 6, 12, 17, 22, 27], "blue": 15},
    {"period": "2024125", "red": [4, 9, 13, 21, 26, 32], "blue": 4},
    {"period": "2024124", "red": [2, 8, 15, 19, 24, 29], "blue": 10},
    {"period": "2024123", "red": [3, 7, 11, 16, 23, 31], "blue": 2},
    {"period": "2024122", "red": [5, 10, 14, 18, 25, 33], "blue": 13},
    {"period": "2024121", "red": [1, 6, 17, 20, 27, 30], "blue": 7},
    {"period": "2024120", "red": [4, 9, 12, 15, 22, 28], "blue": 5},
    {"period": "2024119", "red": [2, 8, 13, 19, 26, 32], "blue": 11},
    {"period": "2024118", "red": [3, 7, 11, 21, 24, 29], "blue": 9},
    {"period": "2024117", "red": [5, 10, 16, 18, 23, 31], "blue": 3},
    {"period": "2024116", "red": [1, 6, 14, 20, 25, 33], "blue": 14},
    {"period": "2024115", "red": [4, 9, 15, 17, 27, 30], "blue": 6},
    {"period": "2024114", "red": [2, 8, 12, 19, 22, 28], "blue": 12},
    {"period": "2024113", "red": [3, 7, 11, 16, 24, 32], "blue": 8},
    {"period": "2024112", "red": [5, 10, 13, 21, 26, 29], "blue": 1},
    {"period": "2024111", "red": [1, 6, 14, 18, 23, 31], "blue": 15},
    {"period": "2024110", "red": [4, 9, 17, 20, 25, 33], "blue": 4},
    {"period": "2024109", "red": [2, 8, 15, 19, 27, 30], "blue": 10},
    {"period": "2024108", "red": [3, 7, 11, 16, 22, 28], "blue": 2},
    {"period": "2024107", "red": [5, 10, 14, 21, 26, 32], "blue": 13},
    {"period": "2024106", "red": [1, 6, 12, 17, 24, 29], "blue": 7},
    {"period": "2024105", "red": [4, 9, 16, 19, 23, 31], "blue": 5},
    {"period": "2024104", "red": [2, 8, 13, 20, 25, 30], "blue": 11},
    {"period": "2024103", "red": [3, 7, 15, 18, 27, 33], "blue": 9},
    {"period": "2024102", "red": [5, 10, 11, 21, 22, 28], "blue": 3},
    {"period": "2024101", "red": [1, 6, 14, 16, 24, 32], "blue": 14},
    {"period": "2024100", "red": [4, 9, 12, 19, 26, 29], "blue": 6},
    {"period": "2024099", "red": [2, 8, 17, 20, 23, 31], "blue": 12},
    {"period": "2024098", "red": [3, 7, 13, 15, 25, 30], "blue": 8},
    {"period": "2024097", "red": [5, 10, 14, 18, 27, 33], "blue": 1},
    {"period": "2024096", "red": [1, 6, 11, 21, 22, 28], "blue": 15},
]

# ============================================================================
# 分析函数
# ============================================================================

def get_recent_data(n=50):
    """获取最近 n 期数据"""
    return HISTORY_DATA[:n]


def calc_ac_value(numbers):
    """计算 AC 值（号码复杂度）"""
    diffs = set()
    n = len(numbers)
    for i in range(n):
        for j in range(i + 1, n):
            diffs.add(abs(numbers[i] - numbers[j]))
    return len(diffs)


def calc_span(numbers):
    """计算跨度"""
    return max(numbers) - min(numbers)


def calc_sum_value(numbers):
    """计算和值"""
    return sum(numbers)


def calc_odd_even(numbers):
    """计算奇偶比"""
    odd = sum(1 for x in numbers if x % 2 == 1)
    return f"{odd}:{6 - odd}"


def calc_size_ratio(numbers):
    """计算大小比（小数1-16，大数17-33）"""
    small = sum(1 for x in numbers if x <= 16)
    return f"{small}:{6 - small}"


def calc_zone_ratio(numbers):
    """计算区间比（一区1-11，二区12-22，三区23-33）"""
    z1 = sum(1 for x in numbers if x <= 11)
    z2 = sum(1 for x in numbers if 12 <= x <= 22)
    z3 = sum(1 for x in numbers if x >= 23)
    return f"{z1}:{z2}:{z3}"


def calc_road_ratio(numbers):
    """计算012路比"""
    r0 = sum(1 for x in numbers if x % 3 == 0)
    r1 = sum(1 for x in numbers if x % 3 == 1)
    r2 = sum(1 for x in numbers if x % 3 == 2)
    return f"{r0}:{r1}:{r2}"


def has_consecutive(numbers, length=2):
    """检查是否有指定长度的连号"""
    sorted_nums = sorted(numbers)
    count = 1
    for i in range(len(sorted_nums) - 1):
        if sorted_nums[i + 1] == sorted_nums[i] + 1:
            count += 1
            if count >= length:
                return True
        else:
            count = 1
    return False


def get_consecutive_count(numbers):
    """获取连号组数"""
    sorted_nums = sorted(numbers)
    groups = 0
    count = 1
    for i in range(len(sorted_nums) - 1):
        if sorted_nums[i + 1] == sorted_nums[i] + 1:
            count += 1
        else:
            if count >= 2:
                groups += 1
            count = 1
    if count >= 2:
        groups += 1
    return groups


def analyze_missing(recent_data, all_data):
    """分析遗漏值"""
    total_periods = len(all_data)

    # 统计每个红球上次出现的位置
    red_last_appear = {}
    for idx, record in enumerate(all_data):
        for ball in record["red"]:
            red_last_appear[ball] = idx

    # 蓝球遗漏
    blue_last_appear = {}
    for idx, record in enumerate(all_data):
        blue_last_appear[record["blue"]] = idx

    # 当前遗漏值
    red_missing = {}
    for ball in range(1, 34):
        last_pos = red_last_appear.get(ball, total_periods)
        red_missing[ball] = total_periods - last_pos

    blue_missing = {}
    for ball in range(1, 17):
        last_pos = blue_last_appear.get(ball, total_periods)
        blue_missing[ball] = total_periods - last_pos

    return red_missing, blue_missing


def analyze_frequency(recent_data):
    """分析频率"""
    recent_n = len(recent_data)
    red_counter = Counter()
    blue_counter = Counter()

    for record in recent_data:
        for ball in record["red"]:
            red_counter[ball] += 1
        blue_counter[record["blue"]] += 1

    # 理论概率
    red_theory = recent_n * 6 / 33
    blue_theory = recent_n / 16

    return red_counter, blue_counter, red_theory, blue_theory


def analyze_sum_value(recent_data):
    """分析和值分布"""
    sum_values = [sum(r["red"]) for r in recent_data]
    return {
        "min": min(sum_values),
        "max": max(sum_values),
        "avg": round(sum(sum_values) / len(sum_values), 1),
        "values": sum_values
    }


def recommend_numbers(recent_data, count=5):
    """
    基于统计分析生成推荐号码组合
    结合遗漏值、频率、各项指标进行综合筛选
    """
    red_missing, blue_missing = analyze_missing(recent_data, HISTORY_DATA)
    red_freq, blue_freq, red_theory, blue_theory = analyze_frequency(recent_data)

    recommendations = []
    attempted = set()

    while len(recommendations) < count:
        # 计算每个红球的综合评分
        red_scores = {}
        for ball in range(1, 34):
            freq_ratio = red_freq.get(ball, 0) / red_theory if red_theory > 0 else 1
            missing_score = min(red_missing[ball] / 8, 1.5)  # 遗漏值加分

            # 012路均衡
            road = ball % 3
            road_balance = 0.8 + 0.2 * random.random()

            score = freq_ratio * 0.3 + missing_score * 0.3 + road_balance * 0.4
            # 加入随机性（因为彩票本质是随机的）
            score += random.uniform(0, 0.5)
            red_scores[ball] = score

        # 选择评分最高的号码（但保留随机性）
        scored_balls = sorted(red_scores.items(), key=lambda x: -x[1])
        # 随机从 top 候选中选择
        top_balls = [b for b, s in scored_balls[:15]]
        selected_red = sorted(random.sample(top_balls, 6))

        # 计算组合评分
        sum_val = calc_sum_value(selected_red)
        span_val = calc_span(selected_red)
        ac_val = calc_ac_value(selected_red)
        odd_even = calc_odd_even(selected_red)
        zone_ratio = calc_zone_ratio(selected_red)
        consec_count = get_consecutive_count(selected_red)

        # 筛选条件
        valid = True
        reasons = []

        # 和值范围
        if 60 <= sum_val <= 130:
            reasons.append(f"和值{sum_val}✓")
        else:
            valid = False

        # 跨度
        if 15 <= span_val <= 30:
            reasons.append(f"跨度{span_val}✓")
        else:
            valid = False

        # AC值
        if 6 <= ac_val <= 10:
            reasons.append(f"AC{ac_val}✓")
        else:
            valid = False

        # 奇偶比
        odd_count = sum(1 for x in selected_red if x % 2 == 1)
        if odd_count in [2, 3, 4]:
            reasons.append(f"奇偶{odd_even}✓")
        else:
            valid = False

        # 区间比（避免某一区为空）
        zone = [int(x) for x in zone_ratio.split(":")]
        if 0 not in zone:
            reasons.append(f"区间{zone_ratio}✓")
        else:
            valid = False

        # 唯一性检查
        key = tuple(selected_red)
        if key in attempted:
            valid = False
        attempted.add(key)

        if valid:
            # 蓝球选择（遗漏值较高优先）
            blue_scores = {}
            for ball in range(1, 17):
                ms = min(blue_missing.get(ball, 10) / 10, 1.5)
                fs = blue_freq.get(ball, 0) / blue_theory if blue_theory > 0 else 1
                blue_scores[ball] = ms * 0.6 + fs * 0.4 + random.uniform(0, 0.3)
            top_blue = sorted(blue_scores.items(), key=lambda x: -x[1])[:5]
            selected_blue = random.choice([b for b, s in top_blue])

            recommendations.append({
                "red": selected_red,
                "blue": selected_blue,
                "analysis": {
                    "sum": sum_val,
                    "span": span_val,
                    "ac": ac_val,
                    "odd_even": odd_even,
                    "size": calc_size_ratio(selected_red),
                    "zone": zone_ratio,
                    "road": calc_road_ratio(selected_red),
                    "consecutive": consec_count,
                    "reasons": reasons
                }
            })

    return recommendations


# ============================================================================
# 输出函数
# ============================================================================

def print_header(title):
    """打印标题"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


def print_red_balls(balls):
    """格式化红球输出"""
    return " ".join(f"{b:02d}" for b in balls)


def cmd_analysis(recent=50, generate=5):
    """综合分析模式"""
    recent_data = get_recent_data(recent)

    print_header("双色球综合分析报告")

    # 基本信息
    print(f"\n📊 数据范围: 最近 {recent} 期")
    print(f"📅 最新期号: {recent_data[0]['period']}")

    # 遗漏值分析
    red_missing, blue_missing = analyze_missing(recent_data, HISTORY_DATA)
    print_header("遗漏值分析")

    sorted_missing = sorted(red_missing.items(), key=lambda x: -x[1])
    print("\n🔴 红球遗漏值 TOP 10 (遗漏越多越冷):")
    for i, (ball, miss) in enumerate(sorted_missing[:10], 1):
        status = "【冷】" if miss > 8 else "【温】" if miss > 4 else "【热】"
        print(f"  {i:2d}. 球 {ball:02d}  遗漏 {miss:2d} 期  {status}")

    print("\n🔵 蓝球遗漏值:")
    for ball in range(1, 17):
        miss = blue_missing.get(ball, 0)
        status = "【冷】" if miss > 8 else "【温】" if miss > 4 else "【热】"
        print(f"  球 {ball:02d}: 遗漏 {miss:2d} 期 {status}")

    # 频率分析
    red_freq, blue_freq, red_theory, blue_theory = analyze_frequency(recent_data)
    print_header("频率统计（最近 {} 期）".format(recent))

    sorted_freq = sorted(red_freq.items(), key=lambda x: -x[1])
    print("\n🔴 红球出现频率 TOP 10:")
    for i, (ball, freq) in enumerate(sorted_freq[:10], 1):
        ratio = freq / red_theory if red_theory > 0 else 0
        bar = "█" * int(ratio * 3)
        status = "过热" if ratio > 1.3 else "过冷" if ratio < 0.7 else "正常"
        print(f"  {i:2d}. 球 {ball:02d} 出现 {freq:2d} 次  {bar}  {status}")

    # 和值分析
    sum_info = analyze_sum_value(recent_data)
    print_header("和值分析")
    print(f"\n📈 和值范围: {sum_info['min']} - {sum_info['max']}")
    print(f"📊 和值均值: {sum_info['avg']}")
    print(f"⭐ 黄金和值带: 75-110（历史高频区间）")
    recent_sums = sum_info['values'][:10]
    print(f"📋 最近10期和值: {' '.join(str(s) for s in recent_sums)}")

    # 形态统计
    print_header("形态统计（最近 {} 期）".format(recent))

    odd_even_stats = Counter()
    size_stats = Counter()
    zone_stats = Counter()
    ac_stats = Counter()

    for record in recent_data:
        red = record["red"]
        odd_even_stats[calc_odd_even(red)] += 1
        size_stats[calc_size_ratio(red)] += 1
        zone_stats[calc_zone_ratio(red)] += 1
        ac_stats[calc_ac_value(red)] += 1

    print("\n📊 奇偶比分布:")
    for k, v in sorted(odd_even_stats.items(), key=lambda x: -x[1]):
        pct = v / recent * 100
        bar = "█" * int(pct / 3)
        print(f"  {k}: {v:3d} 次 ({pct:5.1f}%) {bar}")

    print("\n📊 大小比分布:")
    for k, v in sorted(size_stats.items(), key=lambda x: -x[1]):
        pct = v / recent * 100
        bar = "█" * int(pct / 3)
        print(f"  {k}: {v:3d} 次 ({pct:5.1f}%) {bar}")

    print("\n📊 AC值分布:")
    for k in sorted(ac_stats.keys()):
        v = ac_stats[k]
        pct = v / recent * 100
        bar = "█" * int(pct / 2)
        print(f"  AC={k}: {v:3d} 次 ({pct:5.1f}%) {bar}")

    # 推荐号码
    if generate > 0:
        print_header(f"推荐号码组合（共 {generate} 注）")
        print("\n⚠️  免责声明: 彩票开奖完全随机，本推荐仅供娱乐参考，请理性购彩！\n")

        recs = recommend_numbers(recent_data, generate)

        for i, rec in enumerate(recs, 1):
            red_str = print_red_balls(rec["red"])
            analysis = rec["analysis"]
            print(f"【第 {i:02d} 注】红球: [{red_str}]  蓝球: {rec['blue']:02d}")
            print(f"         和值:{analysis['sum']}  跨度:{analysis['span']}  AC:{analysis['ac']}  "
                  f"奇偶:{analysis['odd_even']}  区间:{analysis['zone']}")
            print()


def cmd_missing():
    """遗漏值分析模式"""
    recent_data = get_recent_data(50)
    red_missing, blue_missing = analyze_missing(recent_data, HISTORY_DATA)

    print_header("遗漏值分析报告")

    print("\n🔴 红球遗漏值排名:")
    print(f"{'排名':<4} {'球号':<6} {'遗漏值':<8} {'状态':<8} {'建议'}")
    print("-" * 50)

    sorted_missing = sorted(red_missing.items(), key=lambda x: -x[1])
    for i, (ball, miss) in enumerate(sorted_missing, 1):
        if miss > 10:
            status = "极冷"
            suggestion = "可关注（回补潜力）"
        elif miss > 7:
            status = "较冷"
            suggestion = "观察"
        elif miss > 4:
            status = "温号"
            suggestion = "正常关注"
        else:
            status = "热号"
            suggestion = "谨慎追热"
        print(f"{i:<4} {ball:02d}号     {miss:<8} {status:<8} {suggestion}")

    print("\n🔵 蓝球遗漏值排名:")
    print(f"{'球号':<6} {'遗漏值':<8} {'状态':<8}")
    print("-" * 30)
    for ball in sorted(blue_missing.keys(), key=lambda x: -blue_missing[x]):
        miss = blue_missing[ball]
        status = "极冷" if miss > 12 else "较冷" if miss > 8 else "温号" if miss > 4 else "热号"
        print(f"{ball:02d}号     {miss:<8} {status}")


def cmd_frequency(recent=30):
    """频率统计模式"""
    recent_data = get_recent_data(recent)
    red_freq, blue_freq, red_theory, blue_theory = analyze_frequency(recent_data)

    print_header(f"频率统计报告（最近 {recent} 期）")

    print(f"\n理论期望: 每期每红球出现 {red_theory:.1f} 次")
    print(f"\n🔴 红球出现频率:")
    print(f"{'球号':<6} {'次数':<6} {'理论':<6} {'实际/理论':<10} {'评价'}")
    print("-" * 50)

    all_balls = list(range(1, 34))
    random.shuffle(all_balls)  # 打乱顺序，按实际频率排序
    sorted_balls = sorted(all_balls, key=lambda x: -red_freq.get(x, 0))

    for ball in sorted_balls:
        freq = red_freq.get(ball, 0)
        ratio = freq / red_theory if red_theory > 0 else 0
        if ratio > 1.5:
            eval_ = "🔥 过热"
        elif ratio > 1.1:
            eval_ = "📈 偏热"
        elif ratio >= 0.9:
            eval_ = "✅ 正常"
        elif ratio > 0.6:
            eval_ = "📉 偏冷"
        else:
            eval_ = "❄️ 过冷"
        print(f"{ball:02d}号     {freq:<6} {red_theory:<6.1f} {ratio:<10.2f} {eval_}")

    print(f"\n🔵 蓝球出现频率:")
    print(f"{'球号':<6} {'次数':<6} {'理论':<6} {'实际/理论':<10} {'评价'}")
    print("-" * 50)
    for ball in sorted(range(1, 17), key=lambda x: -blue_freq.get(x, 0)):
        freq = blue_freq.get(ball, 0)
        ratio = freq / blue_theory if blue_theory > 0 else 0
        if ratio > 1.5:
            eval_ = "🔥 过热"
        elif ratio > 1.1:
            eval_ = "📈 偏热"
        elif ratio >= 0.9:
            eval_ = "✅ 正常"
        elif ratio > 0.6:
            eval_ = "📉 偏冷"
        else:
            eval_ = "❄️ 过冷"
        print(f"{ball:02d}号     {freq:<6} {blue_theory:<6.1f} {ratio:<10.2f} {eval_}")


def cmd_generate(count=5):
    """号码生成模式"""
    recent_data = get_recent_data(50)
    recs = recommend_numbers(recent_data, count)

    print_header("双色球推荐号码")
    print("\n⚠️  仅供参考娱乐，开奖完全随机，请理性购彩！\n")

    for i, rec in enumerate(recs, 1):
        red_str = print_red_balls(rec["red"])
        a = rec["analysis"]
        print(f"┌─────────────────────────────────────────────┐")
        print(f"│  第 {i:02d} 注                                        │")
        print(f"│  红球: {red_str}                       │")
        print(f"│  蓝球: {rec['blue']:02d}                                        │")
        print(f"├─────────────────────────────────────────────┤")
        print(f"│  和值: {a['sum']:<3}  跨度: {a['span']:<2}  AC: {a['ac']:<2}              │")
        print(f"│  奇偶: {a['odd_even']}  大小: {a['size']}                     │")
        print(f"│  区间: {a['zone']}  012路: {a['road']}                     │")
        print(f"│  连号: {a['consecutive']}组                                  │")
        print(f"└─────────────────────────────────────────────┘")
        print()


def cmd_blue():
    """蓝球分析模式"""
    recent_data = get_recent_data(50)
    blue_missing, _ = analyze_missing(recent_data, HISTORY_DATA)
    _, blue_freq, _, blue_theory = analyze_frequency(recent_data)

    print_header("蓝球分析报告")

    print("\n🔵 蓝球遗漏值与频率综合分析:")
    print(f"{'球号':<5} {'遗漏值':<8} {'出现次数':<8} {'热度':<10} {'推荐度'}")
    print("-" * 50)

    for ball in range(1, 17):
        miss = blue_missing.get(ball, 0)
        freq = blue_freq.get(ball, 0)

        # 热度评分
        heat_score = miss / 10 + freq / blue_theory
        if heat_score > 1.8:
            heat = "🔥🔥🔥 极热"
            rec = "★★★☆☆ 优先"
        elif heat_score > 1.4:
            heat = "🔥🔥 较热"
            rec = "★★☆☆☆ 推荐"
        elif heat_score > 1.0:
            heat = "🔥 正常"
            rec = "★☆☆☆☆ 可选"
        else:
            heat = "❄️ 偏冷"
            rec = "☆☆☆☆☆ 观望"

        print(f"{ball:02d}号   {miss:<8} {freq:<8} {heat:<12} {rec}")


# ============================================================================
# 主程序
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="双色球分析预测工具 | 仅供参考娱乐，请理性购彩",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python ssq_predictor.py --analysis --recent 50 --generate 5
  python ssq_predictor.py --missing
  python ssq_predictor.py --frequency --recent 30
  python ssq_predictor.py --generate 10
  python ssq_predictor.py --blue
        """
    )

    parser.add_argument("--analysis", action="store_true", help="综合分析模式")
    parser.add_argument("--missing", action="store_true", help="遗漏值分析模式")
    parser.add_argument("--frequency", action="store_true", help="频率统计模式")
    parser.add_argument("--generate", type=int, metavar="N", default=0, help="生成 N 注推荐号码")
    parser.add_argument("--blue", action="store_true", help="蓝球分析模式")
    parser.add_argument("--recent", type=int, default=50, help="分析最近 N 期数据（默认50）")
    parser.add_argument("--sumvalue", action="store_true", help="和值分析模式")

    args = parser.parse_args()

    # 默认执行综合分析
    if not any([args.analysis, args.missing, args.frequency, args.generate, args.blue, args.sumvalue]):
        args.analysis = True

    if args.analysis:
        cmd_analysis(recent=args.recent, generate=args.generate)
    elif args.missing:
        cmd_missing()
    elif args.frequency:
        cmd_frequency(recent=args.recent)
    elif args.sumvalue:
        recent_data = get_recent_data(args.recent)
        sum_info = analyze_sum_value(recent_data)
        print_header(f"和值分析（最近 {args.recent} 期）")
        print(f"\n和值范围: {sum_info['min']} - {sum_info['max']}")
        print(f"和值均值: {sum_info['avg']}")
        print(f"历史推荐和值带: 75-110")
        print(f"\n最近10期和值序列:")
        print(" ".join(str(s) for s in sum_info['values'][:10]))
    elif args.blue:
        cmd_blue()
    else:
        cmd_generate(count=args.generate)


if __name__ == "__main__":
    main()
