#!/usr/bin/env python3
"""命令行入口"""
import sys
import json
from intent_classifier import classify

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 cli.py <消息>")
        print("示例: python3 cli.py 想买一台电脑")
        sys.exit(1)
    
    text = " ".join(sys.argv[1:])
    result = classify(text)
    print(json.dumps(result, ensure_ascii=False, indent=2))
