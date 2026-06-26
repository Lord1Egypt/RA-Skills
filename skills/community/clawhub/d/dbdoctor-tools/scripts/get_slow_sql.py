"""
get_slow_sql.py - Get slow SQL list

Get slow SQL queries within specified time range, return key fields only.
"""

import argparse
import json
import sys

from common import client
from common.config import config


def simplify_slow_sql_data(raw_data: list) -> list:
    """
    Simplify slow SQL data, extract key fields only.

    Args:
        raw_data: Raw slow SQL list
    Returns:
        Simplified data list
    """
    if not isinstance(raw_data, list):
        return raw_data

    simplified_data = []
    for sql_item in raw_data:
        sql_text = sql_item.get("sqlText", "")
        # Truncate overly long SQL text
        if len(sql_text) > 4000:
            sql_text = sql_text[:4000]

        simplified_item = {
            "sqlText": sql_text,
            "database": sql_item.get("database", ""),
            "number": sql_item.get("number", 0),
            "aveExecTime": sql_item.get("aveExecTime", 0),
            "maxExecTime": sql_item.get("maxExecTime", 0),
            "totalExecTime": sql_item.get("totalExecTime", 0),
            "aveLockWaitTime": sql_item.get("aveLockWaitTime"),
            "maxLockWaitTime": sql_item.get("maxLockWaitTime"),
        }
        simplified_data.append(simplified_item)

    return simplified_data


def get_slow_sql(instance_id: str, start_time: str, end_time: str) -> list:
    """
    Get slow SQL list, return key fields only.

    Args:
        instance_id: Instance ID
        start_time: Start time (Unix timestamp, seconds)
        end_time: End time (Unix timestamp, seconds)
    Returns:
        Simplified slow SQL list
    """
    response = client.get(
        "/drapi/GetsSlowSqlDigest",
        params={
            "InstanceId": instance_id,
            "StartTime": start_time,
            "EndTime": end_time,
            "SqlHash": "",
            "UserId": config.user_id,
        },
    )

    # Extract Data field
    raw_data = response.get("Data", {})

    # Simplify data
    return simplify_slow_sql_data(raw_data)


def main():
    """Command line entry"""
    parser = argparse.ArgumentParser(description="Get slow SQL list within specified time range")
    parser.add_argument("--instance-id", required=True, help="Instance ID")
    parser.add_argument("--start-time", required=True, help="Start time (Unix timestamp, seconds)")
    parser.add_argument("--end-time", required=True, help="End time (Unix timestamp, seconds)")
    args = parser.parse_args()

    try:
        result = get_slow_sql(args.instance_id, args.start_time, args.end_time)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
