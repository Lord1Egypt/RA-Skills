#!/usr/bin/env bash
set -euo pipefail

SECRET_ENV="/root/.openclaw/workspace/.secrets/costco-monitor.env"
if [[ ! -f "$SECRET_ENV" ]]; then
  echo "missing secret file: $SECRET_ENV" >&2
  exit 2
fi

# shellcheck disable=SC1090
source "$SECRET_ENV"

: "${PROXY_URL:?PROXY_URL is required}"
: "${ZIP_CODES:?ZIP_CODES is required}"
: "${OUTPUT_JSONL:?OUTPUT_JSONL is required}"
: "${STATE_FILE:?STATE_FILE is required}"
: "${REPORT_FILE:?REPORT_FILE is required}"
: "${LOG_FILE:?LOG_FILE is required}"

products=()
for name in $(compgen -A variable | grep '^PRODUCT_'); do
  value=${!name}
  [[ -n "$value" ]] && products+=("$value")
done

if [[ ${#products[@]} -eq 0 ]]; then
  echo "at least one PRODUCT_* is required" >&2
  exit 2
fi

zip_args=()
for z in $ZIP_CODES; do
  zip_args+=(--zip "$z")
done

product_args=()
for p in "${products[@]}"; do
  product_args+=(--product "$p")
done

python3 /root/.openclaw/workspace/skills/costco-inventory-monitor/scripts/check_costco_inventory.py  "${product_args[@]}"  "${zip_args[@]}"  --proxy-url "$PROXY_URL"  --output-jsonl "$OUTPUT_JSONL"  --state-file "$STATE_FILE"  --report-file "$REPORT_FILE"  >> "$LOG_FILE" 2>&1
