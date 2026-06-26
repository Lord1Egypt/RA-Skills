#!/usr/bin/env bash
# clicky.sh — Fetch analytics from Clicky API
# Usage: clicky.sh <site_name> <type> [options]
# Credentials read from env: CLICKY_<NAME>_SITE_ID + CLICKY_<NAME>_SITEKEY
# Or for default: CLICKY_SITE_ID + CLICKY_SITEKEY
set -euo pipefail

API_URL="https://api.clicky.com/api/stats/4"

SITE_NAME="${1:?Usage: clicky.sh <site_name> <type> [--date DATE] [--limit N] [--daily]}"
shift

# Resolve credentials from environment
UPPER_NAME=$(echo "$SITE_NAME" | tr '[:lower:]' '[:upper:]' | tr '-' '_')

if [[ "$UPPER_NAME" == "DEFAULT" ]]; then
  SITE_ID="${CLICKY_SITE_ID:?Set CLICKY_SITE_ID env var}"
  SITEKEY="${CLICKY_SITEKEY:?Set CLICKY_SITEKEY env var}"
else
  ID_VAR="CLICKY_${UPPER_NAME}_SITE_ID"
  KEY_VAR="CLICKY_${UPPER_NAME}_SITEKEY"
  SITE_ID="${!ID_VAR:-}"
  SITEKEY="${!KEY_VAR:-}"

  # Fall back to default if named vars not found
  if [[ -z "$SITE_ID" || -z "$SITEKEY" ]]; then
    echo "Error: Set ${ID_VAR} and ${KEY_VAR} environment variables" >&2
    echo "Or use CLICKY_SITE_ID and CLICKY_SITEKEY for a default site" >&2
    exit 1
  fi
fi

TYPE="${1:?Missing type (e.g. visitors,pages,countries)}"
shift

DATE="today"
LIMIT="50"
DAILY=""
OUTPUT="json"
PAGE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --date)    DATE="$2"; shift 2 ;;
    --limit)   LIMIT="$2"; shift 2 ;;
    --daily)   DAILY="1"; shift ;;
    --output)  OUTPUT="$2"; shift 2 ;;
    --page)    PAGE="$2"; shift 2 ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

URL="${API_URL}?site_id=${SITE_ID}&sitekey=${SITEKEY}&type=${TYPE}&date=${DATE}&limit=${LIMIT}&output=${OUTPUT}"
[[ -n "$DAILY" ]] && URL="${URL}&daily=1"
[[ -n "$PAGE" ]] && URL="${URL}&page=${PAGE}"

curl -s "$URL"
