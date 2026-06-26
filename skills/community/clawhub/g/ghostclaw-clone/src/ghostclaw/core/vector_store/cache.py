"""LRU cache for query embeddings with TTL."""

import time
from collections import OrderedDict
from typing import Optional, Tuple
import numpy as np


class EmbeddingCache:
    """
    LRU cache for query embeddings with time-to-live.

    Attributes:
        maxsize: Maximum number of entries to keep
        ttl: Time-to-live in seconds for each entry
    """

    def __init__(self, maxsize: int = 1000, ttl: int = 3600):
        self.maxsize = maxsize
        self.ttl = ttl
        self._cache: OrderedDict[str, Tuple[np.ndarray, float]] = OrderedDict()
        self.hits = 0
        self.misses = 0

    def _normalize(self, query: str) -> str:
        """Normalize query for cache key (lowercase, strip)."""
        return query.strip().lower()

    def get(self, query: str) -> Optional[np.ndarray]:
        """
        Get cached embedding for query, or None if not found/expired.

        Args:
            query: The normalized query string

        Returns:
            numpy array embedding if cached and fresh, else None
        """
        key = self._normalize(query)
        if key not in self._cache:
            self.misses += 1
            return None

        embedding, timestamp = self._cache[key]
        if time.time() - timestamp > self.ttl:
            # Expired
            del self._cache[key]
            self.misses += 1
            return None

        # Move to end (LRU)
        self._cache.move_to_end(key)
        self.hits += 1
        return embedding

    def set(self, query: str, embedding: np.ndarray) -> None:
        """
        Store embedding for query.

        Args:
            query: The query string
            embedding: numpy array embedding
        """
        key = self._normalize(query)
        self._cache[key] = (embedding, time.time())
        # Evict if over capacity
        if len(self._cache) > self.maxsize:
            self._cache.popitem(last=False)  # remove oldest

    def clear(self) -> None:
        """Clear all cached entries."""
        self._cache.clear()
        self.hits = 0
        self.misses = 0

    def stats(self) -> dict:
        """Get cache statistics."""
        total = self.hits + self.misses
        hit_rate = self.hits / total if total > 0 else 0.0
        return {
            "size": len(self._cache),
            "maxsize": self.maxsize,
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": hit_rate,
        }
