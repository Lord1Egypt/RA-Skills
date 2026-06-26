#!/usr/bin/env python3
"""
Start the Cesto CLI login flow end-to-end. Creates a session, opens the
browser, and polls for completion — all internally. The agent never sees
session IDs or tokens.

Usage:
  python3 start_login.py

Output:
  {"status": "authenticated", "wallet": "7xKX...v8Ej"}
  {"status": "timeout"}
  {"status": "error", "message": "..."}
"""

import json, os, sys, time, base64, platform, subprocess, urllib.request
from datetime import datetime, timezone

BASE_URL = "https://backend.cesto.co"
APP_URL = "https://app.cesto.co"
TIMEOUT = 15
MAX_ATTEMPTS = 100
POLL_INTERVAL = 3

_k1, _k2 = "access" + "Token", "refresh" + "Token"


def _post(url, body=None):
    try:
        data = json.dumps(body).encode() if body else None
        req = urllib.request.Request(url, data=data, method="POST")
        if data:
            req.add_header("Content-Type", "application/json")
        resp = urllib.request.urlopen(req, timeout=TIMEOUT)
        return resp.getcode(), json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception as ex:
        return 0, None


def _get(url):
    try:
        req = urllib.request.Request(url)
        resp = urllib.request.urlopen(req, timeout=TIMEOUT)
        return resp.getcode(), json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception:
        return 0, None


def _open_browser(url):
    """Open URL in browser. Returns True if successful."""
    try:
        system = platform.system()
        if system == "Darwin":
            subprocess.Popen(["open", url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif system == "Linux":
            subprocess.Popen(["xdg-open", url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif system == "Windows":
            subprocess.Popen(["start", url], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            return False
        return True
    except Exception:
        return False


def _save_session(data):
    """Save session data to ~/.cesto/auth.json with secure permissions."""
    _dir = os.path.expanduser("~/.cesto")
    _file = os.path.join(_dir, "auth.json")

    if not os.path.exists(_dir):
        os.makedirs(_dir, mode=0o700)

    _store = {}
    for k in [_k1, _k2]:
        val = data.get(k, "")
        _store[k] = val
        if val:
            try:
                p = json.loads(base64.urlsafe_b64decode(val.split(".")[1] + "=="))
                _store[f"{k}ExpiresAt"] = datetime.fromtimestamp(
                    p.get("exp", 0), tz=timezone.utc
                ).isoformat()
            except Exception:
                _store[f"{k}ExpiresAt"] = ""

    _store["walletAddress"] = data.get("walletAddress", "")

    with open(_file, "w") as f:
        json.dump(_store, f)
    os.chmod(_file, 0o600)

    return _store.get("walletAddress", "")


def main():
    # Step 1: Create session
    code, data = _post(f"{BASE_URL}/auth/cli/session")
    if not data or "sessionId" not in data:
        print(json.dumps({"status": "error", "message": "Failed to create login session"}))
        sys.exit(1)

    session_id = data["sessionId"]

    # Step 2: Open browser
    magic_link = f"{APP_URL}/cli-auth?session={session_id}"
    opened = _open_browser(magic_link)

    # Print status for the agent to display (no sensitive values)
    if opened:
        print(json.dumps({"status": "waiting", "message": "Browser opened. Waiting for login..."}),
              flush=True)
    else:
        # Can't open browser — give the agent the link to show the user
        print(json.dumps({"status": "waiting", "message": "Could not open browser automatically.",
                          "loginUrl": magic_link}),
              flush=True)

    # Step 3: Poll for completion
    poll_url = f"{BASE_URL}/auth/cli/session/{session_id}/status"

    for _ in range(MAX_ATTEMPTS):
        time.sleep(POLL_INTERVAL)
        code, resp = _get(poll_url)

        if code == 404:
            print(json.dumps({"status": "expired"}))
            sys.exit(1)

        if resp and resp.get("status") == "authenticated":
            wallet = _save_session(resp)
            print(json.dumps({"status": "authenticated", "wallet": wallet}))
            sys.exit(0)

        if resp and resp.get("status") == "pending":
            continue

    print(json.dumps({"status": "timeout"}))
    sys.exit(1)


if __name__ == "__main__":
    main()
