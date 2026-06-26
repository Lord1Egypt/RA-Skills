#!/bin/bash
# Search script - 封装搜索 API 调用

QUERY="$1"
MAX_RESULTS="${2:-5}"
OUTPUT_FILE="${3:-search_results.json}"

if [ -z "$QUERY" ]; then
  echo "Usage: search.sh <query> [max_results] [output_file]"
  exit 1
fi

# 优先用 Tavily，其次 DuckDuckGo
if [ -n "$TAVILY_API_KEY" ]; then
  curl -s "https://api.tavily.com/search" \
    -H "Authorization: Bearer $TAVILY_API_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"query\": \"$QUERY\", \"max_results\": $MAX_RESULTS}" \
    > "$OUTPUT_FILE"
else
  # DuckDuckGo 免费
 curl -s "https://api.duckduckgo.com/?q=$(echo "$QUERY" | urlencode)&format=json&no_html=1" \
    > "$OUTPUT_FILE"
fi

echo "Results saved to $OUTPUT_FILE"