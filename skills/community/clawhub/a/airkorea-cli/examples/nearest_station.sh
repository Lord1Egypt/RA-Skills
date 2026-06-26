#!/usr/bin/env bash
# Given a 행정동 name (default: 역삼동), find the nearest measuring station
# and emit its latest hourly reading.
#
# Requires: AIRKOREA_SERVICE_KEY exported.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL="$(cd "$here/.." && pwd)"

UMD="${1:-역삼동}"

# Take the first matching umdName in 서울 (you may want to broaden / disambiguate).
read TMX TMY < <("$SKILL/scripts/tm.sh" --umd "$UMD" \
  | jq -r 'select(.sidoName=="서울") | "\(.tmX) \(.tmY)"' | head -1)

if [[ -z "${TMX:-}" || -z "${TMY:-}" ]]; then
  echo "no Seoul match for umdName '$UMD'." >&2
  exit 64
fi

STN=$("$SKILL/scripts/nearby.sh" --tm-x "$TMX" --tm-y "$TMY" \
  | jq -r '.stationName' | head -1)

[[ -z "${STN:-}" ]] && { echo "no nearby station found near TM=($TMX,$TMY)." >&2; exit 22; }

"$SKILL/scripts/realtime.sh" --station "$STN" --period HOUR --num 1 \
  | jq -c --arg umd "$UMD" --arg stn "$STN" \
      '{umdName: $umd, station: $stn, dataTime, pm25Value, pm25Grade, pm10Value, pm10Grade, o3Value, no2Value}'
