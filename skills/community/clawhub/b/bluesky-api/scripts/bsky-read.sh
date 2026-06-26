#!/usr/bin/env bash
set -euo pipefail

# Fetch recent posts from a Bluesky profile (public, no auth needed)
# Usage: bsky-read.sh <handle> [limit]

HANDLE="${1:-}"
LIMIT="${2:-10}"

if [ -z "$HANDLE" ]; then
  echo "Usage: bsky-read.sh <handle> [limit]" >&2
  echo "  handle  — Bluesky handle (e.g. alice.bsky.social)" >&2
  echo "  limit   — number of posts to fetch (default: 10, max: 100)" >&2
  exit 1
fi

# Validate limit is a positive integer to prevent URL injection
if ! [[ "$LIMIT" =~ ^[0-9]+$ ]] || [ "$LIMIT" -lt 1 ] || [ "$LIMIT" -gt 100 ]; then
  echo "Error: limit must be an integer between 1 and 100" >&2
  exit 1
fi

API_URL="https://public.api.bsky.app/xrpc/app.bsky.feed.getAuthorFeed?actor=$(printf '%s' "$HANDLE" | jq -sRr @uri)&limit=${LIMIT}"

RESPONSE=$(curl -sf "$API_URL") || {
  echo "Error: failed to fetch feed for '${HANDLE}'" >&2
  exit 1
}

echo "$RESPONSE" | jq '.feed[] | {
  text: .post.record.text,
  createdAt: .post.record.createdAt,
  uri: .post.uri,
  author: .post.author.handle,
  likes: .post.likeCount,
  reposts: .post.repostCount,
  replies: .post.replyCount
}'
