#!/usr/bin/env python3
"""
Cron Job Manager
Lists and manages OpenClaw cron jobs.
"""
import subprocess
import sys

def list_jobs():
    try:
        result = subprocess.run(["openclaw", "cron", "list"], capture_output=True, text=True, timeout=10)
        return result.stdout
    except Exception as e:
        return f"Error listing jobs: {str(e)}"

if __name__ == "__main__":
    print("📅 **Current Cron Jobs:**")
    print(list_jobs())
