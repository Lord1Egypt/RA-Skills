#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
通用辅助函数
文件操作、路径处理、输出格式化等
"""

import os
import shutil
from pathlib import Path
from typing import Optional, List, Tuple


def ensure_output_path(input_path: Path, output_path: Optional[Path], 
                       suffix: str, output_dir: Optional[Path] = None) -> Path:
    """
    确定输出文件路径
    
    Args:
        input_path: 输入文件路径
        output_path: 用户指定的输出路径（可选）
        suffix: 输出文件后缀（如 .pdf, .md）
        output_dir: 输出目录（可选）
    
    Returns:
        输出文件的完整路径
    """
    if output_path:
        return output_path
    
    if output_dir:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        return output_dir / (input_path.stem + suffix)
    
    return input_path.parent / (input_path.stem + suffix)


def create_image_folder(markdown_path: Path) -> Path:
    """
    创建图片存储文件夹
    
    Args:
        markdown_path: Markdown 文件路径
    
    Returns:
        图片文件夹路径
    """
    image_folder = markdown_path.parent / f"{markdown_path.stem}_images"
    image_folder.mkdir(parents=True, exist_ok=True)
    return image_folder


def get_file_list(input_path: Path, extensions: List[str], 
                  recursive: bool = False) -> List[Path]:
    """
    获取文件列表
    
    Args:
        input_path: 输入路径（文件或目录）
        extensions: 文件扩展名列表（如 ['.docx', '.doc']）
        recursive: 是否递归搜索子目录
    
    Returns:
        文件路径列表
    """
    input_path = Path(input_path)
    
    if input_path.is_file():
        if input_path.suffix.lower() in extensions:
            return [input_path]
        return []
    
    if not input_path.is_dir():
        return []
    
    files = []
    if recursive:
        for ext in extensions:
            files.extend(input_path.rglob(f"*{ext}"))
    else:
        for ext in extensions:
            files.extend(input_path.glob(f"*{ext}"))
    
    return sorted(files)


def print_progress(current: int, total: int, filename: str):
    """打印进度信息"""
    print(f"[{current}/{total}] Processing: {filename}")


def print_success(message: str):
    """打印成功信息"""
    print(f"[OK] {message}")


def print_error(message: str):
    """打印错误信息"""
    print(f"[ERROR] {message}")


def print_info(message: str):
    """打印提示信息"""
    print(f"[INFO] {message}")


def print_warning(message: str):
    """打印警告信息"""
    print(f"[WARN] {message}")
