#!/usr/bin/env python3
import os
from pathlib import Path
from typing import Dict, Optional

DEFAULT_BASE_URL = "https://dashscope.aliyuncs.com/api/v1"
DEFAULT_ENV_PATH = Path(__file__).resolve().parents[3] / "secrets" / "bailian.env"


def _load_env_file(env_path: Path) -> Dict[str, str]:
    if not env_path.exists():
        return {}
    data: Dict[str, str] = {}
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def _get_value(key: str, env_path: Optional[Path]) -> Optional[str]:
    if key in os.environ and os.environ[key].strip():
        return os.environ[key].strip()
    file_values = _load_env_file(env_path or DEFAULT_ENV_PATH)
    value = file_values.get(key)
    return value.strip() if value else None


def get_dashscope_key(env_path: Optional[Path] = None) -> str:
    key = _get_value("DASHSCOPE_API_KEY", env_path)
    if not key:
        raise RuntimeError("Missing DASHSCOPE_API_KEY. Set env or secrets/bailian.env")
    return key


def get_region_base_url(env_path: Optional[Path] = None) -> str:
    return _get_value("DASHSCOPE_BASE_URL", env_path) or DEFAULT_BASE_URL


def get_tts_config(env_path: Optional[Path] = None) -> Dict[str, str]:
    return {
        "model": _get_value("BAILIAN_TTS_MODEL", env_path) or "qwen3-tts-flash",
        "voice": _get_value("BAILIAN_TTS_VOICE", env_path),
        "sample_rate": _get_value("BAILIAN_TTS_SAMPLE_RATE", env_path) or "16000",
    }


def get_oss_config(env_path: Optional[Path] = None) -> Dict[str, str]:
    cfg = {
        "access_key": _get_value("OSS_ACCESS_KEY", env_path),
        "secret_key": _get_value("OSS_SECRET_KEY", env_path),
        "bucket": _get_value("OSS_BUCKET", env_path),
        "endpoint": _get_value("OSS_ENDPOINT", env_path),
        "region": _get_value("OSS_REGION", env_path),
    }
    missing = [k for k, v in cfg.items() if not v]
    if missing:
        raise RuntimeError(f"Missing OSS config: {', '.join(missing)}")
    return cfg
