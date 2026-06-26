#!/usr/bin/env python3
"""
heartbeat.py — Monitor a background Claude task and push the result back to OpenClaw.

Usage:
  heartbeat.py --pid <PID> --log <log_path> --project <name>
               [--session-key <key>] [--gateway-url <url>] [--gateway-token <token>]
               [--config <openclaw.json>]

Notification strategy (in priority order):
  1. OpenClaw /tools/invoke → sessions_send  (injects into the active session; works on any channel)
  2. macOS native notification               (local fallback; always available)
"""

import argparse
import json
import os
import sys
import time
import urllib.request
import urllib.error
import subprocess
from pathlib import Path

# ── Arguments ─────────────────────────────────────────────────────
parser = argparse.ArgumentParser()
parser.add_argument("--pid",           required=True, type=int)
parser.add_argument("--log",           required=True)
parser.add_argument("--project",       required=True)
parser.add_argument("--session-key",   default="main")
parser.add_argument("--gateway-url",   default="")   # Falls back to config if empty
parser.add_argument("--gateway-token", default="")   # Falls back to config if empty
parser.add_argument("--config",
    default=str(Path.home() / ".openclaw" / "openclaw.json"))
args = parser.parse_args()


# ── Helpers ───────────────────────────────────────────────────────
def is_running(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False  # Process does not exist
    except PermissionError:
        return True   # Process exists but we lack permission to signal it — treat as running


def read_log_tail(path: str, lines: int = 80) -> str:
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            all_lines = f.readlines()
        return "".join(all_lines[-lines:]).strip()
    except OSError:
        return "(log unavailable)"


def extract_summary(log_tail: str, max_chars: int = 1800) -> str:
    """Extract the most useful content from the log tail, capped at max_chars."""
    lines = log_tail.splitlines()
    # Prefer content around the ✅ completion marker
    for i, line in enumerate(lines):
        if "✅" in line and ("complete" in line.lower() or "Claude Code" in line):
            snippet = "\n".join(lines[max(0, i - 2):i + 25])
            return snippet[:max_chars]
    # No completion marker found — return the last 35 lines
    tail = "\n".join(lines[-35:])
    return tail[:max_chars]


def load_gateway_config(config_path: str) -> tuple[str, str]:
    """Read the gateway URL and auth token from openclaw.json."""
    try:
        cfg = json.loads(Path(config_path).read_text(encoding="utf-8"))
        port = cfg.get("gateway", {}).get("port", 18789)
        url = f"http://127.0.0.1:{port}"
        token = (
            cfg.get("gateway", {}).get("auth", {}).get("token", "")
            or cfg.get("gateway", {}).get("auth", {}).get("password", "")
        )
        return url, token
    except Exception:
        return "http://127.0.0.1:18789", ""


def sessions_send(gateway_url: str, token: str, session_key: str, message: str) -> bool:
    """
    Call sessions_send via OpenClaw's /tools/invoke endpoint (fire-and-forget).
    Returns True on success.
    """
    payload = json.dumps({
        "tool": "sessions_send",
        "args": {
            "sessionKey": session_key,
            "message": message,
            "timeoutSeconds": 0  # fire-and-forget — do not wait for a reply
        }
    }).encode()

    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    req = urllib.request.Request(
        f"{gateway_url}/tools/invoke",
        data=payload,
        headers=headers,
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            resp = json.loads(r.read())
            if resp.get("ok"):
                print("[heartbeat] ✅ sessions_send succeeded — message injected into session", flush=True)
                return True
            else:
                print(f"[heartbeat] ⚠️  sessions_send returned an error: {resp}", flush=True)
                return False
    except urllib.error.HTTPError as e:
        body = e.read(300).decode(errors="replace")
        print(f"[heartbeat] ⚠️  sessions_send HTTP {e.code}: {body}", flush=True)
        return False
    except Exception as e:
        print(f"[heartbeat] ⚠️  sessions_send failed: {e}", flush=True)
        return False


def macos_notify(title: str, body: str):
    """Send a macOS native notification (fallback — no external dependencies)."""
    try:
        safe_title = title.replace('"', "'")
        safe_body  = body[:200].replace('"', "'").replace("\n", " ")
        script = f'display notification "{safe_body}" with title "{safe_title}" sound name "Glass"'
        subprocess.run(["osascript", "-e", script], check=False, timeout=5)
        print("[heartbeat] 🔔 macOS notification sent", flush=True)
    except Exception as e:
        print(f"[heartbeat] ⚠️  macOS notification failed: {e}", flush=True)


# ── Main loop: watch the PID ──────────────────────────────────────
print(f"[heartbeat] Watching PID={args.pid}, project={args.project}", flush=True)

POLL_INTERVAL = 10  # seconds

while is_running(args.pid):
    time.sleep(POLL_INTERVAL)

print(f"[heartbeat] PID={args.pid} has exited — pushing notification", flush=True)

# Read execution summary from log
log_tail = read_log_tail(args.log)
summary  = extract_summary(log_tail)

# Build the message to inject into the OpenClaw session
inject_message = (
    f"[Background task complete] Claude Code has finished working on **{args.project}**.\n\n"
    f"Summary:\n{summary}\n\n"
    f"(This message was pushed automatically by the heartbeat process.)"
)

# Load gateway config once (avoid reading the file twice)
_gw      = load_gateway_config(args.config)
gw_url   = args.gateway_url   or _gw[0]
gw_token = args.gateway_token or _gw[1]

# Strategy 1: sessions_send via OpenClaw gateway
notified = sessions_send(gw_url, gw_token, args.session_key, inject_message)

# Strategy 2: macOS notification (fallback)
if not notified:
    macos_notify(
        title=f"✅ Claude Code done: {args.project}",
        body=summary[:150]
    )

print("[heartbeat] Done", flush=True)
