#!/bin/bash
# eBay Price Check Wrapper Script

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/scripts/ebay_price_check.py"

if [ $# -lt 1 ]; then
    echo "Usage: ebay-price-check <item_name> [sold]"
    echo "Examples:"
    echo "  ebay-price-check iPhone 14 Pro Max"
    echo "  ebay-price-check MacBook Pro sold"
    exit 1
fi

# Check if python3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is required but not installed"
    exit 1
fi

# Run the Python script
python3 "$PYTHON_SCRIPT" "$@"