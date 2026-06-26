#!/usr/bin/env bash
# new-post.sh — Create or publish a Ghost post via the Admin API
# Usage: new-post.sh --title "Title" --content "Markdown content" [--excerpt "..."] [--tags "news,updates"] [--publish] [--featured]

set -euo pipefail

GHOST_URL="${GHOST_URL:-}"
ADMIN_API_KEY="${GHOST_ADMIN_API_KEY:-}"
TITLE=""
CONTENT=""
EXCERPT=""
TAGS=""
PUBLISH="false"
FEATURED="false"
POST_ID=""

usage() {
  cat <<EOF
Usage: new-post.sh [options]
Options:
  --title     Post title (required)
  --content   Post content in Markdown (required)
  --excerpt   Short excerpt/summary (optional)
  --tags      Comma-separated tag names (optional)
  --publish   Publish immediately (omit for draft)
  --featured  Mark as featured (optional)
  --id        Update existing post by ID
  --ghost-url  Ghost site URL (env: GHOST_URL)
  --api-key    Admin API key (env: GHOST_ADMIN_API_KEY)
EOF
  exit 1
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --title) TITLE="${2:-}"; shift 2 ;;
    --content) CONTENT="${2:-}"; shift 2 ;;
    --excerpt) EXCERPT="${2:-}"; shift 2 ;;
    --tags) TAGS="${2:-}"; shift 2 ;;
    --publish) PUBLISH="true"; shift ;;
    --featured) FEATURED="true"; shift ;;
    --id) POST_ID="${2:-}"; shift 2 ;;
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

if [[ -z "$TITLE" ]] || [[ -z "$CONTENT" ]]; then
  echo "Error: --title and --content are required" >&2
  usage
fi

KEY="${ADMIN_API_KEY##*:}"

# Build post object
POST_JSON=$(jq -n \
  --arg title "$TITLE" \
  --arg content "$CONTENT" \
  --arg excerpt "$EXCERPT" \
  --arg publish "$PUBLISH" \
  --arg featured "$FEATURED" \
  '{
    posts: [{
      title: $title,
      html: null,
      markdown: $content,
      excerpt: (if $excerpt != "" then $excerpt else null end),
      status: (if $publish == "true" then "published" else "draft" end),
      featured: ($featured == "true")
    }]
  }')

# If tags provided, include them
if [[ -n "$TAGS" ]]; then
  TAGSLUGS=$(echo "$TAGS" | tr ',' '\n' | xargs -I{} echo "\"$(echo {} | xargs | tr ' ' '-' | tr '[:upper:]' '[:lower:]')\"" | tr '\n' ',' | sed 's/,$//')
  POST_JSON=$(echo "$POST_JSON" | jq --argjson tags "[$TAGSLUGS]" '.posts[0].tags = tags')
fi

# Determine endpoint
if [[ -n "$POST_ID" ]]; then
  ENDPOINT="${GHOST_URL}/ghost/api/admin/posts/${POST_ID}/"
  METHOD="PUT"
else
  ENDPOINT="${GHOST_URL}/ghost/api/admin/posts/"
  METHOD="POST"
fi

RESPONSE=$(curl -s -w "\n%{http_code}" -X "$METHOD" \
  -H "Authorization: Ghost ${KEY}" \
  -H "Content-Type: application/json" \
  -d "$POST_JSON" \
  "$ENDPOINT")

HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [[ "$HTTP_CODE" != "200" ]] && [[ "$HTTP_CODE" != "201" ]]; then
  echo "Error creating post (HTTP $HTTP_CODE): $BODY" >&2
  exit 1
fi

echo "$BODY" | jq -r '.posts[0] | "Created: \(.title) (ID: \(.id), Status: \(.status))"'
echo ""
echo "$BODY" | jq .
