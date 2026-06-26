#!/usr/bin/env python3
"""文本拆分工具"""
import argparse

def split_text(text, separator=','):
    """拆分文本为多行"""
    parts = text.split(separator)
    return '\n'.join(parts)

def main():
    parser = argparse.ArgumentParser(description="文本拆分工具")
    parser.add_argument("--text", required=True, help="要拆分的文本")
    parser.add_argument("--separator", default=',', help="分隔符")
    args = parser.parse_args()
    print(split_text(args.text, args.separator))

if __name__ == "__main__":
    main()
