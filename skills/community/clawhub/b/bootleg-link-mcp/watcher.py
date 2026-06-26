#!/usr/bin/env python3
"""
Hot-reload wrapper for bootleg-link MCP server.
Watches server.py for changes and auto-restarts the server process.
"""

import os
import sys
import time
import signal
import subprocess

WATCH_FILES = [
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "server.py"),
]
CHECK_INTERVAL = 1.0  # seconds


def get_mtimes():
    """Return dict of path -> mtime for all watched files."""
    result = {}
    for path in WATCH_FILES:
        try:
            result[path] = os.stat(path).st_mtime
        except OSError:
            result[path] = 0
    return result


def main():
    server_cmd = [sys.executable] + [os.path.join(os.path.dirname(os.path.abspath(__file__)), "server.py")]

    last_mtimes = get_mtimes()
    proc = None
    restarting = False

    while True:
        # Start server if not running
        if proc is None:
            print(f"[watcher] Starting MCP server: {' '.join(server_cmd)}", file=sys.stderr, flush=True)
            proc = subprocess.Popen(
                server_cmd,
                stdin=sys.stdin,
                stdout=sys.stdout,
                stderr=subprocess.PIPE,
            )
            last_mtimes = get_mtimes()
            restarting = False

        # Check if process died
        if proc.poll() is not None:
            exit_code = proc.returncode
            # Drain stderr
            try:
                leftover = proc.stderr.read()
                if leftover:
                    sys.stderr.write(leftover.decode(errors="replace"))
                    sys.stderr.flush()
            except Exception:
                pass
            print(f"[watcher] Server exited with code {exit_code}", file=sys.stderr, flush=True)
            if exit_code == 0:
                break  # clean shutdown
            proc = None
            last_mtimes = get_mtimes()
            time.sleep(0.5)
            continue

        # Drain stderr from server (non-blocking)
        try:
            import select
            while True:
                r, _, _ = select.select([proc.stderr], [], [], 0)
                if not r:
                    break
                data = proc.stderr.read(4096)
                if not data:
                    break
                sys.stderr.buffer.write(data)
                sys.stderr.flush()
        except Exception:
            pass

        # Check for file changes
        current = get_mtimes()
        changed = False
        for path in last_mtimes:
            if current.get(path, 0) > last_mtimes[path]:
                changed = True
                break

        if changed and not restarting:
            restarting = True
            print(f"[watcher] File changed, restarting server...", file=sys.stderr, flush=True)
            os.kill(proc.pid, signal.SIGTERM)
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                os.kill(proc.pid, signal.SIGKILL)
                proc.wait()
            proc = None
            continue

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, lambda s, f: sys.exit(0))
    signal.signal(signal.SIGTERM, lambda s, f: sys.exit(0))
    main()
