"""Config loader for feeds-digest."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml

DEFAULT_CONFIG_PATH = Path.home() / ".config" / "feeds-digest" / "config.yaml"


class ConfigError(Exception):
    """Raised when config is invalid."""


def load_config(path: Path | str | None = None) -> dict[str, Any]:
    """Load YAML config from path or default location."""
    config_path = Path(path) if path else DEFAULT_CONFIG_PATH

    if not config_path.exists():
        raise ConfigError(
            f"Config nicht gefunden: {config_path}\n"
            f"Führe zuerst install.sh aus oder kopiere config.example.yaml nach {config_path}"
        )

    with open(config_path, encoding="utf-8") as f:
        config = yaml.safe_load(f) or {}

    if not isinstance(config, dict):
        raise ConfigError("Config muss ein YAML-Dict sein")

    # Set defaults
    config.setdefault("feeds", {})
    config.setdefault("defaults", {})
    defaults = config["defaults"]
    defaults.setdefault("since", "7d")
    defaults.setdefault("topics", [])
    defaults.setdefault("max_per_source", 10)
    defaults.setdefault("llm", False)
    defaults.setdefault("output_format", "markdown")

    config.setdefault("llm", {})
    llm = config["llm"]
    llm.setdefault("provider", "perplexity")
    llm.setdefault("model", "sonar-pro")
    llm.setdefault("prompt_file", "prompts/summary.md")
    llm.setdefault("max_tokens", 800)
    llm.setdefault("temperature", 0.2)

    return config


def parse_since(since_str: str) -> "timedelta":
    """Parse '3d', '2w', '1m', '12h' into a timedelta."""
    from datetime import timedelta

    if not since_str:
        raise ConfigError("since darf nicht leer sein")

    unit = since_str[-1].lower()
    try:
        value = int(since_str[:-1])
    except ValueError:
        raise ConfigError(f"Ungültiges since-Format: {since_str} (erwartet z.B. '7d', '2w')")

    if unit == "h":
        return timedelta(hours=value)
    elif unit == "d":
        return timedelta(days=value)
    elif unit == "w":
        return timedelta(weeks=value)
    elif unit == "m":
        return timedelta(days=value * 30)  # approx
    else:
        raise ConfigError(f"Unbekannte Einheit: {unit} (erlaubt: h, d, w, m)")
