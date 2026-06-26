#!/bin/bash
# DHL Sendungsverfolgung via dhl.de API
# Usage: dhl_track.sh <TRACKING_NUMBER> [language]
# Returns JSON with tracking status, events, and progress

TRACKING_NUMBER="${1:?Usage: dhl_track.sh <TRACKING_NUMBER> [language]}"
LANG="${2:-de}"

curl -s "https://www.dhl.de/int-verfolgen/data/search?piececode=${TRACKING_NUMBER}&language=${LANG}" \
  -H 'Accept: application/json' \
  -H 'User-Agent: Mozilla/5.0'
