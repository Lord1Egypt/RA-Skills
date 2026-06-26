#!/usr/bin/env python3
"""
Codex Reset Radar — change detector.

Compares the current radar snapshot against a local cache and emits a concise
JSON diff when key fields change.  Uses only stdlib.

Cache file: ~/.openclaw/workspace/cache/codex-radar-last.json
"""

from __future__ import annotations

import json
import os
import sys
import urllib.request
from datetime import datetime, timezone, timedelta

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
CURRENT_URL = "https://codex-reset-radar.pages.dev/current.json"
WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
CACHE_DIR = os.path.join(WORKSPACE, "cache")
CACHE_PATH = os.path.join(CACHE_DIR, "codex-radar-last.json")
TZ = timezone(timedelta(hours=8))   # Asia/Shanghai
REQUEST_TIMEOUT = 15
PROB_THRESHOLD = 0.1


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def now_ts() -> str:
    return datetime.now(TZ).isoformat(timespec="seconds")


def safe_get(d, *keys):
    """Return d[keys[0]][keys[1]]... or None."""
    for k in keys:
        if isinstance(d, dict):
            d = d.get(k)
        else:
            return None
    return d


def fetch_json(url: str) -> dict:
    """GET *url*, parse JSON, return dict.  Raises on failure."""
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "codex-radar-check/1.0", "Accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
        raw = resp.read()
    return json.loads(raw)


def load_cache() -> dict | None:
    """Return cached state dict or None (file missing / invalid)."""
    if not os.path.isfile(CACHE_PATH):
        return None
    try:
        with open(CACHE_PATH, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except (json.JSONDecodeError, OSError):
        return None


def save_cache(state: dict) -> None:
    state["last_checked"] = now_ts()
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(CACHE_PATH, "w", encoding="utf-8") as fh:
        json.dump(state, fh, ensure_ascii=False, indent=2)


def build_current_status(data: dict) -> dict:
    """Extract the canonical flat snapshot from the remote payload."""
    return {
        "window_open": bool(data.get("window_open")),
        "status": data.get("status") or "none",
        "current_window_state": safe_get(data, "current_window", "state") or "none",
        "last_window_id": safe_get(data, "last_window", "id") or "",
        "prediction_level": safe_get(data, "prediction", "level") or "low",
        "prediction_probability_24h": float(
            safe_get(data, "prediction", "probability_24h") or 0.0
        ),
    }


# ---------------------------------------------------------------------------
# Diff logic
# ---------------------------------------------------------------------------
def compare(prev: dict, curr: dict, raw_data: dict) -> list[dict] | None:
    """
    Return a list of event dicts, or None if nothing changed.

    Events generated:
      - window_opened  /  window_closed    (window_open bool flip)
      - status_change                      (top-level status string)
      - current_window_state_change        (current_window.state)
      - new_window                         (last_window.id changed)
      - prediction_change                  (prediction.level change)
      - prediction_probability_change      (>= PROB_THRESHOLD delta)

    Each event dict has {type, detail, ...extra}.
    """
    events: list[dict] = []

    # --- window_open boolean ---
    was = bool(prev.get("window_open"))
    now = bool(curr.get("window_open"))
    if was != now:
        last_win = raw_data.get("last_window") or {}
        opened_at = last_win.get("opened_at") or raw_data.get("checked_at")
        scope = last_win.get("scope") or "Codex 用户"
        if now:
            events.append(
                {
                    "type": "window_opened",
                    "detail": "Codex 用量重置窗口已开启",
                    "opened_at": opened_at,
                    "scope": scope,
                }
            )
        else:
            events.append(
                {"type": "window_closed", "detail": "Codex 用量重置窗口已关闭"}
            )

    # --- status string ---
    old_status = str(prev.get("status") or "")
    new_status = str(curr.get("status") or "")
    if old_status != new_status:
        events.append(
            {
                "type": "status_change",
                "detail": f"状态从 {old_status} 变为 {new_status}",
                "from": old_status,
                "to": new_status,
            }
        )

    # --- current_window.state ---
    old_cws = str(prev.get("current_window_state") or "")
    new_cws = str(curr.get("current_window_state") or "")
    if old_cws != new_cws:
        events.append(
            {
                "type": "current_window_state_change",
                "detail": f"当前窗口状态从 {old_cws} 变为 {new_cws}",
                "from": old_cws,
                "to": new_cws,
            }
        )

    # --- last_window.id (new window) ---
    old_lw = str(prev.get("last_window_id") or "")
    new_lw = str(curr.get("last_window_id") or "")
    if old_lw != new_lw:
        events.append(
            {
                "type": "new_window",
                "detail": f"新速蹬窗口: {new_lw}",
                "window_id": new_lw,
                "previous_window_id": old_lw,
            }
        )

    # --- prediction.level ---
    old_plevel = str(prev.get("prediction_level") or "")
    new_plevel = str(curr.get("prediction_level") or "")
    if old_plevel != new_plevel:
        events.append(
            {
                "type": "prediction_change",
                "detail": f"预测等级从 {old_plevel} 升至 {new_plevel}",
                "from": old_plevel,
                "to": new_plevel,
            }
        )

    # --- prediction.probability_24h ---
    old_pprob = float(prev.get("prediction_probability_24h") or 0.0)
    new_pprob = float(curr.get("prediction_probability_24h") or 0.0)
    if abs(new_pprob - old_pprob) >= PROB_THRESHOLD:
        events.append(
            {
                "type": "prediction_probability_change",
                "detail": (
                    f"24h 预测概率从 {old_pprob} "
                    f"{'升至' if new_pprob > old_pprob else '降至'} {new_pprob}"
                ),
                "from": old_pprob,
                "to": new_pprob,
                "probability_24h": new_pprob,
            }
        )

    return events if events else None


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    # 1. Fetch
    try:
        data = fetch_json(CURRENT_URL)
    except Exception as exc:
        print(json.dumps({"has_changes": False, "error": f"网络请求失败: {exc}"}, ensure_ascii=False))
        sys.exit(0)

    curr = build_current_status(data)

    # 2. Load previous
    prev = load_cache()

    # First run – baseline only
    if prev is None:
        save_cache(curr)
        print(
            json.dumps(
                {
                    "has_changes": False,
                    "message": "baseline_created",
                    "current_status": curr,
                },
                ensure_ascii=False,
            )
        )
        return

    # 3. Diff
    events = compare(prev, curr, data)

    # 4. Update cache
    save_cache(curr)

    # 5. Output
    if events is None:
        print(json.dumps({"has_changes": False}, ensure_ascii=False))
    else:
        output = {
            "has_changes": True,
            "events": events,
            "current_status": {
                "window_open": curr["window_open"],
                "status": curr["status"],
                "last_window_id": curr["last_window_id"],
                "prediction_level": curr["prediction_level"],
                "probability_24h": curr["prediction_probability_24h"],
            },
        }
        print(json.dumps(output, ensure_ascii=False))


if __name__ == "__main__":
    main()
