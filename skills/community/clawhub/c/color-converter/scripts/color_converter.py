#!/usr/bin/env python3
"""Color format converter - HEX, RGB, RGBA, HSL, HSLA, named colors."""

import argparse
import colorsys
import re
import sys
import os

# Add named colors lookup (common CSS named colors)
NAMED_COLORS = {
    'black': '#000000', 'white': '#ffffff', 'red': '#ff0000',
    'green': '#008000', 'blue': '#0000ff', 'yellow': '#ffff00',
    'cyan': '#00ffff', 'magenta': '#ff00ff', 'silver': '#c0c0c0',
    'gray': '#808080', 'grey': '#808080', 'maroon': '#800000',
    'olive': '#808000', 'lime': '#00ff00', 'aqua': '#00ffff',
    'teal': '#008080', 'navy': '#000080', 'fuchsia': '#ff00ff',
    'purple': '#800080', 'orange': '#ffa500', 'pink': '#ffc0cb',
    'coral': '#ff7f50', 'tomato': '#ff6347', 'salmon': '#fa8072',
    'gold': '#ffd700', 'khaki': '#f0e68c', 'plum': '#dda0dd',
    'violet': '#ee82ee', 'indigo': '#4b0082', 'turquoise': '#40e0d0',
    'sky': '#87ceeb', 'navyblue': '#000080', 'steelblue': '#4682b4',
    'crimson': '#dc143c', 'sandy': '#f4a460', 'tan': '#d2b48c',
    'beige': '#f5f5dc', 'ivory': '#fffff0', 'snow': '#fffafa',
    'wheat': '#f5deb3', 'peru': '#cd853f', 'rosybrown': '#bc8f8f',
    'dodgerblue': '#1e90ff', 'royalblue': '#4169e1', 'darkviolet': '#9400d3',
    'mediumorchid': '#ba55d3', 'orchid': '#da70d6', 'thistle': '#d8bfd8',
    'lavender': '#e6e6fa', 'mintcream': '#f5fffa', 'honeydew': '#f0fff0',
}


def hex_to_rgb(hex_color: str) -> tuple:
    """Convert HEX to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 3:
        hex_color = ''.join(c * 2 for c in hex_color)
    if len(hex_color) != 6:
        raise ValueError(f"Invalid HEX format: #{hex_color}")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb: tuple) -> str:
    """Convert RGB tuple to HEX."""
    return '#{:02x}{:02x}{:02x}'.format(
        max(0, min(255, int(rgb[0]))),
        max(0, min(255, int(rgb[1]))),
        max(0, min(255, int(rgb[2])))
    )


def rgb_to_hsl(rgb: tuple) -> tuple:
    """Convert RGB to HSL tuple (h in 0-360, s and l in 0-100)."""
    r, g, b = (x / 255.0 for x in rgb)
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return (round(h * 360), round(s * 100), round(l * 100))


def hsl_to_rgb(h: float, s: float, l: float) -> tuple:
    """Convert HSL to RGB tuple."""
    r, g, b = colorsys.hls_to_rgb(h / 360, l / 100, s / 100)
    return (round(r * 255), round(g * 255), round(b * 255))


def parse_color_input(color_str: str):
    """Parse any color input and return (rgb_tuple, alpha)."""
    color_str = color_str.strip()

    # Named color
    if color_str.lower() in NAMED_COLORS:
        return hex_to_rgb(NAMED_COLORS[color_str.lower()]), 1.0

    # HEX
    if color_str.startswith('#'):
        hex_val = color_str.lstrip('#')
        if len(hex_val) == 8:  # With alpha
            rgb = hex_to_rgb(hex_val[:6])
            alpha = int(hex_val[6:], 16) / 255.0
            return rgb, round(alpha, 3)
        elif len(hex_val) in (3, 6):
            return hex_to_rgb(hex_val), 1.0
        raise ValueError(f"Invalid HEX: {color_str}")

    # RGB/RGBA
    rgb_match = re.match(r'rgba?\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(?:,\s*([\d.]+))?\s*\)', color_str, re.I)
    if rgb_match:
        r, g, b = int(rgb_match.group(1)), int(rgb_match.group(2)), int(rgb_match.group(3))
        alpha = float(rgb_match.group(4)) if rgb_match.group(4) else 1.0
        if alpha > 1:
            alpha = alpha / 255.0
        return (r, g, b), round(alpha, 3)

    # HSL/HSLA
    hsl_match = re.match(r'hsla?\s*\(\s*([\d.]+)\s*,\s*([\d.]+)%?\s*,\s*([\d.]+)%?\s*(?:,\s*([\d.]+))?\s*\)', color_str, re.I)
    if hsl_match:
        h, s, l = float(hsl_match.group(1)), float(hsl_match.group(2)), float(hsl_match.group(3))
        alpha = float(hsl_match.group(4)) if hsl_match.group(4) else 1.0
        rgb = hsl_to_rgb(h, s, l)
        return rgb, round(alpha, 3)

    raise ValueError(f"Unknown color format: {color_str}")


def format_output(rgb: tuple, alpha: float, fmt: str) -> str:
    """Format RGB color to requested output format."""
    if fmt == 'hex':
        return rgb_to_hex(rgb)
    elif fmt == 'rgb':
        return f"rgb({rgb[0]}, {rgb[1]}, {rgb[2]})"
    elif fmt == 'rgba':
        return f"rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, {alpha})"
    elif fmt == 'hsl':
        h, s, l = rgb_to_hsl(rgb)
        return f"hsl({h}, {s}%, {l}%)"
    elif fmt == 'hsla':
        h, s, l = rgb_to_hsl(rgb)
        return f"hsla({h}, {s}%, {l}%, {alpha})"
    elif fmt == 'all':
        hex_c = rgb_to_hex(rgb)
        r, g, b = rgb
        h, s, l = rgb_to_hsl(rgb)
        lines = [
            f"HEX:  {hex_c}",
            f"RGB:  rgb({r}, {g}, {b})",
            f"RGBA: rgba({r}, {g}, {b}, {alpha})",
            f"HSL:  hsl({h}, {s}%, {l}%)",
            f"HSLA: hsla({h}, {s}%, {l}%, {alpha})",
        ]
        return '\n'.join(lines)
    else:
        return rgb_to_hex(rgb)


def main():
    parser = argparse.ArgumentParser(description='Convert colors between HEX, RGB, HSL formats')
    parser.add_argument('color', help='Color in any format (HEX, RGB, HSL, named color)')
    parser.add_argument('--output', '-o', default='all',
                       choices=['hex', 'rgb', 'rgba', 'hsl', 'hsla', 'all'],
                       help='Output format (default: all)')

    args = parser.parse_args()

    try:
        rgb, alpha = parse_color_input(args.color)
        output = format_output(rgb, alpha, args.output)
        print(output)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
