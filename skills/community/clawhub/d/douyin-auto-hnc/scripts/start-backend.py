#!/usr/bin/env python3
"""
Start Douyin Automation Backend - Chrome CDP + FastAPI.
Cross-platform. Handles port conflicts gracefully.
"""

import json
import os
import re
import signal
import socket
import subprocess
import sys
import time
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent

# Load config
def load_config():
    cfg = SKILL_DIR / "CONFIG.md"
    if not cfg.exists():
        return None
    text = cfg.read_text(encoding="utf-8")
    m = re.search(r"```json\s*([\s\S]*?)\s*```", text)
    if m:
        try:
            return json.loads(m.group(1))
        except json.JSONDecodeError:
            return None
    return None


def check_port(port):
    """Check if port is in use."""
    s = socket.socket()
    try:
        s.bind(("127.0.0.1", port))
        return False  # free
    except OSError:
        return True   # in use
    finally:
        s.close()


def wait_for_port(port, timeout=10):
    """Wait for port to become available (Chrome) or ready (API)."""
    start = time.time()
    while time.time() - start < timeout:
        s = socket.socket()
        try:
            s.settimeout(1)
            s.connect(("127.0.0.1", port))
            return True
        except (socket.timeout, ConnectionRefusedError, OSError):
            time.sleep(0.5)
        finally:
            s.close()
    return False


def get_chrome_path():
    """Find Chrome executable."""
    home = Path.home()
    if sys.platform == "win32":
        candidates = [
            Path(os.environ.get("ProgramFiles", "")) / "Google/Chrome/Application/chrome.exe",
            Path(os.environ.get("ProgramFiles(x86)", "")) / "Google/Chrome/Application/chrome.exe",
            Path(os.environ.get("LOCALAPPDATA", "")) / "Google/Chrome/Application/chrome.exe",
            Path("C:/Program Files/Google/Chrome/Application/chrome.exe"),
        ]
    elif sys.platform == "darwin":
        candidates = [
            Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
            Path(home / "Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
        ]
    else:
        candidates = [
            Path("/usr/bin/google-chrome"),
            Path("/usr/bin/chromium-browser"),
            Path("/usr/bin/chromium"),
            home / "snap/chromium/current/usr/lib/chromium-browser/chromium-browser",
        ]
    for p in candidates:
        if p.exists():
            return str(p)
    return None


def start_chrome(cdp_port, dry_run=False):
    """Launch Chrome with remote debugging."""
    chrome = get_chrome_path()
    if not chrome:
        return False, "Chrome not found. Install Chrome first."

    user_data_dir = Path.home() / ".openclaw" / "chrome-douyin-profile"
    user_data_dir.mkdir(parents=True, exist_ok=True)

    args = [
        chrome,
        f"--remote-debugging-port={cdp_port}",
        f"--user-data-dir={user_data_dir}",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-popup-blocking",
        "https://creator.douyin.com",
    ]

    if dry_run:
        return True, " ".join(args)

    try:
        subprocess.Popen(
            args,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
        # Wait for Chrome to start
        time.sleep(2)
        if wait_for_port(cdp_port, timeout=10):
            return True, f"Chrome started (CDP port {cdp_port})"
        return False, "Chrome started but CDP not responding"
    except Exception as e:
        return False, f"Failed to start Chrome: {e}"


def start_backend(backend_dir, port):
    """Start FastAPI backend."""
    python = sys.executable
    main_py = Path(backend_dir) / "main.py"
    if not main_py.exists():
        main_py = Path(backend_dir) / "app" / "main.py"

    if not main_py.exists():
        return False, f"main.py not found in {backend_dir}"

    cmd = f'"{python}" "{main_py}"'

    try:
        subprocess.Popen(
            cmd,
            cwd=str(Path(backend_dir).parent),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
        if wait_for_port(port, timeout=15):
            return True, f"Backend started (port {port})"
        return False, "Backend started but port not responding"
    except Exception as e:
        return False, f"Failed to start backend: {e}"


def main():
    print("=" * 50)
    print("  Douyin Automation - Start Services")
    print("=" * 50)

    config = load_config()
    if not config:
        print("ERROR: CONFIG.md not found. Run `python scripts/setup.py` first.")
        sys.exit(1)

    cdp_port = config.get("chrome_cdp_port", 9222)
    backend_port = config.get("agent_port", 8080)
    backend_dir = config.get("agent_backend")

    print(f"  Chrome CDP port:  {cdp_port}")
    print(f"  Backend port:     {backend_port}")
    print(f"  Backend dir:      {backend_dir}")
    print()

    # Chrome
    print(f"[1/2] Chrome CDP (port {cdp_port})...")
    if check_port(cdp_port):
        print(f"      Already running on port {cdp_port}")
    else:
        ok, msg = start_chrome(cdp_port)
        print(f"      {msg}")
        if not ok:
            print(f"      Manual: Start Chrome with --remote-debugging-port={cdp_port}")

    # Backend
    print(f"\n[2/2] Backend API (port {backend_port})...")
    if check_port(backend_port):
        print(f"      Already running on port {backend_port}")
    else:
        ok, msg = start_backend(backend_dir, backend_port)
        print(f"      {msg}")
        if not ok:
            print(f"      Check: cd {backend_dir} && python main.py")

    print()
    print("=" * 50)
    print("  Ready! Run `python scripts/run-pipeline.py` to execute.")
    print("  Press Ctrl+C to stop this script (services keep running).")
    print("=" * 50)


if __name__ == "__main__":
    main()
