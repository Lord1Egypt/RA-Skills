#!/usr/bin/env python3
# /// script
# dependencies = [
#   "requests>=2.28",
#   "rich>=13.0",
# ]
# ///
"""
SSL Certificate Management Script
Manage SSL certificates for aaPanel sites
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

# Import compatible with dev and release environments
_skill_root = Path(__file__).parent.parent

if (_skill_root / "bt_common").exists():
    sys.path.insert(0, str(_skill_root))
else:
    sys.path.insert(0, str(_skill_root.parent / "src"))

from bt_common import BtClient, BtClientManager, load_config


def list_ssl_certs(client: BtClient) -> list:
    """
    List all SSL certificates from site data.

    Args:
        client: BtClient instance

    Returns:
        List of SSL certificate info
    """
    sites_data = client.get_site_list()
    certs = []
    for site in sites_data:
        ssl_info = site.get("ssl", {})
        if ssl_info and ssl_info != -1:
            certs.append({
                "site_name": site.get("name", ""),
                "subject": ssl_info.get("subject", ""),
                "issuer": ssl_info.get("issuer_O", ""),
                "not_before": ssl_info.get("notBefore", ""),
                "not_after": ssl_info.get("notAfter", ""),
                "days_remaining": ssl_info.get("endtime", 0),
                "dns": ssl_info.get("dns", []),
            })
    return certs


def get_ssl_info(client: BtClient, site_name: str) -> dict:
    """
    Get detailed SSL info for a specific site.

    Args:
        client: BtClient instance
        site_name: Site name

    Returns:
        SSL certificate details
    """
    sites_data = client.get_site_list()
    for site in sites_data:
        if site.get("name") == site_name:
            ssl_info = site.get("ssl", {})
            if ssl_info and ssl_info != -1:
                return {
                    "site_name": site_name,
                    "subject": ssl_info.get("subject", ""),
                    "issuer": ssl_info.get("issuer", ""),
                    "issuer_O": ssl_info.get("issuer_O", ""),
                    "not_before": ssl_info.get("notBefore", ""),
                    "not_after": ssl_info.get("notAfter", ""),
                    "endtime": ssl_info.get("endtime", 0),
                    "dns": ssl_info.get("dns", []),
                }
            return {"site_name": site_name, "ssl": None, "status": "no_ssl"}
    return {"site_name": site_name, "error": "site not found"}


def provision_letsencrypt(client: BtClient, site_name: str) -> dict:
    """
    Provision Let's Encrypt certificate for a site.
    Note: Requires DNS verification setup.

    Args:
        client: BtClient instance
        site_name: Site name

    Returns:
        Result of provision operation
    """
    # Get site ID first
    sites_data = client.get_site_list()
    site_id = None
    for site in sites_data:
        if site.get("name") == site_name:
            site_id = site.get("id")
            break

    if not site_id:
        return {"status": False, "msg": f"Site not found: {site_name}"}

    # Use acme API for Let's Encrypt
    # Endpoint: /acme?action=ApplyCert
    params = {
        "siteName": site_name,
        "type": "dns",
        "dnspars": "",
    }
    try:
        result = client.request("/acme?action=ApplyCert", params)
        return result
    except Exception as e:
        return {"status": False, "msg": str(e)}


def renew_ssl(client: BtClient, site_name: str) -> dict:
    """
    Renew SSL certificate for a site.

    Args:
        client: BtClient instance
        site_name: Site name

    Returns:
        Result of renewal operation
    """
    params = {"siteName": site_name}
    try:
        result = client.request("/site?action=RenewCert", params)
        return result
    except Exception as e:
        return {"status": False, "msg": str(e)}


def revoke_ssl(client: BtClient, site_name: str) -> dict:
    """
    Revoke SSL certificate for a site.
    This will disable SSL for the site.

    Args:
        client: BtClient instance
        site_name: Site name

    Returns:
        Result of revoke operation
    """
    params = {"siteName": site_name}
    try:
        result = client.request("/site?action=CloseSsl", params)
        return result
    except Exception as e:
        return {"status": False, "msg": str(e)}


def print_ssl_table(certs: list):
    """Print SSL certificates in table format."""
    try:
        from rich.console import Console
        from rich.table import Table

        console = Console()
        table = Table(show_header=True, header_style="bold")
        table.add_column("Site", style="cyan")
        table.add_column("Subject", style="magenta")
        table.add_column("Issuer", style="blue")
        table.add_column("Expires", style="yellow")
        table.add_column("Days", justify="right")

        for cert in certs:
            days = cert.get("days_remaining", 0)
            if days <= 7:
                days_str = f"[red]{days}[/red]"
            elif days <= 30:
                days_str = f"[yellow]{days}[/yellow]"
            else:
                days_str = f"[green]{days}[/green]"

            table.add_row(
                cert.get("site_name", "-"),
                cert.get("subject", "-"),
                cert.get("issuer", "-"),
                cert.get("not_after", "-"),
                days_str,
            )
        console.print(table)
    except ImportError:
        for cert in certs:
            print(f"{cert['site_name']}: {cert['subject']} (expires {cert['not_after']}, {cert['days_remaining']} days)")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="SSL Certificate Management for aaPanel",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s list --server herobox
  %(prog)s info --server herobox --site argus.5h3ll.site
  %(prog)s provision --server herobox --site argus.5h3ll.site
  %(prog)s renew --server herobox --site argus.5h3ll.site
  %(prog)s revoke --server herobox --site argus.5h3ll.site
        """,
    )
    parser.add_argument("action", choices=["list", "info", "provision", "renew", "revoke"],
                        help="Action to perform")
    parser.add_argument("--server", "-s", required=True, help="Server name")
    parser.add_argument("--site", help="Site name (for info/provision/renew/revoke actions)")
    parser.add_argument("--format", "-f", choices=["json", "table"], default="table", help="Output format")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--config", "-c", help="Config file path")

    args = parser.parse_args()

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
        result = {"certs": list_ssl_certs(client), "count": len(list_ssl_certs(client))}
    elif args.action == "info":
        if not args.site:
            print("Error: --site required for info action", file=sys.stderr)
            sys.exit(1)
        result = get_ssl_info(client, args.site)
    elif args.action == "provision":
        if not args.site:
            print("Error: --site required for provision action", file=sys.stderr)
            sys.exit(1)
        result = provision_letsencrypt(client, args.site)
    elif args.action == "renew":
        if not args.site:
            print("Error: --site required for renew action", file=sys.stderr)
            sys.exit(1)
        result = renew_ssl(client, args.site)
    elif args.action == "revoke":
        if not args.site:
            print("Error: --site required for revoke action", file=sys.stderr)
            sys.exit(1)
        result = revoke_ssl(client, args.site)

    # Output result
    if args.format == "table":
        if args.action == "list":
            certs = result.get("certs", [])
            if certs:
                print_ssl_table(certs)
            else:
                print("No SSL certificates found")
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