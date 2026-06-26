#!/bin/bash
set -euo pipefail

# Convenience wrapper using REST.
# Usage: twenty-create-company.sh "Name" [domain] [employees]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}" )" && pwd)"

NAME="${1:-}"
DOMAIN="${2:-}"
EMPLOYEES="${3:-}"

if [ -z "$NAME" ]; then
  echo "Usage: twenty-create-company.sh \"Name\" [domain] [employees]" >&2
  exit 1
fi
# shellcheck disable=SC1091
source "$SCRIPT_DIR/twenty-config.sh"
require_cmd python3

JSON_BODY="$(python3 - <<'PY' "$NAME" "$DOMAIN" "$EMPLOYEES"
import json,sys
name,domain,employees = sys.argv[1],sys.argv[2],sys.argv[3]
payload = {"name": name}
if domain:
  payload["domainName"] = domain
if employees:
  try:
    payload["employees"] = int(employees)
  except ValueError:
    payload["employees"] = employees
print(json.dumps(payload))
PY
)"

"$SCRIPT_DIR/twenty-rest-post.sh" "/companies" "$JSON_BODY"
