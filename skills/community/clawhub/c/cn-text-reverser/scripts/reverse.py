#!/usr/bin/env python3
"""文本反转工具"""
import argparse
import sys

def reverse_text(text, by_char=False):
    """反转文本"""
    if by_char:
        return text[::-1]
    else:
        words = text.split()
        return ' '.join(reversed(words))

def main():
    parser = argparse.ArgumentParser(description="文本反转工具")
    parser.add_argument("--text", required=True, help="要反转的文本")
    parser.add_argument("--char", action="store_true", help="按字符反转")
    args = parser.parse_args()
    print(reverse_text(args.text, args.char))

if __name__ == "__main__":
    main()
