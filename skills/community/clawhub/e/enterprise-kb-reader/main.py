#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识库只读查询器 - AI Agent Skills
专门用于查询和读取企业知识库内容，不支持上传和管理功能
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, Any, Optional

# 添加src目录到Python路径
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

def main():
    """主函数 - OpenClaw 技能入口点"""
    
    # 解析命令行参数
    if len(sys.argv) < 2:
        print_help()
        return
    
    command = sys.argv[1].lower()
    
    try:
        # 设置默认API密钥（如果环境变量中没有）
        if not os.getenv("DASHSCOPE_API_KEY"):
            print("⚠️ 未设置 DASHSCOPE_API_KEY 环境变量")
            print("请设置环境变量: export DASHSCOPE_API_KEY='your-api-key'")
        
        if command == "chat":
            handle_chat_mode()
        elif command == "query":
            handle_query_command()
        elif command == "list":
            handle_list_command()
        elif command == "stats":
            handle_stats_command()
        elif command == "search":
            handle_search_command()
        elif command == "help":
            print_help()
        else:
            print(f"❌ 未知命令: {command}")
            print_help()
            
    except Exception as e:
        print(f"❌ 执行失败: {e}")
        import traceback
        traceback.print_exc()

def handle_chat_mode():
    """处理对话模式"""
    print("🔍 知识库只读查询器")
    print("=" * 50)
    print("💡 使用说明:")
    print("- 直接提问进行智能查询")
    print("- 输入 'list' 查看文档列表")
    print("- 输入 'stats' 查看统计信息")
    print("- 退出: 输入 'quit' 或 'exit'")
    print("=" * 50)
    
    from src.reader_interface import ReaderInterface
    
    interface = ReaderInterface()
    
    while True:
        try:
            user_input = input("\n🤔 你: ").strip()
            
            if user_input.lower() in ['quit', 'exit', '退出', 'q']:
                print("👋 再见！")
                break
            
            if not user_input:
                continue
            
            # 处理特殊命令
            if user_input.lower() == 'list':
                result = interface.list_documents()
            elif user_input.lower() == 'stats':
                result = interface.get_stats()
            else:
                # 处理查询
                result = interface.query(user_input)
            
            print(f"🤖 助手: {result}")
            
        except KeyboardInterrupt:
            print("\n👋 再见！")
            break
        except Exception as e:
            print(f"❌ 处理失败: {e}")

def handle_query_command():
    """处理查询命令"""
    if len(sys.argv) < 3:
        print("❌ 用法: python main.py query <查询内容>")
        return
    
    query = " ".join(sys.argv[2:])
    
    print(f"🔍 查询: {query}")
    
    from src.reader_interface import ReaderInterface
    
    interface = ReaderInterface()
    result = interface.query(query)
    
    print(f"🤖 结果: {result}")

def handle_search_command():
    """处理搜索命令"""
    if len(sys.argv) < 3:
        print("❌ 用法: python main.py search <搜索内容>")
        return
    
    query = " ".join(sys.argv[2:])
    
    print(f"🔍 搜索: {query}")
    
    from src.reader_interface import ReaderInterface
    
    interface = ReaderInterface()
    result = interface.search_detailed(query)
    
    print(result)

def handle_list_command():
    """处理列表命令"""
    print("📚 知识库文档列表")
    
    from src.reader_interface import ReaderInterface
    
    interface = ReaderInterface()
    result = interface.list_documents()
    
    print(result)

def handle_stats_command():
    """处理统计命令"""
    print("📊 知识库统计信息")
    
    from src.reader_interface import ReaderInterface
    
    interface = ReaderInterface()
    result = interface.get_stats()
    
    print(result)

def print_help():
    """打印帮助信息"""
    print("🔍 知识库只读查询器 - 使用说明")
    print("=" * 50)
    print("📋 可用命令:")
    print()
    print("  chat                    - 进入对话模式")
    print("  query <查询内容>        - 查询知识库")
    print("  search <搜索内容>       - 详细搜索")
    print("  list                   - 列出所有文档")
    print("  stats                  - 显示统计信息")
    print("  help                   - 显示此帮助")
    print()
    print("💡 示例:")
    print("  python main.py chat")
    print("  python main.py query 休假政策是什么")
    print("  python main.py search 蓝源军规")
    print("  python main.py list")
    print()
    print("🔗 OpenClaw 集成:")
    print("  在 OpenClaw 中使用: @kb-reader <命令>")
    print()
    print("⚠️  注意: 此工具仅支持只读操作，无法上传或修改文档")

if __name__ == "__main__":
    main()