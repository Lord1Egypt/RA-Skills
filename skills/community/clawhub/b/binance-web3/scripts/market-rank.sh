#!/bin/bash
# Crypto Market Rank - 市场榜单
# 对应 Skills Hub: crypto-market-rank
# Usage: ./market-rank.sh [type] [chainId]
#
# Types:
#   smart-money  - Smart money signals (聪明钱信号) ✅
#   alpha        - Binance Alpha tokens (需要代理)
#
# Chain IDs:
#   56  - BSC (default)
#   1   - Ethereum

TYPE="${1:-smart-money}"
CHAIN="${2:-56}"
PROXY="${HTTP_PROXY:-http://127.0.0.1:1082}"

usage() {
    echo "Usage: $0 <type> [chainId]"
    echo ""
    echo "Types:"
    echo "  smart-money - Smart money signals (聪明钱信号) ✅"
    echo "  alpha      - Binance Alpha tokens"
    echo ""
    echo "Examples:"
    echo "  $0 smart-money    # BSC"
    echo "  $0 smart-money 1  # Ethereum"
    exit 1
}

if [ -z "$TYPE" ]; then
    usage
fi

echo "=== $TYPE (Chain: $CHAIN) ==="

case "$TYPE" in
    smart-money)
        curl -s -x "$PROXY" \
            "https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/web/signal/smart-money" \
            -H "Accept-Encoding: identity" \
            -H "Content-Type: application/json" \
            -H "Accept: application/json" \
            -d "{\"smartSignalType\":\"\",\"page\":1,\"pageSize\":15,\"chainId\":\"$CHAIN\"}" | jq '.data[]? | {token: .ticker, chain: .chainId, platform: .launchPlatform} ' 2>/dev/null
        ;;
    alpha)
        echo "Binance Alpha API 需要特殊访问权限，暂不可用"
        ;;
    *)
        echo "Unknown type: $TYPE"
        usage
        ;;
esac
