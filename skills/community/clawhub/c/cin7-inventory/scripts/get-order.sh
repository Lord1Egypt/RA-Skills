#!/bin/bash
# Get a single order by ID
# Usage: bash scripts/get-order.sh --id "order-id-here"
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/config.sh"

ID=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --id) ID="$2"; shift 2 ;;
    *) shift ;;
  esac
done

if [ -z "$ID" ]; then
  echo "Error: --id is required"
  exit 1
fi

cin7_get "Sale" "?ID=$ID"
