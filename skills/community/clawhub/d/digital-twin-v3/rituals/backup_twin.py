#!/usr/bin/env python3
"""
数字双生 - 备份功能
一键备份双生系统所有数据
"""

import os
import json
import shutil
from pathlib import Path
from datetime import datetime
import tarfile
import hashlib

WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", "/root/.openclaw/workspace"))
TWIN_DIR = WORKSPACE / ".twin"
BACKUP_DIR = WORKSPACE / ".twin_backups"

def create_backup() -> dict:
    """创建备份"""
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"twin_backup_{timestamp}.tar.gz"
    backup_path = BACKUP_DIR / backup_name
    
    # 创建tar.gz备份
    with tarfile.open(backup_path, "w:gz") as tar:
        tar.add(TWIN_DIR, arcname="twin")
    
    # 计算哈希
    with open(backup_path, "rb") as f:
        file_hash = hashlib.md5(f.read()).hexdigest()
    
    # 记录备份信息
    info = {
        "backup_file": backup_name,
        "created": datetime.now().isoformat(),
        "size_mb": round(backup_path.stat().st_size / 1024 / 1024, 2),
        "hash": file_hash,
        "includes": [
            "twin-covenant.md (双生契约)",
            "values-anchor.md (价值观锚点)",
            "memory/ (所有记忆)",
            "guardian-log.json (守护日志)"
        ]
    }
    
    info_file = BACKUP_DIR / f"info_{timestamp}.json"
    with open(info_file, "w") as f:
        json.dump(info, f, ensure_ascii=False, indent=2)
    
    return info

if __name__ == "__main__":
    print("💾 正在创建双生备份...")
    info = create_backup()
    
    print(f"\n✅ 备份完成!")
    print(f"   文件: {info['backup_file']}")
    print(f"   大小: {info['size_mb']} MB")
    print(f"   哈希: {info['hash'][:16]}...")
    print(f"\n📦 包含:")
    for item in info['includes']:
        print(f"   • {item}")