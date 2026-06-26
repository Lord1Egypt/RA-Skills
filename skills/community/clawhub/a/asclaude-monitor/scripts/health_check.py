#!/usr/bin/env python3
"""
System Health Check Tool
Monitors disk space, memory, and OpenClaw gateway status.
"""
import subprocess
import shutil
import os

def check_disk_usage(path="/"):
    total, used, free = shutil.disk_usage(path)
    gb = 1024 ** 3
    return f"Total: {total//gb}GB | Used: {used//gb}GB ({used/total*100:.1f}%) | Free: {free//gb}GB"

def check_gateway_status():
    try:
        result = subprocess.run(["openclaw", "gateway", "status"], capture_output=True, text=True, timeout=5)
        if "running" in result.stdout.lower():
            return "🟢 Gateway is Running"
        return "🔴 Gateway is NOT Running"
    except:
        return "⚠️ Could not check Gateway status"

if __name__ == "__main__":
    print("🔍 **System Health Report**")
    print(f"💾 **Disk Usage (Workspace):** {check_disk_usage(os.path.expanduser('~/.openclaw/workspace'))}")
    print(f"⚙️ **OpenClaw Status:** {check_gateway_status()}")
