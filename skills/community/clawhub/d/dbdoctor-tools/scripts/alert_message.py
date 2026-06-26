"""
alert_message.py - Get alert overview

Get alert message overview.
"""

import argparse
import json
import sys

from common import client
from common.config import config


def alert_message(
    status: str = "",
    priority: str = "",
    event_name: str = "",
    instance_ip: str = "",
    instance_desc: str = "",
    create_time: str = "",
    modified_time: str = "",
) -> dict:
    """
    Get alert message overview.

    Args:
        status: Alert status (alarming/recovered, optional)
        priority: Alert priority (serious/warning/info, optional)
        event_name: Event name filter (optional)
        instance_ip: Instance IP filter (optional)
        instance_desc: Instance description filter (optional)
        create_time: Create time filter (optional)
        modified_time: Modified time filter (optional)
    Returns:
        API JSON response
    """
    params = {
        "StartPage": 1,
        "PageSize": 100,
        "UserId": config.user_id,
    }
    if status:
        params["Status"] = status
    if priority:
        params["Priority"] = priority
    if event_name:
        params["EventNameCn"] = event_name
    if instance_ip:
        params["InstanceIp"] = instance_ip
    if instance_desc:
        params["InstanceDesc"] = instance_desc
    if create_time:
        params["CreateTime"] = create_time
    if modified_time:
        params["ModifiedTime"] = modified_time

    return client.get(
        "/drapi/alertV2/alertEventList",
        params=params,
    )


def main():
    """Command line entry"""
    parser = argparse.ArgumentParser(description="Get alert message overview")
    parser.add_argument("--status", default="", choices=["", "alarming", "recovered"],
                        help="Alert status (alarming/recovered, optional)")
    parser.add_argument("--priority", default="", choices=["", "serious", "warning", "info"],
                        help="Alert priority (serious/warning/info, optional)")
    parser.add_argument("--event-name", default="", help="Event name filter (optional)")
    parser.add_argument("--instance-ip", default="", help="Instance IP filter (optional)")
    parser.add_argument("--instance-desc", default="", help="Instance description filter (optional)")
    parser.add_argument("--create-time", default="", help="Create time filter (optional)")
    parser.add_argument("--modified-time", default="", help="Modified time filter (optional)")
    args = parser.parse_args()

    try:
        result = alert_message(
            status=args.status,
            priority=args.priority,
            event_name=args.event_name,
            instance_ip=args.instance_ip,
            instance_desc=args.instance_desc,
            create_time=args.create_time,
            modified_time=args.modified_time,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
