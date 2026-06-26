#!/usr/bin/env python3
"""
Image Format Converter
Converts images between PNG, JPG/JPEG, WebP, BMP, GIF, and TIFF formats.

Dependencies:
    pip install Pillow

Usage:
    python image_converter.py <input_image> --format <target_format> [options]
    python image_converter.py --batch <input_dir> --format <target_format> [options]
"""

import argparse
import os
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Error: Pillow is required. Install with: pip install Pillow")
    sys.exit(1)


# Supported format mapping (extension -> PIL format)
FORMAT_MAP = {
    "png": "PNG",
    "jpg": "JPEG",
    "jpeg": "JPEG",
    "webp": "WebP",
    "bmp": "BMP",
    "gif": "GIF",
    "tiff": "TIFF",
    "tif": "TIFF",
}


def get_format_info(target_format: str) -> tuple[str, str]:
    """Validate and return normalized format info."""
    fmt_lower = target_format.lower().lstrip(".")
    
    if fmt_lower not in FORMAT_MAP:
        available = ", ".join(sorted(FORMAT_MAP.keys()))
        raise ValueError(f"Unsupported format: {target_format}. Available: {available}")
    
    return fmt_lower, FORMAT_MAP[fmt_lower]


def convert_single_image(
    input_path: str, 
    target_format: str,
    output_path: str = None,
    quality: int = 95,
    resize: tuple = None,
    optimize: bool = True
) -> str:
    """Convert a single image to the target format."""
    
    ext_lower, pil_format = get_format_info(target_format)
    
    input_file = Path(input_path)
    
    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    # Determine output path
    if output_path is None:
        output_path = input_file.with_suffix(f".{ext_lower}")
    else:
        output_path = Path(output_path)
    
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"Converting: {input_file.name} -> {output_path.name} ({pil_format})")
    
    try:
        # Open and process image
        img = Image.open(input_file)
        
        # Handle color modes based on target format
        if pil_format == "JPEG":
            if img.mode in ("RGBA", "LA", "PA"):
                background = Image.new("RGB", img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1])
                img = background
            elif img.mode != "RGB":
                img = img.convert("RGB")
        
        # Resize if specified
        if resize:
            width, height = resize
            img = img.resize((width, height), Image.LANCZOS)
        
        # Save with appropriate options
        save_kwargs = {}
        
        if pil_format == "JPEG":
            save_kwargs["quality"] = quality
            save_kwargs["optimize"] = optimize
        elif pil_format == "PNG":
            save_kwargs["optimize"] = optimize
        elif pil_format == "WebP":
            save_kwargs["quality"] = quality
        
        img.save(str(output_path), pil_format, **save_kwargs)
        
        # Report file sizes
        input_size = input_file.stat().st_size
        output_size = output_path.stat().st_size
        ratio = (output_size / input_size * 100) if input_size > 0 else 0
        
        print(f"✓ Converted successfully ({input_size/1024:.1f}KB -> {output_size/1024:.1f}KB, {ratio:.1f}% of original)")
        return str(output_path)
        
    except Exception as e:
        print(f"✗ Error converting {input_file.name}: {e}")
        raise


def batch_convert_images(
    input_dir: str, 
    target_format: str, 
    output_dir: str = None,
    **kwargs
) -> list[str]:
    """Convert all images in a directory."""
    
    input_path = Path(input_dir)
    
    if not input_path.is_dir():
        raise NotADirectoryError(f"Input directory not found: {input_dir}")
    
    if output_dir is None:
        output_dir = input_dir
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Find all supported images
    image_extensions = set(FORMAT_MAP.keys())
    image_files = []
    for ext in image_extensions:
        image_files.extend(input_path.glob(f"*.{ext}"))
        image_files.extend(input_path.glob(f"*.{ext.upper()}"))
    
    # Deduplicate and sort
    seen = set()
    unique_files = []
    for f in sorted(image_files):
        f_lower = f.lower()
        if f_lower not in seen:
            seen.add(f_lower)
            unique_files.append(f)
    
    if not unique_files:
        print(f"No image files found in: {input_dir}")
        return []
    
    print(f"Found {len(unique_files)} image file(s)")
    
    results = []
    errors = []
    
    for img_file in unique_files:
        ext_lower, _ = get_format_info(target_format)
        out_file = output_path / f"{img_file.stem}.{ext_lower}"
        try:
            result = convert_single_image(
                str(img_file), 
                target_format, 
                str(out_file),
                **kwargs
            )
            results.append(result)
        except Exception as e:
            errors.append(f"{img_file.name}: {e}")
            continue
    
    summary = f"\nConverted {len(results)}/{len(unique_files)} files successfully"
    if errors:
        summary += f"\nErrors ({len(errors)}):"
        for err in errors[:5]:
            summary += f"\n  - {err}"
        if len(errors) > 5:
            summary += f"\n  ... and {len(errors)-5} more"
    print(summary)
    
    return results


def get_image_info(image_path: str) -> dict:
    """Get detailed information about an image file."""
    img_file = Path(image_path)
    
    if not img_file.exists():
        raise FileNotFoundError(f"File not found: {image_path}")
    
    try:
        img = Image.open(img_file)
        info = {
            "file": img_file.name,
            "format": img.format,
            "mode": img.mode,
            "size": img.size,
            "width": img.width,
            "height": img.height,
            "file_size_bytes": img_file.stat().st_size,
            "file_size_kb": round(img_file.stat().st_size / 1024, 2),
            "has_transparency": img.mode in ("RGBA", "LA", "PA") or "transparency" in img.info,
        }
        return info
    except Exception as e:
        return {"error": str(e)}


def main():
    parser = argparse.ArgumentParser(
        description="Convert images between different formats (PNG, JPG, WebP, BMP, GIF, TIFF)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Supported Formats:
  png, jpg/jpeg, webp, bmp, gif, tiff/tif

Examples:
  python image_converter.py photo.png --format jpg
  python image_converter.py photo.png --format webp --quality 80
  python image_converter.py photo.png --format jpg --resize 1920 1080
  python image_converter.py --batch ./images --format webp --output-dir ./webp_images
  python image_converter.py photo.png --info
        """
    )
    
    parser.add_argument("input", help="Input image or directory (with --batch)")
    parser.add_argument("--format", "-f", dest="target_format", help="Target format (png/jpg/webp/bmp/gif/tiff)")
    parser.add_argument("--output", "-o", help="Output file/directory path")
    parser.add_argument("--batch", "-b", action="store_true", help="Batch mode: convert all images in directory")
    parser.add_argument("--output-dir", help="Output directory for batch mode")
    parser.add_argument("--quality", "-q", type=int, default=95, help="Quality for lossy formats (1-100, default: 95)")
    parser.add_argument("--resize", nargs=2, type=int, metavar=("WIDTH", "HEIGHT"), help="Resize to WIDTH x HEIGHT pixels")
    parser.add_argument("--info", "-i", action="store_true", help="Show image information instead of converting")
    parser.add_argument("--no-optimize", action="store_true", dest="no_optimize", help="Disable optimization")
    
    args = parser.parse_args()
    
    try:
        if args.info:
            info = get_image_info(args.input)
            for k, v in info.items():
                print(f"  {k}: {v}")
            return
        
        if not args.target_format:
            parser.error("Target format is required (--format). Use --info to view image info.")
        
        kwargs = {
            "quality": args.quality,
            "resize": tuple(args.resize) if args.resize else None,
            "optimize": not args.no_optimize,
        }
        
        if args.batch:
            batch_convert_images(args.input, args.target_format, args.output_dir or args.output, **kwargs)
        else:
            convert_single_image(args.input, args.target_format, args.output, **kwargs)
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
