#!/bin/bash
# web-read.sh — 网页抓取降级链（opencli web read → firecrawl → agent-browser）
# 用法: ./web-read.sh "https://example.com"

set -euo pipefail

URL="${1:?Usage: web-read.sh \"url\"}"

# Layer 1: opencli web read (Cookie 零配置)
opencli_exit=0
result=$(opencli web read --url "$URL" -f md 2>&1) || opencli_exit=$?
if [ -n "$result" ] && [ ${#result} -gt 200 ] && ! echo "$result" | grep -qiE "error|failed|exit code"; then
    echo "$result"
    exit 0
fi
# exit 77 = SSO/Cookie 过期，后续层也没有登录态，直接 bail out
if [ "$opencli_exit" -eq 77 ]; then
    echo "# [web-read] SSO/Cookie expired (exit 77). Please re-login in Chrome, then retry."
    echo "# 后续工具 (firecrawl/agent-browser) 也没有登录态，跳过降级。"
    exit 77
fi
echo "# [web-read] opencli web read failed (exit $opencli_exit), trying firecrawl..." >&2

# Layer 2: Firecrawl (JS 渲染 + 结构化提取)
if command -v firecrawl &>/dev/null && [ -n "${FIRECRAWL_API_KEY:-}" ]; then
    fc_result=$(firecrawl scrape "$URL" 2>&1) || true
    if [ -n "$fc_result" ] && [ ${#fc_result} -gt 200 ]; then
        echo "$fc_result"
        exit 0
    fi
    echo "# [web-read] firecrawl failed, trying agent-browser..." >&2
else
    echo "# [web-read] firecrawl not available, trying agent-browser..." >&2
fi

# Layer 3: agent-browser snapshot
if command -v agent-browser &>/dev/null; then
    agent-browser --auto-connect open "$URL" 2>/dev/null || true
    sleep 2
    snapshot=$(agent-browser snapshot -i 2>&1) || true
    agent-browser close 2>/dev/null || true
    if [ -n "$snapshot" ] && [ ${#snapshot} -gt 100 ]; then
        echo "$snapshot"
        exit 0
    fi
fi

echo "# [web-read] ALL LAYERS FAILED for url: $URL"
echo "# Tried: opencli web read, firecrawl, agent-browser"
exit 1
