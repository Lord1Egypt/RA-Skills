#!/usr/bin/env python3

# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "yfinance",
# ]
# ///

"""
Commodities price checker - WTI, Brent, Natural Gas, Gold using yfinance.
"""

import sys

from mutex import acquire_lock
from service import get_commodity_price, format_output


def main():
    if len(sys.argv) < 2:
        print("Usage: commodities <SYMBOL>")
        sys.exit(1)

    symbol = sys.argv[1].upper()
    with acquire_lock():
        result = get_commodity_price(symbol)
    print(format_output(result))


if __name__ == "__main__":
    main()
