#!/bin/bash
# Airdrop radar - check known airdrop sources
set -euo pipefail

echo "=== 🪂 Airdrop Radar ==="
echo "⚠️  Always verify airdrops independently. Never share private keys or seed phrases."
echo ""

# Check DefiLlama airdrops
echo "📡 Checking DeFiLlama airdrops..."
data=$(curl -sf --connect-timeout 10 "https://api.llama.fi/airdrops" 2>/dev/null) || {
    echo "⚠️  DeFiLlama API unavailable"
    data="[]"
}

echo "$data" | jq -r '
    .data[:5][]? | 
    "🪂 \(.name) | \(.protocol // .project) | Status: \(.status // "unknown") | \(.url // "")"
' 2>/dev/null || echo "No active airdrops found"

echo ""
echo "=== Tips ==="
echo "• Track airdrop eligibility on: https://earni.fi"
echo "• Follow airdrop hunters on X/Twitter"
echo "• Use DappRadar for new DeFi protocols"
echo "• NEVER pay gas fees to 'claim' an airdrop (scam!)"
