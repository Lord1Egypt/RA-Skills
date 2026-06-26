#!/usr/bin/env python3
"""
analyze_day.py - 分析当日数据

功能:
- 读取今日交互笔记提取关键指标
- 计算完成率、能量状态、问题点、计划偏差度
- 输出结构化分析报告（供用户查看）
"""

import sys
import os
from datetime import datetime
import json
import re
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from config import NOTE_BASE_DIR, DAILY_RECORDER_SUBDIR

def get_current_note_path():
    """查找今日笔记路径"""
    
    today = datetime.now().date()
    
    notes_dir = os.path.join(NOTE_BASE_DIR, DAILY_RECORDER_SUBDIR)
    
    if not os.path.exists(notes_dir):
        return None
    
    matching_files = [f for f in os.listdir(notes_dir) 
                      if f.startswith(today.strftime('%Y-%m-%d'))]
    
    if not matching_files:
        return None
    
    note_path = os.path.join(notes_dir, matching_files[0])
    
    with open(note_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    return content

def extract_completion_rates(content):
    """提取完成率字段"""
    
    # 搜索各任务完成率
    patterns = [
        r'文案生成.*?:\s*\[\s*([0-9]+)\s*\%\]',
        r'润色优化.*?:\s*\[\s*([0-9]+)\s*\%\]',
        r'其他事项.*?:\s*\[\s*([0-9]+)\s*\%\]'
    ]
    
    results = {}
    for pattern in patterns:
        match = re.search(pattern, content)
        if match:
            # 提取任务名称（从上下文）
            task_name_match = re.search(r'(\w+.*?:)', content.split(match.group(0))[0][-30:])
            task_name = task_name_match.group(1).strip()[:-1] if task_name_match else "未知任务"
            results[task_name] = int(match.group(1))
    
    return results

def extract_energy_score(content):
    """提取能量评分"""
    
    patterns = [
        r'总体评分.*?:\s*\[\s*([1-5])',
        r'评分.*?:\s*\[([1-5])',
        r'能量状态.*?:\s*\[评分\s*([1-5])'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, content)
        if match:
            return int(match.group(1))
    
    return None

def extract_barriers(content):
    """提取问题点列表"""
    
    # 搜索「遇到的问题」字段下的条目
    barrier_section = re.search(r'遇到的问题.*?\n([^#]+)', content)
    if not barrier_section:
        return []
    
    section_content = barrier_section.group(1)
    
    barriers = [line.strip() for line in section_content.split('\n') 
                if line.strip().startswith('-') and '具体阻碍' not in line]
    
    # 过滤占位符文本
    valid_barriers = [b for b in barriers if '待记录' not in b and 'N/A' not in b]
    
    return valid_barriers

def analyze_plan_deviation(content):
    """分析计划偏差度"""
    
    # 原计划 vs 实际执行字段对比
    original_plan = re.search(r'原计划.*?:\s*([^\n]+)', content)
    actual_execution = re.search(r'实际执行.*?:\s*([^\n]+)', content)
    
    if not original_plan or not actual_execution:
        return {
            "status": "无法计算", 
            "reason": "缺少原计划或实际执行记录"
        }
    
    orig_text = original_plan.group(1).strip()
    actual_text = actual_execution.group(1).strip()
    
    # 简单文本差异分析（非精确量化）
    if orig_text == actual_text:
        deviation_percent = 0
        status = "完全按计划 ✓"
    elif len(orig_text) > len(actual_text):
        deviation_percent = max(15, (len(orig_text) - len(actual_text)) * 5)
        status = "部分完成 ⚠️"
    else:
        deviation_percent = min(20, len(actual_text) * 2)
        status = "额外插入任务 ⚠️"
    
    return {
        "original_plan": orig_text,
        "actual_execution": actual_text,
        "deviation_percent": deviation_percent,
        "status": status
    }

def generate_report(content):
    """生成分析报告"""
    
    completion_rates = extract_completion_rates(content)
    energy_score = extract_energy_score(content)
    barriers = extract_barriers(content)
    plan_deviation = analyze_plan_deviation(content)
    
    # 平均完成率计算（如有多个任务）
    avg_completion = sum(completion_rates.values()) / len(completion_rates) if completion_rates else None
    
    report = {
        "date": datetime.now().strftime('%Y-%m-%d'),
        "completion_metrics": {
            "rates_by_task": completion_rates,
            "average_rate": round(avg_completion, 1) if avg_completion else None,
            "status": "高完成度 ✓" if (avg_completion and avg_completion >= 80) 
                           else "中等完成度 ⚠️" if (avg_completion and avg_completion >= 50) 
                           else "低完成度 ✗" if completion_rates else "待记录"
        },
        "energy_status": {
            "score": energy_score,
            "interpretation": ["极累", "疲惫", "正常", "精力充沛", "满电状态"][energy_score-1] 
                             if energy_score else "待评分"
        },
        "barrier_identification": {
            "count": len(barriers),
            "list": barriers,
            "summary": f"共识别 {len(barriers)} 个问题点" if barriers else "未记录问题"
        },
        "plan_deviation": plan_deviation,
    }
    
    return report

def print_report(report):
    """输出结构化报告"""
    
    print("=" * 60)
    print("=== 今日分析报告 ===")
    print(f"日期：{report['date']}")
    print("=" * 60)
    
    print("\n【完成率分析】")
    for task, rate in report['completion_metrics']['rates_by_task'].items():
        print(f"  {task}: [{rate}%]")
    if report['completion_metrics']['average_rate']:
        print(f"  平均完成率：[{report['completion_metrics']['average_rate']}%]")
    print(f"  状态：{report['completion_metrics']['status']}")
    
    print("\n【能量状态】")
    print(f"  评分：{report['energy_status']['score']}")
    print(f"  解读：{report['energy_status']['interpretation']}")
    
    print("\n【问题点识别】")
    if report['barrier_identification']['count'] > 0:
        for barrier in report['barrier_identification']['list']:
            print(f"  - {barrier}")
    else:
        print("  未记录问题点")
    
    print("\n【计划偏差度】")
    if report['plan_deviation']['status'] != "无法计算":
        print(f"  原计划：{report['plan_deviation']['original_plan']}")
        print(f"  实际执行：{report['plan_deviation']['actual_execution']}")
        print(f"  偏差度：[{report['plan_deviation']['deviation_percent']}%]")
        print(f"  状态：{report['plan_deviation']['status']}")
    else:
        print(f"  {report['plan_deviation']['reason']}")
    
    print("=" * 60)

def main():
    """主流程"""
    
    content = get_current_note_path()
    
    if not content:
        print("✗ 今日笔记不存在或尚未完成记录")
        return
    
    report = generate_report(content)
    print_report(report)

if __name__ == "__main__":
    main()
