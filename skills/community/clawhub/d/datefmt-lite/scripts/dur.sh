#!/usr/bin/env bash
# dur.sh — human-friendly duration between two timestamps
# Usage: ./dur.sh <start> [end]   (end defaults to now)
# Accepts anything GNU date can parse, e.g.:
#   ./dur.sh "2026-09-01 09:00" "2026-09-06 08:28"
#   ./dur.sh "@1789412880"
set -euo pipefail

start=$1
end=${2:-now}

s=$(date -d "$start" +%s) || { echo "cannot parse start: $start" >&2; exit 2; }
e=$(date -d "$end"   +%s) || { echo "cannot parse end: $end"     >&2; exit 2; }

delta=$(( e - s ))
[ $delta -lt 0 ] && sign="-" && delta=$(( -delta )) || sign=""

days=$(( delta / 86400 )); delta=$(( delta % 86400 ))
hours=$(( delta / 3600 )); delta=$(( delta % 3600 ))
mins=$(( delta / 60 ));   secs=$(( delta % 60 ))

echo "${sign}${days}d ${hours}h ${mins}m ${secs}s"
