"""start_browser.py — open a real, controllable browser you log into once.

Some sites (X especially) refuse to let an automated browser complete a
login at all: Playwright's own launches get bounced to a login wall even
after a successful sign-in. The way around it is to drive a browser the
HUMAN started, which is what this does.

It launches a real Chrome/Edge with a debugging port and a dedicated
profile directory. Log into the sites you need in that window. Everything
afterwards attaches with --cdp and reuses that session, because the
profile persists.

    python start_browser.py                 # default port 9222
    python start_browser.py --port 9333
    python start_browser.py --url https://x.com/home

Then, in another terminal:

    python harvest.py --sources twitter --cdp http://localhost:9222 ...

Notes
- This is a SEPARATE profile from your everyday browser, on purpose: a
  browser started with a debugging port must not share a profile that
  another running instance holds. Log in once here and it sticks.
- Nothing in this project types or stores your credentials. You log in by
  hand in the window this opens.
- Kill the window (or Ctrl-C here) when finished.
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

CANDIDATES = (
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
)


def find_browser(explicit: str = "") -> str:
    if explicit:
        if not Path(explicit).exists():
            raise SystemExit(f"no such browser: {explicit}")
        return explicit
    for c in CANDIDATES:
        if Path(c).exists():
            return c
    for name in ("google-chrome", "chromium", "chromium-browser", "microsoft-edge"):
        p = shutil.which(name)
        if p:
            return p
    raise SystemExit(
        "could not find Chrome or Edge. Pass --browser /path/to/binary")


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Start a controllable browser.")
    p.add_argument("--port", type=int, default=9222)
    p.add_argument("--browser", default="", help="explicit browser binary")
    p.add_argument("--profile", default="",
                   help="profile dir (default: ~/.cache/AgentEpstein/"
                        "profiles/cdp)")
    p.add_argument("--url", default="https://x.com/home",
                   help="page to open first")
    p.add_argument("--wait", action="store_true",
                   help="stay attached until the browser exits")
    args = p.parse_args(argv)

    binary = find_browser(args.browser)
    profile = Path(args.profile) if args.profile else (
        Path(os.environ.get("HARVEST_PROFILE_ROOT", "")
             or Path.home() / ".cache" / "art-dataset-harvest" / "profiles")
        / "cdp")
    profile.mkdir(parents=True, exist_ok=True)

    cmd = [
        binary,
        f"--remote-debugging-port={args.port}",
        f"--user-data-dir={profile}",
        "--no-first-run",
        "--no-default-browser-check",
        args.url,
    ]
    print(f"browser : {binary}")
    print(f"profile : {profile}")
    print(f"port    : {args.port}")
    print(f"cdp url : http://localhost:{args.port}")
    print()
    print("Log into the sites you need in the window that opens.")
    print("Then, in another terminal, add to your command:")
    print(f"    --cdp http://localhost:{args.port}")
    print()

    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL)
    time.sleep(3)
    if proc.poll() is not None:
        print(f"browser exited immediately (code {proc.returncode})",
              file=sys.stderr)
        return 1

    # Verify the port actually answers before telling the user it worked.
    import urllib.request
    try:
        with urllib.request.urlopen(
                f"http://localhost:{args.port}/json/version", timeout=10) as r:
            import json
            info = json.loads(r.read().decode())
        print(f"debug port alive: {info.get('Browser', 'unknown')}")
    except Exception as e:                                       # noqa: BLE001
        print(f"port {args.port} did not answer: {e}", file=sys.stderr)
        return 1

    if args.wait:
        try:
            proc.wait()
        except KeyboardInterrupt:
            pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
