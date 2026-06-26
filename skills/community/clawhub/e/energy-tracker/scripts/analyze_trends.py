#!/usr/bin/env python3
"""
能量状态趋势分析脚本

功能：读取历史能量状态数据，识别多日模式并生成分析报告

授权方式: 无需外部API授权
"""

import json
import sys
from collections import Counter
from typing import Dict, List, Optional


def load_data(data_file: str) -> List[Dict]:
    """
    加载能量状态数据

    参数:
        data_file: JSON数据文件路径

    返回:
        数据记录列表，每条记录包含 date, answer, interpretation
    """
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if not isinstance(data, list):
            raise ValueError("数据文件格式错误：应为JSON数组")
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"数据文件不存在: {data_file}")
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON解析失败: {e}")


def sort_by_date(data: List[Dict]) -> List[Dict]:
    """
    按日期排序数据记录

    参数:
        data: 数据记录列表

    返回:
        按日期升序排列的记录列表
    """
    return sorted(data, key=lambda x: x.get('date', ''))


def check_consecutive_c(sorted_data: List[Dict]) -> int:
    """
    检测最近连续选择C的天数

    参数:
        sorted_data: 按日期排序的数据记录

    返回:
        最近连续C的天数
    """
    if not sorted_data:
        return 0

    # 从最近的记录开始统计
    consecutive_count = 0
    for record in reversed(sorted_data):
        if record.get('answer') == 'C':
            consecutive_count += 1
        else:
            break

    return consecutive_count


def identify_pattern(sorted_data: List[Dict]) -> Dict:
    """
    识别多日趋势模式

    参数:
        sorted_data: 按日期排序的数据记录

    返回:
        模式识别结果字典
    """
    if not sorted_data:
        return {
            "pattern": "no_data",
            "message": "暂无数据",
            "suggestion": "请先记录至少一天的能量状态",
            "consecutive_c": 0,
            "needs_intervention": False
        }

    # 检测连续C的天数（无论数据量多少都检测）
    consecutive_c = check_consecutive_c(sorted_data)
    needs_intervention = consecutive_c >= 3

    if len(sorted_data) < 7:
        return {
            "pattern": "insufficient_data",
            "message": f"当前有{len(sorted_data)}天数据，建议积累7天以上进行趋势分析",
            "suggestion": "继续每日记录，数据量充足后将提供更准确的趋势判断",
            "consecutive_c": consecutive_c,
            "needs_intervention": needs_intervention
        }

    # 统计各选项出现次数
    answers = [record.get('answer', '') for record in sorted_data]
    answer_count = Counter(answers)

    # 计算持续"是"的天数
    yes_count = answer_count.get('A', 0)
    yes_ratio = yes_count / len(sorted_data)

    # 计算低能量天数（B和C）
    low_energy_count = answer_count.get('B', 0) + answer_count.get('C', 0)
    low_energy_ratio = low_energy_count / len(sorted_data)

    # 判断是否反复波动（好一天坏一天）
    # 检查相邻记录是否频繁交替
    alternations = 0
    for i in range(len(answers) - 1):
        if answers[i] != answers[i + 1]:
            alternations += 1

    # 模式判断逻辑
    # 检测连续C的天数
    consecutive_c = check_consecutive_c(sorted_data)
    needs_intervention = consecutive_c >= 3

    if yes_ratio >= 0.8:  # 80%以上为"是"
        return {
            "pattern": "sustained_high",
            "message": "持续高心理韧性状态",
            "duration": f"{len(sorted_data)}天",
            "suggestion": "这是一个挑战新目标或学习新技能的好时机",
            "consecutive_c": consecutive_c,
            "needs_intervention": needs_intervention
        }
    elif low_energy_ratio >= 0.8 and len(sorted_data) >= 14:
        # 持续低能量超过2周
        return {
            "pattern": "sustained_low",
            "message": "预警信号，可能存在轻度抑郁或长期职业倦怠",
            "duration": f"{len(sorted_data)}天",
            "suggestion": "寻求专业干预。不要试图只靠意志力硬扛，建议咨询心理咨询师，或去医院评估神经递质水平",
            "consecutive_c": consecutive_c,
            "needs_intervention": needs_intervention
        }
    elif alternations >= len(answers) * 0.6:  # 60%以上的日子在波动
        return {
            "pattern": "fluctuating",
            "message": "反复波动，代表环境压力过载",
            "duration": f"{len(sorted_data)}天",
            "suggestion": "寻找压力源。是某个人还是某项工作在消耗你？尝试建立心理边界",
            "consecutive_c": consecutive_c,
            "needs_intervention": needs_intervention
        }
    elif low_energy_ratio >= 0.6:
        return {
            "pattern": "declining",
            "message": "整体能量呈下降趋势",
            "duration": f"{len(sorted_data)}天",
            "suggestion": "注意休息和调整，若持续低能量状态超过2周，建议寻求专业帮助",
            "consecutive_c": consecutive_c,
            "needs_intervention": needs_intervention
        }
    else:
        return {
            "pattern": "mixed",
            "message": "状态混合，整体较为稳定",
            "duration": f"{len(sorted_data)}天",
            "suggestion": "继续保持规律记录，关注能量变化趋势",
            "consecutive_c": consecutive_c,
            "needs_intervention": needs_intervention
        }


def main():
    """
    主函数：处理命令行参数并执行分析
    """
    if len(sys.argv) != 2:
        print(json.dumps({
            "error": "参数错误",
            "usage": "python3 analyze_trends.py <data_file.json>"
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    data_file = sys.argv[1]

    try:
        # 加载并分析数据
        data = load_data(data_file)
        sorted_data = sort_by_date(data)
        result = identify_pattern(sorted_data)

        # 添加数据统计信息
        result["total_days"] = len(sorted_data)
        result["data_summary"] = {
            "A": sum(1 for r in sorted_data if r.get('answer') == 'A'),
            "B": sum(1 for r in sorted_data if r.get('answer') == 'B'),
            "C": sum(1 for r in sorted_data if r.get('answer') == 'C')
        }

        # 输出结果
        print(json.dumps(result, ensure_ascii=False, indent=2))

    except Exception as e:
        print(json.dumps({
            "error": "分析失败",
            "message": str(e)
        }, ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
