#!/usr/bin/env bash
set -euo pipefail

# competitor-scraper.sh — Scrape competitor reviews from multiple sources
# Usage: ./competitor-scraper.sh --product "Product Name" --sources "g2,trustpilot,reddit"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
DATA_DIR="$WORKSPACE_ROOT/data/research"
mkdir -p "$DATA_DIR"

PRODUCT=""
SOURCES="g2,trustpilot,reddit"

# Parse args
while [[ $# -gt 0 ]]; do
  case $1 in
    --product) PRODUCT="$2"; shift 2 ;;
    --sources) SOURCES="$2"; shift 2 ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

if [[ -z "$PRODUCT" ]]; then
  echo "Usage: $0 --product \"Product Name\" [--sources \"g2,trustpilot,reddit\"]" >&2
  exit 1
fi

TIMESTAMP=$(date -u +"%Y%m%d-%H%M%S")
PRODUCT_SLUG=$(echo "$PRODUCT" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd '[:alnum:]-')
OUTPUT_FILE="$DATA_DIR/competitor-${PRODUCT_SLUG}-${TIMESTAMP}.json"

echo "🔍 Scraping reviews for: $PRODUCT" >&2
echo "📦 Sources: $SOURCES" >&2

FINDINGS='[]'
TOTAL_SOURCES=0

# Helper function to add finding
add_finding() {
  local source=$1
  local source_id=$2
  local text=$3
  local rating=$4
  local url=$5
  
  FINDING=$(jq -n \
    --arg source "$source" \
    --arg source_id "$source_id" \
    --arg text "$text" \
    --argjson rating "$rating" \
    --arg url "$url" \
    '{
      source: $source,
      source_id: $source_id,
      text: $text,
      sentiment: null,
      themes: [],
      metadata: {
        rating: $rating,
        url: $url
      }
    }')
  
  FINDINGS=$(echo "$FINDINGS" | jq --argjson finding "$FINDING" '. += [$finding]')
  ((TOTAL_SOURCES++)) || true
}

# Parse sources
IFS=',' read -ra SOURCE_ARRAY <<< "$SOURCES"

for SOURCE in "${SOURCE_ARRAY[@]}"; do
  case "$SOURCE" in
    g2)
      echo "  📊 Fetching G2 reviews..." >&2
      # G2 API requires auth — for MVP, we'll use web scraping simulation
      # In production, use G2 API or headless browser automation
      # For now, placeholder data
      echo "  ⚠️  G2 scraping requires API key or browser automation (not implemented in MVP)" >&2
      ;;
    
    trustpilot)
      echo "  ⭐ Fetching Trustpilot reviews..." >&2
      # Trustpilot public reviews can be scraped from their website
      # URL format: https://www.trustpilot.com/review/{company-slug}
      # For now, placeholder
      echo "  ⚠️  Trustpilot scraping requires browser automation (not implemented in MVP)" >&2
      ;;
    
    reddit)
      echo "  🤖 Fetching Reddit mentions..." >&2
      # Use Reddit search API to find product mentions across relevant subreddits
      SUBREDDITS=("SaaS" "Entrepreneur" "smallbusiness" "productivity")
      
      for SUBREDDIT in "${SUBREDDITS[@]}"; do
        # Search for product name in this subreddit
        URL="https://www.reddit.com/r/${SUBREDDIT}/search.json?q=$(printf %s "$PRODUCT" | jq -sRr @uri)&limit=10&restrict_sr=on"
        
        TEMP_JSON=$(mktemp)
        trap 'rm -f "$TEMP_JSON"' EXIT
        
        if curl -sL -A "OpenClaw/CustomerResearch (by /u/clawdiri)" "$URL" > "$TEMP_JSON" 2>/dev/null; then
          # Extract threads
          while IFS= read -r thread; do
            TITLE=$(echo "$thread" | jq -r '.title')
            SELFTEXT=$(echo "$thread" | jq -r '.selftext // ""')
            PERMALINK=$(echo "$thread" | jq -r '.permalink')
            SCORE=$(echo "$thread" | jq -r '.score')
            THREAD_ID=$(echo "$thread" | jq -r '.id')
            
            if [[ -n "$TITLE" ]] && [[ "$TITLE" != "null" ]]; then
              FULL_TEXT="$TITLE. $SELFTEXT"
              # Normalize score to 0-5 rating (approximate sentiment from upvotes)
              RATING=$(echo "$SCORE" | awk '{if ($1 < 0) print 1; else if ($1 < 10) print 3; else if ($1 < 50) print 4; else print 5}')
              add_finding "reddit" "r/${SUBREDDIT}/${THREAD_ID}" "$FULL_TEXT" "$RATING" "https://www.reddit.com${PERMALINK}"
            fi
          done < <(jq -c '.data.children[]? | select(.kind == "t3") | .data' "$TEMP_JSON" 2>/dev/null || true)
        fi
      done
      ;;
    
    *)
      echo "  ⚠️  Unknown source: $SOURCE" >&2
      ;;
  esac
done

# Calculate summary stats
AVG_RATING=$(echo "$FINDINGS" | jq '[.[].metadata.rating | select(. != null)] | add / length // 0')
RATING_DIST=$(echo "$FINDINGS" | jq 'group_by(.metadata.rating) | map({rating: .[0].metadata.rating, count: length}) | sort_by(.rating)')

# Build output JSON
jq -n \
  --arg skill "customer-research" \
  --arg script "competitor-scraper" \
  --arg timestamp "$(date -u +"%Y-%m-%dT%H:%M:%SZ")" \
  --arg product "$PRODUCT" \
  --arg sources "$SOURCES" \
  --argjson findings "$FINDINGS" \
  --argjson total_sources "$TOTAL_SOURCES" \
  --argjson avg_rating "$AVG_RATING" \
  --argjson rating_dist "$RATING_DIST" \
  '{
    meta: {
      skill: $skill,
      script: $script,
      timestamp: $timestamp,
      query: {
        product: $product,
        sources: $sources
      }
    },
    findings: $findings,
    summary: {
      total_sources: $total_sources,
      avg_rating: $avg_rating,
      rating_distribution: $rating_dist,
      top_themes: [],
      key_insights: [
        "Reddit mentions found in SaaS/Entrepreneur communities",
        "G2 and Trustpilot require browser automation for full scraping",
        "Implement headless browser (Playwright/Puppeteer) for production"
      ]
    }
  }' > "$OUTPUT_FILE"

echo "✅ Results saved to: $OUTPUT_FILE" >&2
echo "📊 Total sources scraped: $TOTAL_SOURCES" >&2
echo "📁 $(realpath "$OUTPUT_FILE")"
