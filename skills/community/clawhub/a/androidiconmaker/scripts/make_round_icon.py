#!/usr/bin/env python3
"""
将 JPG/PNG 图片裁剪为圆形，并生成适配 Android 各分辨率的 PNG 图标。

用法：
    python3 make_round_icon.py <图片路径> <输出目录> [基准尺寸]

示例：
    python3 make_round_icon.py /path/to/photo.jpg /path/to/output
    python3 make_round_icon.py /path/to/photo.jpg /path/to/output 48

生成文件（输出目录内）：
    icon_mdpi.png    (48x48)
    icon_hdpi.png    (72x72)
    icon_xhdpi.png   (96x96)
    icon_xxhdpi.png  (144x144)
    icon_xxxhdpi.png (192x192)
"""

import os
import sys
from PIL import Image, ImageDraw


def make_round_icon(input_path: str, output_dir: str = "android_icons", base_size: int = 48) -> list[str]:
    """
    将图片（JPG 或 PNG）转为 Android 圆形图标，输出各密度版本。

    :param input_path:  输入图片路径（JPG 或 PNG）
    :param output_dir: 输出目录
    :param base_size:  mdpi 基准尺寸（dp），默认 48
    :return:           生成的图标文件路径列表
    """
    img = Image.open(input_path).convert("RGBA")

    # 居中裁剪为正方形
    min_side = min(img.size)
    left = (img.width - min_side) // 2
    top = (img.height - min_side) // 2
    square_img = img.crop((left, top, left + min_side, top + min_side))

    # 圆形蒙版
    mask = Image.new("L", (min_side, min_side), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, min_side, min_side), fill=255)

    # 应用蒙版 → 圆形图
    round_img = Image.new("RGBA", (min_side, min_side), (0, 0, 0, 0))
    round_img.paste(square_img, (0, 0), mask=mask)

    # Android 密度映射（倍率基于 mdpi = 1x）
    densities = {
        "mdpi":    1,
        "hdpi":    1.5,
        "xhdpi":   2,
        "xxhdpi":  3,
        "xxxhdpi": 4,
    }

    os.makedirs(output_dir, exist_ok=True)
    generated = []

    for density, scale in densities.items():
        size = int(base_size * scale)
        resized = round_img.resize((size, size), Image.LANCZOS)
        filename = f"icon_{density}.png"
        filepath = os.path.join(output_dir, filename)
        resized.save(filepath, "PNG")
        generated.append(filepath)
        print(f"已生成: {filepath} ({size}x{size})")

    return generated


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 make_round_icon.py <图片路径> [输出目录] [基准尺寸]")
        sys.exit(1)

    input_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "android_icons"
    base_size  = int(sys.argv[3]) if len(sys.argv) > 3 else 48

    if not os.path.exists(input_path):
        print(f"错误: 文件不存在: {input_path}")
        sys.exit(1)

    print(f"输入: {input_path}")
    print(f"输出: {output_dir}")
    print(f"基准: {base_size}dp")
    print("---")
    make_round_icon(input_path, output_dir, base_size)
    print("完成!")
