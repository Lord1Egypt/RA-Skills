#!/bin/bash
# web-trending.sh — 热榜降级链（opencli <platform> → agent-browser）
# 用法: ./web-trending.sh <platform> [limit]
# 支持平台: twitter, zhihu, hackernews, bilibili, weibo, lobsters, producthunt, reddit

set -euo pipefail

PLATFORM="${1:?Usage: web-trending.sh <platform> [limit]}"
LIMIT="${2:-10}"

# 平台 → 命令映射
case "$PLATFORM" in
    twitter)    CMD="opencli twitter trending --limit $LIMIT -f md" ; URL="https://x.com/explore/tabs/trending" ;;
    zhihu)      CMD="opencli zhihu hot --limit $LIMIT -f md"       ; URL="https://www.zhihu.com/hot" ;;
    hackernews) CMD="opencli hackernews top --limit $LIMIT -f md"  ; URL="https://news.ycombinator.com" ;;
    bilibili)   CMD="opencli bilibili hot --limit $LIMIT -f md"    ; URL="https://www.bilibili.com/v/popular/rank/all" ;;
    weibo)      CMD="opencli weibo hot --limit $LIMIT -f md"       ; URL="https://s.weibo.com/top/summary" ;;
    lobsters)   CMD="opencli lobsters hot --limit $LIMIT -f md"    ; URL="https://lobste.rs" ;;
    producthunt) CMD="opencli producthunt today --limit $LIMIT -f md" ; URL="https://www.producthunt.com" ;;
    reddit)     CMD="opencli reddit hot --limit $LIMIT -f md"      ; URL="https://www.reddit.com/r/popular" ;;
    *)          echo "# Unknown platform: $PLATFORM"; echo "# Supported: twitter zhihu hackernews bilibili weibo lobsters producthunt reddit"; exit 1 ;;
esac

# Layer 1: opencli
result=$(eval "$CMD" 2>&1) || true
if [ -n "$result" ] && [ ${#result} -gt 50 ] && ! echo "$result" | grep -qiE "error|unexpected|exit code|no.*result"; then
    echo "$result"
    exit 0
fi
echo "# [web-trending] opencli $PLATFORM failed, trying agent-browser..." >&2

# Layer 2: agent-browser
agent-browser --auto-connect open "$URL" 2>/dev/null || true
sleep 3
snapshot=$(agent-browser snapshot -i 2>&1) || true
if [ -n "$snapshot" ] && [ ${#snapshot} -gt 100 ]; then
    echo "$snapshot"
    exit 0
fi

echo "# [web-trending] ALL LAYERS FAILED for platform: $PLATFORM"
echo "# Tried: opencli $PLATFORM, agent-browser $URL"
exit 1
