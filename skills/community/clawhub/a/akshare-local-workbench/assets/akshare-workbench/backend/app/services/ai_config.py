from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from threading import Lock

logger = logging.getLogger(__name__)

# Stored locally on the backend host. This is a single-user, local hobbyist
# tool, so the key is kept in a plain JSON file that is excluded from VCS.
_CONFIG_DIR = Path(__file__).resolve().parent.parent / "config"
_CONFIG_PATH = _CONFIG_DIR / "ai_config.json"
_lock = Lock()


@dataclass
class AIConfig:
    base_url: str
    model: str
    api_key: str


def _read() -> dict | None:
    if not _CONFIG_PATH.exists():
        return None
    try:
        with _CONFIG_PATH.open("r", encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        logger.warning("Failed to read AI config: %s", exc)
        return None


def load_config() -> AIConfig | None:
    with _lock:
        payload = _read()
    if not payload:
        return None
    base_url = str(payload.get("base_url", "")).strip()
    model = str(payload.get("model", "")).strip()
    api_key = str(payload.get("api_key", "")).strip()
    if not (base_url and model and api_key):
        return None
    return AIConfig(base_url=base_url, model=model, api_key=api_key)


def save_config(base_url: str, model: str, api_key: str) -> AIConfig:
    config = AIConfig(
        base_url=base_url.strip(),
        model=model.strip(),
        api_key=api_key.strip(),
    )
    with _lock:
        _CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        with _CONFIG_PATH.open("w", encoding="utf-8") as fh:
            json.dump(
                {
                    "base_url": config.base_url,
                    "model": config.model,
                    "api_key": config.api_key,
                },
                fh,
                ensure_ascii=False,
                indent=2,
            )
    return config


def clear_config() -> None:
    with _lock:
        if _CONFIG_PATH.exists():
            _CONFIG_PATH.unlink()
