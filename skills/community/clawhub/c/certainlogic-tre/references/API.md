# Token Reduction Engine — API Reference

## Table of Contents

1. [Core Functions](#core-functions)
2. [Cache Operations](#cache-operations)
3. [Metrics](#metrics)
4. [Configuration](#configuration)
5. [Integration Helpers](#integration-helpers)

---

## Core Functions

### `cache_answer(query, answer)`

Store an LLM response in the cache.

**Parameters:**
- `query` (str): The exact user query
- `answer` (str): The LLM-generated response

**Returns:**
```python
{
    "cached": bool,      # Whether answer was stored
    "flagged": bool,     # Whether guard flagged uncertainty
    "reason": str,       # Why it was/wasn't cached
    "warning": str|None  # User-facing warning if flagged
}
```

**Example:**
```python
from tre import cache_answer

result = cache_answer(
    "What is our refund policy?",
    "30 days, no questions asked."
)
# → {"cached": True, "flagged": False, "reason": "Guard passed"}

result = cache_answer(
    "What's the weather?",
    "I think it might rain, but I'm not sure."
)
# → {"cached": False, "flagged": True, "reason": "Guard flagged: uncertain language"}
```

---

### `get_cached_answer(query)`

Retrieve a cached answer for a query.

**Parameters:**
- `query` (str): The exact user query

**Returns:**
- `(answer, token_count)` tuple if cache hit
- `None` if cache miss or expired

**Example:**
```python
from tre import get_cached_answer

cached = get_cached_answer("What is our refund policy?")
if cached:
    answer, tokens = cached
    print(f"Instant! (saved {tokens} tokens)")
else:
    print("Cache miss — fetching from LLM...")
```

---

### `reduce_tokens(query)`

Legacy function for token budget management. Now returns cached answer if available.

**Parameters:**
- `query` (str): The user query

**Returns:**
```python
{
    "reduced_query": str,    # Cached answer or original query
    "original_tokens": int,
    "reduced_tokens": int,
    "tokens_saved": int,
    "cache_hit": bool,
    "method": str,           # "answer_cache" or "original"
    "routing": str           # "deterministic" or "external"
}
```

---

## Cache Operations

### `clear_cache()`

Clear all cache entries (RAM + disk).

```python
from tre import clear_cache

clear_cache()
# All caches wiped. Next queries will be cache misses.
```

---

### `save_cache()` / `load_cache()`

Manual persistence control.

```python
from tre import save_cache, load_cache

# Force save to disk
save_cache()

# Load from disk (auto-called on import)
load_cache()
```

---

### `_hash_query(query)`

Internal: Generate SHA-256 hash of query for cache key.

```python
from tre import _hash_query

key = _hash_query("What is our refund policy?")
# → "a1b2c3d4...f5" (64-char hex string)
```

**Note:** Identical queries produce identical hashes. Normalize whitespace and case for fuzzy matching.

---

## Metrics

### `get_metrics()`

Get cache performance statistics.

**Returns:**
```python
{
    "total_queries": int,        # Total queries processed
    "cache_hits": int,           # Successful cache retrievals
    "cache_misses": int,         # Cache misses
    "cache_hit_rate_percent": float,  # Hit rate (0-100)
    "cache_size": int,           # Current cache entries
    "flagged_responses": int,    # Guard-flagged answers
    "guard_loaded": bool         # Whether guard is active
}
```

**Example:**
```python
from tre import get_metrics

metrics = get_metrics()
print(f"Hit rate: {metrics['cache_hit_rate_percent']}%")
print(f"Saved: {metrics['cache_hits']} LLM calls")
```

---

## Configuration

### `configure(config_dict)`

Update TRE configuration at runtime.

**Parameters:**
- `config_dict` (dict): Configuration key-value pairs

**Example:**
```python
from tre import configure

configure({
    "cache_ttl": 7200,
    "max_cache_size": 50000,
    "hallucination_guard": True,
    "guard_sensitivity": "medium"
})
```

**Config Keys:**

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `cache_ttl` | int | 3600 | Cache expiry in seconds |
| `max_cache_size` | int | 1000 | Max LRU entries |
| `hallucination_guard` | bool | True | Enable guard |
| `guard_sensitivity` | str | "medium" | "low", "medium", "high" |
| `guard_patterns` | list | [] | Additional flag patterns |
| `persistence_path` | str | ~/.tre/cache.json | Save location |
| `auto_persist` | bool | True | Save on every write |
| `forbidden_commands` | set | {} | Extra blocked commands |
| `log_level` | str | "INFO" | Logging level |

---

## Integration Helpers

### `brain_client` (property)

Attach a Company Brain client for Facts DB integration.

```python
from tre import _store_to_brain_api

# Auto-called when caching if BRAIN_API_URL is set
_store_to_brain_api("query", "answer")
# → POST http://localhost:8000/facts
```

---

## Type Signatures

```python
from typing import Dict, Tuple, Optional

def cache_answer(query: str, answer: str) -> Dict[str, any]: ...
def get_cached_answer(query: str) -> Optional[Tuple[str, int]]: ...
def get_metrics() -> Dict[str, any]: ...
def clear_cache() -> None: ...
def configure(config: Dict[str, any]) -> None: ...
```

---

## Error Handling

TRE never raises exceptions on cache operations. All errors are logged and swallowed:

```python
# Safe to call — never crashes
cached = get_cached_answer(query)  # Returns None on any error
result = cache_answer(query, answer)  # Returns {"cached": False, ...} on error
```

**Logged errors:**
- Disk write failure
- Permission denied on persistence path
- Corrupted cache file (auto-clears)
- Guard module import failure
