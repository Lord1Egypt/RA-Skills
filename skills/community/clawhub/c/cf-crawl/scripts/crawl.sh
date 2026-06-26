#!/usr/bin/env bash
# cf-crawl: Start a Cloudflare crawl job and poll for results
# Usage: crawl.sh <url> [options]
#   --limit N        Max pages (default 10, max 100000)
#   --depth N        Max link depth (default 10)
#   --format FMT     markdown|html|json (default markdown)
#   --render         Enable JS rendering (default: false/fast fetch)
#   --include PAT    Include URL pattern (repeatable)
#   --exclude PAT    Exclude URL pattern (repeatable)
#   --external       Follow external links
#   --subdomains     Follow subdomain links
#   --source SRC     all|sitemaps|links (default all)
#   --max-age SEC    Cache max age in seconds (default 86400)
#   --json-prompt P  Prompt for JSON AI extraction (requires --format json)
#   --json-schema F  Path to JSON schema file (requires --format json)
#   --poll-interval  Seconds between polls (default 5)
#   --timeout SEC    Max seconds to wait (default 300)
#   --output FILE    Write results to file (default stdout)
#   --raw            Output raw API response (no formatting)
#   --start-only     Start job, print ID, don't poll

set -euo pipefail

# Load credentials
if [[ -f ~/.clawdbot/secrets/cloudflare-crawl.env ]]; then
  source ~/.clawdbot/secrets/cloudflare-crawl.env
fi
: "${CF_ACCOUNT_ID:?Set CF_ACCOUNT_ID}"
: "${CF_CRAWL_API_TOKEN:?Set CF_CRAWL_API_TOKEN}"

BASE="https://api.cloudflare.com/client/v4/accounts/${CF_ACCOUNT_ID}/browser-rendering/crawl"

# Defaults
LIMIT=10
DEPTH=10
FORMAT="markdown"
RENDER=false
INCLUDES=()
EXCLUDES=()
EXTERNAL=false
SUBDOMAINS=false
SOURCE="all"
MAX_AGE=86400
JSON_PROMPT=""
JSON_SCHEMA=""
POLL_INTERVAL=5
TIMEOUT=300
OUTPUT=""
RAW=false
START_ONLY=false
URL=""

# Parse args
while [[ $# -gt 0 ]]; do
  case "$1" in
    --limit) LIMIT="$2"; shift 2;;
    --depth) DEPTH="$2"; shift 2;;
    --format) FORMAT="$2"; shift 2;;
    --render) RENDER=true; shift;;
    --include) INCLUDES+=("$2"); shift 2;;
    --exclude) EXCLUDES+=("$2"); shift 2;;
    --external) EXTERNAL=true; shift;;
    --subdomains) SUBDOMAINS=true; shift;;
    --source) SOURCE="$2"; shift 2;;
    --max-age) MAX_AGE="$2"; shift 2;;
    --json-prompt) JSON_PROMPT="$2"; shift 2;;
    --json-schema) JSON_SCHEMA="$2"; shift 2;;
    --poll-interval) POLL_INTERVAL="$2"; shift 2;;
    --timeout) TIMEOUT="$2"; shift 2;;
    --output) OUTPUT="$2"; shift 2;;
    --raw) RAW=true; shift;;
    --start-only) START_ONLY=true; shift;;
    -*) echo "Unknown option: $1" >&2; exit 1;;
    *) URL="$1"; shift;;
  esac
done

[[ -z "$URL" ]] && { echo "Usage: crawl.sh <url> [options]" >&2; exit 1; }

# Build JSON body
BODY=$(jq -n \
  --arg url "$URL" \
  --argjson limit "$LIMIT" \
  --argjson depth "$DEPTH" \
  --argjson render "$RENDER" \
  --arg source "$SOURCE" \
  --argjson maxAge "$MAX_AGE" \
  --argjson external "$EXTERNAL" \
  --argjson subdomains "$SUBDOMAINS" \
  '{
    url: $url,
    limit: $limit,
    depth: $depth,
    render: $render,
    source: $source,
    maxAge: $maxAge,
    formats: [],
    options: {
      includeExternalLinks: $external,
      includeSubdomains: $subdomains
    }
  }')

# Set format
BODY=$(echo "$BODY" | jq --arg fmt "$FORMAT" '.formats = [$fmt]')

# Add include/exclude patterns
for p in "${INCLUDES[@]+"${INCLUDES[@]}"}"; do
  BODY=$(echo "$BODY" | jq --arg p "$p" '.options.includePatterns += [$p]')
done
for p in "${EXCLUDES[@]+"${EXCLUDES[@]}"}"; do
  BODY=$(echo "$BODY" | jq --arg p "$p" '.options.excludePatterns += [$p]')
done

# Add JSON options if format is json
if [[ "$FORMAT" == "json" ]]; then
  if [[ -n "$JSON_PROMPT" ]]; then
    JSON_OPTS=$(jq -n --arg prompt "$JSON_PROMPT" '{prompt: $prompt}')
    if [[ -n "$JSON_SCHEMA" && -f "$JSON_SCHEMA" ]]; then
      JSON_OPTS=$(echo "$JSON_OPTS" | jq --slurpfile schema "$JSON_SCHEMA" '.response_format = {type: "json_schema", json_schema: $schema[0]}')
    fi
    BODY=$(echo "$BODY" | jq --argjson jo "$JSON_OPTS" '.jsonOptions = $jo')
  fi
fi

# Start crawl
RESPONSE=$(curl -s -X POST "$BASE" \
  -H "Authorization: Bearer $CF_CRAWL_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d "$BODY")

SUCCESS=$(echo "$RESPONSE" | jq -r '.success')
if [[ "$SUCCESS" != "true" ]]; then
  echo "Error starting crawl:" >&2
  echo "$RESPONSE" | jq . >&2
  exit 1
fi

JOB_ID=$(echo "$RESPONSE" | jq -r '.result')
echo "Crawl started: $JOB_ID" >&2

if [[ "$START_ONLY" == "true" ]]; then
  echo "$JOB_ID"
  exit 0
fi

# Poll for results
ELAPSED=0
while [[ $ELAPSED -lt $TIMEOUT ]]; do
  sleep "$POLL_INTERVAL"
  ELAPSED=$((ELAPSED + POLL_INTERVAL))

  RESULT=$(curl -s "$BASE/$JOB_ID" \
    -H "Authorization: Bearer $CF_CRAWL_API_TOKEN")

  STATUS=$(echo "$RESULT" | jq -r '.result.status // "unknown"')
  FINISHED=$(echo "$RESULT" | jq -r '.result.finished // 0')
  TOTAL=$(echo "$RESULT" | jq -r '.result.total // 0')

  echo "[$ELAPSED/${TIMEOUT}s] Status: $STATUS ($FINISHED/$TOTAL pages)" >&2

  if [[ "$STATUS" != "running" ]]; then
    break
  fi
done

if [[ "$STATUS" == "running" ]]; then
  echo "Timeout after ${TIMEOUT}s. Job still running: $JOB_ID" >&2
  echo "Poll later: curl -s '$BASE/$JOB_ID' -H 'Authorization: Bearer \$CF_CRAWL_API_TOKEN'" >&2
  exit 2
fi

# Fetch all results (handle pagination)
ALL_RECORDS="[]"
CURSOR=""
while true; do
  QUERY="?status=completed"
  [[ -n "$CURSOR" ]] && QUERY="${QUERY}&cursor=${CURSOR}"

  PAGE=$(curl -s "$BASE/$JOB_ID$QUERY" \
    -H "Authorization: Bearer $CF_CRAWL_API_TOKEN")

  RECORDS=$(echo "$PAGE" | jq '.result.records // []')
  ALL_RECORDS=$(echo "$ALL_RECORDS" "$RECORDS" | jq -s '.[0] + .[1]')

  NEXT_CURSOR=$(echo "$PAGE" | jq -r '.result.cursor // empty')
  if [[ -z "$NEXT_CURSOR" || "$NEXT_CURSOR" == "null" ]]; then
    break
  fi
  CURSOR="$NEXT_CURSOR"
done

# Build final output
FINAL=$(echo "$RESULT" | jq --argjson records "$ALL_RECORDS" '.result.records = $records')

if [[ "$RAW" == "true" ]]; then
  OUT="$FINAL"
else
  # Formatted summary
  OUT=$(echo "$FINAL" | jq '{
    job_id: .result.id,
    status: .result.status,
    browser_seconds: .result.browserSecondsUsed,
    total_pages: .result.total,
    completed_pages: .result.finished,
    pages: [.result.records[] | {
      url: .url,
      title: .metadata.title,
      status: .status,
      content_length: ((.markdown // .html // "") | length),
      json: .json
    }]
  }')
fi

if [[ -n "$OUTPUT" ]]; then
  echo "$FINAL" > "$OUTPUT"
  echo "Results written to $OUTPUT" >&2
  echo "$OUT"
else
  echo "$OUT"
fi
