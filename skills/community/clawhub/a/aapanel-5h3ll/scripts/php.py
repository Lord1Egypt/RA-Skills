#!/usr/bin/env python3
# /// script
# dependencies = [
#   "requests>=2.28",
#   "rich>=13.0",
# ]
# ///
"""
PHP Version Management Script
Set PHP version per site
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


def list_php_versions(client: BtClient) -> list:
    """
    List installed PHP versions.

    Args:
        client: BtClient instance

    Returns:
        List of PHP version info
    """
    try:
        result = client.get_php_versions()
        return result
    except Exception:
        return []


def set_php_version(client: BtClient, site_name: str, version: str) -> dict:
    """
    Set PHP version for a site.

    Args:
        client: BtClient instance
        site_name: Site name
        version: PHP version (e.g., "74", "83")

    Returns:
        Result of operation
    """
    params = {
        "siteName": site_name,
        "version": version
    }
    try:
        result = client.request("/site?action=SetPHPVersion", params)
        return result
    except Exception as e:
        return {"status": False, "msg": str(e)}


def get_site_php_version(client: BtClient, site_name: str) -> str:
    """
    Get current PHP version for a site.

    Args:
        client: BtClient instance
        site_name: Site name

    Returns:
        PHP version string
    """
    sites_data = client.get_site_list()
    for site in sites_data:
        if site.get("name") == site_name:
            php_version = site.get("php_version", "")
            # Convert display format to version number
            if php_version in ["static", "Static", "static"]:
                return "static"
            if php_version in ["other", "Other"]:
                return "other"
            # Extract version number from strings like "PHP-74" or "74"
            if php_version.startswith("PHP-"):
                return php_version.replace("PHP-", "")
            return php_version
    return "unknown"


def print_php_versions_table(versions: list):
    """Print PHP versions in table format."""
    try:
        from rich.console import Console
        from rich.table import Table

        console = Console()
        table = Table(show_header=True, header_style="bold")
        table.add_column("Name", style="cyan")
        table.add_column("Version", style="magenta")
        table.add_column("Status", style="green")
        table.add_column("Type", style="yellow")

        for v in versions:
            name = v.get("name", "")
            status_color = "green" if v.get("status") == "running" else "red"
            table.add_row(
                name,
                v.get("version", "-"),
                f"[{status_color}]{v.get('status', 'unknown')}[/{status_color}]",
                v.get("type", "php"),
            )
        console.print(table)
    except ImportError:
        for v in versions:
            print(f"{v.get('name')}: {v.get('version')} ({v.get('status', 'unknown')})")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="PHP Version Management for aaPanel",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s list --server herobox
  %(prog)s set --server herobox --site example.com --version 83
  %(prog)s get --server herobox --site example.com
        """,
    )
    subparsers = parser.add_subparsers(dest="action", help="Action to perform")

    # list
    subparsers.add_parser("list", help="List installed PHP versions")

    # set
    set_parser = subparsers.add_parser("set", help="Set PHP version for site")
    set_parser.add_argument("--site", required=True, help="Site name")
    set_parser.add_argument("--version", required=True, help="PHP version (e.g., 74, 83)")

    # get
    get_parser = subparsers.add_parser("get", help="Get current PHP version for site")
    get_parser.add_argument("--site", required=True, help="Site name")

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
        versions = list_php_versions(client)
        result = {"versions": versions, "count": len(versions)}
    elif args.action == "set":
        result = set_php_version(client, args.site, args.version)
    elif args.action == "get":
        version = get_site_php_version(client, args.site)
        result = {"site": args.site, "php_version": version}

    # Output result
    if args.format == "table":
        if args.action == "list":
            versions = result.get("versions", [])
            if versions:
                print_php_versions_table(versions)
            else:
                print("No PHP versions found")
        elif args.action == "get":
            print(f"PHP version for {args.site}: {result.get('php_version')}")
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