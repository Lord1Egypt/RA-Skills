#!/usr/bin/env python3
"""文本行排序工具"""
import argparse

def sort_lines(text, descending=False, by_length=False):
    """排序文本行"""
    lines = text.split('\n')
    if by_length:
        lines.sort(key=len, reverse=descending)
    else:
        lines.sort(reverse=descending)
    return '\n'.join(lines)

def main():
    parser = argparse.ArgumentParser(description="文本行排序工具")
    parser.add_argument("--text", required=True, help="要排序的文本")
    parser.add_argument("--desc", action="store_true", help="降序排列")
    parser.add_argument("--by-length", action="store_true", help="按长度排序")
    args = parser.parse_args()
    print(sort_lines(args.text, args.desc, args.by_length))

if __name__ == "__main__":
    main()
