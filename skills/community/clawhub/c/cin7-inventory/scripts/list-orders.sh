#!/bin/bash
# List sales orders
# Usage: bash scripts/list-orders.sh [--status "COMPLETED"] [--page 1]
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/config.sh"

PAGE=1
STATUS=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --status) STATUS="$2"; shift 2 ;;
    --page) PAGE="$2"; shift 2 ;;
    *) shift ;;
  esac
done

PARAMS="?Page=$PAGE&Limit=50"
[ -n "$STATUS" ] && PARAMS="${PARAMS}&Status=$STATUS"

cin7_get "SaleList" "$PARAMS"
