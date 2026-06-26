#!/bin/bash
# Anspire Search wrapper script
# Usage: ./search.sh "your search query" [top_k]

set -euo pipefail

# Check if API key is set
if [ -z "${ANSPIRE_API_KEY:-}" ]; then
    echo "Error: ANSPIRE_API_KEY environment variable is not set" >&2
    echo "Please run: export ANSPIRE_API_KEY='your-api-key'" >&2
    exit 1
fi

# Get query from first argument
if [ $# -lt 1 ]; then
    echo "Usage: $0 \"search query\" [top_k]" >&2
    echo "Example: $0 \"latest AI news\" 5" >&2
    exit 1
fi

QUERY="$1"
TOP_K="${2:-10}"

# Execute search
curl --silent --show-error --fail --location --get \
  "https://plugin.anspire.cn/api/ntsearch/search" \
  --data-urlencode "query=${QUERY}" \
  --data-urlencode "top_k=${TOP_K}" \
  --header "Authorization: Bearer ${ANSPIRE_API_KEY}" \
  --header "Accept: application/json"
