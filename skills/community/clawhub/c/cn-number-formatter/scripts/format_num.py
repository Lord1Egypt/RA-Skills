#!/usr/bin/env python3
"""数字格式化工具"""
import argparse

def format_number(num, style='thousands'):
    """格式化数字"""
    if style == 'thousands':
        return f"{num:,}"
    elif style == 'percent':
        return f"{num:.2%}"
    elif style == 'scientific':
        return f"{num:.2e}"
    return str(num)

def main():
    parser = argparse.ArgumentParser(description="数字格式化")
    parser.add_argument("--number", type=float, required=True)
    parser.add_argument("--thousands", action="store_true")
    parser.add_argument("--percent", action="store_true")
    parser.add_argument("--scientific", action="store_true")
    args = parser.parse_args()

    if args.thousands:
        print(format_number(args.number, 'thousands'))
    elif args.percent:
        print(format_number(args.number, 'percent'))
    elif args.scientific:
        print(format_number(args.number, 'scientific'))
    else:
        print(args.number)

if __name__ == "__main__":
    main()
