#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
纯文本笔记格式化工具
支持多种格式化规则
"""

import sys
import re
from pathlib import Path
from typing import Optional, List, Dict
from datetime import datetime

# 导入工具函数
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import print_success, print_error, print_info


def normalize_whitespace(text: str) -> str:
    """
    规范化空白字符
    
    Args:
        text: 原始文本
    
    Returns:
        规范化后的文本
    """
    # 移除行尾空白
    lines = [line.rstrip() for line in text.split('\n')]
    
    # 移除多余空行（保留段落间的空行）
    normalized_lines = []
    prev_empty = False
    
    for line in lines:
        is_empty = not line.strip()
        
        # 如果当前行和上一行都为空，跳过当前行
        if is_empty and prev_empty:
            continue
        
        normalized_lines.append(line)
        prev_empty = is_empty
    
    return '\n'.join(normalized_lines)


def format_paragraphs(text: str, indent: str = "  ") -> str:
    """
    格式化段落（添加首行缩进）
    
    Args:
        text: 原始文本
        indent: 缩进字符串
    
    Returns:
        格式化后的文本
    """
    lines = text.split('\n')
    formatted_lines = []
    
    for line in lines:
        stripped = line.strip()
        
        # 如果是空行或特殊行（标题、列表等），不缩进
        if (not stripped or 
            stripped.startswith(('#', '*', '-', '>', '```', '1.', '2.', '3.')) or
            re.match(r'^\d+\.', stripped)):
            formatted_lines.append(line)
        else:
            # 普通段落，添加缩进
            formatted_lines.append(indent + stripped)
    
    return '\n'.join(formatted_lines)


def format_titles(text: str, style: str = 'markdown') -> str:
    """
    格式化标题
    
    Args:
        text: 原始文本
        style: 标题风格 ('markdown', 'underline', 'numbered')
    
    Returns:
        格式化后的文本
    """
    lines = text.split('\n')
    formatted_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # 检测可能的标题（全大写、短行、后面跟空行）
        is_heading = False
        
        # Markdown 风格
        if line.strip().startswith('#'):
            formatted_lines.append(line)
            is_heading = True
        
        # 检测全大写或首字母大写的短行
        elif (len(line.strip()) < 50 and 
              line.strip() and 
              (line.strip().isupper() or line.strip().istitle())):
            
            # 检查下一行是否为空
            if i + 1 < len(lines) and not lines[i + 1].strip():
                is_heading = True
                
                if style == 'markdown':
                    formatted_lines.append(f"## {line.strip()}")
                elif style == 'underline':
                    formatted_lines.append(line.strip())
                    formatted_lines.append('=' * len(line.strip()))
                elif style == 'numbered':
                    formatted_lines.append(f"## {line.strip()}")
        
        if not is_heading:
            formatted_lines.append(line)
        
        i += 1
    
    return '\n'.join(formatted_lines)


def format_lists(text: str) -> str:
    """
    格式化列表
    
    Args:
        text: 原始文本
    
    Returns:
        格式化后的文本
    """
    lines = text.split('\n')
    formatted_lines = []
    
    list_pattern = re.compile(r'^(\s*)([-*+]|\d+\.)\s+')
    in_list = False
    list_indent = ""
    
    for line in lines:
        match = list_pattern.match(line)
        
        if match:
            in_list = True
            list_indent = match.group(1)
            formatted_lines.append(line)
        elif in_list and line.strip():
            # 列表项的续行
            if line.startswith(list_indent + '  '):
                formatted_lines.append(line)
            else:
                in_list = False
                formatted_lines.append(line)
        else:
            in_list = False
            formatted_lines.append(line)
    
    return '\n'.join(formatted_lines)


def add_line_numbers(text: str) -> str:
    """
    添加行号
    
    Args:
        text: 原始文本
    
    Returns:
        带行号的文本
    """
    lines = text.split('\n')
    max_num = len(lines)
    width = len(str(max_num))
    
    numbered_lines = []
    for i, line in enumerate(lines, 1):
        numbered_lines.append(f"{i:>{width}} | {line}")
    
    return '\n'.join(numbered_lines)


def extract_outline(text: str) -> str:
    """
    提取文档大纲
    
    Args:
        text: 原始文本
    
    Returns:
        大纲文本
    """
    lines = text.split('\n')
    outline_lines = []
    
    heading_pattern = re.compile(r'^(#{1,6})\s+(.+)$')
    
    for line in lines:
        match = heading_pattern.match(line)
        if match:
            level = len(match.group(1))
            title = match.group(2)
            indent = "  " * (level - 1)
            outline_lines.append(f"{indent}- {title}")
    
    if not outline_lines:
        outline_lines.append("No headings found")
    
    return '\n'.join(outline_lines)


def generate_toc(text: str) -> str:
    """
    生成目录
    
    Args:
        text: 原始文本
    
    Returns:
        目录文本
    """
    lines = text.split('\n')
    toc_lines = ["## 目录\n"]
    
    heading_pattern = re.compile(r'^(#{1,6})\s+(.+)$')
    counters = [0] * 6  # 6 级标题计数器
    
    for line in lines:
        match = heading_pattern.match(line)
        if match:
            level = len(match.group(1))
            title = match.group(2)
            
            # 生成锚点
            anchor = title.lower().replace(' ', '-').replace('?', '')
            anchor = re.sub(r'[^\w\-]', '', anchor)
            
            # 更新计数器
            counters[level - 1] += 1
            for i in range(level, 6):
                counters[i] = 0
            
            # 生成编号
            if level == 1:
                num = f"{counters[0]}."
            elif level == 2:
                num = f"{counters[0]}.{counters[1]}"
            else:
                num = f"{counters[0]}.{counters[1]}.{counters[2]}"
            
            indent = "  " * (level - 1)
            toc_lines.append(f"{indent}{num} [{title}](#{anchor})")
    
    if len(toc_lines) == 1:
        return "No headings found for TOC"
    
    return '\n'.join(toc_lines)


def add_timestamp(text: str, position: str = 'top') -> str:
    """
    添加时间戳
    
    Args:
        text: 原始文本
        position: 时间戳位置 ('top', 'bottom')
    
    Returns:
        添加时间戳后的文本
    """
    timestamp = f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    if position == 'top':
        return f"{timestamp}\n\n{text}"
    else:
        return f"{text}\n\n---\n{timestamp}"


def format_notes(text_path: Path, output_path: Optional[Path] = None,
                  operations: Optional[List[str]] = None,
                  verbose: bool = True) -> bool:
    """
    格式化纯文本笔记
    
    Args:
        text_path: 文本文件路径
        output_path: 输出路径（可选）
        operations: 要执行的格式化操作列表
        verbose: 是否显示详细信息
    
    Returns:
        是否成功
    """
    if not text_path.exists():
        if verbose:
            print_error(f"File not found: {text_path}")
        return False
    
    if operations is None:
        operations = ['normalize', 'titles', 'paragraphs']
    
    try:
        if verbose:
            print_info(f"Reading: {text_path.name}")
        
        # 读取文件
        with open(text_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 应用格式化操作
        for op in operations:
            if op == 'normalize':
                content = normalize_whitespace(content)
                if verbose:
                    print_info("Applied: normalize whitespace")
            
            elif op == 'titles':
                content = format_titles(content, style='markdown')
                if verbose:
                    print_info("Applied: format titles")
            
            elif op == 'paragraphs':
                content = format_paragraphs(content)
                if verbose:
                    print_info("Applied: format paragraphs")
            
            elif op == 'lists':
                content = format_lists(content)
                if verbose:
                    print_info("Applied: format lists")
            
            elif op == 'linenumbers':
                content = add_line_numbers(content)
                if verbose:
                    print_info("Applied: add line numbers")
            
            elif op == 'outline':
                content = extract_outline(content)
                if verbose:
                    print_info("Applied: extract outline")
            
            elif op == 'toc':
                content = generate_toc(content)
                if verbose:
                    print_info("Applied: generate TOC")
            
            elif op == 'timestamp':
                content = add_timestamp(content)
                if verbose:
                    print_info("Applied: add timestamp")
        
        # 确定输出路径
        if output_path is None:
            output_path = text_path.with_suffix('.formatted.md')
        
        # 写入文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        if verbose:
            print_success(f"Created: {output_path}")
        
        return True
    
    except Exception as e:
        if verbose:
            print_error(f"Formatting failed: {e}")
        return False


def batch_format_notes(text_files: List[Path], operations: Optional[List[str]] = None,
                        verbose: bool = True) -> dict:
    """
    批量格式化文本笔记
    
    Args:
        text_files: 文本文件列表
        operations: 格式化操作列表
        verbose: 是否显示详细信息
    
    Returns:
        转换结果统计
    """
    results = {'success': 0, 'failed': 0}
    
    for i, text_file in enumerate(text_files, 1):
        if verbose:
            print(f"\n[{i}/{len(text_files)}] {text_file.name}")
        
        success = format_notes(text_file, operations=operations, verbose=verbose)
        
        if success:
            results['success'] += 1
        else:
            results['failed'] += 1
    
    if verbose:
        print(f"\n{'='*50}")
        print(f"Formatting completed: {results['success']} success, {results['failed']} failed")
    
    return results
