#!/bin/bash
# Whale transaction tracker using Whale Alert free API and Etherscan
set -euo pipefail

usage() {
    cat << EOF
Usage: whale.sh [options]

Options:
  -m, --min-value N   Minimum transaction value in USD (default: 1000000)
  -c, --chain CHAIN   Chain: ethereum|bitcoin|all (default: all)
  -l, --limit N       Max results (default: 20)
  -h, --help          Show this help
EOF
}

MIN_VALUE=1000000
CHAIN="all"
LIMIT=20

while [[ $# -gt 0 ]]; do
    case "$1" in
        -m|--min-value) MIN_VALUE="$2"; shift 2 ;;
        -c|--chain) CHAIN="$2"; shift 2 ;;
        -l|--limit) LIMIT="$2"; shift 2 ;;
        -h|--help) usage; exit 0 ;;
        *) shift ;;
    esac
done

# Try whale-alert.io free API
fetch_whale_alert() {
    local url="https://api.whale-alert.io/v1/transactions?api_key=free&min_value=${MIN_VALUE}&limit=${LIMIT}"
    
    local result
    result=$(curl -sf --connect-timeout 10 "$url" 2>/dev/null) || {
        echo '{"status":"error","message":"Whale Alert API unavailable"}' 
        return 1
    }
    
    echo "$result" | jq -r '
        if .result == "error" then
            "⚠️  Whale Alert API limit reached (free tier: 10 calls/min)"
        else
            .transactions[]? | 
            "🐋 \(.amount) \(.symbol) ($\(.amount_usd)) | \(.from.owner_type // "unknown") → \(.to.owner_type // "unknown") | \(.blockchain) | \(.timestamp | strftime("%Y-%m-%d %H:%M"))"
        end
    ' 2>/dev/null || echo "No whale transactions found"
}

# Etherscan large transfers (free, no API key for basic)
fetch_etherscan_whales() {
    echo "🐋 Ethereum large transfers (last 100 blocks):"
    
    # Use etherscan API for latest block transactions
    local latest_block
    latest_block=$(curl -sf "https://api.etherscan.io/api?module=proxy&action=eth_blockNumber" 2>/dev/null | jq -r '.result // "0"' 2>/dev/null)
    
    if [[ "$latest_block" == "0" || -z "$latest_block" ]]; then
        echo "⚠️  Etherscan API unavailable"
        return
    fi
    
    # Convert hex to decimal
    local block_dec=$((latest_block))
    local count=0
    
    for ((i=0; i<20; i++)); do
        local bn=$((block_dec - i))
        local hex_bn
        hex_bn=$(printf "0x%x" "$bn")
        
        local block
        block=$(curl -sf "https://api.etherscan.io/api?module=proxy&action=eth_getBlockByNumber&tag=$hex_bn&boolean=true" 2>/dev/null)
        
        echo "$block" | jq -r '
            .result.transactions[]? | 
            select((.value | tonumber) > 10000000000000000000) |  # > 10 ETH
            "🐋 \((.value | tonumber / 1000000000000000000 * 100 | round / 100)) ETH | \(.from[0:10])... → \(.to[0:10])... | block \(.blockNumber)"
        ' 2>/dev/null | head -5
        
        count=$((count + 1))
        [[ $count -ge $LIMIT ]] && break
    done
}

echo "=== Whale Tracker ==="
echo "Min value: \$$MIN_VALUE | Chain: $CHAIN"
echo ""

fetch_whale_alert
echo ""
fetch_etherscan_whales

echo ""
echo "💡 Free tier limits apply. For production use, get API keys from whale-alert.io and etherscan.io"
