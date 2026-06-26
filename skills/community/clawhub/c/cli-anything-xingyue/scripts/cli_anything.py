#!/usr/bin/env python3
"""
CLI-Anything for OpenClaw
调用 CLI-Anything 方法论为任意软件生成 CLI 工具
"""

import argparse
import os
import subprocess
import sys
import json
from pathlib import Path

CLI_ANYTHING_REPO = "https://github.com/HKUDS/CLI-Anything.git"
DEFAULT_CLONE_DIR = Path.home() / ".openclaw" / "cli-anything"


def run_command(cmd, cwd=None, capture=True):
    """执行命令"""
    print(f"🔧 执行: {' '.join(cmd)}")
    result = subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=capture,
        text=True
    )
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    return result.returncode == 0


def ensure_cli_anything():
    """确保 CLI-Anything 仓库已克隆"""
    if DEFAULT_CLONE_DIR.exists():
        print(f"📂 CLI-Anything 已存在于 {DEFAULT_CLONE_DIR}")
        # 更新
        os.chdir(DEFAULT_CLONE_DIR)
        run_command(["git", "pull"])
    else:
        print(f"📥 克隆 CLI-Anything 仓库...")
        run_command(["git", "clone", CLI_ANYTHING_REPO, str(DEFAULT_CLONE_DIR)])
    
    return DEFAULT_CLONE_DIR


def build_cli(software_path, refine=False):
    """构建或优化 CLI"""
    cli_anything_dir = ensure_cli_anything()
    
    # 检查路径
    if not Path(software_path).exists():
        print(f"❌ 错误: 路径不存在: {software_path}")
        return False
    
    # 调用 Codex skill 的方式执行
    # 由于 CLI-Anything 对所有平台的生成器是一样的，我们直接使用 Python 实现
    print(f"\n🚀 开始构建 CLI for: {software_path}")
    
    # 使用 CLI-Anything 的核心逻辑
    # 这里我们可以调用其核心模块或直接生成
    os.chdir(cli_anything_dir)
    
    # 检查是否有 codex-skill
    if (cli_anything_dir / "codex-skill").exists():
        print("📦 使用 Codex skill 方法...")
        # 在这里可以进一步调用
        return True
    
    print("⚠️  警告: CLI-Anything 仓库结构可能已变化")
    return False


def validate_cli(software_path):
    """验证生成的 CLI"""
    harness_dir = Path(software_path) / "agent-harness"
    
    if not harness_dir.exists():
        print(f"❌ 错误: 未找到 harness 目录: {harness_dir}")
        return False
    
    print(f"✅ 验证 CLI: {software_path}")
    
    checks = []
    
    # 检查目录结构
    required_files = ["setup.py"]
    for f in required_files:
        if (harness_dir / f).exists():
            checks.append(f"✓ {f} 存在")
        else:
            checks.append(f"✗ {f} 缺失")
    
    # 检查 cli_anything 目录
    if (harness_dir / "cli_anything").exists():
        checks.append("✓ cli_anything 命名空间包存在")
    else:
        checks.append("✗ cli_anything 命名空间包缺失")
    
    for check in checks:
        print(check)
    
    return all("✓" in c for c in checks)


def list_clis():
    """列出所有已生成的 CLI"""
    # 查找当前目录下的 agent-harness
    print("📋 已生成的 CLI 工具:")
    
    cli_dirs = []
    for root, dirs, files in os.walk(os.getcwd()):
        if "agent-harness" in dirs:
            software = Path(root).name
            cli_dirs.append(software)
            print(f"  • {software}")
    
    if not cli_dirs:
        print("  (无)")
        print("\n提示: 使用 /cli-build <路径> 构建新的 CLI")


def main():
    parser = argparse.ArgumentParser(description="CLI-Anything for OpenClaw")
    subparsers = parser.add_subparsers(dest="command", help="子命令")
    
    # build 命令
    build_parser = subparsers.add_parser("build", help="构建 CLI")
    build_parser.add_argument("path", help="软件路径或 GitHub 仓库 URL")
    
    # refine 命令
    refine_parser = subparsers.add_parser("refine", help="优化 CLI")
    refine_parser.add_argument("path", help="软件路径")
    refine_parser.add_argument("focus", nargs="?", default="", help="优化重点")
    
    # validate 命令
    validate_parser = subparsers.add_parser("validate", help="验证 CLI")
    validate_parser.add_argument("path", help="软件路径")
    
    # list 命令
    subparsers.add_parser("list", help="列出已生成的 CLI")
    
    args = parser.parse_args()
    
    if args.command == "build":
        build_cli(args.path)
    elif args.command == "refine":
        build_cli(args.path, refine=True)
    elif args.command == "validate":
        validate_cli(args.path)
    elif args.command == "list":
        list_clis()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
