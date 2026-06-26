#!/usr/bin/env python3
"""轻量推送脚本——直接读取JSON+发请求，不走agent session"""
import json
import random
import sys

def main():
    kind = sys.argv[1] if len(sys.argv) > 1 else "night"
    path = f"/root/.openclaw/workspace/skills/anti-996-reminder/contents/{kind}.json"

    with open(path) as f:
        items = json.load(f)

    text = random.choice(items)
    print(text)

if __name__ == "__main__":
    main()
