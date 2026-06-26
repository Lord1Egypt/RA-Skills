#!/usr/bin/env python3
from __future__ import annotations
import argparse
from datetime import datetime


def main() -> None:
    parser = argparse.ArgumentParser(description="Compose BUYMA output workbook filename")
    parser.add_argument("--date", help="YYMMDD. Defaults to today")
    parser.add_argument("--start", required=True, help="Start order number")
    parser.add_argument("--end", required=True, help="End order number")
    args = parser.parse_args()
    date_str = args.date or datetime.now().strftime("%y%m%d")
    print(f"tmazonORDERLIST{date_str}_{args.start}-{args.end}.xlsx")


if __name__ == "__main__":
    main()
