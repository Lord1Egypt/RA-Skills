#!/usr/bin/env bash
# forecast.sh — getMinuDustFrcstDspth: 대기오염 예보통보 조회.
#
# Returns the most-recent forecast announcements for a search date. Each row
# carries `informCode` (PM10|PM25|O3), `informGrade` (region-by-region grades:
# "서울 : 보통,제주 : 좋음,..."), `informData` (forecast target date),
# `informCause` (날씨/기류 설명), `dataTime` (announcement time).
#
# Usage:
#   forecast.sh --date 2026-04-29
#   forecast.sh --date 2026-04-29 --code PM25
#
# code: PM10  PM25  O3   (default: all three returned)
#
# Output: JSONL — one row per (informCode × dataTime).
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
. "$here/_common.sh"

date_in="" code="" num="20" page="1"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --date)  date_in="$2"; shift 2;;
    --code)  code="$2";    shift 2;;
    --num)   num="$2";     shift 2;;
    --page)  page="$2";    shift 2;;
    -h|--help)
      sed -n '2,15p' "$0" | sed 's/^# \{0,1\}//'
      exit 0;;
    *) echo "error: unknown flag '$1'" >&2; exit 64;;
  esac
done

[[ -z "$date_in" ]] && { echo "error: --date is required (YYYY-MM-DD)." >&2; exit 64; }
valid_yyyy_mm_dd "$date_in"
if [[ -n "$code" ]]; then
  case "$code" in PM10|PM25|O3) ;; *) echo "error: --code must be one of: PM10 PM25 O3." >&2; exit 64;; esac
fi

require_bin curl jq

resp=$(airkorea_get "$ARPLTN_BASE" "getMinuDustFrcstDspth" \
  "searchDate=$date_in" "InformCode=$code" \
  "numOfRows=$num" "pageNo=$page")
echo "$resp" | emit_items
