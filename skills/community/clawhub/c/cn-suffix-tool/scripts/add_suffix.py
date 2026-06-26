#!/usr/bin/env python3
"""后缀添加工具"""
import argparse

def add_suffix(text, suffix):
    """为每行添加后缀"""
    lines = text.split('\n')
    return '\n'.join(line + suffix for line in lines)

def main():
    parser = argparse.ArgumentParser(description="后缀添加工具")
    parser.add_argument("--text", required=True, help="要处理的文本")
    parser.add_argument("--suffix", required=True, help="后缀")
    args = parser.parse_args()
    print(add_suffix(args.text, args.suffix))

if __name__ == "__main__":
    main()
