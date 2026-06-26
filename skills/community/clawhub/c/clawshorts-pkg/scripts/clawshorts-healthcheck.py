#!/usr/bin/env python3
"""ClawShorts Health Check - Auto-restarts daemon if hung.

This script monitors the main daemon and restarts it if it becomes unresponsive.
Runs as a sidecar to ensure the blocker is always active.

Usage:
    python3 clawshorts-healthcheck.py 192.168.1.239 &
    # Or run via cron: */5 * * * * python3 /path/to/clawshorts-healthcheck.py 192.168.1.239
"""
from __future__ import annotations

import logging
import signal
import subprocess
import sys
import time
from pathlib import Path

__all__ = []

log = logging.getLogger(__name__)

DAEMON_SCRIPT = Path(__file__).parent / "clawshorts-daemon.py"
STATE_DIR = Path.home() / ".clawshorts"
LOG_FILE = STATE_DIR / "healthcheck.log"

# How old the log file must be (seconds) to consider daemon dead
LOG_MAX_AGE_SECONDS = 120


def _log(msg: str) -> None:
    """Append a timestamped message to the healthcheck log (mode='a')."""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}\n"
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    LOG_FILE.write_text(LOG_FILE.read_text(errors="replace") + line)
    print(line.strip(), file=sys.stdout)


def is_daemon_healthy() -> bool:
    """Check if exactly ONE daemon is running and responsive."""
    # Check process count
    try:
        result = subprocess.run(
            ["pgrep", "-f", "clawshorts-daemon.py"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        pids = [p for p in result.stdout.strip().split("\n") if p]
        pid_count = len(pids)

        if pid_count == 0:
            _log("Daemon not running")
            return False
        if pid_count > 1:
            _log(f"Multiple daemons running ({pid_count}), need cleanup")
            return False
    except subprocess.TimeoutExpired:
        _log("Process check timed out")
        return False
    except OSError as e:
        _log(f"Process check failed: {e}")
        return False

    # Check heartbeat in daemon log
    try:
        daemon_log = STATE_DIR / "daemon.log"
        if daemon_log.exists():
            # Verify log is recent
            mtime = daemon_log.stat().st_mtime
            age = time.time() - mtime
            content = daemon_log.read_text(errors="replace")
            if "HEARTBEAT" not in content:
                _log("No heartbeat found in log")
                return False
            if age > LOG_MAX_AGE_SECONDS:
                _log(f"Daemon log stale ({age:.0f}s old)")
                return False
        else:
            _log("Daemon log not found")
            return False
    except OSError as e:
        _log(f"Log check failed: {e}")
        return False

    _log("Daemon healthy")
    return True


def kill_daemon() -> None:
    """Kill all clawshorts daemon processes and stop launchctl."""
    try:
        subprocess.run(["launchctl", "stop", "com.fink.clawshorts"], timeout=5)
        time.sleep(1)
        subprocess.run(["pkill", "-9", "-f", "clawshorts-daemon.py"], timeout=10)
        time.sleep(1)
    except subprocess.TimeoutExpired:
        _log("Kill command timed out")
    except OSError as e:
        _log(f"Error killing daemon: {e}")


def start_daemon(ip: str) -> None:
    """Start the daemon for the given IP."""
    try:
        daemon_out = STATE_DIR / "daemon.log"
        subprocess.Popen(
            [sys.executable, str(DAEMON_SCRIPT), ip],
            stdout=open(daemon_out, "a"),
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
        _log(f"Started daemon for {ip}")
    except OSError as e:
        _log(f"Error starting daemon: {e}")


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python3 clawshorts-healthcheck.py <ip>")
        sys.exit(1)

    ip = sys.argv[1]
    _log(f"Health check for {ip}")

    if is_daemon_healthy():
        _log("Daemon is healthy, skipping restart")
        sys.exit(0)

    _log("Daemon unhealthy, restarting...")
    kill_daemon()
    time.sleep(2)

    # Verify no daemons running after kill
    result = subprocess.run(
        ["pgrep", "-f", "clawshorts-daemon.py"],
        capture_output=True,
        text=True,
    )
    if result.stdout.strip():
        _log("Warning: Daemons still running after kill")

    start_daemon(ip)
    time.sleep(1)

    # Verify exactly one started
    result = subprocess.run(
        ["pgrep", "-f", "clawshorts-daemon.py"],
        capture_output=True,
        text=True,
    )
    pids = [p for p in result.stdout.strip().split("\n") if p]
    _log(f"Daemon restarted ({len(pids)} running)")


if __name__ == "__main__":
    main()
