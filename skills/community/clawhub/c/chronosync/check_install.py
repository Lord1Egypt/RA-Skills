#!/usr/bin/env python3
"""安装检查脚本 - 帮用户排查问题"""

import os
import sys
from pathlib import Path

def check():
    """检查安装环境"""
    print("=" * 50)
    print("Session Sync 安装检查")
    print("=" * 50)
    
    # 检查 Python 版本
    py_version = sys.version_info
    print(f"\n✓ Python 版本: {py_version.major}.{py_version.minor}.{py_version.micro}")
    if py_version < (3, 8):
        print("  ✗ 需要 Python 3.8+")
        return False
    
    # 检查 OpenClaw 目录
    openclaw_dir = Path.home() / ".openclaw"
    if "OPENCLAW_STATE_DIR" in os.environ:
        openclaw_dir = Path(os.environ["OPENCLAW_STATE_DIR"])
        print(f"\n✓ OPENCLAW_STATE_DIR 环境变量: {openclaw_dir}")
    else:
        print(f"\n✓ OpenClaw 默认目录: {openclaw_dir}")
    
    if openclaw_dir.exists():
        print("  ✓ 目录存在")
    else:
        print("  ✗ 目录不存在，请先安装 OpenClaw")
        return False
    
    # 检查 sessions 目录
    sessions_dirs = [
        openclaw_dir / "sessions",
        openclaw_dir / "workspace" / "sessions",
    ]
    sessions_found = False
    for sdir in sessions_dirs:
        if sdir.exists():
            print(f"\n✓ Sessions 目录: {sdir}")
            sessions_found = True
            break
    
    if not sessions_found:
        print("\n✗ 未找到 sessions 目录")
        print("  可能的原因：")
        print("  - OpenClaw 未运行过")
        print("  - 使用了非标准配置")
        print(f"  - 请检查: {sessions_dirs}")
    
    # 检查写入权限
    output_dir = openclaw_dir / "workspace" / "memory" / "sync"
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        test_file = output_dir / ".write_test"
        test_file.write_text("test")
        test_file.unlink()
        print(f"\n✓ 写入权限检查通过: {output_dir}")
    except Exception as e:
        print(f"\n✗ 写入权限检查失败: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("检查完成，可以正常使用！")
    print("=" * 50)
    return True

if __name__ == "__main__":
    success = check()
    sys.exit(0 if success else 1)
