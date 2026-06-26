#!/usr/bin/env python3
"""
清理临时克隆目录
"""

import sys
import shutil
import os


def cleanup(directory):
    """
    安全删除临时目录

    Args:
        directory: 要删除的目录路径
    """
    if not os.path.exists(directory):
        print(f"⚠️  目录不存在，跳过清理: {directory}")
        return

    # 安全检查：只删除临时目录
    import tempfile
    temp_dir = tempfile.gettempdir()
    real_path = os.path.realpath(directory)  # 解析真实路径，防止 .. 路径遍历攻击
    if 'github_audit_' not in real_path or not real_path.startswith(temp_dir):
        print(f"❌ 拒绝删除非临时目录: {directory}", file=sys.stderr)
        print(f"   临时目录应在: {temp_dir}", file=sys.stderr)
        sys.exit(1)

    try:
        print(f"🗑️  清理临时目录: {directory}")
        shutil.rmtree(directory)
        print(f"✅ 清理完成")
    except Exception as e:
        print(f"❌ 清理失败: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("用法: python cleanup.py <临时目录路径>")
        sys.exit(1)

    cleanup(sys.argv[1])
