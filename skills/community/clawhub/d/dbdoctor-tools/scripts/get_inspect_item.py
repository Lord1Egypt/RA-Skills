"""
get_inspect_item.py - Get inspection items

Get available inspection item list, support filtering by engine and type.
"""

import argparse
import json
import sys

from common import client
from common.config import config


def get_inspect_item(engine: str = "", inspect_type: str = "") -> list:
    """
    Get available inspection item list, support filtering.

    Args:
        engine: Database engine filter (optional)
        inspect_type: Inspection item type filter (optional, e.g., performance/resource/config/info)
    Returns:
        Simplified inspection item list
    """
    response = client.get(
        "/inspect/QueryInspectItemList",
        params={"UserId": config.user_id},
    )

    raw_data = response.get("Data", [])
    if not isinstance(raw_data, list):
        return raw_data

    # Filter and simplify data
    result = []
    for item in raw_data:
        # Filter by engine
        if engine and item.get("engine") != engine:
            continue
        # Filter by inspection item type
        if inspect_type and item.get("inspectType") != inspect_type:
            continue

        result.append({
            "desc": item.get("desc", ""),
            "engine": item.get("engine", ""),
            "priority": item.get("priority", ""),
        })

    return result


def main():
    """Command line entry"""
    parser = argparse.ArgumentParser(description="Get available inspection item list")
    parser.add_argument("--engine", default="", help="Database engine filter (optional)")
    parser.add_argument("--inspect-type", default="", help="Inspection item type filter (optional: performance/resource/config/info)")
    args = parser.parse_args()

    try:
        result = get_inspect_item(args.engine, args.inspect_type)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
