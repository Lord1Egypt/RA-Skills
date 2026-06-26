#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cached Memory Retrieval
Cache frequent queries to avoid repeated API calls
"""

import hashlib
import json
from pathlib import Path
from datetime import datetime, timedelta

# Cache configuration
CACHE_DIR = Path("C:/Users/Xiabi/.openclaw/workspace/cache")
CACHE_TTL = timedelta(hours=1)  # Cache expires after 1 hour
MAX_CACHE_SIZE = 100  # Max cached queries

class RetrievalCache:
    def __init__(self):
        self.cache_file = CACHE_DIR / "retrieval_cache.json"
        self.cache = self._load_cache()
    
    def _load_cache(self) -> dict:
        """Load cache from file"""
        if self.cache_file.exists():
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _save_cache(self):
        """Save cache to file"""
        CACHE_DIR.mkdir(exist_ok=True)
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump(self.cache, f, ensure_ascii=False, indent=2)
    
    def _get_cache_key(self, query: str) -> str:
        """Generate cache key from query"""
        return hashlib.md5(query.encode()).hexdigest()
    
    def _is_expired(self, timestamp: str) -> bool:
        """Check if cache entry is expired"""
        cached_time = datetime.fromisoformat(timestamp)
        return datetime.now() - cached_time > CACHE_TTL
    
    def _cleanup(self):
        """Remove expired entries and limit cache size"""
        # Remove expired
        self.cache = {
            k: v for k, v in self.cache.items()
            if not self._is_expired(v['timestamp'])
        }
        
        # Limit size (keep most recent)
        if len(self.cache) > MAX_CACHE_SIZE:
            sorted_items = sorted(
                self.cache.items(),
                key=lambda x: x[1]['timestamp'],
                reverse=True
            )
            self.cache = dict(sorted_items[:MAX_CACHE_SIZE])
        
        self._save_cache()
    
    def get(self, query: str) -> list:
        """Get cached results"""
        key = self._get_cache_key(query)
        
        if key in self.cache:
            entry = self.cache[key]
            
            if not self._is_expired(entry['timestamp']):
                print(f"[CACHE] Hit: '{query}'")
                return entry['results']
            else:
                print(f"[CACHE] Expired: '{query}'")
                del self.cache[key]
        
        print(f"[CACHE] Miss: '{query}'")
        return None
    
    def set(self, query: str, results: list):
        """Cache results"""
        key = self._get_cache_key(query)
        
        self.cache[key] = {
            'query': query,
            'results': results,
            'timestamp': datetime.now().isoformat()
        }
        
        self._cleanup()
        print(f"[CACHE] Cached: '{query}' ({len(results)} results)")


# Global cache instance
_cache = None

def get_cache() -> RetrievalCache:
    """Get or create cache instance"""
    global _cache
    if _cache is None:
        _cache = RetrievalCache()
    return _cache


def retrieve_with_cache(query: str, retrieve_func, k: int = 3):
    """
    Retrieve with caching
    
    Args:
        query: Search query
        retrieve_func: Function to call if cache miss
        k: Number of results
    
    Returns:
        Search results
    """
    cache = get_cache()
    
    # Try cache first
    cached = cache.get(query)
    if cached is not None:
        return cached
    
    # Cache miss, call retrieve function
    results = retrieve_func(query, k=k)
    
    # Cache the results
    if results:
        cache.set(query, results)
    
    return results


# Test
if __name__ == "__main__":
    print("=" * 60)
    print("Cached Retrieval Test")
    print("=" * 60)
    
    cache = RetrievalCache()
    
    # Simulate retrieve function
    def mock_retrieve(query, k=3):
        return [f"Result {i} for {query}" for i in range(k)]
    
    # Test 1: First query (cache miss)
    print("\n[Test 1] First query")
    results = retrieve_with_cache("瀑布", mock_retrieve)
    print(f"Results: {results}")
    
    # Test 2: Same query (cache hit)
    print("\n[Test 2] Same query (should hit cache)")
    results = retrieve_with_cache("瀑布", mock_retrieve)
    print(f"Results: {results}")
    
    # Test 3: Different query (cache miss)
    print("\n[Test 3] Different query")
    results = retrieve_with_cache("TTS", mock_retrieve)
    print(f"Results: {results}")
    
    # Show cache stats
    print(f"\n[Cache Stats]")
    print(f"  Entries: {len(cache.cache)}")
    print(f"  File: {cache.cache_file}")
    
    print("\n" + "=" * 60)
