"""
get_sql_rewrite_result.py - Get SQL rewrite result

Get the result of SQL rewrite task.
"""

import argparse
import json
import sys

from common import client
from common.config import config


def get_sql_rewrite_result(task_id: str) -> dict:
    """
    Get SQL rewrite result.

    Args:
        task_id: Task ID returned by ai_sql_rewrite
    Returns:
        API JSON response
    """
    return client.get(
        "/drapi/ai/sqlRewriteHistoryDetail",
        params={
            "TaskId": task_id,
            "Role": config.role,
            "UserId": config.user_id,
        },
    )


def main():
    """Command line entry"""
    parser = argparse.ArgumentParser(description="Get SQL rewrite task result")
    parser.add_argument("--task-id", required=True, help="Task ID returned by ai_sql_rewrite")
    args = parser.parse_args()

    try:
        result = get_sql_rewrite_result(args.task_id)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
