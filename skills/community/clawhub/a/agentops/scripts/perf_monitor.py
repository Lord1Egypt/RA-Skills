#!/usr/bin/env python3
"""性能监控基础指标 - 免费版

用法:
    python3 perf_monitor.py
    python3 perf_monitor.py --watch 30
    python3 perf_monitor.py --json
"""

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime


def get_cpu_usage():
    """获取CPU使用率"""
    try:
        # 使用 /proc/stat 计算CPU使用率
        with open("/proc/stat", "r") as f:
            line = f.readline()
        parts = line.split()
        if parts[0] != "cpu":
            return None
        user, nice, system, idle, iowait = (int(parts[i]) for i in range(1, 6))
        total = user + nice + system + idle + iowait
        idle_total = idle + iowait
        cpu_usage = round((1 - idle_total / total) * 100, 1) if total > 0 else 0
        return cpu_usage
    except Exception:
        # Fallback: 使用 top
        try:
            result = subprocess.run(
                ["top", "-bn1"], capture_output=True, text=True, timeout=5
            )
            for line in result.stdout.split("\n"):
                if "Cpu" in line or "cpu" in line:
                    # Parse: %id (idle)
                    import re
                    idle_match = re.search(r"(\d+\.?\d*)\s*(?:id|idle)", line, re.IGNORECASE)
                    if idle_match:
                        return round(100 - float(idle_match.group(1)), 1)
        except Exception:
            pass
    return None


def get_memory_usage():
    """获取内存使用情况"""
    try:
        with open("/proc/meminfo", "r") as f:
            info = {}
            for line in f:
                parts = line.split()
                info[parts[0].rstrip(":")] = int(parts[1])

        total = info.get("MemTotal", 1)
        available = info.get("MemAvailable", info.get("MemFree", 0))
        used = total - available
        usage_pct = round(used / total * 100, 1)

        return {
            "total_mb": round(total / 1024, 0),
            "used_mb": round(used / 1024, 0),
            "available_mb": round(available / 1024, 0),
            "usage_pct": usage_pct,
        }
    except Exception as e:
        return {"error": str(e)}


def get_disk_usage():
    """获取磁盘使用情况"""
    results = {}
    for mount in ["/", "/home"]:
        try:
            stat = os.statvfs(mount)
            total = stat.f_blocks * stat.f_frsize
            free = stat.f_bavail * stat.f_frsize
            used = total - free
            results[mount] = {
                "total_gb": round(total / (1024**3), 1),
                "used_gb": round(used / (1024**3), 1),
                "free_gb": round(free / (1024**3), 1),
                "usage_pct": round(used / total * 100, 1) if total > 0 else 0,
            }
        except Exception as e:
            results[mount] = {"error": str(e)}
    return results


def get_process_count():
    """获取进程数"""
    try:
        pids = [
            p for p in os.listdir("/proc")
            if p.isdigit()
        ]
        return len(pids)
    except Exception:
        return None


def get_load_average():
    """获取系统负载"""
    try:
        with open("/proc/loadavg", "r") as f:
            parts = f.read().split()
        return {
            "1min": float(parts[0]),
            "5min": float(parts[1]),
            "15min": float(parts[2]),
        }
    except Exception:
        return None


def get_openclaw_process_info():
    """获取OpenClaw进程信息"""
    results = []
    try:
        result = subprocess.run(
            ["ps", "aux"], capture_output=True, text=True, timeout=5
        )
        for line in result.stdout.split("\n"):
            if "openclaw" in line.lower() and "grep" not in line:
                parts = line.split()
                if len(parts) >= 11:
                    results.append({
                        "user": parts[0],
                        "cpu_pct": parts[2],
                        "mem_pct": parts[3],
                        "vsz_mb": round(int(parts[4]) / 1024, 1),
                        "rss_mb": round(int(parts[5]) / 1024, 1),
                        "command": " ".join(parts[10:]),
                    })
    except Exception:
        pass
    return results


def take_snapshot():
    """采集一次性能快照"""
    return {
        "cpu_usage_pct": get_cpu_usage(),
        "memory": get_memory_usage(),
        "disk": get_disk_usage(),
        "load_average": get_load_average(),
        "process_count": get_process_count(),
        "openclaw_processes": get_openclaw_process_info(),
        "timestamp": datetime.now().isoformat(),
    }


def format_text(snapshot):
    """格式化文本输出"""
    lines = []
    lines.append("\n📊 性能监控快照")
    lines.append("=" * 45)

    # CPU
    cpu = snapshot.get("cpu_usage_pct")
    if cpu is not None:
        emoji = "🟢" if cpu < 50 else "🟡" if cpu < 80 else "🔴"
        lines.append(f"  {emoji} CPU使用率: {cpu}%")

    # Memory
    mem = snapshot.get("memory", {})
    if isinstance(mem, dict) and "usage_pct" in mem:
        emoji = "🟢" if mem["usage_pct"] < 50 else "🟡" if mem["usage_pct"] < 80 else "🔴"
        lines.append(f"  {emoji} 内存使用: {mem['usage_pct']}% ({mem['used_mb']:.0f}MB / {mem['total_mb']:.0f}MB)")

    # Disk
    disk = snapshot.get("disk", {})
    for mount, info in disk.items():
        if isinstance(info, dict) and "usage_pct" in info:
            emoji = "🟢" if info["usage_pct"] < 50 else "🟡" if info["usage_pct"] < 80 else "🔴"
            lines.append(f"  {emoji} 磁盘 ({mount}): {info['usage_pct']}% (已用{info['used_gb']}GB / 共{info['total_gb']}GB)")

    # Load
    load = snapshot.get("load_average")
    if load:
        lines.append(f"  📈 系统负载: {load['1min']} / {load['5min']} / {load['15min']}")

    # Process count
    pc = snapshot.get("process_count")
    if pc:
        lines.append(f"  🔢 进程数: {pc}")

    # OpenClaw processes
    oc_procs = snapshot.get("openclaw_processes", [])
    if oc_procs:
        lines.append(f"  🐾 OpenClaw进程数: {len(oc_procs)}")
        for p in oc_procs[:5]:
            lines.append(f"    → CPU:{p['cpu_pct']}% MEM:{p['mem_pct']}% RSS:{p['rss_mb']}MB {p['command'][:60]}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="OpenClaw性能监控工具")
    parser.add_argument("--watch", type=int, default=0, help="持续监控间隔(秒)")
    parser.add_argument("--json", action="store_true", help="输出JSON格式")
    args = parser.parse_args()

    if args.watch > 0:
        print(f"🔍 持续监控中，每{args.watch}秒采集一次 (Ctrl+C 停止)")
        print("-" * 45)
        try:
            while True:
                snapshot = take_snapshot()
                if args.json:
                    print(json.dumps(snapshot, ensure_ascii=False, indent=2))
                else:
                    print(format_text(snapshot))
                    print(f"  [{datetime.now().strftime('%H:%M:%S')}]")
                    print("-" * 45)
                time.sleep(args.watch)
        except KeyboardInterrupt:
            print("\n⏹ 监控已停止")
    else:
        snapshot = take_snapshot()
        if args.json:
            print(json.dumps(snapshot, ensure_ascii=False, indent=2))
        else:
            print(format_text(snapshot))
            print(f"\n💡 免费版功能: 基础性能监控 | 付费版: 性能报告、自动化告警")


if __name__ == "__main__":
    main()
