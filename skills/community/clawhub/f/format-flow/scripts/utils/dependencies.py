#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
依赖管理模块
自动检测和安装缺失的依赖
"""

import sys
import subprocess
from typing import List, Tuple, Dict


def check_and_install_dependencies() -> Tuple[bool, List[str]]:
    """
    检查并自动安装缺失的依赖
    
    Returns:
        (是否全部安装成功, 缺失的依赖列表)
    """
    # 核心依赖（必需）
    required = {
        'python-docx': 'docx',           # Word 文档处理
        'pdfplumber': 'pdfplumber',      # PDF 文本提取
        'Pillow': 'PIL',                 # 图片处理
        'tqdm': 'tqdm',                  # 进度条
        'requests': 'requests',          # HTTP 请求（网页抓取）
        'beautifulsoup4': 'bs4',         # HTML 解析
        'openpyxl': 'openpyxl',          # Excel 处理
    }
    
    # 可选依赖（按功能分组）
    optional = {
        # 文档转换
        'pypandoc': 'pypandoc',          # Markdown → Word（高质量）
        'docx2pdf': 'docx2pdf',          # Word → PDF（Windows + MS Word）
        
        # 数据处理
        'pandas': 'pandas',              # Excel 高级处理
        
        # 图片处理
        'imageio': 'imageio',            # 图片 IO
    }
    
    missing = []
    installed = []
    
    # 检查必需依赖
    for package, module in required.items():
        try:
            __import__(module)
        except ImportError:
            missing.append(package)
    
    # 自动安装缺失的必需依赖
    if missing:
        print(f"[INFO] 检测到缺失依赖: {', '.join(missing)}")
        for package in missing:
            try:
                print(f"[INFO] 正在安装 {package}...")
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", package],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                installed.append(package)
                print(f"[OK] {package} 安装成功")
            except subprocess.CalledProcessError:
                print(f"[ERROR] {package} 安装失败")
                return False, missing
    
    # 检查可选依赖（不自动安装）
    missing_optional = []
    for package, module in optional.items():
        try:
            __import__(module)
        except ImportError:
            missing_optional.append(package)
    
    if missing_optional:
        print(f"[INFO] 可选依赖未安装: {', '.join(missing_optional)}")
        print(f"[INFO] 某些高级功能可能受限")
    
    return True, []


def check_word_to_pdf_support() -> bool:
    """检查是否支持 Word 转 PDF"""
    try:
        import docx2pdf
        return True
    except ImportError:
        return False


def check_markdown_to_word_support() -> bool:
    """检查是否支持 Markdown 转 Word"""
    try:
        import pypandoc
        return True
    except ImportError:
        return False


def check_web_to_markdown_support() -> bool:
    """检查是否支持网页转 Markdown"""
    try:
        import requests
        from bs4 import BeautifulSoup
        return True
    except ImportError:
        return False


def check_excel_to_json_support() -> bool:
    """检查是否支持 Excel 转 JSON"""
    try:
        import openpyxl
        return True
    except ImportError:
        # 尝试 pandas 作为备选
        try:
            import pandas
            return True
        except ImportError:
            return False


def check_image_processing_support() -> bool:
    """检查是否支持图片处理"""
    try:
        from PIL import Image
        return True
    except ImportError:
        return False


def get_feature_availability() -> Dict[str, bool]:
    """
    获取所有功能的可用性状态
    
    Returns:
        功能可用性字典
    """
    return {
        'word_to_pdf': check_word_to_pdf_support(),
        'word_to_markdown': True,  # 始终可用（依赖已包含在必需依赖中）
        'pdf_to_markdown': True,   # 始终可用
        'markdown_to_word': check_markdown_to_word_support(),
        'web_to_markdown': check_web_to_markdown_support(),
        'text_formatter': True,    # 纯 Python，无需额外依赖
        'excel_to_json': check_excel_to_json_support(),
        'image_processor': check_image_processing_support(),
    }


def print_feature_status():
    """打印功能状态"""
    features = get_feature_availability()
    
    print("\n" + "="*60)
    print("功能可用性状态")
    print("="*60)
    
    feature_names = {
        'word_to_pdf': 'Word → PDF',
        'word_to_markdown': 'Word → Markdown',
        'pdf_to_markdown': 'PDF → Markdown',
        'markdown_to_word': 'Markdown → Word',
        'web_to_markdown': '网页 → Markdown',
        'text_formatter': '文本格式化',
        'excel_to_json': 'Excel → JSON',
        'image_processor': '图片处理',
    }
    
    for key, available in features.items():
        status = "[OK]" if available else "[X]"
        name = feature_names.get(key, key)
        print(f"{status} {name}")
    
    print("="*60)


if __name__ == '__main__':
    # 测试依赖检查
    success, missing = check_and_install_dependencies()
    
    if success:
        print("\n[SUCCESS] 所有必需依赖已安装")
        print_feature_status()
    else:
        print(f"\n[FAILED] 以下依赖安装失败: {', '.join(missing)}")
