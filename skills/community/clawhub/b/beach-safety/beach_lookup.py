#!/usr/bin/env python3
"""
Beach Safety Lookup CLI
Quick beach conditions from the command line.

Usage:
    python3 beach_lookup.py "Miami Beach"
    python3 beach_lookup.py "Waikiki Beach, Oahu"
    python3 beach_lookup.py "Bondi Beach, Sydney"
"""

import sys
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))
from server import get_comprehensive_report, format_report_text, geocode_beach

async def main():
    if len(sys.argv) < 2:
        print("Usage: python3 beach_lookup.py \"Beach Name\"")
        print("Example: python3 beach_lookup.py \"Waikiki\"")
        return

    beach_name = " ".join(sys.argv[1:])

    print(f"Looking up {beach_name}...")
    display_name, lat, lon = await geocode_beach(beach_name)

    if lat == 0.0 and lon == 0.0:
        print(f"Beach not found: {beach_name}")
        print("Try adding a state/country, e.g., 'Venice Beach, CA' or 'Bondi Beach, Sydney'")
        return

    beach_name = display_name
    print(f"Found: {display_name}")

    report = await get_comprehensive_report(beach_name, lat, lon)
    print(format_report_text(report))

if __name__ == "__main__":
    asyncio.run(main())
