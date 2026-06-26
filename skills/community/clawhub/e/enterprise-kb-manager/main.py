#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
企业知识库技能主入口 - OpenClaw Skills
支持对话式文档上传和智能问答
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

def setup_shared_environment():
    """设置共享环境（仅在需要时）"""
    from src.system_config import get_system_kb_path
    
    system_path = get_system_kb_path()
    
    # 如果系统目录不存在，则创建
    if not os.path.exists(system_path):
        print("🔧 首次运行，正在设置系统知识库环境...")
        from setup_shared import setup_system_kb
        setup_system_kb()

def main():
    """主函数 - OpenClaw 技能入口点"""
    
    # 首次运行时自动设置共享环境
    setup_shared_environment()
    
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
        elif command == "upload":
            handle_upload_command()
        elif command == "query":
            handle_query_command()
        elif command == "list":
            handle_list_command()
        elif command == "stats":
            handle_stats_command()
        elif command == "delete":
            handle_delete_command()
        elif command == "setup":
            handle_setup_command()
        elif command == "test":
            handle_test_command()
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
    print("🤖 企业知识库对话模式")
    print("=" * 50)
    print("💡 使用说明:")
    print("- 上传文档: 'upload:/path/to/file.pdf 上传到知识库'")
    print("- 查询知识: 直接提问")
    print("- 退出: 输入 'quit' 或 'exit'")
    print("=" * 50)
    
    from src.chat_interface import ChatInterface
    
    interface = ChatInterface()
    
    while True:
        try:
            user_input = input("\n🤔 你: ").strip()
            
            if user_input.lower() in ['quit', 'exit', '退出', 'q']:
                print("👋 再见！")
                break
            
            if not user_input:
                continue
            
            # 检查是否是上传命令
            file_path = None
            message = user_input
            
            if user_input.startswith("upload:"):
                parts = user_input.split(" ", 1)
                if len(parts) >= 2:
                    file_path = parts[0][7:]  # 移除 "upload:" 前缀
                    message = parts[1]
                else:
                    file_path = parts[0][7:]
                    message = "上传到知识库"
            
            # 处理消息
            result = interface.process_message(message, file_path)
            print(f"🤖 助手: {result['message']}")
            
        except KeyboardInterrupt:
            print("\n👋 再见！")
            break
        except Exception as e:
            print(f"❌ 处理失败: {e}")

def handle_upload_command():
    """处理上传命令"""
    if len(sys.argv) < 3:
        print("❌ 用法: python main.py upload <文件路径> [文档名称]")
        return
    
    file_path = sys.argv[2]
    document_name = sys.argv[3] if len(sys.argv) > 3 else None
    
    print(f"📤 上传文档: {file_path}")
    
    from src import load_config, DocumentProcessor
    
    config = load_config()
    processor = DocumentProcessor(config)
    
    result = processor.process_document(file_path, document_name)
    
    if result.success:
        print(f"✅ {result.message}")
        print(f"🆔 文档ID: {result.document_id}")
        print(f"📊 创建块数: {result.chunk_count}")
    else:
        print(f"❌ 上传失败: {result.error}")

def handle_query_command():
    """处理查询命令"""
    if len(sys.argv) < 3:
        print("❌ 用法: python main.py query <查询内容>")
        return
    
    query = " ".join(sys.argv[2:])
    
    print(f"🔍 查询: {query}")
    
    from src import load_config, ChromaVectorDB, Embedder
    from src.advanced_retriever import AdvancedRetriever, RetrievalConfig, RetrievalMode
    
    config = load_config()
    
    db = ChromaVectorDB(
        collection_name=config.collection_name
    )
    
    embedder = Embedder(
        model=config.embedding_model,
        api_key=config.embedding_api_key,
        provider=config.embedding_provider,
        base_url=config.embedding_base_url
    )
    
    retrieval_config = RetrievalConfig(
        mode=RetrievalMode.HYBRID,
        top_k=3,
        enable_rerank=True,
        rerank_model="gte-rerank-v2"
    )
    
    retriever = AdvancedRetriever(db, embedder, retrieval_config)
    
    results = retriever.search(query, top_k=3)
    
    if results:
        print(f"✅ 找到 {len(results)} 个相关结果:")
        for i, result in enumerate(results, 1):
            print(f"\n[结果{i}] 相似度: {result.final_score:.3f}")
            print(f"文档: {result.document_name}")
            content_preview = result.text[:200].replace('\n', ' ')
            print(f"内容: {content_preview}...")
            if result.matched_keywords:
                keywords_str = ', '.join(result.matched_keywords[:3])
                print(f"匹配词: {keywords_str}")
    else:
        print("❌ 未找到相关结果")

def handle_list_command():
    """处理列表命令"""
    print("📚 知识库文档列表")
    
    from src import load_config, ChromaVectorDB
    from src.manager import KnowledgeBaseManager
    
    config = load_config()
    db = ChromaVectorDB(
        collection_name=config.collection_name
    )
    
    manager = KnowledgeBaseManager(db, config.documents_dir)
    documents = manager.list_documents()
    
    if documents:
        print(f"📊 总计: {len(documents)} 个文档\n")
        for i, doc in enumerate(documents, 1):
            print(f"{i}. 📄 {doc['document_name']}")
            print(f"   🆔 ID: {doc['document_id']}")
            print(f"   📦 块数: {doc['chunk_count']}")
            print()
    else:
        print("📭 知识库为空")

def handle_stats_command():
    """处理统计命令"""
    print("📊 知识库统计信息")
    
    from src import load_config, ChromaVectorDB
    from src.manager import KnowledgeBaseManager
    
    config = load_config()
    db = ChromaVectorDB(
        collection_name=config.collection_name
    )
    
    manager = KnowledgeBaseManager(db, config.documents_dir)
    stats = manager.get_statistics()
    
    print(f"📄 文档数量: {stats.get('document_count', 0)}")
    print(f"📦 文档块数: {stats.get('chunk_count', 0)}")
    print(f"💾 存储大小: {stats.get('total_size_mb', 0)} MB")
    print(f"📁 文件数量: {stats.get('stored_files', 0)}")

def handle_delete_command():
    """处理删除命令"""
    if len(sys.argv) < 3:
        print("❌ 用法: python main.py delete <文档ID>")
        return
    
    document_id = sys.argv[2]
    
    print(f"🗑️ 删除文档: {document_id}")
    
    from src import load_config, ChromaVectorDB
    from src.manager import KnowledgeBaseManager
    
    config = load_config()
    db = ChromaVectorDB(
        collection_name=config.collection_name
    )
    
    manager = KnowledgeBaseManager(db, config.documents_dir)
    result = manager.delete_document(document_id)
    
    print(result['message'])

def handle_setup_command():
    """处理设置命令"""
    print("🔧 设置系统知识库环境")
    
    from setup_shared import setup_system_kb
    system_path = setup_system_kb()
    
    print(f"✅ 设置完成！系统目录: {system_path}")
    print("💡 现在可以使用其他命令管理知识库了")

def handle_test_command():
    """处理测试命令"""
    print("🧪 运行系统测试")
    
    # 导入并运行测试
    try:
        import subprocess
        result = subprocess.run([sys.executable, "test_system.py"], 
                              cwd=current_dir, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("错误输出:", result.stderr)
    except Exception as e:
        print(f"❌ 测试失败: {e}")

def print_help():
    """打印帮助信息"""
    print("🔧 企业知识库技能 - 使用说明")
    print("=" * 50)
    print("📋 可用命令:")
    print()
    print("  chat                    - 进入对话模式")
    print("  upload <文件> [名称]     - 上传文档到知识库")
    print("  query <查询内容>        - 查询知识库")
    print("  list                   - 列出所有文档")
    print("  stats                  - 显示统计信息")
    print("  delete <文档ID>         - 删除文档")
    print("  setup                  - 设置系统知识库环境")
    print("  test                   - 运行系统测试")
    print("  help                   - 显示此帮助")
    print()
    print("💡 示例:")
    print("  python main.py chat")
    print("  python main.py upload company_policy.pdf 公司政策")
    print("  python main.py query 休假政策是什么")
    print("  python main.py setup")
    print("  python main.py list")
    print()
    print("🔗 OpenClaw 集成:")
    print("  在 OpenClaw 中使用: @kb-manager <命令>")

if __name__ == "__main__":
    main()