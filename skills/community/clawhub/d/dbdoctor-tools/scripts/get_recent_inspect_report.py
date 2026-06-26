"""
get_recent_inspect_report.py - Get recent inspection report

Get recent inspection report for instance.
"""

import argparse
import json
import sys

from common import client
from common.config import config


def get_recent_inspect_report(
    instance_id: str,
    start_time: int,
    end_time: int,
    tenant: str,
    project: str,
) -> dict:
    """
    Get recent inspection report.

    Args:
        instance_id: Instance ID
        start_time: Start time (Unix timestamp, seconds)
        end_time: End time (Unix timestamp, seconds)
        tenant: Tenant name
        project: Project name
    Returns:
        API JSON response
    """
    return client.get(
        "/inspect/QueryInstanceReportListV2",
        params={
            "InstanceId": instance_id,
            "StartTime": start_time,
            "EndTime": end_time,
            "Offset": 20,
            "StartNum": 0,
            "TenantName": tenant,
            "ProjectName": project,
            "UserId": config.user_id,
        },
    )


def main():
    """Command line entry"""
    parser = argparse.ArgumentParser(description="Get recent inspection report for instance")
    parser.add_argument("--instance-id", required=True, help="Instance ID")
    parser.add_argument("--start-time", required=True, type=int, help="Start time (Unix timestamp, seconds)")
    parser.add_argument("--end-time", required=True, type=int, help="End time (Unix timestamp, seconds)")
    parser.add_argument("--tenant", required=True, help="Tenant name")
    parser.add_argument("--project", required=True, help="Project name")
    args = parser.parse_args()

    try:
        result = get_recent_inspect_report(
            args.instance_id, args.start_time, args.end_time, args.tenant, args.project
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
