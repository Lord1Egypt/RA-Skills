#!/usr/bin/env python3
"""
核心配置自动备份
每天自动备份所有核心配置文件到 memory/snapshots/
保持最近30天备份，自动清理过期
"""

import os
import shutil
import datetime
from typing import List

# 配置
BACKUP_DIR = "/app/working/memory/snapshots/core-backup/"
RETENTION_DAYS = 30
CORE_FILES = [
    # 根目录核心配置
    "/app/working/MEMORY.md",
    "/app/working/config.json",
    "/app/working/chats.json",
    "/app/working/jobs.json",
    "/app/working/copaw_file_metadata.json",
    "/app/working/feishu_receive_ids.json",
    "/app/working/token_usage.json",
    
    # memory 核心配置
    "/app/working/memory/DIRECTORY_STRUCTURE.md",
    "/app/working/memory/SECURITY_RULES.md",
    "/app/working/memory/INDEX.md",
    "/app/working/memory/skills.md",
    "/app/working/memory/tasks.md",
    "/app/working/memory/user_profile.md",
    "/app/working/memory/integrations.md",
    
    # skills 索引
    "/app/working/skills/INDEX.md",
]

def create_backup():
    """创建今日备份"""
    today = datetime.datetime.now().strftime("%Y%m%d")
    backup_path = os.path.join(BACKUP_DIR, today)
    
    os.makedirs(backup_path, exist_ok=True)
    
    success = 0
    failed = 0
    
    for src_path in CORE_FILES:
        if os.path.exists(src_path):
            filename = os.path.basename(src_path)
            rel_dir = os.path.dirname(src_path).replace("/app/working/", "")
            dest_dir = os.path.join(backup_path, rel_dir)
            os.makedirs(dest_dir, exist_ok=True)
            dest_path = os.path.join(backup_path, rel_dir, filename)
            if src_path != dest_path:
                shutil.copy2(src_path, dest_path)
            success += 1
        else:
            failed += 1
            print(f"⚠️  文件不存在，跳过: {src_path}")
    
    print(f"✅ 备份完成: {success} 成功, {failed} 失败")
    return backup_path, success, failed

def cleanup_old_backups():
    """清理过期备份（超过30天）"""
    if not os.path.exists(BACKUP_DIR):
        return 0
    
    today = datetime.datetime.now()
    deleted = 0
    
    for dirname in os.listdir(BACKUP_DIR):
        try:
            backup_date = datetime.datetime.strptime(dirname, "%Y%m%d")
            days_old = (today - backup_date).days
            if days_old > RETENTION_DAYS:
                shutil.rmtree(os.path.join(BACKUP_DIR, dirname))
                deleted += 1
                print(f"🗑️  删除过期备份: {dirname} ({days_old} 天)")
        except ValueError:
            # 不是日期格式的目录，跳过
            continue
    
    print(f"🗑️  清理完成，删除 {deleted} 个过期备份")
    return deleted

def main():
    print("🚀 开始核心配置自动备份...")
    
    os.makedirs(BACKUP_DIR, exist_ok=True)
    
    backup_path, success, failed = create_backup()
    deleted = cleanup_old_backups()
    
    print("\n📊 备份汇总:")
    print(f"  今日备份位置: {backup_path}")
    print(f"  成功: {success} 文件")
    print(f"  跳过: {failed} 文件（不存在）")
    print(f"  删除过期: {deleted} 备份")
    print("✅ 备份完成")

if __name__ == "__main__":
    main()
