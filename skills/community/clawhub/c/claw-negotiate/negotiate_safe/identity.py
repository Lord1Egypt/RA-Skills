"""Identity/profile helpers for negotiate_safe."""
from __future__ import annotations

import os
import subprocess
from typing import Mapping
import json
from pathlib import Path


ENV_PATH_PREFIX = "skills.entries.negotiate_safe.env."
OPENCLAW_CONFIG_PATH = Path("/root/.openclaw/openclaw.json")


def _config_has_value(key: str, value: str, path: Path | None = None) -> bool:
    path = path or OPENCLAW_CONFIG_PATH
    try:
        cfg = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return False
    env = (
        cfg.get("skills", {})
        .get("entries", {})
        .get("negotiate_safe", {})
        .get("env", {})
    )
    return isinstance(env, dict) and str(env.get(key) or "") == value


def build_env_updates(identity: dict) -> dict[str, str]:
    """Map a parsed identity to OpenClaw skill env updates."""
    updates: dict[str, str] = {}
    name = (identity.get("name") or "").strip()
    title = (identity.get("title") or "").strip()
    company = (identity.get("company") or "").strip()
    firm = (identity.get("firm") or "").strip()
    role = identity.get("role", "founder")

    if role == "founder":
        if name:
            updates["FOUNDER_NAME"] = name
        if title:
            updates["FOUNDER_TITLE"] = title
        if company:
            updates["COMPANY_NAME"] = company
    else:
        if name:
            updates["INVESTOR_NAME"] = name
        if firm:
            updates["INVESTOR_FIRM"] = firm
        if title:
            updates["INVESTOR_FIRM"] = updates.get("INVESTOR_FIRM", firm)
    return updates


def persist_env_updates(
    updates: dict[str, str],
    runner=subprocess.run,
) -> list[str]:
    """Apply identity updates via `openclaw config set`."""
    failures: list[str] = []
    for key, value in updates.items():
        path = f"{ENV_PATH_PREFIX}{key}"
        try:
            result = runner(
                ["openclaw", "config", "set", path, value],
                capture_output=True,
                text=True,
                timeout=30,
            )
        except subprocess.TimeoutExpired:
            if not _config_has_value(key, value):
                failures.append(key)
            continue
        except FileNotFoundError:
            failures.append(key)
            continue
        if result.returncode != 0 and not _config_has_value(key, value):
            failures.append(key)
    return failures


def profile_from_env(env: Mapping[str, str] | None = None) -> dict[str, str]:
    """Return the saved profile fields from environment-like mapping."""
    source = env if env is not None else os.environ
    return {
        "founder_name": source.get("FOUNDER_NAME", ""),
        "founder_title": source.get("FOUNDER_TITLE", ""),
        "company_name": source.get("COMPANY_NAME", ""),
        "investor_name": source.get("INVESTOR_NAME", ""),
        "investor_firm": source.get("INVESTOR_FIRM", ""),
    }
