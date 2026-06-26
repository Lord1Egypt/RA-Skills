#!/usr/bin/env python3
"""
Diff Tool - 文本差异比较工具
比较两个文本、文件或字符串的差异，高亮显示新增、删除和修改的行。
"""

import difflib
import json
import sys
import os
import argparse
from typing import List, Tuple, Optional

# ANSI 颜色代码
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'


def colorize(text: str, color: str) -> str:
    """为文本添加颜色"""
    return f"{color}{text}{RESET}"


def compare_strings(str1: str, str2: str, ignore_space: bool = False) -> List[Tuple[str, str, str]]:
    """
    比较两个字符串，返回差异列表
    返回: [(行号, 原始行, 差异类型), ...]
    差异类型: 'equal', 'add', 'remove', 'modify'
    """
    if ignore_space:
        str1 = ' '.join(str1.split())
        str2 = ' '.join(str2.split())
    
    lines1 = str1.splitlines(keepends=True)
    lines2 = str2.splitlines(keepends=True)
    
    diff = list(difflib.unified_diff(
        lines1, lines2,
        fromfile='原始文本',
        tofile='新文本',
        lineterm=''
    ))
    
    result = []
    for line in diff:
        if line.startswith('+++') or line.startswith('---') or line.startswith('@@'):
            continue
        elif line.startswith('+'):
            result.append(('+', line[1:], 'add'))
        elif line.startswith('-'):
            result.append(('-', line[1:], 'remove'))
    
    return result


def compare_files(file1: str, file2: str, ignore_space: bool = False) -> Tuple[List[str], dict]:
    """
    比较两个文件，返回差异
    """
    try:
        with open(file1, 'r', encoding='utf-8') as f:
            lines1 = f.readlines()
    except FileNotFoundError:
        return [f"文件不存在: {file1}"], {}
    except Exception as e:
        return [f"读取文件失败: {e}"], {}
    
    try:
        with open(file2, 'r', encoding='utf-8') as f:
            lines2 = f.readlines()
    except FileNotFoundError:
        return [f"文件不存在: {file2}"], {}
    except Exception as e:
        return [f"读取文件失败: {e}"], {}
    
    if ignore_space:
        lines1 = [' '.join(line.split()) + '\n' for line in lines1]
        lines2 = [' '.join(line.split()) + '\n' for line in lines2]
    
    diff = list(difflib.unified_diff(
        lines1, lines2,
        fromfile=file1,
        tofile=file2,
        lineterm=''
    ))
    
    return diff, {}


def format_diff_std(diff: List[str], show_stats: bool = False) -> str:
    """标准格式输出"""
    output = []
    stats = {'add': 0, 'remove': 0, 'modify': 0}
    
    for line in diff:
        if line.startswith('+++') or line.startswith('---'):
            continue
        elif line.startswith('@@'):
            output.append(colorize(line, BLUE))
            # 解析 @@ -a,b +c,d @@ 获取行号信息
        elif line.startswith('+'):
            stats['add'] += 1
            output.append(colorize(line, GREEN))
        elif line.startswith('-'):
            stats['remove'] += 1
            output.append(colorize(line, RED))
        else:
            output.append(line)
    
    result = '\n'.join(output)
    
    if show_stats:
        stats_text = f"\n{BOLD}统计:{RESET} "
        stats_text += f"{GREEN}+{stats['add']}{RESET} "
        stats_text += f"{RED}-{stats['remove']}{RESET}"
        result += stats_text
    
    return result


def format_diff_simple(diff: List[str]) -> str:
    """简洁格式输出 - 只显示有差异的行"""
    output = []
    
    for line in diff:
        if line.startswith('@@'):
            continue
        elif line.startswith('+'):
            output.append(colorize('+ ' + line[1:], GREEN))
        elif line.startswith('-'):
            output.append(colorize('- ' + line[1:], RED))
    
    return '\n'.join(output)


def format_diff_json(diff: List[str]) -> str:
    """JSON格式输出"""
    result = {
        'diffs': [],
        'stats': {'add': 0, 'remove': 0, 'modify': 0}
    }
    
    for line in diff:
        if line.startswith('@@') or line.startswith('+++') or line.startswith('---'):
            continue
        elif line.startswith('+'):
            result['diffs'].append({'type': 'add', 'content': line[1:]})
            result['stats']['add'] += 1
        elif line.startswith('-'):
            result['diffs'].append({'type': 'remove', 'content': line[1:]})
            result['stats']['remove'] += 1
    
    return json.dumps(result, ensure_ascii=False, indent=2)


def cmd_string(args):
    """比较两个字符串"""
    diff = compare_strings(args.str1, args.str2, args.ignore_space)
    
    if not diff:
        print("两个文本完全相同 ✓")
        return
    
    # 转换为 unified diff 格式以便复用格式化函数
    unified_diff = []
    for status, content, diff_type in diff:
        prefix = '+' if status == '+' else '-'
        unified_diff.append(prefix + content.rstrip('\n'))
    
    if args.format == 'json':
        print(format_diff_json(unified_diff))
    elif args.format == 'simple':
        print(format_diff_simple(unified_diff))
    else:
        print(format_diff_std(unified_diff, args.stats))


def cmd_file(args):
    """比较两个文件"""
    diff, _ = compare_files(args.file1, args.file2, args.ignore_space)
    
    if not diff:
        print("两个文件完全相同 ✓")
        return
    
    # 检查是否是错误信息（不以 --- 或 +++ 开头）
    if diff[0] and not diff[0].startswith(('---', '+++', '@@')):
        print(diff[0])
        return
    
    if args.format == 'json':
        print(format_diff_json(diff))
    elif args.format == 'simple':
        print(format_diff_simple(diff))
    else:
        print(format_diff_std(diff, args.stats))


def main():
    parser = argparse.ArgumentParser(
        description='Diff Tool - 文本差异比较工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s string "hello world" "hello python"
  %(prog)s file /tmp/a.txt /tmp/b.txt
  %(prog)s file /tmp/a.txt /tmp/b.txt --format json --stats
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='子命令')
    
    # string 命令
    string_parser = subparsers.add_parser('string', help='比较两个字符串')
    string_parser.add_argument('str1', help='第一个字符串')
    string_parser.add_argument('str2', help='第二个字符串')
    string_parser.add_argument('--ignore-space', action='store_true', help='忽略空白字符差异')
    string_parser.add_argument('--format', choices=['std', 'simple', 'json'], default='std', help='输出格式')
    string_parser.add_argument('--stats', action='store_true', help='显示统计信息')
    string_parser.set_defaults(func=cmd_string)
    
    # file 命令
    file_parser = subparsers.add_parser('file', help='比较两个文件')
    file_parser.add_argument('file1', help='第一个文件路径')
    file_parser.add_argument('file2', help='第二个文件路径')
    file_parser.add_argument('--ignore-space', action='store_true', help='忽略空白字符差异')
    file_parser.add_argument('--format', choices=['std', 'simple', 'json'], default='std', help='输出格式')
    file_parser.add_argument('--stats', action='store_true', help='显示统计信息')
    file_parser.set_defaults(func=cmd_file)
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        sys.exit(1)
    
    args.func(args)


if __name__ == '__main__':
    main()
