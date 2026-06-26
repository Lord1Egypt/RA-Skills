#!/usr/bin/env python3
"""
颜色转换工具
纯 Python 标准库实现，支持 HEX / RGB / HSL 互转
"""

import argparse
import re
import sys
import colorsys


def hex_to_rgb(hex_color: str) -> tuple:
    """HEX 颜色码转 RGB 元组"""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) not in (3, 6):
        raise ValueError(f"无效的 HEX 颜色码: #{hex_color}")
    
    if len(hex_color) == 3:
        hex_color = ''.join(c * 2 for c in hex_color)
    
    try:
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
    except ValueError:
        raise ValueError(f"无效的 HEX 颜色码: #{hex_color}")
    
    return (r, g, b)


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """RGB 转十六进制颜色码"""
    for val in (r, g, b):
        if not 0 <= val <= 255:
            raise ValueError(f"RGB 值必须在 0-255 之间，当前: {val}")
    return f"#{r:02X}{g:02X}{b:02X}"


def rgb_to_hsl(r: int, g: int, b: int) -> tuple:
    """RGB 转 HSL (H: 0-360, S: 0-100, L: 0-100)"""
    for val in (r, g, b):
        if not 0 <= val <= 255:
            raise ValueError(f"RGB 值必须在 0-255 之间，当前: {val}")
    
    # colorsys 使用 0-1 范围
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    return (round(h * 360), round(s * 100), round(l * 100))


def hsl_to_rgb(h: int, s: int, l: int) -> tuple:
    """HSL 转 RGB (H: 0-360, S: 0-100, L: 0-100)"""
    if not (0 <= h <= 360):
        raise ValueError(f"H 值必须在 0-360 之间，当前: {h}")
    if not (0 <= s <= 100):
        raise ValueError(f"S 值必须在 0-100 之间，当前: {s}")
    if not (0 <= l <= 100):
        raise ValueError(f"L 值必须在 0-100 之间，当前: {l}")
    
    # colorsys 使用 0-1 范围
    r, g, b = colorsys.hls_to_rgb(h / 360, l / 100, s / 100)
    return (round(r * 255), round(g * 255), round(b * 255))


def hex_to_hsl(hex_color: str) -> tuple:
    """一步到位 HEX 转 HSL"""
    r, g, b = hex_to_rgb(hex_color)
    return rgb_to_hsl(r, g, b)


def format_hsl(h: int, s: int, l: int) -> str:
    """格式化 HSL 字符串"""
    return f"hsl({h}, {s}%, {l}%)"


def main():
    parser = argparse.ArgumentParser(
        description='颜色转换工具 - HEX / RGB / HSL 互转',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  %(prog)s hex2rgb "#FF5733"           HEX 转 RGB
  %(prog)s rgb2hex 255 87 51           RGB 转 HEX
  %(prog)s rgb2hsl 255 87 51           RGB 转 HSL
  %(prog)s hsl2rgb 11 100 60           HSL 转 RGB
  %(prog)s hex2hsl "#FF5733"           HEX 转 HSL（一步到位）
  %(prog)s convert "#FF5733"           完整转换（显示所有格式）
        '''
    )

    subparsers = parser.add_subparsers(dest='command', help='子命令')

    p_hex2rgb = subparsers.add_parser('hex2rgb', help='HEX 转 RGB')
    p_hex2rgb.add_argument('hex', help='HEX 颜色码，如 #FF5733')

    p_rgb2hex = subparsers.add_parser('rgb2hex', help='RGB 转 HEX')
    p_rgb2hex.add_argument('r', type=int, help='红色 (0-255)')
    p_rgb2hex.add_argument('g', type=int, help='绿色 (0-255)')
    p_rgb2hex.add_argument('b', type=int, help='蓝色 (0-255)')

    p_rgb2hsl = subparsers.add_parser('rgb2hsl', help='RGB 转 HSL')
    p_rgb2hsl.add_argument('r', type=int, help='红色 (0-255)')
    p_rgb2hsl.add_argument('g', type=int, help='绿色 (0-255)')
    p_rgb2hsl.add_argument('b', type=int, help='蓝色 (0-255)')

    p_hsl2rgb = subparsers.add_parser('hsl2rgb', help='HSL 转 RGB')
    p_hsl2rgb.add_argument('h', type=int, help='色相 (0-360)')
    p_hsl2rgb.add_argument('s', type=int, help='饱和度 (0-100)')
    p_hsl2rgb.add_argument('l', type=int, help='亮度 (0-100)')

    p_hex2hsl = subparsers.add_parser('hex2hsl', help='HEX 转 HSL')
    p_hex2hsl.add_argument('hex', help='HEX 颜色码，如 #FF5733')

    p_convert = subparsers.add_parser('convert', help='完整转换（显示所有格式）')
    p_convert.add_argument('hex', help='HEX 颜色码，如 #FF5733')

    args = parser.parse_args()

    try:
        if args.command == 'hex2rgb':
            r, g, b = hex_to_rgb(args.hex)
            print(f"rgb({r}, {g}, {b})")

        elif args.command == 'rgb2hex':
            print(rgb_to_hex(args.r, args.g, args.b))

        elif args.command == 'rgb2hsl':
            h, s, l = rgb_to_hsl(args.r, args.g, args.b)
            print(format_hsl(h, s, l))

        elif args.command == 'hsl2rgb':
            r, g, b = hsl_to_rgb(args.h, args.s, args.l)
            print(f"rgb({r}, {g}, {b})")

        elif args.command == 'hex2hsl':
            h, s, l = hex_to_hsl(args.hex)
            print(format_hsl(h, s, l))

        elif args.command == 'convert':
            hex_color = args.hex
            r, g, b = hex_to_rgb(hex_color)
            h, s, l = rgb_to_hsl(r, g, b)
            print(f"HEX:  {hex_color}")
            print(f"RGB:  rgb({r}, {g}, {b})")
            print(f"HSL:  {format_hsl(h, s, l)}")

        else:
            parser.print_help()
            sys.exit(1)

    except ValueError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
