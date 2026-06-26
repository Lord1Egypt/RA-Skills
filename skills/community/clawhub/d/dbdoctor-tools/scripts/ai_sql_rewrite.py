"""
ai_sql_rewrite.py - AI SQL rewrite

Trigger AI-driven SQL rewrite optimization, return task ID.
"""

import argparse
import json
import sys

from common import client
from common.config import config


def ai_sql_rewrite(instance_id: str, database: str, schema: str, sql: str) -> dict:
    """
    AI SQL rewrite: Submit rewrite task.

    Args:
        instance_id: Instance ID
        database: Database name
        schema: Schema name
        sql: SQL statement to rewrite
    Returns:
        API JSON response (contains task ID)
    """
    return client.post(
        "/drapi/ai/rewriteAsync",
        params={
            "Role": config.role,
            "UserId": config.user_id,
        },
        json_body={
            "sql": sql,
            "instanceId": instance_id,
            "dbName": database,
            "schemaName": schema,
            "userId": config.user_id,
            "userRole": config.role,
        },
    )


def main():
    """Command line entry"""
    parser = argparse.ArgumentParser(description="AI-driven SQL rewrite optimization")
    parser.add_argument("--instance-id", required=True, help="Instance ID")
    parser.add_argument("--database", required=True, help="Database name")
    parser.add_argument("--schema", required=True, help="Schema name")
    parser.add_argument("--sql", required=True, help="SQL statement to rewrite")
    args = parser.parse_args()

    try:
        result = ai_sql_rewrite(args.instance_id, args.database, args.schema, args.sql)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
