#!/usr/bin/env python3
"""
生成任务报告
用法: python3 generate_report.py "任务ID" "执行结果"
"""
import os
import sys
from datetime import datetime

MISSION_CONTROL_DIR = "/home/huang/.hermes/mission_control"
TEMPLATE_FILE = os.path.join(MISSION_CONTROL_DIR, "MISSION_REPORT_TEMPLATE.md")

def generate_report(task_id, result):
    today = datetime.now().strftime("%Y-%m-%d")
    today_folder = os.path.join(MISSION_CONTROL_DIR, today)
    
    # 确保日期文件夹存在
    os.makedirs(today_folder, exist_ok=True)
    
    # 生成报告文件名
    report_file = os.path.join(today_folder, f"REPORT-{task_id}.md")
    
    # 构建报告内容
    report_content = f"""# 任务报告：{task_id}

## 执行信息
- **任务ID**: {task_id}
- **完成时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- **状态**: ✅已完成

## 执行结果
{result}

## 存档位置
- 方案文件: {today_folder}/PLAN-{task_id}.md
- 报告文件: {report_file}
"""
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f"报告已生成: {report_file}")
    return report_file

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python3 generate_report.py <任务ID> <执行结果>")
        sys.exit(1)
    
    task_id = sys.argv[1]
    result = sys.argv[2]
    
    generate_report(task_id, result)
