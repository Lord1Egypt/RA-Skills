"""
get_aas_info.py - Get AAS (Active Session Statistics)

Get active session statistics summary.
"""

import argparse
import json
import sys

from common import client
from common.config import config


def get_aas_info(instance_id: str, start_time: str, end_time: str) -> dict:
    """
    Get active session statistics (AAS).

    Args:
        instance_id: Instance ID
        start_time: Start timestamp (Unix seconds)
        end_time: End timestamp (Unix seconds)
    Returns:
        API JSON response
    """
    return client.get(
        "/drapi/ai/activeSession/statistics",
        params={
            "InstanceId": instance_id,
            "StartTime": start_time,
            "EndTime": end_time,
            "UserId": config.user_id,
        },
    )


def main():
    """Command line entry"""
    parser = argparse.ArgumentParser(description="Get active session statistics (AAS)")
    parser.add_argument("--instance-id", required=True, help="Instance ID")
    parser.add_argument("--start-time", required=True, help="Start timestamp (Unix seconds)")
    parser.add_argument("--end-time", required=True, help="End timestamp (Unix seconds)")
    args = parser.parse_args()

    try:
        result = get_aas_info(args.instance_id, args.start_time, args.end_time)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
