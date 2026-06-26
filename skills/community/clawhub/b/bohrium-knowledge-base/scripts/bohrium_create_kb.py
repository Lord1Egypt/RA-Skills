#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Create Bohrium Knowledge Base and return (kb_id, nodesID).

Uses ACCESS_KEY from env or ~/.openclaw/openclaw.json (skills entry).

Output: JSON to stdout.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.request
from pathlib import Path

BASE = "https://open.bohrium.com/openapi/v1/knowledge"


def load_access_key_from_openclaw_config() -> str:
    try:
        cfg_path = Path("~/.openclaw/openclaw.json").expanduser()
        if not cfg_path.exists():
            return ""
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
        return (
            (((cfg.get("skills") or {}).get("entries") or {}).get("bohrium-knowledge-file-upload") or {})
            .get("env")
            or {}
        ).get("ACCESS_KEY", "")
    except Exception:
        return ""


def _http_json(url: str, access_key: str, body: dict) -> dict:
    data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("content-type", "application/json")
    req.add_header("accessKey", access_key)
    with urllib.request.urlopen(req, timeout=60) as resp:
        raw = resp.read().decode("utf-8", "replace")
    return json.loads(raw)


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage: bohrium_create_kb.py <KB_NAME> [KB_DESC]", file=sys.stderr)
        return 2

    name = argv[1]
    desc = argv[2] if len(argv) >= 3 else "SciPulse Daily Digest"

    access_key = (os.environ.get("ACCESS_KEY") or "").strip() or load_access_key_from_openclaw_config().strip()
    if not access_key:
        print("Missing ACCESS_KEY (env or ~/.openclaw/openclaw.json)", file=sys.stderr)
        return 2

    url = f"{BASE}/knowledge_base/create"
    obj = _http_json(url, access_key, {
        "knowledgeBaseName": name,
        "introduction": desc,
        "cover": "",
        "privilege": 1,
    })
    print(json.dumps(obj, ensure_ascii=False, indent=2))

    if obj.get("code") != 0:
        return 1
    data = obj.get("data") or {}
    if not data.get("nodesID"):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
