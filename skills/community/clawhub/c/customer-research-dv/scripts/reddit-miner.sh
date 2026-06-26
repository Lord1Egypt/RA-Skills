#!/usr/bin/env bash
set -euo pipefail

# reddit-miner.sh — Mine Reddit threads for customer research
# Usage: ./reddit-miner.sh --subreddit SUBREDDIT --query "search terms" [--limit N] [--sentiment]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
DATA_DIR="$WORKSPACE_ROOT/data/research"
mkdir -p "$DATA_DIR"

# Defaults
SUBREDDIT=""
QUERY=""
LIMIT=50
SENTIMENT=false

# Parse args
while [[ $# -gt 0 ]]; do
  case $1 in
    --subreddit) SUBREDDIT="$2"; shift 2 ;;
    --query) QUERY="$2"; shift 2 ;;
    --limit) LIMIT="$2"; shift 2 ;;
    --sentiment) SENTIMENT=true; shift ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

if [[ -z "$SUBREDDIT" ]] || [[ -z "$QUERY" ]]; then
  echo "Usage: $0 --subreddit SUBREDDIT --query \"search terms\" [--limit N] [--sentiment]" >&2
  exit 1
fi

TIMESTAMP=$(date -u +"%Y%m%d-%H%M%S")
OUTPUT_FILE="$DATA_DIR/reddit-${SUBREDDIT}-${TIMESTAMP}.json"

echo "🔍 Mining r/$SUBREDDIT for: \"$QUERY\" (limit: $LIMIT)" >&2

# Fetch from Reddit JSON API (public, no auth required)
# Reddit JSON endpoint: https://www.reddit.com/r/{subreddit}/search.json?q={query}&limit={limit}&restrict_sr=on
URL="https://www.reddit.com/r/${SUBREDDIT}/search.json?q=$(printf %s "$QUERY" | jq -sRr @uri)&limit=${LIMIT}&restrict_sr=on&sort=relevance"

TEMP_JSON=$(mktemp)
trap 'rm -f "$TEMP_JSON"' EXIT

if ! curl -sL -A "OpenClaw/CustomerResearch (by /u/clawdiri)" "$URL" > "$TEMP_JSON"; then
  echo "❌ Failed to fetch Reddit data" >&2
  exit 1
fi

# Check if Reddit returned error
if jq -e '.error' "$TEMP_JSON" >/dev/null 2>&1; then
  echo "❌ Reddit API error:" >&2
  jq -r '.message // .error' "$TEMP_JSON" >&2
  exit 1
fi

# Extract threads
THREADS=$(jq -c '.data.children[] | select(.kind == "t3") | .data' "$TEMP_JSON")
THREAD_COUNT=$(echo "$THREADS" | wc -l | tr -d ' ')

echo "📊 Found $THREAD_COUNT threads" >&2

# Build findings array
FINDINGS='[]'
while IFS= read -r thread; do
  [[ -z "$thread" ]] && continue
  TITLE=$(echo "$thread" | jq -r '.title')
  SELFTEXT=$(echo "$thread" | jq -r '.selftext // ""')
  URL=$(echo "$thread" | jq -r '.permalink')
  SCORE=$(echo "$thread" | jq -r '.score')
  NUM_COMMENTS=$(echo "$thread" | jq -r '.num_comments')
  CREATED=$(echo "$thread" | jq -r '.created_utc')
  THREAD_ID=$(echo "$thread" | jq -r '.id')
  
  # Combine title + selftext for analysis
  FULL_TEXT="$TITLE. $SELFTEXT"
  
  # Sentiment analysis (if enabled)
  SENTIMENT_SCORE="null"
  if [[ "$SENTIMENT" == true ]]; then
    # Use OpenClaw LLM for sentiment (0 = very negative, 0.5 = neutral, 1 = very positive)
    # For now, placeholder — in production, call gemini or sonnet via openclaw CLI
    # SENTIMENT_SCORE=$(echo "$FULL_TEXT" | openclaw chat --model gemini-3-flash-preview --system "Rate sentiment 0-1. Output only number." --no-stream)
    SENTIMENT_SCORE=0.5  # Placeholder
  fi
  
  FINDING=$(jq -n \
    --arg source "reddit" \
    --arg source_id "r/$SUBREDDIT/comments/$THREAD_ID" \
    --arg text "$FULL_TEXT" \
    --argjson sentiment "$SENTIMENT_SCORE" \
    --arg url "https://www.reddit.com$URL" \
    --argjson score "$SCORE" \
    --argjson comments "$NUM_COMMENTS" \
    --argjson created "$CREATED" \
    '{
      source: $source,
      source_id: $source_id,
      text: $text,
      sentiment: $sentiment,
      themes: [],
      metadata: {
        url: $url,
        score: $score,
        num_comments: $comments,
        created_utc: $created
      }
    }')
  
  FINDINGS=$(echo "$FINDINGS" | jq --argjson finding "$FINDING" '. += [$finding]')
done <<< "$THREADS"

# Build summary
TOTAL_SOURCES=$(echo "$FINDINGS" | jq 'length')
AVG_SENTIMENT=$(echo "$FINDINGS" | jq '[.[].sentiment | select(. != null)] | if length > 0 then add / length else null end')

# Generate output JSON
jq -n \
  --arg skill "customer-research" \
  --arg script "reddit-miner" \
  --arg timestamp "$(date -u +"%Y-%m-%dT%H:%M:%SZ")" \
  --arg subreddit "$SUBREDDIT" \
  --arg query "$QUERY" \
  --argjson limit "$LIMIT" \
  --argjson findings "$FINDINGS" \
  --argjson total_sources "$TOTAL_SOURCES" \
  --argjson avg_sentiment "$AVG_SENTIMENT" \
  '{
    meta: {
      skill: $skill,
      script: $script,
      timestamp: $timestamp,
      query: {
        subreddit: $subreddit,
        query: $query,
        limit: $limit
      }
    },
    findings: $findings,
    summary: {
      total_sources: $total_sources,
      avg_sentiment: $avg_sentiment,
      top_themes: [],
      key_insights: []
    }
  }' > "$OUTPUT_FILE"

echo "✅ Results saved to: $OUTPUT_FILE" >&2
echo "📁 $(realpath "$OUTPUT_FILE")"
