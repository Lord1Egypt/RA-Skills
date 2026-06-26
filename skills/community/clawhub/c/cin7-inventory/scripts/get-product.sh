#!/bin/bash
# Get a single product by ID
# Usage: bash scripts/get-product.sh --id "product-id-here"
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

cin7_get "Product" "?ID=$ID"
