#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
ENQUEUE="$ROOT/scripts/speak-local-queued.sh"
STATUS="$ROOT/scripts/tts-queue-status.sh"

ITERATIONS="5"
STATUS_MODE="none"   # none|pre|post|both
OUTPUT_MODE="compact" # compact|full

usage() {
  cat <<'EOF'
Usage: benchmark-autonoannounce.sh [iterations] [--status none|pre|post|both] [--output compact|full]

Examples:
  benchmark-autonoannounce.sh 5
  benchmark-autonoannounce.sh 5 --status both --output full

Defaults are optimized for foreground speed:
  --status none
  --output compact
EOF
}

if [[ "${1:-}" =~ ^[0-9]+$ ]]; then
  ITERATIONS="$1"
  shift
fi

while [[ $# -gt 0 ]]; do
  case "$1" in
    --status)
      STATUS_MODE="${2:-none}"
      shift 2
      ;;
    --output)
      OUTPUT_MODE="${2:-compact}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

TEXT_PREFIX="benchmark-$(date +%s)"

if [[ "$OUTPUT_MODE" == "full" ]]; then
  echo "[bench] autonoannounce iterations=$ITERATIONS status=$STATUS_MODE output=$OUTPUT_MODE"
fi

run_status() {
  local phase="$1"
  if [[ "$STATUS_MODE" == "$phase" || "$STATUS_MODE" == "both" ]]; then
    [[ "$OUTPUT_MODE" == "full" ]] && echo "[bench] queue status ($phase)"
    "$STATUS" || true
  fi
}

enqueue_one() {
  local text="$1"
  local start_ns end_ns dur_ms
  start_ns=$(date +%s%N)
  "$ENQUEUE" "$text" >/dev/null
  end_ns=$(date +%s%N)
  dur_ms=$(( (end_ns - start_ns) / 1000000 ))
  echo "$dur_ms"
}

run_status pre

sum=0
min=999999
max=0
for i in $(seq 1 "$ITERATIONS"); do
  ms=$(enqueue_one "$TEXT_PREFIX item-$i")
  sum=$((sum + ms))
  (( ms < min )) && min=$ms
  (( ms > max )) && max=$ms
  if [[ "$OUTPUT_MODE" == "full" ]]; then
    echo "[bench] enqueue[$i]=${ms}ms"
  fi
done

avg=$((sum / ITERATIONS))
run_status post

if [[ "$OUTPUT_MODE" == "compact" ]]; then
  echo "enqueue_ms: min=$min avg=$avg max=$max n=$ITERATIONS"
else
  echo "[bench] enqueue_min=${min}ms"
  echo "[bench] enqueue_avg=${avg}ms"
  echo "[bench] enqueue_max=${max}ms"
  echo "[bench] done"
fi
