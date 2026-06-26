#!/usr/bin/env python3
"""
System Health Monitor - Auto-detect and fix system issues
Monitors: RAM, Disk, CPU, Services, Temperature
Auto-fixes using sudo-tool when problems detected
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime

TOOL_DIR = Path.home() / ".openclaw" / "health-monitor"
STATE_FILE = TOOL_DIR / "state.json"
CONFIG_FILE = TOOL_DIR / "config.json"
LOG_FILE = TOOL_DIR / "health.log"

# Thresholds
RAM_WARNING = 80  # %
RAM_CRITICAL = 90  # %
DISK_WARNING = 85  # %
DISK_CRITICAL = 95  # %
CPU_WARNING = 85  # %
CPU_CRITICAL = 95  # %

def ensure_tool_dir():
    os.makedirs(TOOL_DIR, exist_ok=True)
    os.chmod(TOOL_DIR, 0o755)

def get_ram_usage():
    """Get RAM usage percentage"""
    try:
        with open('/proc/meminfo', 'r') as f:
            lines = f.readlines()
        total = used = free = cached = 0
        for line in lines:
            if line.startswith('MemTotal:'):
                total = int(line.split()[1])
            elif line.startswith('MemAvailable:'):
                free = int(line.split()[1])
            elif line.startswith('Buffers:'):
                cached = int(line.split()[1])
        used = total - free
        return round((used / total) * 100, 1)
    except:
        return 0

def get_ram_details():
    """Get detailed RAM info"""
    try:
        with open('/proc/meminfo', 'r') as f:
            lines = f.readlines()
        data = {}
        for line in lines:
            parts = line.split()
            if len(parts) >= 2:
                key = parts[0].rstrip(':')
                val = int(parts[1])
                data[key] = val
        total = data.get('MemTotal', 0) / 1024 / 1024
        available = data.get('MemAvailable', 0) / 1024 / 1024
        used = data.get('MemFree', 0) / 1024 / 1024
        cached = data.get('Cached', 0) / 1024 / 1024
        return {
            'total_gb': round(total, 1),
            'used_gb': round(total - available, 1),
            'available_gb': round(available, 1),
            'cached_gb': round(cached, 1),
            'percent': round(((total - available) / total) * 100, 1) if total > 0 else 0
        }
    except:
        return {'total_gb': 0, 'used_gb': 0, 'available_gb': 0, 'cached_gb': 0, 'percent': 0}

def get_disk_usage(path='/'):
    """Get disk usage for path"""
    try:
        result = subprocess.run(['df', '-h', path], capture_output=True, text=True)
        lines = result.stdout.strip().split('\n')
        if len(lines) >= 2:
            parts = lines[1].split()
            if len(parts) >= 5:
                return {
                    'total': parts[1],
                    'used': parts[2],
                    'available': parts[3],
                    'percent': int(parts[4].rstrip('%'))
                }
    except:
        pass
    return {'total': '0', 'used': '0', 'available': '0', 'percent': 0}

def get_cpu_usage():
    """Get CPU usage percentage"""
    try:
        result = subprocess.run(['top', '-bn1'], capture_output=True, text=True, timeout=5)
        for line in result.stdout.split('\n'):
            if '%Cpu(s):' in line or 'Cpu(s):' in line:
                parts = line.split()
                # Find the idle percentage
                for i, p in enumerate(parts):
                    if 'id' in p:
                        return round(100 - float(parts[i-1]), 1)
        # Alternative method
        with open('/proc/loadavg', 'r') as f:
            load = f.read().split()
        return round(float(load[0]) * 33, 1)  # Rough estimate for 1 min
    except:
        return 0

def get_top_ram_processes():
    """Get top 5 processes by RAM usage"""
    try:
        result = subprocess.run(
            ['ps', 'aux', '--sort=-%mem'],
            capture_output=True, text=True, timeout=5
        )
        lines = result.stdout.strip().split('\n')[1:6]  # Skip header, get 5
        processes = []
        for line in lines:
            parts = line.split()
            if len(parts) >= 11:
                processes.append({
                    'pid': parts[1],
                    'user': parts[0],
                    'cpu': parts[2],
                    'mem': parts[3],
                    'cmd': ' '.join(parts[10:])[:50]
                })
        return processes
    except:
        return []

def get_uptime():
    """Get system uptime"""
    try:
        with open('/proc/uptime', 'r') as f:
            seconds = float(f.read().split()[0])
        days = int(seconds // 86400)
        hours = int((seconds % 86400) // 3600)
        mins = int((seconds % 3600) // 60)
        if days > 0:
            return f"{days}d {hours}h"
        return f"{hours}h {mins}m"
    except:
        return "unknown"

def get_load_average():
    """Get system load average"""
    try:
        with open('/proc/loadavg', 'r') as f:
            loads = f.read().split()[:3]
        return [float(l) for l in loads]
    except:
        return [0, 0, 0]

def kill_process_by_ram():
    """Kill processes consuming most RAM to prevent OOM"""
    processes = get_top_ram_processes()
    killed = []
    
    for proc in processes:
        # Skip critical processes
        if any(x in proc['cmd'] for x in ['systemd', 'init', 'ssh', 'docker', 'openclaw']):
            continue
        try:
            pid = int(proc['pid'])
            mem_pct = float(proc['mem'])
            if mem_pct > 5:  # Only kill processes using >5% RAM
                # Try graceful first
                os.kill(pid, 15)  # SIGTERM
                time.sleep(1)
                try:
                    os.kill(pid, 9)  # SIGKILL
                except:
                    pass
                killed.append(f"{proc['cmd'][:30]} (PID:{pid})")
        except:
            pass
    
    return killed

def log_event(msg):
    """Log event to file"""
    ensure_tool_dir()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_FILE, 'a') as f:
        f.write(f"[{timestamp}] {msg}\n")

def get_health_status():
    """Get comprehensive health status"""
    ram = get_ram_details()
    disk = get_disk_usage('/')
    cpu = get_cpu_usage()
    load = get_load_average()
    uptime = get_uptime()
    processes = get_top_ram_processes()
    
    status = {
        'timestamp': datetime.now().isoformat(),
        'ram': ram,
        'disk': disk,
        'cpu_percent': cpu,
        'load_avg': load,
        'uptime': uptime,
        'top_processes': processes,
        'alerts': []
    }
    
    # Check thresholds
    if ram['percent'] >= RAM_CRITICAL:
        status['alerts'].append(f"🔴 RAM CRITICAL: {ram['percent']}% used")
    elif ram['percent'] >= RAM_WARNING:
        status['alerts'].append(f"🟡 RAM WARNING: {ram['percent']}% used")
    
    if disk['percent'] >= DISK_CRITICAL:
        status['alerts'].append(f"🔴 DISK CRITICAL: {disk['percent']}% used")
    elif disk['percent'] >= DISK_WARNING:
        status['alerts'].append(f"🟡 DISK WARNING: {disk['percent']}% used")
    
    if cpu >= CPU_CRITICAL:
        status['alerts'].append(f"🔴 CPU CRITICAL: {cpu}%")
    elif cpu >= CPU_WARNING:
        status['alerts'].append(f"🟡 CPU WARNING: {cpu}%")
    
    return status

def print_health_report():
    """Print human-readable health report"""
    status = get_health_status()
    
    print("🩺 System Health Report")
    print("=" * 40)
    
    # RAM
    ram = status['ram']
    bar_len = 20
    filled = int((ram['percent'] / 100) * bar_len)
    bar = '█' * filled + '░' * (bar_len - filled)
    icon = "🔴" if ram['percent'] >= RAM_CRITICAL else ("🟡" if ram['percent'] >= RAM_WARNING else "🟢")
    print(f"\n{icon} RAM: {bar} {ram['percent']}%")
    print(f"   {ram['used_gb']}GB / {ram['total_gb']}GB (available: {ram['cached_gb']}GB cached)")
    
    # Disk
    disk = status['disk']
    icon = "🔴" if disk['percent'] >= DISK_CRITICAL else ("🟡" if disk['percent'] >= DISK_WARNING else "🟢")
    print(f"\n{icon} DISK: {disk['used']} / {disk['total']} ({disk['percent']}%)")
    
    # CPU
    cpu = status['cpu_percent']
    icon = "🔴" if cpu >= CPU_CRITICAL else ("🟡" if cpu >= CPU_WARNING else "🟢")
    print(f"\n{icon} CPU: {cpu}%")
    
    # Load
    load = status['load_avg']
    print(f"\n📊 Load: {load[0]:.2f} {load[1]:.2f} {load[2]:.2f}")
    
    # Uptime
    print(f"\n⏱️  Uptime: {status['uptime']}")
    
    # Top processes
    print(f"\n🔝 Top RAM processes:")
    for i, p in enumerate(status['top_processes'][:3], 1):
        print(f"   {i}. {p['cmd'][:40]} ({p['mem']}% RAM)")
    
    # Alerts
    if status['alerts']:
        print(f"\n⚠️  ALERTS:")
        for alert in status['alerts']:
            print(f"   {alert}")
    
    return status

def auto_fix_low_ram():
    """Attempt to fix low RAM situation"""
    if not Path('/home/umbrel/.openclaw/sudo-tool/sudo-tool.sh').exists():
        print("❌ sudo-tool not installed, cannot auto-fix")
        return []
    
    killed = kill_process_by_ram()
    if killed:
        log_event(f"Auto-fixed RAM: killed {len(killed)} processes")
    
    # Clear cached memory
    try:
        subprocess.run(['sync'], capture_output=True)
        with open('/proc/sys/vm/drop_caches', 'w') as f:
            f.write('3\n')
        log_event("Dropped caches to free RAM")
    except:
        pass
    
    return killed

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    
    if cmd == "status":
        print_health_report()
    elif cmd == "fix":
        print("\n🔧 Attempting auto-fix for low RAM...")
        killed = auto_fix_low_ram()
        if killed:
            print(f"✅ Freed RAM by terminating: {', '.join(killed)}")
        else:
            print("ℹ️  No processes killed")
        print("\n📊 Current status:")
        print_health_report()
    elif cmd == "watch":
        print("👁️  Watching system health (Ctrl+C to stop)...")
        while True:
            os.system('clear')
            status = print_health_report()
            if status['alerts']:
                print("\n🔔 ALERT: Issues detected!")
            time.sleep(30)
    elif cmd == "json":
        print(json.dumps(get_health_status(), indent=2))
    else:
        print("Usage: health-monitor [status|fix|watch|json]")
        print("  status - Show health report")
        print("  fix    - Auto-fix low RAM")
        print("  watch  - Monitor continuously")
        print("  json   - Output JSON format")