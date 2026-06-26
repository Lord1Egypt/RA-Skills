#!/usr/bin/env bash
# posts.sh — List Ghost posts via the Admin API
# Usage: posts.sh [--limit 10] [--page 1] [--status published] [--format json|table]

set -euo pipefail

GHOST_URL="${GHOST_URL:-}"
ADMIN_API_KEY="${GHOST_ADMIN_API_KEY:-}"
LIMIT="10"
PAGE="1"
STATUS="published"
FORMAT="json"

usage() {
  cat <<EOF
Usage: posts.sh [options]
Options:
  --limit    Number of posts (default: 10)
  --page     Page number (default: 1)
  --status   Status filter: published, draft, scheduled, all (default: published)
  --format   Output format: json, table (default: json)
  --ghost-url  Ghost site URL (env: GHOST_URL)
  --api-key    Admin API key (env: GHOST_ADMIN_API_KEY)
EOF
  exit 1
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --limit) LIMIT="${2:-}"; shift 2 ;;
    --page) PAGE="${2:-}"; shift 2 ;;
    --status) STATUS="${2:-}"; shift 2 ;;
    --format) FORMAT="${2:-}"; shift 2 ;;
    --ghost-url) GHOST_URL="${2:-}"; shift 2 ;;
    --api-key) ADMIN_API_KEY="${2:-}"; shift 2 ;;
    -h|--help) usage ;;
    *) echo "Unknown option: $1"; usage ;;
  esac
done

if [[ -z "$GHOST_URL" ]]; then
  echo "Error: --ghost-url or GHOST_URL is required" >&2
  exit 1
fi

if [[ -z "$ADMIN_API_KEY" ]]; then
  echo "Error: --api-key or GHOST_ADMIN_API_KEY is required" >&2
  exit 1
fi

# Extract actual key from id:key format
KEY="${ADMIN_API_KEY##*:}"

RESPONSE=$(curl -s -w "\n%{http_code}" \
  -H "Authorization: Ghost ${KEY}" \
  -H "Content-Type: application/json" \
  "${GHOST_URL}/ghost/api/admin/posts/?limit=${LIMIT}&page=${PAGE}&filter=status:${STATUS}&include=tags,authors")

HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [[ "$HTTP_CODE" != "200" ]]; then
  echo "Error fetching posts (HTTP $HTTP_CODE): $BODY" >&2
  exit 1
fi

if [[ "$FORMAT" == "table" ]]; then
  echo "$BODY" | jq -r '.posts[] | "\(.id)\t\(.title)\t\(.status)\t\(.published_at // "draft"}\t\(.visibility // "public")"' | \
    column -t -s $'\t' -N ID,TITLE,STATUS,PUBLISHED,VISIBILITY
else
  echo "$BODY" | jq .
fi
