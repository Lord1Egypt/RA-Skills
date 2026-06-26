"""
execute_sql.py - Execute SQL statement

Execute SQL statement on specified database.
"""

import argparse
import json
import sys

from common import client
from common.config import config


def execute_sql(
    instance_id: str,
    database: str,
    schema: str,
    sql: str,
    engine: str,
    tenant: str,
    project: str,
) -> dict:
    """
    Execute SQL statement.

    Args:
        instance_id: Instance ID
        database: Database name
        schema: Schema name
        sql: SQL statement to execute
        engine: Database engine (mysql/oracle/postgresql)
        tenant: Tenant name
        project: Project name
    Returns:
        API JSON response
    """
    return client.post(
        "/draArmor/sqlConsole/dmsExecuteSql",
        params={
            "Role": config.role,
            "UserId": config.user_id,
        },
        json_body={
            "InstanceId": instance_id,
            "Database": database,
            "Sql": sql,
            "Schema": schema,
            "Engine": engine,
            "PageSize": 100,
            "StartPage": 1,
            "TenantName": tenant,
            "ProjectName": project,
            "Role": config.role,
            "UserId": config.user_id,
        },
    )


def main():
    """Command line entry"""
    parser = argparse.ArgumentParser(description="Execute SQL statement on specified database")
    parser.add_argument("--instance-id", required=True, help="Instance ID")
    parser.add_argument("--database", required=True, help="Database name")
    parser.add_argument("--schema", required=True, help="Schema name")
    parser.add_argument("--sql", required=True, help="SQL statement to execute")
    parser.add_argument("--engine", required=True, help="Database engine (mysql/oracle/postgresql)")
    parser.add_argument("--tenant", required=True, help="Tenant name")
    parser.add_argument("--project", required=True, help="Project name")
    args = parser.parse_args()

    try:
        result = execute_sql(
            instance_id=args.instance_id,
            database=args.database,
            schema=args.schema,
            sql=args.sql,
            engine=args.engine,
            tenant=args.tenant,
            project=args.project,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
