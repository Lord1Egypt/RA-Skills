#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件缓存模块
用于 CLI 工具在进程间共享缓存数据
"""

import os
import json
import time
from typing import Any, Optional, Dict

script_dir = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(script_dir, '.cache')
DEFAULT_TTL = 300  # 5 分钟


def _ensure_cache_dir():
    """确保缓存目录存在"""
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)


def _get_cache_path(key: str) -> str:
    """获取缓存文件路径"""
    safe_key = key.replace('/', '_').replace('\\', '_')
    return os.path.join(CACHE_DIR, f"{safe_key}.json")


def get(key: str, default: Any = None) -> Any:
    """
    从缓存获取数据
    
    Args:
        key: 缓存键
        default: 缓存不存在时的默认值
    
    Returns:
        缓存的数据，不存在返回 default
    """
    cache_path = _get_cache_path(key)
    if not os.path.exists(cache_path):
        return default
    
    try:
        with open(cache_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 检查是否过期
        if data.get('expire_at', 0) < time.time():
            try:
                delete(key)
            except Exception:
                pass  # 删除失败也返回 default
            return default
        
        return data.get('value')
    except Exception:
        return default


def set(key: str, value: Any, ttl: int = DEFAULT_TTL) -> bool:
    """
    设置缓存
    
    Args:
        key: 缓存键
        value: 缓存值
        ttl: 过期时间（秒），默认 300 秒
    
    Returns:
        是否成功
    """
    try:
        _ensure_cache_dir()
        cache_path = _get_cache_path(key)
        
        data = {
            'value': value,
            'expire_at': time.time() + ttl,
            'created_at': time.time()
        }
        
        with open(cache_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return True
    except Exception:
        return False


def delete(key: str) -> bool:
    """
    删除缓存
    
    Args:
        key: 缓存键
    
    Returns:
        是否成功
    """
    try:
        cache_path = _get_cache_path(key)
        if os.path.exists(cache_path):
            os.remove(cache_path)
        return True
    except Exception:
        return False


def clear() -> bool:
    """
    清空所有缓存
    
    Returns:
        是否成功
    """
    try:
        if os.path.exists(CACHE_DIR):
            for filename in os.listdir(CACHE_DIR):
                if filename.endswith('.json'):
                    os.remove(os.path.join(CACHE_DIR, filename))
        return True
    except Exception:
        return False


def get_or_set(key: str, default_func, ttl: int = DEFAULT_TTL) -> Any:
    """
    获取缓存，不存在则调用函数生成并缓存
    
    Args:
        key: 缓存键
        default_func: 生成默认值的函数
        ttl: 过期时间（秒）
    
    Returns:
        缓存值或新生成的值
    """
    value = get(key)
    if value is not None:
        return value
    
    value = default_func()
    set(key, value, ttl)
    return value


def get_stats() -> Dict[str, Any]:
    """
    获取缓存统计信息
    
    Returns:
        包含缓存数量、大小、过期数量的字典
    """
    stats = {
        'count': 0,
        'size': 0,
        'expired': 0,
        'files': []
    }
    
    if not os.path.exists(CACHE_DIR):
        return stats
    
    current_time = time.time()
    for filename in os.listdir(CACHE_DIR):
        if filename.endswith('.json'):
            filepath = os.path.join(CACHE_DIR, filename)
            try:
                file_size = os.path.getsize(filepath)
                stats['count'] += 1
                stats['size'] += file_size
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if data.get('expire_at', 0) < current_time:
                        stats['expired'] += 1
                
                stats['files'].append({
                    'name': filename,
                    'size': file_size
                })
            except Exception:
                pass
    
    stats['size_kb'] = round(stats['size'] / 1024, 2)
    return stats


def cleanup_expired() -> int:
    """
    清理所有过期缓存文件
    
    Returns:
        清理的文件数量
    """
    count = 0
    current_time = time.time()
    
    if not os.path.exists(CACHE_DIR):
        return count
    
    for filename in os.listdir(CACHE_DIR):
        if filename.endswith('.json'):
            filepath = os.path.join(CACHE_DIR, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if data.get('expire_at', 0) < current_time:
                        os.remove(filepath)
                        count += 1
            except Exception:
                pass
    
    return count
