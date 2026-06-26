#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
学术搜索统一入口 V2.0
支持百度学术和arXiv搜索
"""

import sys
import os

def print_usage():
    print("""
╔══════════════════════════════════════════════════════════════════╗
║            学术科研助手 V7.0 - 统一搜索入口                       ║
╚══════════════════════════════════════════════════════════════════╝

使用方法：
  python search.py <模式> <关键词> [参数]

模式：
  baidu / 百度    - 百度学术搜索（按引用量排序）
  arxiv           - arXiv搜索（按相关度排序）

示例：
  python search.py baidu 大模型
  python search.py baidu 人工智能 2024
  python search.py arxiv transformer
  python search.py arxiv "deep learning" 5

功能特性：
  ✅ 按引用量/相关度排序
  ✅ 自动提取核心工作和创新点
  ✅ 显示模型图（如有）
  ✅ 自动下载PDF到 ~/Desktop/papers/<关键词>/
  ✅ PDF命名规范：标题_年份_J/C.pdf（期刊J/会议C）

注意：
  - 百度学术可能触发验证码
  - arXiv API有速率限制，请勿频繁请求
""")
    sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print_usage()
    
    mode = sys.argv[1].lower()
    keyword = sys.argv[2]
    
    # 获取脚本目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    if mode in ["baidu", "百度"]:
        # 百度学术搜索
        sys.path.insert(0, script_dir)
        import main as baidu_main
        
        year = sys.argv[3] if len(sys.argv) >= 4 else None
        baidu_main.search_baidu_xueshu(keyword, year)
        
    elif mode == "arxiv":
        # arXiv搜索
        sys.path.insert(0, script_dir)
        import arxiv_search_v2 as arxiv_main
        
        max_results = int(sys.argv[3]) if len(sys.argv) >= 4 else 10
        arxiv_main.search_arxiv(keyword, max_results)
        
    else:
        print(f"❌ 未知模式：{mode}")
        print("   支持的模式：baidu / 百度 / arxiv")
        sys.exit(1)
