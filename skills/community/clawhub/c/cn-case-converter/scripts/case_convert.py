#!/usr/bin/env python3
"""大小写转换工具"""
import argparse

def main():
    parser = argparse.ArgumentParser(description="大小写转换工具")
    parser.add_argument("--text", required=True, help="要转换的文本")
    parser.add_argument("--upper", action="store_true", help="转大写")
    parser.add_argument("--lower", action="store_true", help="转小写")
    parser.add_argument("--title", action="store_true", help="首字母大写")
    args = parser.parse_args()

    if args.upper:
        print(args.text.upper())
    elif args.lower:
        print(args.text.lower())
    elif args.title:
        print(args.text.title())
    else:
        print(args.text)

if __name__ == "__main__":
    main()
