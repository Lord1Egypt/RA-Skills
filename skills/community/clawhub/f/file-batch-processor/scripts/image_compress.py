#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch Image Compression Tool
Supports JPEG and PNG formats, adjustable quality and size
"""

from PIL import Image
import os
import sys
import argparse
from pathlib import Path

def compress_images(folder_path, quality=70, resize_ratio=1.0, dry_run=False):
    """
    Batch compress images
    
    Args:
        folder_path: Folder path
        quality: Compression quality (1-100)
        resize_ratio: Size scaling ratio (0.1-1.0)
        dry_run: Whether to preview only without execution
    """
    if not os.path.exists(folder_path):
        print(f"Error: Folder does not exist {folder_path}")
        return False
    
    # Supported image formats
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
    
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    image_files = [f for f in files if os.path.splitext(f)[1].lower() in image_extensions]
    
    if not image_files:
        print("Warning: No image files found in the folder")
        return True
    
    print(f"Found {len(image_files)} image files, preparing to compress...")
    
    compressed_count = 0
    for filename in image_files:
        old_path = os.path.join(folder_path, filename)
        name, ext = os.path.splitext(filename)
        
        # Create backup filename
        backup_name = f"{name}_backup{ext}"
        backup_path = os.path.join(folder_path, backup_name)
        
        try:
            # Open image
            with Image.open(old_path) as img:
                # Record original info
                original_size = os.path.getsize(old_path)
                original_width, original_height = img.size
                
                # Adjust size
                if resize_ratio < 1.0:
                    new_width = int(original_width * resize_ratio)
                    new_height = int(original_height * resize_ratio)
                    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Save compressed image
                if dry_run:
                    print(f"Preview: {filename} ({original_width}x{original_height}) → Quality{quality}%, Size{resize_ratio*100}%")
                else:
                    # Save as JPEG (keep original format)
                    if ext.lower() in ['.jpg', '.jpeg']:
                        img.save(old_path, 'JPEG', quality=quality, optimize=True, progressive=True)
                    else:
                        img.save(old_path, 'PNG', optimize=True, compress_level=6)
                    
                    # Calculate compression effect
                    new_size = os.path.getsize(old_path)
                    compression_rate = (original_size - new_size) / original_size * 100
                    
                    print(f"Compressed: {filename} ({original_size/1024:.1f}KB → {new_size/1024:.1f}KB, {compression_rate:.1f}%)")
                    compressed_count += 1
                    
        except Exception as e:
            print(f"Compression failed {filename}: {e}")
    
    print(f"Complete! Total {compressed_count} image files compressed")
    return True

def main():
    parser = argparse.ArgumentParser(description='Batch Image Compression Tool')
    parser.add_argument('folder', help='Folder path to process')
    parser.add_argument('--quality', type=int, default=70, choices=range(1, 101),
                        help='Compression quality (1-100)')
    parser.add_argument('--resize', type=float, default=1.0, choices=[round(x*0.1,1) for x in range(1, 11)],
                        help='Size scaling ratio (0.1-1.0)')
    parser.add_argument('--dry-run', action='store_true', help='Preview only without execution')
    
    args = parser.parse_args()
    
    compress_images(
        folder_path=args.folder,
        quality=args.quality,
        resize_ratio=args.resize,
        dry_run=args.dry_run
    )

if __name__ == "__main__":
    main()