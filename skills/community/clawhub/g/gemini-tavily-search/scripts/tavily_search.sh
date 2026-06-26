#!/usr/bin/env bash
# Tavily Search (REST API-only)
# Usage: ./tavily_search.sh '<json>'
# Example: ./tavily_search.sh '{"query":"AI news","time_range":"week","max_results":10}'

set -euo pipefail

JSON_INPUT="${1:-}"
if [[ -z "$JSON_INPUT" ]]; then
  echo "Usage: ./tavily_search.sh '<json>'" >&2
  echo "" >&2
  echo "Required:" >&2
  echo "  query: string - Search query (keep under 400 chars)" >&2
  echo "" >&2
  echo "Optional:" >&2
  echo "  search_depth: \"ultra-fast\", \"fast\", \"basic\" (default), \"advanced\"" >&2
  echo "  topic: \"general\" (default)" >&2
  echo "  max_results: 1-20 (default: 10)" >&2
  echo "  time_range: \"day\", \"week\", \"month\", \"year\"" >&2
  echo "  start_date: \"YYYY-MM-DD\"" >&2
  echo "  end_date: \"YYYY-MM-DD\"" >&2
  echo "  include_domains: [\"domain1.com\", \"domain2.com\"]" >&2
  echo "  exclude_domains: [\"domain1.com\", \"domain2.com\"]" >&2
  echo "  country: country name (general topic only)" >&2
  echo "  include_raw_content: true/false" >&2
  echo "  include_images: true/false" >&2
  echo "  include_image_descriptions: true/false" >&2
  echo "  include_favicon: true/false" >&2
  echo "" >&2
  echo "Example:" >&2
  echo "  ./tavily_search.sh '{\"query\":\"latest AI trends\",\"time_range\":\"week\"}'" >&2
  exit 1
fi

command -v curl >/dev/null 2>&1 || { echo "Error: curl not found" >&2; exit 1; }
command -v jq   >/dev/null 2>&1 || { echo "Error: jq not found" >&2; exit 1; }

: "${TAVILY_API_KEY:?Error: TAVILY_API_KEY is required (API-only mode)}"

redact_text() {
  local s="$1"
  s="$(printf "%s" "$s" | sed -E 's/[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}/[REDACTED_EMAIL]/g')"
  s="$(printf "%s" "$s" | sed -E 's/\b\+?[0-9][0-9 ()\.-]{6,}[0-9]\b/[REDACTED_PHONE]/g')"
  s="$(printf "%s" "$s" | sed -E 's/\bsk-[A-Za-z0-9_-]{8,}\b/[REDACTED_KEY]/g')"
  printf "%s" "$s"
}

# Validate JSON
echo "$JSON_INPUT" | jq empty >/dev/null 2>&1 || { echo "Error: Invalid JSON input" >&2; exit 1; }

# Require query
QUERY="$(echo "$JSON_INPUT" | jq -r '.query // empty')"
if [[ -z "$QUERY" || "$QUERY" == "null" ]]; then
  echo "Error: 'query' field is required" >&2
  exit 1
fi

# Query minimization / redaction
QUERY="$(redact_text "$QUERY")"
JSON_INPUT="$(echo "$JSON_INPUT" | jq -c --arg q "$QUERY" '.query = $q')"

# Build REST request payload (merge api_key into the JSON)
PAYLOAD="$(echo "$JSON_INPUT" | jq --arg key "$TAVILY_API_KEY" 'del(.api_key) + {api_key: $key}')"

# Call Tavily REST API
RESP="$(
     curl -sS --fail-with-body --proto '=https' --tlsv1.2 \
     --connect-timeout 5 --max-time 25 \
     -X POST "https://api.tavily.com/search" \
     -H "Content-Type: application/json" \
     -d "$PAYLOAD"
 )"

# Ensure JSON output (if Tavily returns HTML/error text, fail)
echo "$RESP" | jq empty >/dev/null 2>&1 || { echo "Error: Tavily returned non-JSON" >&2; exit 1; }

# If Tavily returns an error object, surface it (still valid JSON)
HAS_ERROR="$(echo "$RESP" | jq -r 'has("error")')"
if [[ "$HAS_ERROR" == "true" ]]; then
  echo "$RESP"
  exit 1
fi

echo "$RESP"