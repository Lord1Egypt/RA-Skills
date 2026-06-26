#!/usr/bin/env python3
from __future__ import annotations

import base64
import json
import shutil
import socket
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

USAGE_URL = "https://chatgpt.com/backend-api/wham/usage"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def decode_email(profile: dict[str, Any]) -> str | None:
    access = profile.get("access") or profile.get("token")
    if not isinstance(access, str) or access.count(".") < 2:
        return None
    try:
        payload = access.split(".")[1]
        payload += "=" * (-len(payload) % 4)
        decoded = json.loads(base64.urlsafe_b64decode(payload.encode()).decode())
        return ((decoded.get("https://api.openai.com/profile") or {}).get("email"))
    except Exception:
        return None


def collect_profiles(auth: dict[str, Any]) -> list[dict[str, Any]]:
    profiles = []
    for profile_id, profile in (auth.get("profiles") or {}).items():
        if not str(profile_id).startswith("openai-codex:") or not isinstance(profile, dict):
            continue
        profiles.append(
            {
                "profileId": profile_id,
                "accountId": profile.get("accountId"),
                "email": profile.get("email") or decode_email(profile),
                "access": profile.get("access") or profile.get("token"),
                "expires": profile.get("expires"),
                "lastGood": profile.get("lastGood"),
            }
        )
    profiles.sort(key=lambda item: item["profileId"])
    return profiles


def fetch_usage(profile: dict[str, Any], timeout_seconds: int) -> dict[str, Any]:
    token = profile.get("access")
    if not token:
        return {"error": "missing_token"}
    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": "OpenClaw/1.0",
        "Accept": "application/json",
    }
    if profile.get("accountId"):
        headers["ChatGPT-Account-Id"] = profile["accountId"]
    req = urllib.request.Request(USAGE_URL, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout_seconds) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        return {"error": f"http_{exc.code}"}
    except socket.timeout:
        return {"error": "timeout"}
    except Exception as exc:
        return {"error": exc.__class__.__name__}


def remaining_percent(window: dict[str, Any] | None) -> float | None:
    if not isinstance(window, dict) or window.get("used_percent") is None:
        return None
    return max(0.0, 100.0 - float(window.get("used_percent") or 0))


def effective_remaining(usage: dict[str, Any]) -> float | None:
    if usage.get("error"):
        return None
    rate_limit = usage.get("rate_limit") or {}
    candidates: list[float] = []
    for key in ("primary_window", "secondary_window"):
        value = remaining_percent(rate_limit.get(key))
        if value is not None:
            candidates.append(value)
    review_limit = usage.get("code_review_rate_limit") or {}
    for key in ("primary_window", "secondary_window"):
        value = remaining_percent(review_limit.get(key))
        if value is not None:
            candidates.append(value)
    if not candidates:
        return None
    return min(candidates)


def build_usage_rows(profiles: list[dict[str, Any]], timeout_seconds: int) -> list[dict[str, Any]]:
    rows = []
    for profile in profiles:
        usage = fetch_usage(profile, timeout_seconds)
        rows.append(
            {
                "profileId": profile["profileId"],
                "email": profile.get("email"),
                "accountId": profile.get("accountId"),
                "usage": usage,
                "effectiveRemaining": effective_remaining(usage),
            }
        )
    return rows


def choose_best_candidate(
    rows: list[dict[str, Any]],
    current_profile_id: str | None,
    threshold: float,
    excluded_profile_ids: set[str] | None = None,
) -> dict[str, Any] | None:
    excluded_profile_ids = excluded_profile_ids or set()
    eligible = [
        row
        for row in rows
        if row["profileId"] != current_profile_id
        and row["profileId"] not in excluded_profile_ids
        and row.get("effectiveRemaining") is not None
        and row["effectiveRemaining"] > threshold
    ]
    if not eligible:
        return None
    eligible.sort(key=lambda item: (item["effectiveRemaining"], item["profileId"]), reverse=True)
    return eligible[0]


def append_event(path: Path, event: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False) + "\n")


def backup_file(path: Path) -> Path:
    backup_path = path.with_suffix(path.suffix + f".bak-{int(time.time())}")
    shutil.copy2(path, backup_path)
    return backup_path
