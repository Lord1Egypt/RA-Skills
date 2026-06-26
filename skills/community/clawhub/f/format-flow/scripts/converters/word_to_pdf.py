#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Word 转 PDF 转换器
使用 docx2pdf 或 LibreOffice 进行转换
"""

import sys
from pathlib import Path
from typing import Optional, List

# 导入工具函数
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import print_success, print_error, print_info, check_word_to_pdf_support


def convert_word_to_pdf(docx_path: Path, output_path: Optional[Path] = None,
                        verbose: bool = True) -> bool:
    """
    将 Word 文档转换为 PDF
    
    Args:
        docx_path: Word 文档路径
        output_path: 输出 PDF 路径（可选，默认同名）
        verbose: 是否显示详细信息
    
    Returns:
        是否转换成功
    """
    if not docx_path.exists():
        if verbose:
            print_error(f"File not found: {docx_path}")
        return False
    
    # 确定输出路径
    if output_path is None:
        output_path = docx_path.with_suffix('.pdf')
    
    # 方法1: 使用 docx2pdf (Windows + MS Word)
    if check_word_to_pdf_support():
        try:
            if verbose:
                print_info(f"Converting {docx_path.name} to PDF using docx2pdf...")
            
            from docx2pdf import convert
            convert(str(docx_path), str(output_path))
            
            if verbose:
                print_success(f"Converted: {output_path}")
            return True
        
        except Exception as e:
            if verbose:
                print_error(f"docx2pdf failed: {e}")
    
    # 方法2: 使用 LibreOffice (跨平台)
    try:
        if verbose:
            print_info(f"Trying LibreOffice conversion...")
        
        import subprocess
        cmd = [
            'soffice', '--headless', '--convert-to', 'pdf',
            str(docx_path),
            '--outdir', str(output_path.parent)
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        
        if verbose:
            print_success(f"Converted: {output_path}")
        return True
    
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        if verbose:
            print_error(f"LibreOffice conversion failed: {e}")
    
    # 方法3: 使用 pypandoc (跨平台，质量较低)
    try:
        if verbose:
            print_info(f"Trying pypandoc conversion...")
        
        import pypandoc
        pypandoc.convert_file(
            str(docx_path), 'pdf',
            outputfile=str(pdf_path)
        )
        
        if verbose:
            print_success(f"Converted: {pdf_path}")
        return True
    
    except Exception as e:
        if verbose:
            print_error(f"pypandoc conversion failed: {e}")
    
    if verbose:
        print_error("All conversion methods failed")
        print_info("Please install one of: docx2pdf, LibreOffice, or pypandoc")
    
    return False


def batch_convert_word_to_pdf(docx_files: List[Path], verbose: bool = True) -> dict:
    """
    批量转换 Word 文档为 PDF
    
    Args:
        docx_files: Word 文档路径列表
        verbose: 是否显示详细信息
    
    Returns:
        转换结果统计 {'success': n, 'failed': n}
    """
    results = {'success': 0, 'failed': 0}
    
    for i, docx_file in enumerate(docx_files, 1):
        if verbose:
            print(f"\n[{i}/{len(docx_files)}] {docx_file.name}")
        
        success = convert_word_to_pdf(docx_file, verbose=verbose)
        
        if success:
            results['success'] += 1
        else:
            results['failed'] += 1
    
    if verbose:
        print(f"\n{'='*50}")
        print(f"Conversion completed: {results['success']} success, {results['failed']} failed")
    
    return results
