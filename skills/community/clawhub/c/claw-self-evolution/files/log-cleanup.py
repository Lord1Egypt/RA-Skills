#!/usr/bin/env python3
"""
日志自动清理
保留最近30天日志，自动删除过期日志，节省存储空间
"""

import os
import datetime
from typing import List

LOG_DIR = "/app/working/logs/"
RETENTION_DAYS = 30

def clean_old_logs() -> int:
    """清理30天前的日志"""
    deleted = 0
    today = datetime.datetime.now()
    
    if not os.path.exists(LOG_DIR):
        return 0
    
    for root, dirs, files in os.walk(LOG_DIR):
        for filename in files:
            filepath = os.path.join(root, filename)
            try:
                stat = os.stat(filepath)
                mtime = datetime.datetime.fromtimestamp(stat.st_mtime)
                days_old = (today - mtime).days
                if days_old > RETENTION_DAYS:
                    os.remove(filepath)
                    deleted += 1
                    print(f"🗑️  删除过期日志: {filepath} ({days_old} 天)")
            except Exception as e:
                print(f"⚠️  删除失败 {filepath}: {e}")
    
    # 清理空目录
    for root, dirs, files in os.walk(LOG_DIR, topdown=False):
        for d in dirs:
            dirpath = os.path.join(root, d)
            if not os.listdir(dirpath):
                try:
                    os.rmdir(dirpath)
                except:
                    pass
    
    return deleted

def main():
    print("🚀 开始日志自动清理...")
    print(f"📅 保留最近 {RETENTION_DAYS} 天日志")
    
    deleted = clean_old_logs()
    
    print(f"\n📊 清理完成: 删除 {deleted} 个过期日志")
    print("✅ 清理完成")

if __name__ == "__main__":
    main()
