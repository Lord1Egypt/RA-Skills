#!/usr/bin/env python3
"""Check if the user's daily Brave Browser has remote debugging enabled on port 9222.

Usage:
    python3 check_brave.py

This script ONLY checks status. It never starts, restarts, or kills the browser.
If Brave is not running with CDP, it prints instructions for the user to manually start it.
"""

import json
import sys
import urllib.request

CDP_PORT = 9222


def check():
    url = f"http://localhost:{CDP_PORT}/json/version"
    try:
        with urllib.request.urlopen(url, timeout=3) as resp:
            info = json.loads(resp.read().decode("utf-8"))
            browser = info.get("Browser", "?")
            ws_url = info.get("webSocketDebuggerUrl", "?")
            print(f"✅ Brave CDP available on port {CDP_PORT}")
            print(f"   Browser: {browser}")
            print(f"   WebSocket: {ws_url}")

            # Also list tabs
            try:
                with urllib.request.urlopen(f"http://localhost:{CDP_PORT}/json/list", timeout=3) as tabs_resp:
                    tabs = json.loads(tabs_resp.read().decode("utf-8"))
                    print(f"   Open tabs: {len(tabs)}")
                    for t in tabs[:5]:
                        print(f"     - {t.get('title', '?')[:60]}  ({t.get('url', '')[:60]})")
                    if len(tabs) > 5:
                        print(f"     ... and {len(tabs) - 5} more")
            except Exception:
                pass

            return True
    except Exception:
        print(f"❌ Brave CDP not available on port {CDP_PORT}")
        print()
        print("Please restart Brave with remote debugging enabled:")
        print()
        print("  1. Close ALL Brave windows (Cmd+Q)")
        print("  2. Open Terminal and run:")
        print(f'     /Applications/Brave\\ Browser.app/Contents/MacOS/Brave\\ Browser --remote-debugging-port={CDP_PORT}')
        print()
        print("Or add --remote-debugging-port=9222 to your Brave launch shortcut.")
        return False


if __name__ == "__main__":
    ok = check()
    sys.exit(0 if ok else 1)
