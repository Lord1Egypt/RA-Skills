#!/usr/bin/env bash
set -euo pipefail

# Search Bluesky posts by keyword (public, no auth needed)
# Usage: bsky-search.sh <query> [limit]

QUERY="${1:-}"
LIMIT="${2:-25}"

if [ -z "$QUERY" ]; then
  echo "Usage: bsky-search.sh <query> [limit]" >&2
  echo "  query  — search terms (keywords, hashtags, phrases)" >&2
  echo "  limit  — number of results (default: 25, max: 100)" >&2
  exit 1
fi

# Validate limit is a positive integer to prevent URL injection
if ! [[ "$LIMIT" =~ ^[0-9]+$ ]] || [ "$LIMIT" -lt 1 ] || [ "$LIMIT" -gt 100 ]; then
  echo "Error: limit must be an integer between 1 and 100" >&2
  exit 1
fi

API_URL="https://public.api.bsky.app/xrpc/app.bsky.feed.searchPosts?q=$(printf '%s' "$QUERY" | jq -sRr @uri)&limit=${LIMIT}"

RESPONSE=$(curl -sf "$API_URL") || {
  echo "Error: search failed for query '${QUERY}'" >&2
  exit 1
}

echo "$RESPONSE" | jq '.posts[] | {
  text: .record.text,
  author: .author.handle,
  createdAt: .record.createdAt,
  uri: .uri
}'
