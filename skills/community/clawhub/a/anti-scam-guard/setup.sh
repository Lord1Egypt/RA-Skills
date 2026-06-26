#!/bin/bash
# Phishguard OpenClaw Skill - Setup Script
# Verifies dependencies and optionally downloads blocklist data

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
DATA_DIR="$SKILL_DIR/data/blocklist-shards"
GITHUB_REPO="https://raw.githubusercontent.com/phishguard-niki/blocklist-data/main"
SHARDS_INDEX_URL="$GITHUB_REPO/index.json"

echo "🛡️  Phishguard OpenClaw Skill Setup"
echo "===================================="

# Check dependencies
echo ""
echo "Checking dependencies..."

if ! command -v python3 &>/dev/null; then
    echo "❌ Python3 is required. Install: brew install python3"
    exit 1
fi
echo "✅ Python3 found"

if ! command -v curl &>/dev/null; then
    echo "❌ curl is required."
    exit 1
fi
echo "✅ curl found"

# Quick test (uses on-demand GitHub download, no local data needed)
echo ""
echo "Running quick test..."
RESULT=$(python3 "$SKILL_DIR/lib/check_url.py" "fm888.org" 2>&1)
if echo "$RESULT" | grep -q "critical"; then
    echo "✅ Test passed: fm888.org correctly detected as scam"
else
    echo "❌ Test failed. Result: $RESULT"
    exit 1
fi

RESULT=$(python3 "$SKILL_DIR/lib/check_url.py" "google.com" 2>&1)
if echo "$RESULT" | grep -q '"risk_level": "low"'; then
    echo "✅ Test passed: google.com correctly identified as safe"
else
    echo "❌ Test failed. Result: $RESULT"
    exit 1
fi

echo ""
echo "===================================="
echo "✅ Phishguard ready!"
echo ""
echo "Blocklist data is downloaded on-demand from GitHub (cached 1 hour)."
echo "No need to pre-download — just start using it!"
echo ""
echo "Optional: To pre-download all blocklist data for faster offline use, run:"
echo "  bash $SKILL_DIR/setup.sh --download-all"
echo ""

# Optional: download all shards if --download-all flag is passed
if [[ "${1:-}" == "--download-all" ]]; then
    echo "📥 Downloading all blocklist shards from GitHub..."
    mkdir -p "$DATA_DIR"

    # Download index first
    curl -fsSL "$SHARDS_INDEX_URL" -o "$DATA_DIR/index.json"

    # Parse index and download each shard
    SHARD_FILES=$(python3 -c "
import json
with open('$DATA_DIR/index.json') as f:
    idx = json.load(f)
for v in idx.values():
    if isinstance(v, str) and v.endswith('.json'):
        print(v)
    elif isinstance(v, dict) and 'file' in v:
        print(v['file'])
")

    TOTAL=0
    DOWNLOADED=0
    for shard in $SHARD_FILES; do
        TOTAL=$((TOTAL + 1))
    done

    for shard in $SHARD_FILES; do
        DOWNLOADED=$((DOWNLOADED + 1))
        echo "  [$DOWNLOADED/$TOTAL] Downloading $shard..."
        for attempt in 1 2 3; do
            if curl -fsSL --retry 2 --retry-delay 3 "$GITHUB_REPO/$shard" -o "$DATA_DIR/$shard" 2>/dev/null; then
                break
            fi
            if [ "$attempt" -lt 3 ]; then
                echo "    ⏳ Retry $attempt..."
                sleep 3
            else
                echo "    ⚠️  Failed to download $shard (skipped)"
            fi
        done
    done

    DOMAIN_COUNT=$(python3 -c "
import json, glob
total = 0
for f in glob.glob('$DATA_DIR/shard-*.json'):
    try:
        d = json.load(open(f))
        total += len(d.get('domains', []))
    except: pass
print(total)
")
    echo "✅ Downloaded $TOTAL shard files ($DOMAIN_COUNT domains)"
fi
