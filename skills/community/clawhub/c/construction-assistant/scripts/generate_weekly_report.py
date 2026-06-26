#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成施工周报/月报
汇总周期内的进度、质量、安全、材料等情况
"""

import argparse
import json
from datetime import datetime, timedelta


def get_week_range(year, week):
    """获取指定年份第几周的开始和结束日期"""
    # 找到该年的第一天
    jan_first = datetime(year, 1, 1)
    # 计算第一个周一
    first_monday = jan_first + timedelta(days=(7 - jan_first.weekday()) % 7)
    # 计算目标周的周一
    week_start = first_monday + timedelta(weeks=week - 1)
    week_end = week_start + timedelta(days=6)
    return week_start, week_end


def load_daily_logs(logs_dir, start_date, end_date):
    """加载指定时间段的施工日志"""
    logs = []
    current = start_date
    
    while current <= end_date:
        log_path = f"{logs_dir}/daily_{current.strftime('%Y%m%d')}.md"
        try:
            with open(log_path, "r", encoding="utf-8") as f:
                content = f.read()
                logs.append({
                    "date": current.strftime("%Y-%m-%d"),
                    "content": content
                })
        except FileNotFoundError:
            pass
        current += timedelta(days=1)
    
    return logs


def load_schedule(schedule_path):
    """加载进度计划"""
    with open(schedule_path, "r", encoding="utf-8") as f:
        return json.load(f)


def calculate_week_progress(schedule, start_date, end_date):
    """计算周期内的进度情况"""
    progress_summary = {
        "planned_tasks": [],
        "completed_tasks": [],
        "in_progress_tasks": []
    }
    
    for task in schedule["tasks"]:
        task_start = datetime.strptime(task["start_date"], "%Y-%m-%d")
        task_end = datetime.strptime(task["end_date"], "%Y-%m-%d")
        
        # 判断工序是否在该周期内
        if task_start <= end_date and task_end >= start_date:
            if task["status"] == "completed" or task["progress"] == 100:
                progress_summary["completed_tasks"].append(task)
            elif task["progress"] > 0:
                progress_summary["in_progress_tasks"].append(task)
            else:
                progress_summary["planned_tasks"].append(task)
    
    return progress_summary


def generate_weekly_report(project_name, year, week, progress_summary, daily_logs=None):
    """生成周报内容"""
    week_start, week_end = get_week_range(year, week)
    
    report = []
    report.append(f"# {project_name} - 施工周报")
    report.append(f"\n**第 {week} 周** ({year}年)")
    report.append(f"\n**周期**: {week_start.strftime('%Y-%m-%d')} 至 {week_end.strftime('%Y-%m-%d')}")
    report.append(f"**编制日期**: {datetime.now().strftime('%Y-%m-%d')}")
    
    # 一、本周进度概况
    report.append(f"\n---")
    report.append(f"\n## 一、本周进度概况")
    
    total_tasks = (len(progress_summary["planned_tasks"]) + 
                  len(progress_summary["completed_tasks"]) + 
                  len(progress_summary["in_progress_tasks"]))
    
    report.append(f"\n| 项目 | 数量 | 占比 |")
    report.append(f"|------|------|------|")
    report.append(f"| 计划工序 | {len(progress_summary['planned_tasks'])} | "
                 f"{len(progress_summary['planned_tasks'])/max(total_tasks,1)*100:.1f}% |")
    report.append(f"| 进行中 | {len(progress_summary['in_progress_tasks'])} | "
                 f"{len(progress_summary['in_progress_tasks'])/max(total_tasks,1)*100:.1f}% |")
    report.append(f"| 已完成 | {len(progress_summary['completed_tasks'])} | "
                 f"{len(progress_summary['completed_tasks'])/max(total_tasks,1)*100:.1f}% |")
    
    # 本周完成工序
    if progress_summary["completed_tasks"]:
        report.append(f"\n### 本周完成工序")
        for task in progress_summary["completed_tasks"]:
            report.append(f"- ✅ {task['name']} (计划：{task['start_date']} ~ {task['end_date']})")
    
    # 进行中工序
    if progress_summary["in_progress_tasks"]:
        report.append(f"\n### 进行中工序")
        for task in progress_summary["in_progress_tasks"]:
            report.append(f"- 🔄 {task['name']} - 进度 {task['progress']}%")
    
    # 二、生产情况
    report.append(f"\n---")
    report.append(f"\n## 二、生产情况")
    
    if daily_logs:
        # 汇总日志中的人员、机械信息
        total_workers = 0
        weather_days = {}
        
        for log in daily_logs:
            content = log["content"]
            # 简单解析（实际应更完善）
            if "作业人员" in content:
                # 尝试提取人数
                pass
        
        report.append(f"\n**有效施工天数**: {len(daily_logs)} 天")
        report.append(f"\n**施工日志记录**: {len(daily_logs)} 份")
    else:
        report.append(f"\n【待填写本周生产情况汇总】")
    
    # 三、质量情况
    report.append(f"\n---")
    report.append(f"\n## 三、质量情况")
    report.append(f"\n### 质量检查")
    report.append(f"- [ ] 检验批验收：__ 次")
    report.append(f"- [ ] 隐蔽验收：__ 次")
    report.append(f"- [ ] 材料复检：__ 次")
    
    report.append(f"\n### 质量问题")
    report.append(f"本周无重大质量问题。")
    
    # 四、安全情况
    report.append(f"\n---")
    report.append(f"\n## 四、安全情况")
    report.append(f"\n### 安全检查")
    report.append(f"- [ ] 日常检查：__ 次")
    report.append(f"- [ ] 专项检查：__ 次")
    report.append(f"- [ ] 安全教育：__ 次")
    
    report.append(f"\n### 安全隐患")
    report.append(f"本周无重大安全隐患。")
    
    # 五、材料情况
    report.append(f"\n---")
    report.append(f"\n## 五、材料情况")
    report.append(f"\n| 材料名称 | 单位 | 进场数量 | 使用数量 | 库存 |")
    report.append(f"|---------|------|---------|---------|------|")
    report.append(f"| 【待填写】 | - | - | - | - |")
    
    # 六、下周计划
    report.append(f"\n---")
    report.append(f"\n## 六、下周计划")
    report.append(f"\n### 主要工序安排")
    report.append(f"1. 【待填写下周主要工作】")
    report.append(f"2. 【待填写】")
    report.append(f"3. 【待填写】")
    
    report.append(f"\n### 需协调事项")
    report.append(f"- 【待填写需要协调的问题】")
    
    # 七、问题与建议
    report.append(f"\n---")
    report.append(f"\n## 七、问题与建议")
    report.append(f"\n### 存在问题")
    report.append(f"1. 【待填写】")
    
    report.append(f"\n### 解决建议")
    report.append(f"1. 【待填写】")
    
    # 签署
    report.append(f"\n---")
    report.append(f"\n**编制人**: __________")
    report.append(f"\n**审核人**: __________")
    report.append(f"\n**日期**: {datetime.now().strftime('%Y-%m-%d')}")
    
    return "\n".join(report)


def main():
    parser = argparse.ArgumentParser(description="生成施工周报")
    parser.add_argument("--project", required=True, help="项目名称")
    parser.add_argument("--year", type=int, default=datetime.now().year, help="年份")
    parser.add_argument("--week", type=int, required=True, help="周数 (1-52)")
    parser.add_argument("--schedule", help="进度计划文件路径")
    parser.add_argument("--logs-dir", help="施工日志目录")
    parser.add_argument("--output", help="报告输出路径")
    
    args = parser.parse_args()
    
    # 获取周范围
    week_start, week_end = get_week_range(args.year, args.week)
    
    print(f"📊 生成周报：{args.project}")
    print(f"📅 第 {args.week} 周 ({args.year}年)")
    print(f"📆 周期：{week_start.strftime('%Y-%m-%d')} 至 {week_end.strftime('%Y-%m-%d')}")
    
    # 加载进度计划
    progress_summary = {"planned_tasks": [], "completed_tasks": [], "in_progress_tasks": []}
    if args.schedule:
        schedule = load_schedule(args.schedule)
        progress_summary = calculate_week_progress(schedule, week_start, week_end)
    
    # 加载日志
    daily_logs = []
    if args.logs_dir:
        daily_logs = load_daily_logs(args.logs_dir, week_start, week_end)
    
    # 生成报告
    report = generate_weekly_report(
        args.project, 
        args.year, 
        args.week, 
        progress_summary,
        daily_logs
    )
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"✓ 周报已生成：{args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()
