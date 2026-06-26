#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto File Organization Tool
Automatically categorize files by type into different folders
"""

import os
import shutil
import sys
import argparse
from pathlib import Path

def organize_files(folder_path, dry_run=False):
    """
    Automatically categorize and organize files
    
    Args:
        folder_path: Folder path
        dry_run: Whether to preview only without execution
    """
    if not os.path.exists(folder_path):
        print(f"Error: Folder does not exist {folder_path}")
        return False
    
    # Categorization rules
    categories = {
        'Documents': ['.doc', '.docx', '.pdf', '.txt', '.md', '.rtf'],
        'Images': ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff'],
        'Audio': ['.mp3', '.wav', '.aac', '.ogg', '.m4a'],
        'Video': ['.mp4', '.avi', '.mkv', '.mov', '.wmv'],
        'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz'],
        'Others': []
    }
    
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    
    if not files:
        print("Warning: No files found in the folder")
        return True
    
    print(f"Found {len(files)} files, preparing to categorize...")
    
    # Create category folders
    for category in categories.keys():
        category_folder = os.path.join(folder_path, category)
        if not os.path.exists(category_folder):
            if not dry_run:
                os.makedirs(category_folder)
            print(f"Created folder: {category}")
    
    organized_count = 0
    for filename in files:
        old_path = os.path.join(folder_path, filename)
        name, ext = os.path.splitext(filename)
        
        # Determine file category
        category = 'Others'
        for cat, extensions in categories.items():
            if ext.lower() in extensions:
                category = cat
                break
        
        # Target path
        new_path = os.path.join(folder_path, category, filename)
        
        try:
            if dry_run:
                print(f"Preview: {filename} → {category}/")
            else:
                # Move file
                shutil.move(old_path, new_path)
                print(f"Organized: {filename} → {category}/")
                organized_count += 1
                
        except Exception as e:
            print(f"Organization failed {filename}: {e}")
    
    print(f"Complete! Total {organized_count} files organized")
    return True

def main():
    parser = argparse.ArgumentParser(description='Auto File Organization Tool')
    parser.add_argument('folder', help='Folder path to process')
    parser.add_argument('--dry-run', action='store_true', help='Preview only without execution')
    
    args = parser.parse_args()
    
    organize_files(
        folder_path=args.folder,
        dry_run=args.dry_run
    )

if __name__ == "__main__":
    main()