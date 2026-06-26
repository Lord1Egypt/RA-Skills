#!/usr/bin/env python3
"""
Dataset Splitter
Split image datasets into train/val/test sets
"""

import argparse
import json
import os
import random
import shutil
import sys
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple


def get_image_files(directory: str, extensions: List[str]) -> List[str]:
    """Get all image files from directory"""
    directory = Path(directory)
    image_files = []
    
    for ext in extensions:
        image_files.extend(directory.glob(f"*.{ext}"))
        image_files.extend(directory.glob(f"*.{ext.upper()}"))
    
    return [str(f) for f in image_files if f.is_file()]


def get_class_distribution(annotations_dir: str, image_files: List[str]) -> Dict[str, int]:
    """Get class distribution from annotations"""
    annotations_dir = Path(annotations_dir)
    class_counts = defaultdict(int)
    
    for img_path in image_files:
        img_name = Path(img_path).stem
        ann_path = annotations_dir / f"{img_name}.txt"
        
        if ann_path.exists():
            with open(ann_path, 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    if parts:
                        class_id = int(parts[0])
                        class_counts[class_id] += 1
    
    return class_counts


def stratified_split(image_files: List[str], ratios: List[float], 
                   annotations_dir: str = None, seed: int = 42) -> Tuple[List, List, List]:
    """Split dataset while maintaining class distribution"""
    random.seed(seed)
    
    # Group by primary class
    class_groups = defaultdict(list)
    
    for img_path in image_files:
        img_name = Path(img_path).stem
        class_id = 0
        
        if annotations_dir:
            ann_path = Path(annotations_dir) / f"{img_name}.txt"
            if ann_path.exists():
                with open(ann_path, 'r') as f:
                    first_line = f.readline()
                    if first_line:
                        parts = first_line.strip().split()
                        if parts:
                            class_id = int(parts[0])
        
        class_groups[class_id].append(img_path)
    
    # Split each class group
    train, val, test = [], [], []
    
    for class_id, files in class_groups.items():
        random.shuffle(files)
        n = len(files)
        n_train = int(n * ratios[0] / 100)
        n_val = int(n * ratios[1] / 100)
        
        train.extend(files[:n_train])
        val.extend(files[n_train:n_train + n_val])
        test.extend(files[n_train + n_val:])
    
    random.shuffle(train)
    random.shuffle(val)
    random.shuffle(test)
    
    return train, val, test


def simple_split(image_files: List[str], ratios: List[float], seed: int = 42) -> Tuple[List, List, List]:
    """Simple random split"""
    random.seed(seed)
    shuffled = image_files.copy()
    random.shuffle(shuffled)
    
    n = len(shuffled)
    n_train = int(n * ratios[0] / 100)
    n_val = int(n * ratios[1] / 100)
    
    train = shuffled[:n_train]
    val = shuffled[n_train:n_train + n_val]
    test = shuffled[n_train + n_val:]
    
    return train, val, test


def cmd_split(args):
    """Split dataset"""
    # Get image files
    extensions = args.extensions.split(',')
    image_files = get_image_files(args.directory, extensions)
    
    if not image_files:
        print("No image files found")
        return
    
    print(f"Found {len(image_files)} images")
    
    # Split
    if args.stratify and args.annotations:
        print("Using stratified split...")
        train, val, test = stratified_split(
            image_files, args.ratios, args.annotations, args.seed
        )
    else:
        print("Using random split...")
        train, val, test = simple_split(image_files, args.ratios, args.seed)
    
    # Print summary
    print(f"\nSplit results:")
    print(f"  Train: {len(train)} ({args.ratios[0]}%)")
    print(f"  Val:   {len(val)} ({args.ratios[1]}%)")
    print(f"  Test:  {len(test)} ({args.ratios[2]}%)")
    
    # Create output directories
    output_dir = args.output or args.directory + "_split"
    train_dir = os.path.join(output_dir, "train")
    val_dir = os.path.join(output_dir, "val")
    test_dir = os.path.join(output_dir, "test")
    
    os.makedirs(output_dir, exist_ok=True)
    
    # YOLO format
    if args.yolo:
        train_dir = os.path.join(train_dir, "images")
        val_dir = os.path.join(val_dir, "images")
        test_dir = os.path.join(test_dir, "images")
    
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(val_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)
    
    # Copy/move files
    def process_files(files, dest_dir, src_ann_dir=None, dest_ann_dir=None):
        count = 0
        for img_path in files:
            img_name = Path(img_path).name
            
            if args.copy:
                dest_path = os.path.join(dest_dir, img_name)
                shutil.copy2(img_path, dest_path)
            else:
                dest_path = os.path.join(dest_dir, img_name)
                shutil.move(img_path, dest_path)
            
            # Process annotations
            if args.annotations and src_ann_dir and dest_ann_dir:
                ann_name = Path(img_path).stem + ".txt"
                src_ann = Path(src_ann_dir) / ann_name
                if src_ann.exists():
                    dest_ann = Path(dest_ann_dir) / ann_name
                    if args.copy:
                        shutil.copy2(src_ann, dest_ann)
                    else:
                        shutil.move(src_ann, dest_ann)
            
            count += 1
        
        return count
    
    # Get annotations directories
    ann_dir = args.annotations
    train_ann = os.path.join(output_dir, "train", "labels") if args.yolo and ann_dir else None
    val_ann = os.path.join(output_dir, "val", "labels") if args.yolo and ann_dir else None
    test_ann = os.path.join(output_dir, "test", "labels") if args.yolo and ann_dir else None
    
    if args.yolo and ann_dir:
        os.makedirs(train_ann, exist_ok=True)
        os.makedirs(val_ann, exist_ok=True)
        os.makedirs(test_ann, exist_ok=True)
    
    print(f"\nProcessing files...")
    
    n_train = process_files(train, train_dir, ann_dir, train_ann)
    print(f"✓ Train: {n_train} images")
    
    n_val = process_files(val, val_dir, ann_dir, val_ann)
    print(f"✓ Val: {n_val} images")
    
    n_test = process_files(test, test_dir, ann_dir, test_ann)
    print(f"✓ Test: {n_test} images")
    
    print(f"\nDone! Dataset saved to: {output_dir}")


def cmd_stats(args):
    """Show dataset statistics"""
    extensions = args.extensions.split(',')
    image_files = get_image_files(args.directory, extensions)
    
    print(f"Dataset: {args.directory}")
    print(f"Total images: {len(image_files)}")
    
    # Resolution distribution
    from PIL import Image
    resolutions = defaultdict(int)
    
    print("\nAnalyzing...")
    for i, img_path in enumerate(image_files):
        if i % 50 == 0:
            print(f"  {i}/{len(image_files)}...")
        try:
            with Image.open(img_path) as img:
                res = f"{img.width}x{img.height}"
                resolutions[res] += 1
        except:
            pass
    
    print("\nTop resolutions:")
    for res, count in sorted(resolutions.items(), key=lambda x: -x[1])[:10]:
        print(f"  {res}: {count}")


def main():
    parser = argparse.ArgumentParser(
        description="Dataset Splitter - Split datasets into train/val/test"
    )
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # split command
    parser_split = subparsers.add_parser("split", help="Split dataset")
    parser_split.add_argument("directory", help="Directory containing images")
    parser_split.add_argument("--ratios", "-r", nargs=3, type=int, default=[80, 10, 10],
                            help="Split ratios (train val test)")
    parser_split.add_argument("--seed", "-s", type=int, default=42,
                            help="Random seed")
    parser_split.add_argument("--annotations", "-a",
                            help="Path to annotations (will be split together)")
    parser_split.add_argument("--output", "-o",
                            help="Output directory")
    parser_split.add_argument("--yolo", action="store_true",
                            help="Output in YOLO dataset format")
    parser_split.add_argument("--stratify", action="store_true",
                            help="Maintain class distribution")
    parser_split.add_argument("--copy", action="store_true",
                            help="Copy files instead of moving")
    parser_split.add_argument("--extensions", "-e", default="jpg,jpeg,png,bmp",
                            help="Image extensions")
    parser_split.set_defaults(func=cmd_split)
    
    # stats command
    parser_stats = subparsers.add_parser("stats", help="Show dataset statistics")
    parser_stats.add_argument("directory", help="Directory containing images")
    parser_stats.add_argument("--extensions", "-e", default="jpg,jpeg,png,bmp",
                            help="Image extensions")
    parser_stats.set_defaults(func=cmd_stats)
    
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
