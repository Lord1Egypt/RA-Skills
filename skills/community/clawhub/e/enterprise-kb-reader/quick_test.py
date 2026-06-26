#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速测试脚本
"""

import os
import sys
from pathlib import Path

# 添加src目录到Python路径
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

def main():
    # 设置API密钥
    if not os.getenv("DASHSCOPE_API_KEY"):
        print("⚠️ 未设置 DASHSCOPE_API_KEY 环境变量")
        print("请设置环境变量: export DASHSCOPE_API_KEY='your-api-key'")
        return
    
    from src.reader_interface import ReaderInterface
    
    reader = ReaderInterface()
    
    # 测试几个查询
    queries = ["蓝源", "基本法", "激情", "团队"]
    
    for query in queries:
        print(f"\n查询: {query}")
        result = reader.query(query)
        print(f"结果: {result[:100]}...")

if __name__ == "__main__":
    main()