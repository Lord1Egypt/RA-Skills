#!/usr/bin/env bash
set -euo pipefail

# Load API key
if [ -z "${ARENA_API_KEY:-}" ]; then
  if [ -f "$HOME/clawd/.env" ]; then
    ARENA_API_KEY=$(grep '^ARENA_API_KEY=' "$HOME/clawd/.env" | cut -d= -f2-)
  fi
fi

if [ -z "${ARENA_API_KEY:-}" ]; then
  echo "Error: ARENA_API_KEY not set" >&2
  exit 1
fi

BASE="https://api.starsarena.com"
AGENT_ID="7d511cd6-ee53-45f5-bc8e-f3ae16c33a08"

api() {
  local method="$1" path="$2" data="${3:-}"
  local args=(-s -X "$method" "$BASE$path" -H "X-API-Key: $ARENA_API_KEY" -H "Content-Type: application/json")
  [ -n "$data" ] && args+=(-d "$data")
  local resp
  resp=$(curl "${args[@]}" 2>&1) || { echo "Error: curl failed: $resp" >&2; exit 1; }
  echo "$resp" | python3 -m json.tool 2>/dev/null || echo "$resp"
}

cmd="${1:-help}"
shift || true

case "$cmd" in
  post)
    api POST /agents/threads "{\"content\":$(printf '%s' "$1" | python3 -c 'import sys,json;print(json.dumps(sys.stdin.read()))'),\"privacyType\":0}"
    ;;
  reply)
    threadId="$1"; shift
    api POST /agents/threads/answer "{\"threadId\":\"$threadId\",\"userId\":\"$AGENT_ID\",\"content\":$(printf '%s' "$1" | python3 -c 'import sys,json;print(json.dumps(sys.stdin.read()))')}"
    ;;
  like)
    api POST /agents/threads/like "{\"threadId\":\"$1\"}"
    ;;
  repost)
    api POST /agents/threads/repost "{\"threadId\":\"$1\"}"
    ;;
  quote)
    threadId="$1"; shift
    api POST /agents/threads/quote "{\"content\":$(printf '%s' "$1" | python3 -c 'import sys,json;print(json.dumps(sys.stdin.read()))'),\"quotedThreadId\":\"$threadId\"}"
    ;;
  follow)
    api POST /agents/follow/follow "{\"userId\":\"$1\"}"
    ;;
  feed)
    api GET "/agents/threads/feed/my?page=${1:-1}"
    ;;
  trending)
    api GET "/agents/threads/feed/trendingPosts?page=${1:-1}"
    ;;
  notifications)
    api GET "/agents/notifications?page=${1:-1}"
    ;;
  dm)
    groupId="$1"; shift
    api POST /agents/chat/send "{\"groupId\":\"$groupId\",\"content\":$(printf '%s' "$1" | python3 -c 'import sys,json;print(json.dumps(sys.stdin.read()))')}"
    ;;
  conversations)
    api GET "/agents/chat/conversations?page=${1:-1}"
    ;;
  search)
    api GET "/agents/user/search?searchString=$(python3 -c "import urllib.parse;print(urllib.parse.quote('$1'))")"
    ;;
  profile)
    api GET /agents/user/me
    ;;
  update-profile)
    api PATCH /agents/user/profile "$1"
    ;;
  user)
    api GET "/agents/user/search?searchString=$1"
    ;;
  help)
    echo "Usage: arena.sh <command> [args]"
    echo "Commands: post, reply, like, repost, quote, follow, feed, trending,"
    echo "          notifications, dm, conversations, search, profile, update-profile, user"
    ;;
  *)
    echo "Unknown command: $cmd" >&2; exit 1
    ;;
esac
