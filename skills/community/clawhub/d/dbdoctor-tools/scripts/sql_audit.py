"""
sql_audit.py - SQL audit

Audit and analyze SQL statements.
Automatically get audit results after submission.
"""

import argparse
import json
import sys
import time

from common import client
from common.config import config


def sql_audit(instance_id: str, database: str, schema: str, sql: str) -> dict:
    """
    SQL audit: Submit audit task and get results.

    Args:
        instance_id: Instance ID
        database: Database name
        schema: Schema name
        sql: SQL statement to audit
    Returns:
        Audit result data (Data field content)
    """
    # Step 1: Submit audit task
    submit_resp = client.post(
        "/drapi/sqlAudit/submit",
        params={"UserId": config.user_id},
        json_body={
            "auditType": "Manual",
            "database": database,
            "insName": instance_id,
            "schema": schema,
            "sql": sql,
        },
    )

    # Extract TaskId from submit response
    task_id = submit_resp.get("data", {}).get("taskId") or submit_resp.get("data", {}).get("TaskId")
    if not task_id:
        return {"error": "Failed to submit audit task", "response": submit_resp}

    # Step 2: Get audit result (retry up to 10 times, 2 seconds interval)
    for _ in range(10):
        time.sleep(2)
        result_resp = client.get(
            "/drapi/sqlAudit/sqlAuditResult",
            params={
                "TaskId": task_id,
                "SeqNo": 1,
                "UserId": config.user_id,
            },
        )
        # Return Data if result is ready
        if result_resp.get("success") and result_resp.get("data"):
            return result_resp.get("data", {})

    # Return last result data after timeout
    return result_resp.get("data", {})


def main():
    """Command line entry"""
    parser = argparse.ArgumentParser(description="Audit and analyze SQL statements")
    parser.add_argument("--instance-id", required=True, help="Instance ID")
    parser.add_argument("--database", required=True, help="Database name")
    parser.add_argument("--schema", required=True, help="Schema name")
    parser.add_argument("--sql", required=True, help="SQL statement to audit")
    args = parser.parse_args()

    try:
        result = sql_audit(args.instance_id, args.database, args.schema, args.sql)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
