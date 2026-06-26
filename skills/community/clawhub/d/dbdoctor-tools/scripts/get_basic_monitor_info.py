"""
get_basic_monitor_info.py - Get database monitoring metrics

Get database-level monitoring metrics (MetricFrom=DB).
"""

import argparse
import json
import sys

from common import client
from common.config import config


def get_basic_monitor_info(instance_id: str, start_time: str, end_time: str) -> dict:
    """
    Get database monitoring metrics.

    Args:
        instance_id: Instance ID
        start_time: Start timestamp (Unix seconds)
        end_time: End timestamp (Unix seconds)
    Returns:
        API JSON response
    """
    return client.get(
        "/drapi/ai/getResourceMetricsInNL",
        params={
            "InstanceId": instance_id,
            "StartTime": start_time,
            "EndTime": end_time,
            "MetricFrom": "DB",
            "UserId": config.user_id,
        },
    )


def main():
    """Command line entry"""
    parser = argparse.ArgumentParser(description="Get database-level monitoring metrics")
    parser.add_argument("--instance-id", required=True, help="Instance ID")
    parser.add_argument("--start-time", required=True, help="Start timestamp (Unix seconds)")
    parser.add_argument("--end-time", required=True, help="End timestamp (Unix seconds)")
    args = parser.parse_args()

    try:
        result = get_basic_monitor_info(args.instance_id, args.start_time, args.end_time)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
