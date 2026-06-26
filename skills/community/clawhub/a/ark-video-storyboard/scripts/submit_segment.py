#!/usr/bin/env python3
"""Submit one segment payload to the Ark video generation API."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

API_URL = "https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks"


def load_api_key() -> str | None:
    api_key = os.environ.get("ARK_API_KEY")
    if api_key:
        return api_key

    config_path = Path.home() / ".openclaw" / "openclaw.json"
    if config_path.exists():
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
            skills_section = config.get("skills", {})
            if "entries" in skills_section:
                skills_config = skills_section.get("entries", {}).get("ark-video-storyboard", {})
            else:
                skills_config = skills_section.get("ark-video-storyboard", {})
            return skills_config.get("apiKey") or skills_config.get("env", {}).get("ARK_API_KEY")
        except Exception:
            return None
    return None


def submit(payload: dict, api_key: str | None = None) -> dict:
    headers = ["-H", "Content-Type: application/json"]
    if api_key:
        headers += ["-H", f"Authorization: Bearer {api_key}"]
    cmd = [
        "curl", "-sS", API_URL,
        *headers,
        "-d", json.dumps(payload, ensure_ascii=False),
    ]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if p.returncode != 0:
            return {"ok": False, "error": p.stderr.strip() or "curl failed"}
        return json.loads(p.stdout)
    except Exception as e:
        return {"ok": False, "error": str(e)}


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: submit_segment.py <payload.json>", file=sys.stderr)
        sys.exit(1)
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        payload = json.load(f)
    api_key = load_api_key()
    print(json.dumps(submit(payload, api_key), ensure_ascii=False, indent=2))
