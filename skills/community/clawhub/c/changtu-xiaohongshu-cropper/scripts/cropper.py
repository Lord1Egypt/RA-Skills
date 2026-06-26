#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书长图切割工具 v1.0
功能：将飞书长图按 4:3 比例切割成小红书友好的图片，自动去除底部 Logo

作者：咖啡豆 [COFFEE]
日期：2026-03-20
"""

import argparse
import os
import sys
from pathlib import Path
from datetime import datetime
from PIL import Image, ImageDraw

# ============= 配置参数 =============
DEFAULT_WIDTH = 1080  # 小红书推荐宽度
DEFAULT_HEIGHT = 1440  # 3:4 比例高度（竖版）
DEFAULT_QUALITY = 95  # 图片质量
LOGO_HEIGHT = 160  # 底部 Logo 区域高度（像素，飞书固定值）


def calculate_crops(image_height, start_y=0, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT):
    """
    计算所有切割区域
    
    Args:
        image_height: 原图总高度
        start_y: 起始 Y 坐标（跳过顶部不需要的部分）
        width: 目标宽度
        height: 目标高度（4:3 比例）
    
    Returns:
        list of tuples: [(y_start, y_end), ...]
    """
    crops = []
    current_y = start_y
    
    while current_y < image_height:
        y_end = min(current_y + height, image_height)
        crops.append((current_y, y_end))
        current_y = y_end
        
        # 如果已经到最后，跳出循环
        if y_end >= image_height:
            break
    
    return crops


def fill_blank_space(image, target_height, fill_color=(255, 255, 255)):
    """
    如果图片高度不足，填充空白
    
    Args:
        image: PIL Image 对象
        target_height: 目标高度
        fill_color: 填充颜色（默认白色）
    
    Returns:
        PIL Image: 填充后的图片
    """
    width, height = image.size
    
    if height >= target_height:
        return image
    
    # 创建新画布
    new_image = Image.new('RGB', (width, target_height), fill_color)
    new_image.paste(image, (0, 0))
    
    return new_image


def remove_logo_simple(image, logo_height=LOGO_HEIGHT):
    """
    简单方法：直接裁剪掉底部 Logo 区域
    
    Args:
        image: PIL Image 对象
        Logo_height: Logo 区域高度
    
    Returns:
        PIL Image: 去除 Logo 后的图片
    """
    width, height = image.size
    
    if height <= logo_height:
        print("[WARN]  警告：图片高度小于 Logo 高度，跳过 Logo 去除")
        return image
    
    # 裁剪掉底部 Logo 区域
    cropped = image.crop((0, 0, width, height - logo_height))
    
    return cropped


def remove_logo_inpaint(image, logo_height=LOGO_HEIGHT):
    """
    高级方法：使用 OpenCV Inpaint 算法填充 Logo 区域
    （需要 OpenCV 支持，如果不可用则回退到简单裁剪）
    
    TODO: 后续版本实现
    """
    print("[WARN]  Inpaint 模式暂未实现，使用简单裁剪模式")
    return remove_logo_simple(image, logo_height)


def process_image(input_path, output_dir, start_y=0, width=DEFAULT_WIDTH, 
                  height=DEFAULT_HEIGHT, remove_logo=True, logo_height=LOGO_HEIGHT,
                  output_format='png'):
    """
    处理单张图片
    
    Args:
        input_path: 输入图片路径
        output_dir: 输出目录
        start_y: 起始 Y 坐标
        width: 目标宽度
        height: 目标高度
        remove_logo: 是否去除 Logo
        Logo_height: Logo 区域高度
        output_format: 输出格式（png/jpg）
    
    Returns:
        int: 生成的图片数量
    """
    # 打开图片
    try:
        img = Image.open(input_path)
    except Exception as e:
        print(f"[ERROR] 错误：无法打开图片 - {e}")
        return 0
    
    # 转换为 RGB 模式（处理 PNG 透明通道）
    if img.mode in ('RGBA', 'LA', 'P'):
        img = img.convert('RGB')
    
    original_width, original_height = img.size
    print(f"[INFO] 原图尺寸：{original_width} x {original_height} px")
    
    # 调整宽度（如果需要）
    if original_width != width:
        ratio = width / original_width
        new_height = int(original_height * ratio)
        img = img.resize((width, new_height), Image.Resampling.LANCZOS)
        print(f"[INFO] 调整后尺寸：{width} x {new_height} px")
        # 重要：更新 original_height 为调整后的高度
        original_height = new_height
    
    # 计算切割区域（使用调整后的尺寸）
    crops = calculate_crops(original_height, start_y, width, height)
    print(f"[CROP]  将切割成 {len(crops)} 张图片")
    
    # 创建输出目录
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 生成文件名前缀
    input_name = Path(input_path).stem
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_prefix = f"{input_name}_{timestamp}"
    
    # 开始切割
    count = 0
    for i, (y_start, y_end) in enumerate(crops, 1):
        # 切割图片
        cropped = img.crop((0, y_start, width, y_end))
        
        # 去除 Logo（如果是最后一张且启用了 Logo 去除）
        if remove_logo and i == len(crops):
            print(f"[CLEAN] 正在去除最后一张的 Logo...")
            cropped = remove_logo_simple(cropped, logo_height)
        
        # 填充空白（如果高度不足）
        current_width, current_height = cropped.size
        if current_height < height:
            print(f"[FILL] 最后一张高度不足，填充空白...")
            cropped = fill_blank_space(cropped, height)
        
        # 保存图片
        output_file = output_path / f"{file_prefix}_{i:02d}.{output_format}"
        
        if output_format.lower() == 'jpg' or output_format.lower() == 'jpeg':
            cropped.save(output_file, 'JPEG', quality=DEFAULT_QUALITY)
        else:
            cropped.save(output_file, 'PNG')
        
        count += 1
        print(f"[OK] 已保存：{output_file.name}")
    
    print(f"\n[DONE] 完成！共生成了 {count} 张图片")
    print(f"[DIR] 输出目录：{output_path.absolute()}")
    
    return count


def main():
    parser = argparse.ArgumentParser(
        description='飞书长图切割工具 v1.0 - 按 4:3 比例切割成小红书友好的图片',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例用法:
  # 基础用法（自动检测参数）
  python cropper.py input.png
  
  # 指定起始位置（跳过顶部 200px）
  python cropper.py input.png --start-y 200
  
  # 自定义尺寸和输出格式
  python cropper.py input.png --width 1440 --height 1080 --format jpg
  
  # 保留 Logo（不去除）
  python cropper.py input.png --keep-logo
  
  # 自定义 Logo 高度
  python cropper.py input.png --logo-height 150
        '''
    )
    
    parser.add_argument('input', help='输入图片路径')
    parser.add_argument('-o', '--output', default='./output', 
                        help='输出目录（默认：./output）')
    parser.add_argument('--start-y', type=int, default=0,
                        help='起始 Y 坐标，跳过顶部不需要的部分（默认：0）')
    parser.add_argument('--width', type=int, default=DEFAULT_WIDTH,
                        help=f'目标宽度（默认：{DEFAULT_WIDTH}px）')
    parser.add_argument('--height', type=int, default=DEFAULT_HEIGHT,
                        help=f'目标高度（默认：{DEFAULT_HEIGHT}px，4:3 比例）')
    parser.add_argument('--format', choices=['png', 'jpg', 'jpeg'], default='png',
                        help='输出格式（默认：png）')
    parser.add_argument('--keep-logo', action='store_true',
                        help='保留底部 Logo，不去除')
    parser.add_argument('--logo-height', type=int, default=LOGO_HEIGHT,
                        help=f'Logo 区域高度（默认：{LOGO_HEIGHT}px）')
    
    args = parser.parse_args()
    
    # 检查输入文件
    if not os.path.exists(args.input):
        print(f"[ERROR] 错误：文件不存在 - {args.input}")
        sys.exit(1)
    
    # 打印配置
    print("=" * 60)
    print("[COFFEE] 飞书长图切割工具 v1.0")
    print("=" * 60)
    print(f"[IN] 输入：{args.input}")
    print(f"[OUT] 输出：{args.output}")
    print(f"[INFO] 尺寸：{args.width} x {args.height} px")
    print(f"[TARGET] 起始 Y：{args.start_y} px")
    print(f"[CLEAN] 去除 Logo：{'否' if args.keep_logo else '是'}")
    if not args.keep_logo:
        print(f"   Logo 高度：{args.logo_height} px")
    print(f"[FILE] 格式：{args.format.upper()}")
    print("=" * 60)
    print()
    
    # 处理图片
    count = process_image(
        input_path=args.input,
        output_dir=args.output,
        start_y=args.start_y,
        width=args.width,
        height=args.height,
        remove_logo=not args.keep_logo,
        logo_height=args.logo_height,
        output_format=args.format
    )
    
    if count == 0:
        sys.exit(1)


if __name__ == '__main__':
    main()
