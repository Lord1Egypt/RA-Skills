#!/usr/bin/env bash
# smart-search/scripts/reset-quota.sh
# Manually resets the quota file to zero counters for today.
# Useful during testing or if the file gets corrupted.
set -euo pipefail

QUOTA_PATH="${SEARCH_QUOTA_PATH:-$HOME/.openclaw/workspace/shared/search-quota.json}"
TODAY=$(date +%Y-%m-%d)

if [ ! -f "$QUOTA_PATH" ]; then
  echo "[reset-quota] No quota file found at $QUOTA_PATH — nothing to reset."
  exit 0
fi

echo "[reset-quota] Resetting quota file: $QUOTA_PATH"
cp "$QUOTA_PATH" "${QUOTA_PATH}.bak"
echo "[reset-quota] Backup saved: ${QUOTA_PATH}.bak"

cat > "$QUOTA_PATH" << JSON
{
  "date": "$TODAY",
  "providers": {
    "gemini": { "daily_limit": 0, "remaining": 0, "used": 0, "shared_pool": 0 },
    "brave":  { "daily_limit": 0, "remaining": 0, "used": 0, "shared_pool": 0 }
  },
  "agent_allocations": {}
}
JSON

echo "[reset-quota] ✓ Quota reset to zero for $TODAY."
echo "              Limits and allocations will be restored from openclaw.json on the next call."
