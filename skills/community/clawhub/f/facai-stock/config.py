"""持久化配置管理，读写 data/config.json。"""

import json
from pathlib import Path

_DATA_DIR = Path(__file__).parent / "data"
_CONFIG_PATH = _DATA_DIR / "config.json"


def get(key: str, default=None):
    """读取配置项，文件不存在或键缺失时返回 default。"""
    try:
        data = json.loads(_CONFIG_PATH.read_text(encoding="utf-8"))
        return data.get(key, default)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def set(key: str, value) -> None:
    """写入单个配置项（增量更新，不影响其他键）。"""
    _DATA_DIR.mkdir(parents=True, exist_ok=True)
    try:
        data = json.loads(_CONFIG_PATH.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}
    data[key] = value
    _CONFIG_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def all_config() -> dict:
    """返回全部配置项。"""
    try:
        return json.loads(_CONFIG_PATH.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
