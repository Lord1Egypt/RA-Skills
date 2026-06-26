#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新施工进度计划的实际进度
计算进度偏差并预警延期风险
"""

import argparse
import json
from datetime import datetime


def load_schedule(schedule_path):
    """加载进度计划"""
    with open(schedule_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_schedule(schedule, schedule_path):
    """保存进度计划"""
    with open(schedule_path, "w", encoding="utf-8") as f:
        json.dump(schedule, f, ensure_ascii=False, indent=2)


def update_task_progress(schedule, task_id, progress=None, status=None, 
                         actual_start=None, actual_end=None):
    """更新单个工序的进度"""
    task = None
    for t in schedule["tasks"]:
        if t["id"] == task_id:
            task = t
            break
    
    if not task:
        raise ValueError(f"未找到工序 ID: {task_id}")
    
    # 更新进度
    if progress is not None:
        if progress < 0 or progress > 100:
            raise ValueError("进度必须在 0-100 之间")
        task["progress"] = progress
    
    # 更新状态
    if status:
        task["status"] = status
    
    # 更新实际开始日期
    if actual_start:
        task["actual_start"] = actual_start
    
    # 更新实际完成日期
    if actual_end:
        task["actual_end"] = actual_end
        task["progress"] = 100
        task["status"] = "completed"
    
    return task


def calculate_schedule_variance(schedule):
    """计算进度偏差"""
    today = datetime.now().strftime("%Y-%m-%d")
    variance_report = {
        "check_date": today,
        "total_tasks": len(schedule["tasks"]),
        "completed_tasks": 0,
        "in_progress_tasks": 0,
        "pending_tasks": 0,
        "delayed_tasks": [],
        "overall_progress": 0
    }
    
    total_progress = 0
    
    for task in schedule["tasks"]:
        total_progress += task["progress"]
        
        if task["status"] == "completed" or task["progress"] == 100:
            variance_report["completed_tasks"] += 1
        elif task["progress"] > 0:
            variance_report["in_progress_tasks"] += 1
        else:
            variance_report["pending_tasks"] += 1
        
        # 检查是否延期
        if task["status"] != "completed" and task["progress"] < 100:
            if task["end_date"] < today:
                # 计划结束日期已过但未完成
                days_overdue = (datetime.strptime(today, "%Y-%m-%d") - 
                               datetime.strptime(task["end_date"], "%Y-%m-%d")).days
                variance_report["delayed_tasks"].append({
                    "task_id": task["id"],
                    "task_name": task["name"],
                    "plan_end_date": task["end_date"],
                    "current_progress": task["progress"],
                    "days_overdue": days_overdue,
                    "impact": f"影响后续 {len(task.get('successors', []))} 道工序"
                })
    
    variance_report["overall_progress"] = round(total_progress / len(schedule["tasks"]), 1)
    
    return variance_report


def generate_variance_report(variance_report):
    """生成偏差报告文本"""
    report = []
    report.append("# 进度偏差分析报告")
    report.append(f"\n**检查日期**: {variance_report['check_date']}")
    report.append(f"\n## 总体进度")
    report.append(f"- 总工序数：{variance_report['total_tasks']} 项")
    report.append(f"- 已完成：{variance_report['completed_tasks']} 项")
    report.append(f"- 进行中：{variance_report['in_progress_tasks']} 项")
    report.append(f"- 待开始：{variance_report['pending_tasks']} 项")
    report.append(f"- **整体进度**: {variance_report['overall_progress']}%")
    
    if variance_report["delayed_tasks"]:
        report.append(f"\n## ⚠️ 延期预警")
        report.append(f"发现 **{len(variance_report['delayed_tasks'])}** 道工序延期：\n")
        report.append("| 工序 ID | 工序名称 | 计划完成日期 | 当前进度 | 延期天数 | 影响 |")
        report.append("|--------|---------|-------------|---------|---------|------|")
        
        for task in variance_report["delayed_tasks"]:
            report.append(f"| {task['task_id']} | {task['task_name']} | {task['plan_end_date']} | "
                         f"{task['current_progress']}% | {task['days_overdue']} 天 | {task['impact']} |")
    else:
        report.append(f"\n## ✅ 进度正常")
        report.append("所有工序按计划进行，无延期。")
    
    return "\n".join(report)


def main():
    parser = argparse.ArgumentParser(description="更新施工进度计划")
    parser.add_argument("--schedule", required=True, help="进度计划文件路径")
    parser.add_argument("--task-id", type=int, help="工序 ID")
    parser.add_argument("--progress", type=int, help="完成进度 (0-100)")
    parser.add_argument("--status", choices=["pending", "in_progress", "completed", "suspended"],
                       help="工序状态")
    parser.add_argument("--actual-start", help="实际开始日期 (YYYY-MM-DD)")
    parser.add_argument("--actual-end", help="实际完成日期 (YYYY-MM-DD)")
    parser.add_argument("--check", action="store_true", help="仅检查进度偏差，不更新")
    parser.add_argument("--output", help="偏差报告输出路径")
    
    args = parser.parse_args()
    
    # 加载进度计划
    schedule = load_schedule(args.schedule)
    
    # 仅检查模式
    if args.check:
        variance = calculate_schedule_variance(schedule)
        report = generate_variance_report(variance)
        
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(report)
            print(f"✓ 偏差报告已保存：{args.output}")
        else:
            print(report)
        return
    
    # 更新模式
    if not args.task_id:
        print("❌ 更新模式需要指定 --task-id")
        return
    
    # 更新工序进度
    task = update_task_progress(
        schedule, 
        args.task_id,
        progress=args.progress,
        status=args.status,
        actual_start=args.actual_start,
        actual_end=args.actual_end
    )
    
    # 保存更新后的进度计划
    save_schedule(schedule, args.schedule)
    
    print(f"✓ 工序已更新:")
    print(f"  ID: {task['id']}")
    print(f"  名称：{task['name']}")
    print(f"  进度：{task['progress']}%")
    print(f"  状态：{task['status']}")
    
    # 自动检查偏差
    print(f"\n📊 进度偏差检查:")
    variance = calculate_schedule_variance(schedule)
    report = generate_variance_report(variance)
    
    if args.output:
        # 同时保存报告
        report_path = args.output.replace(".json", "_report.md")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"✓ 偏差报告已保存：{report_path}")
    else:
        print(report)


if __name__ == "__main__":
    main()
