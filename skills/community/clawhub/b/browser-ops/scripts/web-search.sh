#!/bin/bash
# web-search.sh — 搜索降级链（tavily → opencli google → agent-browser）
# 用法: ./web-search.sh "search query" [limit]

set -euo pipefail

QUERY="${1:?Usage: web-search.sh \"query\" [limit]}"
LIMIT="${2:-5}"

# Layer 1: Tavily (如果可用)
if command -v tavily &>/dev/null && [ -n "${TAVILY_API_KEY:-}" ]; then
    result=$(tavily search "$QUERY" --max-results "$LIMIT" 2>&1) || true
    if [ -n "$result" ] && ! echo "$result" | grep -qiE "error|failed"; then
        echo "$result"
        exit 0
    fi
    echo "# [web-search] tavily failed, trying opencli..." >&2
fi

# Layer 2: opencli google search
result=$(opencli google search "$QUERY" --limit "$LIMIT" -f md 2>&1) || true
if [ -n "$result" ] && ! echo "$result" | grep -qiE "error|no.*result|captcha|exit code"; then
    echo "$result"
    exit 0
fi
echo "# [web-search] opencli google failed, trying agent-browser..." >&2

# Layer 3: agent-browser open Google
if command -v agent-browser &>/dev/null; then
    agent-browser --auto-connect open "https://www.google.com/search?q=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$QUERY'))")" 2>/dev/null || true
    sleep 2
    snapshot=$(agent-browser snapshot -i 2>&1) || true
    agent-browser close 2>/dev/null || true
    if [ -n "$snapshot" ] && [ ${#snapshot} -gt 100 ]; then
        echo "$snapshot"
        exit 0
    fi
fi

echo "# [web-search] ALL LAYERS FAILED for query: $QUERY"
exit 1
