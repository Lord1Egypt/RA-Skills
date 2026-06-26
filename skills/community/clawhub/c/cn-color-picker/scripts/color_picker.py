#!/usr/bin/env python3
import sys, json, re

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hsv(r, g, b):
    r, g, b = r/255, g/255, b/255
    mx, mn = max(r,g,b), min(r,g,b)
    h = s = v = mx
    d = mx - mn
    s = 0 if mx == 0 else d/mx
    if mx == mn: h = 0
    elif mx == r: h = (g-b)/d + (6 if g<b else 0)
    elif mx == g: h = (b-r)/d + 2
    else: h = (r-g)/d + 4
    h /= 6
    return int(h*360), int(s*100), int(v*100)

def convert_color(color):
    color = color.strip()
    if re.match(r'^#[0-9a-fA-F]{6}$', color):
        r, g, b = hex_to_rgb(color)
        h, s, v = rgb_to_hsv(r, g, b)
        return {'hex': color.upper(), 'rgb': f'rgb({r},{g},{b})', 'hsl': f'hsl({h},{s}%,{v}%)', 'hsv': f'hsv({h},{s}%,{v}%)'}
    return {'error': '无效颜色格式'}

if __name__ == '__main__':
    print(json.dumps(convert_color(sys.argv[1] if len(sys.argv)>1 else '#000000'), ensure_ascii=False))
