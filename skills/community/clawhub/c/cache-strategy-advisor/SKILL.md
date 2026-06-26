---
name: cache-strategy-advisor
description: Design and optimize caching strategies for applications. Analyze data access patterns, recommend cache layers (browser, CDN, application, database), configure TTLs, invalidation policies, and measure cache hit rates.
---

# Cache Strategy Advisor

Design caching strategies that actually improve performance without introducing stale data bugs. Analyze access patterns, recommend appropriate cache layers, configure TTLs and invalidation policies, measure hit rates, and identify cache-related issues.

Use when: "optimize caching", "cache strategy", "what should we cache", "cache hit rate is low", "stale data issues", "CDN caching", "Redis caching strategy", "cache invalidation", or when adding caching to an application.

## Commands

### 1. `analyze` — Assess Current Caching

#### Step 1: Inventory Existing Cache Layers

```bash
# Check for Redis/Memcached
redis-cli ping 2>/dev/null && redis-cli info stats 2>/dev/null | grep -E "keyspace_hits|keyspace_misses|evicted_keys"
memcached-tool localhost:11211 stats 2>/dev/null | grep -E "get_hits|get_misses|evictions"

# Check for application-level caching
rg "cache\.|@cache|@Cacheable|lru_cache|memoize|NodeCache|redis\." \
  --type-not binary -g '!node_modules' -g '!vendor' 2>/dev/null | head -20

# Check CDN headers
curl -sI "https://$HOST" | grep -iE "cache-control|cdn-cache|x-cache|cf-cache|age:" 2>&1

# Check for HTTP caching headers
curl -sI "https://$HOST/api/products" | grep -iE "cache-control|etag|last-modified|vary:" 2>&1
```

#### Step 2: Measure Current Hit Rates

```bash
# Redis hit rate
redis-cli info stats 2>/dev/null | python3 -c "
import sys
stats = {}
for line in sys.stdin:
    if ':' in line:
        k, v = line.strip().split(':', 1)
        stats[k] = v
hits = int(stats.get('keyspace_hits', 0))
misses = int(stats.get('keyspace_misses', 0))
total = hits + misses
if total > 0:
    rate = hits / total * 100
    status = '🟢' if rate > 90 else '🟡' if rate > 70 else '🔴'
    print(f'{status} Cache hit rate: {rate:.1f}% ({hits:,} hits / {misses:,} misses)')
    print(f'Evictions: {stats.get(\"evicted_keys\", 0)}')
else:
    print('No cache activity')
"

# CDN hit rate (Cloudflare example)
# Check X-Cache or CF-Cache-Status headers across multiple requests
for i in $(seq 1 10); do
  curl -sI "https://$HOST/" | grep -i "cf-cache-status\|x-cache" 2>/dev/null
done | sort | uniq -c
```

#### Step 3: Identify Caching Opportunities

Analyze the application for:

**High-value cache candidates:**
- Repeated database queries (same params, frequent calls)
- Expensive computations (aggregations, reports, ML inference)
- External API calls (rate-limited, slow, costly)
- Static or rarely-changing data (config, feature flags, translations)
- Session/auth data (user profiles, permissions)

**Anti-patterns to flag:**
- Caching mutable data without invalidation
- TTLs that don't match data change frequency
- Cache-aside pattern without error handling (cache miss → DB → cache set)
- Thundering herd on cache expiry (no jitter, no lock)
- Over-caching (caching user-specific data in shared cache)

```bash
# Find repeated queries (Django example — enable logging)
# Look for similar queries in application code
rg "\.filter\(|\.get\(|SELECT.*FROM" --type py -g '!migrations' 2>/dev/null | \
  sed 's/[0-9]*//g' | sort | uniq -c | sort -rn | head -10
```

#### Step 4: Recommend Strategy

```markdown
# Cache Strategy Report

## Current State
- Redis: ✅ Running, 85% hit rate, 2.3% eviction rate
- CDN: ⚠️ 45% hit rate (Cache-Control too short)
- Browser: ❌ No Cache-Control headers on static assets
- Application: ⚠️ Selective caching, 3 endpoints cached

## Recommendations

### Layer 1: Browser Cache
- Static assets (JS/CSS/images): `Cache-Control: public, max-age=31536000, immutable`
  Use content-hash filenames for cache busting
- HTML pages: `Cache-Control: no-cache` (revalidate every time)
- API responses: `Cache-Control: private, max-age=60` for user-specific data

### Layer 2: CDN Cache
- Product listings: 5 min TTL with stale-while-revalidate
- Images: 1 year TTL (content-addressed)
- API: bypass CDN for authenticated endpoints, cache public endpoints

### Layer 3: Application Cache (Redis)
| Data | TTL | Invalidation | Pattern |
|------|-----|-------------|---------|
| Product catalog | 5 min | On update + pub/sub | Read-through |
| User sessions | 30 min | On logout | Write-through |
| Search results | 2 min | TTL only | Cache-aside |
| Rate limit counters | 1 min | TTL only | Increment |
| Feature flags | 30 sec | On deploy | Read-through |

### Layer 4: Database Query Cache
- Enable PostgreSQL shared_buffers tuning
- Add materialized views for expensive aggregations
- Index covering queries for most frequent access patterns

## Invalidation Strategy
- Use pub/sub for real-time invalidation across instances
- Add jitter to TTLs: `TTL * (0.8 + random(0.4))` to prevent thundering herd
- Implement cache stampede protection (lock + stale-while-revalidate)
```

### 2. `configure` — Generate Cache Configuration

Output ready-to-use configuration for:
- Nginx/Caddy proxy cache rules
- Cloudflare/CloudFront cache policies
- Redis cache-aside implementation with proper error handling
- Application-level cache decorators

### 3. `debug` — Diagnose Cache Issues

For common cache problems:
- **Stale data:** trace cache TTL vs data update frequency
- **Low hit rate:** check key cardinality, TTL distribution, eviction policy
- **Memory pressure:** analyze key size distribution, suggest eviction candidates
- **Thundering herd:** detect mass expiry patterns, recommend jitter/locking
