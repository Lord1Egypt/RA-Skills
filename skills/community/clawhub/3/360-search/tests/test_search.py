#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
360 搜索测试
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from search_client import Search360Client


def test_search():
    client = Search360Client(headless=True)
    try:
        client.start()
        results = client.search("Python 编程", max_results=5)
        assert len(results) > 0, "搜索结果不应为空"
        print(f"✅ test_search: 找到 {len(results)} 条结果")
        return True
    except Exception as e:
        print(f"❌ test_search: {e}")
        return False
    finally:
        client.stop()


def test_news():
    client = Search360Client(headless=True)
    try:
        client.start()
        results = client.search_news("人工智能", max_results=5)
        print(f"✅ test_news: 找到 {len(results)} 条新闻")
        return True
    except Exception as e:
        print(f"❌ test_news: {e}")
        return False
    finally:
        client.stop()


if __name__ == "__main__":
    print("运行 360 搜索测试...")
    test_search()
    test_news()
    print("测试完成")
