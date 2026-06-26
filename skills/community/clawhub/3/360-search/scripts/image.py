#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
360 图片搜索脚本
"""

import sys
import json
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from search_client import Search360Client


def main():
    if len(sys.argv) < 2:
        print('用法：python image.py \'{"query":"关键词"}\'')
        return

    params = json.loads(sys.argv[1])
    query = params.get("query", "")
    max_results = params.get("max_results", 20)

    client = Search360Client(headless=True)
    try:
        client.start()
        results = client.search_image(query, max_results)
        print(json.dumps(results, ensure_ascii=False, indent=2))
    finally:
        client.stop()


if __name__ == "__main__":
    main()
