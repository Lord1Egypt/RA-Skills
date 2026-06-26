#!/usr/bin/env python3
"""检查磁盘空间使用"""

import shutil
import sys
from pathlib import Path

def check_disk_space(path: str = None, warning_percent: float = 80.0):
    """检查磁盘空间使用率"""
    if path is None:
        path = str(Path(__file__).parent.parent)
    
    total, used, free = shutil.disk_usage(path)
    
    used_percent = (used / total) * 100
    free_gb = free / (1024 ** 3)
    
    print(f"💾 磁盘空间检查")
    print("=" * 50)
    print(f"路径：       {path}")
    print(f"总容量：     {total / (1024 ** 3):.2f} GB")
    print(f"已使用：     {used / (1024 ** 3):.2f} GB ({used_percent:.1f}%)")
    print(f"可用：       {free_gb:.2f} GB")
    print("=" * 50)
    
    if used_percent >= warning_percent:
        print(f"\n⚠️  警告：磁盘使用率超过 {warning_percent}%!")
        print(f"\n💡 建议立即清理:")
        print(f"   python tools/cleanup_apple_data.py --execute")
        return 1
    elif used_percent >= warning_percent - 10:
        print(f"\n⚠️  注意：磁盘使用率接近 {warning_percent}%")
        print(f"   当前：{used_percent:.1f}% | 告警阈值：{warning_percent}%")
        return 0
    else:
        print(f"\n✅ 磁盘空间充足")
        return 0

if __name__ == "__main__":
    sys.exit(check_disk_space())
