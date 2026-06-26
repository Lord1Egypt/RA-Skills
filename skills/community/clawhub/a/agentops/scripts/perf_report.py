#!/usr/bin/env python3
"""性能报告生成 - 付费版

用法:
    python3 perf_report.py
    python3 perf_report.py --period 7d
    python3 perf_report.py --output report.md
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime


def get_system_info():
    """获取系统信息"""
    info = {}

    # 主机名
    try:
        info["hostname"] = subprocess.run(
            ["hostname"], capture_output=True, text=True, timeout=5
        ).stdout.strip()
    except Exception:
        info["hostname"] = "unknown"

    # 系统信息
    try:
        with open("/proc/version", "r") as f:
            info["kernel"] = f.read().split("(")[0].strip()
    except Exception:
        info["kernel"] = "unknown"

    # CPU信息
    try:
        with open("/proc/cpuinfo", "r") as f:
            for line in f:
                if line.startswith("model name"):
                    info["cpu"] = line.split(":")[1].strip()
                    break
        with open("/proc/cpuinfo", "r") as f:
            cores = sum(1 for line in f if line.startswith("processor"))
            info["cpu_cores"] = cores
    except Exception:
        info["cpu"] = "unknown"
        info["cpu_cores"] = 0

    # 内存
    try:
        with open("/proc/meminfo", "r") as f:
            for line in f:
                if line.startswith("MemTotal"):
                    info["memory_total_gb"] = round(
                        int(line.split()[1]) / (1024 * 1024), 1
                    )
                    break
    except Exception:
        info["memory_total_gb"] = 0

    return info


def get_current_metrics():
    """获取当前指标"""
    metrics = {}

    # CPU
    try:
        with open("/proc/stat", "r") as f:
            parts = f.readline().split()
        user, nice, system, idle, iowait = (int(parts[i]) for i in range(1, 6))
        total = user + nice + system + idle + iowait
        metrics["cpu_usage_pct"] = round((1 - (idle + iowait) / total) * 100, 1)
    except Exception:
        metrics["cpu_usage_pct"] = None

    # Memory
    try:
        with open("/proc/meminfo", "r") as f:
            info = {}
            for line in f:
                parts = line.split()
                info[parts[0].rstrip(":")] = int(parts[1])
        total = info.get("MemTotal", 1)
        available = info.get("MemAvailable", info.get("MemFree", 0))
        metrics["memory_usage_pct"] = round((total - available) / total * 100, 1)
        metrics["memory_total_gb"] = round(total / (1024 * 1024), 1)
        metrics["memory_available_gb"] = round(available / (1024 * 1024), 1)
    except Exception:
        metrics["memory_usage_pct"] = None

    # Disk
    try:
        stat = os.statvfs("/")
        total = stat.f_blocks * stat.f_frsize
        free = stat.f_bavail * stat.f_frsize
        metrics["disk_usage_pct"] = round((total - free) / total * 100, 1)
        metrics["disk_free_gb"] = round(free / (1024**3), 1)
    except Exception:
        metrics["disk_usage_pct"] = None

    # Load
    try:
        with open("/proc/loadavg", "r") as f:
            parts = f.read().split()
            metrics["load_1min"] = float(parts[0])
            metrics["load_5min"] = float(parts[1])
            metrics["load_15min"] = float(parts[2])
    except Exception:
        metrics["load_1min"] = None

    # Uptime
    try:
        with open("/proc/uptime", "r") as f:
            seconds = float(f.read().split()[0])
            days = int(seconds / 86400)
            hours = int((seconds % 86400) / 3600)
            metrics["uptime"] = f"{days}天{hours}小时"
    except Exception:
        metrics["uptime"] = "unknown"

    # Process count
    try:
        metrics["process_count"] = len([
            p for p in os.listdir("/proc") if p.isdigit()
        ])
    except Exception:
        metrics["process_count"] = 0

    return metrics


def get_openclaw_info():
    """获取OpenClaw相关信息"""
    info = {}

    # 版本
    try:
        result = subprocess.run(
            ["openclaw", "--version"], capture_output=True, text=True, timeout=10
        )
        info["version"] = result.stdout.strip() or "unknown"
    except Exception:
        info["version"] = "unknown"

    # Workspace统计
    workspace = os.path.expanduser("~/.openclaw/workspace")
    agent_count = 0
    if os.path.isdir(workspace):
        agent_count = len([
            d for d in os.listdir(workspace)
            if os.path.isdir(os.path.join(workspace, d))
        ])
    info["agent_count"] = agent_count

    # Skills统计
    skills_dir = os.path.expanduser("~/.openclaw/skills")
    skill_count = 0
    if os.path.isdir(skills_dir):
        skill_count = len(os.listdir(skills_dir))
    info["skill_count"] = skill_count

    # Gateway状态
    try:
        result = subprocess.run(
            ["pgrep", "-f", "openclaw"],
            capture_output=True, text=True, timeout=5
        )
        info["gateway_running"] = bool(result.stdout.strip())
    except Exception:
        info["gateway_running"] = False

    return info


def assess_health(metrics):
    """评估系统健康状态"""
    score = 100
    issues = []

    cpu = metrics.get("cpu_usage_pct")
    if cpu is not None:
        if cpu > 90:
            score -= 30
            issues.append("CPU使用率过高 (>90%)")
        elif cpu > 70:
            score -= 10
            issues.append("CPU使用率偏高 (>70%)")

    mem = metrics.get("memory_usage_pct")
    if mem is not None:
        if mem > 90:
            score -= 30
            issues.append("内存使用率过高 (>90%)")
        elif mem > 70:
            score -= 10
            issues.append("内存使用率偏高 (>70%)")

    disk = metrics.get("disk_usage_pct")
    if disk is not None:
        if disk > 90:
            score -= 25
            issues.append("磁盘空间严重不足 (>90%)")
        elif disk > 80:
            score -= 10
            issues.append("磁盘空间不足 (>80%)")

    load = metrics.get("load_1min")
    if load is not None:
        if load > 8:
            score -= 15
            issues.append("系统负载极高")
        elif load > 4:
            score -= 5
            issues.append("系统负载偏高")

    return {
        "score": max(0, score),
        "issues": issues,
        "status": "healthy" if score >= 80 else "warning" if score >= 50 else "critical",
    }


def generate_report():
    """生成性能报告"""
    system = get_system_info()
    metrics = get_current_metrics()
    oc = get_openclaw_info()
    health = assess_health(metrics)

    return {
        "timestamp": datetime.now().isoformat(),
        "system": system,
        "metrics": metrics,
        "openclaw": oc,
        "health": health,
    }


def format_markdown(report):
    """格式化为Markdown报告"""
    lines = []
    lines.append("# 📊 AgentOps 性能报告")
    lines.append("")
    lines.append(f"**生成时间**: {report['timestamp']}")
    lines.append("")

    # 系统信息
    sys_info = report["system"]
    lines.append("## 系统信息")
    lines.append("")
    lines.append(f"- **主机**: {sys_info.get('hostname', 'unknown')}")
    lines.append(f"- **CPU**: {sys_info.get('cpu', 'unknown')} ({sys_info.get('cpu_cores', 0)}核)")
    lines.append(f"- **内存**: {sys_info.get('memory_total_gb', 0)}GB")
    lines.append(f"- **内核**: {sys_info.get('kernel', 'unknown')}")
    lines.append("")

    # 健康状态
    health = report["health"]
    status_emoji = {"healthy": "✅", "warning": "⚠️", "critical": "🔴"}
    lines.append(f"## 健康状态 {status_emoji.get(health['status'], '❓')}")
    lines.append("")
    lines.append(f"- **评分**: {health['score']}/100")
    lines.append(f"- **状态**: {health['status']}")
    if health["issues"]:
        lines.append("- **问题**:")
        for issue in health["issues"]:
            lines.append(f"  - {issue}")
    lines.append("")

    # 性能指标
    m = report["metrics"]
    lines.append("## 性能指标")
    lines.append("")
    if m.get("cpu_usage_pct") is not None:
        lines.append(f"- **CPU使用率**: {m['cpu_usage_pct']}%")
    if m.get("memory_usage_pct") is not None:
        lines.append(f"- **内存使用**: {m['memory_usage_pct']}% ({m.get('memory_available_gb', 0)}GB可用)")
    if m.get("disk_usage_pct") is not None:
        lines.append(f"- **磁盘使用**: {m['disk_usage_pct']}% ({m.get('disk_free_gb', 0)}GB可用)")
    if m.get("load_1min") is not None:
        lines.append(f"- **系统负载**: {m['load_1min']} / {m.get('load_5min', '?')} / {m.get('load_15min', '?')}")
    if m.get("uptime"):
        lines.append(f"- **运行时间**: {m['uptime']}")
    if m.get("process_count"):
        lines.append(f"- **进程数**: {m['process_count']}")
    lines.append("")

    # OpenClaw信息
    oc = report["openclaw"]
    lines.append("## OpenClaw状态")
    lines.append("")
    lines.append(f"- **版本**: {oc.get('version', 'unknown')}")
    lines.append(f"- **Gateway**: {'运行中' if oc.get('gateway_running') else '未运行'}")
    lines.append(f"- **Agent数**: {oc.get('agent_count', 0)}")
    lines.append(f"- **技能数**: {oc.get('skill_count', 0)}")
    lines.append("")

    # 建议
    lines.append("## 建议")
    lines.append("")
    if health["score"] >= 90:
        lines.append("✅ 系统运行良好，无需特别处理。")
    else:
        for issue in health["issues"]:
            if "CPU" in issue:
                lines.append("- 考虑优化CPU密集型任务或使用更快模型")
            if "内存" in issue:
                lines.append("- 检查是否有内存泄漏，考虑重启gateway")
            if "磁盘" in issue:
                lines.append("- 清理不必要的文件或日志")
            if "负载" in issue:
                lines.append("- 减少并发任务或优化任务调度")
    lines.append("")

    lines.append("---")
    lines.append("*由 AgentOps 自动生成*")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="OpenClaw性能报告生成")
    parser.add_argument(
        "--period", default="now",
        choices=["now", "1d", "7d", "30d"],
        help="报告周期",
    )
    parser.add_argument("--output", default=None, help="输出文件路径")
    parser.add_argument("--json", action="store_true", help="输出JSON格式")
    args = parser.parse_args()

    report = generate_report()

    if args.json:
        output = json.dumps(report, ensure_ascii=False, indent=2)
    else:
        output = format_markdown(report)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"✅ 报告已保存到: {args.output}")
    else:
        print(output)
        if not args.json:
            print(f"\n💡 AgentOps Pro 功能: 性能报告 | 免费版: 基础监控、日志分析")


if __name__ == "__main__":
    main()
