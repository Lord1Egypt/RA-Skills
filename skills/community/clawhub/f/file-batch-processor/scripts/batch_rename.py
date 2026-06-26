#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch File Renaming Tool
Supports multiple renaming modes: sequence, date, prefix/suffix, batch replacement, etc.
"""

import os
import sys
import re
from datetime import datetime
import argparse

def rename_files(folder_path, mode='sequence', prefix='', suffix='', start_num=1, 
                 replace_old='', replace_new='', date_format='%Y%m%d', dry_run=False):
    """
    Batch rename files
    
    Args:
        folder_path: Folder path
        mode: Renaming mode ('sequence', 'date', 'prefix', 'suffix', 'replace')
        prefix: Prefix
        suffix: Suffix  
        start_num: Starting number
        replace_old: Old string to replace
        replace_new: New string to replace with
        date_format: Date format
        dry_run: Whether to preview only without execution
    """
    if not os.path.exists(folder_path):
        print(f"Error: Folder does not exist {folder_path}")
        return False
    
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    if not files:
        print("Warning: No files found in the folder")
        return True
    
    print(f"Found {len(files)} files, preparing to rename...")
    
    renamed_count = 0
    for i, filename in enumerate(files):
        old_path = os.path.join(folder_path, filename)
        
        # Separate filename and extension
        name, ext = os.path.splitext(filename)
        
        # Generate new filename based on mode
        if mode == 'sequence':
            new_name = f"{prefix}{str(start_num + i).zfill(3)}{suffix}{ext}"
        elif mode == 'date':
            date_str = datetime.now().strftime(date_format)
            new_name = f"{prefix}{date_str}{suffix}{ext}"
        elif mode == 'prefix':
            new_name = f"{prefix}{name}{suffix}{ext}"
        elif mode == 'suffix':
            new_name = f"{name}{suffix}{ext}"
        elif mode == 'replace':
            new_name = filename.replace(replace_old, replace_new)
        else:
            print(f"Unknown renaming mode: {mode}")
            continue
        
        new_path = os.path.join(folder_path, new_name)
        
        # Check for duplicate names
        if old_path == new_path:
            continue
            
        if dry_run:
            print(f"Preview: {filename} → {new_name}")
        else:
            try:
                os.rename(old_path, new_path)
                print(f"Renamed: {filename} → {new_name}")
                renamed_count += 1
            except Exception as e:
                print(f"Rename failed {filename}: {e}")
    
    print(f"Complete! Total {renamed_count} files renamed")
    return True

def main():
    parser = argparse.ArgumentParser(description='Batch File Renaming Tool')
    parser.add_argument('folder', help='Folder path to process')
    parser.add_argument('--mode', choices=['sequence', 'date', 'prefix', 'suffix', 'replace'], 
                        default='sequence', help='Renaming mode')
    parser.add_argument('--prefix', default='', help='Prefix')
    parser.add_argument('--suffix', default='', help='Suffix')
    parser.add_argument('--start', type=int, default=1, help='Starting number')
    parser.add_argument('--replace-old', default='', help='Old string to replace')
    parser.add_argument('--replace-new', default='', help='New string to replace with')
    parser.add_argument('--date-format', default='%Y%m%d', help='Date format')
    parser.add_argument('--dry-run', action='store_true', help='Preview only without execution')
    
    args = parser.parse_args()
    
    rename_files(
        folder_path=args.folder,
        mode=args.mode,
        prefix=args.prefix,
        suffix=args.suffix,
        start_num=args.start,
        replace_old=args.replace_old,
        replace_new=args.replace_new,
        date_format=args.date_format,
        dry_run=args.dry_run
    )

if __name__ == "__main__":
    main()