#!/bin/bash
# Get sales report for a date range
# Usage: bash scripts/sales-report.sh --from "2026-01-01" --to "2026-03-07"
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/config.sh"

FROM=""
TO=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --from) FROM="$2"; shift 2 ;;
    --to) TO="$2"; shift 2 ;;
    *) shift ;;
  esac
done

if [ -z "$FROM" ] || [ -z "$TO" ]; then
  echo "Error: --from and --to are required (YYYY-MM-DD)"
  exit 1
fi

cin7_get "SaleList" "?SaleOrderDate_from=$FROM&SaleOrderDate_to=$TO&Page=1&Limit=250"
