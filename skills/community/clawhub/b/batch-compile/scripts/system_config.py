from __future__ import annotations

import json
import secrets
import string
import time
from copy import deepcopy

import gitea_api as g
from utils import now_str, slugify

COMMON_MODULE_VERSION = "paperkb-v3.0"
SYSTEM_REPO = "system-config"


def ensure_system_repo() -> None:
    g.create_bot_repo(SYSTEM_REPO, "paper-kb system control plane", private=True)
    for name, initial in {
        "users.json": {},
        "teams.json": {},
        "chat_bindings.json": {},
        "pending_chat_bindings.json": {},
        "chat_binding_events.json": [],
        "sources.json": {},
        "jobs.json": {},
        "active_tasks.json": {},
        "permissions.json": {},
    }.items():
        g.ensure_file(g.BOT_USERNAME, SYSTEM_REPO, name, json.dumps(initial, ensure_ascii=False, indent=2), f"init {name}")


def read_json(name: str, default):
    ensure_system_repo()
    result = g.get_file(g.BOT_USERNAME, SYSTEM_REPO, name)
    if not result:
        return default
    try:
        return json.loads(result[0])
    except json.JSONDecodeError:
        return default


def write_json(name: str, data) -> None:
    ensure_system_repo()
    existing = g.get_file(g.BOT_USERNAME, SYSTEM_REPO, name)
    content = json.dumps(data, ensure_ascii=False, indent=2)
    g.put_file(g.BOT_USERNAME, SYSTEM_REPO, name, content, f"update {name}", sha=existing[1] if existing else None)


def update_json(name: str, mutate_fn, default=None, max_retries: int = 3):
    """Read-modify-write a system-config JSON file with sha retry.

    mutate_fn receives a mutable copy of the current JSON object and may mutate it
    in place or return a replacement object. The written object is returned.
    """
    ensure_system_repo()
    if default is None:
        default = {}
    last_error: Exception | None = None
    for _ in range(max_retries):
        existing = g.get_file(g.BOT_USERNAME, SYSTEM_REPO, name)
        sha = existing[1] if existing else None
        if existing:
            try:
                current = json.loads(existing[0])
            except json.JSONDecodeError:
                current = deepcopy(default)
        else:
            current = deepcopy(default)
        candidate = deepcopy(current)
        returned = mutate_fn(candidate)
        if returned is not None:
            candidate = returned
        try:
            content = json.dumps(candidate, ensure_ascii=False, indent=2)
            g.put_file(g.BOT_USERNAME, SYSTEM_REPO, name, content, f"update {name}", sha=sha)
            return candidate
        except g.GiteaError as exc:
            last_error = exc
            time.sleep(0.3)
    raise g.GiteaError(f"{name} 写入失败（重试 {max_retries} 次）：{last_error}")


def users() -> dict:
    return read_json("users.json", {})


def teams() -> dict:
    return read_json("teams.json", {})


def chat_bindings() -> dict:
    return read_json("chat_bindings.json", {})


def pending_chat_bindings() -> dict:
    return read_json("pending_chat_bindings.json", {})


def chat_binding_events() -> list:
    return read_json("chat_binding_events.json", [])


def sources() -> dict:
    return read_json("sources.json", {})


def jobs() -> dict:
    return read_json("jobs.json", {})


def active_tasks() -> dict:
    return read_json("active_tasks.json", {})


def make_invite_code(team_name: str) -> str:
    prefix = "".join(ch for ch in slugify(team_name).upper() if ch.isalnum())[:8] or "TEAM"
    suffix = "".join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(4))
    return f"{prefix}-{suffix}"


def new_record_id(prefix: str) -> str:
    return f"{prefix}_{secrets.token_hex(4)}"


def touch_record(record: dict) -> dict:
    record["updated_at"] = now_str()
    return record
