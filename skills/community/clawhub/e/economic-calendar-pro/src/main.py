#!/usr/bin/env python3

# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
#
"""Economic Calendar - Fetch TradingEconomics calendar events for a date range."""

import sys

from mutex import acquire_lock
from service import format_output, get_economic_calendar
from utils import resolve_date_range


def main():
    """Entry point for the economic calendar skill."""
    try:
        start_date, end_date = resolve_date_range(sys.argv[1:])
    except ValueError as exc:
        print(f"Error: {exc}")
        sys.exit(1)

    with acquire_lock():
        result = get_economic_calendar(start_date, end_date)
    print(format_output(result))


if __name__ == "__main__":
    main()
