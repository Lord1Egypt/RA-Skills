#!/usr/bin/env python3
"""前缀添加工具"""
import argparse

def add_prefix(text, prefix):
    """为每行添加前缀"""
    lines = text.split('\n')
    return '\n'.join(prefix + line for line in lines)

def main():
    parser = argparse.ArgumentParser(description="前缀添加工具")
    parser.add_argument("--text", required=True, help="要处理的文本")
    parser.add_argument("--prefix", required=True, help="前缀")
    args = parser.parse_args()
    print(add_prefix(args.text, args.prefix))

if __name__ == "__main__":
    main()
