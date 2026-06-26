#!/usr/bin/env python3

# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "yfinance",
# ]
# ///
#
"""
Earnings Countdown - Fetch the next earnings date for a stock ticker.

Usage:
    uv run main.py <TICKER>
"""

import sys

from service import format_output, get_next_earnings_date


def main():
    """Entry point - expects a stock ticker symbol as the first CLI argument."""
    if len(sys.argv) < 2:
        print("Usage: event-countdown-pro <SYMBOL>")
        sys.exit(1)

    symbol = sys.argv[1].upper()
    result = get_next_earnings_date(symbol)
    print(format_output(result))


if __name__ == "__main__":
    main()
