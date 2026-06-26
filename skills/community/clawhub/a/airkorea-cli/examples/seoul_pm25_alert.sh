#!/usr/bin/env bash
# Emit one row per Seoul station whose PM2.5 grade is currently 나쁨(3) or 매우나쁨(4).
# Use as the body of a runner/parent/employee push-notification job.
#
# Requires: AIRKOREA_SERVICE_KEY exported.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL="$(cd "$here/.." && pwd)"

"$SKILL/scripts/sido.sh" --sido 서울 --num 60 \
  | jq -c 'select((.pm25Grade // "-") | tonumber? // 0 | . >= 3)
           | {stationName, dataTime, pm25Value, pm25Grade, pm10Value}'
