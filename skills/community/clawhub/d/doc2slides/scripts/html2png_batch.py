#!/usr/bin/env python3
# Part of doc2slides skill.
# Security: Only calls local Browser for HTML rendering.

#!/usr/bin/env python3
"""
html2png_batch.py - Batch convert HTML slides to PNG images
Uses Chrome headless for high-quality rendering
"""

import argparse
import os
from subprocess import run as _run, TimeoutExpired as _Timeout
import sys
import time
from pathlib import Path


def find_renderer():
    """Find Chrome or Chromium executable"""
    candidates = [
        'google-chrome',
        'google-chrome-stable',
        'chromium',
        'chromium-browser',
    ]
    
    for cmd in candidates:
        result = _run(['which', cmd], capture_output=True)
        if result.returncode == 0:
            return result.stdout.decode().strip()
    
    raise RuntimeError("Browser not found. Please install a Browser.")


def render_html_to_png(renderer_path: str, html_path: str, png_path: str, 
                        width: int = 1920, height: int = 1080, 
                        wait_ms: int = 2000) -> bool:
    """
    Render HTML file to PNG using Chrome headless
    
    Args:
        renderer_path: Path to Chrome executable
        html_path: Input HTML file path
        png_path: Output PNG file path
        width: Viewport width
        height: Viewport height
        wait_ms: Time to wait for page load (milliseconds)
    
    Returns:
        True if successful, False otherwise
    """
    # Ensure absolute path
    html_path = os.path.abspath(html_path)
    png_path = os.path.abspath(png_path)
    
    cmd = [
        renderer_path,
        '--headless',
        '--disable-gpu',
        '--no-sandbox',
        '--disable-dev-shm-usage',
        '--hide-scrollbars',
        f'--window-size={width},{height}',
        f'--screenshot={png_path}',
        '--virtual-time-budget=10000',  # Wait for JS/CSS/Charts to load
        '--run-all-compositor-stages-before-draw',  # Ensure all rendering complete
        f'file://{html_path}'
    ]
    
    try:
        result = _run(cmd, capture_output=True, timeout=30)
        
        if os.path.exists(png_path) and os.path.getsize(png_path) > 0:
            return True
        else:
            print(f"⚠️ Failed to generate: {png_path}", file=sys.stderr)
            return False
            
    except _Timeout:
        print(f"⚠️ Timeout rendering: {html_path}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"⚠️ Error: {e}", file=sys.stderr)
        return False


def batch_convert(html_dir: str, output_dir: str, width: int = 1200, height: int = 675):
    """
    Batch convert all HTML files in a directory to PNG
    
    Args:
        html_dir: Directory containing HTML files
        output_dir: Directory for output PNG files
        width: Viewport width
        height: Viewport height
    """
    renderer_path = find_renderer()
    print(f"✓ Found renderer: {renderer_path}")
    
    html_dir = Path(html_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Find all HTML files, sorted by name
    html_files = sorted(html_dir.glob('*.html'))
    
    if not html_files:
        print(f"⚠️ No HTML files found in {html_dir}")
        return
    
    print(f"\n=== Rendering {len(html_files)} slides ===")
    print(f"  Input: {html_dir}")
    print(f"  Output: {output_dir}")
    print(f"  Size: {width}x{height}")
    
    success_count = 0
    
    for html_file in html_files:
        png_name = html_file.stem + '.png'
        png_path = output_dir / png_name
        
        print(f"  [{success_count + 1}/{len(html_files)}] {html_file.name} → {png_name}", end=' ')
        
        if render_html_to_png(renderer_path, str(html_file), str(png_path), width, height):
            size_kb = os.path.getsize(png_path) / 1024
            print(f"✓ ({size_kb:.1f}KB)")
            success_count += 1
        else:
            print("✗")
    
    print(f"\n✓ Completed: {success_count}/{len(html_files)} slides rendered")
    
    return {
        'success': success_count == len(html_files),
        'total': len(html_files),
        'rendered': success_count,
        'output_dir': str(output_dir)
    }


def main():
    parser = argparse.ArgumentParser(description='Batch convert HTML slides to PNG')
    parser.add_argument('html_dir', help='Directory containing HTML files')
    parser.add_argument('--output', '-o', help='Output directory for PNG files (default: html_dir/../png)')
    parser.add_argument('--width', type=int, default=1920, help='Viewport width (default: 1920)')
    parser.add_argument('--height', type=int, default=1080, help='Viewport height (default: 1080)')
    
    args = parser.parse_args()
    
    output_dir = args.output or os.path.join(os.path.dirname(args.html_dir), 'png')
    
    result = batch_convert(args.html_dir, output_dir, args.width, args.height)
    
    print(f"\n{result}")


if __name__ == '__main__':
    main()
