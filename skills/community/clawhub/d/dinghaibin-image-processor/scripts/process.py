#!/usr/bin/env python3
"""
Image Processor - Process images with resize, crop, compress, and format conversion
Note: Requires Pillow (pip install pillow). Falls back to basic operations without it.
"""

import argparse
import os
import sys
from pathlib import Path


def get_image_info(filepath):
    """Get basic image info."""
    path = Path(filepath)
    if not path.exists():
        return None
    
    size = path.stat().st_size
    return {
        'path': str(path),
        'name': path.name,
        'size': size,
        'format': path.suffix.lstrip('.').lower()
    }


def process_with_pillow(args):
    """Process image using Pillow."""
    try:
        from PIL import Image
    except ImportError:
        print("Error: Pillow not installed. Run: pip install pillow")
        print("Using fallback mode - only format conversion available.")
        return process_fallback(args)
    
    img = Image.open(args.input)
    original = img.copy()
    
    # Resize
    if args.resize:
        w, h = map(int, args.resize.split('x'))
        if w == 0:
            w = original.width * h // original.height
        if h == 0:
            h = original.height * w // original.width
        img = img.resize((w, h), Image.Resampling.LANCZOS)
    
    # Scale
    if args.scale:
        percent = int(args.scale)
        w = original.width * percent // 100
        h = original.height * percent // 100
        img = img.resize((w, h), Image.Resampling.LANCZOS)
    
    # Crop
    if args.crop:
        # Format: WxH+X+Y
        crop_str = args.crop
        if '+' in crop_str:
            dims, offset = crop_str.split('+')
            w, h = map(int, dims.split('x'))
            x, y = map(int, offset.split('y'))
            img = img.crop((x, y, x + w, y + h))
    
    # Rotate
    if args.rotate:
        img = img.rotate(int(args.rotate), expand=True)
    
    # Grayscale
    if args.grayscale:
        img = img.convert('L')
    
    # Blur
    if args.blur:
        from PIL import ImageFilter
        img = img.filter(ImageFilter.GaussianBlur(int(args.blur)))
    
    # Thumbnail
    if args.thumbnail:
        size = int(args.thumbnail.split('x')[0])
        img.thumbnail((size, size), Image.Resampling.LANCZOS)
    
    # Determine format
    output_path = args.output or args.input
    fmt = args.format or Path(output_path).suffix.lstrip('.').upper()
    if not fmt:
        fmt = 'JPEG'
    
    # Quality
    quality = args.quality or 85
    
    # Save
    if fmt.lower() in ['jpg', 'jpeg']:
        if img.mode in ('RGBA', 'LA', 'P'):
            img = img.convert('RGB')
        img.save(output_path, fmt, quality=quality)
    else:
        img.save(output_path, fmt, quality=quality)
    
    # Show result
    original_size = os.path.getsize(args.input)
    new_size = os.path.getsize(output_path)
    print(f"Processed: {args.input} -> {output_path}")
    print(f"Size: {original_size} -> {new_size} bytes ({new_size * 100 // original_size}%)")
    
    return 0


def process_fallback(args):
    """Fallback mode - basic file operations."""
    if not args.format and not args.output:
        print("Error: No operation specified. Install Pillow for full functionality.")
        return 1
    
    # Just copy with new extension
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: {args.input} not found")
        return 1
    
    output_path = Path(args.output) if args.output else input_path.with_suffix(f".{args.format}")
    
    # For now, just copy the file
    import shutil
    shutil.copy(args.input, output_path)
    print(f"Copied: {args.input} -> {output_path}")
    
    return 0


def batch_process(args):
    """Process multiple files."""
    input_path = Path(args.input)
    if not input_path.is_dir():
        return process_with_pillow(args)
    
    # Process all files in directory
    extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp']
    files = [f for f in input_path.iterdir() if f.suffix.lower() in extensions]
    
    print(f"Found {len(files)} images to process")
    
    for f in files:
        args.input = str(f)
        if args.output:
            # Replace extension
            output_name = f.stem + '.' + (args.format or f.suffix.lstrip('.'))
            args.output = str(f.parent / output_name)
        else:
            args.output = None
        process_with_pillow(args)
    
    return 0


def main():
    parser = argparse.ArgumentParser(description='Image Processor')
    parser.add_argument('input', help='Input image file or directory')
    parser.add_argument('--output', help='Output file path')
    parser.add_argument('--resize', help='Resize to WxH (0 for auto)')
    parser.add_argument('--scale', help='Scale by percentage')
    parser.add_argument('--crop', help='Crop: WxH+X+Y')
    parser.add_argument('--format', help='Output format: jpg, png, webp, gif')
    parser.add_argument('--quality', type=int, help='JPEG quality (1-100)')
    parser.add_argument('--thumbnail', help='Create thumbnail (size)')
    parser.add_argument('--grayscale', action='store_true', help='Convert to grayscale')
    parser.add_argument('--blur', help='Apply blur (radius)')
    parser.add_argument('--rotate', help='Rotate (degrees)')
    parser.add_argument('--batch', action='store_true', help='Batch process directory')
    
    args = parser.parse_args()
    
    if args.batch:
        return batch_process(args)
    
    if not os.path.exists(args.input):
        print(f"Error: {args.input} not found")
        return 1
    
    return process_with_pillow(args)


if __name__ == '__main__':
    sys.exit(main())
