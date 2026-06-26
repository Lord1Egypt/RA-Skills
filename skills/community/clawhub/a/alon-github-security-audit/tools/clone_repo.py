#!/usr/bin/env python3
"""
GitHub 仓库浅克隆工具
安全地克隆仓库到临时目录，只下载最新代码
"""

import sys
import os
import subprocess
import tempfile
import uuid
from pathlib import Path


def clone_repo(repo_url):
    """
    浅克隆 GitHub 仓库

    Args:
        repo_url: GitHub 仓库 URL

    Returns:
        str: 克隆后的本地目录路径
    """
    # 验证 URL
    if not repo_url.startswith(('https://github.com/', 'git@github.com:')):
        print(f"❌ 错误: 不是有效的 GitHub URL: {repo_url}", file=sys.stderr)
        sys.exit(1)

    # 提取仓库名
    if repo_url.endswith('.git'):
        repo_url = repo_url[:-4]
    repo_name = repo_url.rstrip('/').split('/')[-1]

    # 创建临时目录
    temp_base = tempfile.gettempdir()
    unique_id = str(uuid.uuid4())[:8]
    clone_dir = os.path.join(temp_base, f"github_audit_{repo_name}_{unique_id}")

    print(f"🔽 开始浅克隆仓库...")
    print(f"   源: {repo_url}")
    print(f"   目标: {clone_dir}")

    try:
        # 执行浅克隆
        result = subprocess.run(
            ['git', 'clone', '--depth', '1', repo_url, clone_dir],
            capture_output=True,
            text=True,
            timeout=300  # 5 分钟超时
        )

        if result.returncode != 0:
            print(f"❌ 克隆失败: {result.stderr}", file=sys.stderr)
            sys.exit(1)

        print(f"✅ 克隆成功!")
        print(f"📁 本地路径: {clone_dir}")

        # 输出目录信息
        total_files = sum(1 for _ in Path(clone_dir).rglob('*') if _.is_file())
        dir_size = sum(f.stat().st_size for f in Path(clone_dir).rglob('*') if f.is_file())
        print(f"📊 文件数: {total_files}")
        print(f"📊 总大小: {dir_size / 1024 / 1024:.2f} MB")

        # 返回路径供后续使用
        print(f"\n---OUTPUT---")
        print(clone_dir)

        return clone_dir

    except subprocess.TimeoutExpired:
        print(f"❌ 克隆超时（5分钟）", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ 未知错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("用法: python clone_repo.py <GitHub仓库URL>")
        sys.exit(1)

    clone_repo(sys.argv[1])
