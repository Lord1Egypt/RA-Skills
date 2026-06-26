# Operations

Use this reference for key pool, rate limit, and run behavior.

## Key Pool

Set keys in the environment:

```text
BAIDU_AI_SEARCH_API_KEYS=key1,key2,key3
```

Allowed uses:

```text
failover
quota isolation
legal rate limiting
separating dev/test/prod usage
```

Do not describe the key pool as a way to bypass official limits.

## Rate Limit Defaults

Prefer `adaptive_search.py`; it uses mode-specific budgets and stops early when marginal value drops.

Adaptive stop conditions are coverage-aware. Normal/deep runs should attempt required intent coverage before stopping on low yield or the raw-result soft cap. This keeps high `top_k` runs from returning only seed-query results.

`run_search_plan.py` is the fixed-budget fallback and defaults to:

```text
--sleep 0.5
--timeout 30
```

For real usage, increase sleep if errors, throttling, or unstable responses appear.

## Adaptive Defaults

```text
fast:   runs 1 query, top_k=10
normal: starts with 3 queries, plans up to 12 diverse queries, top_k=20
deep:   starts with 5 queries, top_k=30 and up to 5 expansion terms
```

Use:

```bash
python scripts/search.py "新能源汽车 口碑" --mode normal
```

Use `--dry-run` to inspect planned budget without calling the API.

Use `--fixed --top-k 50` only when the user explicitly wants broad/exhaustive coverage or when testing the Skill:

```bash
python scripts/search.py "新能源汽车 口碑" --mode deep --fixed --top-k 50
```

If `--out-dir` is omitted, output is written under:

```text
skill/runs/<timestamp>-<process-id>-<mode>-<topic>
```

The timestamp includes microseconds and the process ID to avoid collisions when several agents or dry-runs start in the same second.

## API Testing Without a Key

Use:

```bash
python scripts/baidu_web_search.py --query "新能源汽车 口碑" --top-k 50 --dry-run
```

This prints endpoint and payload only.

## API Testing With a Key

Use a small smoke test first:

```bash
set BAIDU_AI_SEARCH_API_KEYS=...
python scripts/baidu_web_search.py --query "新能源汽车 口碑" --top-k 10 --output smoke.json
```

Then run a 2-query plan before running deep mode.

## Caching

Adaptive and fixed plan runs use a query-level cache by default under:

```text
skill/cache/web_search
```

The cache is keyed by:

```text
endpoint
query
top_k
freshness
include_domains
block_domains
```

The cache stores request payloads and raw API responses. It never stores API keys. Cached responses are marked with `key_id: "cache"` and `cache_hit: true`.

Default TTL is 24 hours:

```bash
python scripts/search.py "新能源汽车 口碑" --mode normal --cache-ttl 86400
```

Force live API calls for latest/current questions:

```bash
python scripts/search.py "新能源汽车 口碑" --mode normal --no-cache
```

Cache should not hide raw API failures; failed calls are not cached.

## File Hygiene

For draft usage, write runs under the skill folder or a user-specified run directory. Do not scatter temporary outputs across Desktop or home.
