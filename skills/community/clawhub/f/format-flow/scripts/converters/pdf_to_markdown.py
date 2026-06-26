#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PDF 转 Markdown 转换器
提取文本内容（不支持图片）
"""

import sys
from pathlib import Path
from typing import Optional, List

# 导入依赖
try:
    import pdfplumber
except ImportError:
    pass

# 导入工具函数
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import print_success, print_error, print_info


def extract_text_with_layout(page) -> str:
    """
    从 PDF 页面提取文本，尽量保留布局
    
    Args:
        page: pdfplumber 页面对象
    
    Returns:
        提取的文本
    """
    text = page.extract_text()
    
    if not text:
        return ""
    
    # 清理多余的空白
    lines = text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        # 移除行首行尾空白
        line = line.strip()
        if line:
            cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)


def detect_heading(text: str) -> tuple:
    """
    检测文本是否为标题
    
    Args:
        text: 文本内容
    
    Returns:
        (是否为标题, 标题级别)
    """
    # 简单的启发式规则
    if not text:
        return False, 0
    
    # 检测常见的标题模式
    import re
    
    # 一级标题: 全大写或数字开头
    if re.match(r'^[A-Z\s]{3,}$', text):
        return True, 1
    
    # 编号标题: 1. 2. 等
    if re.match(r'^\d+\.\s+\S', text):
        return True, 2
    
    # 常见标题关键词
    heading_keywords = [
        '摘要', 'Abstract', '引言', 'Introduction',
        '方法', 'Method', '结果', 'Result',
        '讨论', 'Discussion', '结论', 'Conclusion',
        '参考文献', 'References', '致谢', 'Acknowledgement',
        '附录', 'Appendix', '目录', 'Contents'
    ]
    
    if any(keyword in text for keyword in heading_keywords):
        return True, 2
    
    return False, 0


def convert_pdf_to_markdown(pdf_path: Path, output_path: Optional[Path] = None,
                             verbose: bool = True) -> bool:
    """
    将 PDF 文档转换为 Markdown
    
    Args:
        pdf_path: PDF 文档路径
        output_path: 输出 Markdown 路径（可选）
        verbose: 是否显示详细信息
    
    Returns:
        是否转换成功
    """
    if not pdf_path.exists():
        if verbose:
            print_error(f"File not found: {pdf_path}")
        return False
    
    try:
        # 打开 PDF
        if verbose:
            print_info(f"Reading: {pdf_path.name}")
        
        md_content = []
        
        with pdfplumber.open(str(pdf_path)) as pdf:
            total_pages = len(pdf.pages)
            
            for i, page in enumerate(pdf.pages, 1):
                if verbose and i % 10 == 0:
                    print_info(f"Processing page {i}/{total_pages}...")
                
                # 提取文本
                text = extract_text_with_layout(page)
                
                if text:
                    # 检测标题
                    is_heading, level = detect_heading(text.split('\n')[0])
                    
                    if is_heading:
                        md_content.append(f"\n{'#' * level} {text}\n")
                    else:
                        md_content.append(f"\n{text}\n")
                
                # 添加分页符（可选）
                # md_content.append(f"\n---\n**Page {i}**\n")
        
        # 确定输出路径
        if output_path is None:
            output_path = pdf_path.with_suffix('.md')
        
        # 写入 Markdown 文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(''.join(md_content))
        
        if verbose:
            print_success(f"Created: {output_path}")
            print_info(f"Total pages: {total_pages}")
        
        return True
    
    except Exception as e:
        if verbose:
            print_error(f"Conversion failed: {e}")
        return False


def batch_convert_pdf_to_markdown(pdf_files: List[Path], 
                                    verbose: bool = True) -> dict:
    """
    批量转换 PDF 文档为 Markdown
    
    Args:
        pdf_files: PDF 文档路径列表
        verbose: 是否显示详细信息
    
    Returns:
        转换结果统计
    """
    results = {'success': 0, 'failed': 0}
    
    for i, pdf_file in enumerate(pdf_files, 1):
        if verbose:
            print(f"\n[{i}/{len(pdf_files)}] {pdf_file.name}")
        
        success = convert_pdf_to_markdown(pdf_file, verbose=verbose)
        
        if success:
            results['success'] += 1
        else:
            results['failed'] += 1
    
    if verbose:
        print(f"\n{'='*50}")
        print(f"Conversion completed: {results['success']} success, {results['failed']} failed")
    
    return results
