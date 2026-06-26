"""
performance_diagnosis.py - Database performance comprehensive diagnosis

Perform comprehensive performance diagnosis on database for specified time period,
integrating multiple diagnosis dimensions:
- Instance basic info
- Slow SQL analysis
- Abnormal SQL analysis
- AAS active session statistics
- Resource monitoring metrics (database and host)

Using actual API endpoints:
- /drapi/ai/instance/info
- /drapi/ai/getSlowSqlByTime
- /drapi/ai/getAbnormalSqlByTime
- /drapi/ai/activeSession/statistics
- /drapi/ai/getResourceMetricsInNL
"""

import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

from common import client
from common.config import config


def get_instance_info(instance_id: str) -> dict:
    """Get instance detailed info"""
    return client.get(
        "/drapi/ai/instance/info",
        params={"InstanceId": instance_id, "UserId": config.user_id},
    )


def get_slow_sql(instance_id: str, start_time: str, end_time: str) -> dict:
    """Get slow SQL (diagnosis version)"""
    return client.get(
        "/drapi/ai/getSlowSqlByTime",
        params={
            "InstanceId": instance_id,
            "StartTime": start_time,
            "EndTime": end_time,
            "UserId": config.user_id,
        },
    )


def get_related_sql(instance_id: str, start_time: str, end_time: str) -> dict:
    """Get root cause SQL (abnormal SQL)"""
    return client.get(
        "/drapi/ai/getAbnormalSqlByTime",
        params={
            "InstanceId": instance_id,
            "StartTime": start_time,
            "EndTime": end_time,
            "UserId": config.user_id,
        },
    )


def get_aas_info(instance_id: str, start_time: str, end_time: str) -> dict:
    """Get AAS active session statistics"""
    return client.get(
        "/drapi/ai/getAASInfo",
        params={
            "InstanceId": instance_id,
            "StartTime": start_time,
            "EndTime": end_time,
            "UserId": config.user_id,
        },
    )


def get_resource_metrics(instance_id: str, start_time: str, end_time: str) -> dict:
    """Get resource monitoring metrics (database and host)"""
    return client.get(
        "/drapi/ai/getResourceMetricsInNL",
        params={
            "InstanceId": instance_id,
            "StartTime": start_time,
            "EndTime": end_time,
            "UserId": config.user_id,
        },
    )


def performance_diagnosis(
    instance_id: str, start_time: str, end_time: str
) -> dict:
    """
    Execute comprehensive performance diagnosis.

    Args:
        instance_id: Instance ID
        start_time: Start timestamp (Unix seconds)
        end_time: End timestamp (Unix seconds)
    Returns:
        Comprehensive diagnosis result
    """
    # Define diagnosis tasks
    tasks = {
        "instanceInfo": lambda: get_instance_info(instance_id),
        "slowSql": lambda: get_slow_sql(instance_id, start_time, end_time),
        "abnormalSql": lambda: get_related_sql(instance_id, start_time, end_time),
        "aasInfo": lambda: get_aas_info(instance_id, start_time, end_time),
        "resourceMetrics": lambda: get_resource_metrics(instance_id, start_time, end_time),
    }

    results = {}
    errors = {}

    # Execute all diagnosis tasks in parallel
    with ThreadPoolExecutor(max_workers=6) as executor:
        future_to_name = {
            executor.submit(task): name for name, task in tasks.items()
        }
        for future in as_completed(future_to_name):
            name = future_to_name[future]
            try:
                results[name] = future.result()
            except Exception as e:
                errors[name] = str(e)

    # Build diagnosis report
    diagnosis_report = {
        "diagnosisTime": {
            "startTime": start_time,
            "endTime": end_time,
        },
        "instanceInfo": results.get("instanceInfo", {}),
        "performanceMetrics": {
            "slowSql": results.get("slowSql", {}),
            "abnormalSql": results.get("abnormalSql", {}),
            "aasInfo": results.get("aasInfo", {}),
        },
        "resourceMetrics": results.get("resourceMetrics", {}),
    }

    if errors:
        diagnosis_report["errors"] = errors

    return diagnosis_report


def main():
    """Command line entry"""
    parser = argparse.ArgumentParser(
        description="Database performance comprehensive diagnosis - Integrate multiple diagnosis dimensions"
    )
    parser.add_argument("--instance-id", required=True, help="Instance ID")
    parser.add_argument(
        "--start-time", required=True, help="Start timestamp (Unix seconds)"
    )
    parser.add_argument(
        "--end-time", required=True, help="End timestamp (Unix seconds)"
    )
    args = parser.parse_args()

    try:
        result = performance_diagnosis(
            args.instance_id, args.start_time, args.end_time
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
