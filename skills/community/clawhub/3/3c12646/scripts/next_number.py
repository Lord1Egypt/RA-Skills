#!/usr/bin/env python3
"""
获取下一个任务编号
用法: python3 next_number.py
输出: T-YYYYMMDD-NNN
"""
import os
from datetime import datetime

MISSION_CONTROL_DIR = "/home/huang/.hermes/mission_control"

def get_next_number():
    today = datetime.now().strftime("%Y-%m-%d")
    today_folder = os.path.join(MISSION_CONTROL_DIR, today)
    
    # 如果日期文件夹不存在，创建并返回001
    if not os.path.exists(today_folder):
        os.makedirs(today_folder, exist_ok=True)
        return f"T-{datetime.now().strftime('%Y%m%d')}-001"
    
    # 统计已有任务目录数量
    existing = [f for f in os.listdir(today_folder) if f.startswith("T-") and os.path.isdir(os.path.join(today_folder, f))]
    next_num = len(existing) + 1
    return f"T-{datetime.now().strftime('%Y%m%d')}-{next_num:03d}"

if __name__ == "__main__":
    print(get_next_number())
