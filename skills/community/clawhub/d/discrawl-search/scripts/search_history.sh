#!/usr/bin/env bash
# Search Discord message history via discrawl
# Usage: search_history.sh <query> [channel_id] [limit]
set -euo pipefail

QUERY="${1:-}"
CHANNEL_ID="${2:-}"
LIMIT="${3:-10}"

if [ -z "$QUERY" ]; then
    echo "Usage: search_history.sh <query> [channel_id] [limit]"
    exit 1
fi

if [[ ! "$LIMIT" =~ ^[0-9]+$ ]] || (( LIMIT < 1 || LIMIT > 100 )); then
    echo "limit must be an integer from 1 to 100" >&2
    exit 2
fi

args=(search "$QUERY" --limit "$LIMIT" --json)
if [[ -n "$CHANNEL_ID" ]]; then
    args+=(--channel "$CHANNEL_ID")
fi
discrawl "${args[@]}"
