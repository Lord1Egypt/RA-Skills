#!/usr/bin/env bash
# sync-trust-db.sh — Download the latest trust database from CDN.
#
# Usage:
#   sync-trust-db.sh           — Download trust.json from configured CDN URL
#   sync-trust-db.sh --force   — Download even if recently synced
#   sync-trust-db.sh --url URL — Download from a specific URL

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DATA_DIR="$SCRIPT_DIR/../data"
DB_PATH="$DATA_DIR/trust.json"
CONFIG_PATH="$DATA_DIR/config.json"

mkdir -p "$DATA_DIR"

# Parse arguments
FORCE=false
CUSTOM_URL=""
while [ $# -gt 0 ]; do
  case "$1" in
    --force) FORCE=true; shift ;;
    --url) CUSTOM_URL="$2"; shift 2 ;;
    *) echo "Unknown argument: $1" >&2; exit 1 ;;
  esac
done

# Read CDN URL from config or use default
if [ -n "$CUSTOM_URL" ]; then
  CDN_URL="$CUSTOM_URL"
elif [ -f "$CONFIG_PATH" ]; then
  CDN_URL=$(node --input-type=module -e "
    import { readFileSync } from 'node:fs';
    try {
      const c = JSON.parse(readFileSync('${CONFIG_PATH}', 'utf-8'));
      console.log(c.trust_db_url || 'https://api.fraud-filter.com/trust.json');
    } catch { console.log('https://api.fraud-filter.com/trust.json'); }
  ")
else
  CDN_URL="https://api.fraud-filter.com/trust.json"
fi

# Check if we should skip (synced within last 24 hours)
if [ "$FORCE" = false ] && [ -f "$DB_PATH" ]; then
  AGE_HOURS=$(node --input-type=module -e "
    import { statSync } from 'node:fs';
    const age = (Date.now() - statSync('${DB_PATH}').mtimeMs) / 3600000;
    console.log(Math.floor(age));
  ")
  if [ "$AGE_HOURS" -lt 24 ]; then
    echo "Trust DB is ${AGE_HOURS}h old (< 24h). Use --force to re-download."
    exit 0
  fi
fi

echo "Downloading trust database from: $CDN_URL"

# Download using Node's built-in fetch (Node 18+, already required by this skill).
# No curl or wget dependency.
TEMP_PATH="$DB_PATH.tmp"
if node --input-type=module -e "
  import { writeFileSync } from 'node:fs';
  const res = await fetch('${CDN_URL}', {
    headers: { 'User-Agent': 'fraud-filter-skill/1.0' },
    signal: AbortSignal.timeout(15_000),
  });
  if (!res.ok) throw new Error('HTTP ' + res.status);
  const data = await res.json();
  if (!data.endpoints) throw new Error('missing endpoints field');
  writeFileSync('${TEMP_PATH}', JSON.stringify(data));
  console.log('Valid: ' + Object.keys(data.endpoints).length + ' endpoints');
" 2>&1; then
  mv "$TEMP_PATH" "$DB_PATH"
  chmod 600 "$DB_PATH"
  echo "Trust database updated successfully."
else
  rm -f "$TEMP_PATH"
  echo "Error: download or validation failed" >&2
  exit 1
fi
