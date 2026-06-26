#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
藻类投喂计算脚本
根据日报数据计算投藻量
"""

import re
from typing import Dict, List, Tuple

# 藻类投喂标准数据
FEEDING_STANDARD = {
    "小池": {
        "T": [100, 100, 140, 150, 180, 190, 230, 280],
        "SR": [90, 100, 130, 140, 160, 170, 210, 250],
        "M": [90, 90, 130, 130, 150, 90, 160, 200],
        "YR": [90, 100, 130, 140, 160, 170, 210, 250]
    },
    "大池": {
        "T": [170, 170, 240, 250, 300, 320, 390, 470],
        "SR": [160, 170, 220, 240, 270, 290, 350, 420],
        "M": [150, 150, 220, 220, 250, 150, 270, 340],
        "YR": [160, 170, 220, 240, 270, 290, 350, 420]
    }
}

# 车间池子规格映射
POOL_SIZE = {
    "C1": "小池", "C3": "小池", "C5": "小池", "C7": "小池",
    "C2": "大池", "C4": "大池", "C6": "大池", "C8": "大池"
}


def parse_date(date_str: str) -> int:
    """
    解析日期字符串，返回日期数字（日）
    输入: "4 月 9 日" 或 "4月9日" → 输出：9
    """
    match = re.search(r'(\d+)\s*月\s*(\d+)\s*日', date_str)
    if match:
        return int(match.group(2))
    return 0


def parse_pool_range(pool_range: str) -> List[int]:
    """
    解析池号范围
    输入："1-6" 或 "5,8-14"
    输出：[1, 2, 3, 4, 5, 6] 或 [5, 8, 9, 10, 11, 12, 13, 14]
    """
    pools = []
    parts = pool_range.split(',')
    for part in parts:
        if '-' in part:
            start, end = map(int, part.split('-'))
            pools.extend(range(start, end + 1))
        else:
            pools.append(int(part))
    return pools


def parse_strain_code(code: str) -> str:
    """
    解析品系代码
    输入："T0120" 或 "SR0212" 或 "M0213"
    输出："T" 或 "SR" 或 "M"
    """
    match = re.match(r'^([A-Z]+)', code)
    if match:
        return match.group(1)
    return code


def parse_daily_report(report_text: str) -> List[Dict]:
    """
    解析日报数据
    输入：日报文本
    输出：解析后的数据列表，包含幼体日期信息
    """
    data = []
    lines = report_text.strip().split('\n')
    current_larvae_date = None  # 当前幼体日期

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # 检测幼体日期行：4 月 9 日幼体（N）或 4 月 9 日幼体（N-Z1）
        if '幼体' in line:
            match = re.search(r'(\d+) 月\s*(\d+) 日.*?幼体', line)
            if match:
                current_larvae_date = f"{match.group(1)}月{match.group(2)}日"
            continue

        # 跳过存苗标题行
        if '存苗' in line:
            continue

        # 解析数据行：C1:1-6,C2:1-2，T0120，计价 5600 万，5200
        # 先找到品系代码（字母开头的部分）
        parts = re.split(r'[，,]', line)
        
        # 找到品系代码的位置（包含字母和数字，如 T0120, SR0212, M0213, YR，不包含冒号）
        strain_index = -1
        strain_code = None
        for i, part in enumerate(parts):
            part = part.strip()
            # 品系代码以字母开头，后面跟数字，且不包含冒号
            if ':' not in part and re.match(r'^[A-Z]+\d+', part):
                strain_code = part
                strain_index = i
                break
        
        if not strain_code or strain_index < 1 or not current_larvae_date:
            continue
        
        strain = parse_strain_code(strain_code)
        larvae_day = parse_date(current_larvae_date)
        
        # 解析车间池号（品系之前的所有部分）
        pool_info_parts = parts[:strain_index]
        pool_info = ','.join(pool_info_parts).strip()
        pool_groups = pool_info.split(',')

        # 为每个车间池号组创建记录
        for group in pool_groups:
            if ':' not in group:
                continue

            workshop, pool_range = group.split(':')
            workshop = workshop.strip()
            pool_range = pool_range.strip()

            pools = parse_pool_range(pool_range)

            data.append({
                'workshop': workshop,
                'pools': pools,
                'strain': strain,
                'strain_code': strain_code,
                'larvae_day': larvae_day  # 幼体日期（日）
            })

    return data


def calculate_feeding_amount(data: List[Dict], target_day: int, period: str) -> Tuple[Dict[str, List[Dict]], Dict[str, List[Dict]]]:
    """
    计算投藻量
    输入:
        data: 解析后的日报数据
        target_day: 目标日期（日）
        period: 时间段 ("上午" 或 "下午")
    输出：(小海链藻数据，大海莲藻数据)
    
    规则：
    - 第 1-2 天投小海链藻
    - 第 3-4 天投大海莲藻
    - 超过 4 天不投藻
    """
    if period not in ["上午", "下午"]:
        raise ValueError("时间段必须是'上午'或'下午'")

    # 计算索引
    period_index = 0 if period == "上午" else 1

    # 按藻类类型分组
    small_algae = {}  # 小海链藻（第 1-2 天）
    large_algae = {}  # 大海莲藻（第 3-4 天）

    for item in data:
        workshop = item['workshop']
        pools = item['pools']
        strain = item['strain']
        larvae_day = item['larvae_day']

        # 计算投喂天数 = 目标日 - 幼体日 + 1
        feeding_day = target_day - larvae_day + 1

        # 超过 4 天不投藻
        if feeding_day < 1 or feeding_day > 4:
            continue

        # 获取池子规格
        pool_size = POOL_SIZE.get(workshop)
        if not pool_size:
            continue

        # 计算索引
        day_index = (feeding_day - 1) * 2 + period_index

        # 获取投藻量
        try:
            feeding_amount = FEEDING_STANDARD[pool_size][strain][day_index]
        except KeyError:
            continue

        # 根据投喂天数分配到小海链藻或大海莲藻
        if feeding_day <= 2:
            result_dict = small_algae
        else:
            result_dict = large_algae

        # 添加到结果
        if workshop not in result_dict:
            result_dict[workshop] = []

        result_dict[workshop].append({
            'pools': pools,
            'strain': strain,
            'amount': feeding_amount,
            'feeding_day': feeding_day
        })

    return small_algae, large_algae


def format_output(small_algae: Dict, large_algae: Dict, date: str, period: str) -> str:
    """
    格式化输出
    输入:
        small_algae: 小海链藻数据
        large_algae: 大海莲藻数据
        date: 日期
        period: 时间段
    输出：格式化的投藻量文本
    """
    output = f"{date}{period}投藻：\n"

    # 处理小海链藻
    small_total = 0
    small_items = []
    for workshop in small_algae:
        for item in small_algae[workshop]:
            pool_count = len(item['pools'])
            amount = item['amount']
            small_total += pool_count * amount
            small_items.append({
                'workshop': workshop,
                'pools': item['pools'],
                'strain': item['strain'],
                'amount': amount
            })

    if small_items:
        output += f"小海链藻（{small_total}L）：\n"
        # 按车间、品系、投藻量分组
        grouped = {}
        for item in small_items:
            key = (item['workshop'], item['strain'], item['amount'])
            if key not in grouped:
                grouped[key] = []
            grouped[key].extend(item['pools'])

        # 按车间排序输出
        workshops = sorted(set(item['workshop'] for item in small_items))
        for workshop in workshops:
            # 按池号范围排序
            workshop_items = []
            for key in sorted(grouped.keys()):
                if key[0] == workshop:
                    workshop, strain, amount = key
                    pools = sorted(grouped[key])
                    pool_ranges = merge_pool_ranges(pools)
                    pool_range_str = ','.join(pool_ranges)
                    workshop_items.append((pool_range_str, amount, pools[0]))
            # 按池号范围排序（按起始池号）
            workshop_items.sort(key=lambda x: x[2])
            for pool_range_str, amount, _ in workshop_items:
                output += f"{workshop}:{pool_range_str:<12} {amount}L/池\n"
            # 不同车间之间空一行
            if workshop != workshops[-1]:
                output += "\n"
        output += "\n"

    # 处理大海链藻
    large_total = 0
    large_items = []
    for workshop in large_algae:
        for item in large_algae[workshop]:
            pool_count = len(item['pools'])
            amount = item['amount']
            large_total += pool_count * amount
            large_items.append({
                'workshop': workshop,
                'pools': item['pools'],
                'strain': item['strain'],
                'amount': amount
            })

    if large_items:
        output += f"大海链藻（{large_total}L）：\n"
        # 按车间、品系、投藻量分组
        grouped = {}
        for item in large_items:
            key = (item['workshop'], item['strain'], item['amount'])
            if key not in grouped:
                grouped[key] = []
            grouped[key].extend(item['pools'])

        # 按车间排序输出
        workshops = sorted(set(item['workshop'] for item in large_items))
        for workshop in workshops:
            # 按池号范围排序
            workshop_items = []
            for key in sorted(grouped.keys()):
                if key[0] == workshop:
                    workshop, strain, amount = key
                    pools = sorted(grouped[key])
                    pool_ranges = merge_pool_ranges(pools)
                    pool_range_str = ','.join(pool_ranges)
                    workshop_items.append((pool_range_str, amount, pools[0]))
            # 按池号范围排序（按起始池号）
            workshop_items.sort(key=lambda x: x[2])
            for pool_range_str, amount, _ in workshop_items:
                output += f"{workshop}:{pool_range_str:<12} {amount}L/池\n"
            # 不同车间之间空一行
            if workshop != workshops[-1]:
                output += "\n"
        output += "\n"

    return output


def merge_pool_ranges(pools: List[int]) -> List[str]:
    """
    合并连续的池号为范围
    输入：[1, 2, 3, 5, 6, 7]
    输出：["1-3", "5-7"]
    """
    if not pools:
        return []

    pool_ranges = []
    start = pools[0]
    end = pools[0]

    for pool in pools[1:]:
        if pool == end + 1:
            end = pool
        else:
            if start == end:
                pool_ranges.append(f"{start}")
            else:
                pool_ranges.append(f"{start}-{end}")
            start = pool
            end = pool

    if start == end:
        pool_ranges.append(f"{start}")
    else:
        pool_ranges.append(f"{start}-{end}")

    return pool_ranges


def main():
    """
    主函数 - 示例用法
    """
    # 示例日报数据
    report_text = """
4 月 10 日 C 区存苗：
4 月 10 日幼体（N）
C2:3-6，T0211，计价 3700 万，3400
C2:7-11，SR0212，计价 5200 万，4800
C2:12-19，M0213，计价 8200 万，7600

4 月 9 日幼体（N-Z1）
C1:1-6,C2:1-2，T0120，计价 5600 万，5000
C1:7-12，T0128，计价 3800 万，3400
C1:13-19，T0211，计价 4300 万，3800
C1:20-27，SR0212，计价 4800 万，4300
C1:28-39，M0213，计价 7600 万，6800
"""

    # 解析日报
    data = parse_daily_report(report_text)

    # 计算 4 月 11 日的投藻量
    # 4 月 10 日幼体 → 4 月 11 日是第 2 天（小海链藻）
    # 4 月 9 日幼体 → 4 月 11 日是第 3 天（大海链藻）
    target_day = 11
    period = "上午"
    small_algae, large_algae = calculate_feeding_amount(data, target_day, period)

    # 格式化输出
    output = format_output(small_algae, large_algae, "4 月 11 日", period)
    print(output)


if __name__ == "__main__":
    main()
