#!/usr/bin/env bash
# sido.sh — getCtprvnRltmMesureDnsty: 시도별 실시간 측정정보 조회.
#
# Returns one row per measuring station within a given province, with current
# PM10 / PM2.5 / O3 / NO2 / CO / SO2 readings + grade flags.
#
# Usage:
#   sido.sh --sido 서울
#   sido.sh --sido 전국 --num 600
#
# sido: 전국 서울 부산 대구 인천 광주 대전 울산 경기 강원 충북 충남 전북 전남 경북 경남 제주 세종
#
# Output: JSONL — one row per station.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
. "$here/_common.sh"

sido="" num="100" page="1"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --sido)  sido="$2"; shift 2;;
    --num)   num="$2";  shift 2;;
    --page)  page="$2"; shift 2;;
    -h|--help)
      sed -n '2,13p' "$0" | sed 's/^# \{0,1\}//'
      exit 0;;
    *) echo "error: unknown flag '$1'" >&2; exit 64;;
  esac
done

[[ -z "$sido" ]] && { echo "error: --sido is required." >&2; exit 64; }
valid_sido "$sido"
require_bin curl jq

resp=$(airkorea_get "$ARPLTN_BASE" "getCtprvnRltmMesureDnsty" \
  "sidoName=$sido" "numOfRows=$num" "pageNo=$page")
echo "$resp" | emit_items
