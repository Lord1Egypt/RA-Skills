#!/usr/bin/env python3
"""
aaPanel File Extraction Script

Features:
- Extract zip/tar.gz/tar.bz2 files
- Support password-protected archives
- Set directory permissions after extraction

API Reference:
- /files?action=UnZip - Extract files
"""

import sys
import argparse
from pathlib import Path

# Add parent directory to sys.path to support importing bt_common
_script_dir = Path(__file__).parent
_skill_root = _script_dir.parent
if (_skill_root / "bt_common").exists():
    sys.path.insert(0, str(_skill_root))
else:
    sys.path.insert(0, str(_skill_root.parent))

from bt_common.bt_client import BtClient, BtClientManager
from bt_common.config import get_servers


def get_client(server_name: str = None) -> BtClient:
    """Get aaPanel client."""
    if server_name:
        servers = get_servers()
        for server in servers:
            name = server.name if hasattr(server, 'name') else server.get('name')
            if name == server_name:
                config = {
                    'name': server.name if hasattr(server, 'name') else server.get('name'),
                    'host': server.host if hasattr(server, 'host') else server.get('host'),
                    'token': server.token if hasattr(server, 'token') else server.get('token'),
                    'timeout': server.timeout if hasattr(server, 'timeout') else server.get('timeout', 10000),
                    'verify_ssl': server.verify_ssl if hasattr(server, 'verify_ssl') else server.get('verify_ssl', True)
                }
                return BtClient(
                    name=config['name'],
                    host=config['host'],
                    token=config['token'],
                    timeout=config['timeout'],
                    verify_ssl=config['verify_ssl']
                )
        raise ValueError(f"Server not found: {server_name}")
    else:
        manager = BtClientManager()
        return manager.get_client()


def get_archive_type(filepath: str) -> str:
    """Determine archive type from file extension."""
    filepath = filepath.lower()
    if filepath.endswith('.zip'):
        return 'zip'
    elif filepath.endswith('.tar.gz') or filepath.endswith('.tgz'):
        return 'tar.gz'
    elif filepath.endswith('.tar.bz2') or filepath.endswith('.tbz2'):
        return 'tar.bz2'
    elif filepath.endswith('.tar'):
        return 'tar'
    elif filepath.endswith('.gz'):
        return 'gz'
    elif filepath.endswith('.bz2'):
        return 'bz2'
    elif filepath.endswith('.rar'):
        return 'rar'
    elif filepath.endswith('.7z'):
        return '7z'
    else:
        return 'zip'  # default zip


def format_size(size_bytes: int) -> str:
    """Format file size."""
    if size_bytes < 1024:
        return f"{size_bytes}B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f}KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f}MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.2f}GB"


def cmd_unzip(args):
    """Extract archive."""
    client = get_client(args.server)

    # Auto-detect archive type
    archive_type = args.type or get_archive_type(args.source)

    print(f"\n📤 Extracting file...")
    print(f"   Source: {args.source}")
    print(f"   Destination: {args.dest}")
    print(f"   Archive type: {archive_type}")
    if args.password:
        print(f"   Password: {'*' * len(args.password)}")
    print(f"   Directory permissions: {args.permission}")
    print()

    endpoint = "/files?action=UnZip"
    params = {
        "sfile": args.source,
        "dfile": args.dest,
        "type": archive_type,
        "coding": args.coding,
        "password": args.password or "",
        "power": args.permission
    }

    try:
        result = client.request(endpoint, params)

        if result.get('status'):
            print(f"✅ {result.get('msg', 'File extracted successfully!')}")
            print(f"   Extracted to: {args.dest}")
            return 0
        else:
            print(f"❌ Extraction failed: {result.get('msg', 'Unknown error')}")
            return 1

    except Exception as e:
        print(f"❌ Request failed: {e}")
        return 1


def cmd_info(args):
    """Show archive info."""
    client = get_client(args.server)

    # Get file info
    endpoint = "/files?action=GetFileBody"
    params = {
        "path": args.source
    }

    print(f"\n📦 Archive info: {args.source}")
    print("-" * 50)

    # API may not support preview, show basic info
    archive_type = get_archive_type(args.source)
    print(f"   Archive type: {archive_type}")
    print(f"   File path: {args.source}")
    print()
    print("💡 Use unzip command to extract this file")


def cmd_support(args):
    """Show supported archive formats."""
    print("\n📦 Supported archive formats:")
    print("-" * 50)

    formats = [
        ("zip", "ZIP archive", "Most common"),
        ("tar.gz", "Gzip archive", "Common on Linux"),
        ("tar.bz2", "Bzip2 archive", "High compression"),
        ("tar", "TAR archive", "No compression"),
        ("gz", "Gzip single file", "Single file compression"),
        ("bz2", "Bzip2 single file", "Single file compression"),
        ("rar", "RAR archive", "Requires unrar"),
        ("7z", "7-Zip archive", "High compression ratio"),
    ]

    for fmt, name, note in formats:
        print(f"   {fmt:<10} {name:<20} ({note})")

    print()
    print("💡 Auto-detection: automatically identifies archive type from file extension")


def main():
    parser = argparse.ArgumentParser(
        description="aaPanel file extraction tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract WordPress (auto-detect type)
  python3 unzip.py -s "herobox" unzip \\
      --source "/www/test/wordpress.zip" \\
      --dest "/www/test"

  # Extract password-protected archive
  python3 unzip.py -s "herobox" unzip \\
      --source "/www/test/protected.zip" \\
      --dest "/www/test" \\
      --password "mypassword"

  # Extract tar.gz with permissions
  python3 unzip.py -s "herobox" unzip \\
      --source "/www/test/backup.tar.gz" \\
      --dest "/www/backup" \\
      --permission 755

  # Show supported formats
  python3 unzip.py support
        """
    )

    # Global arguments
    parser.add_argument('-s', '--server', help='Server name')

    subparsers = parser.add_subparsers(dest='command', help='Subcommands')

    # unzip command
    unzip_parser = subparsers.add_parser('unzip', help='Extract files')
    unzip_parser.add_argument('--source', required=True, help='Source file path (archive path)')
    unzip_parser.add_argument('--dest', required=True, help='Destination directory (where to extract)')
    unzip_parser.add_argument('--type', choices=['zip', 'tar.gz', 'tar.bz2', 'tar', 'gz', 'bz2', 'rar', '7z'],
                              help='Archive type (auto-detect)')
    unzip_parser.add_argument('--password', help='Extraction password (if any)')
    unzip_parser.add_argument('--coding', default='UTF-8', help='Filename encoding (default UTF-8)')
    unzip_parser.add_argument('--permission', default='755', help='Post-extraction directory permissions (default 755)')
    unzip_parser.set_defaults(func=cmd_unzip)

    # info command
    info_parser = subparsers.add_parser('info', help='Show archive info')
    info_parser.add_argument('--source', required=True, help='Archive path')
    info_parser.set_defaults(func=cmd_info)

    # support command
    support_parser = subparsers.add_parser('support', help='Show supported archive formats')
    support_parser.set_defaults(func=cmd_support)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())