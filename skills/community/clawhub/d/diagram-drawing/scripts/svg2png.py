#!/usr/bin/env python3
"""
SVG to PNG converter with multiple backend support.
Tries: rsvg-convert (CLI) → cairosvg (Python) → reports error.

Usage:
    python3 svg2png.py input.svg [output.png] [width]

Examples:
    python3 svg2png.py diagram.svg              # output.png in same dir
    python3 svg2png.py diagram.svg out.png      # custom output
    python3 svg2png.py diagram.svg out.png 1920 # 1920px width
"""

import sys
import os
import subprocess
import shutil

def try_rsvg_convert(svg_path, output_path, width=None):
    """Try rsvg-convert CLI tool."""
    if shutil.which("rsvg-convert") is None:
        return False
    
    cmd = ["rsvg-convert", "-o", output_path, svg_path]
    if width:
        cmd.insert(1, "-w")
        cmd.insert(2, str(width))
    
    try:
        result = subprocess.run(cmd, capture_output=True, timeout=30)
        return result.returncode == 0
    except (subprocess.TimeoutExpired, Exception):
        return False

def try_cairosvg(svg_path, output_path, width=None):
    """Try cairosvg Python library."""
    try:
        import cairosvg
        
        width_int = width or 1920
        cairosvg.svg2png(url=svg_path, write_to=output_path, output_width=width_int)
        return True
    except ImportError:
        return False
    except Exception:
        return False

def try_pillow_with_svglib(svg_path, output_path, width=None):
    """Try svglib + Pillow (pure Python, no external deps)."""
    try:
        from svglib.svglib import svg2rlg
        from reportlab.graphics import renderPM
        
        width_int = width or 1920
        drawing = svg2rlg(svg_path)
        if drawing is None:
            return False
        
        # Scale to target width
        scale = width_int / drawing.width
        drawing.width = width_int
        drawing.height = drawing.height * scale
        drawing.scale(scale, scale)
        
        renderPM.drawToFile(drawing, output_path, fmt="PNG")
        return True
    except ImportError:
        return False
    except Exception:
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: svg2png.py <input.svg> [output.png] [width]")
        sys.exit(1)
    
    svg_path = os.path.abspath(sys.argv[1])
    
    if len(sys.argv) >= 3:
        output_path = os.path.abspath(sys.argv[2])
    else:
        base = os.path.splitext(svg_path)[0]
        output_path = base + ".png"
    
    width = int(sys.argv[3]) if len(sys.argv) >= 4 else 1920
    
    if not os.path.exists(svg_path):
        print(f"Error: File not found: {svg_path}")
        sys.exit(1)
    
    print(f"Converting: {svg_path}")
    print(f"Output: {output_path}")
    print(f"Width: {width}px")
    
    # Try backends in order of preference
    if try_rsvg_convert(svg_path, output_path, width):
        print("✓ Converted using rsvg-convert")
        sys.exit(0)
    
    if try_cairosvg(svg_path, output_path, width):
        print("✓ Converted using cairosvg")
        sys.exit(0)
    
    if try_pillow_with_svglib(svg_path, output_path, width):
        print("✓ Converted using svglib+Pillow")
        sys.exit(0)
    
    # All backends failed
    print("""
Error: No SVG-to-PNG converter available.

Install one of:
  1. rsvg-convert (recommended):
     macOS:    brew install librsvg
     Ubuntu:   sudo apt install librsvg2-bin
     
  2. cairosvg (Python):
     pip install cairosvg
     
  3. svglib+Pillow (pure Python):
     pip install svglib reportlab Pillow
""", file=sys.stderr)
    sys.exit(1)

if __name__ == "__main__":
    main()
