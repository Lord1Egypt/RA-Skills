#!/usr/bin/env python3
"""
合并 OpenClaw 文档脚本
按照 docs.json 的结构合并所有文档，方便放入 NotebookLM
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Any

def read_markdown_file(file_path: Path) -> str:
    """读取 Markdown 文件内容"""
    if not file_path.exists():
        return f"\n<!-- 文件不存在: {file_path} -->\n"
    
    try:
        content = file_path.read_text(encoding='utf-8')
        # 移除 frontmatter（YAML 头部）
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                content = parts[2].strip()
        return content
    except Exception as e:
        return f"\n<!-- 读取文件错误 {file_path}: {e} -->\n"

def process_pages(pages: List[Any], base_dir: Path, merged_content: List[str], level: int = 3):
    """递归处理页面列表"""
    for page in pages:
        if isinstance(page, str):
            page_path = base_dir / f"{page}.md"
            title_level = "#" * level
            # 使用更友好的标题格式：将路径转换为标题
            # 移除语言前缀（如 zh-CN/）
            page_title = page
            if page_title.startswith('zh-CN/'):
                page_title = page_title[6:]  # 移除 'zh-CN/'
            elif page_title.startswith('ja-JP/'):
                page_title = page_title[6:]  # 移除 'ja-JP/'
            
            # 将路径转换为标题
            page_title = page_title.replace('/', ' / ').replace('-', ' ').replace('_', ' ')
            # 首字母大写（但保留中文等非ASCII字符）
            words = page_title.split()
            title_words = []
            for word in words:
                if word and word[0].isascii() and word[0].isalpha():
                    title_words.append(word.capitalize())
                else:
                    title_words.append(word)
            page_title = ' '.join(title_words)
            
            merged_content.append(f"\n{title_level} {page_title}\n\n")
            merged_content.append(f"<!-- 来源: {page}.md -->\n")
            content = read_markdown_file(page_path)
            merged_content.append(content)
            merged_content.append("\n\n" + "-" * 80 + "\n\n")
        elif isinstance(page, dict):
            # 处理嵌套组
            if 'group' in page:
                nested_group_name = page['group']
                title_level = "#" * level
                merged_content.append(f"\n{title_level} {nested_group_name}\n\n")
                if 'pages' in page:
                    process_pages(page['pages'], base_dir, merged_content, level + 1)

def merge_documents(docs_json_path: Path, output_dir: Path, language: str = "en"):
    """按照 docs.json 结构合并文档"""
    
    # 读取 docs.json
    with open(docs_json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # 找到对应语言的配置
    lang_config = None
    for lang in config['navigation']['languages']:
        if lang['language'] == language:
            lang_config = lang
            break
    
    if not lang_config:
        print(f"未找到语言配置: {language}")
        return
    
    base_dir = docs_json_path.parent
    merged_content = []
    
    # 添加文档头部
    merged_content.append(f"# OpenClaw 文档合并版本 ({language})\n")
    merged_content.append(f"本文档由 OpenClaw 文档自动合并生成，按照官方文档结构组织。\n")
    merged_content.append("=" * 80 + "\n\n")
    
    # 遍历所有标签页
    for tab in lang_config['tabs']:
        tab_name = tab['tab']
        merged_content.append(f"\n{'=' * 80}\n")
        merged_content.append(f"# {tab_name}\n")
        merged_content.append(f"{'=' * 80}\n\n")
        
        # 遍历所有组
        for group in tab['groups']:
            if isinstance(group, dict):
                if 'group' in group:
                    group_name = group['group']
                    merged_content.append(f"\n## {group_name}\n\n")
                    
                    # 处理页面
                    if 'pages' in group:
                        process_pages(group['pages'], base_dir, merged_content, level=3)
                elif 'pages' in group:
                    # 直接包含页面，没有组名
                    process_pages(group['pages'], base_dir, merged_content, level=3)
    
    # 写入合并后的文件
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"openclaw-docs-merged-{language}.md"
    output_file.write_text(''.join(merged_content), encoding='utf-8')
    print(f"✅ 已生成合并文档: {output_file}")
    print(f"   总长度: {len(''.join(merged_content))} 字符")

def main():
    """主函数"""
    script_dir = Path(__file__).parent
    docs_json_path = script_dir / "docs.json"
    output_dir = script_dir / "merged"
    
    if not docs_json_path.exists():
        print(f"错误: 找不到 docs.json 文件: {docs_json_path}")
        return
    
    # 合并英文文档
    print("正在合并英文文档...")
    merge_documents(docs_json_path, output_dir, "en")
    
    # 合并中文文档
    print("\n正在合并中文文档...")
    merge_documents(docs_json_path, output_dir, "zh-Hans")
    
    print("\n✅ 文档合并完成！")

if __name__ == "__main__":
    main()
