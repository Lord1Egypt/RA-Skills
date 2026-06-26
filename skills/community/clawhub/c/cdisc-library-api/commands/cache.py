#!/usr/bin/env python3
"""
/cdisc-library-api cache [clear|status] - 缓存管理
"""

import sys
import shutil
from pathlib import Path

from pathlib import Path`nsys.path.insert(0, str(Path(__file__).parent.parent))


def get_cache_dir():
    return Path(__file__).parent.parent / ".cache"


def get_cache_size():
    cache_dir = get_cache_dir()
    if not cache_dir.exists():
        return 0, 0
    
    total_size = 0
    file_count = 0
    for f in cache_dir.glob("*.json"):
        total_size += f.stat().st_size
        file_count += 1
    
    return file_count, total_size


def format_size(size_bytes):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def main():
    action = sys.argv[1].lower() if len(sys.argv) > 1 else "status"
    
    if action == "clear":
        cache_dir = get_cache_dir()
        if not cache_dir.exists():
            print("ℹ️  缓存目录不存在")
            return
        
        file_count, total_size = get_cache_size()
        shutil.rmtree(cache_dir)
        cache_dir.mkdir()
        
        print(f"✓ 已清除缓存：{file_count} 个文件，{format_size(total_size)}")
    
    elif action == "status":
        cache_dir = get_cache_dir()
        
        if not cache_dir.exists():
            print("📦 缓存状态\n")
            print("  缓存目录：未创建")
            print("  首次查询后自动创建")
            return
        
        file_count, total_size = get_cache_size()
        
        print("📦 缓存状态\n")
        print(f"  目录：{cache_dir}")
        print(f"  文件数：{file_count}")
        print(f"  总大小：{format_size(total_size)}")
        print(f"  缓存有效期：1 小时")
        
        if file_count > 0:
            print(f"\n💡 使用 /cdisc-library-api cache clear 清除缓存")
    
    else:
        print("用法：/cdisc-library-api cache [clear|status]")
        print("\n命令:")
        print("  status  - 查看缓存状态（默认）")
        print("  clear   - 清除所有缓存")


if __name__ == "__main__":
    main()

