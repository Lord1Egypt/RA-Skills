#!/usr/bin/env python3
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _cpbl_api import post_api

def probe_game(year, kind, sno):
    print(f"--- Probing Game {sno} ({year}, {kind}) ---")
    
    # Try /box/gamedata
    print("\nTesting /box/gamedata...")
    try:
        res = post_api('/box/gamedata', {
            'year': year,
            'kindCode': kind,
            'gameSno': sno
        })
        print(json.dumps(res, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error calling /box/gamedata: {e}")

    # Try /box/getlive (already used in cpbl_live.py, but let's see everything)
    print("\nTesting /box/getlive...")
    try:
        res = post_api('/box/getlive', {
            'year': year,
            'kindCode': kind,
            'gameSno': sno
        })
        print(json.dumps(res, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error calling /box/getlive: {e}")

if __name__ == "__main__":
    # Test with game 37, 2026-04-15
    probe_game('2026', 'A', '37')
