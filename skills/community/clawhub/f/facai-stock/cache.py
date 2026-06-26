"""股票列表本地缓存管理"""

import json
import time
from pathlib import Path

_DATA_DIR = Path(__file__).parent / "data"
CACHE_FILE = _DATA_DIR / "stock_id.info"
CACHE_TTL = 24 * 60 * 60  # 24 小时


def load() -> list[dict] | None:
    """读取缓存；不存在或已过期返回 None"""
    if not CACHE_FILE.exists():
        return None
    try:
        payload = json.loads(CACHE_FILE.read_text(encoding="utf-8"))
        age = time.time() - payload.get("saved_at", 0)
        if age > CACHE_TTL:
            return None
        return payload["data"]
    except Exception:
        return None


def save(data: list[dict]) -> None:
    """将数据连同时间戳序列化写入缓存文件"""
    _DATA_DIR.mkdir(parents=True, exist_ok=True)
    payload = {"saved_at": time.time(), "data": data}
    CACHE_FILE.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")


def cache_age_hours() -> float | None:
    """返回当前缓存距今的小时数；文件不存在返回 None"""
    if not CACHE_FILE.exists():
        return None
    try:
        payload = json.loads(CACHE_FILE.read_text(encoding="utf-8"))
        return (time.time() - payload.get("saved_at", 0)) / 3600
    except Exception:
        return None
