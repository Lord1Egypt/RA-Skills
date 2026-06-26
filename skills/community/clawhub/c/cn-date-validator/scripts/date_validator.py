#!/usr/bin/env python3

import argparse, json, sys, re
from datetime import datetime

def validate_date(s):
    formats = ["%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y", "%d/%m/%Y", "%m/%d/%Y"]
    for fmt in formats:
        try:
            d = datetime.strptime(s, fmt)
            return {"valid": True, "format": fmt, "year": d.year, "month": d.month, "day": d.day, "weekday": d.strftime("%A")}
        except:
            pass
    return {"valid": False, "error": "Invalid date format"}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    args = parser.parse_args()
    print(json.dumps(validate_date(args.date), ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
