#!/usr/bin/env bash
# stats.sh — Get Ghost site stats (posts, members, and pageviews if available)
# Usage: stats.sh [--format json|table]

set -euo pipefail

GHOST_URL="${GHOST_URL:-}"
ADMIN_API_KEY="${GHOST_ADMIN_API_KEY:-}"
FORMAT="json"

usage() {
  cat <<EOF
Usage: stats.sh [options]
Options:
  --format     Output format: json, table (default: json)
  --ghost-url  Ghost site URL (env: GHOST_URL)
  --api-key    Admin API key (env: GHOST_ADMIN_API_KEY)
EOF
  exit 1
}

while [[ $# -gt 0 ]]; do
  case "$1" in
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

KEY="${ADMIN_API_KEY##*:}"

# Fetch posts count
POSTS_RESPONSE=$(curl -s -w "\n%{http_code}" \
  -H "Authorization: Ghost ${KEY}" \
  -H "Content-Type: application/json" \
  "${GHOST_URL}/ghost/api/admin/posts/?limit=1&include=tags,authors")

POSTS_HTTP=$(echo "$POSTS_RESPONSE" | tail -1)
POSTS_BODY=$(echo "$POSTS_RESPONSE" | sed '$d')

# Fetch members
MEMBERS_RESPONSE=$(curl -s -w "\n%{http_code}" \
  -H "Authorization: Ghost ${KEY}" \
  -H "Content-Type: application/json" \
  "${GHOST_URL}/ghost/api/admin/members/?limit=1")

MEMBERS_HTTP=$(echo "$MEMBERS_RESPONSE" | tail -1)
MEMBERS_BODY=$(echo "$MEMBERS_RESPONSE" | sed '$d')

# Fetch site
SITE_RESPONSE=$(curl -s -w "\n%{http_code}" \
  -H "Authorization: Ghost ${KEY}" \
  -H "Content-Type: application/json" \
  "${GHOST_URL}/ghost/api/admin/site/")

SITE_HTTP=$(echo "$SITE_RESPONSE" | tail -1)
SITE_BODY=$(echo "$SITE_RESPONSE" | sed '$d')

if [[ "$POSTS_HTTP" != "200" ]]; then
  echo "Error fetching posts (HTTP $POSTS_HTTP): $POSTS_BODY" >&2
  exit 1
fi

if [[ "$FORMAT" == "table" ]]; then
  TOTAL_POSTS=$(echo "$POSTS_BODY" | jq -r '.meta.pagination.total // 0')
  PUBLISHED=$(echo "$POSTS_BODY" | jq -r '[.posts[] | select(.status == "published")] | length')
  DRAFTS=$(echo "$POSTS_BODY" | jq -r '[.posts[] | select(.status == "draft")] | length')

  TOTAL_MEMBERS=$(echo "$MEMBERS_BODY" | jq -r '.meta.pagination.total // 0')
  PAID_MEMBERS=$(echo "$MEMBERS_BODY" | jq -r '[.members[] | select(.subscribed == true)] | length')

  echo "Ghost Site Statistics"
  echo "===================="
  echo ""
  echo "Posts:"
  echo "  Total:    $TOTAL_POSTS"
  echo "  Published: $PUBLISHED"
  echo "  Drafts:   $DRAFTS"
  echo ""
  echo "Members:"
  echo "  Total:    $TOTAL_MEMBERS"
  echo "  Paid:     $PAID_MEMBERS"
else
  # Build combined JSON output
  jq -n \
    --argjson posts_total "$(echo "$POSTS_BODY" | jq '.meta.pagination.total // 0')" \
    --argjson posts_published "$(echo "$POSTS_BODY" | jq '[.posts[] | select(.status == "published")] | length')" \
    --argjson posts_draft "$(echo "$POSTS_BODY" | jq '[.posts[] | select(.status == "draft")] | length')" \
    --argjson members_total "$(echo "$MEMBERS_BODY" | jq '.meta.pagination.total // 0')" \
    --argjson members_paid "$(echo "$MEMBERS_BODY" | jq '[.members[] | select(.subscribed == true)] | length')" \
    '{
      posts: {
        total: $posts_total,
        published: $posts_published,
        draft: $posts_draft
      },
      members: {
        total: $members_total,
        paid: $members_paid
      }
    }' 
fi
