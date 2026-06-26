#!/usr/bin/env bash
# tags.sh — List, create, and get Ghost tags via the Admin API
# Usage: tags.sh --list [--limit 20]
#   or:  tags.sh --create --name "Tag Name" [--description "..."] [--slug "tag-slug"]
#   or:  tags.sh --slug "tag-slug"

set -euo pipefail

GHOST_URL="${GHOST_URL:-}"
ADMIN_API_KEY="${GHOST_ADMIN_API_KEY:-}"
ACTION="list"
LIMIT="20"
NAME=""
DESCRIPTION=""
SLUG=""
FORMAT="json"

usage() {
  cat <<EOF
Usage: tags.sh [options]
Actions:
  --list              List all tags (default)
  --create            Create a new tag
  --slug              Get tag by slug
Options:
  --limit    Number of tags for --list (default: 20)
  --name     Tag name (required for --create)
  --description  Tag description (optional for --create)
  --slug     Tag slug (optional for --create, auto-generated if omitted)
  --format   Output format: json, table (default: json)
  --ghost-url  Ghost site URL (env: GHOST_URL)
  --api-key    Admin API key (env: GHOST_ADMIN_API_KEY)
EOF
  exit 1
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --list) ACTION="list"; shift ;;
    --create) ACTION="create"; shift ;;
    --slug)
      ACTION="get"
      SLUG="${2:-}"
      shift 2
      ;;
    --limit) LIMIT="${2:-}"; shift 2 ;;
    --name) NAME="${2:-}"; shift 2 ;;
    --description) DESCRIPTION="${2:-}"; shift 2 ;;
    --slug-only) SLUG="${2:-}"; shift 2 ;;
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

case "$ACTION" in
  list)
    RESPONSE=$(curl -s -w "\n%{http_code}" \
      -H "Authorization: Ghost ${KEY}" \
      -H "Content-Type: application/json" \
      "${GHOST_URL}/ghost/api/admin/tags/?limit=${LIMIT}&include=count.posts")

    HTTP_CODE=$(echo "$RESPONSE" | tail -1)
    BODY=$(echo "$RESPONSE" | sed '$d')

    if [[ "$HTTP_CODE" != "200" ]]; then
      echo "Error listing tags (HTTP $HTTP_CODE): $BODY" >&2
      exit 1
    fi

    if [[ "$FORMAT" == "table" ]]; then
      echo "$BODY" | jq -r '.tags[] | "\(.slug)\t\(.name)\t\(.count.posts) posts\t\(.description // "")"' | \
        column -t -s $'\t' -N SLUG,NAME,POSTS,DESCRIPTION
    else
      echo "$BODY" | jq .
    fi
    ;;

  get)
    if [[ -z "$SLUG" ]]; then
      echo "Error: --slug is required for --get action" >&2
      exit 1
    fi

    RESPONSE=$(curl -s -w "\n%{http_code}" \
      -H "Authorization: Ghost ${KEY}" \
      -H "Content-Type: application/json" \
      "${GHOST_URL}/ghost/api/admin/tags/slug/${SLUG}/?include=count.posts")

    HTTP_CODE=$(echo "$RESPONSE" | tail -1)
    BODY=$(echo "$RESPONSE" | sed '$d')

    if [[ "$HTTP_CODE" != "200" ]]; then
      echo "Error fetching tag (HTTP $HTTP_CODE): $BODY" >&2
      exit 1
    fi

    echo "$BODY" | jq .
    ;;

  create)
    if [[ -z "$NAME" ]]; then
      echo "Error: --name is required for --create" >&2
      exit 1
    fi

    # Auto-generate slug if not provided
    if [[ -z "$SLUG" ]]; then
      SLUG=$(echo "$NAME" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9-')
    fi

    TAG_JSON=$(jq -n \
      --arg name "$NAME" \
      --arg desc "$DESCRIPTION" \
      --arg slug "$SLUG" \
      '{
        tags: [{
          name: $name,
          description: (if $desc != "" then $desc else null end),
          slug: $slug
        }]
      }')

    RESPONSE=$(curl -s -w "\n%{http_code}" -X POST \
      -H "Authorization: Ghost ${KEY}" \
      -H "Content-Type: application/json" \
      -d "$TAG_JSON" \
      "${GHOST_URL}/ghost/api/admin/tags/")

    HTTP_CODE=$(echo "$RESPONSE" | tail -1)
    BODY=$(echo "$RESPONSE" | sed '$d')

    if [[ "$HTTP_CODE" != "201" ]] && [[ "$HTTP_CODE" != "200" ]]; then
      echo "Error creating tag (HTTP $HTTP_CODE): $BODY" >&2
      exit 1
    fi

    echo "$BODY" | jq -r '.tags[0] | "Created tag: \(.name) (slug: \(.slug), ID: \(.id))"'
    echo ""
    echo "$BODY" | jq .
    ;;
esac
