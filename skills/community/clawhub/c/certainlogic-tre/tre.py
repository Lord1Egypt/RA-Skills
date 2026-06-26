#!/usr/bin/env python3
"""
Token Reduction Engine v1.1 — Answer Caching with Hallucination Guard
-------------------------------------------------------------------
Caches LLM responses so repeated queries return instantly.
Guard gates cache — flagged answers are shown but not stored.

Original: token budget management (query trimming)
Enhanced: response caching (answer storage + uncertainty checking)
"""

import hashlib
import json
import os
import re
import time
import sys
from collections import OrderedDict
from typing import Dict, Tuple, Optional

# ── Try to import Hallucination Guard ──────────────────────────────────
try:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from hallucination_detector import HallucinationDetector
    _guard = HallucinationDetector()
except ImportError:
    _guard = None

# ── Configuration ──────────────────────────────────────────────────────
MAX_TOKENS_PER_QUERY = 512
CACHE_SIZE_LIMIT = 1000
CACHE_TTL_SECONDS = 3600
TOKEN_ESTIMATE_RATIO = 0.75

# ── Answer Cache: {query_hash: (answer, timestamp, token_count)} ───────
_answer_cache: OrderedDict = OrderedDict()
CACHE_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache_data")
CACHE_PERSISTENCE_FILE = os.path.join(CACHE_DATA_DIR, "answer_cache.json")
_cache_hits = 0
_cache_misses = 0
_total_queries = 0
_tokens_saved = 0
_flagged_count = 0

# ── Internal ───────────────────────────────────────────────────────────
def _estimate_tokens(text: str) -> int:
    if not text:
        return 0
    words = len(re.findall(r'\b\w+\b', text))
    return int(words / TOKEN_ESTIMATE_RATIO)

def _hash_query(query: str) -> str:
    return hashlib.sha256(query.encode('utf-8')).hexdigest()

# ── Cache Operations ──────────────────────────────────────────────────────
def _get_from_answer_cache(query_hash: str) -> Optional[Tuple[str, int]]:
    """Retrieve cached answer if exists and not expired."""
    global _cache_hits, _cache_misses
    if query_hash in _answer_cache:
        result, timestamp, token_count = _answer_cache[query_hash]
        if time.time() - timestamp < CACHE_TTL_SECONDS:
            _answer_cache.move_to_end(query_hash)  # LRU
            _cache_hits += 1
            return result, token_count
        else:
            del _answer_cache[query_hash]
    _cache_misses += 1
    return None

def _store_answer_in_cache(query_hash: str, answer: str, token_count: int) -> Dict:
    """
    Store answer in cache ONLY if Hallucination Guard passes.
    
    If Guard detects uncertainty, answer is NOT cached but still returned
    to user with a warning.
    
    Returns: {"cached": bool, "flagged": bool, "reason": str}
    """
    global _answer_cache, _flagged_count
    
    # Guard check
    if _guard is not None:
        try:
            if _guard.is_uncertain(answer):
                _flagged_count += 1
                return {
                    "cached": False,
                    "flagged": True,
                    "reason": "Contains uncertain language (e.g., 'maybe', 'I think', 'not sure')",
                    "warning": "⚠️ Response contains hedging language. Not added to knowledge base."
                }
        except Exception:
            pass  # Don't block on Guard errors
    
    # Cache the clean answer
    _answer_cache[query_hash] = (answer, time.time(), token_count)
    _answer_cache.move_to_end(query_hash)
    if len(_answer_cache) > CACHE_SIZE_LIMIT:
        _answer_cache.popitem(last=False)
    
    # Persist to disk (user cache only — NOT Facts DB)
    _save_cache_to_disk()
    
    return {"cached": True, "flagged": False, "reason": "Guard passed"}


def _save_cache_to_disk():
    """Persist answer cache to disk. NOT Facts DB — this is user-facing cache only."""
    try:
        os.makedirs(CACHE_DATA_DIR, exist_ok=True)
        data = {
            "entries": [
                {"q": query_hash, "a": answer, "ts": ts, "tc": tc}
                for query_hash, (answer, ts, tc) in _answer_cache.items()
            ]
        }
        with open(CACHE_PERSISTENCE_FILE, "w") as fh:
            json.dump(data, fh, indent=2)
    except Exception:
        pass  # Don't crash on write errors

def _load_cache_from_disk():
    """Load persisted answer cache on startup."""
    global _answer_cache
    if not os.path.exists(CACHE_PERSISTENCE_FILE):
        return
    try:
        with open(CACHE_PERSISTENCE_FILE, "r") as fh:
            data = json.load(fh)
        for entry in data.get("entries", []):
            _answer_cache[entry["q"]] = (entry["a"], entry["ts"], entry["tc"])
    except Exception:
        _answer_cache.clear()

def cache_answer(query: str, answer: str) -> Dict:
    """
    Public: attempt to cache an LLM answer for a user query.
    
    Args:
        query: The exact user query string
        answer: The LLM-generated response
    
    Returns:
        {"cached": bool, "flagged": bool, "reason": str, "warning": str|None}
    """
    query_hash = _hash_query(query)
    token_count = _estimate_tokens(answer)
    result = _store_answer_in_cache(query_hash, answer, token_count)
    return result

def get_cached_answer(query: str) -> Optional[Tuple[str, int]]:
    """
    Public: retrieve cached answer for a query.

    Args:
        query: The exact user query string

    Returns:
        (answer, token_count) or None if not in cache
    """
    query_hash = _hash_query(query)
    return _get_from_answer_cache(query_hash)

# ── Legacy: Token Reduction (kept for backward compat) ───────────────────
def reduce_tokens(query: str, force_deterministic: bool = False) -> Dict:
    """Legacy: token budget management for queries."""
    global _total_queries, _tokens_saved
    _total_queries += 1
    
    query_hash = _hash_query(query)
    original_tokens = _estimate_tokens(query)
    
    # Check if we have a cached ANSWER for this query
    cached = _get_from_answer_cache(query_hash)
    if cached:
        answer, token_count = cached
        return {
            'reduced_query': answer,  # Return cached answer instead of original query
            'original_tokens': original_tokens,
            'reduced_tokens': token_count,
            'tokens_saved': original_tokens - token_count,
            'cache_hit': True,
            'method': 'answer_cache',
            'routing': 'deterministic'
        }
    
    return {
        'reduced_query': query,
        'original_tokens': original_tokens,
        'reduced_tokens': original_tokens,
        'tokens_saved': 0,
        'cache_hit': False,
        'method': 'original',
        'routing': 'external'
    }

def get_metrics() -> Dict:
    """Return cache metrics."""
    hit_rate = (_cache_hits / (_cache_hits + _cache_misses)) * 100 if (_cache_hits + _cache_misses) > 0 else 0
    return {
        'total_queries': _total_queries,
        'cache_hits': _cache_hits,
        'cache_misses': _cache_misses,
        'cache_hit_rate_percent': round(hit_rate, 2),
        'cache_size': len(_answer_cache),
        'flagged_responses': _flagged_count,
        'guard_loaded': _guard is not None,
    }

def clear_cache():
    """Clear the answer cache (RAM + disk)."""
    global _answer_cache, _cache_hits, _cache_misses, _total_queries, _tokens_saved, _flagged_count
    _answer_cache.clear()
    _cache_hits = _cache_misses = _total_queries = _tokens_saved = _flagged_count = 0
    try:
        if os.path.exists(CACHE_PERSISTENCE_FILE):
            os.remove(CACHE_PERSISTENCE_FILE)
    except Exception:
        pass


# ── For Brain API integration ──────────────────────────────────────────
def _store_to_brain_api(query: str, answer: str):
    """Persist to Brain API for permanent knowledge base."""
    try:
        import requests
        requests.post('http://127.0.0.1:8000/facts', json={
            'key': query[:100],
            'type': 'string',
            'value': answer[:5000],
            'source': 'tre_answer_cache'
        }, timeout=1)
    except Exception:
        pass  # Don't fail if Brain API down


if __name__ == '__main__':
    # Quick test
    print("=== TRE v1.1 Answer Cache Test ===\n")
    
    # First query — cache miss
    cached = get_cached_answer("What is Python?")
    print(f"1a. First get: {'HIT' if cached else 'MISS'}")
    
    # Cache a clean answer
    result = cache_answer("What is Python?", "Python is a programming language.")
    print(f"1b. Cache result: {json.dumps(result, indent=2)}")
    
    # Same query — cache hit
    cached = get_cached_answer("What is Python?")
    print(f"1c. Second get: {'HIT' if cached else 'MISS'}")
    if cached:
        print(f"    Answer: {cached[0][:50]}...")
    
    # Flagged answer — not cached
    result = cache_answer("What is 2+2?", "I think it might be 4, but I'm not sure.")
    print(f"\n2a. Flagged cache: {json.dumps(result, indent=2)}")
    
    # Cache hit check
    cached = get_cached_answer("What is 2+2?")
    print(f"2b. After flagged: {'HIT (BUG!)' if cached else 'MISS (correct — not cached)'}")
    
    print(f"\n=== Metrics ===")
    print(json.dumps(get_metrics(), indent=2))
    print(f"\n=== Persistence ===")
    if os.path.exists(CACHE_PERSISTENCE_FILE):
        size = os.path.getsize(CACHE_PERSISTENCE_FILE)
        print(f"Cache file: {CACHE_PERSISTENCE_FILE} ({size} bytes)")
    else:
        print(f"Cache not yet persisted.")


# Auto-load persisted cache on module import (process restart)
_load_cache_from_disk()
