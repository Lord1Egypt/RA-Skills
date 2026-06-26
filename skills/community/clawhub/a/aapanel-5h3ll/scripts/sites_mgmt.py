#!/usr/bin/env python3
# /// script
# dependencies = [
#   "requests>=2.28",
#   "rich>=13.0",
# ]
# ///
"""
Site Management Script
Create, delete sites and manage domains
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


def list_sites(client: BtClient) -> list:
    """
    List all sites.

    Args:
        client: BtClient instance

    Returns:
        List of sites with basic info
    """
    sites_data = client.get_site_list()
    sites = []
    for site in sites_data:
        sites.append({
            "id": site.get("id"),
            "name": site.get("name", ""),
            "path": site.get("path", ""),
            "status": "running" if site.get("status") == "1" else "stopped",
            "php_version": site.get("php_version", ""),
            "type": site.get("project_type", "PHP"),
            "domains": site.get("domain", 0),
            "ssl_enabled": site.get("ssl") not in [None, -1],
            "addtime": site.get("addtime", ""),
            "ps": site.get("ps", ""),
        })
    return sites


def create_site(client: BtClient, name: str, path: str, php_version: str = "74") -> dict:
    """
    Create a new site.

    Args:
        client: BtClient instance
        name: Site name (domain)
        path: Document root path
        php_version: PHP version (e.g., "74", "83")

    Returns:
        Result of creation operation
    """
    # webname must be JSON format
    webname = json.dumps({
        "siteinfo": {
            "name": name,
            "domain": name,
            "path": path,
            "type": 0,  # PHP site
            "php_version": php_version
        }
    })
    params = {"webname": webname}

    try:
        result = client.request("/site?action=AddSite", params)
        return result
    except Exception as e:
        return {"status": False, "msg": str(e)}


def delete_site(client: BtClient, site_name: str) -> dict:
    """
    Delete a site.

    Args:
        client: BtClient instance
        site_name: Site name to delete

    Returns:
        Result of deletion operation
    """
    # Find site ID first
    sites_data = client.get_site_list()
    site_id = None
    for site in sites_data:
        if site.get("name") == site_name:
            site_id = site.get("id")
            break

    if not site_id:
        return {"status": False, "msg": f"Site not found: {site_name}"}

    params = {"id": site_id}
    try:
        result = client.request("/site?action=DeleteSite", params)
        return result
    except Exception as e:
        return {"status": False, "msg": str(e)}


def add_domain(client: BtClient, site_name: str, domain: str, port: int = 80) -> dict:
    """
    Add domain to a site.

    Args:
        client: BtClient instance
        site_name: Site name
        domain: Domain to add
        port: Port (default 80)

    Returns:
        Result of add operation
    """
    params = {
        "siteName": site_name,
        "domain": domain,
        "id": 1,  # required parameter
        "port": port
    }
    try:
        result = client.request("/site?action=AddDomain", params)
        return result
    except Exception as e:
        return {"status": False, "msg": str(e)}


def remove_domain(client: BtClient, site_name: str, domain: str, port: int = 80) -> dict:
    """
    Remove domain from a site.

    Args:
        client: BtClient instance
        site_name: Site name
        domain: Domain to remove
        port: Port (default 80)

    Returns:
        Result of remove operation
    """
    params = {
        "siteName": site_name,
        "domain": domain,
        "port": port
    }
    try:
        result = client.request("/site?action=DeleteDomain", params)
        return result
    except Exception as e:
        return {"status": False, "msg": str(e)}


def get_domains(client: BtClient, site_name: str) -> list:
    """
    Get domains for a site.

    Args:
        client: BtClient instance
        site_name: Site name

    Returns:
        List of domain info
    """
    # Find site ID first
    sites_data = client.get_site_list()
    site_id = None
    for site in sites_data:
        if site.get("name") == site_name:
            site_id = site.get("id")
            break

    if not site_id:
        return []

    # Get domains from datalist
    params = {
        "type": "-1",
        "search": "",
        "p": 1,
        "limit": 100,
        "table": "domain",
        "order": "",
        "where": f"pid={site_id}"
    }
    try:
        result = client.request("/datalist/data/get_data_list", params)
        if isinstance(result, dict):
            return result.get("data", [])
        return []
    except Exception:
        return []


def print_sites_table(sites: list):
    """Print sites in table format."""
    try:
        from rich.console import Console
        from rich.table import Table

        console = Console()
        table = Table(show_header=True, header_style="bold")
        table.add_column("Name", style="cyan")
        table.add_column("Path", style="magenta")
        table.add_column("Status", width=10)
        table.add_column("PHP", width=8)
        table.add_column("Domains", justify="right")
        table.add_column("SSL", width=6)

        for site in sites:
            status_color = "green" if site["status"] == "running" else "red"
            ssl_color = "green" if site["ssl_enabled"] else "red"

            table.add_row(
                site.get("name", "-")[:40],
                site.get("path", "-")[:30],
                f"[{status_color}]{site['status']}[/{status_color}]",
                site.get("php_version", "-"),
                str(site.get("domains", 0)),
                f"[{ssl_color}]{'Yes' if site['ssl_enabled'] else 'No'}[/{ssl_color}]",
            )
        console.print(table)
    except ImportError:
        for site in sites:
            print(f"{site['name']}: {site['path']} ({site['status']})")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Site Management for aaPanel",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s list --server herobox
  %(prog)s create --server herobox --name test.site --path /www/wwwroot/test.site
  %(prog)s delete --server herobox --name test.site
  %(prog)s add-domain --server herobox --site test.site --domain www.test.site
  %(prog)s remove-domain --server herobox --site test.site --domain www.test.site
  %(prog)s domains --server herobox --site test.site
        """,
    )
    subparsers = parser.add_subparsers(dest="action", help="Action to perform")

    # list
    subparsers.add_parser("list", help="List all sites")

    # create
    create_parser = subparsers.add_parser("create", help="Create a new site")
    create_parser.add_argument("--name", required=True, help="Site name (domain)")
    create_parser.add_argument("--path", required=True, help="Document root path")
    create_parser.add_argument("--php", default="74", help="PHP version (default: 74)")

    # delete
    delete_parser = subparsers.add_parser("delete", help="Delete a site")
    delete_parser.add_argument("--name", required=True, help="Site name to delete")

    # add-domain
    add_domain_parser = subparsers.add_parser("add-domain", help="Add domain to site")
    add_domain_parser.add_argument("--site", required=True, help="Site name")
    add_domain_parser.add_argument("--domain", required=True, help="Domain to add")
    add_domain_parser.add_argument("--port", type=int, default=80, help="Port (default: 80)")

    # remove-domain
    remove_domain_parser = subparsers.add_parser("remove-domain", help="Remove domain from site")
    remove_domain_parser.add_argument("--site", required=True, help="Site name")
    remove_domain_parser.add_argument("--domain", required=True, help="Domain to remove")
    remove_domain_parser.add_argument("--port", type=int, default=80, help="Port (default: 80)")

    # domains
    domains_parser = subparsers.add_parser("domains", help="Get domains for a site")
    domains_parser.add_argument("--site", required=True, help="Site name")

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
        result = {"sites": list_sites(client), "count": 0}
        result["count"] = len(result["sites"])
    elif args.action == "create":
        result = create_site(client, args.name, args.path, args.php)
    elif args.action == "delete":
        result = delete_site(client, args.name)
    elif args.action == "add-domain":
        result = add_domain(client, args.site, args.domain, args.port)
    elif args.action == "remove-domain":
        result = remove_domain(client, args.site, args.domain, args.port)
    elif args.action == "domains":
        result = {"domains": get_domains(client, args.site)}

    # Output result
    if args.format == "table":
        if args.action == "list":
            sites = result.get("sites", [])
            if sites:
                print_sites_table(sites)
            else:
                print("No sites found")
        elif args.action == "domains":
            domains = result.get("domains", [])
            if domains:
                print(f"Domains for {args.site}:")
                for d in domains:
                    print(f"  - {d.get('name')}:{d.get('port', 80)}")
            else:
                print("No domains found")
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