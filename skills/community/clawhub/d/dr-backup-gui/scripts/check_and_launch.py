#!/usr/bin/env python3
"""
DR Backup GUI — Dependency checker and launcher.
Usage: python3 check_and_launch.py [--install]
"""
import subprocess
import sys
import shutil
import os
import json

TOOLS = {
    "velero": {
        "check": ["velero", "version"],
        "install": "brew install velero  # macOS\n# or: curl -L https://raw.githubusercontent.com/vmware-tanzu/velero/main/install | kubectl apply -f -",
        "desc": "K8s 备份与恢复",
    },
    "rclone": {
        "check": ["rclone", "version"],
        "install": "brew install rclone  # macOS\n# or: https://rclone.org/install/",
        "desc": "云存储同步 (70+ 后端)",
    },
    "rsync": {
        "check": ["rsync", "--version"],
        "install": "brew install rsync  # macOS (or pre-installed)",
        "desc": "文件级增量同步",
    },
    "coriolis": {
        "check": ["coriolis", "--version"],
        "install": "pip install python-coriolisclient\n# or: https://Coriolis.readthedocs.io/",
        "desc": "跨云平台迁移",
    },
}

REQUIRED_PY = {
    "PyQt6": "PyQt6",
}

def check_py_pkg(name: str) -> bool:
    try:
        __import__(name.lower().replace("-", "_"))
        return True
    except ImportError:
        return False

def check_tool(name: str, cmd: list) -> bool:
    try:
        r = subprocess.run(cmd, capture_output=True, timeout=10)
        return r.returncode == 0
    except Exception:
        return False

def print_report():
    print("=" * 55)
    print("  DR Backup GUI — 依赖检查报告")
    print("=" * 55)
    all_ok = True

    print("\n[Python 包]")
    for pkg, import_name in REQUIRED_PY.items():
        ok = check_py_pkg(import_name)
        icon = "✅" if ok else "❌"
        print(f"  {icon} {pkg}")
        if not ok:
            all_ok = False

    print("\n[系统工具]")
    for tool, info in TOOLS.items():
        ok = check_tool(tool, info["check"])
        icon = "✅" if ok else "❌"
        print(f"  {icon} {tool:10s} — {info['desc']}")
        if not ok:
            all_ok = False
            print(f"     安装: {info['install'][:60]}...")

    print()
    if all_ok:
        print("✅ 所有依赖已就绪！运行: python3 dr_backup_gui.py")
    else:
        print("⚠️  部分依赖未安装。运行: python3 check_and_launch.py --install")
        print("   或手动安装缺失依赖。")
    return all_ok

def install_deps():
    print("正在安装 Python 依赖...")
    subprocess.run([sys.executable, "-m", "pip", "install", "PyQt6", "--quiet"])
    print("✅ PyQt6 已安装")
    print()
    print("=" * 55)
    print("  系统工具安装提示 (请手动安装):")
    print("=" * 55)
    for tool, info in TOOLS.items():
        ok = check_tool(tool, info["check"])
        if not ok:
            print(f"\n  {tool}:")
            for line in info["install"].split("\n"):
                print(f"    {line}")

if __name__ == "__main__":
    if "--install" in sys.argv:
        install_deps()
    else:
        print_report()
