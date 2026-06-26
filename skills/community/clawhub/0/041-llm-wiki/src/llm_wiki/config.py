"""
LLM-Wiki 配置加载器

支持 config.yaml 的读取、默认值合并和环境变量插值。
"""

import os
import re
from pathlib import Path
from typing import Any, Dict, Optional

import yaml


DEFAULT_CONFIG: Dict[str, Any] = {
    "embedding": {
        "enabled": False,
        "provider": "ollama",
        "model": "nomic-embed-text",
        "ollama": {
            "base_url": "http://localhost:11434",
        },
        "openai": {
            "api_key": None,
            "base_url": None,
        },
        "mcp": {
            "transport": "stdio",
            "command": None,
            "args": None,
            "env": None,
            "url": None,
            "tool_name": None,
        },
    },
    "retrieval": {
        "top_k": 10,
        "keyword_weight": 0.3,
        "vector_weight": 0.5,
        "link_weight": 0.2,
        "enable_link_traversal": True,
    },
    "linking": {
        "enabled": True,
        "light_mode": {
            "top_k": 5,
            "min_score": 0.3,
            "auto_link": True,
            "keyword_weight": 0.6,
            "vector_weight": 0.0,
            "link_weight": 0.4,
        },
        "deep_mode": {
            "top_k": 10,
            "min_score": 0.2,
            "max_backward_updates": 5,
            "require_diff_review": True,
            "strategies_allowed": [
                "link_only",
                "append_related",
                "append_section",
            ],
        },
    },
}


_ENV_PATTERN = re.compile(r"\$\{(\w+)(?::-([^}]*))?\}")


def _interpolate_env(value: Any) -> Any:
    """递归替换字符串中的 ${VAR} 或 ${VAR:-default}"""
    if isinstance(value, str):

        def replacer(match):
            var_name = match.group(1)
            default = match.group(2)
            result = os.environ.get(var_name)
            if result is None and default is not None:
                return default
            if result is None:
                return match.group(0)
            return result

        return _ENV_PATTERN.sub(replacer, value)
    if isinstance(value, dict):
        return {k: _interpolate_env(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_interpolate_env(item) for item in value]
    return value


def _deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    """深合并两个字典，override 优先级更高"""
    result = dict(base)
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def load_config(wiki_root: Path) -> Dict[str, Any]:
    """加载 wiki 根目录下的 config.yaml，与默认值合并"""
    config = dict(DEFAULT_CONFIG)
    config_path = wiki_root / "config.yaml"
    if config_path.exists():
        try:
            raw = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
            raw = _interpolate_env(raw)
            config = _deep_merge(config, raw)
        except Exception as e:
            raise ValueError(f"Failed to load config from {config_path}: {e}")
    return config
