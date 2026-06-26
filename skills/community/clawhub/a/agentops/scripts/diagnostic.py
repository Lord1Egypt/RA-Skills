#!/usr/bin/env python3
"""故障诊断工具 - 付费版

用法:
    python3 diagnostic.py
    python3 diagnostic.py --issue <问题类型>
    python3 diagnostic.py --json
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime


ISSUES = {
    "session_timeout": {
        "name": "会话超时",
        "description": "Agent会话频繁断开或超时",
    },
    "high_memory": {
        "name": "内存过高",
        "description": "Agent进程占用过多内存",
    },
    "slow_response": {
        "name": "响应缓慢",
        "description": "Agent响应时间过长",
    },
    "skill_error": {
        "name": "技能错误",
        "description": "技能加载或执行失败",
    },
    "connection_error": {
        "name": "连接错误",
        "description": "Agent无法连接到服务",
    },
    "config_error": {
        "name": "配置错误",
        "description": "配置文件有误导致启动失败",
    },
}


def check_disk_space():
    """检查磁盘空间"""
    try:
        stat = os.statvfs("/")
        total = stat.f_blocks * stat.f_frsize
        free = stat.f_bavail * stat.f_frsize
        usage_pct = round((total - free) / total * 100, 1)
        return {
            "usage_pct": usage_pct,
            "free_gb": round(free / (1024**3), 1),
            "ok": usage_pct < 90,
        }
    except Exception as e:
        return {"error": str(e), "ok": False}


def check_process():
    """检查关键进程"""
    results = {}

    # OpenClaw gateway
    try:
        result = subprocess.run(
            ["pgrep", "-f", "openclaw"],
            capture_output=True, text=True, timeout=5
        )
        pids = [p for p in result.stdout.strip().split("\n") if p]
        results["openclaw_gateway"] = {
            "running": len(pids) > 0,
            "pids": pids,
        }
    except Exception as e:
        results["openclaw_gateway"] = {"error": str(e)}

    # Node.js
    try:
        result = subprocess.run(
            ["node", "--version"],
            capture_output=True, text=True, timeout=5
        )
        results["node"] = {
            "available": result.returncode == 0,
            "version": result.stdout.strip(),
        }
    except Exception as e:
        results["node"] = {"error": str(e)}

    return results


def check_memory():
    """检查内存"""
    try:
        with open("/proc/meminfo", "r") as f:
            info = {}
            for line in f:
                parts = line.split()
                info[parts[0].rstrip(":")] = int(parts[1])
        total = info.get("MemTotal", 1)
        available = info.get("MemAvailable", info.get("MemFree", 0))
        usage_pct = round((total - available) / total * 100, 1)
        return {
            "usage_pct": usage_pct,
            "total_mb": round(total / 1024, 0),
            "available_mb": round(available / 1024, 0),
            "ok": usage_pct < 85,
        }
    except Exception as e:
        return {"error": str(e), "ok": False}


def check_config():
    """检查配置文件"""
    config_path = os.path.expanduser("~/.openclaw/openclaw.json")
    result = {"path": config_path}

    if not os.path.exists(config_path):
        result["exists"] = False
        result["ok"] = False
        return result

    result["exists"] = True
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
        result["valid_json"] = True
        result["ok"] = True
    except json.JSONDecodeError as e:
        result["valid_json"] = False
        result["error"] = str(e)
        result["ok"] = False

    return result


def diagnose_issue(issue_key):
    """诊断特定问题"""
    issue = ISSUES.get(issue_key)
    if not issue:
        return {
            "error": f"未知问题类型: {issue_key}",
            "available": list(ISSUES.keys()),
        }

    findings = []
    root_cause = None
    recommendations = []

    if issue_key == "session_timeout":
        # 检查网络
        checks = check_process()
        if not checks.get("openclaw_gateway", {}).get("running"):
            findings.append("Gateway进程未运行")
            root_cause = "gateway_stopped"
            recommendations.append("启动gateway: openclaw gateway start")

        cfg = check_config()
        if not cfg.get("ok"):
            findings.append(f"配置文件异常: {cfg.get('error', '文件不存在')}")
            root_cause = "config_error"
            recommendations.append("检查配置文件: ~/.openclaw/openclaw.json")

        if not root_cause:
            root_cause = "unknown"
            findings.append("Gateway运行正常，可能是网络或超时配置问题")
            recommendations.append("检查网络稳定性")
            recommendations.append("考虑调整session timeout配置")

    elif issue_key == "high_memory":
        mem = check_memory()
        if isinstance(mem, dict) and "usage_pct" in mem:
            if not mem["ok"]:
                findings.append(f"系统内存使用率: {mem['usage_pct']}%")
                root_cause = "system_memory_pressure"
                recommendations.append("检查是否有内存泄漏进程")
                recommendations.append("考虑增加swap空间")
            else:
                # 检查openclaw进程内存
                try:
                    result = subprocess.run(
                        ["ps", "aux"], capture_output=True, text=True, timeout=5
                    )
                    for line in result.stdout.split("\n"):
                        if "openclaw" in line.lower() and "grep" not in line:
                            parts = line.split()
                            mem_pct = float(parts[3]) if len(parts) > 3 else 0
                            if mem_pct > 5:
                                findings.append(f"OpenClaw进程内存: {mem_pct}%")
                                root_cause = "agent_memory_leak"
                                recommendations.append("考虑重启gateway释放内存")
                                recommendations.append("检查是否有大量未释放的会话")
                except Exception:
                    pass

        if not root_cause:
            root_cause = "normal"
            findings.append("内存使用在正常范围")

    elif issue_key == "slow_response":
        checks = check_process()
        if not checks.get("openclaw_gateway", {}).get("running"):
            root_cause = "gateway_stopped"
            findings.append("Gateway未运行")
            recommendations.append("启动gateway")
        else:
            load = None
            try:
                with open("/proc/loadavg", "r") as f:
                    parts = f.read().split()
                    load = float(parts[0])
            except Exception:
                pass

            cpu = None
            try:
                with open("/proc/stat", "r") as f:
                    parts = f.readline().split()
                user, nice, system, idle, iowait = (int(parts[i]) for i in range(1, 6))
                total = user + nice + system + idle + iowait
                cpu = round((1 - (idle + iowait) / total) * 100, 1)
            except Exception:
                pass

            if load and load > 4:
                findings.append(f"系统负载较高: {load}")
                root_cause = "system_overloaded"
                recommendations.append("减少并发任务")
            elif cpu and cpu > 80:
                findings.append(f"CPU使用率较高: {cpu}%")
                root_cause = "cpu_pressure"
                recommendations.append("检查是否有CPU密集型任务")
            else:
                root_cause = "network_or_api"
                findings.append("系统资源正常，可能是API响应慢")
                recommendations.append("检查模型API状态")
                recommendations.append("考虑使用更快的模型")

    elif issue_key == "skill_error":
        skills_dir = os.path.expanduser("~/.openclaw/skills")
        if not os.path.isdir(skills_dir):
            findings.append("用户技能目录不存在")
            root_cause = "skills_dir_missing"
            recommendations.append("创建技能目录: ~/.openclaw/skills")
        else:
            # 检查技能文件结构
            for name in os.listdir(skills_dir):
                skill_md = os.path.join(skills_dir, name, "SKILL.md")
                if os.path.isdir(os.path.join(skills_dir, name)) and not os.path.exists(skill_md):
                    findings.append(f"技能 '{name}' 缺少 SKILL.md")
                    root_cause = "missing_skill_md"
                    recommendations.append(f"为 '{name}' 添加 SKILL.md 或移除该目录")

        if not root_cause:
            root_cause = "normal"
            findings.append("技能目录结构正常")

    elif issue_key == "connection_error":
        # 检查网络连接
        try:
            result = subprocess.run(
                ["ping", "-c", "1", "-W", "3", "8.8.8.8"],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode != 0:
                findings.append("无法访问外网 (ping 8.8.8.8 失败)")
                root_cause = "network_down"
                recommendations.append("检查网络连接")
            else:
                findings.append("网络连接正常")
        except Exception:
            pass

        # 检查DNS
        try:
            with open("/etc/resolv.conf", "r") as f:
                content = f.read()
            if "nameserver" not in content:
                findings.append("DNS未配置")
                root_cause = "dns_missing"
                recommendations.append("配置 /etc/resolv.conf")
        except Exception:
            pass

        if not root_cause:
            root_cause = "api_specific"
            findings.append("网络连接正常，可能是特定API不可达")
            recommendations.append("检查模型API端点配置")

    elif issue_key == "config_error":
        cfg = check_config()
        if not cfg.get("exists"):
            root_cause = "config_missing"
            findings.append("配置文件不存在")
            recommendations.append("创建配置文件: ~/.openclaw/openclaw.json")
        elif not cfg.get("valid_json"):
            root_cause = "config_invalid"
            findings.append(f"JSON解析错误: {cfg.get('error')}")
            recommendations.append("修复配置文件JSON格式")
        else:
            root_cause = "normal"
            findings.append("配置文件格式正确")

    return {
        "issue": issue_key,
        "issue_name": issue["name"],
        "root_cause": root_cause,
        "findings": findings,
        "recommendations": recommendations,
        "timestamp": datetime.now().isoformat(),
    }


def format_text(result):
    """格式化文本输出"""
    if "error" in result and "issue" not in result:
        return f"❌ {result['error']}\n💡 可用问题类型: {', '.join(result.get('available', []))}"

    # 自动诊断模式
    if result.get("type") == "auto_diagnostic":
        lines = []
        lines.append("\n🔍 自动诊断报告")
        lines.append("=" * 45)
        checks = result.get("checks", {})
        for name, check in checks.items():
            ok = check.get("ok", check.get("running", check.get("valid_json", True)))
            emoji = "✅" if ok else "❌"
            if "error" in check:
                emoji = "⚠️"
            lines.append(f"  {emoji} {name}: {'OK' if ok else 'ISSUE'}")
        problems = result.get("problems", [])
        if problems:
            lines.append("")
            lines.append("  📋 发现的问题:")
            for p in problems:
                lines.append(f"    • {p}")
        return "\n".join(lines)

    lines = []
    lines.append(f"\n🔧 故障诊断: {result['issue_name']}")
    lines.append("=" * 45)
    lines.append(f"  根因: {result['root_cause']}")
    lines.append("")

    if result["findings"]:
        lines.append("  🔍 发现:")
        for f in result["findings"]:
            lines.append(f"    • {f}")

    if result["recommendations"]:
        lines.append("")
        lines.append("  💡 建议:")
        for i, r in enumerate(result["recommendations"], 1):
            lines.append(f"    {i}. {r}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="OpenClaw故障诊断工具")
    parser.add_argument(
        "--issue",
        choices=list(ISSUES.keys()),
        default=None,
        help="问题类型",
    )
    parser.add_argument("--json", action="store_true", help="输出JSON格式")
    parser.add_argument("--list", action="store_true", help="列出可用问题类型")
    args = parser.parse_args()

    if args.list:
        if args.json:
            print(json.dumps(ISSUES, ensure_ascii=False, indent=2))
        else:
            print("\n📋 可用问题类型")
            print("=" * 45)
            for key, info in ISSUES.items():
                print(f"  {key}: {info['description']}")
        return

    if args.issue:
        result = diagnose_issue(args.issue)
    else:
        # 自动检测：运行所有关键检查
        results = {}
        results["disk"] = check_disk_space()
        results["process"] = check_process()
        results["memory"] = check_memory()
        results["config"] = check_config()

        problems = []
        if not results["disk"].get("ok"):
            problems.append("磁盘空间不足")
        if not results["process"].get("openclaw_gateway", {}).get("running"):
            problems.append("Gateway未运行")
        if not results["memory"].get("ok"):
            problems.append("内存使用过高")
        if not results["config"].get("ok"):
            problems.append("配置异常")

        result = {
            "type": "auto_diagnostic",
            "timestamp": datetime.now().isoformat(),
            "checks": results,
            "problems": problems if problems else ["未发现明显问题"],
            "status": "issues_found" if problems else "all_clear",
        }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_text(result))


if __name__ == "__main__":
    main()
