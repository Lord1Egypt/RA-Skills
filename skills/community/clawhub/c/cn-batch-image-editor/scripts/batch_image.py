#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量图片处理工具
支持：压缩、调尺寸、水印、格式转换、重命名
"""

import os
import sys
import argparse
from pathlib import Path
from datetime import datetime

try:
    from PIL import Image, ImageDraw, ImageFont, ImageEnhance
except ImportError:
    print("请先安装Pillow: pip install Pillow")
    sys.exit(1)

SUPPORTED_FORMATS = {'.png', '.jpg', '.jpeg', '.webp', '.gif', '.bmp'}


def get_image_files(input_dir: str) -> list:
    """获取目录下所有图片文件"""
    input_path = Path(input_dir)
    if not input_path.exists():
        print(f"错误：目录不存在 {input_dir}")
        return []

    files = []
    for f in input_path.iterdir():
        if f.is_file() and f.suffix.lower() in SUPPORTED_FORMATS:
            files.append(f)

    return sorted(files)


def ensure_output_dir(output_dir: str) -> Path:
    """确保输出目录存在"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    return output_path


def compress_image(img: Image.Image, quality: int = 85) -> Image.Image:
    """压缩图片"""
    # 转换为RGB模式（去掉alpha通道以支持JPEG）
    if img.mode in ('RGBA', 'P'):
        img = img.convert('RGB')
    return img


def resize_image(img: Image.Image, width: int = None, height: int = None, mode: str = 'scale') -> Image.Image:
    """调整图片尺寸

    Args:
        img: PIL图片对象
        width: 目标宽度
        height: 目标高度
        mode: scale(等比缩放) | crop(裁剪) | fill(填充)
    """
    orig_w, orig_h = img.size

    if not width and not height:
        return img

    # 计算目标尺寸
    if width and height:
        target_w, target_h = width, height
    elif width:
        ratio = width / orig_w
        target_w = width
        target_h = int(orig_h * ratio)
    else:  # height only
        ratio = height / orig_h
        target_w = int(orig_w * ratio)
        target_h = height

    if mode == 'scale':
        return img.resize((target_w, target_h), Image.Resampling.LANCZOS)

    elif mode == 'crop':
        # 居中裁剪
        left = (orig_w - target_w) // 2 if orig_w > target_w else 0
        top = (orig_h - target_h) // 2 if orig_h > target_h else 0
        right = min(orig_w, left + target_w)
        bottom = min(orig_h, top + target_h)
        img = img.crop((left, top, right, bottom))
        return img.resize((target_w, target_h), Image.Resampling.LANCZOS)

    elif mode == 'fill':
        # 填充背景
        new_img = Image.new('RGB', (target_w, target_h), (255, 255, 255))
        ratio = min(target_w / orig_w, target_h / orig_h)
        new_w = int(orig_w * ratio)
        new_h = int(orig_h * ratio)
        resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        offset_x = (target_w - new_w) // 2
        offset_y = (target_h - new_h) // 2
        new_img.paste(resized, (offset_x, offset_y))
        return new_img

    return img


def add_watermark(img: Image.Image, text: str = None, logo: str = None, position: str = 'bottom-right', opacity: float = 0.5) -> Image.Image:
    """添加水印

    Args:
        img: PIL图片对象
        text: 水印文字
        logo: 水印图片路径
        position: 位置 (top-left/top-right/bottom-left/bottom-right/center/tile)
        opacity: 透明度 (0-1)
    """
    # 确保有alpha通道
    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    watermark_layer = Image.new('RGBA', img.size, (0, 0, 0, 0))

    if logo:
        # 图片水印
        logo_img = Image.open(logo).convert('RGBA')
        # 缩放logo（不超过图片的1/4）
        max_size = min(img.size) // 4
        logo_w, logo_h = logo_img.size
        if max(logo_w, logo_h) > max_size:
            ratio = max_size / max(logo_w, logo_h)
            logo_img = logo_img.resize((int(logo_w * ratio), int(logo_h * ratio)), Image.Resampling.LANCZOS)

        logo_w, logo_h = logo_img.size
        pos = get_position(img.size, (logo_w, logo_h), position)

        # 应用透明度
        logo_with_opacity = Image.new('RGBA', logo_img.size, (0, 0, 0, 0))
        for x in range(logo_w):
            for y in range(logo_h):
                r, g, b, a = logo_img.getpixel((x, y))
                a = int(a * opacity)
                logo_with_opacity.putpixel((x, y), (r, g, b, a))

        watermark_layer.paste(logo_with_opacity, pos, logo_with_opacity)

    elif text:
        # 文字水印
        try:
            # 尝试使用系统字体
            font_size = max(img.size) // 20
            font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", font_size)
        except:
            font = ImageFont.load_default()

        draw = ImageDraw.Draw(watermark_layer)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]

        pos = get_position(img.size, (text_w, text_h), position)

        # 绘制文字（带透明度）
        alpha = int(255 * opacity)
        draw.text(pos, text, font=font, fill=(255, 255, 255, alpha))

    # 合并图层
    return Image.alpha_composite(img, watermark_layer)


def get_position(img_size: tuple, obj_size: tuple, position: str) -> tuple:
    """计算水印位置"""
    img_w, img_h = img_size
    obj_w, obj_h = obj_size
    margin = 20

    positions = {
        'top-left': (margin, margin),
        'top-right': (img_w - obj_w - margin, margin),
        'bottom-left': (margin, img_h - obj_h - margin),
        'bottom-right': (img_w - obj_w - margin, img_h - obj_h - margin),
        'center': ((img_w - obj_w) // 2, (img_h - obj_h) // 2),
    }

    return positions.get(position, positions['bottom-right'])


def convert_format(img: Image.Image, format: str, quality: int = 85) -> tuple:
    """转换格式，返回(图片, 保存参数)"""
    format = format.lower()
    save_kwargs = {}

    if format in ('jpg', 'jpeg'):
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
        save_kwargs['quality'] = quality
        save_kwargs['optimize'] = True
        ext = '.jpg'
    elif format == 'webp':
        save_kwargs['quality'] = quality
        ext = '.webp'
    elif format == 'png':
        save_kwargs['optimize'] = True
        ext = '.png'
    elif format == 'gif':
        ext = '.gif'
    else:
        ext = '.png'

    return img, ext, save_kwargs


def batch_compress(input_dir: str, output_dir: str = None, quality: int = 85):
    """批量压缩"""
    files = get_image_files(input_dir)
    if not files:
        print("未找到图片文件")
        return

    output_path = ensure_output_dir(output_dir or os.path.join(input_dir, 'output'))

    total_orig = 0
    total_new = 0

    print(f"处理 {len(files)} 张图片...")
    for i, f in enumerate(files, 1):
        img = Image.open(f)
        orig_size = os.path.getsize(f)
        total_orig += orig_size

        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')

        output_file = output_path / f"{f.stem}_compressed.jpg"
        img.save(output_file, 'JPEG', quality=quality, optimize=True)

        new_size = os.path.getsize(output_file)
        total_new += new_size

        print(f"  [{i}/{len(files)}] {f.name}: {orig_size/1024:.1f}KB → {new_size/1024:.1f}KB")

    ratio = (1 - total_new / total_orig) * 100 if total_orig > 0 else 0
    print(f"\n完成！总大小：{total_orig/1024/1024:.1f}MB → {total_new/1024/1024:.1f}MB（压缩{ratio:.0f}%）")


def batch_resize(input_dir: str, output_dir: str = None, width: int = None, height: int = None, mode: str = 'scale'):
    """批量调整尺寸"""
    files = get_image_files(input_dir)
    if not files:
        print("未找到图片文件")
        return

    output_path = ensure_output_dir(output_dir or os.path.join(input_dir, 'output'))

    print(f"处理 {len(files)} 张图片...")
    for i, f in enumerate(files, 1):
        img = Image.open(f)
        img = resize_image(img, width, height, mode)
        output_file = output_path / f.name
        img.save(output_file)
        print(f"  [{i}/{len(files)}] {f.name} → {img.size}")

    print(f"\n完成！输出到：{output_path}")


def batch_watermark(input_dir: str, output_dir: str = None, text: str = None, logo: str = None, position: str = 'bottom-right', opacity: float = 0.5):
    """批量添加水印"""
    if not text and not logo:
        print("错误：请指定 --text 或 --logo")
        return

    files = get_image_files(input_dir)
    if not files:
        print("未找到图片文件")
        return

    output_path = ensure_output_dir(output_dir or os.path.join(input_dir, 'output'))

    print(f"处理 {len(files)} 张图片...")
    for i, f in enumerate(files, 1):
        img = Image.open(f)
        img = add_watermark(img, text=text, logo=logo, position=position, opacity=opacity)
        output_file = output_path / f.name
        if img.mode == 'RGBA':
            img.save(output_file)
        else:
            img.save(output_file)
        print(f"  [{i}/{len(files)}] {f.name}")

    print(f"\n完成！输出到：{output_path}")


def batch_convert(input_dir: str, output_dir: str = None, format: str = 'jpg', quality: int = 85):
    """批量格式转换"""
    files = get_image_files(input_dir)
    if not files:
        print("未找到图片文件")
        return

    output_path = ensure_output_dir(output_dir or os.path.join(input_dir, 'output'))

    print(f"处理 {len(files)} 张图片...")
    for i, f in enumerate(files, 1):
        img = Image.open(f)
        img, ext, save_kwargs = convert_format(img, format, quality)
        output_file = output_path / (f.stem + ext)
        img.save(output_file, **save_kwargs)
        print(f"  [{i}/{len(files)}] {f.name} → {ext}")

    print(f"\n完成！输出到：{output_path}")


def batch_rename(input_dir: str, output_dir: str = None, prefix: str = '', start: int = 1, date_format: str = None):
    """批量重命名"""
    files = get_image_files(input_dir)
    if not files:
        print("未找到图片文件")
        return

    output_path = ensure_output_dir(output_dir or os.path.join(input_dir, 'renamed'))

    print(f"处理 {len(files)} 张图片...")
    for i, f in enumerate(files, 1):
        img = Image.open(f)

        if date_format:
            try:
                mtime = datetime.fromtimestamp(f.stat().st_mtime)
                new_name = mtime.strftime(date_format) + f.suffix
            except:
                new_name = f"{prefix}{start + i - 1:04d}{f.suffix}"
        else:
            new_name = f"{prefix}{start + i - 1:04d}{f.suffix}"

        output_file = output_path / new_name
        img.save(output_file)
        print(f"  [{i}/{len(files)}] {f.name} → {new_name}")

    print(f"\n完成！输出到：{output_path}")


def main():
    parser = argparse.ArgumentParser(description="批量图片处理工具")
    subparsers = parser.add_subparsers(dest='command', help='命令')

    # compress命令
    compress_parser = subparsers.add_parser('compress', help='批量压缩')
    compress_parser.add_argument('input', help='输入目录')
    compress_parser.add_argument('--output', '-o', help='输出目录')
    compress_parser.add_argument('--quality', '-q', type=int, default=85, help='压缩质量(1-100)')

    # resize命令
    resize_parser = subparsers.add_parser('resize', help='批量调整尺寸')
    resize_parser.add_argument('input', help='输入目录')
    resize_parser.add_argument('--output', '-o', help='输出目录')
    resize_parser.add_argument('--width', '-W', type=int, help='目标宽度')
    resize_parser.add_argument('--height', '-H', type=int, help='目标高度')
    resize_parser.add_argument('--mode', '-m', choices=['scale', 'crop', 'fill'], default='scale', help='调整模式')

    # watermark命令
    watermark_parser = subparsers.add_parser('watermark', help='批量添加水印')
    watermark_parser.add_argument('input', help='输入目录')
    watermark_parser.add_argument('--output', '-o', help='输出目录')
    watermark_parser.add_argument('--text', '-t', help='水印文字')
    watermark_parser.add_argument('--logo', '-l', help='水印图片路径')
    watermark_parser.add_argument('--position', '-p', default='bottom-right',
        choices=['top-left', 'top-right', 'bottom-left', 'bottom-right', 'center'],
        help='水印位置')
    watermark_parser.add_argument('--opacity', type=float, default=0.5, help='透明度(0-1)')

    # convert命令
    convert_parser = subparsers.add_parser('convert', help='批量格式转换')
    convert_parser.add_argument('input', help='输入目录')
    convert_parser.add_argument('--output', '-o', help='输出目录')
    convert_parser.add_argument('--format', '-f', default='jpg', choices=['png', 'jpg', 'webp', 'gif'], help='目标格式')
    convert_parser.add_argument('--quality', '-q', type=int, default=85, help='压缩质量')

    # rename命令
    rename_parser = subparsers.add_parser('rename', help='批量重命名')
    rename_parser.add_argument('input', help='输入目录')
    rename_parser.add_argument('--output', '-o', help='输出目录')
    rename_parser.add_argument('--prefix', default='', help='文件名前缀')
    rename_parser.add_argument('--start', type=int, default=1, help='起始序号')
    rename_parser.add_argument('--date-format', help='日期格式（如 %%Y%%m%%d_%%H%%M%%S）')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    if args.command == 'compress':
        batch_compress(args.input, args.output, args.quality)
    elif args.command == 'resize':
        batch_resize(args.input, args.output, args.width, args.height, args.mode)
    elif args.command == 'watermark':
        batch_watermark(args.input, args.output, args.text, args.logo, args.position, args.opacity)
    elif args.command == 'convert':
        batch_convert(args.input, args.output, args.format, args.quality)
    elif args.command == 'rename':
        batch_rename(args.input, args.output, args.prefix, args.start, args.date_format)


if __name__ == "__main__":
    main()
