"""Shared utilities for Demo-Slap scripts."""
import os
import sys
import json
import time
import requests
from datetime import datetime, timezone

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
STEAM_IDS_FILE = os.path.join(DATA_DIR, "steam_ids.json")
CONFIG_FILE = os.path.join(DATA_DIR, "config.json")
STATE_FILE = os.path.join(DATA_DIR, "state.json")
LOG_FILE = os.path.join(DATA_DIR, "history.log")
HIGHLIGHTS_FILE = os.path.join(DATA_DIR, "highlights.json")

DEMOSLAP_API_BASE = "https://api.demo-slap.net"
LEETIFY_API_BASE = "https://api-public.cs-prod.leetify.com"


# --- Config ---

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {}
    with open(CONFIG_FILE, "r") as f:
        try:
            return json.load(f)
        except Exception:
            return {}


def get_demo_slap_key():
    key = os.environ.get("DEMOSLAP_API_KEY") or load_config().get("demoslap_api_key")
    if not key:
        print("❌ DEMOSLAP_API_KEY is missing.")
        sys.exit(1)
    return key


def get_leetify_key():
    return os.environ.get("LEETIFY_API_KEY") or load_config().get("leetify_api_key")


# --- Steam IDs ---

def load_steam_ids():
    if not os.path.exists(STEAM_IDS_FILE):
        return {}
    with open(STEAM_IDS_FILE, "r") as f:
        try:
            return json.load(f)
        except Exception:
            return {}


def get_steam_id(username):
    return load_steam_ids().get(username)


# --- State ---

def read_state():
    if not os.path.exists(STATE_FILE):
        return {"status": "idle"}
    with open(STATE_FILE, "r") as f:
        try:
            return json.load(f)
        except Exception:
            return {"status": "idle"}


def write_state(status, **kwargs):
    prev = read_state()
    state = {
        "status": status,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }

    preserved_keys = [
        "chat_id",
        "watchdog_job_id",
        "job_id",
        "render_job_id",
        "render_mode",
        "replay_url",
        "highlights_count",
        "clip_urls",
        "estimated_finish",
        "notification",
        "last_completed_op",
        "last_error_op",
    ]
    for key in preserved_keys:
        if key in prev:
            state[key] = prev[key]

    if status in ("analyzing", "rendering"):
        state["notification"] = {
            "sent": False,
            "sent_at": None,
            "last_attempt_at": None,
            "error": None,
        }

    state.update(kwargs)
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def write_highlights(highlights):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(HIGHLIGHTS_FILE, "w") as f:
        json.dump(highlights, f, indent=2, ensure_ascii=False)


def append_log(entry):
    os.makedirs(DATA_DIR, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{ts}] {entry}\n")


# --- Demo-Slap API ---

def api_demo_slap(method, path, data=None, params=None, retries=5, backoff=15):
    headers = {
        "x-api-key": get_demo_slap_key(),
        "Content-Type": "application/json",
    }
    url = f"{DEMOSLAP_API_BASE}{path}"

    for attempt in range(1, retries + 1):
        try:
            if method.upper() == "POST":
                r = requests.post(url, json=data, headers=headers, params=params, timeout=30)
            else:
                r = requests.get(url, headers=headers, params=params, timeout=30)

            try:
                j = r.json()
            except Exception:
                j = {"error": r.text}

            if r.status_code >= 400:
                return {"success": False, "status": r.status_code, "data": j}
            return {"success": True, "status": r.status_code, "data": j}

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            if attempt == retries:
                print(f"❌ Network error after {retries} attempts: {e}")
                sys.exit(1)
            wait = backoff * attempt
            print(f"⚠️  Network error (attempt {attempt}/{retries}), retrying in {wait}s...")
            time.sleep(wait)
