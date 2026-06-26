#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建施工进度计划
生成标准工序的进度安排（JSON 格式）
"""

import argparse
import json
from datetime import datetime, timedelta

# 标准工序模板（可根据项目类型调整）
STANDARD_TASKS = [
    {"name": "前期准备", "duration": 7, "predecessors": []},
    {"name": "测量放线", "duration": 3, "predecessors": [0]},
    {"name": "土方开挖", "duration": 15, "predecessors": [1]},
    {"name": "基础垫层", "duration": 5, "predecessors": [2]},
    {"name": "基础钢筋", "duration": 10, "predecessors": [3]},
    {"name": "基础模板", "duration": 7, "predecessors": [3]},
    {"name": "基础混凝土", "duration": 5, "predecessors": [4, 5]},
    {"name": "基础验收", "duration": 3, "predecessors": [6]},
    {"name": "主体结构一层", "duration": 20, "predecessors": [7]},
    {"name": "主体结构二层", "duration": 20, "predecessors": [8]},
    {"name": "主体结构三层", "duration": 20, "predecessors": [9]},
    {"name": "砌体工程", "duration": 25, "predecessors": [10]},
    {"name": "屋面工程", "duration": 15, "predecessors": [10]},
    {"name": "门窗安装", "duration": 20, "predecessors": [11]},
    {"name": "装饰装修", "duration": 45, "predecessors": [12, 13]},
    {"name": "水电安装", "duration": 30, "predecessors": [11]},
    {"name": "室外工程", "duration": 20, "predecessors": [14]},
    {"name": "竣工验收", "duration": 8, "predecessors": [14, 15, 16]},
]


def create_schedule(project_name, start_date_str, duration_days=None):
    """创建进度计划"""
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    
    schedule = {
        "project_name": project_name,
        "start_date": start_date_str,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "tasks": []
    }
    
    task_dates = {}  # 记录每个任务的最早开始时间
    
    for idx, task_template in enumerate(STANDARD_TASKS):
        # 计算最早开始时间（基于前置任务）
        if task_template["predecessors"]:
            earliest_start = max(
                task_dates[pre_idx] + STANDARD_TASKS[pre_idx]["duration"]
                for pre_idx in task_template["predecessors"]
            )
        else:
            earliest_start = 0
        
        task_start = start_date + timedelta(days=earliest_start)
        task_end = task_start + timedelta(days=task_template["duration"] - 1)
        
        task_dates[idx] = earliest_start
        
        task = {
            "id": idx + 1,
            "name": task_template["name"],
            "duration": task_template["duration"],
            "start_date": task_start.strftime("%Y-%m-%d"),
            "end_date": task_end.strftime("%Y-%m-%d"),
            "predecessors": [p + 1 for p in task_template["predecessors"]],  # 转为 1-based
            "progress": 0,
            "status": "pending"
        }
        schedule["tasks"].append(task)
    
    # 计算总工期
    total_duration = max(td + STANDARD_TASKS[idx]["duration"] 
                        for idx, td in task_dates.items())
    schedule["total_duration"] = total_duration
    schedule["end_date"] = (start_date + timedelta(days=total_duration - 1)).strftime("%Y-%m-%d")
    
    return schedule


def main():
    parser = argparse.ArgumentParser(description="创建施工进度计划")
    parser.add_argument("--project-name", required=True, help="项目名称")
    parser.add_argument("--start-date", required=True, help="开始日期 (YYYY-MM-DD)")
    parser.add_argument("--duration", type=int, help="总工期 (天，可选)")
    parser.add_argument("--output", default="schedule.json", help="输出文件路径")
    
    args = parser.parse_args()
    
    schedule = create_schedule(args.project_name, args.start_date, args.duration)
    
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(schedule, f, ensure_ascii=False, indent=2)
    
    print(f"✓ 进度计划已创建：{args.output}")
    print(f"  项目名称：{schedule['project_name']}")
    print(f"  开始日期：{schedule['start_date']}")
    print(f"  结束日期：{schedule['end_date']}")
    print(f"  总工期：{schedule['total_duration']} 天")
    print(f"  工序数量：{len(schedule['tasks'])} 项")


if __name__ == "__main__":
    main()
