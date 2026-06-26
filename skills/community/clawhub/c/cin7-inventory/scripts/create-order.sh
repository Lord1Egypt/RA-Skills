#!/bin/bash
# Create a new sales order
# Usage: bash scripts/create-order.sh --data '{"Customer":"name","Lines":[{"ProductID":"id","Quantity":1}]}'
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

cin7_post "Sale" "$DATA"
