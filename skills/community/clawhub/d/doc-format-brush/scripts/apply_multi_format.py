#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
apply_multi_format.py — 多格式文档格式刷

功能：
  参照模板文档的格式，将任意格式的输入文档（.docx, .md, .txt）
  转换为具有统一格式的输出文档（.docx, .md, .txt）。

用法：
  # 方式一：使用内置公文格式
  python apply_multi_format.py <输入文档> --official --output <输出文档>
  
  # 方式二：参照模板格式
  python apply_multi_format.py <输入文档> <模板文件> --output <输出文档>
  
  # 方式三：指定格式描述文件
  python apply_multi_format.py <输入文档> --format-json <格式描述.json> --output <输出文档>

支持的格式：
  输入：.docx (Word), .md (Markdown), .txt (纯文本)
  输出：.docx (Word), .md (Markdown), .txt (纯文本)
"""

import sys
import os
import json
import argparse
from pathlib import Path

# 导入格式处理模块
import format_bridge
import extract_format
import apply_format


def get_official_config():
    """获取内置公文格式配置"""
    return apply_format.get_official_config()


def main():
    parser = argparse.ArgumentParser(
        description='多格式文档格式刷 - 参照模板整理任意文档格式',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  # 将 Markdown 转为公文格式 Word
  python apply_multi_format.py 报告.md --official --output 报告_公文.docx
  
  # 将文本文件转为 Markdown（使用模板格式）
  python apply_multi_format.py 笔记.txt 模板.docx --output 笔记_格式.md
  
  # Word 转 Word（格式对照）
  python apply_multi_format.py 源文件.docx 模板.docx --输出 目标文件.docx
        """
    )
    
    parser.add_argument('input', help='输入文档路径 (.docx, .md, .txt)')
    parser.add_argument('template', nargs='?', help='模板文档路径 (可选)')
    parser.add_argument('--official', action='store_true', help='使用内置公文格式')
    parser.add_argument('--format-json', dest='format_json', help='格式描述JSON文件路径')
    parser.add_argument('--output', '-o', required=True, help='输出文档路径')
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    output_path = Path(args.output)
    
    if not input_path.exists():
        print(f"错误：输入文件不存在: {input_path}")
        sys.exit(1)
    
    # 确定格式配置来源
    if args.official:
        config = get_official_config()
        print("使用内置公文格式 (GB/T 9704-2012)")
    elif args.format_json:
        with open(args.format_json, 'r', encoding='utf-8') as f:
            config = json.load(f)
        print(f"从格式文件加载配置: {args.format_json}")
    elif args.template:
        template_path = Path(args.template)
        if not template_path.exists():
            print(f"错误：模板文件不存在: {template_path}")
            sys.exit(1)
        
        print(f"从模板提取格式: {template_path}")
        # 使用 extract_format 提取模板格式
        sys.argv = ['extract_format.py', str(template_path), '--output', '-']
        # 临时重定向输出
        import io
        from contextlib import redirect_stdout
        
        # 提取格式到临时变量
        extracted_profile = extract_format.extract_format_json(str(template_path))
        config = apply_format.analyze_profile_advanced(extracted_profile)
    else:
        print("错误：请指定 --official, --format-json 或提供模板文件")
        sys.exit(1)
    
    # 显示格式配置
    print("\n格式配置:")
    for key in ['title', 'level1', 'level2', 'body']:
        if key in config:
            fmt = config[key]
            align = fmt.get('alignment', 'LEFT')
            align_name = "居中" if "CENTER" in align else "两端对齐" if "JUSTIFY" in align else "左对齐"
            print(f"  {key}: {fmt.get('font_name', 'N/A')} {fmt.get('font_size_pt', 12)}pt, {align_name}")
    
    # 读取输入文档
    print(f"\n读取输入: {input_path}")
    paragraphs, metadata = format_bridge.read_document(str(input_path))
    print(f"  段落数: {len(paragraphs)}")
    print(f"  输入格式: {metadata.get('format', 'unknown')}")
    
    # 检测段落类型统计
    para_types = {}
    for i, para in enumerate(paragraphs):
        ptype = format_bridge.detect_paragraph_type(para, i, len(paragraphs))
        para_types[ptype] = para_types.get(ptype, 0) + 1
    
    print(f"  段落类型: {para_types}")
    
    # 写入输出文档
    print(f"\n生成输出: {output_path}")
    format_bridge.write_document(paragraphs, str(output_path), config)
    print(f"  输出格式: {output_path.suffix}")
    
    print("\n完成!")
    print(f"输出文件: {output_path.absolute()}")


if __name__ == '__main__':
    main()
