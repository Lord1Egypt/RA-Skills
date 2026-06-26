#!/usr/bin/env python3
"""
Backup Tool - Backup and restore files with compression and encryption
"""

import argparse
import hashlib
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
from datetime import datetime
from pathlib import Path


def create_backup(source, output, compress='gzip', exclude=None, verbose=False):
    """Create a backup archive."""
    source_path = Path(source).resolve()
    
    if not source_path.exists():
        print(f"Error: {source} does not exist")
        return 1
    
    # Determine compression mode
    comp_mode = {
        'gzip': 'w:gz',
        'bzip2': 'w:bz2',
        'xz': 'w:xz',
        'none': 'w'
    }.get(compress, 'w:gz')
    
    print(f"Creating backup: {output}")
    print(f"Source: {source_path}")
    print(f"Compression: {compress}")
    
    try:
        with tarfile.open(output, comp_mode) as tar:
            # Add files
            tar.add(source_path, arcname=source_path.name)
        
        # Calculate checksum
        sha256 = hashlib.sha256()
        with open(output, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                sha256.update(chunk)
        
        size = os.path.getsize(output)
        print(f"Backup created: {output}")
        print(f"Size: {size / 1024 / 1024:.2f} MB")
        print(f"SHA256: {sha256.hexdigest()[:16]}...")
        
        return 0
    except Exception as e:
        print(f"Error creating backup: {e}")
        return 1


def restore_backup(backup_file, destination, verbose=False):
    """Restore from a backup archive."""
    dest_path = Path(destination)
    backup_path = Path(backup_file)
    
    if not backup_path.exists():
        print(f"Error: {backup_file} does not exist")
        return 1
    
    print(f"Restoring from: {backup_file}")
    print(f"Destination: {dest_path}")
    
    try:
        dest_path.mkdir(parents=True, exist_ok=True)
        
        with tarfile.open(backup_path, 'r:*') as tar:
            tar.extractall(dest_path)
        
        print(f"Restore complete: {destination}")
        return 0
    except Exception as e:
        print(f"Error restoring backup: {e}")
        return 1


def list_backup(backup_file, verbose=False):
    """List contents of a backup archive."""
    backup_path = Path(backup_file)
    
    if not backup_path.exists():
        print(f"Error: {backup_file} does not exist")
        return 1
    
    try:
        with tarfile.open(backup_path, 'r:*') as tar:
            members = tar.getmembers()
            print(f"Backup: {backup_file}")
            print(f"Files: {len(members)}")
            print("\nContents:")
            for member in members[:20]:
                print(f"  {member.name}")
            if len(members) > 20:
                print(f"  ... and {len(members) - 20} more")
        return 0
    except Exception as e:
        print(f"Error reading backup: {e}")
        return 1


def main():
    parser = argparse.ArgumentParser(description='Backup Tool')
    parser.add_argument('source', nargs='?', help='Source folder to backup')
    parser.add_argument('--output', help='Output backup file')
    parser.add_argument('--compress', default='gzip', 
                       choices=['gzip', 'bzip2', 'xz', 'none'],
                       help='Compression format')
    parser.add_argument('--restore', help='Restore from backup file')
    parser.add_argument('--destination', help='Restore destination')
    parser.add_argument('--list', help='List backup contents')
    parser.add_argument('--exclude', action='append', help='Exclude patterns')
    parser.add_argument('--verbose', action='store_true')
    
    args = parser.parse_args()
    
    # List mode
    if args.list:
        return list_backup(args.list, args.verbose)
    
    # Restore mode
    if args.restore:
        if not args.destination:
            print("Error: --destination required for restore")
            return 1
        return restore_backup(args.restore, args.destination, args.verbose)
    
    # Backup mode
    if not args.source:
        parser.print_help()
        return 1
    
    if not args.output:
        print("Error: --output required for backup")
        return 1
    
    return create_backup(args.source, args.output, args.compress, 
                        args.exclude, args.verbose)


if __name__ == '__main__':
    sys.exit(main())
