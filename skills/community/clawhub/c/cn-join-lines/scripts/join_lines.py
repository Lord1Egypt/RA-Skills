#!/usr/bin/env python3
"""文本行合并工具"""
import argparse

def join_lines(text, separator=' '):
    """合并文本行"""
    lines = text.split('\n')
    return separator.join(lines)

def main():
    parser = argparse.ArgumentParser(description="文本行合并工具")
    parser.add_argument("--text", required=True, help="要合并的文本")
    parser.add_argument("--separator", default=' ', help="分隔符")
    args = parser.parse_args()
    print(join_lines(args.text, args.separator))

if __name__ == "__main__":
    main()
