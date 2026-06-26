#!/usr/bin/env python3
"""模板缓存模块 - v2.5.0"""

import time
from typing import Dict, Any, Optional
from collections import OrderedDict
from dataclasses import dataclass, field
import threading

@dataclass
class CacheEntry:
    key: str
    value: Any
    created_at: float = field(default_factory=time.time)
    last_accessed: float = field(default_factory=time.time)
    access_count: int = 0
    size_bytes: int = 0
    
    def touch(self):
        self.last_accessed = time.time()
        self.access_count += 1

class TemplateCache:
    def __init__(self, max_size: int = 100, max_memory_mb: int = 512, ttl_seconds: int = 3600):
        self._cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self._lock = threading.RLock()
        self.max_size = max_size
        self.max_memory_bytes = max_memory_mb * 1024 * 1024
        self.ttl_seconds = ttl_seconds
        self._current_memory = 0
        self.hits = 0
        self.misses = 0
    
    def _is_expired(self, entry: CacheEntry) -> bool:
        if self.ttl_seconds <= 0:
            return False
        return (time.time() - entry.created_at) > self.ttl_seconds
    
    def _evict_if_needed(self):
        while (len(self._cache) >= self.max_size or self._current_memory >= self.max_memory_bytes) and self._cache:
            key, entry = self._cache.popitem(last=False)
            self._current_memory -= entry.size_bytes
    
    def get(self, key: str) -> Optional[Any]:
        with self._lock:
            if key not in self._cache:
                self.misses += 1
                return None
            entry = self._cache[key]
            if self._is_expired(entry):
                del self._cache[key]
                self._current_memory -= entry.size_bytes
                self.misses += 1
                return None
            entry.touch()
            self._cache.move_to_end(key)
            self.hits += 1
            return entry.value
    
    def set(self, key: str, value: Any, size_bytes: int = None):
        with self._lock:
            if key in self._cache:
                old_entry = self._cache.pop(key)
                self._current_memory -= old_entry.size_bytes
            self._evict_if_needed()
            if size_bytes is None:
                size_bytes = len(str(value).encode('utf-8'))
            entry = CacheEntry(key=key, value=value, size_bytes=size_bytes)
            self._cache[key] = entry
            self._current_memory += size_bytes
    
    def clear(self):
        with self._lock:
            self._cache.clear()
            self._current_memory = 0
    
    def stats(self) -> Dict:
        with self._lock:
            hit_rate = (self.hits / (self.hits + self.misses) * 100) if (self.hits + self.misses) > 0 else 0
            return {'entries': len(self._cache), 'memory_bytes': self._current_memory, 'memory_mb': self._current_memory / 1024 / 1024, 'hits': self.hits, 'misses': self.misses, 'hit_rate': hit_rate, 'max_size': self.max_size, 'max_memory_mb': self.max_memory_bytes / 1024 / 1024}
    
    def __len__(self) -> int:
        return len(self._cache)
    
    def __bool__(self) -> bool:
        """确保缓存对象始终为 True"""
        return True
