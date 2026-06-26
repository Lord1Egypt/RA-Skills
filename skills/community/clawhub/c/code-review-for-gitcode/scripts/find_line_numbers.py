#!/usr/bin/env python3
"""
查找代码片段在文件中的行号区间

用法:
    python find_line_numbers.py <file_path> <code_snippet>
    
示例:
    python find_line_numbers.py file_parser.py 'return entries'
    python find_line_numbers.py extractors.py 'return "UNKNOWN"'
对于多行代码，需用 \n 分隔
    python find_line_numbers.py extractors.py 'except Exception as e:\n            print(f"Error reading file {file_path}: {e}")'
"""

import sys
import re


def find_code_in_file(file_path: str, code_snippet: str) -> list:
    """
    在文件中查找代码片段的行号区间
    
    Args:
        file_path: 文件路径
        code_snippet: 要查找的代码片段（支持多行）
        
    Returns:
        list: 匹配的行号区间列表，每个元素是 (start_line, end_line, matched_text)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"错误: 文件不存在: {file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"错误: 无法读取文件: {e}")
        sys.exit(1)
    
    # 规范化代码片段（去除首尾空白，统一换行符）
    code_lines = code_snippet.strip().split('\\n')
    code_lines = [line.rstrip() for line in code_lines]
    
    matches = []
    
    # 单行代码片段
    if len(code_lines) == 1:
        target = code_lines[0]
        for i, line in enumerate(lines, start=1):
            if target in line:
                matches.append((i, i, line.strip()))
    else:
        # 多行代码片段
        for i in range(len(lines) - len(code_lines) + 1):
            match = True
            matched_text = []
            for j, code_line in enumerate(code_lines):
                file_line = lines[i + j].rstrip()
                matched_text.append(file_line)
                if code_line not in file_line:
                    match = False
                    break
            if match:
                matches.append((i + 1, i + len(code_lines), '\n'.join(matched_text)))
    
    return matches


def main():
    if len(sys.argv) < 3:
        print("用法: python find_line_numbers.py <file_path> <code_snippet>")
        print("示例:")
        print('  python find_line_numbers.py file_parser.py "return entries"')
        print('  python find_line_numbers.py extractors.py \'return "UNKNOWN"\'')
        sys.exit(1)
    
    file_path = sys.argv[1]
    code_snippet = sys.argv[2]
    
    matches = find_code_in_file(file_path, code_snippet)
    
    if not matches:
        print(f"未找到代码片段: {code_snippet}")
        sys.exit(1)
    
    print(f"\n在文件 '{file_path}' 中找到 {len(matches)} 处匹配:\n")
    
    for idx, (start, end, text) in enumerate(matches, 1):
        if start == end:
            print(f"匹配 #{idx}: 第 {start} 行")
        else:
            print(f"匹配 #{idx}: 第 {start}-{end} 行")
        print(f"代码:\n{text}")
        print("-" * 60)


if __name__ == "__main__":
    main()
