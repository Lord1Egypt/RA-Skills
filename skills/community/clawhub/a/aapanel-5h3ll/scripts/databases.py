#!/usr/bin/env python3
# /// script
# dependencies = [
#   "requests>=2.28",
#   "rich>=13.0",
# ]
# ///
"""
Database Management Script
Create, delete databases and manage users
"""

import argparse
import json
import sys
from pathlib import Path

# Import compatible with dev and release environments
_skill_root = Path(__file__).parent.parent

if (_skill_root / "bt_common").exists():
    sys.path.insert(0, str(_skill_root))
else:
    sys.path.insert(0, str(_skill_root.parent / "src"))

from bt_common import BtClientManager, BtClient


def list_databases(client: BtClient) -> list:
    """
    List all databases.

    Args:
        client: BtClient instance

    Returns:
        List of database info
    """
    params = {
        "type": "-1",
        "search": "",
        "p": 1,
        "limit": 100,
        "table": "databases",
        "order": ""
    }
    try:
        result = client.request("/datalist/data/get_data_list", params)
        if isinstance(result, dict):
            return result.get("data", [])
        return []
    except Exception:
        return []


def create_database(client: BtClient, name: str, db_user: str, password: str,
                   coding: str = "utf8mb4") -> dict:
    """
    Create a new database.

    Args:
        client: BtClient instance
        name: Database name
        db_user: Database user name
        password: Database user password
        coding: Character encoding (default: utf8mb4)

    Returns:
        Result of creation operation
    """
    params = {
        "name": name,
        "db_user": db_user,
        "password": password,
        "type": "MySQL",
        "coding": coding
    }
    try:
        result = client.request("/database?action=CreateDatabase", params)
        return result
    except Exception as e:
        return {"status": False, "msg": str(e)}


def delete_database(client: BtClient, name: str) -> dict:
    """
    Delete a database.

    Args:
        client: BtClient instance
        name: Database name

    Returns:
        Result of deletion operation
    """
    params = {"name": name}
    try:
        result = client.request("/database?action=DeleteDatabase", params)
        return result
    except Exception as e:
        return {"status": False, "msg": str(e)}


def create_user(client: BtClient, db_user: str, password: str, rights: str = "ALL") -> dict:
    """
    Create a database user.

    Args:
        client: BtClient instance
        db_user: User name
        password: Password
        rights: Privileges (default: ALL)

    Returns:
        Result of creation operation
    """
    params = {
        "db_user": db_user,
        "password": password,
        "rights": rights
    }
    try:
        result = client.request("/database?action=CreateUser", params)
        return result
    except Exception as e:
        return {"status": False, "msg": str(e)}


def grant_privileges(client: BtClient, db_user: str, db_name: str, rights: str = "ALL") -> dict:
    """
    Grant privileges to a user on a database.

    Args:
        client: BtClient instance
        db_user: Database user
        db_name: Database name
        rights: Privileges to grant (default: ALL)

    Returns:
        Result of grant operation
    """
    params = {
        "db_user": db_user,
        "db_name": db_name,
        "rights": rights
    }
    try:
        result = client.request("/database?action=GrantPriv", params)
        return result
    except Exception as e:
        return {"status": False, "msg": str(e)}


def revoke_privileges(client: BtClient, db_user: str, db_name: str) -> dict:
    """
    Revoke privileges from a user.

    Args:
        client: BtClient instance
        db_user: Database user
        db_name: Database name

    Returns:
        Result of revoke operation
    """
    params = {"db_user": db_user, "db_name": db_name}
    try:
        result = client.request("/database?action=RevokePriv", params)
        return result
    except Exception as e:
        return {"status": False, "msg": str(e)}


def print_databases_table(databases: list):
    """Print databases in table format."""
    try:
        from rich.console import Console
        from rich.table import Table

        console = Console()
        table = Table(show_header=True, header_style="bold")
        table.add_column("Name", style="cyan")
        table.add_column("User", style="magenta")
        table.add_column("Encoding", style="blue")
        table.add_column("Created", style="yellow")

        for db in databases:
            table.add_row(
                db.get("name", "-"),
                db.get("db_user", "-"),
                db.get("coding", "utf8mb4"),
                db.get("addtime", "-"),
            )
        console.print(table)
    except ImportError:
        for db in databases:
            print(f"{db.get('name')}: user={db.get('db_user')}, encoding={db.get('coding', 'utf8mb4')}")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Database Management for aaPanel",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s list --server herobox
  %(prog)s create --server herobox --name mydb --user myuser --password Secret123
  %(prog)s delete --server herobox --name mydb
  %(prog)s create-user --server herobox --user newuser --password Secret123
  %(prog)s grant --server herobox --user newuser --db mydb
        """,
    )
    subparsers = parser.add_subparsers(dest="action", help="Action to perform")

    # list
    subparsers.add_parser("list", help="List all databases")

    # create
    create_parser = subparsers.add_parser("create", help="Create a new database")
    create_parser.add_argument("--name", required=True, help="Database name")
    create_parser.add_argument("--user", required=True, help="Database user")
    create_parser.add_argument("--password", required=True, help="Database user password")
    create_parser.add_argument("--coding", default="utf8mb4", help="Character encoding")

    # delete
    delete_parser = subparsers.add_parser("delete", help="Delete a database")
    delete_parser.add_argument("--name", required=True, help="Database name")

    # create-user
    create_user_parser = subparsers.add_parser("create-user", help="Create database user")
    create_user_parser.add_argument("--user", required=True, help="Username")
    create_user_parser.add_argument("--password", required=True, help="Password")
    create_user_parser.add_argument("--rights", default="ALL", help="Privileges")

    # grant
    grant_parser = subparsers.add_parser("grant", help="Grant privileges")
    grant_parser.add_argument("--user", required=True, help="Database user")
    grant_parser.add_argument("--db", required=True, help="Database name")
    grant_parser.add_argument("--rights", default="ALL", help="Privileges")

    # revoke
    revoke_parser = subparsers.add_parser("revoke", help="Revoke privileges")
    revoke_parser.add_argument("--user", required=True, help="Database user")
    revoke_parser.add_argument("--db", required=True, help="Database name")

    parser.add_argument("--server", "-s", required=True, help="Server name")
    parser.add_argument("--format", "-f", choices=["json", "table"], default="table", help="Output format")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--config", "-c", help="Config file path")

    args = parser.parse_args()

    if not args.action:
        parser.print_help()
        sys.exit(1)

    # Initialize manager
    manager = BtClientManager()
    try:
        manager.load_config(args.config)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        client = manager.get_client(args.server)
    except KeyError:
        print(f"Error: Server not found: {args.server}", file=sys.stderr)
        sys.exit(1)

    # Execute action
    result = None
    if args.action == "list":
        result = {"databases": list_databases(client), "count": 0}
        result["count"] = len(result.get("databases", []))
    elif args.action == "create":
        result = create_database(client, args.name, args.user, args.password, args.coding)
    elif args.action == "delete":
        result = delete_database(client, args.name)
    elif args.action == "create-user":
        result = create_user(client, args.user, args.password, args.rights)
    elif args.action == "grant":
        result = grant_privileges(client, args.user, args.db, args.rights)
    elif args.action == "revoke":
        result = revoke_privileges(client, args.user, args.db)

    # Output result
    if args.format == "table":
        if args.action == "list":
            databases = result.get("databases", [])
            if databases:
                print_databases_table(databases)
            else:
                print("No databases found")
        else:
            if result.get("status"):
                print(f"Success: {result.get('msg', 'Operation completed')}")
            else:
                print(f"Error: {result.get('msg', 'Unknown error')}", file=sys.stderr)
    else:
        output = json.dumps(result, ensure_ascii=False, indent=2)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(output)
            print(f"Result saved to: {args.output}")
        else:
            print(output)


if __name__ == "__main__":
    main()