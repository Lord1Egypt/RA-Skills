#!/usr/bin/env bash
# check-endpoint.sh — Look up trust data for an endpoint URL.
#
# Usage:
#   check-endpoint.sh <url>              — Full trust assessment
#   check-endpoint.sh <url> --price 0.05 — Also check for price anomaly
#
# Output: JSON trust assessment

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SERVER_DIR="$SCRIPT_DIR/../server"

if [ $# -lt 1 ]; then
  echo "Usage: check-endpoint.sh <endpoint-url> [--price <amount>]" >&2
  exit 1
fi

URL="$1"
PRICE=""
shift
while [ $# -gt 0 ]; do
  case "$1" in
    --price) PRICE="$2"; shift 2 ;;
    *) echo "Unknown argument: $1" >&2; exit 1 ;;
  esac
done

node --input-type=module -e "
  import { checkEndpoint, checkPriceAnomaly } from '${SERVER_DIR}/trust-db.js';

  const url = process.argv[1];
  const price = process.argv[2] || null;

  const assessment = checkEndpoint(url);
  const result = { ...assessment };

  if (price) {
    result.price_check = checkPriceAnomaly(url, price);
  }

  console.log(JSON.stringify(result, null, 2));
" "$URL" "$PRICE"
