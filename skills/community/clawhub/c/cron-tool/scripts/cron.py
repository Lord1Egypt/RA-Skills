#!/usr/bin/env python3
"""Cron Tool - Manage cron jobs easily."""

import argparse
import subprocess
import sys
import os
import tempfile
from datetime import datetime
from typing import List, Optional


def get_crontab() -> str:
    """Get current crontab content."""
    try:
        result = subprocess.run(
            ["crontab", "-l"], capture_output=True, text=True, check=True
        )
        return result.stdout
    except subprocess.CalledProcessError:
        return ""
    except FileNotFoundError:
        return ""


def write_crontab(content: str) -> bool:
    """Write content to crontab."""
    try:
        # Use stdin to avoid temp file issues
        proc = subprocess.Popen(
            ["crontab", "-"], 
            stdin=subprocess.PIPE, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        proc.communicate(input=content.encode())
        return proc.returncode == 0
    except Exception as e:
        print(f"Error writing crontab: {e}", file=sys.stderr)
        return False


def list_crons() -> None:
    """List all cron jobs."""
    content = get_crontab()
    
    if not content.strip():
        print("No crontab for current user")
        return
    
    print("Current crontab:")
    print("-" * 60)
    print(content)
    print("-" * 60)


def add_cron(schedule: str, command: str, comment: Optional[str] = None) -> bool:
    """Add a new cron job."""
    content = get_crontab()
    
    # Validate schedule format (basic check)
    parts = schedule.split()
    if len(parts) != 5:
        print("Error: Invalid schedule format. Use: minute hour day month weekday", file=sys.stderr)
        return False
    
    # Build the cron line
    cron_line = f"{schedule} {command}"
    if comment:
        cron_line = f"{cron_line} # {comment}"
    
    # Append to existing crontab
    if content.strip():
        content += "\n"
    content += cron_line + "\n"
    
    if write_crontab(content):
        print(f"Added cron job: {schedule} {command}")
        if comment:
            print(f"  Comment: {comment}")
        return True
    else:
        print("Error: Failed to add cron job", file=sys.stderr)
        return False


def remove_cron(identifier: str) -> bool:
    """Remove a cron job by ID (line number) or command pattern."""
    content = get_crontab()
    lines = content.splitlines()
    
    new_lines = []
    removed = False
    
    # Try to remove by line number
    if identifier.isdigit():
        idx = int(identifier) - 1
        if 0 <= idx < len(lines):
            removed_line = lines.pop(idx)
            print(f"Removed cron job (line {identifier}): {removed_line}")
            removed = True
    else:
        # Remove by command pattern
        new_lines = []
        for line in lines:
            if identifier not in line and not line.strip().startswith('#'):
                new_lines.append(line)
            elif identifier in line:
                print(f"Removed: {line.strip()}")
                removed = True
    
    if not removed:
        print(f"No cron job found matching: {identifier}", file=sys.stderr)
        return False
    
    new_content = "\n".join(new_lines) + "\n"
    return write_crontab(new_content)


def enable_cron(identifier: str) -> bool:
    """Enable a disabled cron job (uncomment)."""
    content = get_crontab()
    lines = content.splitlines()
    
    enabled = False
    new_lines = []
    
    for line in lines:
        if identifier in line and line.strip().startswith('#'):
            # Uncomment the line
            new_lines.append(line[1:].strip())
            enabled = True
            print(f"Enabled: {new_lines[-1]}")
        else:
            new_lines.append(line)
    
    if not enabled:
        print(f"No disabled cron job found matching: {identifier}", file=sys.stderr)
        return False
    
    new_content = "\n".join(new_lines) + "\n"
    return write_crontab(new_content)


def disable_cron(identifier: str) -> bool:
    """Disable a cron job (comment out)."""
    content = get_crontab()
    lines = content.splitlines()
    
    disabled = False
    new_lines = []
    
    for line in lines:
        if identifier in line and not line.strip().startswith('#'):
            # Comment out the line
            new_lines.append("# " + line)
            disabled = True
            print(f"Disabled: {line.strip()}")
        else:
            new_lines.append(line)
    
    if not disabled:
        print(f"No active cron job found matching: {identifier}", file=sys.stderr)
        return False
    
    new_content = "\n".join(new_lines) + "\n"
    return write_crontab(new_content)


def backup_crons(filepath: str) -> bool:
    """Backup crontab to file."""
    content = get_crontab()
    
    try:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Backed up crontab to: {filepath}")
        return True
    except Exception as e:
        print(f"Error backing up: {e}", file=sys.stderr)
        return False


def restore_crons(filepath: str) -> bool:
    """Restore crontab from backup."""
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}", file=sys.stderr)
        return False
    
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        
        # Ask for confirmation
        print("Warning: This will replace your current crontab")
        print("Current crontab:")
        print("-" * 40)
        print(get_crontab() or "(empty)")
        print("-" * 40)
        print("New crontab:")
        print("-" * 40)
        print(content)
        print("-" * 40)
        
        confirm = input("Proceed? (y/n): ")
        if confirm.lower() != 'y':
            print("Cancelled")
            return False
        
        if write_crontab(content):
            print("Restored crontab from backup")
            return True
        else:
            print("Error restoring crontab", file=sys.stderr)
            return False
    except Exception as e:
        print(f"Error restoring: {e}", file=sys.stderr)
        return False


def edit_crontab() -> bool:
    """Edit crontab in editor."""
    content = get_crontab()
    
    # Create temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.cron', delete=False) as f:
        f.write(content)
        temp_file = f.name
    
    try:
        # Open in editor
        editor = os.environ.get('EDITOR', 'vim')
        subprocess.call([editor, temp_file])
        
        # Read back
        with open(temp_file, 'r') as f:
            new_content = f.read()
        
        # Write to crontab
        if write_crontab(new_content):
            print("Updated crontab")
            return True
        else:
            print("Error updating crontab", file=sys.stderr)
            return False
    finally:
        os.unlink(temp_file)


def main():
    parser = argparse.ArgumentParser(description='Cron job management tool')
    
    parser.add_argument('--list', '-l', action='store_true', help='List cron jobs')
    parser.add_argument('--add', nargs=2, metavar=('SCHEDULE', 'COMMAND'), help='Add cron job')
    parser.add_argument('--comment', help='Comment for cron job (use with --add)')
    parser.add_argument('--remove', metavar='ID', help='Remove cron job (line number or command)')
    parser.add_argument('--enable', metavar='ID', help='Enable a disabled cron job')
    parser.add_argument('--disable', metavar='ID', help='Disable a cron job')
    parser.add_argument('--backup', metavar='FILE', help='Backup crontab to file')
    parser.add_argument('--restore', metavar='FILE', help='Restore crontab from file')
    parser.add_argument('--edit', '-e', action='store_true', help='Edit crontab in editor')
    
    args = parser.parse_args()
    
    if args.list:
        list_crons()
    elif args.add:
        add_cron(args.add[0], args.add[1], args.comment)
    elif args.remove:
        remove_cron(args.remove)
    elif args.enable:
        enable_cron(args.enable)
    elif args.disable:
        disable_cron(args.disable)
    elif args.backup:
        backup_crons(args.backup)
    elif args.restore:
        restore_crons(args.restore)
    elif args.edit:
        edit_crontab()
    else:
        parser.print_help()
        print("\nExamples:")
        print("  cron-tool --list                           # List cron jobs")
        print('  cron-tool --add "*/5 * * * *" "script.sh"  # Add job')
        print("  cron-tool --remove 3                       # Remove line 3")
        print("  cron-tool --backup my-crons.txt            # Backup")
        print("  cron-tool --edit                           # Edit in vim")


if __name__ == '__main__':
    main()
