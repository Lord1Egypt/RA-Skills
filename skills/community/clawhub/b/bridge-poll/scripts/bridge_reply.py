#!/usr/bin/env python3
"""Send a reply to the bridge outbox. Handles JSON encoding properly.

Why not curl? Messages with newlines, quotes, or special characters break
curl's -d flag. This script JSON-encodes safely every time.

Usage:
  python3 bridge_reply.py "your reply here"
  echo "multi-line reply" | python3 bridge_reply.py

Env vars (override defaults):
  BRIDGE_URL   — bridge reply endpoint (default http://localhost:18790/api/reply)
  BRIDGE_TOKEN — auth token
"""
import json, os, sys

BRIDGE_URL = os.environ.get("BRIDGE_URL", "http://localhost:18790/api/reply")
BRIDGE_TOKEN = os.environ.get("BRIDGE_TOKEN", "YOUR_TOKEN_HERE")
BRIDGE_FROM = os.environ.get("BRIDGE_FROM", "agent")


def send_reply(text: str) -> dict:
    # Use urllib to avoid requiring 'requests' package
    import urllib.request
    payload = json.dumps({"message": text, "from": BRIDGE_FROM}).encode()
    req = urllib.request.Request(
        BRIDGE_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {BRIDGE_TOKEN}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read())


if __name__ == "__main__":
    text = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else sys.stdin.read().strip()
    if not text:
        print("Error: no text provided", file=sys.stderr)
        sys.exit(1)
    print(json.dumps(send_reply(text)))
