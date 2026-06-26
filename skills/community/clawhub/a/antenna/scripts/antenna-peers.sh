#!/usr/bin/env bash
# antenna-peers.sh — List known Antenna peers
# Usage: antenna-peers.sh [list|json]
#
# Reads from the flat antenna-peers.json format (no .peers wrapper).
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
PEERS_FILE="$SKILL_DIR/antenna-peers.json"

ACTION="${1:-list}"

case "$ACTION" in
  list)
    jq -r 'to_entries[] | select((.value | type) == "object" and (.value.url? | type) == "string") | "\(.key)\t\(.value.display_name // "—")\t\(.value.url)\t\(if .value.self then "(self)" else "" end)"' \
      "$PEERS_FILE" | column -t -s $'\t' -N "PEER,NAME,URL,NOTE"
    ;;
  json)
    jq '.' "$PEERS_FILE"
    ;;
  *)
    echo "Usage: antenna-peers.sh [list|json]" >&2
    exit 1
    ;;
esac
