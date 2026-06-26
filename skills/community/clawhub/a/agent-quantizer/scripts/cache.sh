#!/usr/bin/env bash
# Smart Cache - 工具结果缓存 & 语义去重
# 避免重复 API 调用

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
CACHE_DIR="$SKILL_DIR/cache"
CACHE_DB="$CACHE_DIR/cache.json"
STATS_FILE="$CACHE_DIR/stats.json"

mkdir -p "$CACHE_DIR"

init_cache() {
    [[ -f "$CACHE_DB" ]] || echo '{"entries":{}}' > "$CACHE_DB"
    [[ -f "$STATS_FILE" ]] || echo '{"hits":0,"misses":0}' > "$STATS_FILE"
}

hash_query() {
    echo -n "$1" | sha256sum | cut -c1-16
}

# 语义相似度 (Jaccard)
similarity() {
    python3 -c "
import sys
a = set('''$1'''.lower().split())
b = set('''$2'''.lower().split())
print(round(len(a & b) / len(a | b), 4) if a and b else 0)
" 2>/dev/null || echo "0"
}

cmd_get() {
    local query="$1"
    local category="${2:-general}"
    local threshold="${3:-0.85}"

    init_cache
    local qhash
    qhash=$(hash_query "$query")

    # 精确匹配
    local entry
    entry=$(jq -r --arg h "$qhash" '.entries[$h] // empty' "$CACHE_DB" 2>/dev/null)
    if [[ -n "$entry" ]]; then
        local ttl created now age
        ttl=$(echo "$entry" | jq -r '.ttl // 3600')
        created=$(echo "$entry" | jq -r '.created // 0')
        now=$(date +%s)
        age=$((now - created))

        if [[ $age -lt $ttl ]]; then
            jq '.hits += 1' "$STATS_FILE" > "$STATS_FILE.tmp" && mv "$STATS_FILE.tmp" "$STATS_FILE"
            echo "HIT|exact|$(echo "$entry" | jq -r '.response')"
            return 0
        fi
    fi

    # 语义匹配
    local now
    now=$(date +%s)
    jq -r --arg c "$category" '.entries | to_entries[] | select(.value.category == $c) | [.key, .value.query, .value.response, .value.ttl, .value.created] | @tsv' "$CACHE_DB" 2>/dev/null | \
    while IFS=$'\t' read -r key cached_q cached_r ttl created; do
        local age=$((now - created))
        [[ $age -ge $ttl ]] && continue

        local sim
        sim=$(similarity "$query" "$cached_q")
        if (( $(echo "$sim >= $threshold" | bc -l 2>/dev/null || echo 0) )); then
            jq '.hits += 1' "$STATS_FILE" > "$STATS_FILE.tmp" && mv "$STATS_FILE.tmp" "$STATS_FILE"
            echo "HIT|semantic($sim)|$cached_r"
            return 0
        fi
    done

    jq '.misses += 1' "$STATS_FILE" > "$STATS_FILE.tmp" && mv "$STATS_FILE.tmp" "$STATS_FILE"
    echo "MISS"
    return 1
}

cmd_set() {
    local query="$1"
    local response="$2"
    local category="${3:-general}"
    local ttl="${4:-3600}"

    init_cache
    local qhash
    qhash=$(hash_query "$query")
    local now
    now=$(date +%s)

    jq --arg h "$qhash" --arg q "$query" --arg r "$response" --arg c "$category" \
       --argjson ttl "$ttl" --argjson ts "$now" \
       '.entries[$h] = {query:$q, response:$r, category:$c, ttl:$ttl, created:$ts}' \
       "$CACHE_DB" > "$CACHE_DB.tmp" && mv "$CACHE_DB.tmp" "$CACHE_DB"

    echo "OK|$qhash"
}

cmd_clean() {
    init_cache
    local now
    now=$(date +%s)

    jq --argjson now "$now" '.entries |= with_entries(select((.value.created + .value.ttl) > $now))' \
       "$CACHE_DB" > "$CACHE_DB.tmp" && mv "$CACHE_DB.tmp" "$CACHE_DB"
    echo "OK"
}

cmd_stats() {
    init_cache
    local total hits misses rate=0
    total=$(jq '.entries | length' "$CACHE_DB")
    hits=$(jq '.hits // 0' "$STATS_FILE")
    misses=$(jq '.misses // 0' "$STATS_FILE")
    if [[ $((hits + misses)) -gt 0 ]]; then
        rate=$((hits * 100 / (hits + misses)))
    fi

    echo "📊 缓存统计"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  条目: $total"
    echo "  命中: $hits"
    echo "  未命中: $misses"
    echo "  命中率: ${rate}%"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━"

    echo ""
    echo "按类别:"
    jq -r '.entries | to_entries[].value.category' "$CACHE_DB" 2>/dev/null | sort | uniq -c | sort -rn | \
    while read -r c cat; do echo "  $cat: $c"; done
}

cmd_list() {
    init_cache
    jq -r '.entries | to_entries | sort_by(.value.created) | reverse[:20][] |
        "\(.value.created) | \(.value.category) | \(.value.query[:50])"' "$CACHE_DB" 2>/dev/null || echo "(空)"
}

cmd_flush() {
    echo '{"entries":{}}' > "$CACHE_DB"
    echo '{"hits":0,"misses":0}' > "$STATS_FILE"
    echo "OK"
}

# TTL 预设
get_ttl() {
    case "${1:-general}" in
        tool)     echo 1800 ;;
        knowledge) echo 86400 ;;
        realtime) echo 300 ;;
        *)        echo 3600 ;;
    esac
}

case "${1:-help}" in
    get)    shift; cmd_get "$@" ;;
    set)    shift; cmd_set "$@" ;;
    clean)  cmd_clean ;;
    stats)  cmd_stats ;;
    list)   shift; cmd_list ;;
    flush)  cmd_flush ;;
    help|-h|--help)
        echo "Smart Cache - API 调用缓存"
        echo ""
        echo "  get <query> [category] [threshold]"
        echo "  set <query> <response> [category] [ttl_sec]"
        echo "  clean    清理过期"
        echo "  stats    统计"
        echo "  list     列出条目"
        echo "  flush    清空"
        echo ""
        echo "类别: general(1h) tool(30m) knowledge(24h) realtime(5m)"
        ;;
    *) echo "未知: $1" >&2; exit 1 ;;
esac
