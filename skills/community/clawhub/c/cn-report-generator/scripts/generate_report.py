#!/usr/bin/env python3
"""
企业日报/周报自动生成脚本

用法:
  python generate_report.py daily    # 生成日报
  python generate_report.py weekly   # 生成周报
  python generate_report.py monthly  # 生成月报
"""

import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
import re

# 配置
WORKSPACE = Path.home() / ".qclaw" / "workspace"
MEMORY_FILE = WORKSPACE / "MEMORY.md"
DAILY_LOG_DIR = WORKSPACE / "memory"
IN_PROGRESS_FILE = WORKSPACE / "memory" / "in_progress.md"
REPORT_DIR = Path.home() / "reports"


def read_file(path):
    """读取文件内容"""
    if not path.exists():
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def extract_tasks(text):
    """从文本中提取任务"""
    completed = re.findall(r"- \[x\] (.+)", text)
    in_progress = re.findall(r"- \[ \] (.+)", text)
    return completed, in_progress


def extract_sections(text):
    """提取各部分内容"""
    sections = {
        "completed": [],
        "in_progress": [],
        "problems": [],
        "plans": []
    }
    
    # 匹配完成事项
    sections["completed"] = re.findall(r"- \[x\] (.+)", text)
    
    # 匹配进行中
    sections["in_progress"] = re.findall(r"- \[ \] (.+)", text)
    
    # 匹配问题
    sections["problems"] = re.findall(r"问题[：:]\s*(.+)", text)
    sections["problems"].extend(re.findall(r"⚠️\s*(.+)", text))
    
    return sections


def generate_daily_report(date=None):
    """生成日报"""
    if date is None:
        date = datetime.now()
    
    date_str = date.strftime("%Y-%m-%d")
    
    # 读取今日daily log
    daily_log = read_file(DAILY_LOG_DIR / f"{date_str}.md")
    
    # 读取in_progress
    in_progress = read_file(IN_PROGRESS_FILE)
    
    # 读取MEMORY.md（获取长期任务）
    memory = read_file(MEMORY_FILE)
    
    # 提取内容
    sections = extract_sections(daily_log + "\n" + in_progress)
    
    # 生成报告
    report = f"""# {date.strftime("%Y年%m月%d日")} 工作日报

## ✅ 今日完成

"""
    if sections["completed"]:
        for item in sections["completed"]:
            report += f"- {item}\n"
    else:
        report += "- 无\n"
    
    report += """
## 🚧 进行中

"""
    if sections["in_progress"]:
        for item in sections["in_progress"]:
            report += f"- {item}\n"
    else:
        report += "- 无\n"
    
    report += """
## ⚠️ 问题与风险

"""
    if sections["problems"]:
        for item in sections["problems"]:
            report += f"- {item}\n"
    else:
        report += "- 无\n"
    
    report += """
## 📅 明日计划

待填写...

---
*生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M")}*
*千策·千万·千成 🦞*
"""
    
    return report, date_str


def generate_weekly_report(date=None):
    """生成周报"""
    if date is None:
        date = datetime.now()
    
    # 计算本周起止日期
    week_start = date - timedelta(days=date.weekday())
    week_end = week_start + timedelta(days=6)
    
    week_num = date.isocalendar()[1]
    
    # 读取本周7天的daily log
    all_logs = ""
    for i in range(7):
        day = week_start + timedelta(days=i)
        log = read_file(DAILY_LOG_DIR / f"{day.strftime('%Y-%m-%d')}.md")
        all_logs += log + "\n"
    
    # 提取内容
    sections = extract_sections(all_logs)
    
    # 生成报告
    report = f"""# {date.year}年第{week_num}周 工作周报

**时间范围**: {week_start.strftime("%Y-%m-%d")} ~ {week_end.strftime("%Y-%m-%d")}

## 本周成果

"""
    if sections["completed"]:
        for item in sections["completed"][:10]:  # 最多显示10项
            report += f"- {item}\n"
    else:
        report += "- 无\n"
    
    report += """
## 数据统计

"""
    report += f"- 完成事项：{len(sections['completed'])}项\n"
    report += f"- 进行中：{len(sections['in_progress'])}项\n"
    
    report += """
## 问题与解决方案

"""
    if sections["problems"]:
        for item in sections["problems"][:5]:
            report += f"- {item}\n"
    else:
        report += "- 无\n"
    
    report += """
## 下周计划

待填写...

---
*生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M")}*
*千策·千万·千成 🦞*
"""
    
    return report, f"{date.year}-W{week_num:02d}"


def save_report(report, report_type, filename):
    """保存报告"""
    # 创建目录
    output_dir = REPORT_DIR / report_type
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 保存文件
    output_path = output_dir / f"{filename}.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)
    
    return output_path


def main():
    if len(sys.argv) < 2:
        print("用法: python generate_report.py <daily|weekly|monthly>")
        sys.exit(1)
    
    report_type = sys.argv[1]
    
    if report_type == "daily":
        report, filename = generate_daily_report()
        output_path = save_report(report, "daily", filename)
        print(f"✅ 日报已生成: {output_path}")
    
    elif report_type == "weekly":
        report, filename = generate_weekly_report()
        output_path = save_report(report, "weekly", filename)
        print(f"✅ 周报已生成: {output_path}")
    
    elif report_type == "monthly":
        print("⚠️ 月报功能开发中...")
    
    else:
        print(f"未知报告类型: {report_type}")
        sys.exit(1)


if __name__ == "__main__":
    main()
