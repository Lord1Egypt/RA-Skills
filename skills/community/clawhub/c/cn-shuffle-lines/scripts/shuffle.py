#!/usr/bin/env python3
"""文本行随机排序工具"""
import argparse
import random

def shuffle_lines(text):
    """随机打乱行顺序"""
    lines = text.split('\n')
    random.shuffle(lines)
    return '\n'.join(lines)

def main():
    parser = argparse.ArgumentParser(description="文本行随机排序")
    parser.add_argument("--text", help="要处理的文本")
    parser.add_argument("--file", help="输入文件")
    args = parser.parse_args()

    if args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        text = args.text or ""

    print(shuffle_lines(text))

if __name__ == "__main__":
    main()
