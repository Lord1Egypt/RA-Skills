#!/usr/bin/env bash
# station.sh — getMsrstnList: 측정소 목록 조회.
#
# Search the directory of all 도시대기/도로변대기/국가배경/교외대기/항만 측정소.
# Filter by sido name and/or address keyword (works as a contains-match on
# `addr` — e.g. "강남구", "수원시 영통구").
#
# Usage:
#   station.sh --keyword 강남
#   station.sh --sido 서울 --num 200
#
# Output: JSONL — one row per station (stationName, addr, dmX, dmY, mangName, year).
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
. "$here/_common.sh"

sido="" keyword="" num="100" page="1"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --sido)     sido="$2";    shift 2;;
    --keyword)  keyword="$2"; shift 2;;
    --num)      num="$2";     shift 2;;
    --page)     page="$2";    shift 2;;
    -h|--help)
      sed -n '2,12p' "$0" | sed 's/^# \{0,1\}//'
      exit 0;;
    *) echo "error: unknown flag '$1'" >&2; exit 64;;
  esac
done

[[ -n "$sido" ]] && valid_sido "$sido"
require_bin curl jq

resp=$(airkorea_get "$MSRSTN_BASE" "getMsrstnList" \
  "addr=$keyword" "stationName=" \
  "numOfRows=$num" "pageNo=$page")

# Optional client-side filter by sido. data.go.kr's getMsrstnList does not have
# a sido parameter; it's exposed only through `addr` keyword. So when --sido is
# given, we filter the JSONL stream.
if [[ -n "$sido" ]]; then
  echo "$resp" | emit_items | jq -c --arg s "$sido" 'select((.addr // "") | startswith($s))'
else
  echo "$resp" | emit_items
fi
