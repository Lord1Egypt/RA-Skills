"""LRU cache for search results with TTL and parameterized keys."""

import time
import hashlib
from collections import OrderedDict
from typing import Any, Dict, List, Optional


class SearchCache:
    """
    LRU cache for search results with time-to-live.

    Caches based on query + all filter parameters. Uses SHA256 hash of the
    canonical parameter string as the cache key.

    Attributes:
        maxsize: Maximum number of entries to keep
        ttl: Time-to-live in seconds for each entry
    """

    def __init__(self, maxsize: int = 500, ttl: int = 300):
        self.maxsize = maxsize
        self.ttl = ttl
        self._cache: OrderedDict[str, Dict] = OrderedDict()
        self.hits = 0
        self.misses = 0

    def _make_key(
        self,
        query: str,
        limit: int,
        repo_path: Optional[str],
        stack: Optional[str],
        min_score: Optional[int],
        max_score: Optional[int],
    ) -> str:
        """Create a stable hash key from search parameters."""
        # Normalize None to empty string for stable canonical form
        repo = repo_path or ""
        stack = stack or ""
        min_s = str(min_score) if min_score is not None else ""
        max_s = str(max_score) if max_score is not None else ""
        # Build canonical string
        canonical = f"q={query}|l={limit}|r={repo}|s={stack}|min={min_s}|max={max_s}"
        return hashlib.sha256(canonical.encode()).hexdigest()[:16]

    def get(
        self,
        query: str,
        limit: int = 10,
        repo_path: Optional[str] = None,
        stack: Optional[str] = None,
        min_score: Optional[int] = None,
        max_score: Optional[int] = None,
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Retrieve cached search results if available and fresh.

        Returns:
            List of result dicts if cached, else None
        """
        key = self._make_key(query, limit, repo_path, stack, min_score, max_score)
        if key not in self._cache:
            self.misses += 1
            return None

        entry = self._cache[key]
        if time.time() - entry["timestamp"] > self.ttl:
            del self._cache[key]
            self.misses += 1
            return None

        # Move to end (LRU)
        self._cache.move_to_end(key)
        self.hits += 1
        return entry["results"]

    def set(
        self,
        query: str,
        results: List[Dict[str, Any]],
        limit: int = 10,
        repo_path: Optional[str] = None,
        stack: Optional[str] = None,
        min_score: Optional[int] = None,
        max_score: Optional[int] = None,
    ) -> None:
        """
        Store search results in cache.

        Args:
            query: Search query string
            results: List of result dictionaries to cache
            limit, repo_path, stack, min_score, max_score: must match the original search params
        """
        key = self._make_key(query, limit, repo_path, stack, min_score, max_score)
        self._cache[key] = {
            "results": results,
            "timestamp": time.time(),
        }
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
