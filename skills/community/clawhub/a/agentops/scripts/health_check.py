#!/usr/bin/env python3
"""Agent健康检查工具 - 免费版

用法:
    python3 health_check.py --check <service|session|config|all>
    python3 health_check.py --check all --json
"""

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime


def check_service():
    """检查OpenClaw服务运行状态"""
    results = {}

    # 检查 gateway 进程
    try:
        result = subprocess.run(
            ["pgrep", "-f", "openclaw"],
            capture_output=True, text=True, timeout=5
        )
        pids = result.stdout.strip().split("\n") if result.stdout.strip() else []
        results["gateway_process"] = {
            "status": "running" if pids else "stopped",
            "pids": [p for p in pids if p],
        }
    except Exception as e:
        results["gateway_process"] = {"status": "error", "error": str(e)}

    # 检查 gateway 端口
    try:
        result = subprocess.run(
            ["ss", "-tlnp"],
            capture_output=True, text=True, timeout=5
        )
        port_in_use = any(
            ":3000" in line or ":3001" in line
            for line in result.stdout.split("\n")
        )
        results["gateway_port"] = {
            "status": "listening" if port_in_use else "not_listening",
            "checked_ports": [3000, 3001],
        }
    except Exception as e:
        results["gateway_port"] = {"status": "error", "error": str(e)}

    # 检查 Node.js 可用性
    try:
        result = subprocess.run(
            ["node", "--version"],
            capture_output=True, text=True, timeout=5
        )
        results["node_runtime"] = {
            "status": "ok" if result.returncode == 0 else "error",
            "version": result.stdout.strip(),
        }
    except Exception as e:
        results["node_runtime"] = {"status": "error", "error": str(e)}

    overall = all(
        r.get("status") in ("running", "listening", "ok")
        for r in results.values()
    )

    return {
        "check": "service",
        "status": "healthy" if overall else "degraded",
        "details": results,
        "timestamp": datetime.now().isoformat(),
    }


def check_session():
    """检查Agent会话状态"""
    workspace = os.path.expanduser("~/.openclaw/workspace/agent")
    results = {}

    # 检查 workspace 是否存在
    results["workspace"] = {
        "path": workspace,
        "exists": os.path.isdir(workspace),
    }

    # 检查关键文件
    key_files = ["SOUL.md", "USER.md", "AGENTS.md", "MEMORY.md"]
    file_status = {}
    for f in key_files:
        path = os.path.join(workspace, f)
        file_status[f] = {
            "exists": os.path.exists(path),
            "size_bytes": os.path.getsize(path) if os.path.exists(path) else 0,
        }
    results["key_files"] = file_status

    # 检查 memory 目录
    mem_dir = os.path.join(workspace, "memory")
    if os.path.isdir(mem_dir):
        daily_files = [
            f for f in os.listdir(mem_dir)
            if f.endswith(".md") and f.startswith("20")
        ]
        results["memory_dir"] = {
            "exists": True,
            "daily_files_count": len(daily_files),
            "latest_file": sorted(daily_files)[-1] if daily_files else None,
        }
    else:
        results["memory_dir"] = {"exists": False}

    overall = results["workspace"]["exists"] and all(
        fs["exists"] for fs in file_status.values()
    )

    return {
        "check": "session",
        "status": "healthy" if overall else "degraded",
        "details": results,
        "timestamp": datetime.now().isoformat(),
    }


def check_config():
    """检查配置有效性"""
    config_path = os.path.expanduser("~/.openclaw/openclaw.json")
    results = {}

    results["config_file"] = {
        "path": config_path,
        "exists": os.path.exists(config_path),
    }

    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
            results["config_file"]["valid_json"] = True
            results["config_file"]["keys"] = list(config.keys())

            # 检查关键配置项
            critical = ["plugins", "skills", "gateway"]
            missing = [k for k in critical if k not in config]
            results["config_validation"] = {
                "critical_keys_present": len(missing) == 0,
                "missing_keys": missing,
            }
        except json.JSONDecodeError as e:
            results["config_file"]["valid_json"] = False
            results["config_file"]["error"] = str(e)

    # 检查 skills 目录
    skills_dirs = [
        os.path.expanduser("~/.openclaw/skills"),
        os.path.expanduser("~/.nvm/versions/node/v24.14.0/lib/node_modules/openclaw/skills"),
    ]
    skills_info = {}
    for d in skills_dirs:
        if os.path.isdir(d):
            skills_info[d] = {
                "exists": True,
                "skill_count": len(os.listdir(d)),
            }
        else:
            skills_info[d] = {"exists": False}
    results["skills_dirs"] = skills_info

    overall = results["config_file"]["exists"] and results.get("config_validation", {}).get("critical_keys_present", False)

    return {
        "check": "config",
        "status": "healthy" if overall else "degraded",
        "details": results,
        "timestamp": datetime.now().isoformat(),
    }


def format_text(data):
    """格式化文本输出"""
    lines = []
    check = data["check"]
    status = data["status"]
    emoji = "✅" if status == "healthy" else "⚠️"

    labels = {
        "service": "🔧 服务状态",
        "session": "💬 会话状态",
        "config": "⚙️ 配置状态",
    }
    lines.append(f"\n{labels.get(check, check)} [{status}]")
    lines.append("=" * 45)

    details = data.get("details", {})
    for key, val in details.items():
        if isinstance(val, dict):
            lines.append(f"  {key}:")
            for k, v in val.items():
                lines.append(f"    {k}: {v}")
        else:
            lines.append(f"  {key}: {val}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="OpenClaw Agent健康检查工具")
    parser.add_argument(
        "--check", choices=["service", "session", "config", "all"],
        default="all", help="检查类型"
    )
    parser.add_argument("--json", action="store_true", help="输出JSON格式")
    args = parser.parse_args()

    checks = {
        "service": check_service,
        "session": check_session,
        "config": check_config,
    }

    if args.check == "all":
        results = []
        for name, fn in checks.items():
            try:
                results.append(fn())
            except Exception as e:
                results.append({
                    "check": name,
                    "status": "error",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat(),
                })

        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            for r in results:
                print(format_text(r))
            print(f"\n💡 检查完成于 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("   免费版功能: 健康检查 | 付费版: 配置优化、自动化告警、故障诊断")
    else:
        try:
            result = checks[args.check]()
        except Exception as e:
            result = {
                "check": args.check,
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }

        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(format_text(result))
            print(f"\n💡 检查完成于 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
