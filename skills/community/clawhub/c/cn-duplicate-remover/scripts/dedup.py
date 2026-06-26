#!/usr/bin/env python3
"""重复行去除工具"""
import argparse
from collections import OrderedDict

def dedup_lines(text, keep_order=True):
    """去重"""
    lines = text.split('\n')
    if keep_order:
        seen = OrderedDict()
        for line in lines:
            seen[line] = None
        return '\n'.join(seen.keys())
    else:
        return '\n'.join(set(lines))

def main():
    parser = argparse.ArgumentParser(description="重复行去除工具")
    parser.add_argument("--text", help="要处理的文本")
    parser.add_argument("--file", help="输入文件")
    parser.add_argument("--output", help="输出文件")
    parser.add_argument("--sort", action="store_true", help="排序输出")
    args = parser.parse_args()

    if args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        text = args.text or ""

    result = dedup_lines(text, keep_order=not args.sort)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"已保存到 {args.output}")
    else:
        print(result)

if __name__ == "__main__":
    main()
