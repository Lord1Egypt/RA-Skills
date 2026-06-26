#!/bin/bash
# Check stock levels (all or for a specific product)
# Usage: bash scripts/get-stock.sh [--product-id "id"] [--page 1]
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/config.sh"

PRODUCT_ID=""
PAGE=1

while [[ $# -gt 0 ]]; do
  case $1 in
    --product-id) PRODUCT_ID="$2"; shift 2 ;;
    --page) PAGE="$2"; shift 2 ;;
    *) shift ;;
  esac
done

PARAMS="?Page=$PAGE&Limit=50"
[ -n "$PRODUCT_ID" ] && PARAMS="${PARAMS}&ProductID=$PRODUCT_ID"

cin7_get "ref/productavailability" "$PARAMS"
