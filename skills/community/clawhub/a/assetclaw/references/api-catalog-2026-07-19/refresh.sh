#!/bin/bash
# Refresh the AssetHub API catalog snapshots from the live backend.
# Usage: bash references/api-catalog-2026-07-19/refresh.sh [base_url]
#   base_url defaults to http://127.0.0.1:5183

set -e
BASE_URL="${1:-http://127.0.0.1:5183}"
OUT_DIR="$(cd "$(dirname "$0")" && pwd)"
TS=$(date -u +"%Y-%m-%dT%H:%M:%S.000Z")

echo "[refresh] target: $BASE_URL"
echo "[refresh] output: $OUT_DIR"
echo "[refresh] timestamp: $TS"

# 1. Endpoint catalog (raw, by module)
echo "[refresh] capturing endpoint catalog..."
curl -sS -m 30 "$BASE_URL/api/api-documentation/modules" \
  -H "Accept: application/json" \
  -o "$OUT_DIR/_raw-modules.json" 2>/dev/null || echo "  (modules endpoint requires auth, skipping)"

curl -sS -m 30 "$BASE_URL/api/api-documentation/endpoints" \
  -H "Accept: application/json" \
  -o "$OUT_DIR/_raw-endpoints.json" 2>/dev/null || echo "  (endpoints endpoint requires auth, skipping)"

# 2. Per-module endpoint dump (no-auth, public module doc)
echo "[refresh] capturing per-module endpoint snapshots..."
for mod in health dashboard assets maintenance inventory scrapping; do
  curl -sS -m 10 "$BASE_URL/api/api-documentation/module/$mod" \
    -H "Accept: application/json" \
    -o "$OUT_DIR/_raw-$mod.json" 2>/dev/null && echo "  ✓ $mod" || echo "  ✗ $mod (skip)"
done

echo "[refresh] done. Authenticated modules need to be captured via:"
echo "  bash scripts/assethub_api.sh modules > $OUT_DIR/modules-list.txt"
