#!/bin/bash
# Generate Crypto Daily Report
# Usage: ./generate-report.sh [--send CHANNEL_ID]

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Get prices
get_prices() {
    log_info "Fetching prices..."
    
    # ETH, SOL, BNB via onchainos
    local prices=$(onchainos market prices "1:0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee,501:So11111111111111111111111111111111111111112,56:0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee" 2>/dev/null)
    
    if [ $? -ne 0 ]; then
        log_error "Failed to fetch prices from onchainos"
        return 1
    fi
    
    echo "$prices"
}

# Get BTC price via search (placeholder - actual implementation uses web_search tool)
get_btc_price() {
    log_info "Fetching BTC price..."
    # This is a placeholder - actual BTC price comes from web_search
    echo "69469"
}

# Get Fear & Greed Index
get_fear_greed() {
    log_info "Fetching Fear & Greed Index..."
    
    local data=$(curl -s "https://api.alternative.me/fng/?limit=2" 2>/dev/null)
    
    if [ $? -ne 0 ] || [ -z "$data" ]; then
        log_warn "Failed to fetch Fear & Greed Index"
        echo '{"data":[{"value":"N/A","value_classification":"Unknown"}]}'
        return
    fi
    
    echo "$data"
}

# Main execution
main() {
    log_info "Generating Crypto Daily Report..."
    
    # Get all data
    local prices=$(get_prices)
    local btc_price=$(get_btc_price)
    local fear_greed=$(get_fear_greed)
    
    # TODO: Implement full report generation
    # This script serves as a reference implementation
    # Actual report generation is handled by the AI agent using the skill
    
    log_info "Report data collected successfully"
    
    # Output JSON for agent consumption
    cat <<EOF
{
  "btc_price": "$btc_price",
  "prices": $prices,
  "fear_greed": $fear_greed,
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF
}

main "$@"
