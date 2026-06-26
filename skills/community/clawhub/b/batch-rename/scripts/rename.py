#!/usr/bin/env python3
"""
Batch Rename
Batch rename images and annotation files
"""

import argparse
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple


def get_image_files(directory: str, extensions: List[str]) -> List[str]:
    """Get all image files from directory"""
    directory = Path(directory)
    image_files = []
    
    for ext in extensions:
        image_files.extend(directory.glob(f"*.{ext}"))
        image_files.extend(directory.glob(f"*.{ext.upper()}"))
    
    return sorted([str(f) for f in image_files if f.is_file()])


def generate_new_name(original_path: str, pattern: str, prefix: str, suffix: str, 
                     index: int, start: int, date_str: str) -> str:
    """Generate new filename based on pattern"""
    original = Path(original_path)
    stem = original.stem
    ext = original.suffix
    
    # Apply pattern
    new_stem = pattern.format(index - 1 + start)
    new_stem = new_stem.replace('{original}', stem)
    new_stem = new_stem.replace('{date}', date_str)
    
    # Apply prefix and suffix
    new_stem = prefix + new_stem + suffix
    
    return new_stem + ext.lower()


def cmd_rename(args):
    """Batch rename files"""
    # Get image files
    extensions = args.extensions.split(',')
    image_files = get_image_files(args.directory, extensions)
    
    if not image_files:
        print("No image files found")
        return
    
    print(f"Found {len(image_files)} images")
    
    # Get annotations directory
    ann_dir = args.annotations
    if ann_dir:
        ann_dir = Path(ann_dir)
    
    # Generate preview
    date_str = datetime.now().strftime('%Y%m%d')
    renames = []
    
    for i, img_path in enumerate(image_files, 1):
        new_name = generate_new_name(
            img_path, args.pattern, args.prefix, args.suffix,
            i, args.start, date_str
        )
        
        ann_path = None
        new_ann_path = None
        
        if ann_dir:
            # Check for annotation file
            original_stem = Path(img_path).stem
            for ext in ['.txt', '.json', '.xml']:
                potential_ann = ann_dir / f"{original_stem}{ext}"
                if potential_ann.exists():
                    ann_path = potential_ann
                    new_ann_path = ann_dir / (Path(new_name).stem + ext)
                    break
        
        renames.append({
            'old_img': img_path,
            'new_img': new_name,
            'old_ann': ann_path,
            'new_ann': new_ann_path
        })
    
    # Preview
    print(f"\nPreview (first {min(10, len(renames))}):")
    for r in renames[:10]:
        print(f"  {Path(r['old_img']).name} -> {r['new_img']}")
        if r['old_ann']:
            print(f"    + {r['old_ann'].name} -> {r['new_ann'].name}")
    
    if args.preview:
        print("\n(Preview only - no changes made)")
        return
    
    # Confirm
    confirm = input(f"\nApply changes to {len(renames)} files? (y/n): ")
    if confirm.lower() != 'y':
        print("Cancelled")
        return
    
    # Apply renames
    # First, check for conflicts
    new_names = [r['new_img'] for r in renames]
    if len(new_names) != len(set(new_names)):
        print("Error: Duplicate filenames would be created")
        return
    
    # Rename files
    renamed_images = 0
    renamed_annotations = 0
    errors = []
    
    for r in renames:
        old_path = Path(args.directory) / Path(r['old_img']).name
        new_path = Path(args.directory) / r['new_img']
        
        try:
            # Handle overwrite
            if args.force and new_path.exists():
                new_path.unlink()
            
            old_path.rename(new_path)
            renamed_images += 1
            
            # Rename annotation if exists
            if r['old_ann'] and r['new_ann']:
                if args.force and r['new_ann'].exists():
                    r['new_ann'].unlink()
                r['old_ann'].rename(r['new_ann'])
                renamed_annotations += 1
        
        except Exception as e:
            errors.append(f"{old_path.name}: {e}")
    
    print(f"\n✓ Renamed {renamed_images} images")
    print(f"✓ Renamed {renamed_annotations} annotation files")
    
    if errors:
        print(f"\nErrors:")
        for err in errors:
            print(f"  {err}")


def cmd_restore(args):
    """Restore from backup"""
    backup_file = Path(args.directory) / ".rename_backup.json"
    
    if not backup_file.exists():
        print("No backup found")
        return
    
    import json
    with open(backup_file, 'r') as f:
        backup = json.load(f)
    
    print(f"Found backup with {len(backup)} files")
    
    confirm = input("Restore original filenames? (y/n): ")
    if confirm.lower() != 'y':
        print("Cancelled")
        return
    
    restored = 0
    for item in backup:
        try:
            current = Path(item['current'])
            original = Path(item['original'])
            if current.exists():
                current.rename(original)
                restored += 1
        except Exception as e:
            print(f"Error: {e}")
    
    print(f"✓ Restored {restored} files")
    backup_file.unlink()


def main():
    parser = argparse.ArgumentParser(
        description="Batch Rename - Rename images and annotation files"
    )
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # rename command
    parser_rename = subparsers.add_parser("rename", help="Batch rename files")
    parser_rename.add_argument("directory", help="Directory containing images")
    parser_rename.add_argument("--pattern", "-p", default="img_{:04d}",
                              help="Output filename pattern (default: img_{:04d})")
    parser_rename.add_argument("--prefix", default="",
                              help="Add prefix to filename")
    parser_rename.add_argument("--suffix", default="",
                              help="Add suffix to filename (before extension)")
    parser_rename.add_argument("--start", type=int, default=1,
                              help="Starting number (default: 1)")
    parser_rename.add_argument("--annotations", "-a",
                              help="Path to annotation files")
    parser_rename.add_argument("--preview", action="store_true",
                              help="Preview changes without applying")
    parser_rename.add_argument("--force", "-f", action="store_true",
                              help="Overwrite existing files")
    parser_rename.add_argument("--extensions", "-e", default="jpg,jpeg,png,bmp",
                              help="Image extensions")
    parser_rename.set_defaults(func=cmd_rename)
    
    # restore command
    parser_restore = subparsers.add_parser("restore", help="Restore from backup")
    parser_restore.add_argument("directory", help="Directory containing images")
    parser_restore.set_defaults(func=cmd_restore)
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        return
    
    try:
        args.func(args)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
