#!/usr/bin/env python3
"""System health monitoring and reports."""

import argparse
import os
import platform
import socket
import subprocess
import sys
import time
from datetime import datetime


def get_cpu_info():
    """Get CPU information."""
    info = {"cores": os.cpu_count() or 0, "load": []}

    try:
        with open("/proc/loadavg") as f:
            parts = f.read().split()
            info["load"] = [float(x) for x in parts[:3]]
            info["load_1"], info["load_5"], info["load_15"] = info["load"]
    except (FileNotFoundError, ValueError):
        try:
            info["load"] = [float(x) for x in os.getloadavg()]
        except (OSError, AttributeError):
            pass

    # CPU usage from /proc/stat
    try:
        with open("/proc/stat") as f:
            line = f.readline()
        parts = line.split()[1:]
        vals = [int(x) for x in parts]
        idle = vals[3] + vals[4] if len(vals) > 4 else vals[3]
        total = sum(vals)
        info["idle_pct"] = (idle / total) * 100 if total > 0 else 0
        info["usage_pct"] = 100 - info["idle_pct"]
    except (FileNotFoundError, ValueError):
        info["usage_pct"] = None

    # Model name
    try:
        with open("/proc/cpuinfo") as f:
            for line in f:
                if "model name" in line:
                    info["model"] = line.split(":", 1)[1].strip()
                    break
    except FileNotFoundError:
        info["model"] = platform.processor() or "Unknown"

    return info


def get_memory_info():
    """Get memory information."""
    info = {}
    try:
        with open("/proc/meminfo") as f:
            mem = {}
            for line in f:
                parts = line.split()
                key = parts[0].rstrip(":")
                mem[key] = int(parts[1]) * 1024  # Convert kB to bytes

        info["total"] = mem.get("MemTotal", 0)
        info["available"] = mem.get("MemAvailable", mem.get("MemFree", 0))
        info["free"] = mem.get("MemFree", 0)
        info["buffers"] = mem.get("Buffers", 0)
        info["cached"] = mem.get("Cached", 0)
        info["used"] = info["total"] - info["available"]
        info["usage_pct"] = (info["used"] / info["total"]) * 100 if info["total"] > 0 else 0

        info["swap_total"] = mem.get("SwapTotal", 0)
        info["swap_free"] = mem.get("SwapFree", 0)
        info["swap_used"] = info["swap_total"] - info["swap_free"]
    except FileNotFoundError:
        # Fallback for non-Linux
        try:
            import multiprocessing
            info = {"total": 0, "usage_pct": 0, "available": 0}
        except Exception:
            pass

    return info


def get_disk_info():
    """Get disk usage information."""
    disks = []
    try:
        output = subprocess.check_output(["df", "-h"], text=True, timeout=5)
        for line in output.strip().split("\n")[1:]:
            parts = line.split()
            if len(parts) >= 6 and parts[0].startswith("/"):
                disks.append({
                    "device": parts[0],
                    "size": parts[1],
                    "used": parts[2],
                    "available": parts[3],
                    "usage_pct": int(parts[4].rstrip("%")),
                    "mount": parts[5],
                })
    except (subprocess.SubprocessError, FileNotFoundError):
        # Fallback using os.statvfs
        try:
            stat = os.statvfs("/")
            total = stat.f_blocks * stat.f_frsize
            free = stat.f_bavail * stat.f_frsize
            used = total - free
            pct = (used / total) * 100 if total > 0 else 0
            disks.append({
                "device": "/",
                "size": f"{total / 1024**3:.1f}G",
                "used": f"{used / 1024**3:.1f}G",
                "available": f"{free / 1024**3:.1f}G",
                "usage_pct": int(pct),
                "mount": "/",
            })
        except Exception:
            pass

    return disks


def get_network_info():
    """Get network information."""
    info = {"hostname": socket.gethostname(), "interfaces": []}

    try:
        # Get IP addresses
        result = subprocess.run(["ip", "-4", "addr", "show"], capture_output=True, text=True, timeout=5)
        current_if = None
        for line in result.stdout.split("\n"):
            if line and not line.startswith(" "):
                parts = line.split(":")
                if len(parts) >= 2:
                    current_if = parts[1].strip()
            elif "inet " in line and current_if:
                ip = line.strip().split()[1].split("/")[0]
                info["interfaces"].append({"name": current_if, "ip": ip})
    except (subprocess.SubprocessError, FileNotFoundError):
        # Fallback
        try:
            ip = socket.gethostbyname(socket.gethostname())
            info["interfaces"].append({"name": "default", "ip": ip})
        except Exception:
            pass

    # Check DNS
    try:
        socket.getaddrinfo("google.com", 80)
        info["dns_ok"] = True
    except Exception:
        info["dns_ok"] = False

    return info


def get_top_processes(n=10):
    """Get top processes by CPU/memory."""
    processes = []
    try:
        result = subprocess.run(
            ["ps", "aux", "--sort=-%mem"],
            capture_output=True, text=True, timeout=5
        )
        for line in result.stdout.strip().split("\n")[1:n+1]:
            parts = line.split(None, 10)
            if len(parts) >= 11:
                processes.append({
                    "user": parts[0],
                    "pid": parts[1],
                    "cpu": parts[2],
                    "mem": parts[3],
                    "command": parts[10][:60],
                })
    except (subprocess.SubprocessError, FileNotFoundError):
        pass

    return processes


def get_uptime():
    """Get system uptime."""
    try:
        with open("/proc/uptime") as f:
            seconds = float(f.read().split()[0])
        days = int(seconds // 86400)
        hours = int((seconds % 86400) // 3600)
        mins = int((seconds % 3600) // 60)
        return f"{days}d {hours}h {mins}m"
    except (FileNotFoundError, ValueError):
        return "Unknown"


def format_bytes(b):
    """Format bytes to human readable."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if b < 1024:
            return f"{b:.1f} {unit}"
        b /= 1024
    return f"{b:.1f} PB"


def health_bar(pct, width=20):
    """Generate a health bar."""
    filled = int(pct / 100 * width)
    if pct >= 90:
        char = "🔴"
    elif pct >= 70:
        char = "🟡"
    else:
        char = "🟢"
    bar = char * filled + "⬜" * (width - filled)
    return f"[{bar}] {pct:.0f}%"


def quick_check(threshold=80):
    """Run a quick health check."""
    print(f"🏥 System Health Check — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'═' * 50}\n")

    issues = []

    # CPU
    cpu = get_cpu_info()
    load_1 = cpu["load"][0] if cpu["load"] else 0
    cores = cpu["cores"]
    load_pct = (load_1 / cores * 100) if cores > 0 else 0
    status = "✅" if load_pct < threshold else "⚠️"
    print(f"  {status} CPU: {load_1:.2f} / {cores} cores ({load_pct:.0f}%)")
    if load_pct >= threshold:
        issues.append(f"CPU load high: {load_1:.2f}")

    # Memory
    mem = get_memory_info()
    if mem.get("total"):
        pct = mem["usage_pct"]
        status = "✅" if pct < threshold else "⚠️"
        print(f"  {status} Memory: {format_bytes(mem['used'])} / {format_bytes(mem['total'])} ({pct:.0f}%)")
        if pct >= threshold:
            issues.append(f"Memory usage high: {pct:.0f}%")

    # Disk
    for disk in get_disk_info():
        pct = disk["usage_pct"]
        status = "✅" if pct < threshold else "⚠️"
        print(f"  {status} Disk {disk['mount']}: {disk['used']} / {disk['size']} ({pct}%)")
        if pct >= threshold:
            issues.append(f"Disk {disk['mount']} full: {pct}%")

    # Network
    net = get_network_info()
    dns_status = "✅" if net["dns_ok"] else "❌"
    print(f"  {dns_status} DNS: {'OK' if net['dns_ok'] else 'FAILED'}")

    if not net["dns_ok"]:
        issues.append("DNS resolution failing")

    # Uptime
    uptime = get_uptime()
    print(f"  ℹ️  Uptime: {uptime}")

    print(f"\n{'═' * 50}")
    if issues:
        print(f"  ⚠️  {len(issues)} issue(s) detected:")
        for issue in issues:
            print(f"     • {issue}")
    else:
        print("  ✅ All systems nominal")


def full_report(output=None):
    """Generate a full system report."""
    lines = []

    def log(line=""):
        print(line)
        lines.append(line)

    log(f"📊 System Health Report")
    log(f"   Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log(f"{'═' * 60}")

    # System info
    log(f"\n🖥️  System Information")
    log(f"   Hostname:  {socket.gethostname()}")
    log(f"   OS:        {platform.system()} {platform.release()}")
    log(f"   Arch:      {platform.machine()}")
    log(f"   Python:    {platform.python_version()}")
    log(f"   Uptime:    {get_uptime()}")

    # CPU
    cpu = get_cpu_info()
    log(f"\n🔧 CPU")
    log(f"   Model:  {cpu.get('model', 'Unknown')}")
    log(f"   Cores:  {cpu['cores']}")
    if cpu["load"]:
        log(f"   Load:   {cpu['load'][0]:.2f} (1m)  {cpu['load'][1]:.2f} (5m)  {cpu['load'][2]:.2f} (15m)")
    if cpu.get("usage_pct") is not None:
        log(f"   Usage:  {health_bar(cpu['usage_pct'])}")

    # Memory
    mem = get_memory_info()
    if mem.get("total"):
        log(f"\n💾 Memory")
        log(f"   Total:     {format_bytes(mem['total'])}")
        log(f"   Used:      {format_bytes(mem['used'])}")
        log(f"   Available: {format_bytes(mem['available'])}")
        log(f"   Buffers:   {format_bytes(mem['buffers'])}")
        log(f"   Cached:    {format_bytes(mem['cached'])}")
        log(f"   Usage:     {health_bar(mem['usage_pct'])}")
        if mem.get("swap_total", 0) > 0:
            swap_pct = (mem["swap_used"] / mem["swap_total"]) * 100
            log(f"   Swap:      {format_bytes(mem['swap_used'])} / {format_bytes(mem['swap_total'])} ({swap_pct:.0f}%)")

    # Disk
    log(f"\n💿 Disk")
    for disk in get_disk_info():
        log(f"   {disk['mount']}")
        log(f"     Device: {disk['device']}")
        log(f"     Size:   {disk['size']}  Used: {disk['used']}  Avail: {disk['available']}")
        log(f"     Usage:  {health_bar(disk['usage_pct'])}")

    # Network
    net = get_network_info()
    log(f"\n🌐 Network")
    log(f"   Hostname: {net['hostname']}")
    for iface in net["interfaces"]:
        log(f"   {iface['name']}: {iface['ip']}")
    log(f"   DNS:      {'✅ OK' if net['dns_ok'] else '❌ FAILED'}")

    # Top processes
    procs = get_top_processes(5)
    if procs:
        log(f"\n📋 Top Processes (by memory)")
        log(f"   {'PID':<8} {'CPU%':<7} {'MEM%':<7} {'Command'}")
        log(f"   {'─' * 8} {'─' * 7} {'─' * 7} {'─' * 40}")
        for p in procs:
            log(f"   {p['pid']:<8} {p['cpu']:<7} {p['mem']:<7} {p['command']}")

    log(f"\n{'═' * 60}")

    if output:
        with open(output, "w") as f:
            f.write("\n".join(lines))
        print(f"\n📝 Report saved to {output}")


def monitor_loop(interval, threshold=80):
    """Continuous monitoring loop."""
    print(f"👁️  Monitoring system health (every {interval}s, Ctrl+C to stop)")
    print(f"   Alert threshold: {threshold}%\n")

    try:
        while True:
            now = datetime.now().strftime("%H:%M:%S")
            cpu = get_cpu_info()
            mem = get_memory_info()
            disks = get_disk_info()

            load_pct = (cpu["load"][0] / cpu["cores"] * 100) if cpu["load"] and cpu["cores"] else 0
            mem_pct = mem.get("usage_pct", 0)
            disk_max = max((d["usage_pct"] for d in disks), default=0)

            alerts = []
            if load_pct >= threshold:
                alerts.append(f"CPU {load_pct:.0f}%")
            if mem_pct >= threshold:
                alerts.append(f"MEM {mem_pct:.0f}%")
            if disk_max >= threshold:
                alerts.append(f"DISK {disk_max}%")

            alert_str = f" ⚠️  {', '.join(alerts)}" if alerts else ""
            print(f"[{now}] CPU: {load_pct:.0f}% | MEM: {mem_pct:.0f}% | DISK: {disk_max}%{alert_str}")

            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n🛑 Monitoring stopped")


def main():
    parser = argparse.ArgumentParser(description="🏥 System Health — monitor system resources")
    sub = parser.add_subparsers(dest="command")

    p_check = sub.add_parser("check", help="Quick health check")
    p_check.add_argument("--category", choices=["cpu", "memory", "disk", "network", "processes"])
    p_check.add_argument("--threshold", type=int, default=80, help="Alert threshold %%")

    p_report = sub.add_parser("report", help="Generate full report")
    p_report.add_argument("--output", "-o", help="Save report to file")
    p_report.add_argument("--threshold", type=int, default=80)

    p_mon = sub.add_parser("monitor", help="Continuous monitoring")
    p_mon.add_argument("--interval", type=int, default=60, help="Seconds between checks")
    p_mon.add_argument("--threshold", type=int, default=80, help="Alert threshold %%")

    args = parser.parse_args()

    if args.command == "check":
        if args.category == "cpu":
            cpu = get_cpu_info()
            print(f"🔧 CPU: {cpu.get('model', 'Unknown')}, {cpu['cores']} cores")
            print(f"   Load: {cpu['load']}")
        elif args.category == "memory":
            mem = get_memory_info()
            print(f"💾 Memory: {format_bytes(mem.get('used', 0))} / {format_bytes(mem.get('total', 0))}")
        elif args.category == "disk":
            for d in get_disk_info():
                print(f"💿 {d['mount']}: {d['used']}/{d['size']} ({d['usage_pct']}%)")
        elif args.category == "network":
            net = get_network_info()
            print(f"🌐 DNS: {'OK' if net['dns_ok'] else 'FAILED'}")
            for i in net["interfaces"]:
                print(f"   {i['name']}: {i['ip']}")
        elif args.category == "processes":
            for p in get_top_processes(5):
                print(f"   {p['pid']} {p['mem']}% {p['command']}")
        else:
            quick_check(args.threshold)
    elif args.command == "report":
        full_report(args.output)
    elif args.command == "monitor":
        monitor_loop(args.interval, args.threshold)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
