#!/usr/bin/env python3
"""
图片背景处理工具 - 支持去除背景、替换背景、背景模糊
依赖: rembg, Pillow
"""
import argparse
import sys
import os

def check_dependencies():
    """检查并提示缺失的依赖"""
    missing = []
    try:
        import rembg
    except ImportError:
        missing.append("rembg")
    try:
        from PIL import Image
    except ImportError:
        missing.append("Pillow")
    if missing:
        print(f"缺少依赖: {', '.join(missing)}", file=sys.stderr)
        print(f"请运行: pip install {' '.join(missing)}", file=sys.stderr)
        sys.exit(1)

def remove_bg(input_path, output_path, model="u2net"):
    """去除背景，输出透明PNG"""
    from rembg import remove
    from PIL import Image

    img = Image.open(input_path)
    result = remove(img, alpha_matting=True, alpha_matting_foreground_threshold=240, alpha_matting_background_threshold=10)
    result.save(output_path, "PNG")
    print(f"✅ 背景已去除 → {output_path}")

def replace_bg(input_path, output_path, bg_color=None, bg_image=None, model="u2net"):
    """去除背景后替换为指定颜色或图片"""
    from rembg import remove
    from PIL import Image

    img = Image.open(input_path)
    # 抠图
    fg = remove(img, alpha_matting=True, alpha_matting_foreground_threshold=240, alpha_matting_background_threshold=10)

    if bg_image:
        # 用图片做背景
        bg = Image.open(bg_image).convert("RGBA")
        bg = bg.resize(fg.size, Image.LANCZOS)
    elif bg_color:
        # 用纯色做背景
        color = parse_color(bg_color)
        bg = Image.new("RGBA", fg.size, color)
    else:
        # 默认白色背景
        bg = Image.new("RGBA", fg.size, (255, 255, 255, 255))

    # 合成
    result = Image.alpha_composite(bg, fg)
    result.save(output_path, "PNG")
    print(f"✅ 背景已替换 → {output_path}")

def blur_bg(input_path, output_path, radius=15, model="u2net"):
    """保留前景主体，背景高斯模糊"""
    from rembg import remove
    from PIL import Image, ImageFilter
    import numpy as np

    img = Image.open(input_path).convert("RGBA")
    # 获取前景蒙版
    fg = remove(img, only_mask=True)

    # 模糊原图作为背景
    blurred = img.filter(ImageFilter.GaussianBlur(radius=radius))

    # 用蒙版合成：前景清晰 + 背景模糊
    mask = fg.convert("L")
    result = Image.composite(img, blurred, mask)
    result.save(output_path, "PNG")
    print(f"✅ 背景已模糊(radius={radius}) → {output_path}")

def parse_color(color_str):
    """解析颜色字符串，支持 hex (#FF0000) 和 rgb (255,0,0) 格式"""
    color_str = color_str.strip()
    if color_str.startswith("#"):
        hex_str = color_str.lstrip("#")
        if len(hex_str) == 6:
            r, g, b = int(hex_str[0:2], 16), int(hex_str[2:4], 16), int(hex_str[4:6], 16)
            return (r, g, b, 255)
        elif len(hex_str) == 8:
            r, g, b, a = int(hex_str[0:2], 16), int(hex_str[2:4], 16), int(hex_str[4:6], 16), int(hex_str[6:8], 16)
            return (r, g, b, a)
    elif "," in color_str:
        parts = [int(x.strip()) for x in color_str.split(",")]
        if len(parts) == 3:
            return (parts[0], parts[1], parts[2], 255)
        elif len(parts) == 4:
            return tuple(parts)

    # 预设颜色名称
    colors = {
        "white": (255, 255, 255, 255),
        "black": (0, 0, 0, 255),
        "red": (255, 0, 0, 255),
        "green": (0, 255, 0, 255),
        "blue": (0, 0, 255, 255),
        "transparent": (0, 0, 0, 0),
    }
    if color_str.lower() in colors:
        return colors[color_str.lower()]

    print(f"⚠️ 无法解析颜色 '{color_str}'，使用白色", file=sys.stderr)
    return (255, 255, 255, 255)

def main():
    parser = argparse.ArgumentParser(description="图片背景处理工具")
    subparsers = parser.add_subparsers(dest="command", help="操作类型")

    # 去除背景
    rm_parser = subparsers.add_parser("remove", help="去除背景（输出透明PNG）")
    rm_parser.add_argument("input", help="输入图片路径")
    rm_parser.add_argument("-o", "--output", help="输出路径（默认: input_nobg.png）")

    # 替换背景
    rp_parser = subparsers.add_parser("replace", help="替换背景")
    rp_parser.add_argument("input", help="输入图片路径")
    rp_parser.add_argument("-o", "--output", help="输出路径")
    rp_parser.add_argument("-c", "--color", help="背景颜色（#FF0000 / 255,0,0 / red）")
    rp_parser.add_argument("-i", "--bg-image", help="背景图片路径")

    # 背景模糊
    bl_parser = subparsers.add_parser("blur", help="背景模糊（人像模式）")
    bl_parser.add_argument("input", help="输入图片路径")
    bl_parser.add_argument("-o", "--output", help="输出路径")
    bl_parser.add_argument("-r", "--radius", type=int, default=15, help="模糊半径（默认15）")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # 自动生成输出路径
    if not args.output:
        base, ext = os.path.splitext(args.input)
        suffix = {"remove": "_nobg", "replace": "_newbg", "blur": "_blur"}
        args.output = f"{base}{suffix[args.command]}.png"

    check_dependencies()

    if args.command == "remove":
        remove_bg(args.input, args.output)
    elif args.command == "replace":
        replace_bg(args.input, args.output, bg_color=args.color, bg_image=args.bg_image)
    elif args.command == "blur":
        blur_bg(args.input, args.output, radius=args.radius)

if __name__ == "__main__":
    main()
