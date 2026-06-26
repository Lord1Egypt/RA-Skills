#!/usr/bin/env python3
# /// script
# dependencies = [
#   "requests>=2.28",
#   "rich>=13.0",
# ]
# ///
"""
Firewall Management Script
List firewall rules and manage IP whitelist/blacklist
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


def list_firewall_rules(client: BtClient) -> list:
    """
    List all firewall rules.

    Args:
        client: BtClient instance

    Returns:
        List of firewall rules
    """
    # Use datalist with table=firewall
    params = {
        "type": "-1",
        "search": "",
        "p": 1,
        "limit": 100,
        "table": "firewall",
        "order": ""
    }
    try:
        result = client.request("/datalist/data/get_data_list", params)
        if isinstance(result, dict):
            return result.get("data", [])
        return []
    except Exception:
        return []


def get_firewall_status(client: BtClient) -> dict:
    """
    Get firewall status.

    Args:
        client: BtClient instance

    Returns:
        Firewall status info
    """
    try:
        result = client.request("/safe?action=GetFirewallStatus", {})
        return result
    except Exception as e:
        return {"status": False, "msg": str(e)}


def add_ip_whitelist(client: BtClient, ip_address: str) -> dict:
    """
    Add IP to whitelist (allow).

    Args:
        client: BtClient instance
        ip_address: IP address to whitelist

    Returns:
        Result of operation
    """
    params = {"address": ip_address}
    try:
        result = client.request("/firewall?action=AddAcceptAddress", params)
        return result
    except Exception as e:
        return {"status": False, "msg": str(e)}


def remove_ip_whitelist(client: BtClient, ip_address: str) -> dict:
    """
    Remove IP from whitelist.

    Args:
        client: BtClient instance
        ip_address: IP address to remove

    Returns:
        Result of operation
    """
    params = {"address": ip_address}
    try:
        result = client.request("/firewall?action=DelAddress", params)
        return result
    except Exception as e:
        return {"status": False, "msg": str(e)}


def add_ip_blacklist(client: BtClient, ip_address: str) -> dict:
    """
    Add IP to blacklist (drop).

    Args:
        client: BtClient instance
        ip_address: IP address to blacklist

    Returns:
        Result of operation
    """
    params = {"address": ip_address}
    try:
        result = client.request("/firewall?action=AddDropAddress", params)
        return result
    except Exception as e:
        return {"status": False, "msg": str(e)}


def remove_ip_blacklist(client: BtClient, ip_address: str) -> dict:
    """
    Remove IP from blacklist.

    Args:
        client: BtClient instance
        ip_address: IP address to remove

    Returns:
        Result of operation
    """
    params = {"address": ip_address}
    try:
        result = client.request("/firewall?action=DelDropAddress", params)
        return result
    except Exception as e:
        return {"status": False, "msg": str(e)}


def print_firewall_table(rules: list):
    """Print firewall rules in table format."""
    try:
        from rich.console import Console
        from rich.table import Table

        console = Console()
        table = Table(show_header=True, header_style="bold")
        table.add_column("Address", style="cyan")
        table.add_column("Port", style="magenta")
        table.add_column("Type", style="yellow")
        table.add_column("Action", style="green")
        table.add_column("Comment", style="blue")

        for rule in rules:
            rule_type = rule.get("type", "accept")
            action_color = "green" if rule_type == "accept" else "red"
            table.add_row(
                rule.get("address", "-"),
                rule.get("port", "-"),
                rule_type,
                f"[{action_color}]{rule_type}[/{action_color}]",
                rule.get("ps", ""),
            )
        console.print(table)
    except ImportError:
        for rule in rules:
            print(f"{rule.get('address')}:{rule.get('port', '*')} ({rule.get('type', 'accept')})")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Firewall Management for aaPanel",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s list --server herobox
  %(prog)s status --server herobox
  %(prog)s allow --server herobox --ip 192.168.1.100
  %(prog)s deny --server herobox --ip 10.0.0.50
  %(prog)s remove --server herobox --ip 10.0.0.50 --type deny
        """,
    )
    subparsers = parser.add_subparsers(dest="action", help="Action to perform")

    # list
    subparsers.add_parser("list", help="List firewall rules")

    # status
    subparsers.add_parser("status", help="Get firewall status")

    # allow (whitelist)
    allow_parser = subparsers.add_parser("allow", help="Add IP to whitelist")
    allow_parser.add_argument("--ip", required=True, help="IP address")

    # deny (blacklist)
    deny_parser = subparsers.add_parser("deny", help="Add IP to blacklist")
    deny_parser.add_argument("--ip", required=True, help="IP address")

    # remove
    remove_parser = subparsers.add_parser("remove", help="Remove IP from list")
    remove_parser.add_argument("--ip", required=True, help="IP address")
    remove_parser.add_argument("--type", choices=["allow", "deny"], default="allow",
                              help="List type (default: allow)")

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
        result = {"rules": list_firewall_rules(client), "count": 0}
        result["count"] = len(result.get("rules", []))
    elif args.action == "status":
        result = get_firewall_status(client)
    elif args.action == "allow":
        result = add_ip_whitelist(client, args.ip)
    elif args.action == "deny":
        result = add_ip_blacklist(client, args.ip)
    elif args.action == "remove":
        if args.type == "allow":
            result = remove_ip_whitelist(client, args.ip)
        else:
            result = remove_ip_blacklist(client, args.ip)

    # Output result
    if args.format == "table":
        if args.action == "list":
            rules = result.get("rules", [])
            if rules:
                print_firewall_table(rules)
            else:
                print("No firewall rules found")
        elif args.action == "status":
            print(f"Firewall status: {result}")
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