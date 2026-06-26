#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识库只读查询器使用示例
"""

import os
import sys
from pathlib import Path

# 添加src目录到Python路径
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

def main():
    """示例主函数"""
    print("🔍 知识库只读查询器使用示例")
    print("=" * 50)
    
    # 设置API密钥
    if not os.getenv("DASHSCOPE_API_KEY"):
        print("⚠️ 未设置 DASHSCOPE_API_KEY 环境变量")
        print("请设置环境变量: export DASHSCOPE_API_KEY='your-api-key'")
        return
    
    try:
        from src.reader_interface import ReaderInterface
        
        # 初始化查询器
        print("🔧 初始化查询器...")
        reader = ReaderInterface()
        print("✅ 初始化成功")
        
        # 显示统计信息
        print("\n📊 知识库统计:")
        print(reader.get_stats())
        
        # 显示文档列表
        print("\n📚 文档列表:")
        print(reader.list_documents())
        
        # 示例查询
        queries = [
            "蓝源的核心价值观是什么？",
            "激情创业的要求",
            "团队合作的重要性",
            "客户导向原则"
        ]
        
        print("\n🔍 示例查询:")
        for query in queries:
            print(f"\n查询: {query}")
            print("-" * 30)
            result = reader.query(query)
            # 只显示前200个字符
            display_result = result[:200] + "..." if len(result) > 200 else result
            print(display_result)
        
        print("\n✅ 示例完成")
        
    except Exception as e:
        print(f"❌ 示例运行失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()