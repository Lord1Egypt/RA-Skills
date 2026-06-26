#!/usr/bin/env python3
"""
Configuration manager for screen-vision skill.
Loads and validates configuration from file or environment.
"""

import json
import os

DEFAULT_CONFIG = {
    "vision": {
        "provider": "",
        "baseUrl": "",
        "apiKey": "",
        "model": ""
    },
    "safety": {
        "max_duration_min": 5,
        "max_actions": 100,
        "confirm_before": ["delete", "format", "rm", "sudo", "payment"],
        "screenshot_log": True,
        "auto_stop_on_error": True
    },
    "performance": {
        "screenshot_interval_sec": 1.0,
        "diff_threshold": 0.02,
        "wait_after_action_sec": 1.0,
        "max_retries": 3
    },
    "display": {
        "resolution": "1024x768",
        "display_id": ""
    }
}

CONFIG_PATHS = [
    os.path.expanduser("~/.openclaw/workspace/skills/screen-vision/config.json"),
    "/etc/screen-vision/config.json"
]


def load_config():
    """Load config from file, environment, or defaults."""
    config = DEFAULT_CONFIG.copy()
    
    # Try config files
    for path in CONFIG_PATHS:
        if os.path.exists(path):
            try:
                with open(path) as f:
                    file_config = json.load(f)
                config = deep_merge(config, file_config)
                break
            except (json.JSONDecodeError, IOError):
                pass
    
    # Environment variable overrides
    env_overrides = {
        "SV_VISION_API_KEY": ("vision", "apiKey"),
        "SV_VISION_BASE_URL": ("vision", "baseUrl"),
        "SV_VISION_MODEL": ("vision", "model"),
        "SV_VISION_PROVIDER": ("vision", "provider"),
        "SV_DISPLAY": ("display", "display_id"),
        "SV_RESOLUTION": ("display", "resolution"),
        "SV_MAX_DURATION": ("safety", "max_duration_min"),
        "SV_MAX_ACTIONS": ("safety", "max_actions"),
        "SV_SCREENSHOT_INTERVAL": ("performance", "screenshot_interval_sec"),
    }
    
    for env_key, (section, key) in env_overrides.items():
        val = os.environ.get(env_key)
        if val:
            # Type conversion
            if key in ("max_duration_min", "max_actions"):
                val = int(val)
            elif key in ("screenshot_interval_sec",):
                val = float(val)
            config[section][key] = val
    
    return config


def deep_merge(base, override):
    """Deep merge two dicts."""
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def save_config(config, path=None):
    """Save config to file."""
    if path is None:
        path = CONFIG_PATHS[0]
    
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    return path


if __name__ == "__main__":
    config = load_config()
    print(json.dumps(config, indent=2, ensure_ascii=False))
