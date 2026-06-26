#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
格式转换器
将 open-novel-writing 生成的正文格式转换为 fanqie-publisher 需要的格式
"""

import re
import os
from pathlib import Path
from typing import List, Dict, Optional, Tuple


class Chapter:
    """代表一章"""
    def __init__(self, chapter_num: int, title: str, content: str, words: int):
        self.chapter_num = chapter_num
        self.title = title
        self.content = content
        self.words = words


def extract_chapter_info(content: str) -> Tuple[Optional[str], str]:
    """从正文提取章节标题和内容"""
    lines = content.split('\n')
    title = None
    content_lines = []
    
    # 常见标题模式
    title_patterns = [
        r'^第\s*\d+\s*章[：:\s].*',  # 第 1 章：标题
        r'^第\d+章[：:\s].*',        # 第1章：标题
        r'^\d+\.\s+.*',              # 1. 标题
        r'^#\s+第\s*\d+\s*章.*',     # # 第 1 章
        r'^#\s+.*\d+.*',             # # ... 包含数字
    ]
    
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
            
        # 检查是否是标题
        is_title = False
        if title is None:
            for pattern in title_patterns:
                if re.match(pattern, line):
                    title = re.sub(r'^#\s+', '', line)
                    title = re.sub(r'^[0-9]+\.\s+', '', title)
                    is_title = True
                    break
            if is_title:
                continue
        
        content_lines.append(line)
    
    if title is None:
        # 如果没找到标题，从第一行提取
        if lines:
            first_line = lines[0].strip()
            if first_line:
                title = first_line
                content_lines = lines[1:]
            else:
                title = "未命名"
                content_lines = lines
    
    return title, '\n'.join(content_lines).strip()


def convert_open_novel_to_fanqie(
    open_novel_dir: str,
    chapter_start: Optional[int] = None,
    chapter_end: Optional[int] = None
) -> List[Chapter]:
    """
    将 open-novel-writing 格式的正文转换为 fanqie-publisher 可发布的格式
    
    Args:
        open_novel_dir: open-novel-writing 项目目录
        chapter_start: 起始章节号（None表示自动检测最新）
        chapter_end: 结束章节号
    
    Returns:
        Chapter列表
    """
    content_dir = Path(open_novel_dir) / "正文"
    if not content_dir.exists():
        raise FileNotFoundError(f"正文目录不存在: {content_dir}")
    
    # 找到所有正文文件
    chapter_files = []
    for ext in ['*.txt', '*.md']:
        chapter_files.extend(list(content_dir.glob(ext)))
    
    # 解析章节号
    parsed_files = []
    chapter_pattern = re.compile(r'(?:第|^)(\d+)(?:章|).*')
    
    for f in chapter_files:
        match = chapter_pattern.search(f.name)
        if match:
            num = int(match.group(1))
            parsed_files.append((num, f))
    
    # 按章节号排序
    parsed_files.sort(key=lambda x: x[0])
    
    # 根据范围筛选
    result = []
    for num, f in parsed_files:
        if chapter_start is not None and num < chapter_start:
            continue
        if chapter_end is not None and num > chapter_end:
            continue
        
        # 读取文件
        with open(f, 'r', encoding='utf-8') as fp:
            content = fp.read()
        
        title, clean_content = extract_chapter_info(content)
        word_count = len(clean_content.replace('\n', '').replace(' ', ''))
        
        chapter = Chapter(num, title, clean_content, word_count)
        result.append(chapter)
    
    return result


def convert_to_fanqie_format(chapter: Chapter) -> dict:
    """转换为 fanqie-publisher publish 接口需要的格式"""
    return {
        'title': chapter.title,
        'content': chapter.content,
        'chapter_num': chapter.chapter_num,
        'words': chapter.words
    }


def save_for_publish(chapters: List[Chapter], output_dir: str) -> str:
    """
    将转换后的章节保存为可发布格式，生成发布用的汇总文件
    
    Returns:
        汇总文件路径
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 保存单个章节文件
    for chapter in chapters:
        filename = f"第{chapter.chapter_num:03d}章_{chapter.title}.md"
        filepath = output_path / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# {chapter.title}\n\n")
            f.write(chapter.content)
        
        print(f"  已保存: {filename}")
    
    # 生成发布清单
    manifest_path = output_path / "publish_manifest.md"
    with open(manifest_path, 'w', encoding='utf-8') as f:
        f.write("# 待发布章节清单\n\n")
        f.write(f"总计: {len(chapters)} 章\n\n")
        f.write("| 章节 | 标题 | 字数 | 文件 |\n")
        f.write("|------|------|------|------|\n")
        for chapter in chapters:
            filename = f"第{chapter.chapter_num:03d}章_{chapter.title}.md"
            f.write(f"| {chapter.chapter_num} | {chapter.title} | {chapter.words} | {filename} |\n")
    
    print(f"\n  清单已生成: {manifest_path}")
    return str(manifest_path)


if __name__ == "__main__":
    # 测试
    import sys
    if len(sys.argv) > 1:
        test_dir = sys.argv[1]
        chapters = convert_open_novel_to_fanqie(test_dir)
        print(f"找到 {len(chapters)} 章:")
        for c in chapters:
            print(f"  {c.chapter_num}: {c.title} ({c.words}字)")
