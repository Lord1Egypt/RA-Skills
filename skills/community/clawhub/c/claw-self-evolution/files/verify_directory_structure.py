#!/usr/bin/env python3
"""
Verify and enforce OpenClaw directory structure standard
Compliant with: memory/DIRECTORY_STRUCTURE.md
"""

import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Tuple, Dict

# 标准目录结构定义
WORKING_ROOT = Path("/app/working")
REQUIRED_DIRS = [
    "logs",
    "temp",
    "scripts",
    "output", 
    "archive",
    "embedding_cache",
    "file_store",
    "memory/episodic",
    "memory/episodic/daily",
    "memory/episodic/archive",
    "memory/semantic",
    "memory/procedural",
    "memory/snapshots",
    "sessions",
    "tool_result",
]

# memory根目录允许保留的文件（白名单）
MEMORY_ROOT_ALLOWED_FILES = {
    "DIRECTORY_STRUCTURE.md",
    "SECURITY_RULES.md", 
    "integrations.md",
    "skills.md",
    "tasks.md",
    "user_profile.md",
}

# 根目录允许保留的核心配置文件（严格7个）
ROOT_ALLOWED_FILES = {
    "MEMORY.md",
    "config.json",
    "chats.json",
    "jobs.json",
    "copaw_file_metadata.json",
    "feishu_receive_ids.json",
    "token_usage.json",
}

def ensure_required_dirs() -> List[str]:
    """确保所有必需目录存在，创建缺失的"""
    created = []
    for dir_path in REQUIRED_DIRS:
        full_path = WORKING_ROOT / dir_path
        if not full_path.exists():
            full_path.mkdir(parents=True, exist_ok=True)
            created.append(dir_path)
    return created

def find_misplaced_files() -> Tuple[List[Path], List[Tuple[Path, str]]]:
    """查找错位的文件，返回需要移动的列表"""
    misplaced_daily_logs = []  # YYYY-MM-DD.md 在memory根
    misplaced_runtime = []    # 运行时日志在memory根
    
    # 检查memory根目录
    memory_root = WORKING_ROOT / "memory"
    for entry in os.scandir(memory_root):
        if entry.is_file():
            filename = entry.name
            
            if filename in MEMORY_ROOT_ALLOWED_FILES:
                continue
                
            # 日期格式的对话日志
            if filename.endswith('.md') and len(filename) == 11:
                try:
                    # 验证是否为有效日期格式
                    year = int(filename[:4])
                    month = int(filename[5:7])
                    day = int(filename[8:10])
                    misplaced_daily_logs.append(Path(entry.path))
                except ValueError:
                    continue
                    
            # 运行时日志文件
            if filename in ['wal.log', 'working_buffer.json'] or filename.endswith('.log'):
                misplaced_runtime.append((Path(entry.path), "logs/"))
    
    return misplaced_daily_logs, misplaced_runtime

def move_misplaced_files(
    misplaced_daily_logs: List[Path],
    misplaced_runtime: List[Tuple[Path, str]]
) -> int:
    """移动错位文件到正确位置"""
    moved = 0
    
    # 移动日期日志到 episodic/daily
    for src_path in misplaced_daily_logs:
        filename = src_path.name
        dst_path = WORKING_ROOT / "memory" / "episodic" / "daily" / filename
        
        if dst_path.exists():
            # 合并内容
            with open(src_path, 'r', encoding='utf-8') as f:
                new_content = f.read()
            with open(dst_path, 'a', encoding='utf-8') as f:
                f.write("\n\n--- Merged from memory root ---\n\n" + new_content)
            os.remove(src_path)
        else:
            shutil.move(str(src_path), str(dst_path))
        
        moved += 1
        print(f"  ✓ Moved daily log: {filename} → memory/episodic/daily/")
    
    # 移动运行时日志到 logs
    for src_path, target_dir in misplaced_runtime:
        filename = src_path.name
        dst_path = WORKING_ROOT / target_dir / filename
        
        if dst_path.exists():
            os.remove(src_path)
        else:
            shutil.move(str(src_path), str(dst_path))
            
        moved += 1
        print(f"  ✓ Moved runtime file: {filename} → {target_dir}")
    
    return moved

def check_root_directory() -> List[Path]:
    """检查根目录是否有不允许的文件"""
    extra_files = []
    for entry in os.scandir(WORKING_ROOT):
        if entry.is_file():
            if entry.name not in ROOT_ALLOWED_FILES:
                # 忽略特定扩展名的文件
                if entry.name.endswith('.log') or entry.name == '.gitkeep':
                    continue
                extra_files.append(Path(entry.path))
    return extra_files

def archive_old_daily_logs() -> Tuple[int, int]:
    """
    归档超过30天的日志到 episodic/archive
    保持daily目录只存最近30天
    """
    daily_dir = WORKING_ROOT / "memory" / "episodic" / "daily"
    archive_dir = WORKING_ROOT / "memory" / "episodic" / "archive"
    archive_dir.mkdir(parents=True, exist_ok=True)
    
    archived = 0
    total = 0
    
    if not daily_dir.exists():
        return 0, 0
    
    today = datetime.now()
    for entry in os.scandir(daily_dir):
        if entry.is_file() and entry.name.endswith('.md') and len(entry.name) == 11:
            total += 1
            try:
                # 解析日期
                file_date = datetime.strptime(entry.name[:10], "%Y-%m-%d")
                days_old = (today - file_date).days
                
                if days_old > 30:
                    src_path = Path(entry.path)
                    dst_path = archive_dir / entry.name
                    if not dst_path.exists():
                        shutil.move(str(src_path), str(dst_path))
                    else:
                        # 合并
                        with open(src_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        with open(dst_path, 'a', encoding='utf-8') as f:
                            f.write("\n\n--- Merged from daily ---\n\n" + content)
                        os.remove(src_path)
                    archived += 1
            except ValueError:
                continue
    
    return archived, total

def main():
    """主检查流程"""
    print(f"=" * 60)
    print(f"🔍 OpenClaw Directory Structure Verification")
    print(f"📅 {datetime.now()}")
    print(f"=" * 60)
    
    # 1. 确保目录存在
    print("\n📁 Step 1: Checking required directories...")
    created = ensure_required_dirs()
    if created:
        print(f"  ✅ Created missing directories: {created}")
    else:
        print(f"  ✅ All required directories exist")
    
    # 2. 查找并移动错位文件
    print("\n🗺️  Step 2: Finding misplaced files...")
    misplaced_daily, misplaced_runtime = find_misplaced_files()
    
    if misplaced_daily or misplaced_runtime:
        print(f"  🔍 Found {len(misplaced_daily) + len(misplaced_runtime)} misplaced files")
        moved = move_misplaced_files(misplaced_daily, misplaced_runtime)
        print(f"  ✅ Moved {moved} files to correct locations")
    else:
        print("  ✅ No misplaced files found")
    
    # 3. 归档旧日志
    print("\n🗄️  Step 3: Archiving old daily logs (>30 days)...")
    archived, total = archive_old_daily_logs()
    if archived > 0:
        print(f"  ✅ Archived {archived} old logs from {total} total")
    else:
        print(f"  ✅ No old logs need archiving (total: {total})")
    
    # 4. 检查根目录
    print("\n🔎 Step 4: Checking root directory for extra files...")
    extra_root_files = check_root_directory()
    if extra_root_files:
        print(f"  ⚠️  Extra files in root directory:")
        for f in extra_root_files:
            print(f"      {f.name}")
        print("  💡 Tip: Root should only have 7 core config files per spec")
    else:
        print("  ✅ Root directory clean (only 7 core config files)")
    
    # 总结
    print("\n" + "=" * 60)
    print(f"✅ Verification complete!")
    total_moved = len(misplaced_daily) + len(misplaced_runtime)
    if total_moved > 0 or archived > 0:
        print(f"   - Moved {total_moved} misplaced files")
        print(f"   - Archived {archived} old daily logs")
    else:
        print(f"   - Directory structure conforms to standard")
    print("=" * 60)

if __name__ == "__main__":
    main()
