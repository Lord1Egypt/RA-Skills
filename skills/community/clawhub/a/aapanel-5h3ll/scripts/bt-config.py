#!/usr/bin/env python3
# /// script
# dependencies = [
#   "pyyaml>=6.0",
# ]
# ///
"""
aaPanel Config Management Tool
Supports viewing, adding, deleting, and modifying server configurations
"""

import argparse
import json
import sys
from pathlib import Path

# Import compatible with dev and release environments
# release environment: bt_common/ (scripts in scripts/)
# dev environment: src/bt_common/ (scripts in src/bt_common/scripts/)
_script_root = Path(__file__).parent.parent
if (_script_root / "bt_common").exists():
    # release environment: scripts in {baseDir}/scripts/, bt_common in {baseDir}/bt_common/
    sys.path.insert(0, str(_script_root))
else:
    # dev environment: scripts in src/bt_common/scripts/, bt_common in src/bt_common/
    sys.path.insert(0, str(_script_root))

from bt_common import (
    GLOBAL_CONFIG_FILE,
    MIN_PANEL_VERSION,
    add_server,
    create_default_global_config,
    find_config_file,
    get_config_info,
    load_config,
    normalize_host,
    remove_server,
    update_thresholds,
    validate_host,
)


def cmd_list(args):
    """List all server configs"""
    try:
        config_info = get_config_info()

        print("=" * 60)
        print("aaPanel Configuration Info")
        print("=" * 60)
        print(f"Config file: {config_info.get('current_config_path', 'Not set')}")
        print(f"Global config: {config_info.get('global_config_path', '')}")
        print(f"aaPanel version requirement: >= {config_info.get('min_panel_version', MIN_PANEL_VERSION)}")
        print()

        servers = config_info.get("servers", [])
        if not servers:
            print("No server configs yet")
            print()
            print("Use the following command to add a server:")
            print("  bt-config add --name <name> --host <address> --token <key>")
            return 0

        print(f"Server list ({len(servers)}):")
        print("-" * 60)
        for server in servers:
            status = "✓" if server.get("enabled", True) else "✗"
            verify_ssl = "✓" if server.get("verify_ssl", True) else "✗"
            print(f"  [{status}] {server['name']}")
            print(f"       Address: {server['host']}")
            print(f"       SSL verification: [{verify_ssl}]")
        print()

        thresholds = config_info.get("thresholds", {})
        if thresholds:
            print("Alert thresholds:")
            print(f"  CPU: {thresholds.get('cpu', 80)}%")
            print(f"  Memory: {thresholds.get('memory', 85)}%")
            print(f"  Disk: {thresholds.get('disk', 90)}%")

        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def cmd_add(args):
    """Add server config"""
    try:
        # Validate and normalize address
        is_valid, result = validate_host(args.host)
        if not is_valid:
            print(f"Error: {result}", file=sys.stderr)
            return 1

        normalized_host = result
        if normalized_host != args.host:
            print(f"Hint: Address normalized to {normalized_host}")

        # Check if already exists
        config_info = get_config_info()
        existing_names = [s["name"] for s in config_info.get("servers", [])]

        if args.name in existing_names and not args.force:
            print(f"Error: Server '{args.name}' already exists, use --force to overwrite")
            return 1

        # Determine SSL verification setting
        verify_ssl = args.verify_ssl if args.verify_ssl is not None else True

        result = add_server(
            name=args.name,
            host=normalized_host,
            token=args.token,
            timeout=args.timeout,
            enabled=not args.disabled,
            verify_ssl=verify_ssl,
        )

        if result:
            print(f"✓ Server added: {args.name}")
            print(f"  Address: {normalized_host}")
            print(f"  Timeout: {args.timeout}ms")
            print(f"  Status: {'Disabled' if args.disabled else 'Enabled'}")
            print(f"  SSL verification: {'Enabled' if verify_ssl else 'Disabled'}")
            print()
            print(f"Config file: {GLOBAL_CONFIG_FILE}")
            return 0
        else:
            print("Failed to add")
            return 1

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def cmd_remove(args):
    """Remove server config"""
    try:
        result = remove_server(args.name)

        if result:
            print(f"✓ Server removed: {args.name}")
            print(f"Config file: {GLOBAL_CONFIG_FILE}")
            return 0
        else:
            print(f"Server not found: {args.name}")
            return 1

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def cmd_update(args):
    """Update server config"""
    try:
        # First delete then add
        config_info = get_config_info()
        existing = None
        for s in config_info.get("servers", []):
            if s["name"] == args.name:
                existing = s
                break

        if not existing:
            print(f"Server not found: {args.name}")
            return 1

        # Merge parameters
        new_host = args.host if args.host else existing["host"]
        new_token = args.token if args.token else existing.get("token", "")
        new_timeout = args.timeout if args.timeout else existing.get("timeout", 10000)
        new_enabled = not args.disabled if args.disabled is not None else existing.get("enabled", True)
        new_verify_ssl = args.verify_ssl if args.verify_ssl is not None else existing.get("verify_ssl", True)

        # Remove old, add new
        remove_server(args.name)
        add_server(
            name=args.name,
            host=new_host,
            token=new_token,
            timeout=new_timeout,
            enabled=new_enabled,
            verify_ssl=new_verify_ssl,
        )

        print(f"✓ Server updated: {args.name}")
        print(f"  Address: {new_host}")
        print(f"  Timeout: {new_timeout}ms")
        print(f"  Status: {'Disabled' if not new_enabled else 'Enabled'}")
        print(f"  SSL verification: {'Enabled' if new_verify_ssl else 'Disabled'}")
        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def cmd_threshold(args):
    """Set alert threshold values"""
    try:
        result = update_thresholds(
            cpu=args.cpu,
            memory=args.memory,
            disk=args.disk,
        )

        if result:
            print("✓ Alert thresholds updated:")
            if args.cpu:
                print(f"  CPU: {args.cpu}%")
            if args.memory:
                print(f"  Memory: {args.memory}%")
            if args.disk:
                print(f"  Disk: {args.disk}%")
            print(f"Config file: {GLOBAL_CONFIG_FILE}")
            return 0
        else:
            print("Update failed")
            return 1

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def cmd_init(args):
    """Initialize config file"""
    try:
        config_path = create_default_global_config()
        print(f"✓ Config file created: {config_path}")
        print()
        print("Please edit the config file to add server info:")
        print(f"  {config_path}")
        print()
        print("Or use command to add server:")
        print("  bt-config add --name <name> --host <address> --token <key>")
        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def cmd_show(args):
    """Show full config"""
    try:
        config_path = find_config_file()
        if not config_path:
            print("Config file not found")
            print("Run 'bt-config init' to create config file")
            return 1

        config = load_config(config_path)

        if args.format == "json":
            print(json.dumps(config, ensure_ascii=False, indent=2))
        else:
            import yaml
            print(yaml.dump(config, default_flow_style=False, allow_unicode=True, sort_keys=False))

        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def cmd_path(args):
    """Show config file path"""
    config_path = find_config_file()
    print(f"Global config: {GLOBAL_CONFIG_FILE}")
    print(f"Global config exists: {'Yes' if GLOBAL_CONFIG_FILE.exists() else 'No'}")
    if config_path:
        print(f"Currently using: {config_path}")
    else:
        print("Currently using: Not configured")
    print()
    print("Config priority:")
    print("  1. BT_CONFIG_PATH environment variable")
    print(f"  2. Global config: {GLOBAL_CONFIG_FILE}")
    print("  3. Local config: config/servers.local.yaml")
    print("  4. Default config: config/servers.yaml")
    return 0


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="aaPanel Configuration Management Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Initialize config file
  bt-config init

  # List all servers
  bt-config list

  # Add server (SSL verification enabled by default)
  bt-config add --name prod-01 --host https://panel.example.com:8888 --token YOUR_TOKEN

  # Add server (disable SSL verification for self-signed certs)
  bt-config add --name prod-01 --host https://panel.example.com:8888 --token YOUR_TOKEN --verify-ssl false

  # Update server
  bt-config update prod-01 --host https://new.example.com:8888

  # Disable server
  bt-config update prod-01 --disabled

  # Update SSL verification setting
  bt-config update prod-01 --verify-ssl false

  # Remove server
  bt-config remove prod-01

  # Set alert thresholds
  bt-config threshold --cpu 75 --memory 80

  # Show config file path
  bt-config path

  # Show full config
  bt-config show
  bt-config show --format json
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # list command
    subparsers.add_parser("list", help="List all server configurations")

    # add command
    add_parser = subparsers.add_parser("add", help="Add server configuration")
    add_parser.add_argument("--name", "-n", required=True, help="Server name")
    add_parser.add_argument("--host", "-H", required=True, help="Panel address (e.g., https://panel.example.com:8888)")
    add_parser.add_argument("--token", "-t", required=True, help="API Token")
    add_parser.add_argument("--timeout", type=int, default=10000, help="Timeout (milliseconds), default 10000")
    add_parser.add_argument("--disabled", action="store_true", help="Disable this server")
    add_parser.add_argument("--force", "-f", action="store_true", help="Force overwrite existing config")
    add_parser.add_argument("--verify-ssl", type=lambda x: x.lower() in ("true", "1", "yes"), default=None, help="Whether to verify SSL certificate (true/false), default true")

    # remove command
    remove_parser = subparsers.add_parser("remove", help="Remove server configuration")
    remove_parser.add_argument("name", help="Server name")

    # update command
    update_parser = subparsers.add_parser("update", help="Update server configuration")
    update_parser.add_argument("name", help="Server name")
    update_parser.add_argument("--host", "-H", help="Panel address")
    update_parser.add_argument("--token", "-t", help="API Token")
    update_parser.add_argument("--timeout", type=int, help="Timeout (milliseconds)")
    update_parser.add_argument("--disabled", type=lambda x: x.lower() in ("true", "1", "yes"), help="Whether to disable (true/false)")
    update_parser.add_argument("--verify-ssl", type=lambda x: x.lower() in ("true", "1", "yes"), default=None, help="Whether to verify SSL certificate (true/false)")

    # threshold command
    threshold_parser = subparsers.add_parser("threshold", help="Set alert thresholds")
    threshold_parser.add_argument("--cpu", type=int, help="CPU usage threshold (%)")
    threshold_parser.add_argument("--memory", type=int, help="Memory usage threshold (%)")
    threshold_parser.add_argument("--disk", type=int, help="Disk usage threshold (%)")

    # init command
    subparsers.add_parser("init", help="Initialize config file")

    # show command
    show_parser = subparsers.add_parser("show", help="Show full config")
    show_parser.add_argument("--format", "-f", choices=["yaml", "json"], default="yaml", help="Output format")

    # path command
    subparsers.add_parser("path", help="Show config file path")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    # Dispatch commands
    commands = {
        "list": cmd_list,
        "add": cmd_add,
        "remove": cmd_remove,
        "update": cmd_update,
        "threshold": cmd_threshold,
        "init": cmd_init,
        "show": cmd_show,
        "path": cmd_path,
    }

    handler = commands.get(args.command)
    if handler:
        return handler(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
