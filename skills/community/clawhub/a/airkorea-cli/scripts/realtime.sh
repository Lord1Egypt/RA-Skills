#!/usr/bin/env bash
# realtime.sh — getMsrstnAcctoRltmMesureDnsty: 측정소별 실시간 측정값 조회.
#
# Returns one row per hour for the named station, with PM10 / PM2.5 / O3 / NO2
# / CO / SO2 concentrations + grade flags (1=좋음 2=보통 3=나쁨 4=매우나쁨).
#
# Usage:
#   realtime.sh --station 종로구
#   realtime.sh --station 강남구 --period DAILY --num 24
#
# period (dataTerm): DAILY=24h HOUR=1h MONTH=30d 3MONTH=90d
#
# Output: JSONL — one row per measurement timestamp.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
. "$here/_common.sh"

station="" period="DAILY" num="100" page="1"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --station)  station="$2"; shift 2;;
    --period)   period="$2";  shift 2;;
    --num)      num="$2";     shift 2;;
    --page)     page="$2";    shift 2;;
    -h|--help)
      sed -n '2,13p' "$0" | sed 's/^# \{0,1\}//'
      exit 0;;
    *) echo "error: unknown flag '$1'" >&2; exit 64;;
  esac
done

[[ -z "$station" ]] && { echo "error: --station is required (e.g. 종로구, 강남구; use station.sh to look up)." >&2; exit 64; }
valid_period "$period"
require_bin curl jq

resp=$(airkorea_get "$ARPLTN_BASE" "getMsrstnAcctoRltmMesureDnsty" \
  "stationName=$station" "dataTerm=$period" \
  "numOfRows=$num" "pageNo=$page")
echo "$resp" | emit_items
