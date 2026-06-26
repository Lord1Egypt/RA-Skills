#!/usr/bin/env python3
"""
AgentPulse — Thin monitoring agent
Reports system metrics to the AgentPulse cloud API.

Usage:
  agentpulse-agent --quick          # Fast health check
  agentpulse-agent --full           # Comprehensive report
  agentpulse-agent --install        # Install cron entries
"""

import argparse
import json
import os
import platform
import subprocess
import sys
import time
import urllib.request
import urllib.error
import ssl

# --- Configuration ---
CONFIG_PATH = os.environ.get("AGENTPULSE_CONF", "/etc/agentpulse.conf")
API_KEY = os.environ.get("AGENTPULSE_API_KEY", "")
SERVER_ID = os.environ.get("AGENTPULSE_SERVER_ID", "")
API_URL = os.environ.get("AGENTPULSE_API_URL", "https://api.agentpulse.io")


def load_config():
    """Load config from file if env vars aren't set."""
    global API_KEY, SERVER_ID, API_URL
    if not API_KEY and os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH) as f:
            for line in f:
                line = line.strip()
                if "=" in line and not line.startswith("#"):
                    key, val = line.split("=", 1)
                    key, val = key.strip(), val.strip()
                    if key == "API_KEY":
                        API_KEY = API_KEY or val
                    elif key == "SERVER_ID":
                        SERVER_ID = SERVER_ID or val
                    elif key == "API_URL":
                        API_URL = API_URL or val


# --- Service aliases for cross-distro compat ---
SERVICE_ALIASES = {
    "sshd": "ssh",
    "docker-engine": "docker",
}

IGNORED_INACTIVE = {"docker", "telegraf", "containerd"}

CRITICAL_SERVICES = ["ssh", "cron", "rsyslog", "systemd-resolved"]
WARNING_SERVICES = ["fail2ban", "docker", "telegraf"]


def get_service_status(name):
    """Check if a systemd service is active."""
    resolved = SERVICE_ALIASES.get(name, name)
    try:
        result = subprocess.run(
            ["systemctl", "is-active", resolved],
            capture_output=True, text=True, timeout=5
        )
        return result.stdout.strip() == "active"
    except Exception:
        return False


def collect_quick():
    """Fast health check — services + basic resource usage."""
    load1, load5, load15 = os.getloadavg()
    mem_info = {}
    try:
        with open("/proc/meminfo") as f:
            for line in f:
                parts = line.split()
                if len(parts) >= 2:
                    mem_info[parts[0].rstrip(":")] = int(parts[1])
    except IOError:
        pass

    mem_total = mem_info.get("MemTotal", 0) * 1024
    mem_available = mem_info.get("MemAvailable", 0) * 1024
    mem_used_pct = round((1 - mem_available / mem_total) * 100, 1) if mem_total else 0

    disk_used_pct = 0
    try:
        stat = os.statvfs("/")
        total = stat.f_blocks * stat.f_frsize
        avail = stat.f_bavail * stat.f_frsize
        disk_used_pct = round((1 - avail / total) * 100, 1) if total else 0
    except OSError:
        pass

    services = {}
    for svc in CRITICAL_SERVICES + WARNING_SERVICES:
        if svc not in services:
            services[svc] = get_service_status(svc)

    return {
        "hostname": platform.node(),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "report_type": "quick",
        "load": {"1min": load1, "5min": load5, "15min": load15},
        "memory": {"used_pct": mem_used_pct, "total_bytes": mem_total, "available_bytes": mem_available},
        "disk": {"used_pct": disk_used_pct},
        "services": services,
    }


def collect_full():
    """Comprehensive report including processes, ports, and network."""
    data = collect_quick()
    data["report_type"] = "full"

    # Process count
    try:
        data["processes"] = len([p for p in os.listdir("/proc") if p.isdigit()])
    except OSError:
        data["processes"] = 0

    # Listening ports
    ports = set()
    try:
        result = subprocess.run(
            ["ss", "-tlnp"], capture_output=True, text=True, timeout=10
        )
        for line in result.stdout.splitlines()[1:]:
            parts = line.split()
            if len(parts) >= 4:
                addr = parts[3]
                if ":" in addr:
                    port = addr.rsplit(":", 1)[-1]
                    if port.isdigit():
                        ports.add(int(port))
    except Exception:
        pass
    data["listening_ports"] = sorted(ports)

    # Uptime
    try:
        with open("/proc/uptime") as f:
            data["uptime_seconds"] = float(f.read().split()[0])
    except OSError:
        pass

    return data


def send_report(data):
    """POST metrics to the AgentPulse API."""
    url = f"{API_URL}/api/v1/report"
    payload = json.dumps({
        "server_id": SERVER_ID,
        "api_key": API_KEY,
        "metrics": data,
    }).encode()

    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})

    # Allow self-signed certs for dogfood phase
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
            return resp.status == 200
    except urllib.error.HTTPError as e:
        print(f"API error: {e.code} {e.reason}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Connection error: {e}", file=sys.stderr)
        return False


def install_cron():
    """Install cron entries for scheduled reporting."""
    agent_path = os.path.abspath(__file__)
    entries = [
        f"*/5 * * * * {sys.executable} {agent_path} --quick",
        f"*/30 * * * * {sys.executable} {agent_path} --full",
        f"0 8 * * * {sys.executable} {agent_path} --full",
    ]
    try:
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
        existing = result.stdout if result.returncode == 0 else ""
        lines = [l for l in existing.splitlines() if "agentpulse" not in l.lower() and l.strip()]
        lines.extend(entries)
        new_cron = "\n".join(lines) + "\n"
        proc = subprocess.run(["crontab", "-"], input=new_cron, text=True)
        if proc.returncode == 0:
            print("Cron entries installed successfully.")
        else:
            print("Failed to install cron entries.", file=sys.stderr)
    except Exception as e:
        print(f"Cron install error: {e}", file=sys.stderr)


def main():
    load_config()

    if not API_KEY or not SERVER_ID:
        print("Error: AGENTPULSE_API_KEY and AGENTPULSE_SERVER_ID must be set.", file=sys.stderr)
        sys.exit(3)

    parser = argparse.ArgumentParser(description="AgentPulse monitoring agent")
    parser.add_argument("--quick", action="store_true", help="Quick health check")
    parser.add_argument("--full", action="store_true", help="Full report")
    parser.add_argument("--install", action="store_true", help="Install cron entries")
    args = parser.parse_args()

    if args.install:
        install_cron()
        return

    if not args.quick and not args.full:
        args.quick = True  # default to quick

    if args.full:
        data = collect_full()
    else:
        data = collect_quick()

    success = send_report(data)

    # Exit code reflects health: 0=healthy, 1=warning, 2=critical, 3=error
    if not success:
        sys.exit(3)

    # Check for critical conditions
    for svc, active in data.get("services", {}).items():
        if not active and svc in CRITICAL_SERVICES and svc not in IGNORED_INACTIVE:
            print(f"CRITICAL: {svc} is down")
            sys.exit(2)

    if data.get("disk", {}).get("used_pct", 0) > 90:
        print(f"CRITICAL: Disk usage {data['disk']['used_pct']}%")
        sys.exit(2)

    if data.get("memory", {}).get("used_pct", 0) > 90:
        print(f"WARNING: Memory usage {data['memory']['used_pct']}%")
        sys.exit(1)

    print(f"OK — {data['report_type']} report sent")


if __name__ == "__main__":
    main()
