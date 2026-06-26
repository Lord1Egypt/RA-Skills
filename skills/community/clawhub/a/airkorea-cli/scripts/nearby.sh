#!/usr/bin/env bash
# nearby.sh — getNearbyMsrstnList: 근접측정소 목록 조회.
#
# Given TM coordinates (X, Y) — usually fetched via tm.sh first — return the
# closest measuring stations sorted by distance.
#
# Usage:
#   nearby.sh --tm-x 244148.546388 --tm-y 412423.75772
#
# Tip: chain with tm.sh —
#   eval $(scripts/tm.sh --umd 역삼동 \
#     | jq -r 'select(.sidoName=="서울") | "TMX=\(.tmX); TMY=\(.tmY)"' | head -1)
#   scripts/nearby.sh --tm-x "$TMX" --tm-y "$TMY"
#
# Output: JSONL — one row per nearby station (stationName, addr, tm).
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
. "$here/_common.sh"

tm_x="" tm_y=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --tm-x)  tm_x="$2"; shift 2;;
    --tm-y)  tm_y="$2"; shift 2;;
    -h|--help)
      sed -n '2,15p' "$0" | sed 's/^# \{0,1\}//'
      exit 0;;
    *) echo "error: unknown flag '$1'" >&2; exit 64;;
  esac
done

[[ -z "$tm_x" || -z "$tm_y" ]] && { echo "error: --tm-x and --tm-y are both required (use tm.sh to resolve)." >&2; exit 64; }
require_bin curl jq

resp=$(airkorea_get "$MSRSTN_BASE" "getNearbyMsrstnList" \
  "tmX=$tm_x" "tmY=$tm_y")
echo "$resp" | emit_items
