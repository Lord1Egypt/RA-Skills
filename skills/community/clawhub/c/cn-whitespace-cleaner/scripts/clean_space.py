#!/usr/bin/env python3
"""空白字符清理工具"""
import argparse
import re

def clean_whitespace(text):
    """清理多余空白"""
    return re.sub(r'\s+', ' ', text).strip()

def main():
    parser = argparse.ArgumentParser(description="空白字符清理工具")
    parser.add_argument("--text", help="要清理的文本")
    parser.add_argument("--file", help="输入文件")
    parser.add_argument("--output", help="输出文件")
    args = parser.parse_args()

    if args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        text = args.text or ""

    result = clean_whitespace(text)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"已保存到 {args.output}")
    else:
        print(result)

if __name__ == "__main__":
    main()
