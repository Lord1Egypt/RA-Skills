#!/usr/bin/env python3
"""
CLI-Anything Skill for OpenClaw
让任意软件都可以被 AI Agent 控制
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

# 配置
CLI_ANYTHING_REPO = "https://github.com/HKUDS/CLI-Anything.git"
INSTALL_DIR = Path.home() / ".openclaw" / "cli-anything"


def ensure_repo():
    """确保 CLI-Anything 仓库已安装"""
    if not INSTALL_DIR.exists():
        print(f"📥 克隆 CLI-Anything 仓库...")
        subprocess.run(["git", "clone", CLI_ANYTHING_REPO, str(INSTALL_DIR)], check=True)
        print(f"✅ 已克隆到 {INSTALL_DIR}")
    else:
        print(f"📂 CLI-Anything 已安装: {INSTALL_DIR}")
        # 可选：更新
        # os.chdir(INSTALL_DIR)
        # subprocess.run(["git", "pull"], capture_output=True)
    
    return INSTALL_DIR


def list_available_clis():
    """列出所有可用的 CLI"""
    print("📋 可用的 CLI 工具:")
    print("-" * 40)
    
    if not INSTALL_DIR.exists():
        print("  (CLI-Anything 未安装)")
        return []
    
    clis = []
    for item in INSTALL_DIR.iterdir():
        if item.is_dir():
            harness = item / "agent-harness"
            if harness.exists():
                clis.append(item.name)
                print(f"  • {item.name}")
    
    if not clis:
        print("  (无预生成的 CLI)")
    
    return clis


def install_cli(software_name: str):
    """安装指定的 CLI 到系统"""
    if not INSTALL_DIR.exists():
        ensure_repo()
    
    harness_dir = INSTALL_DIR / software_name / "agent-harness"
    
    if not harness_dir.exists():
        print(f"❌ 未找到 CLI: {software_name}")
        print("使用 /cli-list 查看可用 CLI")
        return False
    
    print(f"📦 安装 CLI: {software_name}")
    print(f"   目录: {harness_dir}")
    
    # 安装到当前用户
    result = subprocess.run(
        ["pip", "install", "-e", "."],
        cwd=harness_dir,
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print(f"✅ 安装成功!")
        print(f"   命令: cli-anything-{software_name}")
        return True
    else:
        print(f"❌ 安装失败:")
        print(result.stderr)
        return False


def cmd_build(software_path: str):
    """构建 CLI"""
    if not software_path:
        print("❌ 请指定软件路径")
        print()
        print("用法:")
        print("  /cli-build ./gimp                    # 本地软件")
        print("  /cli-build https://github.com/...   # GitHub 仓库")
        print()
        print("💡 提示: 还可以直接安装预生成的 CLI:")
        print("  /cli-install gimp")
        print("  /cli-install blender")
        return
    
    print(f"🚀 开始构建 CLI for: {software_path}")
    print()
    print("=" * 50)
    print("💡 CLI-Anything 完整构建需要在 Claude Code 或 Codex 中进行")
    print("=" * 50)
    print()
    print("步骤:")
    print("  1. 在 Claude Code 中:")
    print("     /plugin marketplace add HKUDS/CLI-Anything")
    print("     /plugin install cli-anything")
    print("     /cli-anything:cli-anything " + software_path)
    print()
    print("  2. 构建完成后，将生成的 agent-harness 目录复制到")
    print(f"     {INSTALL_DIR}/<软件名>/")
    print()
    print("  3. 然后使用 /cli-install <软件名> 安装")


def cmd_refine(software_path: str, focus: str = ""):
    """优化 CLI"""
    if not software_path:
        print("❌ 请指定软件路径")
        return
    
    print(f"🔧 优化 CLI for: {software_path}")
    if focus:
        print(f"📌 优化重点: {focus}")
    
    print()
    print("请在 Claude Code 或 Codex 中运行:")
    print(f"  /cli-anything:refine {software_path} {focus}")


def cmd_validate(software_path: str):
    """验证 CLI"""
    if not software_path:
        print("❌ 请指定软件路径")
        return
    
    harness_dir = Path(software_path) / "agent-harness"
    
    if not harness_dir.exists():
        print(f"❌ 未找到 harness 目录: {harness_dir}")
        print("请先使用 /cli-build 构建 CLI")
        return
    
    print(f"🔍 验证 CLI: {software_path}")
    print("-" * 30)
    
    # 检查必要文件
    checks = []
    
    check_file = harness_dir / "setup.py"
    status = "✅" if check_file.exists() else "❌"
    print(f"{status} setup.py")
    checks.append(check_file.exists())
    
    check_dir = harness_dir / "cli_anything"
    status = "✅" if check_dir.exists() else "❌"
    print(f"{status} cli_anything/")
    checks.append(check_dir.exists())
    
    print("-" * 30)
    
    if all(checks):
        print("✅ CLI 验证通过!")
    else:
        print("❌ CLI 验证失败")


def cmd_install(software_name: str):
    """安装 CLI"""
    if not software_name:
        print("❌ 请指定要安装的 CLI 名称")
        print()
        list_available_clis()
        return
    
    # 转换为小写
    software_name = software_name.lower()
    
    # 检查可用的
    available = list_available_clis()
    
    # 尝试匹配
    match = None
    for cli in available:
        if cli.lower() == software_name:
            match = cli
            break
    
    if match:
        install_cli(match)
    else:
        print(f"❌ 未找到: {software_name}")
        print()
        print("可用的 CLI:")
        for cli in available:
            print(f"  • {cli}")


def cmd_list():
    """列出已生成的 CLI"""
    list_available_clis()


def main():
    if len(sys.argv) < 2:
        cmd_list()
        return
    
    command = sys.argv[1]
    
    if command == "build":
        software_path = sys.argv[2] if len(sys.argv) > 2 else ""
        cmd_build(software_path)
    elif command == "refine":
        software_path = sys.argv[2] if len(sys.argv) > 2 else ""
        focus = sys.argv[3] if len(sys.argv) > 3 else ""
        cmd_refine(software_path, focus)
    elif command == "validate":
        software_path = sys.argv[2] if len(sys.argv) > 2 else ""
        cmd_validate(software_path)
    elif command == "install":
        software_name = sys.argv[2] if len(sys.argv) > 2 else ""
        cmd_install(software_name)
    elif command == "list":
        cmd_list()
    else:
        print(f"未知命令: {command}")
        print()
        print("可用命令:")
        print("  /cli-build <路径>     - 构建新的 CLI")
        print("  /cli-install <名称>   - 安装预生成的 CLI")
        print("  /cli-refine <路径>    - 优化 CLI")
        print("  /cli-validate <路径>  - 验证 CLI")
        print("  /cli-list             - 列出可用 CLI")


if __name__ == "__main__":
    main()
