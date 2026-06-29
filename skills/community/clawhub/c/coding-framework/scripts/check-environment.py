#!/usr/bin/env python3
"""
check-environment.py — 环境检查脚本

检查 coding-framework 所需的依赖和环境。

用法:
  python scripts/check-environment.py
  python scripts/check-environment.py --json
  python scripts/check-environment.py --verbose
"""

import argparse
import json
import os
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional


def get_version_output(cmd: list) -> Optional[str]:
    """执行命令并返回输出，失败返回 None。"""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=10,
        )
        return result.stdout.strip() or result.stderr.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return None


def check_python() -> dict:
    """检查 Python 版本。"""
    version = sys.version_info
    result = {
        "name": "Python",
        "required": True,
        "required_version": "3.10+",
        "installed": True,
        "version": f"{version.major}.{version.minor}.{version.micro}",
        "ok": version.major >= 3 and version.minor >= 10,
    }
    if not result["ok"]:
        result["message"] = "Python 3.10+ 是必需的"
    return result


def check_git() -> dict:
    """检查 Git 版本。"""
    output = get_version_output(["git", "--version"])
    if not output:
        return {
            "name": "Git",
            "required": True,
            "required_version": "2.28+",
            "installed": False,
            "ok": False,
            "message": "Git 未安装或不在 PATH 中",
        }
    
    # 解析版本: git version 2.42.0
    match = re.search(r"(\d+\.\d+(?:\.\d+)?)", output)
    version = match.group(1) if match else "unknown"
    
    # 检查版本 >= 2.28
    ok = True
    if match:
        parts = version.split(".")
        major, minor = int(parts[0]), int(parts[1]) if len(parts) > 1 else 0
        ok = major > 2 or (major == 2 and minor >= 28)
    
    return {
        "name": "Git",
        "required": True,
        "required_version": "2.28+",
        "installed": True,
        "version": version,
        "ok": ok,
        "message": None if ok else "Git 2.28+ 是必需的（worktree 支持）",
    }


def check_bash() -> dict:
    """检查 bash 版本。"""
    # Windows: 检查 Git Bash
    if platform.system() == "Windows":
        # 尝试常见路径
        git_bash_paths = [
            r"C:\Program Files\Git\bin\bash.exe",
            r"C:\Program Files (x86)\Git\bin\bash.exe",
            os.path.expanduser(r"~\AppData\Local\Programs\Git\bin\bash.exe"),
        ]
        for path in git_bash_paths:
            if Path(path).exists():
                return {
                    "name": "bash (Git Bash)",
                    "required": True,
                    "required_version": "4.0+",
                    "installed": True,
                    "version": "Git Bash",
                    "path": path,
                    "ok": True,
                }
        return {
            "name": "bash",
            "required": True,
            "required_version": "4.0+",
            "installed": False,
            "ok": False,
            "message": "Windows 需要安装 Git Bash",
        }
    
    # Unix: 检查 bash
    output = get_version_output(["bash", "--version"])
    if not output:
        return {
            "name": "bash",
            "required": True,
            "required_version": "4.0+",
            "installed": False,
            "ok": False,
            "message": "bash 未安装或不在 PATH 中",
        }
    
    # 解析版本: GNU bash, version 5.2.15
    match = re.search(r"version\s+(\d+\.\d+)", output)
    version = match.group(1) if match else "unknown"
    
    ok = True
    if match:
        major = int(version.split(".")[0])
        ok = major >= 4
    
    return {
        "name": "bash",
        "required": True,
        "required_version": "4.0+",
        "installed": True,
        "version": version,
        "ok": ok,
        "message": None if ok else "bash 4.0+ 是必需的",
    }


def check_jq() -> dict:
    """检查 jq（可选）。"""
    output = get_version_output(["jq", "--version"])
    if not output:
        return {
            "name": "jq",
            "required": False,
            "required_version": "1.6+",
            "installed": False,
            "ok": True,  # 可选，不算失败
            "message": "jq 未安装，hook 脚本将使用 bash fallback（功能受限）",
        }
    
    # 解析版本: jq-1.6
    match = re.search(r"(\d+\.\d+)", output)
    version = match.group(1) if match else "unknown"
    
    return {
        "name": "jq",
        "required": False,
        "required_version": "1.6+",
        "installed": True,
        "version": version,
        "ok": True,
    }


def check_claude_code() -> dict:
    """检查 Claude Code（可选）。"""
    output = get_version_output(["claude", "--version"])
    if not output:
        return {
            "name": "Claude Code",
            "required": False,
            "required_version": "latest",
            "installed": False,
            "ok": True,
            "message": "Claude Code 未安装（外部代理委派需要）",
        }
    
    return {
        "name": "Claude Code",
        "required": False,
        "required_version": "latest",
        "installed": True,
        "version": output.split("\n")[0],
        "ok": True,
    }


def check_codex() -> dict:
    """检查 Codex（可选）。"""
    output = get_version_output(["codex", "--version"])
    if not output:
        return {
            "name": "Codex",
            "required": False,
            "required_version": "latest",
            "installed": False,
            "ok": True,
            "message": "Codex 未安装（外部代理委派需要）",
        }
    
    return {
        "name": "Codex",
        "required": False,
        "required_version": "latest",
        "installed": True,
        "version": output.split("\n")[0],
        "ok": True,
    }


def check_workspace() -> dict:
    """检查是否在 Git 仓库中。"""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        is_repo = result.stdout.strip() == "true"
        return {
            "name": "Git 仓库",
            "required": False,
            "ok": is_repo,
            "message": None if is_repo else "当前目录不是 Git 仓库（迭代循环的 Git 集成需要）",
        }
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return {
            "name": "Git 仓库",
            "required": False,
            "ok": False,
            "message": "无法检查 Git 仓库状态",
        }


def main():
    parser = argparse.ArgumentParser(
        description="环境检查脚本 — 检查 coding-framework 所需的依赖和环境"
    )
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    parser.add_argument("--verbose", action="store_true", help="显示详细信息")
    args = parser.parse_args()
    
    checks = [
        check_python(),
        check_git(),
        check_bash(),
        check_jq(),
        check_claude_code(),
        check_codex(),
        check_workspace(),
    ]
    
    # 统计
    required_ok = sum(1 for c in checks if c.get("required") and c.get("ok"))
    required_total = sum(1 for c in checks if c.get("required"))
    optional_ok = sum(1 for c in checks if not c.get("required") and c.get("ok"))
    optional_total = sum(1 for c in checks if not c.get("required"))
    
    all_ok = required_ok == required_total
    
    if args.json:
        output = {
            "success": all_ok,
            "platform": platform.system(),
            "checks": checks,
            "summary": {
                "required": f"{required_ok}/{required_total}",
                "optional": f"{optional_ok}/{optional_total}",
            }
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print(f"\n{'='*50}")
        print(f"  coding-framework 环境检查")
        print(f"  平台: {platform.system()} {platform.release()}")
        print(f"{'='*50}\n")
        
        print("必需依赖:")
        for c in checks:
            if c.get("required"):
                status = "✅" if c.get("ok") else "❌"
                version = c.get("version", "N/A")
                print(f"  {status} {c['name']} {version}")
                if c.get("message"):
                    print(f"     └─ {c['message']}")
        
        print("\n可选依赖:")
        for c in checks:
            if not c.get("required"):
                status = "✅" if c.get("installed") else "⚠️"
                version = c.get("version", "未安装")
                print(f"  {status} {c['name']} {version}")
                if c.get("message") and args.verbose:
                    print(f"     └─ {c['message']}")
        
        print(f"\n{'='*50}")
        print(f"  必需: {required_ok}/{required_total}  |  可选: {optional_ok}/{optional_total}")
        print(f"{'='*50}\n")
        
        if all_ok:
            print("✅ 环境检查通过！coding-framework 可以正常运行。")
        else:
            print("❌ 环境检查失败，请安装缺少的必需依赖。")
            sys.exit(1)


if __name__ == "__main__":
    main()
