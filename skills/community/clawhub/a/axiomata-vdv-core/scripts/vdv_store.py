#!/usr/bin/env python3
"""
VDV Store v1.0 — Local JSON Storage
Stores VDV analysis results to local JSON file (no Qdrant required).
"""

import sys
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional


def store_to_json(content: str, vtype: str = "vdv", tags: list = None, 
                  storage_path: str = "vdv_results.json") -> Dict:
    """Store result in local JSON file."""
    
    payload = {
        "type": vtype,
        "content": content,
        "tags": tags or [],
        "timestamp": datetime.now().isoformat()
    }
    
    results = []
    p = Path(storage_path)
    if p.exists():
        try:
            with open(p) as f:
                results = json.load(f)
        except json.JSONDecodeError:
            results = []
    
    results.append(payload)
    
    # Keep last 100 results
    results = results[-100:]
    
    with open(p, "w") as f:
        json.dump(results, f, indent=2)
    
    return {"status": "stored", "path": str(p.absolute()), "count": len(results)}


def load_results(storage_path: str = "vdv_results.json", limit: int = 10) -> list:
    """Load recent VDV results."""
    p = Path(storage_path)
    if not p.exists():
        return []
    
    with open(p) as f:
        results = json.load(f)
    
    return results[-limit:]


def main():
    parser = argparse.ArgumentParser(description="VDV Store v1.0")
    parser.add_argument("--content", "-c", required=True, help="Content to store")
    parser.add_argument("--type", "-t", default="vdv", help="Result type")
    parser.add_argument("--tags", nargs="*", help="Tags")
    parser.add_argument("--path", "-p", default="vdv_results.json", help="Storage path")
    parser.add_argument("--load", "-l", action="store_true", help="Load recent results")
    parser.add_argument("--limit", "-n", type=int, default=10, help="Number of results to load")
    
    args = parser.parse_args()
    
    if args.load:
        results = load_results(args.path, args.limit)
        print(json.dumps(results, indent=2))
        return 0
    
    result = store_to_json(args.content, args.type, args.tags, args.path)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())