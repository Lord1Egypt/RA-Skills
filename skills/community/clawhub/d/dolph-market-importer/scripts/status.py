#!/usr/bin/env python3
"""Show market importer status and recently imported markets."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from market_importer import load_seen

def main():
    seen = load_seen()
    print(f"🎯 Market Importer Status")
    print(f"   Total imported: {len(seen)}")
    if seen:
        recent = list(seen.items())[-10:]
        print(f"\n   Last {len(recent)} imports:")
        for mid, info in reversed(recent):
            q = info.get("question", mid) if isinstance(info, dict) else mid
            ts = info.get("imported_at", "") if isinstance(info, dict) else ""
            print(f"     • {q}")
            if ts:
                print(f"       {ts}")

if __name__ == "__main__":
    main()
