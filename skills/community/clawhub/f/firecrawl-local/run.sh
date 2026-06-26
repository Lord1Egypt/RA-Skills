#!/bin/bash
# Firecrawl Local Skill — run.sh
# Uses Firecrawl v1 REST API against a self-hosted instance.
# Prerequisites: curl, jq

set -euo pipefail

LOCAL_URL="${FIRECRAWL_LOCAL_URL:-http://localhost:3002}"
API_KEY="${FIRECRAWL_API_KEY:-}"

# ── helpers ──────────────────────────────────────────────────────────────────

usage() {
  echo "Usage:"
  echo "  firecrawl-local <url>                      # scrape (default)"
  echo "  firecrawl-local map <url> [--limit N]"
  echo "  firecrawl-local scrape <url> [--formats markdown,html]"
  echo "  firecrawl-local crawl <url> [--limit N] [--max-depth N] [--include /path] [--exclude /path]"
  exit 1
}

auth_header() {
  if [ -n "$API_KEY" ]; then
    echo "-H" "Authorization: Bearer $API_KEY"
  fi
}

api_call() {
  local method="$1" endpoint="$2" body="$3"
  curl -s -X "$method" \
    "$LOCAL_URL$endpoint" \
    -H "Content-Type: application/json" \
    $(auth_header) \
    -d "$body"
}

# ── connectivity check ────────────────────────────────────────────────────────

if ! curl -s --max-time 3 -f "$LOCAL_URL/health" >/dev/null 2>&1; then
  echo "❌ Local Firecrawl at $LOCAL_URL is not reachable."
  echo "   Start your Firecrawl instance and try again."
  exit 1
fi

echo "✅ Connected to Firecrawl at $LOCAL_URL"

# ── argument parsing ──────────────────────────────────────────────────────────

[ $# -lt 1 ] && usage

# Support both:
#   firecrawl-local https://example.com          → scrape (default)
#   firecrawl-local scrape https://example.com   → explicit scrape
#   firecrawl-local map https://example.com      → map
#   firecrawl-local crawl https://example.com    → crawl
case "$1" in
  map|scrape|crawl)
    ACTION="$1"; shift
    [ $# -lt 1 ] && usage
    TARGET_URL="$1"; shift
    ;;
  http://*|https://*)
    ACTION="scrape"
    TARGET_URL="$1"; shift
    ;;
  *)
    echo "❌ Expected a URL or subcommand (map|scrape|crawl), got: $1"
    usage
    ;;
esac

# Defaults
LIMIT=50
MAX_DEPTH=2
INCLUDE_PATH=""
EXCLUDE_PATH=""
FORMATS="markdown"

while [ $# -gt 0 ]; do
  case "$1" in
    --limit)    LIMIT="$2";        shift 2 ;;
    --max-depth) MAX_DEPTH="$2";   shift 2 ;;
    --include)  INCLUDE_PATH="$2"; shift 2 ;;
    --exclude)  EXCLUDE_PATH="$2"; shift 2 ;;
    --formats)  FORMATS="$2";      shift 2 ;;
    *) echo "Unknown option: $1"; usage ;;
  esac
done

# ── map ───────────────────────────────────────────────────────────────────────

if [ "$ACTION" = "map" ]; then
  BODY=$(jq -n \
    --arg url "$TARGET_URL" \
    --argjson limit "$LIMIT" \
    '{url: $url, limit: $limit}')

  echo "🗺  Mapping $TARGET_URL (limit: $LIMIT)..."
  api_call POST /v1/map "$BODY" | jq '.'

# ── scrape ────────────────────────────────────────────────────────────────────

elif [ "$ACTION" = "scrape" ]; then
  # Convert comma-separated formats string to JSON array
  FORMATS_JSON=$(echo "$FORMATS" | jq -Rc 'split(",")')

  BODY=$(jq -n \
    --arg url "$TARGET_URL" \
    --argjson formats "$FORMATS_JSON" \
    '{url: $url, formats: $formats}')

  echo "📄 Scraping $TARGET_URL (formats: $FORMATS)..."
  api_call POST /v1/scrape "$BODY" | jq '.'

# ── crawl (async with polling) ────────────────────────────────────────────────

elif [ "$ACTION" = "crawl" ]; then
  # Build crawl options — only add optional fields if set
  CRAWL_OPTS=$(jq -n \
    --argjson maxDepth "$MAX_DEPTH" \
    --arg includePath "$INCLUDE_PATH" \
    --arg excludePath "$EXCLUDE_PATH" \
    '{
      maxDepth: $maxDepth,
      includePaths: (if $includePath != "" then [$includePath] else [] end),
      excludePaths: (if $excludePath != "" then [$excludePath] else [] end)
    }')

  BODY=$(jq -n \
    --arg url "$TARGET_URL" \
    --argjson limit "$LIMIT" \
    --argjson opts "$CRAWL_OPTS" \
    '{url: $url, limit: $limit, crawlerOptions: $opts}')

  echo "🕷  Starting crawl of $TARGET_URL (limit: $LIMIT, max-depth: $MAX_DEPTH)..."
  RESPONSE=$(api_call POST /v1/crawl "$BODY")

  JOB_ID=$(echo "$RESPONSE" | jq -r '.id // empty')
  if [ -z "$JOB_ID" ]; then
    echo "❌ Crawl failed to start:"
    echo "$RESPONSE" | jq '.'
    exit 1
  fi

  echo "⏳ Crawl job started (id: $JOB_ID) — polling for results..."

  # Poll until complete (max 5 minutes, 5s interval)
  MAX_ATTEMPTS=60
  ATTEMPT=0
  while [ $ATTEMPT -lt $MAX_ATTEMPTS ]; do
    sleep 5
    STATUS_RESP=$(api_call GET "/v1/crawl/$JOB_ID" "")
    STATUS=$(echo "$STATUS_RESP" | jq -r '.status // "unknown"')
    COMPLETED=$(echo "$STATUS_RESP" | jq -r '.completed // 0')
    TOTAL=$(echo "$STATUS_RESP" | jq -r '.total // "?"')

    echo "   [$((ATTEMPT+1))/$MAX_ATTEMPTS] status: $STATUS ($COMPLETED/$TOTAL pages)"

    if [ "$STATUS" = "completed" ]; then
      echo "✅ Crawl complete — $COMPLETED pages"
      echo "$STATUS_RESP" | jq '.data'
      exit 0
    elif [ "$STATUS" = "failed" ]; then
      echo "❌ Crawl failed:"
      echo "$STATUS_RESP" | jq '.'
      exit 1
    fi

    ATTEMPT=$((ATTEMPT + 1))
  done

  echo "⚠️  Timed out waiting for crawl. Job ID: $JOB_ID"
  echo "   Check manually: curl $LOCAL_URL/v1/crawl/$JOB_ID | jq '.'"
  exit 1

else
  echo "❌ Unknown action: $ACTION"
  usage
fi
