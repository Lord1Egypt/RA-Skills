#!/usr/bin/env python3
"""
Word Counter - 统计文本字数、字符数、行数
"""
import sys
import json

def count_words(text: str) -> dict:
    """统计文本字数"""
    words = len(text.split()) if text else 0
    chars = len(text) if text else 0
    lines = text.count('\n') + 1 if text else 0
    return {'words': words, 'chars': chars, 'lines': lines}

def main():
    text = sys.argv[1] if len(sys.argv) > 1 else ''
    result = count_words(text)
    print(json.dumps(result))

if __name__ == '__main__':
    main()
