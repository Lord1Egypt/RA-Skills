#!/bin/bash
# Market Analysis Wrapper
# Fetches fresh data and outputs a structured prompt for agent analysis

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="${1:-$HOME/market-data}"

echo "🔄 Fetching fresh market data..."
python3 "$SCRIPT_DIR/market-data-fetcher.py" all --output "$OUTPUT_DIR"

echo ""
echo "📊 Market Data Analysis Prompt"
echo "================================"
echo ""
echo "Analyze the market data in the following files:"
echo "  - $OUTPUT_DIR/crypto-latest.json"
echo "  - $OUTPUT_DIR/stocks-latest.json"
echo ""
echo "Focus on:"
echo "  1. Market sentiment (Fear & Greed Index)"
echo "  2. Top movers (biggest 24h gains/losses in crypto)"
echo "  3. Macro environment (DXY, 10Y yields, VIX)"
echo "  4. Notable divergences (crypto vs stocks)"
echo "  5. Trading signals or opportunities"
echo ""
echo "Output a concise market summary (3-5 key points)."
echo ""
echo "Data files ready for analysis:"
ls -lh "$OUTPUT_DIR"/*.json 2>/dev/null || echo "  (No data files found)"
