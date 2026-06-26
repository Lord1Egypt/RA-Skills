"""Configuration module for Chronos skill."""
import json
import os
from pathlib import Path


def get_config_path() -> Path:
    """Return the configuration file path."""
    configured = os.getenv("CHRONOS_CONFIG_PATH")
    if configured:
        return Path(configured).expanduser()
    return Path.home() / ".config" / "chronos" / "config.json"


def _load_config_file(config_path: Path) -> tuple[dict, str | None]:
    if not config_path.exists():
        return {}, None

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f), None
    except (json.JSONDecodeError, IOError) as exc:
        return {}, f"Failed to read chronos config: {exc}"


def inspect_config() -> dict:
    """Return structured diagnostics for configuration resolution."""
    config_path = get_config_path()
    env_chat_id = os.getenv("CHRONOS_CHAT_ID")
    file_config, file_error = _load_config_file(config_path)
    file_chat_id = file_config.get("chat_id") if isinstance(file_config, dict) else None

    env_chat_id = env_chat_id.strip() if isinstance(env_chat_id, str) else env_chat_id
    file_chat_id = str(file_chat_id).strip() if file_chat_id is not None else None

    resolved_chat_id = None
    source = None
    status = "ok"
    error = file_error

    if env_chat_id:
        resolved_chat_id = env_chat_id
        source = "env"
    elif file_chat_id:
        resolved_chat_id = file_chat_id
        source = "config"
    else:
        status = "error"
        if not error:
            error = (
                "CHRONOS_CHAT_ID not configured. Please set an environment variable or add "
                f"chat_id to {config_path}"
            )

    return {
        "status": status,
        "config_path": str(config_path),
        "config_exists": config_path.exists(),
        "env_chat_id_present": bool(env_chat_id),
        "file_chat_id_present": bool(file_chat_id),
        "chat_id": resolved_chat_id,
        "source": source,
        "error": error,
        "config": file_config if isinstance(file_config, dict) else {},
    }


def validate_config() -> dict:
    """Return config diagnostics and raise when config is invalid."""
    info = inspect_config()
    if info["status"] != "ok":
        raise ValueError(info["error"])
    return info


def get_chat_id() -> str:
    """Get the chat ID for reminders.

    Priority:
    1. Environment variable: CHRONOS_CHAT_ID
    2. Config file: ~/.config/chronos/config.json or CHRONOS_CONFIG_PATH (field: chat_id)
    3. Raises error if not configured
    """
    return validate_config()["chat_id"]


def get_config() -> dict:
    """Get full configuration dictionary."""
    info = validate_config()
    config = dict(info["config"])
    config["chat_id"] = info["chat_id"]
    config["chat_id_source"] = info["source"]
    config["config_path"] = info["config_path"]
    return config
