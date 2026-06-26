#!/usr/bin/env bash
# Log an ask-more run result.
# Usage: bash scripts/log-run.sh <skill-dir> <json-payload>
# JSON payload should include: timestamp, question_hash, models[], results[], total_time_ms
# Appends one JSON line to logs/runs.jsonl

set -euo pipefail

SKILL_DIR="${1:-.}"
PAYLOAD="${2:-}"
LOG_DIR="$SKILL_DIR/logs"
LOG_FILE="$LOG_DIR/runs.jsonl"

if [[ -z "$PAYLOAD" ]]; then
  echo "ERROR: No JSON payload provided" >&2
  exit 1
fi

mkdir -p "$LOG_DIR"
echo "$PAYLOAD" >> "$LOG_FILE"
echo "Logged to $LOG_FILE"
