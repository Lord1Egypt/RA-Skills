"""
get_instance_abnormal.py - Get instance abnormal info

Get abnormal/alert information for specified instance.
"""

import argparse
import json
import sys

from common import client


def get_instance_abnormal(instance_id: str) -> dict:
    """
    Get instance abnormal information.

    Args:
        instance_id: Instance ID
    Returns:
        API JSON response
    """
    return client.get(
        "/drapi/ai/instranceMessageAbnormal",
        params={"instanceId": instance_id},
    )


def main():
    """Command line entry"""
    parser = argparse.ArgumentParser(description="Get abnormal/alert information for specified instance")
    parser.add_argument("--instance-id", required=True, help="Instance ID")
    args = parser.parse_args()

    try:
        result = get_instance_abnormal(args.instance_id)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
