#!/usr/bin/env python3
# coding: utf-8
"""
aaPanel File Operations CLI Tool
Provides basic file management commands
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

# Import compatible with dev and release environments
# release environment: bt_common/ (scripts in scripts/)
# dev environment: src/bt_common/ (scripts in src/btpanel_files/scripts/)
_skill_root = Path(__file__).parent.parent  # skill package root directory

# Prioritize release environment (skill package root), then dev environment
if (_skill_root / "bt_common").exists():
    sys.path.insert(0, str(_skill_root))
else:
    sys.path.insert(0, str(_skill_root.parent / "src"))

from bt_common.utils import format_bytes, format_timestamp


def format_size(size: int, is_dir: bool = False) -> str:
    """Format file size display"""
    if is_dir:
        # Directory size is usually in KB
        if size >= 1024 * 1024:
            return f"{size / (1024 * 1024):.1f}GB"
        elif size >= 1024:
            return f"{size / 1024:.1f}MB"
        else:
            return f"{size}KB"
    else:
        # File size is in bytes
        if size >= 1024 * 1024 * 1024:
            return f"{size / (1024 * 1024 * 1024):.1f}GB"
        elif size >= 1024 * 1024:
            return f"{size / (1024 * 1024):.1f}MB"
        elif size >= 1024:
            return f"{size / 1024:.1f}KB"
        else:
            return f"{size}B"


def format_time(timestamp: int) -> str:
    """Format timestamp"""
    try:
        return datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
    except:
        return str(timestamp)


def cmd_ls(args):
    """List directory contents"""
    from bt_common.files_client import FilesClient

    client = FilesClient(args.server)
    result = client.get_dir(args.path, args.page, args.rows)

    if 'error' in result:
        print(f"Error: {result['error']}")
        return 1

    # Print path
    print(f"\n📁 {result.get('path', args.path)}\n")

    # Print directory list
    dirs = result.get('dir', [])
    files = result.get('files', [])

    if dirs:
        print("  Directories:")
        for d in dirs:
            name = d.get('nm', 'unknown')
            size = format_size(d.get('sz', 0), is_dir=True)
            mtime = format_time(d.get('mt', 0))
            acc = d.get('acc', '---')
            user = d.get('user', 'unknown')
            print(f"    📁 {name:<30} {size:>8}  {acc:<5}  {user:<10}  {mtime}")

    if files:
        print("\n  Files:")
        for f in files:
            name = f.get('nm', 'unknown')
            size = format_size(f.get('sz', 0), is_dir=False)
            mtime = format_time(f.get('mt', 0))
            acc = f.get('acc', '---')
            user = f.get('user', 'unknown')
            # Show remark if any
            rmk = f.get('rmk', '')
            rmk_str = f"  # {rmk}" if rmk else ""
            print(f"    📄 {name:<30} {size:>8}  {acc:<5}  {user:<10}  {mtime}{rmk_str}")

    if not dirs and not files:
        print("  (Empty directory)")

    # Print pagination info
    page_info = result.get('page', '')
    if page_info:
        print(f"\n  {page_info}")

    return 0


def cmd_cat(args):
    """Read file content"""
    from bt_common.files_client import FilesClient

    client = FilesClient(args.server)
    result = client.get_file_body(args.path)

    if not result.get('status') and not result.get('only_read') == False:
        print(f"Error: {result.get('msg', 'Read failed')}")
        return 1

    data = result.get('data', '')

    if args.lines:
        # Show only last N lines
        lines = data.split('\n')
        data = '\n'.join(lines[-args.lines:])

    print(data)

    # Show file info
    if args.verbose:
        print(f"\n--- File Info ---", file=sys.stderr)
        print(f"Size: {format_bytes(result.get('size', 0))}", file=sys.stderr)
        print(f"Encoding: {result.get('encoding', 'utf-8')}", file=sys.stderr)
        print(f"Read-only: {'Yes' if result.get('only_read') else 'No'}", file=sys.stderr)

    return 0


def cmd_edit(args):
    """Edit file content"""
    from bt_common.files_client import FilesClient

    client = FilesClient(args.server)

    # If content parameter specified
    if args.content:
        content = args.content
    elif args.file:
        # Read content from file
        with open(args.file, 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        # Read from stdin
        content = sys.stdin.read()

    # Get current file's st_mtime
    try:
        file_info = client.get_file_body(args.path)
        st_mtime = file_info.get('st_mtime')
    except:
        st_mtime = None

    result = client.save_file_body(args.path, content, args.encoding, st_mtime)

    if result.get('status'):
        print(f"✅ File saved: {args.path}")
        return 0
    else:
        print(f"❌ Save failed: {result.get('msg', 'Unknown error')}")
        return 1


def cmd_mkdir(args):
    """Create directory"""
    from bt_common.files_client import FilesClient

    client = FilesClient(args.server)
    result = client.create_dir(args.path)

    if result.get('status'):
        print(f"✅ Directory created: {args.path}")
        return 0
    else:
        print(f"❌ Create failed: {result.get('msg', 'Unknown error')}")
        return 1


def cmd_touch(args):
    """Create file"""
    from bt_common.files_client import FilesClient

    client = FilesClient(args.server)
    result = client.create_file(args.path)

    if result.get('status'):
        print(f"✅ File created: {args.path}")
        return 0
    else:
        print(f"❌ Create failed: {result.get('msg', 'Unknown error')}")
        return 1


def cmd_rm(args):
    """Delete file"""
    from bt_common.files_client import FilesClient

    client = FilesClient(args.server)
    result = client.delete_file(args.path)

    if result.get('status'):
        msg = result.get('msg', 'Deleted')
        print(f"✅ {msg}: {args.path}")
        return 0
    else:
        print(f"❌ Delete failed: {result.get('msg', 'Unknown error')}")
        return 1


def cmd_rmdir(args):
    """Delete directory"""
    from bt_common.files_client import FilesClient

    client = FilesClient(args.server)
    result = client.delete_dir(args.path)

    if result.get('status'):
        msg = result.get('msg', 'Deleted')
        print(f"✅ {msg}: {args.path}")
        return 0
    else:
        print(f"❌ Delete failed: {result.get('msg', 'Unknown error')}")
        return 1


def cmd_stat(args):
    """View file permissions"""
    from bt_common.files_client import FilesClient

    client = FilesClient(args.server)
    result = client.get_file_access(args.path)

    if 'chmod' in result and 'chown' in result:
        print(f"File: {args.path}")
        print(f"Permissions: {result['chmod']}")
        print(f"Owner: {result['chown']}")
        return 0
    else:
        print(f"❌ Get failed: {result.get('msg', 'Unknown error')}")
        return 1


def cmd_chmod(args):
    """Set file permissions"""
    from bt_common.files_client import FilesClient

    client = FilesClient(args.server)
    result = client.set_file_access(
        args.path,
        args.access,
        user=args.user,
        group=args.group,
        all_files=args.recursive
    )

    if result.get('status'):
        print(f"✅ Permissions set: {args.path} -> {args.access}")
        return 0
    else:
        print(f"❌ Set failed: {result.get('msg', 'Unknown error')}")
        return 1


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='aaPanel File Operations Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '-s', '--server',
        help='Server name (name configured with bt-config)'
    )

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # ls command - List directory
    ls_parser = subparsers.add_parser('ls', help='List directory contents')
    ls_parser.add_argument('path', nargs='?', default='/www', help='Directory path')
    ls_parser.add_argument('-p', '--page', type=int, default=1, help='Page number')
    ls_parser.add_argument('-r', '--rows', type=int, default=500, help='Items per page')
    ls_parser.set_defaults(func=cmd_ls)

    # cat command - Read file
    cat_parser = subparsers.add_parser('cat', help='Read file content')
    cat_parser.add_argument('path', help='File path')
    cat_parser.add_argument('-n', '--lines', type=int, help='Show last N lines')
    cat_parser.add_argument('-v', '--verbose', action='store_true', help='Show file info')
    cat_parser.set_defaults(func=cmd_cat)

    # edit command - Edit file
    edit_parser = subparsers.add_parser('edit', help='Edit file content')
    edit_parser.add_argument('path', help='File path')
    edit_parser.add_argument('content', nargs='?', help='File content')
    edit_parser.add_argument('-f', '--file', help='Read content from file')
    edit_parser.add_argument('-e', '--encoding', default='utf-8', help='File encoding')
    edit_parser.set_defaults(func=cmd_edit)

    # mkdir command - Create directory
    mkdir_parser = subparsers.add_parser('mkdir', help='Create directory')
    mkdir_parser.add_argument('path', help='Directory path')
    mkdir_parser.set_defaults(func=cmd_mkdir)

    # touch command - Create file
    touch_parser = subparsers.add_parser('touch', help='Create file')
    touch_parser.add_argument('path', help='File path')
    touch_parser.set_defaults(func=cmd_touch)

    # rm command - Delete file
    rm_parser = subparsers.add_parser('rm', help='Delete file')
    rm_parser.add_argument('path', help='File path')
    rm_parser.set_defaults(func=cmd_rm)

    # rmdir command - Delete directory
    rmdir_parser = subparsers.add_parser('rmdir', help='Delete directory')
    rmdir_parser.add_argument('path', help='Directory path')
    rmdir_parser.set_defaults(func=cmd_rmdir)

    # stat command - View permissions
    stat_parser = subparsers.add_parser('stat', help='View file permissions')
    stat_parser.add_argument('path', help='File path')
    stat_parser.set_defaults(func=cmd_stat)

    # chmod command - Set permissions
    chmod_parser = subparsers.add_parser('chmod', help='Set file permissions')
    chmod_parser.add_argument('access', help='Permission code (e.g., 755, 644)')
    chmod_parser.add_argument('path', help='File path')
    chmod_parser.add_argument('-u', '--user', help='Owner username', default='www')
    chmod_parser.add_argument('-g', '--group', help='Group name', default='www')
    chmod_parser.add_argument('-R', '--recursive', action='store_true', help='Recursively set subdirectories and files')
    chmod_parser.set_defaults(func=cmd_chmod)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
