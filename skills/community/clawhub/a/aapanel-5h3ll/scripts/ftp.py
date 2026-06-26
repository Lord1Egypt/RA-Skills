#!/usr/bin/env python3
# /// script
# dependencies = [
#   "requests>=2.28",
#   "rich>=13.0",
# ]
# ///
"""
FTP Account Management Script
List, create, and delete FTP accounts
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


def list_ftp_accounts(client: BtClient) -> list:
    """
    List all FTP accounts.

    Args:
        client: BtClient instance

    Returns:
        List of FTP account info
    """
    params = {
        "type": "-1",
        "search": "",
        "p": 1,
        "limit": 100,
        "table": "ftps",
        "order": ""
    }
    try:
        result = client.request("/datalist/data/get_data_list", params)
        if isinstance(result, dict):
            return result.get("data", []) or []
        return []
    except Exception:
        return []


def create_ftp_user(client: BtClient, username: str, password: str, path: str,
                   active: bool = True) -> dict:
    """
    Create a new FTP account.

    Args:
        client: BtClient instance
        username: FTP username
        password: FTP password
        path: Home directory path
        active: Whether account is active

    Returns:
        Result of creation operation
    """
    params = {
        "ftp_username": username,
        "ftp_password": password,
        "path": path,
        "active": "true" if active else "false"
    }
    try:
        result = client.request("/ftp?action=CreateUser", params)
        return result
    except Exception as e:
        return {"status": False, "msg": str(e)}


def delete_ftp_user(client: BtClient, user_id: int) -> dict:
    """
    Delete an FTP account.

    Args:
        client: BtClient instance
        user_id: FTP account ID

    Returns:
        Result of deletion operation
    """
    params = {"id": user_id}
    try:
        result = client.request("/ftp?action=DeleteUser", params)
        return result
    except Exception as e:
        return {"status": False, "msg": str(e)}


def set_ftp_password(client: BtClient, user_id: int, password: str) -> dict:
    """
    Set FTP account password.

    Args:
        client: BtClient instance
        user_id: FTP account ID
        password: New password

    Returns:
        Result of operation
    """
    params = {"id": user_id, "password": password}
    try:
        result = client.request("/ftp?action=SetPassword", params)
        return result
    except Exception as e:
        return {"status": False, "msg": str(e)}


def print_ftp_table(accounts: list):
    """Print FTP accounts in table format."""
    try:
        from rich.console import Console
        from rich.table import Table

        console = Console()
        table = Table(show_header=True, header_style="bold")
        table.add_column("ID", justify="right")
        table.add_column("Username", style="cyan")
        table.add_column("Home Directory", style="magenta")
        table.add_column("Status", style="green")
        table.add_column("Created", style="yellow")

        for account in accounts:
            active = account.get("active", True)
            status_color = "green" if active else "red"
            table.add_row(
                str(account.get("id", "")),
                account.get("user", "-"),
                account.get("path", "-")[:40],
                f"[{status_color}]{'Active' if active else 'Inactive'}[/{status_color}]",
                account.get("addtime", "-"),
            )
        console.print(table)
    except ImportError:
        for account in accounts:
            print(f"{account.get('user')}: {account.get('path')} (active={account.get('active', True)})")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="FTP Account Management for aaPanel",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s list --server herobox
  %(prog)s create --server herobox --user ftpuser --password Secret123 --path /www/wwwroot
  %(prog)s delete --server herobox --id 1
  %(prog)s set-password --server herobox --id 1 --password NewSecret123
        """,
    )
    subparsers = parser.add_subparsers(dest="action", help="Action to perform")

    # list
    subparsers.add_parser("list", help="List all FTP accounts")

    # create
    create_parser = subparsers.add_parser("create", help="Create FTP account")
    create_parser.add_argument("--user", required=True, help="FTP username")
    create_parser.add_argument("--password", required=True, help="FTP password")
    create_parser.add_argument("--path", required=True, help="Home directory")

    # delete
    delete_parser = subparsers.add_parser("delete", help="Delete FTP account")
    delete_parser.add_argument("--id", type=int, required=True, help="FTP account ID")

    # set-password
    pass_parser = subparsers.add_parser("set-password", help="Set FTP password")
    pass_parser.add_argument("--id", type=int, required=True, help="FTP account ID")
    pass_parser.add_argument("--password", required=True, help="New password")

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
        result = {"accounts": list_ftp_accounts(client), "count": 0}
        result["count"] = len(result.get("accounts", []))
    elif args.action == "create":
        result = create_ftp_user(client, args.user, args.password, args.path)
    elif args.action == "delete":
        result = delete_ftp_user(client, args.id)
    elif args.action == "set-password":
        result = set_ftp_password(client, args.id, args.password)

    # Output result
    if args.format == "table":
        if args.action == "list":
            accounts = result.get("accounts", [])
            if accounts:
                print_ftp_table(accounts)
            else:
                print("No FTP accounts found")
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