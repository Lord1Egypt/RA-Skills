#!/usr/bin/env python3
"""Read-only Fing Local API helper for OpenClaw skills.

Environment:
  FING_API_HOST  default localhost
  FING_API_PORT  default 49090
  FING_API_KEY   required unless --api-key is provided
  FING_API_SCHEME default http
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any


def load_env_file(path: str) -> None:
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def die(message: str, code: int = 2) -> None:
    print(json.dumps({"ok": False, "error": message}, indent=2), file=sys.stderr)
    raise SystemExit(code)


def request_json(base_url: str, endpoint: str, api_key: str) -> dict[str, Any]:
    params = urllib.parse.urlencode({"auth": api_key})
    url = f"{base_url}/1/{endpoint}?{params}"
    safe_url = f"{base_url}/1/{endpoint}?auth=***"
    req = urllib.request.Request(url, method="GET", headers={
        "Accept": "application/json",
        "User-Agent": "openclaw-fing-helper/0.1",
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            try:
                body: Any = json.loads(raw) if raw else None
            except Exception:
                body = raw
            return {"ok": True, "status": resp.status, "url": safe_url, "response": body}
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        try:
            body = json.loads(raw)
        except Exception:
            body = raw
        return {"ok": False, "status": e.code, "url": safe_url, "response": body}
    except urllib.error.URLError as e:
        return {"ok": False, "status": None, "url": safe_url, "error": str(e.reason)}


def summarize_devices(result: dict[str, Any], include_devices: bool = True) -> dict[str, Any]:
    if not result.get("ok"):
        return result
    data = result.get("response") or {}
    devices = data.get("devices") or []
    up = [d for d in devices if d.get("state") == "UP"]
    down = [d for d in devices if d.get("state") == "DOWN"]
    by_type: dict[str, int] = {}
    for d in devices:
        typ = d.get("type") or "UNKNOWN"
        by_type[typ] = by_type.get(typ, 0) + 1
    summary = {
        "ok": True,
        "status": result.get("status"),
        "networkId": data.get("networkId"),
        "totalDevices": len(devices),
        "upDevices": len(up),
        "downDevices": len(down),
        "types": dict(sorted(by_type.items(), key=lambda kv: (-kv[1], kv[0]))),
    }
    if include_devices:
        summary["devices"] = [
            {
                "name": d.get("name"),
                "ip": d.get("ip"),
                "mac": d.get("mac"),
                "state": d.get("state"),
                "type": d.get("type"),
                "make": d.get("make"),
                "model": d.get("model"),
                "last_changed": d.get("last_changed"),
            }
            for d in devices
        ]
    return summary


def summarize_people(result: dict[str, Any]) -> dict[str, Any]:
    if not result.get("ok"):
        return result
    data = result.get("response") or {}
    people = data.get("people") or []
    online = [p for p in people if p.get("currentState") == "ONLINE"]
    offline = [p for p in people if p.get("currentState") == "OFFLINE"]
    return {
        "ok": True,
        "status": result.get("status"),
        "networkId": data.get("networkId"),
        "lastChangeTime": data.get("lastChangeTime"),
        "totalPeople": len(people),
        "onlinePeople": len(online),
        "offlinePeople": len(offline),
        "people": [
            {
                "displayName": (p.get("contactInfo") or {}).get("displayName"),
                "contactType": (p.get("contactInfo") or {}).get("contactType"),
                "currentState": p.get("currentState"),
                "stateChangeTime": p.get("stateChangeTime"),
            }
            for p in people
        ],
    }


def main() -> None:
    load_env_file(os.path.join(os.getcwd(), ".env"))
    parser = argparse.ArgumentParser(description="Read-only Fing Local API helper")
    parser.add_argument("--host", default=os.getenv("FING_API_HOST", "localhost"))
    parser.add_argument("--port", default=os.getenv("FING_API_PORT", "49090"))
    parser.add_argument("--scheme", default=os.getenv("FING_API_SCHEME", "http"), choices=["http", "https"])
    parser.add_argument("--api-key", default=os.getenv("FING_API_KEY"), help="Fing API key; defaults to FING_API_KEY")
    parser.add_argument("--raw", action="store_true", help="Print raw API response wrapper")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("devices", help="List all discovered devices")
    sub.add_parser("people", help="List Fing Desktop contacts/presence; may be unsupported on Fing Agent/Fingbox")
    sub.add_parser("summary", help="Compact health/device summary")

    args = parser.parse_args()
    if not args.api_key:
        die("Missing API key. Set FING_API_KEY or pass --api-key.")
    base_url = f"{args.scheme}://{args.host}:{args.port}"

    if args.command == "devices":
        result = request_json(base_url, "devices", args.api_key)
        output = result if args.raw else summarize_devices(result)
    elif args.command == "people":
        result = request_json(base_url, "people", args.api_key)
        output = result if args.raw else summarize_people(result)
    else:
        devices = summarize_devices(request_json(base_url, "devices", args.api_key), include_devices=False)
        people_raw = request_json(base_url, "people", args.api_key)
        people = summarize_people(people_raw) if people_raw.get("ok") else {
            "ok": False,
            "status": people_raw.get("status"),
            "error": people_raw.get("error") or people_raw.get("response"),
        }
        output = {"ok": bool(devices.get("ok")), "baseUrl": base_url, "devices": devices, "people": people}

    print(json.dumps(output, indent=2, ensure_ascii=False))
    raise SystemExit(0 if output.get("ok") else 1)


if __name__ == "__main__":
    main()
