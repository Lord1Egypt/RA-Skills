#!/usr/bin/env python3
# /// script
# dependencies = [
#   "requests>=2.28",
#   "pyyaml>=6.0",
#   "rich>=13.0",
# ]
# ///
"""
Log Reading Script
Reads various log files on the server (Nginx/Apache/Redis/MySQL/PostgreSQL error logs, etc.)

Notes:
- Only installed services can have logs retrieved
- MySQL uses a special interface to get logs, not file paths
- PostgreSQL requires pgsql_manager plugin
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# Import compatible with dev and release environments
_skill_root = Path(__file__).parent.parent

if (_skill_root / "bt_common").exists():
    sys.path.insert(0, str(_skill_root))
else:
    sys.path.insert(0, str(_skill_root.parent / "src"))

from bt_common import (
    BtClient,
    BtClientManager,
    SERVICE_LOG_PATHS,
    SPECIAL_SERVICE_APIS,
    load_config,
)


# Supported service logs (file path + special interfaces)
SUPPORTED_LOG_SERVICES = list(SERVICE_LOG_PATHS.keys()) + list(SPECIAL_SERVICE_APIS.keys())


def check_service_installed(client: BtClient, service: str) -> tuple[bool, str]:
    """
    Check if service is installed

    Args:
        client: aaPanel client
        service: Service name

    Returns:
        (is_installed, status_info)
    """
    try:
        status = client.get_service_status(service)
        installed = status.get("installed", False)
        running = status.get("status", False)

        if not installed:
            return False, "Service not installed"
        elif not running:
            return True, "Service installed but not running"
        else:
            return True, "Service running"
    except Exception as e:
        return False, f"Failed to check status: {str(e)}"


def get_service_log(client: BtClient, service: str, log_type: str = "error",
                    lines: int = 100, check_installed: bool = True) -> dict:
    """
    Get service log

    Args:
        client: aaPanel client
        service: Service name
        log_type: Log type (error/slow)
        lines: Return last N lines
        check_installed: Whether to check service installation status

    Returns:
        Log content
    """
    result = {
        "server": client.name,
        "service": service,
        "log_type": log_type,
        "timestamp": datetime.now().isoformat(),
        "path": None,
        "content": "",
        "size": 0,
        "installed": True,
        "running": True,
        "error": None,
    }

    try:
        # Check if service is supported
        if service not in SUPPORTED_LOG_SERVICES:
            result["error"] = f"Unsupported service: {service}. Supported: {', '.join(SUPPORTED_LOG_SERVICES)}"
            result["installed"] = False
            return result

        # Check service installation status
        if check_installed:
            installed, status_msg = check_service_installed(client, service)
            result["installed"] = installed

            if not installed:
                result["error"] = f"Cannot get log: {status_msg}"
                return result

        # Special service handling (pgsql, mysql)
        if service in SPECIAL_SERVICE_APIS:
            api_key = "log" if log_type == "error" else "slow_log"
            endpoint = SPECIAL_SERVICE_APIS[service].get(api_key)
            if not endpoint:
                result["error"] = f"Unsupported log type: {log_type}"
                return result

            response = client.request(endpoint)
            if response.get("status"):
                # Log may be list format or string
                log_data = response.get("data", [])
                if isinstance(log_data, list):
                    result["content"] = "\n".join(str(line) for line in log_data)
                elif isinstance(log_data, str):
                    # MySQL log may be directly a string
                    result["content"] = log_data
                else:
                    result["content"] = str(log_data)
            else:
                result["error"] = response.get("msg", "Failed to get log")
            return result

        # Standard service log paths (nginx, apache, redis)
        if service not in SERVICE_LOG_PATHS:
            result["error"] = f"Unsupported service: {service}"
            return result

        log_path = SERVICE_LOG_PATHS[service]
        result["path"] = log_path

        # Read file content
        response = client.get_file_body(log_path)
        if response.get("status"):
            content = response.get("data", "")
            result["size"] = response.get("size", 0)

            # Only return last N lines
            if content:
                content_lines = content.split("\n")
                if len(content_lines) > lines:
                    content_lines = content_lines[-lines:]
                result["content"] = "\n".join(content_lines)
        else:
            result["error"] = response.get("msg", "Failed to read log file")

    except Exception as e:
        result["error"] = str(e)

    return result


def run_log_check(manager: BtClientManager, server: Optional[str] = None,
                  log_type: str = "error", service: Optional[str] = None,
                  lines: int = 100) -> dict:
    """
    Execute log check

    Args:
        manager: Client manager
        server: Specify server name
        log_type: Log type
        service: Service name
        lines: Number of lines to return

    Returns:
        Check results
    """
    # Single server
    if server:
        client = manager.get_client(server)
        return get_service_log(client, service, log_type, lines)

    # All servers
    all_clients = manager.get_all_clients()
    results = {
        "timestamp": datetime.now().isoformat(),
        "servers": [],
    }

    for name, client in all_clients.items():
        try:
            log_result = get_service_log(client, service, log_type, lines)
            results["servers"].append(log_result)
        except Exception as e:
            results["servers"].append({
                "server": name,
                "error": str(e),
            })

    return results


def print_log_output(results: dict, format_type: str = "table"):
    """Print log output"""
    try:
        from rich.console import Console
        from rich.panel import Panel
        from rich.syntax import Syntax

        console = Console()

        if "servers" in results:
            # Multi-server mode
            for server_data in results["servers"]:
                if "error" in server_data and "content" not in server_data:
                    server_name = server_data.get("server", "Unknown")
                    installed = server_data.get("installed", True)
                    if not installed:
                        console.print(f"[yellow]Server {server_name}: {server_data['error']}[/yellow]")
                    else:
                        console.print(f"[red]Server {server_name} error: {server_data['error']}[/red]")
                    continue

                server_name = server_data.get("server", "Unknown")
                service = server_data.get("service", "unknown")
                content = server_data.get("content", "")

                console.print(f"\n[bold cyan]═══ {server_name} - {service} ═══[/bold cyan]")

                if isinstance(content, str):
                    # Log content
                    if content.strip():
                        # Try syntax highlighting
                        try:
                            syntax = Syntax(content, "log", theme="monokai", line_numbers=True)
                            console.print(syntax)
                        except Exception:
                            console.print(content)
                    else:
                        console.print("[yellow]Log is empty[/yellow]")
                else:
                    console.print(str(content))

                if server_data.get("size"):
                    console.print(f"\n[dim]File size: {server_data['size']} bytes[/dim]")

        else:
            # Single server mode
            server_name = results.get("server", "Unknown")
            service = results.get("service", "unknown")
            content = results.get("content", "")
            error = results.get("error")
            installed = results.get("installed", True)

            if error:
                if not installed:
                    console.print(f"[yellow]Skipped: {error}[/yellow]")
                else:
                    console.print(f"[red]Error: {error}[/red]")
                return

            console.print(Panel(f"[bold]{server_name} - {service}[/bold]", title="Log"))

            if isinstance(content, str):
                if content.strip():
                    try:
                        syntax = Syntax(content, "log", theme="monokai", line_numbers=True)
                        console.print(syntax)
                    except Exception:
                        console.print(content)
                else:
                    console.print("[yellow]Log is empty[/yellow]")
            else:
                console.print(str(content))

            if results.get("size"):
                console.print(f"\n[dim]File size: {results['size']} bytes[/dim]")

    except ImportError:
        # Without rich library, use simple output
        if "servers" in results:
            for server_data in results["servers"]:
                print(f"\n=== {server_data.get('server', 'Unknown')} ===")
                content = server_data.get("content", "")
                print(content)
        else:
            content = results.get("content", "")
            print(content)


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="aaPanel Service Log Reading",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # View Nginx error log
  %(prog)s --service nginx

  # View Redis log
  %(prog)s --service redis

  # View Apache error log
  %(prog)s --service apache

  # View MySQL error log
  %(prog)s --service mysql

  # View MySQL slow query log
  %(prog)s --service mysql --log-type slow

  # View PostgreSQL log (requires plugin)
  %(prog)s --service pgsql

  # View PostgreSQL slow log
  %(prog)s --service pgsql --log-type slow

  # Specify server and line count
  %(prog)s --server prod-01 --service nginx --lines 200

  # JSON format output
  %(prog)s --service nginx --format json

Supported services: nginx, apache, redis, mysql, pgsql

Notes:
  - Only installed services can have logs retrieved
  - MySQL uses API interface to get logs, not file paths
  - PostgreSQL requires pgsql_manager plugin
        """,
    )
    parser.add_argument("--server", "-s", help="Specify server name")
    parser.add_argument("--service", required=True,
                        help="Service name (nginx/apache/redis/mysql/pgsql)")
    parser.add_argument("--log-type", choices=["error", "slow"], default="error",
                        help="Log type: error (error log), slow (slow log, supported by mysql/pgsql)")
    parser.add_argument("--lines", "-n", type=int, default=100,
                        help="Return last N lines of log (default: 100)")
    parser.add_argument("--format", "-f", choices=["json", "table"], default="table",
                        help="Output format")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--config", "-c", help="Config file path")
    parser.add_argument("--no-check", action="store_true",
                        help="Skip service installation status check")

    args = parser.parse_args()

    # Initialize client manager
    manager = BtClientManager()

    try:
        manager.load_config(args.config)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        print("Please configure server first: bt-config.py add", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Failed to load config: {e}", file=sys.stderr)
        sys.exit(1)

    if not manager.get_all_clients():
        print("Error: No servers configured", file=sys.stderr)
        sys.exit(1)

    # Execute log reading
    try:
        results = run_log_check(
            manager,
            server=args.server,
            log_type=args.log_type,
            service=args.service,
            lines=args.lines,
        )
    except KeyError as e:
        print(f"Error: Server not found {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Failed to read log: {e}", file=sys.stderr)
        sys.exit(1)

    # Output result
    if args.format == "json":
        output = json.dumps(results, ensure_ascii=False, indent=2)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(output)
            print(f"Result saved to: {args.output}")
        else:
            print(output)
    else:
        print_log_output(results, args.format)


if __name__ == "__main__":
    main()
