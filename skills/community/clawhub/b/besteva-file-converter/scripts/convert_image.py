#!/usr/bin/env python3
"""
Image Format Converter - 图片格式转换脚本
支持: PNG, JPG/JPEG, WebP, GIF, BMP, TIFF, ICO 等格式互转

依赖: pip install Pillow

用法:
  python convert_image.py <input_path> <output_format> [output_dir] [options]
  
示例:
  # 单文件转换
  python convert_image.py photo.png webp
  
  # 指定输出目录
  python convert_image.py photo.png jpg ./converted/
  
  # 批量转换目录下所有图片
  python convert_image.py ./images/ webp --batch
  
  # 带参数转换
  python convert_image.png photo.png jpg --quality 90 --resize 1920x1080
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Optional, List, Tuple

try:
    from PIL import Image, ImageOps
except ImportError:
    print("错误: 需要安装 Pillow 库")
    print("请执行: pip install Pillow")
    sys.exit(1)

# 支持的图片格式映射
FORMAT_MAP = {
    'png': 'PNG',
    'jpg': 'JPEG',
    'jpeg': 'JPEG',
    'webp': 'WEBP',
    'gif': 'GIF',
    'bmp': 'BMP',
    'tiff': 'TIFF',
    'tif': 'TIFF',
    'ico': 'ICO',
}

# 有损压缩格式
LOSSY_FORMATS = {'jpg', 'jpeg', 'webp'}


def parse_size(size_str: str) -> Optional[Tuple[int, int]]:
    """解析尺寸字符串，如 '1920x1080' 或 '50%' """
    if 'x' in size_str.lower():
        parts = size_str.lower().split('x')
        if len(parts) == 2:
            try:
                return int(parts[0]), int(parts[1])
            except ValueError:
                pass
    elif size_str.endswith('%'):
        try:
            return float(size_str[:-1]) / 100
        except ValueError:
            pass
    return None


def convert_single_image(
    input_path: str,
    output_format: str,
    output_dir: Optional[str] = None,
    quality: int = 85,
    resize: Optional[Tuple] = None,
    rotate: Optional[int] = None,
    grayscale: bool = False,
    optimize: bool = True,
    preserve_exif: bool = False,
    overwrite: bool = False,
) -> dict:
    """转换单张图片"""
    
    input_path = Path(input_path)
    if not input_path.exists():
        return {'success': False, 'error': f'输入文件不存在: {input_path}'}
    
    # 确定输出路径
    fmt_lower = output_format.lower()
    if fmt_lower not in FORMAT_MAP:
        return {'success': False, 'error': f'不支持的输出格式: {output_format}。支持: {", ".join(FORMAT_MAP.keys())}'}
    
    if output_dir:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    else:
        output_dir = input_path.parent
    
    output_filename = input_path.stem + '.' + fmt_lower
    output_path = output_dir / output_filename
    
    # 检查是否覆盖
    if output_path.exists() and not overwrite:
        return {
            'success': False,
            'error': f'输出文件已存在（使用 --overwrite 覆盖）: {output_path}',
            'output_path': str(output_path)
        }
    
    try:
        # 打开图片
        img = Image.open(input_path)
        
        # 处理透明通道（转换为有损格式时）
        if fmt_lower in LOSSY_FORMATS and img.mode in ('RGBA', 'LA', 'PA'):
            # 创建白色背景
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'RGBA':
                background.paste(img, mask=img.split()[3])
            else:
                background.paste(img)
            img = background
        
        # 自动旋转（根据EXIF信息）
        if preserve_exif or hasattr(img, '_getexif'):
            try:
                img = ImageOps.exif_transpose(img)
            except Exception:
                pass
        
        # 手动旋转
        if rotate:
            img = img.rotate(rotate, expand=True)
        
        # 缩放
        if resize:
            if isinstance(resize, tuple) and len(resize) == 2:
                if isinstance(resize[0], float):
                    # 百分比缩放
                    w, h = img.size
                    new_w, new_h = int(w * resize[0]), int(h * resize[0])
                    img = img.resize((new_w, new_h), Image.LANCZOS)
                else:
                    # 固定尺寸
                    img = img.resize(resize, Image.LANCZOS)
        
        # 灰度化
        if grayscale:
            img = img.convert('L')
        
        # 保存参数
        save_kwargs = {}
        if fmt_lower in ('jpg', 'jpeg'):
            save_kwargs['quality'] = quality
            save_kwargs['optimize'] = optimize
        elif fmt_lower == 'webp':
            save_kwargs['quality'] = quality
            save_kwargs['method'] = 6  # 更好的压缩
        elif fmt_lower == 'png':
            save_kwargs['optimize'] = optimize
            
        img.save(output_path, format=FORMAT_MAP[fmt_lower], **save_kwargs)
        
        # 获取文件大小信息
        input_size = input_path.stat().st_size
        output_size = output_path.stat().st_size
        
        return {
            'success': True,
            'input_path': str(input_path),
            'output_path': str(output_path),
            'input_size': input_size,
            'output_size': output_size,
            'compression_ratio': round((1 - output_size / input_size) * 100, 1) if input_size > 0 else 0,
            'dimensions': img.size,
            'format': fmt_lower.upper()
        }
        
    except Exception as e:
        return {'success': False, 'error': str(e)}


def batch_convert(
    input_dir: str,
    output_format: str,
    output_subdir: str = 'converted',
    **kwargs
) -> List[dict]:
    """批量转换目录下的所有图片"""
    
    input_dir = Path(input_dir)
    if not input_dir.is_dir():
        return [{'success': False, 'error': f'输入目录不存在: {input_dir}'}]
    
    # 支持的扩展名
    supported_exts = {'.png', '.jpg', '.jpeg', '.webp', '.gif', '.bmp', '.tiff', '.tif', '.ico'}
    
    # 收集所有图片
    image_files = []
    for ext in supported_exts:
        image_files.extend(input_dir.glob(f'*{ext}'))
        image_files.extend(input_dir.glob(f'*{ext.upper()}'))
    
    if not image_files:
        return [{'success': False, 'error': f'目录中没有找到支持的图片文件: {input_dir}'}]
    
    # 输出目录
    output_dir = input_dir / output_subdir
    
    results = []
    for i, img_path in enumerate(sorted(image_files)):
        print(f'[{"▓" * ((i+1)*20//len(image_files))}{"░" * (20-(i+1)*20//len(image_files))}] 转换中 ({i+1}/{len(image_files)}): {img_path.name}', end='\r')
        result = convert_single_image(str(img_path), output_format, str(output_dir), **kwargs)
        results.append(result)
    
    print()  # 换行
    return results


def get_image_info(image_path: str) -> dict:
    """获取图片详细信息"""
    path = Path(image_path)
    if not path.exists():
        return {'success': False, 'error': '文件不存在'}
    
    try:
        img = Image.open(path)
        stat = path.stat()
        return {
            'success': True,
            'filename': path.name,
            'format': img.format,
            'mode': img.mode,
            'size_pixels': img.size,
            'size_bytes': stat.st_stize,
            'size_human': _format_size(stat.st_stize),
            'modified': stat.st_mtime,
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}


def _format_size(size_bytes: int) -> str:
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f'{size_bytes:.1f} {unit}'
        size_bytes /= 1024
    return f'{size_bytes:.1f} TB'


def main():
    parser = argparse.ArgumentParser(
        description='图片格式转换工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  %(prog)s photo.png webp              # PNG 转 WebP
  %(prog)s photo.jpg png --quality 95   # JPG 转 PNG
  %(prog)s ./photos/ webp --batch       # 批量转换整个目录
  %(prog)s photo.png jpg --resize 800x600 --quality 75
  %(prog)s photo.png jpg --grayscale --rotate 90
'''
    )
    
    parser.add_argument('input', help='输入图片路径或目录')
    parser.add_argument('output_format', help='目标格式 (png/jpg/webp/gif/bmp/tiff/ico)')
    parser.add_argument('output_dir', nargs='?', help='输出目录（默认同输入目录）')
    
    parser.add_argument('--batch', '-b', action='store_true', help='批量模式：转换目录下所有图片')
    parser.add_argument('--quality', '-q', type=int, default=85, metavar='N', help='输出质量 (1-100)，默认85')
    parser.add_argument('--resize', '-r', metavar='WxH', help='调整尺寸，如 1920x1080 或 50%%')
    parser.add_argument('--rotate', metavar='DEGREES', type=int, help='旋转角度')
    parser.add_argument('--grayscale', '-g', action='store_true', help='转为灰度图')
    parser.add_argument('--no-optimize', action='store_true', help='禁用优化压缩')
    parser.add_argument('--overwrite', '-f', action='store_true', help='覆盖已存在的文件')
    parser.add_argument('--info', '-i', action='store_true', help='仅显示图片信息')
    
    args = parser.parse_args()
    
    # 仅显示信息
    if args.info:
        info = get_image_info(args.input)
        if info.get('success'):
            print(f"文件: {info['filename']}")
            print(f"格式: {info['format']} ({info['mode']})")
            print(f"尺寸: {info['size_pixels'][0]} x {info['size_pixels'][1]}")
            print(f"大小: {info['size_human']}")
        else:
            print(f"错误: {info.get('error')}")
        sys.exit(0)
    
    kwargs = {
        'quality': args.quality,
        'resize': parse_size(args.resize) if args.resize else None,
        'rotate': args.rotate,
        'grayscale': args.grayscale,
        'optimize': not args.no_optimize,
        'overwrite': args.overwrite,
    }
    
    # 批量模式
    if args.batch:
        results = batch_convert(
            args.input,
            args.output_format,
            output_subdir=args.output_dir or 'converted',
            **kwargs
        )
    else:
        results = [convert_single_image(
            args.input,
            args.output_format,
            args.output_dir,
            **kwargs
        )]
    
    # 输出结果
    success_count = sum(1 for r in results if r.get('success'))
    fail_count = len(results) - success_count
    
    print(f'\n{"="*50}')
    print(f'转换完成: {success_count} 成功, {fail_count} 失败')
    print('='*50)
    
    for r in results:
        if r.get('success'):
            print(f"✓ {Path(r['input_path']).name} → {Path(r['output_path']).name}")
            print(f"  尺寸: {r['dimensions'][0]}x{r['dimensions'][1]}")
            print(f"  大小: {_format_size(r['input_size'])} → {_format_size(r['output_size'])} (压缩 {r['compression_ratio']}%)")
        else:
            print(f"✗ 错误: {r.get('error')}")


if __name__ == '__main__':
    main()
