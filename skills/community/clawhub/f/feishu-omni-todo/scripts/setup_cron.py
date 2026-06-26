#!/usr/bin/env python3
"""
设置定时任务
"""
import sys
from crontab import CronTab
import os

SCRIPT_PATH = os.path.abspath(__file__)
REMINDER_SCRIPT = os.path.join(os.path.dirname(SCRIPT_PATH), "reminder_check.py")
PYTHON_PATH = sys.executable

def setup_cron():
    """设置定时任务"""
    cron = CronTab(user=True)
    
    # 检查是否已经存在该任务
    job_exists = False
    for job in cron:
        if REMINDER_SCRIPT in str(job.command):
            job_exists = True
            break
    
    if not job_exists:
        # 创建新任务：每分钟运行一次
        job = cron.new(command=f"{PYTHON_PATH} {REMINDER_SCRIPT} >> /tmp/todo_reminder.log 2>&1", comment="飞书Todo提醒")
        job.minute.every(1)
        cron.write()
        print("✅ 定时提醒任务已设置，每分钟检查一次待办提醒")
    else:
        print("ℹ️ 定时提醒任务已存在")
    
    # 列出所有任务
    print("\n当前定时任务：")
    for job in cron:
        print(job)

if __name__ == "__main__":
    import sys
    setup_cron()
