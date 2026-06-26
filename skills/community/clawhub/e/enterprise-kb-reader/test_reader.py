#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识库只读查询器测试脚本
"""

import os
import sys
from pathlib import Path

# 添加src目录到Python路径
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

def test_reader():
    """测试只读查询器"""
    print("🧪 知识库只读查询器测试")
    print("=" * 50)
    
    try:
        # 设置API密钥
        if not os.getenv("DASHSCOPE_API_KEY"):
            print("⚠️ 未设置 DASHSCOPE_API_KEY 环境变量")
            print("请设置环境变量: export DASHSCOPE_API_KEY='your-api-key'")
            return
        
        from src.reader_interface import ReaderInterface
        
        # 初始化查询器
        print("🔧 初始化查询器...")
        reader = ReaderInterface()
        print("✅ 查询器初始化成功")
        
        # 测试统计信息
        print("\n📊 测试统计信息...")
        stats = reader.get_stats()
        print(stats)
        
        # 测试文档列表
        print("\n📚 测试文档列表...")
        docs = reader.list_documents()
        print(docs)
        
        # 测试查询
        test_queries = [
            "蓝源的核心价值观",
            "激情创业",
            "团队合作",
            "客户导向"
        ]
        
        print("\n🔍 测试查询功能...")
        for query in test_queries:
            print(f"\n查询: {query}")
            print("-" * 30)
            result = reader.query(query)
            print(result[:500] + "..." if len(result) > 500 else result)
        
        print("\n✅ 所有测试完成")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_reader()