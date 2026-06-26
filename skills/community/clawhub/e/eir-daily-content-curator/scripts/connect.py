#!/usr/bin/env python3
"""connect.py — Register OpenClaw with Eir using a pairing code.

Usage: python3 connect.py <PAIRING_CODE>

Get a pairing code from Eir → Settings → Connect OpenClaw.
"""
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
CONFIG_DIR = SCRIPT_DIR.parent / "config"
CONFIG_PATH = CONFIG_DIR / "eir.json"
API_BASE = "https://api.heyeir.com/api"


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 connect.py <PAIRING_CODE>", file=sys.stderr)
        print("Get a pairing code from Eir → Settings → Connect OpenClaw", file=sys.stderr)
        sys.exit(1)

    code = sys.argv[1].replace("-", "").upper()

    # Exchange pairing code
    payload = json.dumps({"code": code}).encode()
    req = urllib.request.Request(
        f"{API_BASE}/oc/connect",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = json.loads(e.read()) if e.fp else {}
        print(f"✗ Connection failed: {body.get('error', e.reason)}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"✗ Connection failed: {e}", file=sys.stderr)
        sys.exit(1)

    # Save credentials locally
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    config = {
        "apiUrl": API_BASE,
        "apiKey": data["apiKey"],
        "userId": data["userId"],
        "connectedAt": datetime.now(timezone.utc).isoformat(),
    }
    CONFIG_PATH.write_text(json.dumps(config, indent=2))

    print(f"✓ Connected to Eir")
    print(f"  User ID: {data['userId']}")
    print(f"  API Key saved to {CONFIG_PATH}")


if __name__ == "__main__":
    main()
