"""
🛠️ axiom-color-palette — Color Palette Generator
=================================================

Skill Axiome #14 (Phase 4 — Extraction)

⚠️ LIMITATIONS CONNUES :
- Pas d'extraction depuis image (utiliser PIL pour ça)
- Pas de gestion d'alpha (RGB seulement)
- Pas de WCAG accessibility scoring (à ajouter)

GÉNÈRE DES HARMONIES DE COULEURS À PARTIR D'UNE COULEUR DE BASE
"""

import colorsys
import re
import sys


def parse_hex(hex_str: str) -> tuple:
    """Parse a hex color string to (r, g, b) tuple (0-255)."""
    hex_str = hex_str.strip().lstrip("#")
    if len(hex_str) == 3:
        hex_str = "".join(c * 2 for c in hex_str)
    if len(hex_str) != 6:
        raise ValueError(f"Invalid hex color: {hex_str}")
    try:
        r = int(hex_str[0:2], 16)
        g = int(hex_str[2:4], 16)
        b = int(hex_str[4:6], 16)
        return (r, g, b)
    except ValueError:
        raise ValueError(f"Invalid hex color: {hex_str}")


def to_hex(rgb: tuple) -> str:
    """Convert (r, g, b) tuple to #RRGGBB string."""
    return "#{:02X}{:02X}{:02X}".format(*rgb)


def to_rgb_string(rgb: tuple) -> str:
    """Convert to 'rgb(r, g, b)' string."""
    return f"rgb({rgb[0]}, {rgb[1]}, {rgb[2]})"


def hsl(rgb: tuple) -> tuple:
    """Convert (r, g, b) to (h, s, l) where h is 0-360, s and l are 0-100."""
    r, g, b = [v / 255.0 for v in rgb]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return (round(h * 360, 1), round(s * 100, 1), round(l * 100, 1))


def to_hsl_string(rgb: tuple) -> str:
    """Convert to 'hsl(h, s%, l%)' string."""
    h, s, l = hsl(rgb)
    return f"hsl({h}, {s}%, {l}%)"


def rotate_hue(rgb: tuple, degrees: float) -> tuple:
    """Rotate hue by N degrees."""
    r, g, b = [v / 255.0 for v in rgb]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    new_h = (h + degrees / 360.0) % 1.0
    new_r, new_g, new_b = colorsys.hls_to_rgb(new_h, l, s)
    return (round(new_r * 255), round(new_g * 255), round(new_b * 255))


def adjust_lightness(rgb: tuple, delta: float) -> tuple:
    """Adjust lightness by delta (positive = lighter, negative = darker)."""
    r, g, b = [v / 255.0 for v in rgb]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    new_l = max(0, min(1, l + delta / 100.0))
    new_r, new_g, new_b = colorsys.hls_to_rgb(h, new_l, s)
    return (round(new_r * 255), round(new_g * 255), round(new_b * 255))


def complementary(rgb: tuple) -> list:
    """Complementary color (opposite on color wheel)."""
    return [rgb, rotate_hue(rgb, 180)]


def analogous(rgb: tuple) -> list:
    """Analogous colors (adjacent on color wheel)."""
    return [rotate_hue(rgb, -30), rgb, rotate_hue(rgb, 30)]


def triadic(rgb: tuple) -> list:
    """Triadic colors (120° apart)."""
    return [rgb, rotate_hue(rgb, 120), rotate_hue(rgb, 240)]


def tetradic(rgb: tuple) -> list:
    """Tetradic / square colors (90° apart)."""
    return [rgb, rotate_hue(rgb, 90), rotate_hue(rgb, 180), rotate_hue(rgb, 270)]


def split_complementary(rgb: tuple) -> list:
    """Split-complementary (180° ± 30°)."""
    return [rgb, rotate_hue(rgb, 150), rotate_hue(rgb, 210)]


def monochromatic(rgb: tuple, count: int = 5) -> list:
    """Monochromatic palette (same hue, varying lightness)."""
    if count < 2:
        return [rgb]
    step = 80 / (count - 1)
    return [adjust_lightness(rgb, -40 + i * step) for i in range(count)]


HARMONIES = {
    "complementary": complementary,
    "analogous": analogous,
    "triadic": triadic,
    "tetradic": tetradic,
    "split_complementary": split_complementary,
    "monochromatic": monochromatic,
}


def generate(base_color: str, harmony: str = "complementary") -> dict:
    """
    Generate a color palette from a base color.

    Args:
        base_color: hex string like "#FF5500" or "FF5500"
        harmony: complementary, analogous, triadic, tetradic, split_complementary, monochromatic

    Returns:
        dict with: base, base_hsl, palette (list of {hex, rgb, hsl})
    """
    rgb = parse_hex(base_color)
    func = HARMONIES.get(harmony)
    if not func:
        raise ValueError(f"Unknown harmony: {harmony}. Use one of: {list(HARMONIES.keys())}")

    colors = func(rgb)

    return {
        "base": to_hex(rgb),
        "base_rgb": rgb,
        "base_hsl": hsl(rgb),
        "harmony": harmony,
        "palette": [
            {
                "hex": to_hex(c),
                "rgb": c,
                "hsl": hsl(c),
                "css_rgb": to_rgb_string(c),
                "css_hsl": to_hsl_string(c),
            }
            for c in colors
        ],
    }


def to_css(palette: dict, format: str = "hex") -> str:
    """Format a palette as CSS custom properties."""
    lines = [f"/* {palette['harmony']} palette from {palette['base']} */"]
    for i, color in enumerate(palette["palette"]):
        var_name = f"--color-{i+1}"
        if format == "hex":
            value = color["hex"]
        elif format == "rgb":
            value = color["css_rgb"]
        elif format == "hsl":
            value = color["css_hsl"]
        else:
            value = color["hex"]
        lines.append(f"{var_name}: {value};")
    return "\n".join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="axiom-color-palette ")
    parser.add_argument("color", nargs="?", help="Base color (hex)")
    parser.add_argument("--harmony", default="complementary",
                        choices=list(HARMONIES.keys()),
                        help="Color harmony")
    parser.add_argument("--format", default="hex", choices=["hex", "rgb", "hsl", "css"], help="Output format")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    if not args.color:
        # Demo
        examples = [
            ("#FF5500", "complementary"),
            ("#3B82F6", "analogous"),
            ("#10B981", "triadic"),
            ("#8B5CF6", "monochromatic"),
        ]
        for color, harmony in examples:
            result = generate(color, harmony)
            print(f"\n{color} ({harmony}):")
            for c in result["palette"]:
                print(f"  {c['hex']}  {c['css_rgb']}  {c['css_hsl']}")
        return 0

    result = generate(args.color, args.harmony)
    if args.json or args.format == "json":
        import json
        print(json.dumps(result, indent=2))
    elif args.format == "css":
        print(to_css(result, "hex"))
    else:
        print(f"Base: {result['base']}  HSL: {result['base_hsl']}")
        print(f"Harmony: {result['harmony']}")
        for i, c in enumerate(result["palette"]):
            if args.format == "rgb":
                value = c["css_rgb"]
            elif args.format == "hsl":
                value = c["css_hsl"]
            else:
                value = c["hex"]
            print(f"  {i+1}. {value}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
