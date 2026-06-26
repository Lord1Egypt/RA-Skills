"""
get_instance_info.py - Get instance detailed info

Get detailed instance information for diagnosis.
"""

import argparse
import json
import sys

from common import client
from common.config import config


def get_instance_info(instance_id: str) -> dict:
    """
    Get instance detailed information.

    Args:
        instance_id: Instance ID
    Returns:
        API JSON response
    """
    return client.get(
        "/drapi/ai/instance/info",
        params={
            "InstanceId": instance_id,
            "UserId": config.user_id,
        },
    )


def main():
    """Command line entry"""
    parser = argparse.ArgumentParser(description="Get detailed instance information for diagnosis")
    parser.add_argument("--instance-id", required=True, help="Instance ID")
    args = parser.parse_args()

    try:
        result = get_instance_info(args.instance_id)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
