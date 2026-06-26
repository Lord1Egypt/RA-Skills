#!/usr/bin/env python3
"""Convert the generated SVG report to PNG.
Attempts to use cairosvg if installed, otherwise falls back to the system tool `rsvg-convert`.
The output file is placed alongside the SVG with the same base name and .png extension.
"""
import sys, pathlib, subprocess

def convert_with_cairosvg(svg_path, png_path):
    try:
        import cairosvg
    except ImportError:
        return False
    try:
        cairosvg.svg2png(url=str(svg_path), write_to=str(png_path))
        return True
    except Exception as e:
        sys.stderr.write(f"cairosvg conversion failed: {e}\n")
        return False

def convert_with_rsvg(svg_path, png_path):
    # rsvg-convert is part of librsvg (common on Linux)
    cmd = ["rsvg-convert", "-o", str(png_path), str(svg_path)]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        return True
    except Exception as e:
        sys.stderr.write(f"rsvg-convert failed: {e}\n")
        return False

def main():
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: svg_to_png.py <report.svg>\n")
        sys.exit(1)
    svg_path = pathlib.Path(sys.argv[1])
    if not svg_path.is_file():
        sys.stderr.write(f"SVG file not found: {svg_path}\n")
        sys.exit(1)
    png_path = svg_path.with_suffix('.png')
    if convert_with_cairosvg(svg_path, png_path):
        print(f"Converted {svg_path} -> {png_path} using cairosvg")
        sys.exit(0)
    if convert_with_rsvg(svg_path, png_path):
        print(f"Converted {svg_path} -> {png_path} using rsvg-convert")
        sys.exit(0)
    sys.stderr.write("Failed to convert SVG to PNG – install cairosvg (`pip install cairosvg`) or librsvg (`apt install librsvg2-bin`).\n")
    sys.exit(1)

if __name__ == '__main__':
    main()
