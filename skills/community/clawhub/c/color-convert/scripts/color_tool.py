#!/usr/bin/env python3
"""Color Toolkit - Convert, palette, contrast. Zero dependencies."""

import math
import colorsys
import random
import sys
import re
import argparse

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'

def rgb_to_hsl(r, g, b):
    r, g, b = r/255, g/255, b/255
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return (round(h*360, 1), round(s*100, 1), round(l*100, 1))

def hsl_to_rgb(h, s, l):
    h, s, l = h/360, s/100, l/100
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return (round(r*255), round(g*255), round(b*255))

def rgb_to_hsv(r, g, b):
    r, g, b = r/255, g/255, b/255
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    return (round(h*360, 1), round(s*100, 1), round(v*100, 1))

def rgb_to_cmyk(r, g, b):
    if r == g == b == 0:
        return (0, 0, 0, 100)
    c = 1 - r/255; m = 1 - g/255; y = 1 - b/255
    k = min(c, m, y)
    c = (c-k)/(1-k)*100; m = (m-k)/(1-k)*100; y = (y-k)/(1-k)*100
    return (round(c), round(m), round(y), round(k*100))

def parse_color(text):
    text = text.strip()
    if text.startswith('#'):
        return hex_to_rgb(text)
    m = re.match(r'rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)', text)
    if m:
        return (int(m.group(1)), int(m.group(2)), int(m.group(3)))
    m = re.match(r'hsl\(\s*(\d+)\s*,\s*(\d+)%?\s*,\s*(\d+)%?\s*\)', text)
    if m:
        return hsl_to_rgb(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    return None

def relative_luminance(r, g, b):
    def linearize(c):
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * linearize(r) + 0.7152 * linearize(g) + 0.0722 * linearize(b)

def contrast_ratio(rgb1, rgb2):
    l1 = relative_luminance(*rgb1)
    l2 = relative_luminance(*rgb2)
    lighter = max(l1, l2); darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)

def palette_complementary(h, s, l):
    return [(h, s, l), ((h + 180) % 360, s, l)]

def palette_analogous(h, s, l):
    return [(h, s, l), ((h + 30) % 360, s, l), ((h - 30) % 360, s, l)]

def palette_triadic(h, s, l):
    return [(h, s, l), ((h + 120) % 360, s, l), ((h + 240) % 360, s, l)]

def palette_split_complementary(h, s, l):
    return [(h, s, l), ((h + 150) % 360, s, l), ((h + 210) % 360, s, l)]

def palette_shades(h, s, l, count=5):
    result = []
    for i in range(count):
        new_l = max(5, l - (l - 5) * i / (count - 1))
        result.append((h, s, round(new_l)))
    return result

def palette_tints(h, s, l, count=5):
    result = []
    for i in range(count):
        new_l = min(95, l + (95 - l) * i / (count - 1))
        result.append((h, s, round(new_l)))
    return result

def main():
    parser = argparse.ArgumentParser(description='Color Toolkit')
    sub = parser.add_subparsers(dest='command')
    
    p = sub.add_parser('convert', help='Convert color')
    p.add_argument('color'); p.add_argument('-t', '--to', choices=['hex', 'rgb', 'hsl', 'hsv', 'cmyk'], default='hex')
    
    p = sub.add_parser('palette', help='Generate palette')
    p.add_argument('color'); p.add_argument('-t', '--type', choices=['complementary', 'analogous', 'triadic', 'split', 'shades', 'tints'], default='complementary')
    p.add_argument('-n', '--count', type=int, default=5)
    
    p = sub.add_parser('contrast', help='WCAG contrast ratio')
    p.add_argument('color1'); p.add_argument('color2')
    
    p = sub.add_parser('random', help='Random palette')
    p.add_argument('-n', '--count', type=int, default=5)
    
    args = parser.parse_args()
    
    if args.command == 'convert':
        rgb = parse_color(args.color)
        if not rgb:
            print("Could not parse color"); return
        r, g, b = rgb
        if args.to == 'hex':
            print(rgb_to_hex(r, g, b))
        elif args.to == 'rgb':
            print(f"rgb({r}, {g}, {b})")
        elif args.to == 'hsl':
            h, s, l = rgb_to_hsl(r, g, b)
            print(f"hsl({h}, {s}%, {l}%)")
        elif args.to == 'hsv':
            h, s, v = rgb_to_hsv(r, g, b)
            print(f"hsv({h}, {s}%, {v}%)")
        elif args.to == 'cmyk':
            c, m, y, k = rgb_to_cmyk(r, g, b)
            print(f"cmyk({c}%, {m}%, {y}%, {k}%)")
    
    elif args.command == 'palette':
        rgb = parse_color(args.color)
        if not rgb:
            print("Could not parse color"); return
        h, s, l = rgb_to_hsl(*rgb)
        funcs = {'complementary': palette_complementary, 'analogous': palette_analogous,
                 'triadic': palette_triadic, 'split': palette_split_complementary,
                 'shades': lambda h,s,l: palette_shades(h,s,l,args.count),
                 'tints': lambda h,s,l: palette_tints(h,s,l,args.count)}
        colors = funcs[args.type](h, s, l)
        for ch, cs, cl in colors:
            cr, cg, cb = hsl_to_rgb(ch, cs, cl)
            print(f"{rgb_to_hex(cr, cg, cb)}  rgb({cr}, {cg}, {cb})  hsl({ch}, {cs}%, {cl}%)")
    
    elif args.command == 'contrast':
        rgb1 = parse_color(args.color1)
        rgb2 = parse_color(args.color2)
        if not rgb1 or not rgb2:
            print("Could not parse colors"); return
        ratio = contrast_ratio(rgb1, rgb2)
        print(f"Contrast ratio: {ratio:.2f}:1")
        print(f"AA normal text: {'✅ PASS' if ratio >= 4.5 else '❌ FAIL'}")
        print(f"AA large text: {'✅ PASS' if ratio >= 3 else '❌ FAIL'}")
        print(f"AAA normal text: {'✅ PASS' if ratio >= 7 else '❌ FAIL'}")
        print(f"AAA large text: {'✅ PASS' if ratio >= 4.5 else '❌ FAIL'}")
    
    elif args.command == 'random':
        base_h = random.uniform(0, 360)
        for i in range(args.count):
            h = (base_h + i * 360 / args.count) % 360
            s = random.randint(50, 90)
            l = random.randint(35, 65)
            r, g, b = hsl_to_rgb(h, s, l)
            print(f"{rgb_to_hex(r, g, b)}  hsl({h:.0f}, {s}%, {l}%)")
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
