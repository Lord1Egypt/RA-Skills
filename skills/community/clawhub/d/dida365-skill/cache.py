"""Dida365 Cache Management."""

from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Any, Optional


CACHE_FILE = os.path.join(os.path.dirname(__file__), ".dida-cache.json")
# 默认缓存失效时间 (分钟)
DEFAULT_EXPIRATION = int(os.environ.get("DIDA_CACHE_MINUTES", "365"))


def load_cache() -> dict[str, Any]:
    """从本地文件加载缓存。"""
    if not os.path.exists(CACHE_FILE):
        return {}
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def save_cache(cache_data: dict[str, Any]) -> None:
    """保存缓存到本地文件。"""
    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)
    except OSError:
        pass


def get_cached_data(key: str, sub_key: Optional[str] = None) -> Any:
    """
    获取缓存数据。
    如果 sub_key 存在，则从 key 对应的字典中查找。
    如果数据过期或不存在，返回 None。
    """
    cache = load_cache()
    entry = cache.get(key)
    
    if sub_key and entry:
        if not isinstance(entry, dict):
            return None
        entry = entry.get(sub_key)

    if not entry:
        return None

    timestamp = entry.get("timestamp", 0)
    # 过期检查
    if datetime.now().timestamp() - timestamp > DEFAULT_EXPIRATION * 60:
        return None

    return entry.get("data")


def set_cached_data(key: str, data: Any, sub_key: Optional[str] = None) -> None:
    """
    设置缓存数据。
    如果 sub_key 存在，则更新 key 对应的字典。
    如果 data 为 None，则视为清除该缓存项。
    """
    cache = load_cache()
    
    if data is None:
        # 清除逻辑
        if sub_key:
            if key in cache and isinstance(cache[key], dict):
                cache[key].pop(sub_key, None)
        else:
            cache.pop(key, None)
    else:
        # 保存逻辑
        entry = {"timestamp": datetime.now().timestamp(), "data": data}
        if sub_key:
            if key not in cache or not isinstance(cache[key], dict):
                cache[key] = {}
            cache[key][sub_key] = entry
        else:
            cache[key] = entry

    save_cache(cache)


def invalidate_project_cache(project_id: Optional[str] = None) -> None:
    """
    失效项目相关的缓存。
    如果不传 project_id，则清除所有项目的任务缓存。
    """
    if project_id:
        set_cached_data("project_data", None, sub_key=project_id)
    else:
        set_cached_data("project_data", None)
    # 项目列表本身通常也需要联动清除
    set_cached_data("projects", None)


def clear_all_cache() -> None:
    """删除缓存文件。"""
    if os.path.exists(CACHE_FILE):
        try:
            os.remove(CACHE_FILE)
        except OSError:
            pass
