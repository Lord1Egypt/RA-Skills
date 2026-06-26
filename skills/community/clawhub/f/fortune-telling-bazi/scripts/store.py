#!/usr/bin/env python3
"""
数据存储模块
"""
import os, json
from datetime import datetime, timezone, timedelta

TZ = timezone(timedelta(hours=8))
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR  = os.path.join(SKILL_DIR, "data")
USERS_FILE = os.path.join(DATA_DIR, "users.json")
ACTIVE_FILE = os.path.join(DATA_DIR, "active.json")


def ensure_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


def load_users():
    ensure_dir()
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_users(data):
    ensure_dir()
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_active():
    if os.path.exists(ACTIVE_FILE):
        with open(ACTIVE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"active": False, "names": []}


def save_active(data):
    ensure_dir()
    with open(ACTIVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def now_iso():
    return datetime.now(TZ).isoformat()
