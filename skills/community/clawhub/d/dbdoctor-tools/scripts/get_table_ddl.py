"""
get_table_ddl.py - Get table DDL

Get structure definition of specified table.
"""

import argparse
import json
import sys

from common import client
from common.config import config


def get_table_ddl(instance_id: str, database: str, schema: str, table: str) -> dict:
    """
    Get table DDL structure definition.

    Args:
        instance_id: Instance ID
        database: Database name
        schema: Schema name (same as database name for MySQL)
        table: Table name
    Returns:
        API JSON response
    """
    return client.get(
        "/draArmor/sqlConsole/queryDdlText",
        params={
            "InstanceId": instance_id,
            "Database": database,
            "Schema": schema,
            "ObjectType": "table",
            "ObjectName": table,
            "Role": config.role,
            "UserId": config.user_id,
        },
    )


def main():
    """Command line entry"""
    parser = argparse.ArgumentParser(description="Get DDL structure definition of specified table")
    parser.add_argument("--instance-id", required=True, help="Instance ID")
    parser.add_argument("--database", required=True, help="Database name")
    parser.add_argument("--schema", required=True, help="Schema name (same as database name for MySQL)")
    parser.add_argument("--table", required=True, help="Table name")
    args = parser.parse_args()

    try:
        result = get_table_ddl(args.instance_id, args.database, args.schema, args.table)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
