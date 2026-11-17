#!/usr/bin/env python3
"""Color toolkit — convert, analyze, and generate color palettes from the CLI.

Features:
- Convert between HEX, RGB, HSL, HSV, CMYK
- WCAG contrast ratio checker (AA/AAA compliance)
- Color palette generation (complementary, analogous, triadic, split-complementary, monochromatic)
- Lighten/darken/saturate/desaturate colors
- Mix two colors
- Random color generation
- Named CSS colors lookup
- JSON output support

No external dependencies (Python stdlib only).
"""

import argparse
import colorsys
import json
import math
import random
import sys


# --- CSS Named Colors (subset of most common) ---
CSS_COLORS = {
    "black": "#000000", "white": "#ffffff", "red": "#ff0000", "green": "#008000",
    "blue": "#0000ff", "yellow": "#ffff00", "cyan": "#00ffff", "magenta": "#ff00ff",
    "silver": "#c0c0c0", "gray": "#808080", "grey": "#808080", "maroon": "#800000",
    "olive": "#808000", "lime": "#00ff00", "aqua": "#00ffff", "teal": "#008080",
    "navy": "#000080", "fuchsia": "#ff00ff", "purple": "#800080", "orange": "#ffa500",
    "pink": "#ffc0cb", "coral": "#ff7f50", "salmon": "#fa8072", "tomato": "#ff6347",
    "gold": "#ffd700", "khaki": "#f0e68c", "indigo": "#4b0082", "violet": "#ee82ee",
    "plum": "#dda0dd", "orchid": "#da70d6", "lavender": "#e6e6fa", "beige": "#f5f5dc",
    "ivory": "#fffff0", "linen": "#faf0e6", "wheat": "#f5deb3", "tan": "#d2b48c",
    "chocolate": "#d2691e", "sienna": "#a0522d", "brown": "#a52a2a", "crimson": "#dc143c",
    "firebrick": "#b22222", "darkred": "#8b0000", "orangered": "#ff4500",
    "darkorange": "#ff8c00", "peachpuff": "#ffdab9", "moccasin": "#ffe4b5",
    "chartreuse": "#7fff00", "springgreen": "#00ff7f", "aquamarine": "#7fffd4",
    "turquoise": "#40e0d0", "steelblue": "#4682b4", "royalblue": "#4169e1",
    "cornflowerblue": "#6495ed", "dodgerblue": "#1e90ff", "deepskyblue": "#00bfff",
    "skyblue": "#87ceeb", "slateblue": "#6a5acd", "darkslateblue": "#483d8b",
    "midnightblue": "#191970", "hotpink": "#ff69b4", "deeppink": "#ff1493",
    "mediumvioletred": "#c71585", "rosybrown": "#bc8f8f", "darkgray": "#a9a9a9",
    "dimgray": "#696969", "lightgray": "#d3d3d3", "gainsboro": "#dcdcdc",
    "whitesmoke": "#f5f5f5", "snow": "#fffafa", "ghostwhite": "#f8f8ff",
    "floralwhite": "#fffaf0", "aliceblue": "#f0f8ff", "honeydew": "#f0fff0",
    "mintcream": "#f5fffa", "seashell": "#fff5ee", "oldlace": "#fdf5e6",
}


# --- Color parsing and conversion ---

def parse_color(color_str):
    """Parse a color string to (r, g, b) tuple (0-255)."""
    color_str = color_str.strip().lower()

    # Named CSS color
    if color_str in CSS_COLORS:
        color_str = CSS_COLORS[color_str]

    # HEX
    if color_str.startswith("#"):
        hex_str = color_str[1:]
        if len(hex_str) == 3:
            hex_str = "".join(c * 2 for c in hex_str)
        if len(hex_str) == 6:
            r = int(hex_str[0:2], 16)
            g = int(hex_str[2:4], 16)
            b = int(hex_str[4:6], 16)
            return (r, g, b)

    # rgb(r, g, b)
    if color_str.startswith("rgb(") and color_str.endswith(")"):
        parts = color_str[4:-1].split(",")
        if len(parts) == 3:
            return tuple(int(p.strip()) for p in parts)

    # r,g,b
    if "," in color_str:
        parts = color_str.split(",")
        if len(parts) == 3:
            return tuple(int(p.strip()) for p in parts)

    # hsl(h, s%, l%)
    if color_str.startswith("hsl(") and color_str.endswith(")"):
        parts = color_str[4:-1].replace("%", "").split(",")
        if len(parts) == 3:
            h = float(parts[0].strip()) / 360
            s = float(parts[1].strip()) / 100
            l = float(parts[2].strip()) / 100
            r, g, b = colorsys.hls_to_rgb(h, l, s)
            return (int(r * 255), int(g * 255), int(b * 255))

    raise ValueError(f"Cannot parse color: '{color_str}'. Use #hex, rgb(r,g,b), hsl(h,s%,l%), r,g,b, or a CSS name.")


def rgb_to_hex(r, g, b):
    return f"#{r:02x}{g:02x}{b:02x}"


def rgb_to_hsl(r, g, b):
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    return (round(h * 360, 1), round(s * 100, 1), round(l * 100, 1))


def rgb_to_hsv(r, g, b):
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    return (round(h * 360, 1), round(s * 100, 1), round(v * 100, 1))


def rgb_to_cmyk(r, g, b):
    if r == 0 and g == 0 and b == 0:
        return (0, 0, 0, 100)
    c = 1 - r / 255
    m = 1 - g / 255
    y = 1 - b / 255
    k = min(c, m, y)
    c = round((c - k) / (1 - k) * 100, 1)
    m = round((m - k) / (1 - k) * 100, 1)
    y = round((y - k) / (1 - k) * 100, 1)
    k = round(k * 100, 1)
    return (c, m, y, k)


def hsl_to_rgb(h, s, l):
    """h in degrees, s and l in 0-100."""
    r, g, b = colorsys.hls_to_rgb(h / 360, l / 100, s / 100)
    return (int(round(r * 255)), int(round(g * 255)), int(round(b * 255)))


def format_color(r, g, b, as_json=False):
    """Format a color in all representations."""
    hex_val = rgb_to_hex(r, g, b)
    h, s, l = rgb_to_hsl(r, g, b)
    hv, sv, vv = rgb_to_hsv(r, g, b)
    c, m, y, k = rgb_to_cmyk(r, g, b)

    # Find CSS name
    css_name = None
    for name, hex_code in CSS_COLORS.items():
        if hex_code == hex_val:
            css_name = name
            break

    data = {
        "hex": hex_val,
        "rgb": f"rgb({r}, {g}, {b})",
        "hsl": f"hsl({h}, {s}%, {l}%)",
        "hsv": f"hsv({hv}, {sv}%, {vv}%)",
        "cmyk": f"cmyk({c}%, {m}%, {y}%, {k}%)",
    }
    if css_name:
        data["name"] = css_name

    if as_json:
        return data

    lines = []
    for key, val in data.items():
        lines.append(f"  {key:>5}: {val}")
    return "\n".join(lines)


# --- WCAG Contrast ---

def relative_luminance(r, g, b):
    """Calculate relative luminance per WCAG 2.0."""
    def linearize(c):
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    return 0.2126 * linearize(r) + 0.7152 * linearize(g) + 0.0722 * linearize(b)


def contrast_ratio(rgb1, rgb2):
    """Calculate WCAG contrast ratio between two colors."""
    l1 = relative_luminance(*rgb1)
    l2 = relative_luminance(*rgb2)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def wcag_compliance(ratio):
    """Return WCAG compliance levels."""
    levels = []
    if ratio >= 3:
        levels.append("AA Large Text")
    if ratio >= 4.5:
        levels.append("AA Normal Text")
    if ratio >= 4.5:
        levels.append("AAA Large Text")
    if ratio >= 7:
        levels.append("AAA Normal Text")
    return levels if levels else ["Fails all WCAG levels"]


# --- Palette Generation ---

def rotate_hue(h, s, l, degrees):
    new_h = (h + degrees) % 360
    return hsl_to_rgb(new_h, s, l)


def palette_complementary(r, g, b):
    h, s, l = rgb_to_hsl(r, g, b)
    return [(r, g, b), rotate_hue(h, s, l, 180)]


def palette_analogous(r, g, b):
    h, s, l = rgb_to_hsl(r, g, b)
    return [rotate_hue(h, s, l, -30), (r, g, b), rotate_hue(h, s, l, 30)]


def palette_triadic(r, g, b):
    h, s, l = rgb_to_hsl(r, g, b)
    return [(r, g, b), rotate_hue(h, s, l, 120), rotate_hue(h, s, l, 240)]


def palette_split_complementary(r, g, b):
    h, s, l = rgb_to_hsl(r, g, b)
    return [(r, g, b), rotate_hue(h, s, l, 150), rotate_hue(h, s, l, 210)]


def palette_monochromatic(r, g, b, count=5):
    h, s, l = rgb_to_hsl(r, g, b)
    step = 80 / (count - 1) if count > 1 else 0
    start_l = max(10, l - 40)
    colors = []
    for i in range(count):
        new_l = min(95, start_l + step * i)
        colors.append(hsl_to_rgb(h, s, new_l))
    return colors


# --- Color manipulation ---

def lighten(r, g, b, amount=10):
    h, s, l = rgb_to_hsl(r, g, b)
    l = min(100, l + amount)
    return hsl_to_rgb(h, s, l)


def darken(r, g, b, amount=10):
    h, s, l = rgb_to_hsl(r, g, b)
    l = max(0, l - amount)
    return hsl_to_rgb(h, s, l)


def saturate(r, g, b, amount=10):
    h, s, l = rgb_to_hsl(r, g, b)
    s = min(100, s + amount)
    return hsl_to_rgb(h, s, l)


def desaturate(r, g, b, amount=10):
    h, s, l = rgb_to_hsl(r, g, b)
    s = max(0, s - amount)
    return hsl_to_rgb(h, s, l)


def mix_colors(rgb1, rgb2, weight=0.5):
    r = int(rgb1[0] * (1 - weight) + rgb2[0] * weight)
    g = int(rgb1[1] * (1 - weight) + rgb2[1] * weight)
    b = int(rgb1[2] * (1 - weight) + rgb2[2] * weight)
    return (r, g, b)


# --- Commands ---

def cmd_convert(args):
    rgb = parse_color(args.color)
    if args.json:
        print(json.dumps(format_color(*rgb, as_json=True), indent=2))
    else:
        print(format_color(*rgb))


def cmd_contrast(args):
    fg = parse_color(args.foreground)
    bg = parse_color(args.background)
    ratio = contrast_ratio(fg, bg)
    compliance = wcag_compliance(ratio)

    if args.json:
        print(json.dumps({
            "foreground": rgb_to_hex(*fg),
            "background": rgb_to_hex(*bg),
            "ratio": round(ratio, 2),
            "compliance": compliance,
        }, indent=2))
    else:
        print(f"Foreground: {rgb_to_hex(*fg)}")
        print(f"Background: {rgb_to_hex(*bg)}")
        print(f"Ratio:      {ratio:.2f}:1")
        print(f"Compliance: {', '.join(compliance)}")


def cmd_palette(args):
    rgb = parse_color(args.color)
    scheme = args.scheme

    palette_map = {
        "complementary": palette_complementary,
        "analogous": palette_analogous,
        "triadic": palette_triadic,
        "split-complementary": palette_split_complementary,
    }

    if scheme == "monochromatic":
        colors = palette_monochromatic(*rgb, count=args.count)
    elif scheme in palette_map:
        colors = palette_map[scheme](*rgb)
    else:
        print(f"Unknown scheme: {scheme}", file=sys.stderr)
        sys.exit(1)

    if args.json:
        result = [format_color(*c, as_json=True) for c in colors]
        print(json.dumps(result, indent=2))
    else:
        print(f"Palette: {scheme} from {rgb_to_hex(*rgb)}\n")
        for i, c in enumerate(colors, 1):
            print(f"  {i}. {rgb_to_hex(*c)}  rgb({c[0]}, {c[1]}, {c[2]})")


def cmd_modify(args):
    rgb = parse_color(args.color)
    amount = args.amount

    operations = {
        "lighten": lighten,
        "darken": darken,
        "saturate": saturate,
        "desaturate": desaturate,
    }

    if args.operation not in operations:
        print(f"Unknown operation: {args.operation}", file=sys.stderr)
        sys.exit(1)

    result = operations[args.operation](*rgb, amount)
    original_hex = rgb_to_hex(*rgb)
    result_hex = rgb_to_hex(*result)

    if args.json:
        print(json.dumps({
            "original": original_hex,
            "operation": args.operation,
            "amount": amount,
            "result": format_color(*result, as_json=True),
        }, indent=2))
    else:
        print(f"Original:  {original_hex}")
        print(f"Operation: {args.operation} by {amount}")
        print(f"Result:    {result_hex}")
        print(format_color(*result))


def cmd_mix(args):
    c1 = parse_color(args.color1)
    c2 = parse_color(args.color2)
    result = mix_colors(c1, c2, args.weight)

    if args.json:
        print(json.dumps({
            "color1": rgb_to_hex(*c1),
            "color2": rgb_to_hex(*c2),
            "weight": args.weight,
            "result": format_color(*result, as_json=True),
        }, indent=2))
    else:
        print(f"Color 1: {rgb_to_hex(*c1)}")
        print(f"Color 2: {rgb_to_hex(*c2)}")
        print(f"Weight:  {args.weight}")
        print(f"Result:  {rgb_to_hex(*result)}")
        print(format_color(*result))


def cmd_random(args):
    colors = []
    for _ in range(args.count):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        colors.append((r, g, b))

    if args.json:
        result = [format_color(*c, as_json=True) for c in colors]
        print(json.dumps(result, indent=2))
    else:
        for c in colors:
            print(f"  {rgb_to_hex(*c)}  rgb({c[0]}, {c[1]}, {c[2]})")


def cmd_lookup(args):
    query = args.name.lower()
    matches = {k: v for k, v in CSS_COLORS.items() if query in k}

    if not matches:
        print(f"No CSS colors matching '{args.name}'.")
        return

    if args.json:
        print(json.dumps(matches, indent=2))
    else:
        print(f"CSS colors matching '{args.name}':\n")
        for name, hex_val in sorted(matches.items()):
            print(f"  {name:<25} {hex_val}")


def main():
    parser = argparse.ArgumentParser(
        description="Color toolkit — convert, analyze, and generate color palettes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  %(prog)s convert '#ff6347'
  %(prog)s convert 'rgb(255, 99, 71)'
  %(prog)s convert tomato
  %(prog)s contrast '#000000' '#ffffff'
  %(prog)s palette '#3498db' --scheme triadic
  %(prog)s modify '#3498db' --op lighten --amount 20
  %(prog)s mix '#ff0000' '#0000ff' --weight 0.5
  %(prog)s random -n 5
  %(prog)s lookup blue
"""
    )
    sub = parser.add_subparsers(dest="command", help="Command to run")

    # convert
    p_conv = sub.add_parser("convert", help="Convert color between formats")
    p_conv.add_argument("color", help="Color (#hex, rgb(), hsl(), name, or r,g,b)")
    p_conv.add_argument("--json", action="store_true", help="JSON output")

    # contrast
    p_cont = sub.add_parser("contrast", help="WCAG contrast ratio checker")
    p_cont.add_argument("foreground", help="Foreground color")
    p_cont.add_argument("background", help="Background color")
    p_cont.add_argument("--json", action="store_true", help="JSON output")

    # palette
    p_pal = sub.add_parser("palette", help="Generate color palettes")
    p_pal.add_argument("color", help="Base color")
    p_pal.add_argument("--scheme", "-s", required=True,
                       choices=["complementary", "analogous", "triadic",
                                "split-complementary", "monochromatic"],
                       help="Palette scheme")
    p_pal.add_argument("--count", "-n", type=int, default=5,
                       help="Number of colors for monochromatic (default: 5)")
    p_pal.add_argument("--json", action="store_true", help="JSON output")

    # modify
    p_mod = sub.add_parser("modify", help="Lighten, darken, saturate, or desaturate")
    p_mod.add_argument("color", help="Color to modify")
    p_mod.add_argument("--op", "--operation", dest="operation", required=True,
                       choices=["lighten", "darken", "saturate", "desaturate"],
                       help="Modification operation")
    p_mod.add_argument("--amount", "-a", type=float, default=10,
                       help="Amount (0-100 scale, default: 10)")
    p_mod.add_argument("--json", action="store_true", help="JSON output")

    # mix
    p_mix = sub.add_parser("mix", help="Mix two colors")
    p_mix.add_argument("color1", help="First color")
    p_mix.add_argument("color2", help="Second color")
    p_mix.add_argument("--weight", "-w", type=float, default=0.5,
                       help="Weight of second color (0.0-1.0, default: 0.5)")
    p_mix.add_argument("--json", action="store_true", help="JSON output")

    # random
    p_rand = sub.add_parser("random", help="Generate random colors")
    p_rand.add_argument("-n", "--count", type=int, default=1,
                        help="Number of colors (default: 1)")
    p_rand.add_argument("--json", action="store_true", help="JSON output")

    # lookup
    p_look = sub.add_parser("lookup", help="Search CSS named colors")
    p_look.add_argument("name", help="Color name to search for")
    p_look.add_argument("--json", action="store_true", help="JSON output")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(0)

    cmd_map = {
        "convert": cmd_convert,
        "contrast": cmd_contrast,
        "palette": cmd_palette,
        "modify": cmd_modify,
        "mix": cmd_mix,
        "random": cmd_random,
        "lookup": cmd_lookup,
    }

    cmd_map[args.command](args)


if __name__ == "__main__":
    main()
