#!/usr/bin/env python3
"""
超简单文件监控器
就一个脚本，检测新文件直接通知
"""

import os
import time
import json
from pathlib import Path
from datetime import datetime

# 加载配置
SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent  # skills/file-monitor
CONFIG_FILE = SKILL_DIR / 'config.json'
config = json.load(open(CONFIG_FILE, 'r', encoding='utf-8'))

WATCH_DIR = Path(config['watch_dir'])
NOTIFY_FILE = SKILL_DIR / config.get('notify_file', '.data/.pending_notify.md')

print(f"[监控] 目录：{WATCH_DIR}")
print(f"[监控] 按 Ctrl+C 停止\n")

# 记录已知文件
known_files = set()
if WATCH_DIR.exists():
    for f in WATCH_DIR.iterdir():
        if f.is_file() and not f.name.startswith('.'):
            known_files.add(f.name)

print(f"[监控] 已知文件：{len(known_files)} 个\n")

while True:
    time.sleep(3)
    
    if not WATCH_DIR.exists():
        continue
    
    # 扫描当前文件
    current_files = set()
    for f in WATCH_DIR.iterdir():
        if f.is_file() and not f.name.startswith('.') and not f.name.startswith('$'):
            current_files.add(f.name)
    
    # 检查新文件
    new_files = current_files - known_files
    for filename in new_files:
        filepath = WATCH_DIR / filename
        size = filepath.stat().st_size
        mtime = datetime.fromtimestamp(filepath.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')
        size_str = f"{size/1024:.1f} KB"
        
        print(f"[新文件] {filename} ({size_str})")
        
        # 写入通知
        msg = f"""# 待发送通知

**文件**: {filename}
**大小**: {size_str}
**时间**: {mtime}

---

[FILE] 文件监控提醒

文件名：{filename}
大小：{size_str}
时间：{mtime}

路径：{WATCH_DIR}\\{filename}

---

需要我处理这个文件吗？"""
        
        try:
            NOTIFY_FILE.write_text(msg, encoding='utf-8')
            print(f"  [OK] 已写入通知")
        except Exception as e:
            print(f"  [ERR] 写入失败：{e}")
        
        known_files.add(filename)
    
    # 清理删除的文件
    deleted = known_files - current_files
    for f in deleted:
        known_files.discard(f)
