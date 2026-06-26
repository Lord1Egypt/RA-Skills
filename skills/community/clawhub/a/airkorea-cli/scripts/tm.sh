#!/usr/bin/env bash
# tm.sh — getTMStdrCrdnt: TM 기준좌표 조회.
#
# Resolve a 행정동/법정동 name to its TM(중부원점) X/Y coordinates — needed by
# nearby.sh (getNearbyMsrstnList only accepts TM coordinates, not WGS84).
#
# Usage:
#   tm.sh --umd 역삼동
#   tm.sh --umd 양재동 --num 5
#
# Output: JSONL — one row per matching umdName (umdName, sggName, sidoName, tmX, tmY).
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
. "$here/_common.sh"

umd="" num="100" page="1"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --umd)   umd="$2";  shift 2;;
    --num)   num="$2";  shift 2;;
    --page)  page="$2"; shift 2;;
    -h|--help)
      sed -n '2,12p' "$0" | sed 's/^# \{0,1\}//'
      exit 0;;
    *) echo "error: unknown flag '$1'" >&2; exit 64;;
  esac
done

[[ -z "$umd" ]] && { echo "error: --umd is required (행정/법정동 name, e.g. '역삼동')." >&2; exit 64; }
require_bin curl jq

resp=$(airkorea_get "$MSRSTN_BASE" "getTMStdrCrdnt" \
  "umdName=$umd" "numOfRows=$num" "pageNo=$page")
echo "$resp" | emit_items
