#!/usr/bin/env python3
import os
import sys
import subprocess
import time
from pathlib import Path

def main():
    args = sys.argv[1:]
    if not args:
        print("Usage: run_adb.py <adb command...>")
        sys.exit(1)
    
    # Read the ADB server address from the environment instead of parsing the JSON manually
    adb_server = os.environ.get('ADB_SERVER_ADDRESS')
    base_cmd = ["adb"]
    
    if adb_server:
        # If it looks like an IP address/port, attempt to connect first
        if ":" in adb_server:
            subprocess.run(["adb", "connect", adb_server], capture_output=True)
        base_cmd.extend(["-s", adb_server])
        
    cmd = base_cmd + args
    print(f"Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
    except subprocess.CalledProcessError as e:
        print(f"ADB command failed with code {e.returncode}", file=sys.stderr)
        print(e.stderr, file=sys.stderr)
        
    # Take screenshot
    workspace = Path.home() / '.openclaw' / 'workspace'
    workspace.mkdir(parents=True, exist_ok=True)
    timestamp = int(time.time())
    screenshot_path = workspace / f"adb-screenshot-{timestamp}.png"
    
    screencap_cmd = base_cmd + ["exec-out", "screencap", "-p"]
    try:
        with open(screenshot_path, "wb") as f:
            subprocess.run(screencap_cmd, stdout=f, check=True)
        print(f"Screenshot saved to: {screenshot_path}")
    except Exception as e:
        print(f"Failed to take screenshot: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
