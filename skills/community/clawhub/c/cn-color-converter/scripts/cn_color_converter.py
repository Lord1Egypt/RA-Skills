#!/usr/bin/env python3
"""
cn-color-converter - 颜色格式转换器
支持HEX、RGB、RGBA、HSL、HSLA、CMYK格式转换
"""
import argparse
import re
import colorsys

def parse_color(color_str):
    """解析颜色字符串"""
    color_str = color_str.strip()
    
    # HEX格式
    if color_str.startswith('#'):
        hex_val = color_str[1:]
        if len(hex_val) == 3:
            hex_val = ''.join([c*2 for c in hex_val])
        if len(hex_val) == 6:
            r = int(hex_val[0:2], 16)
            g = int(hex_val[2:4], 16)
            b = int(hex_val[4:6], 16)
            return (r, g, b, 255)
        elif len(hex_val) == 8:
            r = int(hex_val[0:2], 16)
            g = int(hex_val[2:4], 16)
            b = int(hex_val[4:6], 16)
            a = int(hex_val[6:8], 16)
            return (r, g, b, a)
    
    # RGB/RGBA格式
    rgb_match = re.match(r'rgba?\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(?:,\s*([\d.]+))?\s*\)', color_str)
    if rgb_match:
        r, g, b = int(rgb_match.group(1)), int(rgb_match.group(2)), int(rgb_match.group(3))
        a = float(rgb_match.group(4)) * 255 if rgb_match.group(4) else 255
        return (r, g, b, int(a))
    
    # HSL/HSLA格式
    hsl_match = re.match(r'hsla?\s*\(\s*([\d.]+)\s*,\s*([\d.]+)%\s*,\s*([\d.]+)%\s*(?:,\s*([\d.]+))?\s*\)', color_str)
    if hsl_match:
        h = float(hsl_match.group(1)) / 360
        s = float(hsl_match.group(2)) / 100
        l = float(hsl_match.group(3)) / 100
        a = float(hsl_match.group(4)) if hsl_match.group(4) else 1
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        return (int(r*255), int(g*255), int(b*255), int(a*255))
    
    # 逗号分隔的RGB
    if ',' in color_str:
        parts = color_str.replace(' ', '').split(',')
        if len(parts) >= 3:
            try:
                r, g, b = int(parts[0]), int(parts[1]), int(parts[2])
                return (r, g, b, 255)
            except:
                pass
    
    return None

def rgb_to_hex(r, g, b, a=255):
    """RGB转HEX"""
    if a < 255:
        return f"#{r:02x}{g:02x}{b:02x}{a:02x}"
    return f"#{r:02x}{g:02x}{b:02x}"

def rgb_to_hsl(r, g, b):
    """RGB转HSL"""
    r, g, b = r/255, g/255, b/255
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return (int(h*360), int(s*100), int(l*100))

def rgb_to_cmyk(r, g, b):
    """RGB转CMYK"""
    if r == 0 and g == 0 and b == 0:
        return (0, 0, 0, 100)
    c = 1 - (r / 255)
    m = 1 - (g / 255)
    y = 1 - (b / 255)
    k = min(c, m, y)
    c = ((c - k) / (1 - k)) * 100 if k < 1 else 0
    m = ((m - k) / (1 - k)) * 100 if k < 1 else 0
    y = ((y - k) / (1 - k)) * 100 if k < 1 else 0
    return (int(c), int(m), int(y), int(k*100))

def generate_palette(base_color, count):
    """生成调色板"""
    r, g, b, a = parse_color(base_color) if isinstance(parse_color(base_color), tuple) else (128, 128, 128, 255)
    h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
    
    colors = []
    for i in range(count):
        # 调整亮度
        new_l = max(0.1, min(0.9, l + (i - count/2) * 0.15))
        nr, ng, nb = colorsys.hls_to_rgb(h, new_l, s)
        colors.append((int(nr*255), int(ng*255), int(nb*255)))
    return colors

def color_preview(r, g, b):
    """生成ASCII颜色预览"""
    # 使用ANSI颜色代码
    r_code = min(5, int(r / 51))
    g_code = min(5, int(g / 51))
    b_code = min(5, int(b / 51))
    
    # 前景色
    fg = f"\033[38;5;{16 + r_code*36 + g_code*6 + b_code}m"
    bg = f"\033[48;5;{16 + r_code*36 + g_code*6 + b_code}m"
    reset = "\033[0m"
    
    return f"{bg}{fg}  {reset}"

def main():
    parser = argparse.ArgumentParser(description='颜色格式转换器')
    parser.add_argument('color', nargs='?', help='输入颜色')
    parser.add_argument('--rgb', action='store_true', help='输出RGB')
    parser.add_argument('--hex', action='store_true', help='输出HEX')
    parser.add_argument('--hsl', action='store_true', help='输出HSL')
    parser.add_argument('--cmyk', action='store_true', help='输出CMYK')
    parser.add_argument('--preview', action='store_true', help='颜色预览')
    parser.add_argument('--palette', type=int, metavar='N', help='生成N色调色板')
    
    args = parser.parse_args()
    
    if not args.color:
        print("用法:")
        print("  python3 cn_color_converter.py '#FF5733'")
        print("  python3 cn_color_converter.py 'rgb(255,87,51)'")
        print("  python3 cn_color_converter.py '#3498db' --rgb --hsl")
        print("  python3 cn_color_converter.py '#E74C3C' --preview")
        print("  python3 cn_color_converter.py '#3498db' --palette 5")
        return
    
    # 解析颜色
    parsed = parse_color(args.color)
    if not parsed:
        print(f"无法解析颜色: {args.color}")
        return
    
    r, g, b, a = parsed
    
    # 调色板模式
    if args.palette:
        colors = generate_palette(args.color, args.palette)
        for i, (cr, cg, cb) in enumerate(colors):
            hex_code = rgb_to_hex(cr, cg, cb)
            print(f"{i+1}. {hex_code} rgb({cr},{cg},{cb})", end='')
            if args.preview:
                print(f" {color_preview(cr, cg, cb)}", end='')
            print()
        return
    
    # 预览模式
    if args.preview:
        print(f"{args.color} → ", end='')
    
    # 输出各格式
    outputs = []
    if args.rgb or (not args.hex and not args.hsl and not args.cmyk):
        if a < 255:
            outputs.append(f"rgba({r}, {g}, {b}, {a/255:.2f})")
        else:
            outputs.append(f"rgb({r}, {g}, {b})")
    
    if args.hex or (not args.rgb and not args.hsl and not args.cmyk):
        outputs.append(rgb_to_hex(r, g, b, a))
    
    if args.hsl:
        h, s, l = rgb_to_hsl(r, g, b)
        if a < 255:
            outputs.append(f"hsla({h}, {s}%, {l}%, {a/255:.2f})")
        else:
            outputs.append(f"hsl({h}, {s}%, {l}%)")
    
    if args.cmyk:
        c, m, y, k = rgb_to_cmyk(r, g, b)
        outputs.append(f"cmyk({c}%, {m}%, {y}%, {k}%)")
    
    for output in outputs:
        print(output)
    
    if args.preview:
        print(color_preview(r, g, b))

if __name__ == '__main__':
    main()