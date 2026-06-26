#!/bin/bash
# Update an existing sales order
# Usage: bash scripts/update-order.sh --id "order-id" --data '{"Status":"COMPLETED"}'
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/config.sh"

ID=""
DATA=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --id) ID="$2"; shift 2 ;;
    --data) DATA="$2"; shift 2 ;;
    *) shift ;;
  esac
done

if [ -z "$ID" ] || [ -z "$DATA" ]; then
  echo "Error: --id and --data are required"
  exit 1
fi

FULL_DATA=$(echo "$DATA" | sed "s/^{/{\"ID\":\"$ID\",/")

cin7_put "Sale" "$FULL_DATA"
