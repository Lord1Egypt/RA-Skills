#!/bin/bash
set -euo pipefail

# Usage: twenty-find-companies.sh "search" [limit]
# Uses REST filter with ilike (may vary by Twenty version/workspace).

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}" )" && pwd)"

SEARCH="${1:-}"
LIMIT="${2:-10}"

if [ -z "$SEARCH" ]; then
  echo "Usage: twenty-find-companies.sh \"search\" [limit]" >&2
  exit 1
fi
if [[ ! "$LIMIT" =~ ^[0-9]+$ ]]; then
  echo "Invalid limit '$LIMIT'. Expected a non-negative integer." >&2
  exit 1
fi
if ! command -v python3 >/dev/null 2>&1; then
  echo "Missing required command: python3" >&2
  exit 1
fi

FILTER=$(python3 - <<'PY' "$SEARCH"
import json,sys
s=sys.argv[1]
print(json.dumps({"name":{"ilike":f"%{s}%"}}))
PY
)

"$SCRIPT_DIR/twenty-rest-get.sh" "/companies" "filter=$FILTER" "limit=$LIMIT" "offset=0"
