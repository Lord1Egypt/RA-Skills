#!/usr/bin/env python3
"""
Web Image Optimizer v2 - Visually lossless compression for web.
Uses binary search on quality to find the best quality that fits target size.
Output quality is always visually acceptable (no perceptible quality loss).
"""

import sys
import os
import argparse
from pathlib import Path
from PIL import Image
from io import BytesIO
import math


# Minimum acceptable quality for visually lossless results
# Below these thresholds, quality loss becomes perceptible
MIN_VISUAL_QUALITY = {
    "JPEG": 75,   # JPEG below 75 shows visible artifacts
    "WEBP": 70,   # WebP is more efficient, can go slightly lower
    "PNG": None,  # PNG is lossless, no quality parameter
}


def get_image_info(filepath):
    """Get image file info."""
    size_bytes = os.path.getsize(filepath)
    size_kb = size_bytes / 1024
    try:
        with Image.open(filepath) as img:
            width, height = img.size
            fmt = img.format or "UNKNOWN"
            mode = img.mode
        return {
            "path": filepath,
            "width": width,
            "height": height,
            "format": fmt,
            "mode": mode,
            "size_bytes": size_bytes,
            "size_kb": round(size_kb, 1),
        }
    except Exception as e:
        return {"path": filepath, "error": str(e)}


def prepare_image(img, target_format):
    """Prepare image for target format (handle alpha, color mode)."""
    if target_format == "JPEG":
        # JPEG doesn't support alpha
        if img.mode in ("RGBA", "LA", "P"):
            bg = Image.new("RGB", img.size, (255, 255, 255))
            if img.mode == "P":
                img = img.convert("RGBA")
            if img.mode in ("RGBA", "LA"):
                bg.paste(img, mask=img.split()[-1])
                img = bg
            else:
                img = img.convert("RGB")
        elif img.mode != "RGB":
            img = img.convert("RGB")
    elif target_format == "WEBP":
        # WebP supports alpha
        if img.mode in ("P",):
            img = img.convert("RGBA")
        elif img.mode not in ("RGB", "RGBA"):
            img = img.convert("RGB")
    elif target_format == "PNG":
        if img.mode not in ("RGB", "RGBA", "L", "LA"):
            img = img.convert("RGBA")
    
    return img


def encode_image(img, fmt, quality):
    """Encode image to bytes buffer with given format and quality."""
    buf = BytesIO()
    params = {}
    
    if fmt == "JPEG":
        params["quality"] = quality
        params["optimize"] = True
        params["progressive"] = True
        params["subsampling"] = "4:2:0"  # Chroma subsampling for better compression
    elif fmt == "WEBP":
        params["quality"] = quality
        params["method"] = 6  # Best compression method
    elif fmt == "PNG":
        params["optimize"] = True
    
    img.save(buf, format=fmt, **params)
    return buf


def binary_search_quality(img, fmt, target_bytes, lo=None, hi=95):
    """
    Binary search for the best quality that fits target size.
    Never goes below minimum visual quality threshold.
    
    Returns (quality, actual_bytes) tuple.
    """
    min_q = lo or MIN_VISUAL_QUALITY.get(fmt, 70)
    
    # First, check if max quality already fits
    buf = encode_image(img, fmt, hi)
    if buf.tell() <= target_bytes:
        return hi, buf.tell()
    
    # Binary search between min_q and hi
    best_quality = min_q
    best_size = float("inf")
    
    while hi - min_q > 2:
        mid = (min_q + hi) // 2
        buf = encode_image(img, fmt, mid)
        size = buf.tell()
        
        if size <= target_bytes:
            # This quality fits, try higher
            best_quality = mid
            best_size = size
            min_q = mid
        else:
            # Too big, try lower
            hi = mid
    
    # Return the best quality that fits
    # If no quality fits, return the minimum acceptable quality
    buf = encode_image(img, fmt, min_q)
    
    # Check if the lower bound fits
    buf_lo = encode_image(img, fmt, min_q)
    buf_hi = encode_image(img, fmt, hi)
    
    if buf_lo.tell() <= target_bytes:
        return min_q, buf_lo.tell()
    elif buf_hi.tell() <= target_bytes:
        return hi, buf_hi.tell()
    else:
        # Even minimum quality is too large - need to resize
        return None, buf_lo.tell()


def compress_single(input_path, output_path=None, max_kb=500, output_format="auto", quality=85):
    """
    Compress a single image with visually lossless quality.
    
    Strategy:
    1. Format conversion (PNG -> WebP for massive savings)
    2. Binary search for best quality within target size
    3. If quality alone can't meet target, resize proportionally
    4. Never drop below visual quality threshold
    
    Returns dict with result info.
    """
    input_path = Path(input_path)
    
    if not input_path.exists():
        return {"error": f"File not found: {input_path}"}
    
    # Determine output format
    if output_format == "auto":
        # Prefer WebP for best compression
        suffix = ".webp"
        fmt = "WEBP"
    elif output_format == "jpeg":
        suffix = ".jpeg"
        fmt = "JPEG"
    elif output_format == "png":
        suffix = ".png"
        fmt = "PNG"
    else:
        suffix = ".webp"
        fmt = "WEBP"
    
    if output_path is None:
        output_path = input_path.parent / f"{input_path.stem}_web{suffix}"
    else:
        output_path = Path(output_path)
    
    max_bytes = max_kb * 1024
    input_size = os.path.getsize(input_path)
    
    try:
        with Image.open(input_path) as img:
            original_width, original_height = img.size
            
            # Prepare image format
            img = prepare_image(img, fmt)
            
            # For PNG format with no quality control, try WebP first
            if fmt == "PNG":
                buf_webp = encode_image(img, "WEBP", quality)
                if buf_webp.tell() <= max_bytes:
                    # WebP is smaller and visually lossless at same quality
                    output_path = Path(str(output_path).replace(".png", ".webp"))
                    with open(output_path, "wb") as f:
                        f.write(buf_webp.getvalue())
                    output_size = os.path.getsize(output_path)
                    return {
                        "success": True,
                        "input": str(input_path),
                        "output": str(output_path),
                        "input_size_kb": round(input_size / 1024, 1),
                        "output_size_kb": round(output_size / 1024, 1),
                        "savings_percent": round((1 - output_size / input_size) * 100, 1),
                        "format": "WEBP",
                        "quality": quality,
                        "dimensions": f"{original_width}x{original_height}",
                        "resized": False,
                        "note": "PNG requested but WebP is visually lossless and much smaller",
                    }
            
            # Binary search for best quality within target
            best_quality, actual_size = binary_search_quality(img, fmt, max_bytes, hi=quality)
            
            if best_quality is not None:
                # Quality adjustment alone works
                buf = encode_image(img, fmt, best_quality)
                with open(output_path, "wb") as f:
                    f.write(buf.getvalue())
                
                output_size = os.path.getsize(output_path)
                savings = (1 - output_size / input_size) * 100
                
                return {
                    "success": True,
                    "input": str(input_path),
                    "output": str(output_path),
                    "input_size_kb": round(input_size / 1024, 1),
                    "output_size_kb": round(output_size / 1024, 1),
                    "savings_percent": round(savings, 1),
                    "format": fmt,
                    "quality": best_quality,
                    "dimensions": f"{original_width}x{original_height}",
                    "resized": False,
                }
            
            # Need to resize - calculate scale factor
            # Even at minimum visual quality, file is too large
            scale = math.sqrt(max_bytes / actual_size)
            scale = min(scale, 1.0)  # Never upscale
            new_width = max(100, int(original_width * scale))
            new_height = max(100, int(original_height * scale))
            
            img_resized = img.resize((new_width, new_height), Image.LANCZOS)
            
            # Binary search again on resized image
            best_quality, _ = binary_search_quality(img_resized, fmt, max_bytes, hi=quality)
            
            if best_quality is None:
                best_quality = MIN_VISUAL_QUALITY.get(fmt, 70)
            
            buf = encode_image(img_resized, fmt, best_quality)
            with open(output_path, "wb") as f:
                f.write(buf.getvalue())
            
            output_size = os.path.getsize(output_path)
            savings = (1 - output_size / input_size) * 100
            
            return {
                "success": True,
                "input": str(input_path),
                "output": str(output_path),
                "input_size_kb": round(input_size / 1024, 1),
                "output_size_kb": round(output_size / 1024, 1),
                "savings_percent": round(savings, 1),
                "format": fmt,
                "quality": best_quality,
                "dimensions": f"{new_width}x{new_height}",
                "original_dimensions": f"{original_width}x{original_height}",
                "resized": True,
            }
    
    except Exception as e:
        return {"error": str(e), "input": str(input_path)}


def batch_compress(directory, max_kb=500, output_format="auto", quality=85, recursive=False):
    """Batch compress all images in a directory."""
    directory = Path(directory)
    if not directory.is_dir():
        return [{"error": f"Not a directory: {directory}"}]
    
    supported_ext = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff", ".gif"}
    
    if recursive:
        files = [f for f in directory.rglob("*") if f.suffix.lower() in supported_ext]
    else:
        files = [f for f in directory.iterdir() if f.suffix.lower() in supported_ext]
    
    if not files:
        return [{"info": f"No images found in {directory}"}]
    
    results = []
    total_input = 0
    total_output = 0
    success_count = 0
    
    for f in sorted(files):
        result = compress_single(f, max_kb=max_kb, output_format=output_format, quality=quality)
        results.append(result)
        if result.get("success"):
            success_count += 1
            total_input += result.get("input_size_kb", 0)
            total_output += result["output_size_kb"]
    
    if success_count > 0:
        results.append({
            "summary": True,
            "total_files": success_count,
            "total_input_kb": round(total_input, 1),
            "total_output_kb": round(total_output, 1),
            "total_savings_kb": round(total_input - total_output, 1),
            "total_savings_percent": round((1 - total_output / total_input) * 100, 1),
        })
    
    return results


def main():
    parser = argparse.ArgumentParser(
        description="Web Image Optimizer v2 - Visually lossless compression for web",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Compress single image (auto WebP, under 500KB, visually lossless)
  python web_image_optimizer.py compress photo.jpg
  
  # Compress to JPEG, max 300KB
  python web_image_optimizer.py compress photo.jpg --format jpeg --max-kb 300
  
  # Batch compress directory
  python web_image_optimizer.py batch ./images/
  
  # Batch with recursive scan
  python web_image_optimizer.py batch ./photos/ --recursive
  
  # Check image info
  python web_image_optimizer.py info photo.jpg

Compression Strategy:
  1. Convert PNG to WebP (70-90% smaller, visually identical)
  2. Binary search best quality within target size
  3. Quality never drops below visual threshold (JPEG:75, WebP:70)
  4. If still too large, proportionally resize then re-optimize
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Compress
    cp = subparsers.add_parser("compress", help="Compress single image for web")
    cp.add_argument("input", help="Input image path")
    cp.add_argument("-o", "--output", help="Output path (default: input_web.webp)")
    cp.add_argument("-m", "--max-kb", type=int, default=500, help="Max output size KB (default: 500)")
    cp.add_argument("-f", "--format", choices=["auto", "webp", "jpeg", "png"], default="auto")
    cp.add_argument("-q", "--quality", type=int, default=90, help="Max quality ceiling 1-100 (default: 90)")
    
    # Batch
    bp = subparsers.add_parser("batch", help="Batch compress images in directory")
    bp.add_argument("directory", help="Directory containing images")
    bp.add_argument("-m", "--max-kb", type=int, default=500)
    bp.add_argument("-f", "--format", choices=["auto", "webp", "jpeg", "png"], default="auto")
    bp.add_argument("-q", "--quality", type=int, default=90)
    bp.add_argument("-r", "--recursive", action="store_true")
    
    # Info
    ip = subparsers.add_parser("info", help="Show image information")
    ip.add_argument("input", help="Image file path")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    if args.command == "compress":
        result = compress_single(args.input, output_path=args.output, max_kb=args.max_kb, output_format=args.format, quality=args.quality)
        print_result(result)
    elif args.command == "batch":
        results = batch_compress(args.directory, max_kb=args.max_kb, output_format=args.format, quality=args.quality, recursive=args.recursive)
        for r in results:
            print_result(r)
    elif args.command == "info":
        result = get_image_info(args.input)
        print_result(result)


def print_result(result):
    """Print result in clean format."""
    if "error" in result:
        print(f"  ERROR: {result['error']}")
    elif "info" in result:
        print(f"  INFO: {result['info']}")
    elif result.get("summary"):
        print(f"\n  {'='*50}")
        print(f"  BATCH SUMMARY")
        print(f"  {'='*50}")
        print(f"  Files processed: {result['total_files']}")
        print(f"  Total input:     {result['total_input_kb']:>8.1f} KB")
        print(f"  Total output:    {result['total_output_kb']:>8.1f} KB")
        print(f"  Total saved:     {result['total_savings_kb']:>8.1f} KB ({result['total_savings_percent']}%)")
        print(f"  {'='*50}")
    elif result.get("success"):
        status = "OK" if result['output_size_kb'] <= 500 else "WARN"
        print(f"  [{status}] {Path(result['input']).name}")
        print(f"    {result['input_size_kb']:>8.1f} KB --> {result['output_size_kb']:>8.1f} KB  ({result['savings_percent']:+.1f}%)")
        print(f"    Format: {result['format']}  Quality: {result['quality']}  Size: {result['dimensions']}")
        if result.get('resized'):
            orig = result.get('original_dimensions', '?')
            print(f"    Resized: {orig} -> {result['dimensions']}")
        if result.get('note'):
            print(f"    Note: {result['note']}")
        print(f"    Output: {result['output']}")


if __name__ == "__main__":
    main()
