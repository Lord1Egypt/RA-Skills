#!/bin/bash
# Transfer stock between warehouse locations
# Usage: bash scripts/stock-transfer.sh --data '{"Lines":[{"ProductID":"id","From":"warehouse-a","To":"warehouse-b","Quantity":5}]}'
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/config.sh"

DATA=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --data) DATA="$2"; shift 2 ;;
    *) shift ;;
  esac
done

if [ -z "$DATA" ]; then
  echo "Error: --data is required (JSON string)"
  exit 1
fi

cin7_post "StockTransfer" "$DATA"
