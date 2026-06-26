#!/usr/bin/env python3

import argparse, json, sys, colorsys

def hsl_to_hex(h, s, l):
    r, g, b = colorsys.hls_to_rgb(h/360, l/100, s/100)
    return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", required=True, help="Base color (hex, e.g. #ff5733)")
    parser.add_argument("--format", choices=["hex","rgb"], default="hex")
    args = parser.parse_args()
    
    hex_color = args.base.strip("#")
    r, g, b = int(hex_color[0:2], 16)/255, int(hex_color[2:4], 16)/255, int(hex_color[4:6], 16)/255
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    h, s, l = h*360, s*100, l*100
    
    schemes = {
        "complementary": [h, (h+180)%360],
        "triadic": [h, (h+120)%360, (h+240)%360],
        "analogous": [h, (h-30)%360, (h+30)%360],
    }
    
    result = {}
    for name, angles in schemes.items():
        result[name] = [hsl_to_hex(a, s, l) for a in angles]
    
    print(json.dumps({"base": args.base, "schemes": result}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
