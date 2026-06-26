#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
图片处理工具
支持压缩、格式转换、调整尺寸等
"""

import sys
import os
from pathlib import Path
from typing import Optional, List, Tuple

# 导入依赖
try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

# 导入工具函数
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import print_success, print_error, print_info


def compress_image(image_path: Path, output_path: Optional[Path] = None,
                   quality: int = 85, max_size: Optional[Tuple[int, int]] = None,
                   verbose: bool = True) -> bool:
    """
    压缩图片
    
    Args:
        image_path: 图片路径
        output_path: 输出路径（可选）
        quality: 压缩质量 (1-100)
        max_size: 最大尺寸 (宽, 高)
        verbose: 是否显示详细信息
    
    Returns:
        是否成功
    """
    if not HAS_PIL:
        if verbose:
            print_error("Pillow not installed. Install: pip install Pillow")
        return False
    
    if not image_path.exists():
        if verbose:
            print_error(f"File not found: {image_path}")
        return False
    
    try:
        if verbose:
            print_info(f"Processing: {image_path.name}")
        
        # 打开图片
        img = Image.open(image_path)
        original_size = image_path.stat().st_size
        
        # 调整尺寸
        if max_size:
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            if verbose:
                print_info(f"Resized to: {img.size[0]}x{img.size[1]}")
        
        # 确定输出路径
        if output_path is None:
            output_path = image_path.with_name(f"{image_path.stem}_compressed{image_path.suffix}")
        
        # 保存（根据格式选择参数）
        save_kwargs = {'quality': quality}
        
        if img.format == 'JPEG':
            save_kwargs['optimize'] = True
        elif img.format == 'PNG':
            save_kwargs['optimize'] = True
            # PNG 不支持 quality 参数
            del save_kwargs['quality']
        elif img.format == 'WEBP':
            save_kwargs['method'] = 4  # 压缩方法
        
        img.save(output_path, **save_kwargs)
        
        # 计算压缩比
        new_size = output_path.stat().st_size
        ratio = (1 - new_size / original_size) * 100
        
        if verbose:
            print_success(f"Created: {output_path}")
            print_info(f"Original: {original_size / 1024:.1f} KB")
            print_info(f"Compressed: {new_size / 1024:.1f} KB")
            print_info(f"Saved: {ratio:.1f}%")
        
        return True
    
    except Exception as e:
        if verbose:
            print_error(f"Compression failed: {e}")
        return False


def convert_image_format(image_path: Path, output_path: Optional[Path] = None,
                         target_format: str = 'PNG',
                         quality: int = 95,
                         verbose: bool = True) -> bool:
    """
    转换图片格式
    
    Args:
        image_path: 图片路径
        output_path: 输出路径（可选）
        target_format: 目标格式 ('PNG', 'JPEG', 'WEBP', 'GIF', 'BMP')
        quality: 质量（用于 JPEG/WEBP）
        verbose: 是否显示详细信息
    
    Returns:
        是否成功
    """
    if not HAS_PIL:
        if verbose:
            print_error("Pillow not installed. Install: pip install Pillow")
        return False
    
    if not image_path.exists():
        if verbose:
            print_error(f"File not found: {image_path}")
        return False
    
    try:
        if verbose:
            print_info(f"Converting: {image_path.name} -> {target_format}")
        
        # 打开图片
        img = Image.open(image_path)
        
        # 处理透明通道（JPEG 不支持透明）
        if target_format.upper() == 'JPEG' and img.mode in ('RGBA', 'LA', 'P'):
            # 创建白色背景
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
            img = background
        
        # 确定输出路径
        if output_path is None:
            output_path = image_path.with_suffix(f'.{target_format.lower()}')
        
        # 保存
        save_kwargs = {}
        if target_format.upper() in ['JPEG', 'WEBP']:
            save_kwargs['quality'] = quality
        elif target_format.upper() == 'PNG':
            save_kwargs['optimize'] = True
        
        img.save(output_path, format=target_format.upper(), **save_kwargs)
        
        if verbose:
            print_success(f"Created: {output_path}")
        
        return True
    
    except Exception as e:
        if verbose:
            print_error(f"Conversion failed: {e}")
        return False


def resize_image(image_path: Path, output_path: Optional[Path] = None,
                 size: Optional[Tuple[int, int]] = None,
                 scale: Optional[float] = None,
                 maintain_aspect: bool = True,
                 verbose: bool = True) -> bool:
    """
    调整图片尺寸
    
    Args:
        image_path: 图片路径
        output_path: 输出路径（可选）
        size: 目标尺寸 (宽, 高)
        scale: 缩放比例
        maintain_aspect: 是否保持宽高比
        verbose: 是否显示详细信息
    
    Returns:
        是否成功
    """
    if not HAS_PIL:
        if verbose:
            print_error("Pillow not installed. Install: pip install Pillow")
        return False
    
    if not image_path.exists():
        if verbose:
            print_error(f"File not found: {image_path}")
        return False
    
    try:
        if verbose:
            print_info(f"Resizing: {image_path.name}")
        
        # 打开图片
        img = Image.open(image_path)
        original_size = img.size
        
        # 计算新尺寸
        if scale:
            new_size = (int(original_size[0] * scale), int(original_size[1] * scale))
        elif size:
            if maintain_aspect:
                # 保持宽高比，适应目标尺寸
                img.thumbnail(size, Image.Resampling.LANCZOS)
                new_size = img.size
            else:
                new_size = size
        else:
            if verbose:
                print_error("Either size or scale must be specified")
            return False
        
        # 调整尺寸
        if not maintain_aspect or scale:
            img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        # 确定输出路径
        if output_path is None:
            output_path = image_path.with_name(f"{image_path.stem}_{new_size[0]}x{new_size[1]}{image_path.suffix}")
        
        # 保存
        img.save(output_path, quality=95)
        
        if verbose:
            print_success(f"Created: {output_path}")
            print_info(f"Original: {original_size[0]}x{original_size[1]}")
            print_info(f"New: {new_size[0]}x{new_size[1]}")
        
        return True
    
    except Exception as e:
        if verbose:
            print_error(f"Resize failed: {e}")
        return False


def rotate_image(image_path: Path, output_path: Optional[Path] = None,
                 angle: float = 90, verbose: bool = True) -> bool:
    """
    旋转图片
    
    Args:
        image_path: 图片路径
        output_path: 输出路径（可选）
        angle: 旋转角度（逆时针）
        verbose: 是否显示详细信息
    
    Returns:
        是否成功
    """
    if not HAS_PIL:
        if verbose:
            print_error("Pillow not installed. Install: pip install Pillow")
        return False
    
    try:
        img = Image.open(image_path)
        rotated = img.rotate(angle, expand=True)
        
        if output_path is None:
            output_path = image_path.with_name(f"{image_path.stem}_rotated{image_path.suffix}")
        
        rotated.save(output_path, quality=95)
        
        if verbose:
            print_success(f"Created: {output_path}")
            print_info(f"Rotated: {angle} degrees")
        
        return True
    
    except Exception as e:
        if verbose:
            print_error(f"Rotation failed: {e}")
        return False


def crop_image(image_path: Path, output_path: Optional[Path] = None,
               box: Tuple[int, int, int, int] = None,
               verbose: bool = True) -> bool:
    """
    裁剪图片
    
    Args:
        image_path: 图片路径
        output_path: 输出路径（可选）
        box: 裁剪区域 (left, top, right, bottom)
        verbose: 是否显示详细信息
    
    Returns:
        是否成功
    """
    if not HAS_PIL:
        if verbose:
            print_error("Pillow not installed. Install: pip install Pillow")
        return False
    
    try:
        img = Image.open(image_path)
        
        if box:
            cropped = img.crop(box)
        else:
            if verbose:
                print_error("Crop box must be specified")
            return False
        
        if output_path is None:
            output_path = image_path.with_name(f"{image_path.stem}_cropped{image_path.suffix}")
        
        cropped.save(output_path, quality=95)
        
        if verbose:
            print_success(f"Created: {output_path}")
            print_info(f"Cropped area: {box}")
        
        return True
    
    except Exception as e:
        if verbose:
            print_error(f"Crop failed: {e}")
        return False


def batch_compress_images(image_files: List[Path], quality: int = 85,
                          max_size: Optional[Tuple[int, int]] = None,
                          verbose: bool = True) -> dict:
    """
    批量压缩图片
    
    Args:
        image_files: 图片文件列表
        quality: 压缩质量
        max_size: 最大尺寸
        verbose: 是否显示详细信息
    
    Returns:
        处理结果统计
    """
    results = {'success': 0, 'failed': 0, 'total_saved': 0}
    
    for i, image_file in enumerate(image_files, 1):
        if verbose:
            print(f"\n[{i}/{len(image_files)}] {image_file.name}")
        
        # 获取原始大小
        original_size = image_file.stat().st_size
        
        success = compress_image(
            image_file,
            quality=quality,
            max_size=max_size,
            verbose=verbose
        )
        
        if success:
            results['success'] += 1
            # 计算节省的空间
            output_file = image_file.with_name(f"{image_file.stem}_compressed{image_file.suffix}")
            if output_file.exists():
                new_size = output_file.stat().st_size
                results['total_saved'] += (original_size - new_size)
        else:
            results['failed'] += 1
    
    if verbose:
        print(f"\n{'='*50}")
        print(f"Compression completed: {results['success']} success, {results['failed']} failed")
        if results['total_saved'] > 0:
            print(f"Total space saved: {results['total_saved'] / 1024 / 1024:.2f} MB")
    
    return results


def batch_convert_format(image_files: List[Path], target_format: str,
                         quality: int = 95, verbose: bool = True) -> dict:
    """
    批量转换图片格式
    
    Args:
        image_files: 图片文件列表
        target_format: 目标格式
        quality: 质量
        verbose: 是否显示详细信息
    
    Returns:
        处理结果统计
    """
    results = {'success': 0, 'failed': 0}
    
    for i, image_file in enumerate(image_files, 1):
        if verbose:
            print(f"\n[{i}/{len(image_files)}] {image_file.name}")
        
        success = convert_image_format(
            image_file,
            target_format=target_format,
            quality=quality,
            verbose=verbose
        )
        
        if success:
            results['success'] += 1
        else:
            results['failed'] += 1
    
    if verbose:
        print(f"\n{'='*50}")
        print(f"Conversion completed: {results['success']} success, {results['failed']} failed")
    
    return results
