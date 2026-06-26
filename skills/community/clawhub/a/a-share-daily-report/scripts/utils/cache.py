
"""
缓存工具模块
提供本地文件缓存功能，减少API调用频率
"""

import os
import json
import time
import hashlib

# 缓存根目录
CACHE_ROOT = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    'cache'
)


def _get_cache_path(key, namespace='default'):
    key_hash = hashlib.md5(key.encode('utf-8')).hexdigest()
    namespace_dir = os.path.join(CACHE_ROOT, namespace)
    os.makedirs(namespace_dir, exist_ok=True)
    return os.path.join(namespace_dir, f'{key_hash}.json')


def get_cache(key, ttl=3600, namespace='default'):
    cache_path = _get_cache_path(key, namespace)
    if not os.path.exists(cache_path):
        return None
    try:
        with open(cache_path, 'r', encoding='utf-8') as f:
            cache_data = json.load(f)
        timestamp = cache_data.get('timestamp', 0)
        if time.time() - timestamp > ttl:
            try:
                os.remove(cache_path)
            except OSError:
                pass
            return None
        return cache_data.get('data')
    except Exception:
        try:
            os.remove(cache_path)
        except OSError:
            pass
        return None


def set_cache(key, data, ttl=3600, namespace='default'):
    cache_path = _get_cache_path(key, namespace)
    try:
        cache_data = {
            'timestamp': time.time(),
            'ttl': ttl,
            'data': data
        }
        with open(cache_path, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False


def clear_cache(namespace='default'):
    """清除指定命名空间的缓存"""
    namespace_dir = os.path.join(CACHE_ROOT, namespace)
    if not os.path.exists(namespace_dir):
        return 0
    count = 0
    for file in os.listdir(namespace_dir):
        if file.endswith('.json'):
            file_path = os.path.join(namespace_dir, file)
            try:
                os.remove(file_path)
                count += 1
            except OSError:
                pass
    return count

