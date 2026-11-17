#!/bin/bash
# Dorar Hadith Search Script v2
# Usage: bash dorar_search.sh "search query"
# Returns: Formatted hadith results with narrator, source, grade, and Dorar URL

QUERY="$1"
if [ -z "$QUERY" ]; then
  echo "Usage: bash dorar_search.sh \"search query\""
  exit 1
fi

# URL encode the query
ENCODED=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$QUERY'))")

RESULT=$(curl -s -L \
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" \
  -H "Accept: application/json, text/javascript, */*" \
  -H "Referer: https://dorar.net/" \
  "https://dorar.net/dorar_api.json?skey=${ENCODED}&callback=?")

export DORAR_QUERY="$QUERY"
# Resolve dorar_parser.py relative to this script (skill-relative, works after install)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
echo "$RESULT" | python3 "$SCRIPT_DIR/dorar_parser.py"
