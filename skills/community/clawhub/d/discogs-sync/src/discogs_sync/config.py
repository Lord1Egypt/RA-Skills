"""Credential and configuration persistence."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from .exceptions import ConfigError

DEFAULT_CONFIG_DIR = Path.home() / ".discogs-sync"
DEFAULT_CONFIG_FILE = DEFAULT_CONFIG_DIR / "config.json"
TOKEN_ENV_VAR = "DISCOGS_USER_TOKEN"


def get_config_path() -> Path:
    return DEFAULT_CONFIG_FILE


def load_config() -> dict:
    """Load configuration from disk. Returns empty dict if file doesn't exist."""
    path = get_config_path()
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        raise ConfigError(f"Failed to read config file {path}: {e}") from e


def save_config(config: dict) -> None:
    """Save configuration to disk."""
    path = get_config_path()
    try:
        path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        path.write_text(json.dumps(config, indent=2), encoding="utf-8")
        # Restrict permissions to owner-only on non-Windows platforms
        if sys.platform != "win32":
            path.chmod(0o600)
    except OSError as e:
        raise ConfigError(f"Failed to write config file {path}: {e}") from e


def get_cache_ttl() -> int:
    """Return the cache TTL in seconds.

    Reads ``cache_ttl_hours`` from the config file. If not set, defaults to
    24 hours (86400 seconds). The value may be a float (e.g. 0.5 for 30 minutes).
    """
    config = load_config()
    hours = config.get("cache_ttl_hours", 24)
    try:
        return int(float(hours) * 3600)
    except (TypeError, ValueError):
        return 86400


def get_tokens() -> dict | None:
    """Return the personal access token settings, or None if not configured.

    The DISCOGS_USER_TOKEN environment variable takes precedence over the
    token stored in the config file by the ``auth`` command.
    """
    env_token = os.environ.get(TOKEN_ENV_VAR)
    if env_token:
        return {"auth_mode": "token", "user_token": env_token, "username": None}

    config = load_config()
    user_token = config.get("user_token")
    if user_token:
        return {
            "auth_mode": "token",
            "user_token": user_token,
            "username": config.get("username"),
        }
    return None


def save_user_token(user_token: str, username: str | None = None) -> None:
    """Store a personal access token to config file."""
    config = load_config()
    config.update(
        {
            "auth_mode": "token",
            "user_token": user_token,
            "username": username,
        }
    )
    save_config(config)


def clear_tokens() -> None:
    """Remove all stored credentials, including keys left by older OAuth configs."""
    config = load_config()
    for key in [
        "auth_mode", "user_token",
        "access_token", "access_token_secret",
        "consumer_key", "consumer_secret",
        "username",
    ]:
        config.pop(key, None)
    save_config(config)
