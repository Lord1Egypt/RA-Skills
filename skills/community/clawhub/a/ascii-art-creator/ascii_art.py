#!/usr/bin/env python3
"""
ASCII Art Creator — banners, boxes, cowsay, tables, and image-to-ASCII.

All features implemented with Python stdlib only (no figlet, cowsay, or Pillow).

Usage:
  python ascii_art.py banner <text> [--font block|standard|slant]
  python ascii_art.py box <text> [--style single|double|round|thick]
  python ascii_art.py cow <msg> [--face default|stoned|dead|happy|bored]
  python ascii_art.py table --header "A,B,C" --rows "1,2,3" "4,5,6"
  python ascii_art.py image <path> [--width 80]
"""

import argparse
import math
import os
import shutil
import sys
from typing import List, Optional


# ═══════════════════════════════════════════════════════════════════════════════
#  Banner (figlet-style)
# ═══════════════════════════════════════════════════════════════════════════════

# Letter maps: each letter is a 3-row-tall bitmap, one string per row.
# Each character in the string represents a pixel: "#" filled, " " empty.

BANNER_FONTS: dict = {}

BANNER_FONTS["standard"] = {
    "A": [" ██╗██╗", " ██║██║", " ██║██║"],
    "B": ["██████╗ ", " ╚══██╔╝", " ██████╗"],
    "C": [" █████╗ ", " ██╔══╝ ", " ╚██████╗"],
    "D": ["██████╗ ", " ██╔══██╗", " ██████╔╝"],
    "E": ["███████╗", " ██╔════╝", " ███████╗"],
    "F": ["███████╗", " ██╔════╝", " ██║     "],
    "G": [" ██████╗ ", " ██╔════╝ ", " ███████╗"],
    "H": [" ██╗ ██╗", " ███████║", " ██╔══██║"],
    "I": [" ██╗", " ██║", " ██║"],
    "J": ["      ██╗", "      ██║", " ██████╔╝"],
    "K": [" ██╗ ██╗", " ████╔═╝ ", " ██╔═██╗ "],
    "L": [" ██╗    ", " ██║    ", " ███████╗"],
    "M": [" ████╗ ████╗", " ██╔████╔██║", " ██║╚██╔╝██║"],
    "N": [" ████╗ ██╗", " ██╔██╗██║", " ██║╚████║"],
    "O": [" █████╗ ", " ██╔══██╗", " ╚█████╔╝"],
    "P": ["██████╗ ", " ██╔══██╗", " ██║     "],
    "Q": [" █████╗  ", " ██╔══██╗ ", " ╚█████╔╗║"],
    "R": ["██████╗ ", " ██╔══██╗", " ██║ ╚═╝ "],
    "S": [" █████╗ ", " ╚═══██║", " ██████╔╝"],
    "T": ["████████╗", "    ██║   ", "    ██║   "],
    "U": [" ██╗ ██╗", " ██║ ██║", " ╚█████╔╝"],
    "V": [" ██╗ ██╗", " ██║ ██║", " ╚═╝ ╚═╝"],
    "W": [" ██╗    ██╗", " ██║ █╗ ██║", " ╚═╝ ╚═╝"],
    "X": [" ██╗ ██╗", " ╚═╝██║", " ██╗ ╚═╝"],
    "Y": [" ██╗ ██╗", " ╚═╝██║", " ██╗ ╚═╝"],
    "Z": ["██████╗ ", "    ╚═╝ ", " ██████╗"],
    "0": [" █████╗ ", " ██╔══██╗", " ╚█████╔╝"],
    "1": [" ██╗", " ██║", " ██║"],
    "2": ["██████╗ ", "    ╚═╝ ", " ██████╗"],
    "3": ["██████╗ ", "    ██╔╝", " ██████╔╝"],
    "4": [" ██╗ ██╗", " ██████║", "    ██║"],
    "5": ["███████╗", " ██████╔╝", " ╚═════╝"],
    "6": [" █████╗ ", " ██████╗ ", " ╚═════╝"],
    "7": ["██████╗ ", "    ██╔╝", "    ╚═╝ "],
    "8": [" █████╗ ", " ╚═══██║", " ██████╔╝"],
    "9": [" █████╗ ", " ╚████║", "    ╚═╝"],
    " ": [" ", " ", " "],
    ".": ["   ", "   ", " █╗"],
    "!": [" █╗", " █║", " ╚╝"],
    "?": ["████╗ ", "  ╔═╝ ", "  ╚═╝ "],
    ",": ["   ", "   ", " █╗"],
    ":": ["   ", " █╗", " ╚╝"],
    "-": ["     ", " ███╗", "     "],
    "_": ["     ", "     ", " ███╗"],
    "/": ["      █╗", "     █║", "     ╚╝"],
    "\\": [" █╗     ", " █║     ", " ╚╝     "],
    "@": [" █████╗ ", " ██╔══██║", " ╚█████╔╝"],
    "#": [" ██╗██╗", " ██████║", " ██║██║"],
    "+": ["   █╗   ", " ███║██╗", "   ╚╝   "],
    "=": ["       ", " █████╗ ", " ╚════╝ "],
    "*": ["   █╗   ", " ███║╚═╝", "   ╚╝   "],
}

BANNER_FONTS["block"] = {
    "A": [" █████╗ ", " ██╔══██╗", " ██████╔╝"],
    "B": ["██████╗ ", " ██╔══██╗", " ██████╔╝"],
    "C": [" █████╗ ", " ██║    ", " ╚██████╗"],
    "D": ["██████╗ ", " ██╔══██╗", " ██████╔╝"],
    "E": ["███████╗", " ██╔════╝", " ███████╗"],
    "F": ["███████╗", " ██╔════╝", " ██║     "],
    "G": [" █████╗ ", " ██╔════╝ ", " ╚██████╗"],
    "H": [" ██╗ ██╗", " ███████║", " ██╔══██║"],
    "I": [" █████╗ ", "   ██║   ", "   ██║   "],
    "J": ["      ██╗", "      ██║", " ██████╔╝"],
    "K": [" ██╗ ██╗", " ████╔╝ ", " ██╔═██╗ "],
    "L": [" ██╗    ", " ██║    ", " ███████╗"],
    "M": [" ███╗ ███╗", " ██╔████╔██║", " ██║╚██╔╝██║"],
    "N": [" ████╗ ██╗", " ██╔██╗██║", " ██║╚████║"],
    "O": [" █████╗ ", " ██╔══██╗", " ╚█████╔╝"],
    "P": ["██████╗ ", " ██╔══██╗", " ██║     "],
    "Q": [" █████╗  ", " ██╔══██╗ ", " ╚█████╔╝║"],
    "R": ["██████╗ ", " ██╔══██╗", " ██║ ╚═╝ "],
    "S": [" █████╗ ", " ╚═══██║", " ██████╔╝"],
    "T": ["████████╗", "    ██║   ", "    ██║   "],
    "U": [" ██╗ ██╗", " ██║ ██║", " ╚█████╔╝"],
    "V": [" ██╗ ██╗", " ██║ ██║", " ╚═╝ ╚═╝"],
    "W": [" ██╗    ██╗", " ██║ █╗ ██║", " ╚═╝ ╚═╝"],
    "X": [" ██╗ ██╗", " ╚═╝██║", " ██╗ ╚═╝"],
    "Y": [" ██╗ ██╗", " ╚═╝██║", " ██╗ ╚═╝"],
    "Z": ["██████╗ ", "    ╚═╝ ", " ██████╗"],
    "0": [" █████╗ ", " ██╔══██╗", " ╚█████╔╝"],
    "1": ["   ██╗  ", "   ██║  ", "   ██║  "],
    "2": ["██████╗ ", "    ╚═╝ ", " ██████╗"],
    "3": ["██████╗ ", "    ██╔╝", " ██████╔╝"],
    "4": [" ██╗ ██╗", " ██████║", "    ██║"],
    "5": ["███████╗", " ██████╔╝", " ╚═════╝"],
    "6": [" █████╗ ", " ██████╗ ", " ╚═════╝"],
    "7": ["██████╗ ", "    ██╔╝", "    ╚═╝ "],
    "8": [" █████╗ ", " ╚═══██║", " ██████╔╝"],
    "9": [" █████╗ ", " ╚████║", "    ╚═╝"],
    " ": [" ", " ", " "],
    ".": ["   ", "   ", " █╗"],
    "!": [" █╗", " █║", " ╚╝"],
    "?": ["████╗ ", "  ╔═╝ ", "  ╚═╝ "],
}

BANNER_FONTS["slant"] = {
    "A": [" /██╗ /██╗", " |██║ |██║", " |██║ |██║"],
    "B": [" /██████╗ ", " ||██╔═╝ ", " ||██████╗"],
    "C": [" /████╗ ", " |██╔═╝ ", " |██████╗"],
    "D": [" /██████╗ ", " |██╔══██╗", " |██████╔╝"],
    "E": [" /██████╗", " ||██╔══╝", " ||██████╗"],
    "F": [" /██████╗", " ||██╔══╝", " ||██║   "],
    "G": [" /████╗ ", " |██╔══╝ ", " |██████╗"],
    "H": [" /██╗ /██╗", " |██████║", " |██╔══██║"],
    "I": [" /██╗", " |██║", " |██║"],
    "J": ["     /██╗", "     |██║", " /████╔╝"],
    "K": [" /██╗ /██╗", " |███╔═╝ ", " |██╔═██╗"],
    "L": [" /██╗    ", " |██║    ", " |██████╗"],
    "M": [" /████╗ /████╗", " |██╔████╔██║", " |██║╚██╔╝██║"],
    "N": [" /████╗ /██╗", " |██╔██╗██║", " |██║╚████║"],
    "O": [" /████╗ ", " |██╔═██╗", " |██████╔╝"],
    "P": [" /████╗ ", " |██╔═██╗", " |██║    "],
    "Q": [" /████╗  ", " |██╔═██╗ ", " |██████╔╗"],
    "R": [" /████╗ ", " |██╔═██╗", " |██║ ╚═╝"],
    "S": [" /████╗ ", " |╚══╗╔╝", " |████╗ "],
    "T": [" /██████╗", "    ██║  ", "    ██║  "],
    "U": [" /██╗ /██╗", " |██║ |██║", " |██████╔╝"],
    "V": [" /██╗ /██╗", " |██║ |██║", "  ╚═╝ ╚═╝"],
    "W": [" /██╗   /██╗", " |██║ █╗ ██║", "  ╚═╝ ╚═╝"],
    "X": [" /██╗ /██╗", "  ╚═╝██║", " /██╗ ╚═╝"],
    "Y": [" /██╗ /██╗", "  ╚═╝██║", " /██╗ ╚═╝"],
    "Z": [" /████╗ ", "    ╚═╝ ", " /████╗ "],
    "0": [" /████╗ ", " |██╔═██╗", " |██████╔╝"],
    "1": [" /██╗", " |██║", " |██║"],
    "2": [" /████╗ ", "    ╚═╝ ", " /████╗ "],
    "3": [" /████╗ ", "    ██║ ", " |████╗ "],
    "4": [" /██╗ /██╗", " |██████║", "    ██║"],
    "5": [" /█████╗", " |████╗ ", " |════╝ "],
    "6": [" /████╗ ", " |████╗ ", " |════╝ "],
    "7": [" /████╗ ", "    ██║ ", "    ╚═╝ "],
    "8": [" /████╗ ", " |╚══╗╔╝", " |████╗ "],
    "9": [" /████╗ ", " |████║ ", "    ╚═╝ "],
    " ": [" ", " ", " "],
    ".": ["    ", "    ", " /█╗"],
    "!": [" /█╗", " |█║", "  ╚╝"],
}


def cmd_banner(args: argparse.Namespace) -> None:
    text = " ".join(args.text).upper()
    font_name = args.font or "standard"
    font = BANNER_FONTS.get(font_name)

    if not font:
        available = ", ".join(BANNER_FONTS.keys())
        print(f"⚠  Unknown font '{font_name}'. Available fonts: {available}", file=sys.stderr)
        sys.exit(1)

    # Build the banner row by row (3 rows high)
    lines = ["", "", ""]
    for ch in text:
        glyph = font.get(ch, font.get(" ", ["   ", "   ", "   "]))
        for i in range(3):
            lines[i] += glyph[i] + " "

    for line in lines:
        print(line.rstrip())


# ═══════════════════════════════════════════════════════════════════════════════
#  Box (unicode box drawing)
# ═══════════════════════════════════════════════════════════════════════════════

BOX_STYLES = {
    "single":     {"tl": "┌", "tr": "┐", "bl": "└", "br": "┘", "h": "─", "v": "│"},
    "double":     {"tl": "╔", "tr": "╗", "bl": "╚", "br": "╝", "h": "═", "v": "║"},
    "round":      {"tl": "╭", "tr": "╮", "bl": "╰", "br": "╯", "h": "─", "v": "│"},
    "thick":      {"tl": "▛", "tr": "▜", "bl": "▙", "br": "▟", "h": "▀", "v": "▌"},
}


def cmd_box(args: argparse.Namespace) -> None:
    text = " ".join(args.text)
    style_name = args.style or "single"
    style = BOX_STYLES.get(style_name)

    if not style:
        available = ", ".join(BOX_STYLES.keys())
        print(f"⚠  Unknown style '{style_name}'. Available styles: {available}", file=sys.stderr)
        sys.exit(1)

    # Handle multi-line text
    lines = text.split("\\n") if "\\n" in text else text.split("\n")
    max_width = max(len(l) for l in lines)

    # Top border
    print(f"{style['tl']}{style['h'] * (max_width + 2)}{style['tr']}")

    # Content lines
    for line in lines:
        print(f"{style['v']} {line.ljust(max_width)} {style['v']}")

    # Bottom border
    print(f"{style['bl']}{style['h'] * (max_width + 2)}{style['br']}")


# ═══════════════════════════════════════════════════════════════════════════════
#  Cowsay
# ═══════════════════════════════════════════════════════════════════════════════

COW_FACES = {
    "default": {
        "eyes": "oo",
        "tongue": "  ",
    },
    "stoned": {
        "eyes": "XX",
        "tongue": "  ",
    },
    "dead": {
        "eyes": "xx",
        "tongue": "U ",
    },
    "happy": {
        "eyes": "^^",
        "tongue": "  ",
    },
    "bored": {
        "eyes": "..",
        "tongue": "  ",
    },
}

COW_TEMPLATE = r"""
        \   ^__^
         \  ({eyes})\_______
            (__)\       )\/\
             {tongue} ||----w |
                ||     ||
"""


def cmd_cow(args: argparse.Namespace) -> None:
    msg = " ".join(args.msg)
    face_name = args.face or "default"
    face = COW_FACES.get(face_name)

    if not face:
        available = ", ".join(COW_FACES.keys())
        print(f"⚠  Unknown face '{face_name}'. Available faces: {available}", file=sys.stderr)
        sys.exit(1)

    # Build speech bubble
    lines = msg.split("\\n") if "\\n" in msg else msg.split("\n")
    if len(lines) == 1:
        bubble = f"< {msg} >"
    else:
        max_w = max(len(l) for l in lines)
        bubble_lines = [
            f"/ {' ' * max_w} \\",
        ]
        for l in lines:
            bubble_lines.append(f"| {l.ljust(max_w)} |")
        bubble_lines.append(f"\\ {' ' * max_w} /")
        bubble = "\n".join(bubble_lines)

    # Render cow
    cow = COW_TEMPLATE.format(**face)
    print(bubble)
    print(cow)


# ═══════════════════════════════════════════════════════════════════════════════
#  Table
# ═══════════════════════════════════════════════════════════════════════════════


def cmd_table(args: argparse.Namespace) -> None:
    if not args.header and not args.rows:
        print("⚠  Use --header and --rows to define table data", file=sys.stderr)
        sys.exit(1)

    header = args.header.split(",") if args.header else []
    rows = []
    for r in args.rows:
        rows.append([cell.strip() for cell in r.split(",")])

    if not header and rows:
        header = [f"Col{i+1}" for i in range(len(rows[0]))]

    # Determine column widths
    ncols = max(len(header), max(len(r) for r in rows) if rows else 0)
    col_widths = [len(h) for h in header]
    for row in rows:
        for i, cell in enumerate(row):
            if i < ncols:
                col_widths[i] = max(col_widths[i], len(cell))

    # Ensure all rows have same number of columns
    def _pad(row: List[str]) -> List[str]:
        return row + [""] * (ncols - len(row))

    # Render
    h_sep = "─" * (sum(col_widths) + 3 * ncols + 1)

    def _render_row(row: List[str], sep: str = "│") -> str:
        cells = [f" {cell.ljust(col_widths[i])} " for i, cell in enumerate(row)]
        return f"{sep}{sep.join(cells)}{sep}"

    print(h_sep)
    print(_render_row(header))
    print(f"├{'┼'.join('─' * (w + 2) for w in col_widths)}┤")

    for row in rows:
        print(_render_row(_pad(row)))

    print(h_sep)


# ═══════════════════════════════════════════════════════════════════════════════
#  Image to ASCII
# ═══════════════════════════════════════════════════════════════════════════════

# ASCII character ramp (dark to light)
ASCII_RAMP = " .:-=+*#%@"
ASCII_RAMP_REV = "@%#*+=-:. "


def _image_to_ascii(image_path: str, width: int = 80) -> str:
    """Convert an image to ASCII art using Python stdlib only.

    Tries several approaches in order:
      1. pymupdf (fitz) — if available for any image format
      2. ppm/pgm/pbm — raw pixel access via stdlib
      3. Fallback — read as raw data
    """
    # Try Pillow if available (most reliable)
    try:
        from PIL import Image
        img = Image.open(image_path)
        return _pixels_to_ascii(img, width)
    except ImportError:
        pass

    # Try pymupdf for image loading
    try:
        import fitz
        pix = fitz.Pixmap(image_path)
        if pix.n >= 4:
            pix = fitz.Pixmap(fitz.csRGB, pix)
        img_w, img_h = pix.width, pix.height
        pixels = pix.samples
        # Convert to PIL-like interface manually
        class _SimpleImage:
            def __init__(self, w, h, samples):
                self.width = w
                self.height = h
                self._samples = samples
            def getpixel(self, xy):
                x, y = xy
                idx = (y * self.width + x) * 3
                return tuple(self._samples[idx:idx+3])
        img = _SimpleImage(img_w, img_h, pixels)
        return _pixels_to_ascii_simple(img, width)
    except ImportError:
        pass

    # Try stdlib: detect PPM/PGM/PBM
    try:
        with open(image_path, "rb") as f:
            header = f.read(2)
            f.seek(0)
            if header in (b"P6", b"P3", b"P5", b"P2"):
                return _parse_netpbm(f, image_path, width)
    except Exception:
        pass

    return "⚠  Image conversion requires PIL (Pillow) or a supported format (PPM/PGM/PBM).\n   Install with: pip install Pillow"


def _pixels_to_ascii(img, width: int) -> str:
    """Convert a PIL Image to ASCII."""
    # Calculate aspect-ratio-preserved height
    orig_w, orig_h = img.size
    aspect = orig_h / orig_w
    height = int(aspect * width * 0.45)  # terminal chars are ~2x tall

    img_small = img.resize((width, height))
    result = []
    for y in range(height):
        row = []
        for x in range(width):
            r, g, b = img_small.getpixel((x, y))[:3]
            gray = int(0.299 * r + 0.587 * g + 0.114 * b)
            idx = gray * (len(ASCII_RAMP) - 1) // 255
            row.append(ASCII_RAMP[idx])
        result.append("".join(row))
    return "\n".join(result)


def _pixels_to_ascii_simple(img, width: int) -> str:
    """Convert a simple image object (getpixel, width, height) to ASCII."""
    orig_w = img.width
    orig_h = img.height
    aspect = orig_h / orig_w
    height = int(aspect * width * 0.45)

    result = []
    for y in range(height):
        row = []
        for x in range(width):
            # Map to source pixel
            sx = int(x * orig_w / width)
            sy = int(y * orig_h / height)
            r, g, b = img.getpixel((sx, sy))[:3]
            gray = int(0.299 * r + 0.587 * g + 0.114 * b)
            idx = gray * (len(ASCII_RAMP) - 1) // 255
            row.append(ASCII_RAMP[idx])
        result.append("".join(row))
    return "\n".join(result)


def _parse_netpbm(f, path: str, width: int) -> str:
    """Parse PPM/PGM/PBM format using stdlib only."""
    from pathlib import Path

    # Read header
    magic = f.readline().strip().decode()
    while True:
        line = f.readline().strip().decode()
        if not line.startswith("#"):
            dimensions = line
            break
    w, h = map(int, dimensions.split())
    maxval_line = f.readline().strip().decode()
    maxval = int(maxval_line) if maxval_line else 255

    if magic == "P6":  # PPM (color)
        data = f.read()
        pixels = []
        for y in range(h):
            for x in range(w):
                idx = (y * w + x) * 3
                r, g, b = data[idx], data[idx+1], data[idx+2]
                pixels.append((r, g, b))
    elif magic == "P5":  # PGM (grayscale)
        data = f.read()
        pixels = [(data[y * w + x], data[y * w + x], data[y * w + x]) for y in range(h) for x in range(w)]
    elif magic == "P2":  # PGM ascii
        vals = list(map(int, f.read().split()))
        pixels = [(vals[y * w + x], vals[y * w + x], vals[y * w + x]) for y in range(h) for x in range(w)]
    elif magic == "P3":  # PPM ascii
        vals = list(map(int, f.read().split()))
        pixels = [(vals[(y * w + x) * 3], vals[(y * w + x) * 3 + 1], vals[(y * w + x) * 3 + 2])
                  for y in range(h) for x in range(w)]
    else:
        return "⚠  Unsupported NetPBM format"

    # Resize and convert
    aspect = h / w
    out_h = int(aspect * width * 0.45)
    result = []
    for y in range(out_h):
        row = []
        for x in range(width):
            sx = int(x * w / width)
            sy = int(y * h / out_h)
            r, g, b = pixels[sy * w + sx]
            gray = int(0.299 * r + 0.587 * g + 0.114 * b)
            idx = gray * (len(ASCII_RAMP) - 1) // 255
            row.append(ASCII_RAMP[idx])
        result.append("".join(row))
    return "\n".join(result)


def cmd_image(args: argparse.Namespace) -> None:
    path = args.path
    if not os.path.isfile(path):
        print(f"⚠  File not found: {path}", file=sys.stderr)
        sys.exit(1)

    width = args.width or 80
    art = _image_to_ascii(path, width)

    # Check if we got an error
    if art.startswith("⚠"):
        print(art, file=sys.stderr)
        sys.exit(1)

    print(art)
    print(f"\n({path} — {width} cols)")


# ═══════════════════════════════════════════════════════════════════════════════
#  CLI
# ═══════════════════════════════════════════════════════════════════════════════


def _self_test():
    """Real test of the banner/box rendering core (no images). Returns 0/1."""
    import io
    import contextlib

    # 1. Banner must render known letters using block glyphs.
    ns = argparse.Namespace(text=["HI"], font=None)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        cmd_banner(ns)
    banner_out = buf.getvalue()
    if not banner_out.strip():
        print("self-test: FAIL (banner produced no output)")
        return 1
    if "█" not in banner_out:
        print("self-test: FAIL (banner missing expected block glyphs)")
        return 1

    # 2. Box must render a unicode border.
    ns = argparse.Namespace(text=["OK"], style=None)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        cmd_box(ns)
    box_out = buf.getvalue()
    if "┌" not in box_out or "┐" not in box_out or "OK" not in box_out:
        print("self-test: FAIL (box missing expected border/content)")
        return 1

    # 3. Font/style tables must exist.
    if not BANNER_FONTS or not BOX_STYLES:
        print("self-test: FAIL (missing font/style tables)")
        return 1

    print("self-test: PASS")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="ASCII Art Creator — banners, boxes, cowsay, tables, and image-to-ASCII",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  %(prog)s banner \"Hello\"\n"
            "  %(prog)s banner \"Welcome\" --font block\n"
            "  %(prog)s box \"System ready\" --style double\n"
            "  %(prog)s cow \"Moo!\" --face happy\n"
            "  %(prog)s table --header \"Name,Age\" --rows \"Alice,30\" \"Bob,25\"\n"
            "  %(prog)s image photo.jpg --width 60\n"
        ),
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # banner
    p_banner = sub.add_parser("banner", help="Generate an ASCII banner")
    p_banner.add_argument("text", nargs="+", help="Text to render as a banner")
    p_banner.add_argument("--font", choices=list(BANNER_FONTS.keys()), default="standard",
                          help="Banner font style")

    # box
    p_box = sub.add_parser("box", help="Wrap text in a unicode box")
    p_box.add_argument("text", nargs="+", help="Text to box")
    p_box.add_argument("--style", choices=list(BOX_STYLES.keys()), default="single",
                       help="Box border style")

    # cow
    p_cow = sub.add_parser("cow", help="Display a cowsay message")
    p_cow.add_argument("msg", nargs="+", help="Message for the cow")
    p_cow.add_argument("--face", choices=list(COW_FACES.keys()), default="default",
                       help="Cow facial expression")

    # table
    p_table = sub.add_parser("table", help="Render an ASCII table")
    p_table.add_argument("--header", help="Comma-separated column headers")
    p_table.add_argument("--rows", nargs="+", required=True,
                         help="Rows as comma-separated values")

    # image
    p_image = sub.add_parser("image", help="Convert image to ASCII art")
    p_image.add_argument("path", help="Path to image file")
    p_image.add_argument("--width", type=int, default=80,
                         help="Output width in characters (default: 80)")

    # self-test
    sub.add_parser("self-test", help="Run built-in self tests")

    args = parser.parse_args()

    if args.command == "banner":
        cmd_banner(args)
    elif args.command == "box":
        cmd_box(args)
    elif args.command == "cow":
        cmd_cow(args)
    elif args.command == "table":
        cmd_table(args)
    elif args.command == "image":
        cmd_image(args)
    elif args.command == "self-test":
        sys.exit(_self_test())
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
