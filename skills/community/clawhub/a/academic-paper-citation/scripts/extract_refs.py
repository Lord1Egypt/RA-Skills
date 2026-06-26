#!/usr/bin/env python3
"""
参考文献解析器
从论文markdown文件中提取参考文献列表
"""

import re
import json

def extract_references(md_content):
    """从markdown内容中提取参考文献"""
    
    # 找到参考文献部分
    ref_pattern = r'参考文献\s*\n(.*?)(?=致谢|$)'
    ref_match = re.search(ref_pattern, md_content, re.DOTALL)
    
    if not ref_match:
        print("未找到参考文献部分")
        return []
    
    ref_section = ref_match.group(1).strip()
    
    # 解析每条参考文献
    references = []
    
    # 匹配 [数字] 开头的引用
    ref_lines = re.findall(r'\[(\d+)\]\s*(.+?)(?=\[\d+\]|$)', ref_section, re.DOTALL)
    
    for num, content in ref_lines:
        content = content.strip().replace('\n', ' ')
        ref_info = {
            'id': int(num),
            'raw': content,
            'type': detect_ref_type(content),
            'authors': extract_authors(content),
            'title': extract_title(content),
            'year': extract_year(content)
        }
        references.append(ref_info)
    
    return references

def detect_ref_type(content):
    """检测参考文献类型"""
    if '[J]' in content:
        return 'journal'
    elif '[M]' in content:
        return 'book'
    elif '[D]' in content:
        return 'thesis'
    elif '[C]' in content:
        return 'conference'
    elif '[Z]' in content:
        return 'standard'
    elif '[R]' in content:
        return 'report'
    else:
        return 'unknown'

def extract_authors(content):
    """提取作者信息"""
    # 尝试匹配作者部分（通常在文献类型标记之前）
    match = re.match(r'^([^\[\]]+?)\[', content)
    if match:
        authors = match.group(1).strip()
        # 移除末尾的句点
        authors = authors.rstrip('.')
        return authors
    return ""

def extract_title(content):
    """提取标题"""
    # 尝试匹配文献类型标记后的标题
    match = re.search(r'\[[JMDCRZ]\]\.?\s*([^\.]+)', content)
    if match:
        return match.group(1).strip()
    return ""

def extract_year(content):
    """提取年份"""
    match = re.search(r'(\d{4})', content)
    if match:
        return int(match.group(1))
    return None

if __name__ == "__main__":
    # 读取markdown文件
    with open('/Users/openclaw2026/.qclaw/workspace/论文初稿v4.0.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    references = extract_references(content)
    
    print(f"共提取到 {len(references)} 条参考文献")
    
    # 保存为JSON
    with open('/Users/openclaw2026/.qclaw/workspace/references.json', 'w', encoding='utf-8') as f:
        json.dump(references, f, ensure_ascii=False, indent=2)
    
    print("参考文献已保存到 references.json")
    
    # 显示前5条作为示例
    print("\n前5条参考文献：")
    for ref in references[:5]:
        print(f"[{ref['id']}] {ref['type'].upper()} - {ref['title'][:50]}...")
