#!/bin/bash
# List/search customers
# Usage: bash scripts/get-customers.sh [--search "name"] [--page 1]
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/config.sh"

PAGE=1
SEARCH=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --search) SEARCH="$2"; shift 2 ;;
    --page) PAGE="$2"; shift 2 ;;
    *) shift ;;
  esac
done

PARAMS="?Page=$PAGE&Limit=50"
[ -n "$SEARCH" ] && PARAMS="${PARAMS}&Name=$SEARCH"

cin7_get "Customer" "$PARAMS"
