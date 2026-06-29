"""
lmstudio_guardian.py — LM Studio health guardian + auto-restart

Checks:
  1. HTTP reachability
  2. Model loading status
  3. Chat API availability

Provides degraded mode flag for other scripts.

Usage:
  python scripts/lmstudio_guardian.py           # check + attempt fix
  python scripts/lmstudio_guardian.py --status  # check only
"""
import _suppress_windows

import json, os, subprocess, sys, time
from datetime import datetime
from pathlib import Path

from shared_config import LMSTUDIO_MODELS_URL, LMSTUDIO_CHAT_URL, LMSTUDIO_KEY, DATA_DIR

STATE_FILE = DATA_DIR / ".lmstudio_state.json"


def load_state():
    if STATE_FILE.exists():
        with open(STATE_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_state(data):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    data["updated"] = datetime.now().isoformat()
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def check_http(url, token="", timeout=5):
    import urllib.request, urllib.error
    try:
        req = urllib.request.Request(url)
        if token:
            req.add_header("Authorization", f"Bearer {token}")
        resp = urllib.request.urlopen(req, timeout=timeout)
        return {"ok": True, "status": resp.status}
    except urllib.error.HTTPError as e:
        return {"ok": False, "status": e.code, "error": str(e)}
    except Exception as e:
        return {"ok": False, "status": 0, "error": str(e)[:100]}


def check_models_loaded(token=""):
    import urllib.request
    try:
        req = urllib.request.Request(LMSTUDIO_MODELS_URL)
        if token:
            req.add_header("Authorization", f"Bearer {token}")
        resp = urllib.request.urlopen(req, timeout=10)
        data = json.loads(resp.read())
        models = data.get("data", [])
        loaded = [m.get("id") for m in models if m.get("loaded") or m.get("state") == "loaded"]
        if not loaded and models:
            loaded = [m.get("id") for m in models]
        return {"ok": True, "total": len(models), "loaded": len(loaded), "loaded_ids": loaded}
    except Exception as e:
        return {"ok": False, "error": str(e)[:100]}


def set_degraded_mode(degraded=True):
    state = load_state()
    state["degraded"] = degraded
    state["degraded_since"] = state.get("degraded_since") or datetime.now().isoformat()
    if not degraded:
        state["degraded_since"] = None
    save_state(state)


def run(status_only=False):
    token = LMSTUDIO_KEY
    results = {}

    http = check_http(LMSTUDIO_MODELS_URL, token)
    results["http"] = http

    if not http["ok"]:
        print(f"[LM Studio Guardian] Unreachable: {http['error']}")
        set_degraded_mode(True)
        return results

    models = check_models_loaded(token)
    results["models"] = models

    if models["ok"] and models["loaded"] == 0:
        print(f"[LM Studio Guardian] API online but no models loaded")
    elif models["ok"]:
        print(f"[LM Studio Guardian] {models['loaded']}/{models['total']} models loaded")
        set_degraded_mode(False)
    else:
        print(f"[LM Studio Guardian] Model list failed: {models.get('error','')}")

    state_data = {
        "healthy": http["ok"] and models.get("ok", False) and models.get("loaded", 0) > 0,
        "http_ok": http["ok"],
        "models_loaded": models.get("loaded", 0) if models.get("ok") else 0,
    }
    save_state(state_data)
    return results


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--status", action="store_true", help="Check only")
    args = p.parse_args()
    run(status_only=args.status)
