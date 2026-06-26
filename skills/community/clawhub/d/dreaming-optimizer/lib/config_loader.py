#!/usr/bin/env python3
"""YAML configuration loader with fallback defaults."""
import yaml
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger("dreaming-optimizer.config")

DEFAULT_CONFIG = {
    "version": "1.0.0",
    "scoring": {
        "default_threshold": 70,
        "archive_threshold": 35,
        "max_entries_per_cycle": 1000,
    },
    "fact_terms": {
        "zh": [
            "数据库", "API", "配置", "bug", "修复", "测试", "agent", "skill",
            "已修复", "已实现", "完成了", "测试通过", "deployed", "fixed",
            "代码", "函数", "模块", "架构", "部署", "上线", "发布",
        ],
        "en": [
            "fixed", "deployed", "implemented", "completed", "tested",
            "bug", "api", "config", "module", "architecture",
        ],
    },
    "dedup": {
        "token_threshold": 0.85,
        "use_embeddings": False,
        "embedding_model": "paraphrase-multilingual-MiniLM-L12-v2",
        "check_blayer_limit": 1000,
    },
    "blayer": {
        "db_name": "main.sqlite",
        "auto_create_schema": True,
    },
    "archive": {
        "enabled": True,
        "dir": "dreaming-archives",
        "max_archive_age_days": 90,
    },
    "output": {
        "summary_dir": "dreaming-summaries",
        "summary_format": "json",
    },
}


def get_default_config() -> dict:
    """Return the default configuration dictionary.
    
    Returns:
        Deep copy of DEFAULT_CONFIG to prevent mutation.
    """
    import copy
    return copy.deepcopy(DEFAULT_CONFIG)


def load_config(config_path: Path = None) -> dict:
    """Load configuration from YAML file with fallback to defaults.
    
    Args:
        config_path: Path to config YAML. Defaults to:
                     ~/.openclaw/workspace/skills/dreaming-optimizer/config/default_threshold.yaml
        
    Returns:
        dict: Configuration dictionary (merged with defaults for missing keys)
    """
    if config_path is None:
        config_path = Path.home() / ".openclaw" / "workspace" / "skills" / "dreaming-optimizer" / "config" / "default_threshold.yaml"
    
    config = get_default_config()
    
    if not config_path.exists():
        logger.info(f"Config file not found at {config_path}, using defaults")
        return config
    
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            user_config = yaml.safe_load(f) or {}
        
        # Merge user config into defaults (deep merge)
        config = _deep_merge(config, user_config)
        logger.info(f"Loaded config from {config_path}")
    except yaml.YAMLError as e:
        logger.warning(f"Failed to parse config YAML: {e}, using defaults")
    except Exception as e:
        logger.warning(f"Failed to load config: {e}, using defaults")
    
    return config


def _deep_merge(base: dict, override: dict) -> dict:
    """Deep merge override dict into base dict.
    
    Args:
        base: Base dictionary (modified in place)
        override: Override dictionary
        
    Returns:
        dict: Merged result
    """
    for key, value in override.items():
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            base[key] = _deep_merge(base[key], value)
        else:
            base[key] = value
    return base


def get_threshold(config: dict = None) -> int:
    """Get the current score threshold from config.
    
    Args:
        config: Config dict (loads default if None)
        
    Returns:
        int: Threshold score (default: 70)
    """
    if config is None:
        config = load_config()
    return config.get("scoring", {}).get("default_threshold", 70)


if __name__ == "__main__":
    import json
    cfg = load_config()
    print(json.dumps(cfg, indent=2, ensure_ascii=False))
