#!/usr/bin/env python3
"""
Verify EvoMap heartbeat status.
Checks: (1) LaunchAgent process, (2) heartbeat log, (3) Hub API response.
"""
import urllib.request
import json
import os
import subprocess
import sys
from datetime import datetime, timedelta

HUB_URL = "https://evomap.ai"
HEARTBEAT_ENDPOINT = f"{HUB_URL}/a2a/heartbeat"
HEARTBEAT_LOG = os.path.expanduser("~/.openclaw/cron/heartbeat.log")


def check_launchctl():
    """Check if LaunchAgent is loaded."""
    try:
        result = subprocess.run(
            ["launchctl", "list"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        for line in result.stdout.split("\n"):
            if "evomap" in line.lower():
                print(f"[OK] LaunchAgent: {line.strip()}")
                return True
        print("[WARN] LaunchAgent 'evomap' not found in launchctl list")
        return False
    except Exception as e:
        print(f"[ERROR] launchctl check failed: {e}")
        return False


def check_heartbeat_log(max_age_minutes=10):
    """Check heartbeat log for recent activity."""
    if not os.path.exists(HEARTBEAT_LOG):
        print(f"[WARN] Heartbeat log not found: {HEARTBEAT_LOG}")
        return False

    try:
        with open(HEARTBEAT_LOG) as f:
            lines = f.readlines()

        if not lines:
            print("[WARN] Heartbeat log is empty")
            return False

        last_line = lines[-1].strip()
        print(f"[OK] Last heartbeat log entry: {last_line}")

        # Check if recent (within max_age_minutes)
        # Log format: "--- Thu Apr 17 01:30:00 ---"
        for line in reversed(lines):
            if "---" in line and "GMT" in line:
                try:
                    ts_str = line.strip("-\n ").split(" ", 1)[1]
                    dt = datetime.strptime(ts_str, "%a %b %d %H:%M:%S %Y")
                    age = (datetime.now() - dt).total_seconds() / 60
                    if age < max_age_minutes:
                        print(f"[OK] Last heartbeat: {age:.1f} minutes ago")
                        return True
                    else:
                        print(f"[WARN] Last heartbeat: {age:.1f} minutes ago (>{max_age_minutes}m)")
                        return False
                except Exception:
                    pass
                break
        return True
    except Exception as e:
        print(f"[ERROR] Log check failed: {e}")
        return False


def check_hub_api():
    """Check Hub API for node status."""
    node_id = os.environ.get("EVOMAP_NODE_ID")
    node_secret = os.environ.get("EVOMAP_NODE_SECRET")

    if not node_id or not node_secret:
        print("[ERROR] EVOMAP_NODE_ID or EVOMAP_NODE_SECRET not set")
        return None

    try:
        import urllib.request

        body = json.dumps({"node_id": node_id}).encode("utf-8")
        request = urllib.request.Request(
            HEARTBEAT_ENDPOINT,
            data=body,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {node_secret}",
            },
            method="POST",
        )

        with urllib.request.urlopen(request, timeout=15) as resp:
            result = json.loads(resp.read().decode("utf-8"))

        status = result.get("status")
        credits = result.get("credit_balance", "N/A")
        node_status = result.get("node_status", "N/A")
        print(f"[OK] Hub API: status={status}, credits={credits}, node_status={node_status}")
        return status == "ok"
    except urllib.error.HTTPError as e:
        print(f"[ERROR] Hub API HTTP {e.code}: {e.read().decode()}")
        return None
    except Exception as e:
        print(f"[ERROR] Hub API check failed: {e}")
        return None


def main():
    print("=== EvoMap Heartbeat Check ===\n")

    results = []
    results.append(("LaunchAgent", check_launchctl()))
    results.append(("Heartbeat Log", check_heartbeat_log()))
    results.append(("Hub API", check_hub_api()))

    print("\n=== Summary ===")
    for name, ok in results:
        status = "PASS" if ok else ("FAIL" if ok is False else "SKIP")
        print(f"  {name}: {status}")

    all_pass = all(r[1] is True for r in results)
    sys.exit(0 if all_pass else 1)


if __name__ == "__main__":
    main()
