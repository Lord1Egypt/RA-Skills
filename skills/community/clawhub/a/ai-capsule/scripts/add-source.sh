#!/usr/bin/env bash
# Add a new data source to sources/{industry}.yaml
#
# Usage:
#   bash scripts/add-source.sh --industry ai --type rss --name "My Blog" --url https://example.com/feed --limit 5
#   bash scripts/add-source.sh --industry ai --type webfetch --name "My Blog" --url https://example.com --limit 5 --note "latest 5 posts"
#   bash scripts/add-source.sh --industry ai --type tavily --name "Reddit X" --query "LLM X" --domains "reddit.com" --limit 5

set -e
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"

INDUSTRY="ai"
TYPE=""
NAME=""
URL=""
QUERY=""
DOMAINS=""
LIMIT=5
NOTE=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --industry) INDUSTRY="$2"; shift 2 ;;
    --type)     TYPE="$2";     shift 2 ;;
    --name)     NAME="$2";     shift 2 ;;
    --url)      URL="$2";      shift 2 ;;
    --query)    QUERY="$2";    shift 2 ;;
    --domains)  DOMAINS="$2";  shift 2 ;;
    --limit)    LIMIT="$2";    shift 2 ;;
    --note)     NOTE="$2";     shift 2 ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

FILE="$SKILL_DIR/sources/${INDUSTRY}.yaml"
[ ! -f "$FILE" ] && echo "ERROR: $FILE not found" && exit 1
[ -z "$TYPE" ] && echo "ERROR: --type required (rss|webfetch|tavily)" && exit 1
[ -z "$NAME" ] && echo "ERROR: --name required" && exit 1

# Duplicate check
if grep -q "name: $NAME" "$FILE" 2>/dev/null; then
  echo "ERROR: source '$NAME' already exists in $FILE"
  exit 1
fi

# Build YAML block
case "$TYPE" in
  rss)
    [ -z "$URL" ] && echo "ERROR: --url required for rss" && exit 1
    BLOCK="
  - name: $NAME
    type: rss
    url: $URL
    limit: $LIMIT"
    ;;
  webfetch)
    [ -z "$URL" ] && echo "ERROR: --url required for webfetch" && exit 1
    BLOCK="
  - name: $NAME
    type: webfetch
    url: $URL
    limit: $LIMIT"
    [ -n "$NOTE" ] && BLOCK="$BLOCK
    note: $NOTE"
    ;;
  tavily)
    [ -z "$QUERY" ] && echo "ERROR: --query required for tavily" && exit 1
    BLOCK="
  - name: $NAME
    type: tavily
    query: \"$QUERY\""
    if [ -n "$DOMAINS" ]; then
      BLOCK="$BLOCK
    include_domains:"
      IFS=',' read -ra dom_arr <<< "$DOMAINS"
      for d in "${dom_arr[@]}"; do
        d="$(echo "$d" | tr -d ' ')"
        BLOCK="$BLOCK
      - $d"
      done
    fi
    BLOCK="$BLOCK
    time_range: day
    limit: $LIMIT"
    ;;
  *)
    echo "ERROR: unknown type '$TYPE' (rss|webfetch|tavily)"
    exit 1
    ;;
esac

printf "%s\n" "$BLOCK" >> "$FILE"
echo "Added '$NAME' ($TYPE) to $FILE"
