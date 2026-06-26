"""Shared utilities for Leetify scripts."""
import os
import sys
import json

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
STEAM_IDS_FILE = os.path.join(DATA_DIR, "steam_ids.json")
CONFIG_FILE = os.path.join(DATA_DIR, "config.json")

LEETIFY_API_BASE = "https://api-public.cs-prod.leetify.com"


def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {}
    with open(CONFIG_FILE, "r") as f:
        try:
            return json.load(f)
        except Exception:
            return {}


def get_leetify_key():
    key = os.environ.get("LEETIFY_API_KEY") or load_config().get("leetify_api_key")
    if not key:
        print("❌ LEETIFY_API_KEY is not set.")
        sys.exit(1)
    return key


def load_steam_ids():
    if not os.path.exists(STEAM_IDS_FILE):
        return {}
    with open(STEAM_IDS_FILE, "r") as f:
        try:
            return json.load(f)
        except Exception:
            return {}


def get_steam_id(username):
    sid = load_steam_ids().get(username)
    if not sid:
        print(f"❌ Unknown Steam ID for '{username}'. Known: {list(load_steam_ids().keys())}")
        sys.exit(1)
    return sid


def save_steam_id(username, steam_id):
    os.makedirs(DATA_DIR, exist_ok=True)
    data = load_steam_ids()
    data[username] = steam_id
    with open(STEAM_IDS_FILE, "w") as f:
        json.dump(data, f, indent=4)
    print(f"✅ Saved: {username} -> {steam_id}")
