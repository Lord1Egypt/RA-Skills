#!/bin/bash
set -euo pipefail

EMAIL="${1:-${EMAIL:-}}"
[[ -n "$EMAIL" ]] || { echo "Usage: $0 <email> (or set EMAIL=...)" >&2; exit 1; }

curl -sS 'https://api.datahive.ai/api/auth/magic-link/request' \
  -H 'content-type: application/json' \
  --data-raw "{\"email\":\"$EMAIL\",\"redirectUrl\":\"https://dashboard.datahive.ai/auth\"}"
