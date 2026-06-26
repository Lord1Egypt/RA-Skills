# Token Reduction Engine — Configuration Guide

## Table of Contents

1. [Quick Config](#quick-config)
2. [Environment Variables](#environment-variables)
3. [Cache Settings](#cache-settings)
4. [Hallucination Guard](#hallucination-guard)
5. [Intent Filtering](#intent-filtering)
6. [Integration Modes](#integration-modes)

---

## Quick Config

```python
# Minimal setup
from tre import configure

configure({
    "cache_ttl": 3600,          # Seconds before cache expiry
    "max_cache_size": 10000,    # Max entries in LRU cache
    "hallucination_guard": True, # Flag hedged responses
    "persistence_path": "~/.tre/cache.json"  # Where to save cache
})
```

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `TRE_CACHE_TTL` | `3600` | Cache time-to-live in seconds |
| `TRE_MAX_CACHE` | `10000` | Maximum cache entries |
| `TRE_PERSISTENCE` | `~/.tre/cache.json` | Cache persistence file path |
| `TRE_GUARD_SENSITIVITY` | `medium` | Hallucination guard: `low`, `medium`, `high` |
| `TRE_LOG_LEVEL` | `INFO` | Logging: `DEBUG`, `INFO`, `WARN`, `ERROR` |
| `TRE_FORBIDDEN_COMMANDS` | (built-in) | Comma-separated list of blocked commands |
| `BRAIN_API_URL` | (none) | URL for Brain Facts DB integration |

---

## Cache Settings

### TTL (Time-To-Live)

```python
# Short TTL for volatile data (stock prices, news)
configure(cache_ttl=300)  # 5 minutes

# Long TTL for stable facts (company policies)
configure(cache_ttl=86400 * 7)  # 7 days

# Infinite TTL for immutable facts
configure(cache_ttl=-1)  # Never expires
```

### Cache Size

```python
# Small footprint
configure(max_cache_size=1000)

# Production workload
configure(max_cache_size=100000)

# Disable limit (not recommended)
configure(max_cache_size=-1)
```

### Persistence

```python
# Auto-save on every write (default)
configure(auto_persist=True)

# Manual save only
configure(auto_persist=False)
# tre.save_cache()  # Call when you want

# No persistence (RAM only, lost on restart)
configure(persistence_path=None)
```

---

## Hallucination Guard

Detects uncertain language in LLM responses before caching.

### Sensitivity Levels

| Level | Triggers | Use Case |
|-------|----------|----------|
| `low` | "I don't know", "unsure" | High-trust environments |
| `medium` | "I think", "probably", "maybe" | Balanced (default) |
| `high` | "might be", "could be", "possibly" | Strict quality control |

```python
# Config
configure(guard_sensitivity="high")

# Result when flagged:
{
    "cached": False,
    "flagged": True,
    "reason": "Contains uncertain language",
    "warning": "⚠️ Response contains hedging language. Not cached."
}
```

### Custom Guard Patterns

```python
# Add domain-specific uncertainty phrases
configure(guard_patterns=[
    "I'm not a lawyer",
    "consult a professional",
    "this is not financial advice"
])
```

---

## Intent Filtering

### Domain Intents

Define which domains your agent handles:

```python
configure(intents={
    "product": {
        "allowed_ops": ["brain.query", "brain.get_page"],
        "forbidden_ops": ["brain.delete_brain", "brain.put_page"]
    },
    "security": {
        "allowed_ops": ["brain.get_page"],
        "forbidden_ops": ["brain.put_page", "brain.ingest"]
    }
})
```

### Forbidden Commands

Built-in blocked commands (extendable):

```python
FORBIDDEN_COMMANDS = {
    "brain.delete_brain",    # Never allow
    "brain.purge",           # Never allow mass purge
    "brain.override_intent", # Intent is human-controlled
    "brain.exec_shell",      # No shell access
    "brain.send_email",      # No outbound email
}

# Add your own
configure(forbidden_commands={"brain.payment.process"})
```

---

## Integration Modes

### Mode 1: Standalone (Pure TRE)

```python
from tre import cache_answer, get_cached_answer

# No brain, no router — just cache
```

### Mode 2: With Company Brain

```python
# Brain provides facts, TRE caches them
from company_brain import get_facts
tre.brain_client = BrainClient("http://localhost:8000")

# Facts auto-populate cache on startup
tre.warm_cache_from_brain()
```

### Mode 3: With Smart Router

```python
# Router decides tier, TRE decides cache
from smart_router import route

# TRE intercepts before routing
cached = tre.get_cached_answer(query)
if cached:
    return cached

# Not cached — router picks cheapest model that can handle it
tier = route(query)
answer = llm_call(query, tier=tier)
tre.cache_answer(query, answer)
```

### Mode 4: Full Stack

```python
from company_brain import get_facts
from smart_router import route
from tre import cache_answer, get_cached_answer

# 1. Brain facts (free)
facts = get_facts(query)
if facts:
    return facts

# 2. TRE cache (free)
cached = get_cached_answer(query)
if cached:
    return cached

# 3. Smart Router (cheapest model)
tier = route(query)
answer = llm_call(query, tier=tier)

# 4. Cache for next time
cache_answer(query, answer)
return answer
```

---

## Performance Tuning

```python
# High-throughput API server
configure(
    cache_ttl=300,          # Short TTL, fast eviction
    max_cache_size=100000,   # Large cache
    auto_persist=False,      # Batch saves
    guard_sensitivity="low"  # Fewer flag checks
)

# Long-running agent
configure(
    cache_ttl=86400,        # Keep all day
    max_cache_size=5000,    # Memory constrained
    auto_persist=True,      # Survive restarts
    guard_sensitivity="high" # Strict quality
)

# Dev/test environment
configure(
    cache_ttl=60,           # Fast turnover
    max_cache_size=100,     # Tiny
    persistence_path=None,  # Reset on restart
    guard_sensitivity="low"
)
```

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Cache miss on identical queries | Query includes timestamps, IDs | Strip variable fields before hashing |
| High flag rate | Guard too sensitive | Lower sensitivity or add domain exceptions |
| Cache not persisting | Path permission | Check `TRE_PERSISTENCE` path is writable |
| Slow cache hits | Cache too large | Reduce `max_cache_size` or use Redis (Pro) |
| Intent blocks valid queries | Intent too narrow | Expand `allowed_ops` for domain |
