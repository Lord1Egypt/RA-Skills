#!/usr/bin/env python3
"""
Backup OpenClaw personalized configuration and user data to GitHub
"""

import os
import sys
import json
import yaml
import base64
from datetime import datetime
from pathlib import Path

try:
    from github import Github
    from dotenv import load_dotenv
except ImportError:
    print("❌ 请先安装依赖: pip install -r requirements.txt")
    sys.exit(1)

# 加载环境变量
load_dotenv()

# OpenClaw 工作区
WORKSPACE = Path("/root/.openclaw/workspace")
HOME_OPENCLAW = Path("/root/.openclaw")

# GitHub 配置
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO", "fangbb-coder/OC-backup")  # 默认仓库

# 需要备份的文件列表（相对路径）
# 注意：此列表应根据个人需求自定义，以下为示例
BACKUP_FILES = [
    # 核心配置文件
    "openclaw.json",  # ~/.openclaw/openclaw.json

    # 长期记忆
    "MEMORY.md",

    # 用户信息
    "USER.md",
    "IDENTITY.md",
    "SOUL.md",

    # 工具配置
    "TOOLS.md",
    "HEARTBEAT.md",

    # 定时任务
    "cron/jobs.json",

    # 监控面板（如果存在）
    "openclaw-monitor/openclaw-monitor.cjs",
    "monitor/openclaw-monitor.cjs",

    # 自定义配置文件（按需添加）
    # 例如：你配置过的技能文件
    # "skills/your-skill/skill.yaml",
    # "skills/your-skill/README.md",

    # 自定义脚本（按需添加）
    # "stock_monitor.py",
    # "daily_xiaohongshu_post.py",
    # "start_xhs_mcp_xvfb.sh",
]

# 排除模式（不备份的文件/目录）
EXCLUDE_PATTERNS = [
    "skills/*/__pycache__",
    "skills/*/.pytest_cache",
    "skills/*/venv",
    "skills/*/node_modules",
    "skills/*/models",
    "memory/*.md",  # 每日记忆文件不备份（太大且动态）
    "cron/runs/*",  # 运行日志
    ".git",
    ".DS_Store",
    "*.log",
    "*.tmp",
]


def should_exclude(path: Path) -> bool:
    """检查是否应排除该文件"""
    for pattern in EXCLUDE_PATTERNS:
        if pattern.startswith("*"):
            # 后缀匹配
            if path.name.endswith(pattern[1:]):
                return True
        elif "*" in pattern:
            # 简单通配
            import fnmatch
            if fnmatch.fnmatch(str(path), pattern):
                return True
        else:
            # 路径包含
            if pattern in str(path):
                return True
    return False


def collect_backup_files():
    """收集需要备份的文件"""
    backup_files = []

    for rel_path in BACKUP_FILES:
        full_path = WORKSPACE / rel_path
        if full_path.exists() and full_path.is_file():
            if should_exclude(full_path):
                continue
            backup_files.append({
                "path": rel_path,
                "content": full_path.read_text(encoding='utf-8', errors='ignore'),
                "size": full_path.stat().st_size,
                "modified": full_path.stat().st_mtime
            })
        else:
            print(f"⚠️  文件不存在: {rel_path}")

    # 备份 MEMORY.md 到 GitHub
    memory_path = WORKSPACE / "MEMORY.md"
    if memory_path.exists():
        backup_files.append({
            "path": "MEMORY.md",
            "content": memory_path.read_text(encoding='utf-8'),
            "size": memory_path.stat().st_size,
            "modified": memory_path.stat().st_mtime
        })

    # 备份 openclaw.json（如果存在）
    config_path = HOME_OPENCLAW / "openclaw.json"
    if config_path.exists():
        backup_files.append({
            "path": "openclaw.json",
            "content": config_path.read_text(encoding='utf-8'),
            "size": config_path.stat().st_size,
            "modified": config_path.stat().st_mtime
        })

    return backup_files


def push_to_github(backup_files):
    """推送备份到 GitHub"""
    if not GITHUB_TOKEN:
        print("❌ 请设置 GITHUB_TOKEN 环境变量")
        sys.exit(1)

    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(GITHUB_REPO)

    # 创建 commit 消息
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_message = f"OpenClaw backup {timestamp}"

    # 获取默认分支
    default_branch = repo.default_branch
    ref = repo.get_git_ref(f"heads/{default_branch}")
    latest_commit = repo.get_commit(ref.object.sha)

    # 创建 tree
    tree_elements = []
    for file in backup_files:
        blob = repo.create_git_blob(file['content'], encoding='utf-8')
        element = {
            "path": file['path'],
            "mode": "100644",
            "type": "blob",
            "sha": blob.sha
        }
        tree_elements.append(element)

    tree = repo.create_git_tree(tree_elements, ref.object.sha)

    # 创建 commit
    commit = repo.create_git_commit(
        message=commit_message,
        tree=tree,
        parents=[latest_commit.commit]
    )

    # 更新分支
    ref.edit(commit.sha)

    print(f"✅ 备份成功！Commit: {commit.sha}")
    print(f"📦 备份文件数: {len(backup_files)}")
    print(f"🔗 仓库: https://github.com/{GITHUB_REPO}")

    return commit.sha


def restore_from_github():
    """从 GitHub 恢复备份"""
    if not GITHUB_TOKEN:
        print("❌ 请设置 GITHUB_TOKEN 环境变量")
        sys.exit(1)

    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(GITHUB_REPO)

    # 获取最新 commit
    commits = repo.get_commits()
    if commits.totalCount == 0:
        print("❌ 仓库为空，无法恢复")
        sys.exit(1)

    latest_commit = commits[0]

    # 遍历所有文件
    print(f"🔍 正在恢复备份 (commit: {latest_commit.sha[:8]})...")

    restored = 0
    for file in latest_commit.commit.files:
        if file.status in ['added', 'modified']:
            # 下载文件内容
            content = file.raw_data.decode('utf-8', errors='ignore')

            # 确定保存路径
            if file.path == "openclaw.json":
                save_path = HOME_OPENCLAW / "openclaw.json"
            else:
                save_path = WORKSPACE / file.path

            save_path.parent.mkdir(parents=True, exist_ok=True)
            save_path.write_text(content, encoding='utf-8')
            print(f"✅ 恢复: {file.path}")
            restored += 1

    print(f"✅ 恢复完成！共恢复 {restored} 个文件")
    print("⚠️  请重启 OpenClaw 服务以应用配置")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="OpenClaw Backup to GitHub")
    parser.add_argument("--action", choices=["backup", "restore"], required=True,
                        help="执行备份或恢复")
    parser.add_argument("--token", help="GitHub Token (也可设置 GITHUB_TOKEN 环境变量)")
    parser.add_argument("--repo", help="GitHub 仓库 (格式: owner/repo)")
    parser.add_argument("--dry-run", action="store_true", help="仅显示将要备份的文件，不执行")

    args = parser.parse_args()

    # 设置 token 和 repo
    if args.token:
        global GITHUB_TOKEN
        GITHUB_TOKEN = args.token
    if args.repo:
        global GITHUB_REPO
        GITHUB_REPO = args.repo

    if args.action == "backup":
        print("🔍 正在收集需要备份的文件...")
        files = collect_backup_files()
        print(f"📦 找到 {len(files)} 个文件:")
        for f in files:
            size_kb = f['size'] / 1024
            print(f"  - {f['path']} ({size_kb:.1f} KB)")

        if args.dry_run:
            print("✅ Dry-run 完成，未实际推送")
            return

        if len(files) == 0:
            print("⚠️  没有文件需要备份")
            return

        print(f"\n🚀 开始推送到 GitHub: {GITHUB_REPO}")
        sha = push_to_github(files)
        print(f"✅ 备份完成: {sha[:8]}")

    elif args.action == "restore":
        print("⚠️  恢复备份将覆盖现有配置文件！")
        confirm = input("确认恢复？(yes/no): ")
        if confirm.lower() != 'yes':
            print("取消恢复")
            return
        restore_from_github()


if __name__ == "__main__":
    main()
