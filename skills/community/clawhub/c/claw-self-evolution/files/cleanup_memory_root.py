#!/usr/bin/env python3
"""
清理 memory 根目录，将错位文件移动到正确位置
符合 DIRECTORY_STRUCTURE.md 规范
"""

import os
import shutil
from datetime import datetime

# 定义路径
MEMORY_ROOT = "/app/working/memory"
LOGS_DIR = "/app/working/logs"
EPISODIC_DAILY_DIR = "/app/working/memory/episodic/daily"

# 允许在 memory 根目录保留的文件（白名单）
ALLOWED_FILES = {
    "DIRECTORY_STRUCTURE.md",
    "SECURITY_RULES.md", 
    "integrations.md",
    "skills.md",
    "tasks.md",
    "user_profile.md"
}

# 需要创建的目录结构
REQUIRED_DIRS = [
    EPISODIC_DAILY_DIR,
    LOGS_DIR,
]

def ensure_dirs():
    """确保必需目录存在"""
    for d in REQUIRED_DIRS:
        os.makedirs(d, exist_ok=True)

def move_daily_logs(filename):
    """移动日期格式的对话日志到 episodic/daily"""
    src = os.path.join(MEMORY_ROOT, filename)
    dst = os.path.join(EPISODIC_DAILY_DIR, filename)
    if os.path.exists(dst):
        # 如果目标已存在，合并内容
        with open(src, 'r', encoding='utf-8') as f:
            new_content = f.read()
        with open(dst, 'a', encoding='utf-8') as f:
            f.write("\n\n--- Merged from root ---\n\n" + new_content)
        os.remove(src)
        print(f"✓ 已合并: {filename} -> episodic/daily/")
    else:
        shutil.move(src, dst)
        print(f"✓ 已移动: {filename} -> episodic/daily/")

def move_runtime_files(filename):
    """移动运行时日志到 logs 目录"""
    src = os.path.join(MEMORY_ROOT, filename)
    dst = os.path.join(LOGS_DIR, filename)
    if os.path.exists(dst):
        os.remove(src)
    else:
        shutil.move(src, dst)
    print(f"✓ 已移动: {filename} -> logs/")

def main():
    print(f"=== 开始清理 memory 根目录 [{datetime.now()}] ===")
    ensure_dirs()
    
    # 遍历 memory 根目录所有文件
    for entry in os.scandir(MEMORY_ROOT):
        if entry.is_file():
            filename = entry.name
            
            # 跳过允许的文件
            if filename in ALLOWED_FILES:
                continue
                
            # 处理日期格式的对话日志 (YYYY-MM-DD.md)
            if filename.endswith('.md') and len(filename) == 11:
                move_daily_logs(filename)
                continue
                
            # 处理运行时日志文件
            if filename in ['wal.log', 'working_buffer.json'] or filename.endswith('.log'):
                move_runtime_files(filename)
                continue
                
            # 其他未知文件，暂不处理，提示
            print(f"⚠  未识别文件留在原地: {filename}")
    
    print(f"=== 清理完成 [{datetime.now()}] ===")

if __name__ == "__main__":
    main()
