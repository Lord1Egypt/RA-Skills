#!/usr/bin/env python3
"""文本统计工具"""
import argparse
from collections import Counter

def analyze_text(text):
    """分析文本"""
    lines = text.split('\n')
    chars = text.replace('\n', '').replace(' ', '')
    return {
        "总行数": len(lines),
        "非空行数": len([l for l in lines if l.strip()]),
        "总字符数": len(text),
        "中文字数": len([c for c in chars if '\u4e00' <= c <= '\u9fff']),
        "英文词数": len([w for w in text.split() if w.isalpha() and w.isascii()])
    }

def word_frequency(text, top=10):
    """词频统计"""
    words = [w for w in text.split() if len(w) > 1]
    return Counter(words).most_common(top)

def main():
    parser = argparse.ArgumentParser(description="文本统计")
    parser.add_argument("--text", help="要统计的文本")
    parser.add_argument("--file", help="输入文件")
    parser.add_argument("--freq", action="store_true", help="显示词频")
    args = parser.parse_args()

    if args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        text = args.text or ""

    result = analyze_text(text)
    for k, v in result.items():
        print(f"{k}: {v}")

    if args.freq:
        print("\n高频词TOP10:")
        for word, count in word_frequency(text):
            print(f"  {word}: {count}")

if __name__ == "__main__":
    main()
