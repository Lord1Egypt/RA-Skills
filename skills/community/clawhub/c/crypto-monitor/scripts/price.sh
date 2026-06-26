#!/bin/bash
# crypto-monitor/scripts/price.sh
# Real-time cryptocurrency price fetcher using CoinGecko free API
set -euo pipefail

API_BASE="https://api.coingecko.com/api/v3"
CACHE_DIR="${HOME}/.cache/crypto-monitor"
CACHE_TTL=60  # seconds

# Ensure jq is available
command -v jq >/dev/null 2>&1 || { echo "Installing jq..." >&2; apt-get install -y -qq jq 2>/dev/null || true; }

usage() {
    cat << EOF
Usage: price.sh [options] [coin_ids...]

Options:
  -t, --top N       Show top N coins by market cap (default: 10)
  -c, --convert CURR  Convert to currency (default: usd)
  -f, --format FMT  Output format: text|json|csv (default: text)
  -w, --watch SEC   Watch mode, refresh every SEC seconds
  -h, --help        Show this help

Examples:
  price.sh bitcoin ethereum
  price.sh --top 5
  price.sh bitcoin --format json
  price.sh --top 3 --watch 30
EOF
}

# Parse args
TOP=10
CURRENCY="usd"
FORMAT="text"
WATCH=0
COINS=()

while [[ $# -gt 0 ]]; do
    case "$1" in
        -t|--top) TOP="$2"; shift 2 ;;
        -c|--convert) CURRENCY="$2"; shift 2 ;;
        -f|--format) FORMAT="$2"; shift 2 ;;
        -w|--watch) WATCH="$2"; shift 2 ;;
        -h|--help) usage; exit 0 ;;
        *) COINS+=("$1"); shift ;;
    esac
done

fetch_prices() {
    local url
    if [[ ${#COINS[@]} -gt 0 ]]; then
        local ids
        ids=$(IFS=,; echo "${COINS[*]}")
        url="${API_BASE}/simple/price?ids=${ids}&vs_currencies=${CURRENCY}&include_24hr_change=true&include_market_cap=true&include_24hr_vol=true"
    else
        url="${API_BASE}/coins/markets?vs_currency=${CURRENCY}&order=market_cap_desc&per_page=${TOP}&page=1&sparkline=false&price_change_percentage=24h"
    fi

    curl -sf --connect-timeout 10 "$url" 2>/dev/null || {
        echo '{"error": "API request failed. Rate limit may be reached."}' >&2
        return 1
    }
}

output_text() {
    local data="$1"
    
    if [[ ${#COINS[@]} -gt 0 ]]; then
        # Simple price mode
        for coin in "${COINS[@]}"; do
            local price change mcap vol
            price=$(echo "$data" | jq -r ".[\"$coin\"].${CURRENCY} // \"N/A\"")
            change=$(echo "$data" | jq -r ".[\"$coin\"].${CURRENCY}_24h_change // 0")
            mcap=$(echo "$data" | jq -r ".[\"$coin\"].${CURRENCY}_market_cap // 0")
            vol=$(echo "$data" | jq -r ".[\"$coin\"].${CURRENCY}_24h_vol // 0")
            
            local sign="" arrow=""
            if (( $(echo "$change > 0" | bc -l 2>/dev/null || echo 1) )); then
                sign="+"; arrow="📈"
            elif (( $(echo "$change < 0" | bc -l 2>/dev/null || echo 0) )); then
                arrow="📉"
            else
                arrow="➡️"
            fi
            
            printf "%s %s: \$%'.2f (%s%.1f%% 24h) | Vol: \$%'.0f | MCap: \$%'.0f\n" \
                "$arrow" "${coin^}" "$price" "$sign" "$change" "$(( $(printf '%.0f' "$vol") ))" "$(( $(printf '%.0f' "$mcap") ))"
        done
    else
        # Top N mode
        local count=0
        echo "$data" | jq -r '.[] | [.market_cap_rank, .symbol, .current_price, .price_change_percentage_24h, .market_cap, .total_volume] | @tsv' | \
        while IFS=$'\t' read -r rank symbol price change mcap vol; do
            count=$((count + 1))
            if [[ "$count" -gt "$TOP" ]]; then break; fi
            
            local arrow=""
            if (( $(echo "$change > 0" | bc -l 2>/dev/null || echo 0) )); then
                arrow="📈"
            elif (( $(echo "$change < 0" | bc -l 2>/dev/null || echo 0) )); then
                arrow="📉"
            else
                arrow="➡️"
            fi
            
            local sign=""
            (( $(echo "$change > 0" | bc -l 2>/dev/null || echo 0) )) && sign="+"
            
            printf "%s #%s %s: \$%'.2f (%s%.1f%%) | MCap: \$%'.0f | Vol: \$%'.0f\n" \
                "$arrow" "$rank" "${symbol^^}" "$price" "$sign" "$change" "$(( $(printf '%.0f' "$mcap") ))" "$(( $(printf '%.0f' "$vol") ))"
        done
    fi
}

output_json() {
    echo "$1" | jq '.'
}

output_csv() {
    local data="$1"
    if [[ ${#COINS[@]} -gt 0 ]]; then
        echo "coin,price,change_24h,market_cap,volume_24h"
        for coin in "${COINS[@]}"; do
            local price change mcap vol
            price=$(echo "$data" | jq -r ".[\"$coin\"].${CURRENCY} // \"\"" )
            change=$(echo "$data" | jq -r ".[\"$coin\"].${CURRENCY}_24h_change // \"\"" )
            mcap=$(echo "$data" | jq -r ".[\"$coin\"].${CURRENCY}_market_cap // \"\"" )
            vol=$(echo "$data" | jq -r ".[\"$coin\"].${CURRENCY}_24h_vol // \"\"" )
            echo "$coin,$price,$change,$mcap,$vol"
        done
    else
        echo "rank,symbol,price,change_24h,market_cap,volume_24h"
        echo "$data" | jq -r '.[] | [.market_cap_rank, .symbol, .current_price, .price_change_percentage_24h, .market_cap, .total_volume] | @csv'
    fi
}

main() {
    while true; do
        DATA=$(fetch_prices) || { echo "❌ Failed to fetch prices"; exit 1; }
        
        case "$FORMAT" in
            json) output_json "$DATA" ;;
            csv)  output_csv "$DATA" ;;
            *)    output_text "$DATA" ;;
        esac
        
        [[ "$WATCH" -gt 0 ]] && sleep "$WATCH" || break
    done
}

main
