"""
get_current_process.py - Get current processes

Query current database session/process list.
"""

import argparse
import json
import sys

from common import client
from common.config import config


def get_current_process(
    instance_id: str,
    database: str = "",
    sql_keyword: str = "",
) -> dict:
    """
    Get current database session/process list.

    Args:
        instance_id: Instance ID
        database: Database name filter (optional)
        sql_keyword: SQL keyword filter (optional)
    Returns:
        API JSON response
    """
    params = {
        "instanceId": instance_id,
        "UserId": config.user_id,
    }
    if database:
        params["database"] = database
    if sql_keyword:
        params["sql"] = sql_keyword

    return client.get(
        "/drapi/realTimeProcess/query",
        params=params,
    )


def main():
    """Command line entry"""
    parser = argparse.ArgumentParser(description="Query current database session/process list")
    parser.add_argument("--instance-id", required=True, help="Instance ID")
    parser.add_argument("--database", default="", help="Database name filter (optional)")
    parser.add_argument("--sql-keyword", default="", help="SQL keyword filter (optional)")
    args = parser.parse_args()

    try:
        result = get_current_process(args.instance_id, args.database, args.sql_keyword)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
