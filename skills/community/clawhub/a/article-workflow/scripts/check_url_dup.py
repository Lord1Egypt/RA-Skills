#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文章 URL 去重检查工具（混合去重）

用法：
  python check_url_dup.py <url>
  python check_url_dup.py <url> --check-content <title>
  python check_url_dup.py <url> --add <title> <record_id> <doc_url>

返回：0=新 URL，1=重复 URL

注意：此工具可独立运行，不需要 OpenClaw 环境
"""

import sys
from pathlib import Path

# 模块路径（相对路径）
SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
CORE_DIR = SKILL_DIR / "core"

# 导入核心模块
sys.path.insert(0, str(CORE_DIR))
from dedup import check_duplicate, add_url_to_cache

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：")
        print("  python check_url_dup.py <url>")
        print("  python check_url_dup.py <url> --check-content <title>")
        print("  python check_url_dup.py <url> --add <title> <record_id> <doc_url>")
        sys.exit(1)
    
    url = sys.argv[1]
    
    # 模式 1: 添加
    if len(sys.argv) >= 6 and sys.argv[2] == "--add":
        title = sys.argv[3]
        record_id = sys.argv[4]
        doc_url = sys.argv[5]
        add_url_to_cache(url, title, record_id, doc_url)
        print(f"✅ URL 已添加到缓存：{url}")
        print(f"   标题：{title}")
        sys.exit(0)
    
    # 模式 2: 检查（带内容指纹）
    if len(sys.argv) >= 4 and sys.argv[2] == "--check-content":
        title = sys.argv[3]
        result = check_duplicate(url, title=title, content="")
        
        if result["is_duplicate"]:
            print(f"⚠️ 重复内容！")
            print(f"   检测类型：{result['check_type']}")
            print(f"   标准化 URL: {result['normalized_url']}")
            print(f"   标题：{result['record']['title']}")
            print(f"   文档：{result['record']['doc_url']}")
            sys.exit(1)
        else:
            print(f"✅ 新内容")
            print(f"   标准化 URL: {result['normalized_url']}")
            sys.exit(0)
    
    # 模式 3: 仅检查 URL
    result = check_duplicate(url)
    
    if result["is_duplicate"]:
        print(f"⚠️ 重复 URL！")
        print(f"   检测类型：{result['check_type']}")
        print(f"   标准化 URL: {result['normalized_url']}")
        print(f"   标题：{result['record']['title']}")
        print(f"   文档：{result['record']['doc_url']}")
        sys.exit(1)
    else:
        print(f"✅ 新 URL")
        print(f"   标准化 URL: {result['normalized_url']}")
        sys.exit(0)
