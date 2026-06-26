#!/usr/bin/env python3
"""中文笑话库 - 从本地 JSON 获取笑话"""

import json
import random
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent
JOKES_FILE = ROOT_DIR / "jokes.json"

def load_jokes():
    """加载笑话库"""
    with open(JOKES_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)['jokes']

def get_random_joke(joke_type=None, count=1):
    """获取随机笑话"""
    jokes = load_jokes()
    
    if joke_type:
        jokes = [j for j in jokes if j.get('type') == joke_type]
    
    if not jokes:
        print(f"未找到类型 '{joke_type}' 的笑话", error=True)
        return
    
    selected = random.sample(jokes, min(count, len(jokes)))
    
    for i, joke in enumerate(selected):
        print(joke['joke'])
        print(f"—— {joke.get('category', '笑话')}")
        if i < len(selected) - 1:
            print()

def list_types():
    """列出所有类型"""
    jokes = load_jokes()
    types = sorted(set(j.get('type', 'unknown') for j in jokes))
    print("可用类型：", ", ".join(types))

def main():
    parser = argparse.ArgumentParser(description='中文笑话库工具')
    parser.add_argument('command', choices=['random', 'help'], nargs='?', default='random')
    parser.add_argument('--type', '-t', help='过滤类型：pun, program, life, brain, story')
    parser.add_argument('--count', '-c', type=int, default=1, help='获取笑话数量')
    parser.add_argument('--list', '-l', action='store_true', help='列出所有类型')
    
    args = parser.parse_args()
    
    if args.command == 'help' or args.list:
        if args.list:
            list_types()
        else:
            parser.print_help()
        return
    
    get_random_joke(args.type, args.count)

if __name__ == '__main__':
    main()
