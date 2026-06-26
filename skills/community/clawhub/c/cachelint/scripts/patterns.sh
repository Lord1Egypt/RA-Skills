#!/usr/bin/env bash
# CacheLint -- Caching Anti-Pattern Definitions
# 90 patterns across 6 categories, 15 patterns each.
#
# Format per line:
#   REGEX|SEVERITY|CHECK_ID|DESCRIPTION|RECOMMENDATION
#
# Severity levels:
#   critical -- Immediate data integrity or availability risk
#   high     -- Significant caching problem requiring prompt attention
#   medium   -- Moderate concern that should be addressed in current sprint
#   low      -- Best practice suggestion or informational finding
#
# IMPORTANT: All regexes use POSIX ERE syntax (grep -E compatible).
# - Use [[:space:]] instead of \s
# - Use [[:alnum:]] instead of \w
# - NEVER use pipe (|) for alternation inside regex -- it conflicts with
#   the field delimiter. Use separate patterns or character classes instead.
# - Use \b-free alternatives where boundary assertions are unavailable
#
# Categories:
#   CI (Cache Invalidation)   -- 15 patterns (CI-001 to CI-015)
#   TE (TTL & Expiry)         -- 15 patterns (TE-001 to TE-015)
#   CS (Cache Stampede)       -- 15 patterns (CS-001 to CS-015)
#   RM (Redis/Store Misuse)   -- 15 patterns (RM-001 to RM-015)
#   CA (Cache Architecture)   -- 15 patterns (CA-001 to CA-015)
#   SH (Security & Hygiene)   -- 15 patterns (SH-001 to SH-015)

set -euo pipefail

# ============================================================================
# 1. CACHE INVALIDATION (CI-001 through CI-015)
#    Detects missing invalidation after write/update/delete, manual cache.del
#    without pattern, stale data after mutation, partial invalidation.
# ============================================================================

declare -a CACHELINT_CI_PATTERNS=()

CACHELINT_CI_PATTERNS+=(
  # CI-001: Database update without cache invalidation nearby
  'UPDATE[[:space:]].*SET[[:space:]].*WHERE.*[;]|high|CI-001|SQL UPDATE without cache invalidation in surrounding context|Add cache.del() or cache.invalidate() after every UPDATE to prevent stale reads'

  # CI-002: Database DELETE without cache invalidation
  'DELETE[[:space:]]FROM[[:space:]]|high|CI-002|SQL DELETE without cache invalidation in surrounding context|Invalidate related cache keys after DELETE operations to prevent stale data'

  # CI-003: Single key cache.del without pattern-based invalidation
  'cache\.del\([[:space:]]*["\x27][a-zA-Z_]+["\x27][[:space:]]*\)|medium|CI-003|Single-key cache deletion without pattern-based invalidation|Use pattern-based invalidation (scan + del) to ensure all related keys are cleared'

  # CI-004: SET after UPDATE without preceding DEL
  'cache\.set\([^)]*\).*UPDATE[[:space:]]|high|CI-004|Cache SET colocated with UPDATE without preceding cache DEL|Delete cache key before database UPDATE, then let next read repopulate the cache'

  # CI-005: save/update model call without cache invalidation
  '\.save\(\)[[:space:]]*;|medium|CI-005|ORM save() without cache invalidation|Add cache invalidation after model save() to prevent stale cached data'

  # CI-006: Bulk insert/update without cache clear
  'insertMany\([^)]*\)|high|CI-006|Bulk insert operation without cache invalidation|Invalidate affected cache keys or flush cache namespace after bulk writes'

  # CI-007: updateMany/updateAll without invalidation
  'updateMany\([^)]*\)|high|CI-007|Bulk update operation without cache invalidation|Clear all related cache entries after bulk update operations'

  # CI-008: Redis SET without checking for stale keys
  'redis\.set\([[:space:]]*["\x27][^"]*["\x27]|medium|CI-008|Redis SET without verifying stale key removal|Ensure old cache entries are invalidated before setting new values'

  # CI-009: Cache write then DB write ordering
  'cache\.set.*\.[a-z]*[Ss]ave\(\)|critical|CI-009|Cache written before database save (wrong ordering)|Write database first, then update cache to prevent inconsistency on DB failure'

  # CI-010: No invalidation in event handler after mutation
  'on[A-Z][a-z]*[Cc]reated\([^)]*\)[[:space:]]*\{|medium|CI-010|Entity creation event handler without cache invalidation|Add cache invalidation logic to creation event handlers'

  # CI-011: Manual key construction for deletion
  'del\([[:space:]]*["\x27][a-z]+[:_]["\x27][[:space:]]*\+|medium|CI-011|Manual cache key construction for deletion (fragile)|Use a centralized key builder function to ensure consistent key generation and deletion'

  # CI-012: Remove/destroy without cache cleanup
  '\.destroy\(\)[[:space:]]*;|medium|CI-012|Record destroy without cache cleanup|Invalidate cache entries when records are destroyed to prevent orphaned cache data'

  # CI-013: No cascade invalidation for related entities
  'cache\.del\([^)]*\)[[:space:]]*;[[:space:]]*$|low|CI-013|Cache deletion without cascade invalidation for related entities|Invalidate dependent cache keys when parent entities change'

  # CI-014: No invalidation on bulk delete
  'deleteMany\([^)]*\)|high|CI-014|Bulk delete operation without cache invalidation|Flush relevant cache namespace or pattern after bulk delete operations'

  # CI-015: Mutation endpoint without invalidation call
  'router\.[a-z]*\([[:space:]]*["\x27].*["\x27].*req.*res.*\{|low|CI-015|Route handler (potential mutation) without visible cache invalidation|Ensure POST/PUT/DELETE route handlers include cache invalidation logic'
)

# ============================================================================
# 2. TTL & EXPIRY (TE-001 through TE-015)
#    Detects missing TTL on cache.set, TTL too long/short, no jitter,
#    hardcoded TTL magic numbers, missing TTL on session stores.
# ============================================================================

declare -a CACHELINT_TE_PATTERNS=()

CACHELINT_TE_PATTERNS+=(
  # TE-001: cache.set without TTL/expiry argument
  'cache\.set\([[:space:]]*["\x27][^"]*["\x27][[:space:]]*,[[:space:]]*[^,)]*\)[[:space:]]*;|high|TE-001|cache.set() without TTL or expiry argument|Always pass a TTL: cache.set(key, value, { ttl: seconds }) to prevent unbounded growth'

  # TE-002: TTL exceeding 24 hours (86400 seconds)
  '[Tt][Tt][Ll][[:space:]]*[:=][[:space:]]*[0-9]{6,}|medium|TE-002|TTL value exceeds 86400 seconds (24 hours)|Reduce TTL to match data freshness requirements; long TTLs risk serving stale data'

  # TE-003: TTL set to less than 1 second
  '[Tt][Tt][Ll][[:space:]]*[:=][[:space:]]*0\.[0-9]|medium|TE-003|TTL less than 1 second (ineffective caching)|Sub-second TTLs provide negligible caching benefit; increase to at least 1-5 seconds'

  # TE-004: Hardcoded TTL magic numbers
  'expire[[:space:]]*\([[:space:]]*["\x27][^"]*["\x27][[:space:]]*,[[:space:]]*3600[[:space:]]*\)|low|TE-004|Hardcoded TTL magic number (3600)|Use named constants for TTL values: const CACHE_TTL_1H = 3600'

  # TE-005: No jitter on TTL values
  'setex\([[:space:]]*["\x27][^"]*["\x27][[:space:]]*,[[:space:]]*[0-9]+[[:space:]]*,|medium|TE-005|Cache SETEX without TTL jitter|Add random jitter to TTL: ttl + random(0, ttl*0.1) to prevent synchronized expiry'

  # TE-006: Session store without TTL/maxAge
  'session[Ss]tore\([^)]*\)|medium|TE-006|Session store configuration without visible TTL or maxAge|Configure maxAge or TTL on session stores to prevent unbounded session growth'

  # TE-007: Redis SET without EX or PX option
  'redis\.set\([[:space:]]*["\x27][^"]*["\x27][[:space:]]*,[[:space:]]*[^,)]*\)[[:space:]]*[;]|high|TE-007|Redis SET without EX/PX expiry option|Use SET with EX: redis.set(key, value, "EX", ttl) to prevent memory leaks'

  # TE-008: PERSIST command removing TTL
  '\.persist\([[:space:]]*["\x27]|high|TE-008|Redis PERSIST removing TTL from key|Avoid PERSIST unless intentional; removing TTL creates keys that never expire'

  # TE-009: No default TTL configuration
  'createClient\([[:space:]]*\{[^}]*\}[[:space:]]*\)|low|TE-009|Cache client created without default TTL configuration|Configure a default TTL in client options as a safety net for missing per-key TTLs'

  # TE-010: maxAge missing on local cache
  'new[[:space:]][A-Z][a-zA-Z]*Cache\([[:space:]]*\{|medium|TE-010|Local cache instantiation without maxAge or TTL option|Set maxAge on local cache: new LRUCache({ max: 500, maxAge: 1000 * 60 })'

  # TE-011: Inconsistent TTL on related keys
  'setex.*user[[:space:]]*.*[0-9]+|low|TE-011|Cache SETEX with potentially inconsistent TTL for related keys|Use consistent TTL values across related cache keys to prevent partial staleness'

  # TE-012: TTL not matching SLA requirements
  'expire.*[0-9]{7,}|medium|TE-012|TTL exceeds 1 million seconds (potentially mismatched with SLA)|Review TTL against data freshness SLA; values over 11 days are rarely appropriate'

  # TE-013: No sliding expiration where needed
  'cache\.get\([^)]*\)[[:space:]]*;[[:space:]]*$|low|TE-013|Cache read without sliding expiration renewal|Consider refreshing TTL on read (sliding expiration) for frequently accessed keys'

  # TE-014: Cache set without EX/PX in Redis command string
  '["\x27]SET["\x27][[:space:]]*,[[:space:]]*["\x27][^"]*["\x27][[:space:]]*,[[:space:]]*["\x27][^"]*["\x27][[:space:]]*\)|high|TE-014|Redis SET command string without EX/PX expiry|Include EX in Redis SET commands: SET key value EX ttl'

  # TE-015: Missing default TTL in cache config
  'cacheManager\.[a-z]*\([[:space:]]*\{[^}]*\}|low|TE-015|Cache manager configuration without default TTL|Set a default TTL in cache manager config as a safety net'
)

# ============================================================================
# 3. CACHE STAMPEDE (CS-001 through CS-015)
#    Detects missing locking on cache miss, thundering herd on expiry,
#    missing singleflight/coalesce, no stale-while-revalidate.
# ============================================================================

declare -a CACHELINT_CS_PATTERNS=()

CACHELINT_CS_PATTERNS+=(
  # CS-001: Cache miss triggering direct database query without lock
  'cache\.get.*null.*[Qq]uery\(|critical|CS-001|Cache miss triggers direct database query without stampede protection|Add distributed lock or singleflight on cache miss to prevent thundering herd'

  # CS-002: Cache miss with immediate fetch (no mutex)
  'cache\.get.*null.*fetch\(|critical|CS-002|Cache miss triggers immediate HTTP fetch without lock|Use a mutex or singleflight pattern to coalesce concurrent cache rebuild requests'

  # CS-003: Missing singleflight or request coalescing
  'if.*cache\.get.*null[^}]*cache\.set|high|CS-003|Cache miss check-then-set without coalescing or singleflight|Implement singleflight pattern to prevent parallel cache rebuilds for the same key'

  # CS-004: No stale-while-revalidate pattern
  'cache\.get\([^)]*\)[[:space:]]*;[[:space:]]*if[[:space:]]*\(!|medium|CS-004|Cache read without stale-while-revalidate pattern|Serve stale data while revalidating in background to avoid cache miss latency'

  # CS-005: Parallel cache rebuild on miss
  'Promise\.all.*cache\.set|high|CS-005|Parallel cache set operations (potential stampede on coordinated miss)|Use a single writer pattern; only one process should rebuild the cache entry'

  # CS-006: Missing distributed lock on cache rebuild
  'cache\.get.*null.*cache\.set|high|CS-006|Cache get-miss-set without distributed lock (stampede risk)|Use Redis SETNX or Redlock for distributed locking during cache rebuild'

  # CS-007: No early recompute before expiry
  'expire[sd].*cache\.get|medium|CS-007|Cache key with expiry but no early recompute strategy|Implement probabilistic early expiration to refresh cache before actual TTL expires'

  # CS-008: Hot key access without protection
  '\.get\([[:space:]]*["\x27]popular|medium|CS-008|Hot key cache access without stampede protection|Add special handling for hot keys: local cache tier, lock on rebuild, or longer TTL'

  # CS-009: Multiple clients check cache simultaneously
  'async.*cache\.get.*cache\.set|high|CS-009|Async cache get-then-set pattern (concurrent stampede risk)|Use atomic getOrSet or lock-protected rebuild to prevent concurrent rebuilds'

  # CS-010: Missing probabilistic early expiration
  'ttl[[:space:]]*[-=][[:space:]]*[0-9].*cache\.set|low|CS-010|Fixed TTL without probabilistic early expiration|Add probabilistic early recompute: if(ttl < threshold * random()) then rebuild'

  # CS-011: No read-through cache pattern
  'cache\.get.*==[[:space:]]*null|medium|CS-011|Manual cache miss handling instead of read-through pattern|Use a read-through cache that automatically fetches on miss with built-in stampede protection'

  # CS-012: Cache warming absent for predictable hot data
  'app\.listen\([[:space:]]*[0-9]|low|CS-012|Server startup without cache warming for hot data|Pre-warm critical cache keys at startup to prevent cold-start stampede'

  # CS-013: Missing background refresh for expiring keys
  'cache\.get.*expire|low|CS-013|Cache read near expiry without background refresh|Implement background refresh to rebuild cache entries before they expire'

  # CS-014: No request coalescing on concurrent misses
  'await[[:space:]]cache\.get|medium|CS-014|Awaiting cache get without request coalescing|Use a deduplication layer to coalesce concurrent requests for the same cache key'

  # CS-015: Delete then rebuild without lock
  'cache\.del.*cache\.set|high|CS-015|Cache delete immediately followed by set without lock protection|Use distributed lock between delete and rebuild to prevent stampede window'
)

# ============================================================================
# 4. REDIS/STORE MISUSE (RM-001 through RM-015)
#    Detects KEYS * in production, missing connection pooling, no maxmemory
#    policy, unbounded lists, missing pipelines.
# ============================================================================

declare -a CACHELINT_RM_PATTERNS=()

CACHELINT_RM_PATTERNS+=(
  # RM-001: KEYS * command in production code
  '\.keys\([[:space:]]*["\x27]\*["\x27]|critical|RM-001|Redis KEYS * command used (blocks server, O(N) scan)|Replace KEYS * with SCAN for production use to avoid blocking the Redis server'

  # RM-002: Missing connection pooling
  'createClient\(\)[[:space:]]*;|medium|RM-002|Redis client created without connection pooling configuration|Use a connection pool (e.g., generic-pool) to manage Redis connections efficiently'

  # RM-003: No maxmemory-policy configuration
  'redis\.createClient\([[:space:]]*\{[^}]*port|low|RM-003|Redis client without visible maxmemory-policy awareness|Configure maxmemory-policy (allkeys-lru recommended) to handle memory pressure gracefully'

  # RM-004: Unbounded LPUSH/RPUSH without LTRIM
  '[lr]push\([[:space:]]*["\x27][^"]*["\x27]|medium|RM-004|Redis LPUSH/RPUSH without corresponding LTRIM (unbounded list growth)|Add LTRIM after push operations to cap list length and prevent memory exhaustion'

  # RM-005: Missing pipeline for batch operations
  'for.*redis\.[a-z]+\(|high|RM-005|Redis commands in a loop without pipeline (N round trips)|Use redis.pipeline() to batch multiple Redis commands and reduce network round trips'

  # RM-006: BLPOP/BRPOP without timeout
  'b[lr]pop\([[:space:]]*["\x27][^"]*["\x27][[:space:]]*,[[:space:]]*0|high|RM-006|Redis BLPOP/BRPOP with timeout 0 (blocks indefinitely)|Set a reasonable timeout for blocking operations to prevent hung connections'

  # RM-007: FLUSHALL or FLUSHDB in application code
  'flush[Aa]ll\(\)|critical|RM-007|Redis FLUSHALL in application code (deletes ALL data)|Remove FLUSHALL from application code; use targeted key deletion instead'

  # RM-008: FLUSHDB in application code
  'flush[Dd][Bb]\(\)|critical|RM-008|Redis FLUSHDB in application code (deletes entire database)|Remove FLUSHDB; use SCAN + DEL for targeted cleanup instead'

  # RM-009: Redis SELECT for database switching
  '\.select\([[:space:]]*[0-9]+[[:space:]]*\)|medium|RM-009|Redis SELECT for database switching (anti-pattern in production)|Use key prefixes or separate Redis instances instead of SELECT for namespace isolation'

  # RM-010: Missing AUTH or password on Redis connection
  'createClient\([[:space:]]*\{[[:space:]]*host|low|RM-010|Redis client connection without visible authentication|Configure password/AUTH on Redis connections to prevent unauthorized access'

  # RM-011: Large value storage (JSON.stringify of large object)
  'JSON\.stringify\([^)]*\)[[:space:]]*\)[[:space:]]*;.*cache|medium|RM-011|Large serialized object stored in cache (potential memory waste)|Compress large values or store only essential fields; keep cached values under 1MB'

  # RM-012: Missing MULTI/EXEC for atomic operations
  'redis\.[a-z]+.*redis\.[a-z]+|medium|RM-012|Multiple Redis commands without MULTI/EXEC for atomicity|Wrap related Redis operations in MULTI/EXEC for atomic execution'

  # RM-013: SET without EXPIRE (missing TTL after SET)
  'redis\.set\([^)]*\)[[:space:]]*$|high|RM-013|Redis SET without subsequent EXPIRE (key never expires)|Use SET with EX option or call EXPIRE immediately after SET'

  # RM-014: Synchronous Redis in async context
  'redis\.[a-z]+Sync\(|high|RM-014|Synchronous Redis call in potentially async context|Use async Redis operations to avoid blocking the event loop'

  # RM-015: No Redis health check
  'redis\.createClient\([^)]*\)[[:space:]]*;[[:space:]]*$|low|RM-015|Redis client created without health check or ready event handler|Add redis.on("ready") and redis.on("error") handlers for connection health monitoring'
)

# ============================================================================
# 5. CACHE ARCHITECTURE (CA-001 through CA-015)
#    Detects cache-aside without error fallback, write-through without
#    confirmation, local cache without distributed sync, N+1 cache gets.
# ============================================================================

declare -a CACHELINT_CA_PATTERNS=()

CACHELINT_CA_PATTERNS+=(
  # CA-001: Cache-aside without error fallback
  'cache\.get.*catch.*throw|high|CA-001|Cache-aside pattern without fallback on cache failure|Add fallback to database on cache error; never let cache failure break the request'

  # CA-002: Write-through without write confirmation
  'cache\.set.*\.[a-z]*[Ss]ave|medium|CA-002|Write-through cache without verifying database write success|Confirm database write succeeds before updating cache to prevent inconsistency'

  # CA-003: Local cache without distributed sync
  'new[[:space:]]Map\(\)[[:space:]]*;.*cache|medium|CA-003|Local in-memory cache (Map) without distributed synchronization|Use a distributed cache (Redis/Memcached) or add pub/sub sync for multi-instance consistency'

  # CA-004: Missing cache warming on startup
  'app\.listen.*[0-9]+|low|CA-004|Application startup without cache warming strategy|Pre-populate hot cache keys at startup to prevent cold-start performance degradation'

  # CA-005: N+1 cache gets in a loop
  'for.*cache\.get\(|high|CA-005|N+1 cache gets inside a loop (excessive round trips)|Use multi-get (mget) to fetch multiple cache keys in a single round trip'

  # CA-006: Serialization of large objects into cache
  'JSON\.stringify\([[:space:]]*[a-zA-Z]+[[:space:]]*\).*cache\.set|medium|CA-006|Full object serialization into cache (potential >100KB)|Cache only essential fields; use projections to reduce serialized cache value size'

  # CA-007: No cache layer abstraction
  'redis\.[a-z]+\([[:space:]]*["\x27]|low|CA-007|Direct Redis calls without cache abstraction layer|Create a cache service/wrapper to decouple business logic from cache implementation'

  # CA-008: Mixing cache strategies in same module
  'cache\.set.*cache\.get.*writeThrough|medium|CA-008|Mixed cache strategies (cache-aside and write-through) in same module|Use one consistent caching strategy per data domain to reduce complexity'

  # CA-009: Cache without eviction policy
  'new[[:space:]][A-Z][a-zA-Z]*Cache\([[:space:]]*\)|medium|CA-009|Cache created without eviction policy configuration|Configure max size and eviction policy (LRU/LFU) to prevent unbounded memory growth'

  # CA-010: Storing mutable references in local cache
  'cache\.set\([^,]*,[[:space:]]*[a-zA-Z]+[[:space:]]*\)|low|CA-010|Storing object reference in cache (mutations affect cached value)|Clone objects before caching to prevent unintended mutation of cached data'

  # CA-011: No cache miss metrics or monitoring
  'cache\.get\([^)]*\)[[:space:]]*;[[:space:]]*$|low|CA-011|Cache access without miss rate metrics or monitoring|Add cache hit/miss counters for monitoring; track cache hit ratio over time'

  # CA-012: Cache tightly coupled to business logic
  'cache\.get.*cache\.set.*return|low|CA-012|Cache logic interleaved with business logic (tight coupling)|Extract caching into a decorator or middleware to separate concerns'

  # CA-013: No multi-tier cache strategy
  'redis\.get\([^)]*\)[[:space:]]*;[[:space:]]*$|low|CA-013|Single-tier cache without local memory layer|Add a local in-memory cache tier (L1) in front of Redis (L2) for hot keys'

  # CA-014: Missing cache-aside retry on failure
  'cache\.get.*catch[[:space:]]*\{[[:space:]]*\}|high|CA-014|Cache failure silently swallowed without fallback to database|On cache failure, fall through to database and optionally log the cache error'

  # CA-015: No error boundary around cache operations
  'await[[:space:]]cache\.[a-z]+\(|medium|CA-015|Awaiting cache operation without try/catch error boundary|Wrap cache operations in try/catch; cache failures should never break the application'
)

# ============================================================================
# 6. SECURITY & HYGIENE (SH-001 through SH-015)
#    Detects sensitive data in cache, PII in keys, missing auth on Redis,
#    cache key injection, missing namespaces.
# ============================================================================

declare -a CACHELINT_SH_PATTERNS=()

CACHELINT_SH_PATTERNS+=(
  # SH-001: Sensitive data in cache without encryption
  'cache\.set\([^)]*password|critical|SH-001|Password or sensitive data stored in cache without encryption|Never cache plaintext passwords; hash or encrypt sensitive data before caching'

  # SH-002: PII in cache keys
  'cache\.get\([[:space:]]*["\x27].*email.*["\x27]|high|SH-002|PII (email) used directly in cache key|Hash or tokenize PII in cache keys to prevent exposure in logs and monitoring'

  # SH-003: Redis connection without authentication
  'redis://localhost|medium|SH-003|Redis connection URL without authentication credentials|Use redis://:password@host:port or configure AUTH for Redis connections'

  # SH-004: User input directly in cache key (injection risk)
  'cache\.[a-z]+\([[:space:]]*req\.[a-z]+\.|high|SH-004|User request input used directly in cache key (injection risk)|Sanitize and validate user input before using in cache keys; use allowlists for key components'

  # SH-005: Missing namespace prefix on cache keys
  'cache\.set\([[:space:]]*["\x27][a-z]+["\x27]|low|SH-005|Cache key without namespace prefix|Add namespace prefix to cache keys: app:entity:id to prevent collisions across services'

  # SH-006: No monitoring or metrics on cache
  'createClient\([^)]*\)[[:space:]]*;[[:space:]]*[a-z]|low|SH-006|Cache client setup without monitoring or metrics configuration|Add cache metrics: hit rate, miss rate, latency, eviction count for operational visibility'

  # SH-007: Unencrypted Redis transport
  'redis://[^s]|medium|SH-007|Redis connection using unencrypted transport (redis:// not rediss://)|Use TLS: rediss:// protocol or configure TLS options for encrypted Redis transport'

  # SH-008: Token or secret in cache value
  'cache\.set\([^)]*token|high|SH-008|Token or secret stored in cache value|Encrypt sensitive tokens before caching or store only token hashes'

  # SH-009: Missing access control on cache
  'cache\.[a-z]+\([[:space:]]*["\x27]admin|medium|SH-009|Admin-level cache key without access control verification|Verify authorization before accessing privileged cache entries'

  # SH-010: Cache shared across trust boundaries
  'shared[Cc]ache\.[a-z]+\(|high|SH-010|Shared cache accessed across trust boundaries|Isolate caches per tenant or trust boundary; use key prefixes per tenant at minimum'

  # SH-011: No audit logging on cache operations
  'cache\.del\([^)]*\)[[:space:]]*;[[:space:]]*$|low|SH-011|Cache deletion without audit logging|Log cache invalidation events for debugging and audit trails'

  # SH-012: User ID from request directly in cache key
  'cache\.[a-z]+\([[:space:]]*["\x27].*req\.params\.[a-z]+|high|SH-012|Request parameter used directly in cache key without validation|Validate and sanitize request parameters before embedding in cache keys'

  # SH-013: Session data cached without encryption
  'cache\.set\([^)]*session|high|SH-013|Session data stored in cache without encryption|Encrypt session data before caching to protect user session integrity'

  # SH-014: Missing cache size monitoring
  'redis\.createClient|low|SH-014|Redis client without cache size or memory monitoring setup|Monitor Redis memory usage with INFO memory and set maxmemory alerts'

  # SH-015: Redis connection without TLS
  'port[[:space:]]*:[[:space:]]*6379|medium|SH-015|Redis connection on default port without visible TLS configuration|Enable TLS on Redis connections in production environments'
)

# ============================================================================
# Utility Functions
# ============================================================================

# Get total pattern count across all categories
cachelint_pattern_count() {
  local count=0
  count=$((count + ${#CACHELINT_CI_PATTERNS[@]}))
  count=$((count + ${#CACHELINT_TE_PATTERNS[@]}))
  count=$((count + ${#CACHELINT_CS_PATTERNS[@]}))
  count=$((count + ${#CACHELINT_RM_PATTERNS[@]}))
  count=$((count + ${#CACHELINT_CA_PATTERNS[@]}))
  count=$((count + ${#CACHELINT_SH_PATTERNS[@]}))
  echo "$count"
}

# Get pattern count for a specific category
cachelint_category_count() {
  local category="$1"
  local patterns_name
  patterns_name=$(get_cachelint_patterns_for_category "$category")
  if [[ -z "$patterns_name" ]]; then
    echo 0
    return
  fi
  local -n _ref="$patterns_name"
  echo "${#_ref[@]}"
}

# Get patterns array name for a category
get_cachelint_patterns_for_category() {
  local category="$1"
  case "$category" in
    CI|ci) echo "CACHELINT_CI_PATTERNS" ;;
    TE|te) echo "CACHELINT_TE_PATTERNS" ;;
    CS|cs) echo "CACHELINT_CS_PATTERNS" ;;
    RM|rm) echo "CACHELINT_RM_PATTERNS" ;;
    CA|ca) echo "CACHELINT_CA_PATTERNS" ;;
    SH|sh) echo "CACHELINT_SH_PATTERNS" ;;
    *)     echo "" ;;
  esac
}

# Get the human-readable label for a category
get_cachelint_category_label() {
  local category="$1"
  case "$category" in
    CI|ci) echo "Cache Invalidation" ;;
    TE|te) echo "TTL & Expiry" ;;
    CS|cs) echo "Cache Stampede" ;;
    RM|rm) echo "Redis/Store Misuse" ;;
    CA|ca) echo "Cache Architecture" ;;
    SH|sh) echo "Security & Hygiene" ;;
    *)     echo "$category" ;;
  esac
}

# All category codes for iteration
get_all_cachelint_categories() {
  echo "CI TE CS RM CA SH"
}

# Get categories available for a given tier level
# free=0 -> CI, TE (30 patterns)
# pro=1  -> CI, TE, CS, RM (60 patterns)
# team=2 -> all 6 (90 patterns)
# enterprise=3 -> all 6 (90 patterns)
get_cachelint_categories_for_tier() {
  local tier_level="${1:-0}"
  if [[ "$tier_level" -ge 2 ]]; then
    echo "CI TE CS RM CA SH"
  elif [[ "$tier_level" -ge 1 ]]; then
    echo "CI TE CS RM"
  else
    echo "CI TE"
  fi
}

# Severity to numeric points for scoring
severity_to_points() {
  case "$1" in
    critical) echo 25 ;;
    high)     echo 15 ;;
    medium)   echo 8 ;;
    low)      echo 3 ;;
    *)        echo 0 ;;
  esac
}

# List patterns by category
cachelint_list_patterns() {
  local filter_category="${1:-all}"

  if [[ "$filter_category" == "all" ]]; then
    for cat in CI TE CS RM CA SH; do
      cachelint_list_patterns "$cat"
    done
    return
  fi

  local patterns_name
  patterns_name=$(get_cachelint_patterns_for_category "$filter_category")
  if [[ -z "$patterns_name" ]]; then
    echo "Unknown category: $filter_category"
    return 1
  fi

  local -n _patterns_ref="$patterns_name"
  local label
  label=$(get_cachelint_category_label "$filter_category")

  echo "  ${label} (${filter_category}):"
  for entry in "${_patterns_ref[@]}"; do
    IFS='|' read -r regex severity check_id description recommendation <<< "$entry"
    printf "    %-8s %-10s %s\n" "$check_id" "$severity" "$description"
  done
  echo ""
}

# Validate that a category code is valid
is_valid_cachelint_category() {
  local category="$1"
  case "$category" in
    CI|ci|TE|te|CS|cs|RM|rm|CA|ca|SH|sh) return 0 ;;
    *) return 1 ;;
  esac
}
