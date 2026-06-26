from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict


ROOT_DIR = Path(__file__).resolve().parents[2]
CONFIG_DIR = ROOT_DIR / "config"
REFERENCES_DIR = ROOT_DIR / "references"
GENERATED_DIR = ROOT_DIR / "generated_images"
OUTPUT_CONTENT = ROOT_DIR / "generated_content.json"
OUTPUT_CAPTION = ROOT_DIR / "generated_caption.json"
DEFAULT_CONFIG_PATH = CONFIG_DIR / "default-config.json"
LOCAL_CONFIG_PATH = CONFIG_DIR / "local-config.json"
ENV_CONFIG_KEY = "EASY_XHS_CONFIG"


class EasyXHSError(Exception):
    """Base error for the skill."""


class ConfigError(EasyXHSError):
    """Raised for invalid or missing configuration."""


class ApiError(EasyXHSError):
    """Raised for remote API failures."""


class PublishError(EasyXHSError):
    """Raised for publish failures."""


@dataclass
class AppConfig:
    raw: Dict[str, Any]

    @property
    def api_key(self) -> str:
        return str(
            self.raw.get("api", {}).get("key")
            or self.raw.get("api", {}).get("api_key")
            or ""
        ).strip()

    @property
    def base_url(self) -> str:
        return str(
            self.raw.get("api", {}).get("base_url")
            or "https://z.3i0.cn/v1beta"
        ).rstrip("/")

    @property
    def model(self) -> str:
        return str(
            self.raw.get("api", {}).get("model")
            or "gemini-3.1-flash-image-preview"
        ).strip()

    @property
    def timeout_seconds(self) -> int:
        value = self.raw.get('api', {}).get('timeout_seconds', 120)
        try:
            return max(1, int(value))
        except (TypeError, ValueError):
            return 120

    @property
    def max_retries(self) -> int:
        value = self.raw.get('api', {}).get('max_retries', 3)
        try:
            return max(1, int(value))
        except (TypeError, ValueError):
            return 3

    @property
    def mcp_url(self) -> str:
        return str(
            os.environ.get("XHS_MCP_URL")
            or self.raw.get("mcp", {}).get("url")
            or self.raw.get("publish", {}).get("mcp_url")
            or self.raw.get("xhs_mcp", {}).get("url")
            or "http://localhost:18060/mcp"
        ).rstrip("/")

    @property
    def mcp_timeout_seconds(self) -> int:
        value = (
            self.raw.get('mcp', {}).get('timeout_seconds')
            or self.raw.get('publish', {}).get('timeout_seconds')
            or 30
        )
        try:
            return max(1, int(value))
        except (TypeError, ValueError):
            return 30


def deep_merge(base: Dict[str, Any], extra: Dict[str, Any]) -> Dict[str, Any]:
    merged = dict(base)
    for key, value in extra.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def load_json(path: Path, *, default: Any = None) -> Any:
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_config() -> AppConfig:
    config: Dict[str, Any] = {}

    default_cfg = load_json(DEFAULT_CONFIG_PATH, default={}) or {}
    local_cfg = load_json(LOCAL_CONFIG_PATH, default={}) or {}
    config = deep_merge(config, default_cfg)
    config = deep_merge(config, local_cfg)

    env_cfg_raw = os.environ.get(ENV_CONFIG_KEY, "").strip()
    if env_cfg_raw:
        try:
            env_cfg = json.loads(env_cfg_raw)
        except json.JSONDecodeError as exc:
            raise ConfigError(f"环境变量 {ENV_CONFIG_KEY} 不是合法 JSON: {exc}") from exc
        config = deep_merge(config, env_cfg)

    app_config = AppConfig(raw=config)
    if not app_config.api_key:
        raise ConfigError(
            "缺少 API Key。请在 config/local-config.json 或环境变量 EASY_XHS_CONFIG 中设置 api.key"
        )
    return app_config


def load_reference_json(filename: str, *, default: Any = None) -> Any:
    return load_json(REFERENCES_DIR / filename, default=default)


def load_reference_text(filename: str) -> str:
    path = REFERENCES_DIR / filename
    if not path.exists():
        raise ConfigError(f"参考文件不存在: {path}")
    return path.read_text(encoding="utf-8")
