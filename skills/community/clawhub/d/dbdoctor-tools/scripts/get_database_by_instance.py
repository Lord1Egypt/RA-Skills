"""
get_database_by_instance.py - Get databases by instance

Get all database list under specified instance.
"""

import argparse
import json
import sys

from common import client
from common.config import config


def get_database_by_instance(instance_id: str) -> dict:
    """
    Get database list under instance.

    Args:
        instance_id: Instance ID
    Returns:
        API JSON response
    """
    return client.get(
        "/draArmor/sqlConsole/queryDbObject",
        params={
            "InstanceId": instance_id,
            "ObjectType": "database",
            "PageSize": 100,
            "StartPage": 1,
            "Role": config.role,
            "UserId": config.user_id,
        },
    )


def main():
    """Command line entry"""
    parser = argparse.ArgumentParser(description="Get all database list under specified instance")
    parser.add_argument("--instance-id", required=True, help="Instance ID")
    args = parser.parse_args()

    try:
        result = get_database_by_instance(args.instance_id)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
