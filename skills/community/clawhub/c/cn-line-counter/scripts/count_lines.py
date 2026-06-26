#!/usr/bin/env python3
"""行数统计工具"""
import argparse

def count_text(text):
    """统计文本"""
    lines = text.split('\n')
    return {
        "总行数": len(lines),
        "非空行数": len([l for l in lines if l.strip()]),
        "字数": len(text.replace('\n', '').replace(' ', '')),
        "字符数": len(text)
    }

def main():
    parser = argparse.ArgumentParser(description="行数统计工具")
    parser.add_argument("--text", help="要统计的文本")
    parser.add_argument("--file", help="输入文件")
    args = parser.parse_args()

    if args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        text = args.text or ""

    result = count_text(text)
    for k, v in result.items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    main()
