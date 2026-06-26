#!/usr/bin/env python3
"""
cn-diff-checker - 文本差异比对工具
支持逐行、逐词、逐字符比对
"""
import argparse
import difflib
import sys
import os

# ANSI颜色代码
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'

def read_content(text_or_file):
    """读取内容（文本或文件）"""
    if os.path.isfile(text_or_file):
        try:
            with open(text_or_file, 'r', encoding='utf-8') as f:
                return f.read().splitlines()
        except:
            with open(text_or_file, 'r', encoding='gbk') as f:
                return f.read().splitlines()
    else:
        return text_or_file.splitlines()

def diff_lines(old, new):
    """逐行比对"""
    diff = list(difflib.unified_diff(old, new, lineterm='', n=3))
    if not diff:
        print("两个文本完全相同")
        return
    
    for line in diff:
        if line.startswith('---'):
            print(f"{YELLOW}{line}{RESET}")
        elif line.startswith('+++'):
            print(f"{YELLOW}{line}{RESET}")
        elif line.startswith('@@'):
            print(f"{BLUE}{line}{RESET}")
        elif line.startswith('-'):
            print(f"{RED}{line}{RESET}")
        elif line.startswith('+'):
            print(f"{GREEN}{line}{RESET}")
        else:
            print(line)

def diff_words(old_text, new_text):
    """逐词比对"""
    old_lines = old_text.split('\n')
    new_lines = new_text.split('\n')
    
    matcher = difflib.SequenceMatcher(None, old_text.split(), new_text.split())
    
    print(f"{BOLD}逐词差异：{RESET}\n")
    
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            print(' '.join(old_text.split()[i1:i2]), end=' ')
        elif tag == 'replace':
            print(f"{RED}{' '.join(old_text.split()[i1:i2])}{RESET} → {GREEN}{' '.join(new_text.split()[j1:j2])}{RESET}", end=' ')
        elif tag == 'delete':
            print(f"{RED}{' '.join(old_text.split()[i1:i2])}{RESET}", end=' ')
        elif tag == 'insert':
            print(f"{GREEN}{' '.join(new_text.split()[j1:j2])}{RESET}", end=' ')
    print()

def diff_chars(old_text, new_text):
    """逐字符比对"""
    matcher = difflib.SequenceMatcher(None, old_text, new_text)
    
    print(f"{BOLD}逐字符差异：{RESET}\n")
    
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            print(old_text[i1:i2], end='')
        elif tag == 'replace':
            print(f"{RED}{old_text[i1:i2]}{RESET}→{GREEN}{new_text[j1:j2]}{RESET}", end='')
        elif tag == 'delete':
            print(f"{RED}{old_text[i1:i2]}{RESET}", end='')
        elif tag == 'insert':
            print(f"{GREEN}{new_text[j1:j2]}{RESET}", end='')
    print()

def main():
    parser = argparse.ArgumentParser(description='文本差异比对工具')
    parser.add_argument('old', help='原始文本或文件')
    parser.add_argument('new', help='新文本或文件')
    parser.add_argument('--line', action='store_true', help='逐行比对')
    parser.add_argument('--word', action='store_true', help='逐词比对')
    parser.add_argument('--char', action='store_true', help='逐字符比对')
    parser.add_argument('--output', help='输出到文件')
    
    args = parser.parse_args()
    
    # 读取内容
    old_content = read_content(args.old)
    new_content = read_content(args.new)
    
    # 统一为字符串
    old_str = '\n'.join(old_content)
    new_str = '\n'.join(new_content)
    
    # 选择比对模式
    if args.word:
        diff_words(old_str, new_str)
    elif args.char:
        diff_chars(old_str, new_str)
    else:
        # 默认逐行
        diff_lines(old_content, new_content)

if __name__ == '__main__':
    main()