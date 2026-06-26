#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
企业知识库查询脚本 - 使用Dify风格的父子检索策略
"""

import os
import sys
from pathlib import Path

# 添加src目录到Python路径
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

def main():
    print("=" * 70)
    print("🔍 企业知识库查询系统 (Dify风格父子检索)")
    print("=" * 70)
    
    try:
        # 设置API密钥
        api_key = os.getenv("DASHSCOPE_API_KEY")
        if not api_key:
            print("⚠️ 未设置 DASHSCOPE_API_KEY 环境变量")
            print("请设置环境变量: export DASHSCOPE_API_KEY='your-api-key'")
            return
        
        # 导入模块
        from src import load_config, ChromaVectorDB, Embedder
        from src.advanced_retriever import AdvancedRetriever, RetrievalConfig, RetrievalMode
        
        # 加载配置
        config = load_config()
        
        # 初始化组件
        db = ChromaVectorDB(
            collection_name=config.collection_name
        )
        
        embedder = Embedder(
            model=config.embedding_model,
            api_key=config.embedding_api_key,
            provider=config.embedding_provider,
            base_url=config.embedding_base_url
        )
        
        # 创建高级检索器 - 使用父子检索模式
        retrieval_config = RetrievalConfig(
            mode=RetrievalMode.PARENT_CHILD,
            top_k=3,
            vector_threshold=0.3,
            keyword_threshold=0.2,
            final_threshold=0.2,
            child_search_top_k=15,
            parent_return_top_k=5,
            enable_diversity=True,
            max_same_document=2
        )
        
        retriever = AdvancedRetriever(db, embedder, retrieval_config)
        
        print("✅ 高级检索系统初始化完成")
        print(f"📊 检索模式: {retrieval_config.mode.value}")
        print(f"📊 子块搜索数: {retrieval_config.child_search_top_k}")
        print(f"📊 父块返回数: {retrieval_config.parent_return_top_k}")
        
        # 预定义查询列表
        predefined_queries = [
            "蓝源的核心价值观是什么？",
            "激情创业的具体要求",
            "团队合作的重要性",
            "客户导向原则",
            "细节决定成败的含义",
            "忠诚专业的要求",
            "拼搏执行的标准",
            "蓝源基本法",
            "企业文化",
            "工作原则"
        ]
        
        print("\n" + "=" * 70)
        print("🔍 预定义查询测试")
        print("=" * 70)
        
        for i, query in enumerate(predefined_queries, 1):
            print(f"\n🔍 查询 {i}: {query}")
            print("-" * 50)
            
            try:
                results = retriever.search(query, top_k=3)
                
                if results:
                    print(f"✅ 找到 {len(results)} 个相关结果:")
                    
                    for j, result in enumerate(results, 1):
                        print(f"\n[结果{j}] 相似度: {result.final_score:.3f} | 类型: {result.chunk_type}")
                        print(f"文档: {result.document_name}")
                        
                        # 显示内容摘要
                        content_preview = result.text[:150].replace('\n', ' ')
                        print(f"内容: {content_preview}...")
                        
                        # 显示匹配的关键词
                        if result.matched_keywords:
                            keywords_str = ', '.join(result.matched_keywords[:5])
                            print(f"匹配词: {keywords_str}")
                        
                        # 显示子块信息（如果是父块）
                        if result.chunk_type == "parent" and result.child_ids:
                            print(f"包含子块: {len(result.child_ids)} 个")
                else:
                    print("❌ 未找到相关结果")
                    
            except Exception as e:
                print(f"❌ 查询失败: {e}")
        
        print("\n" + "=" * 70)
        print("💬 交互式查询 (输入 'quit' 退出)")
        print("=" * 70)
        
        while True:
            try:
                query = input("\n🤔 请输入你的问题: ").strip()
                
                if query.lower() in ['quit', 'exit', '退出', 'q']:
                    print("👋 再见！")
                    break
                
                if not query:
                    continue
                
                print(f"\n🔍 搜索: {query}")
                print("-" * 40)
                
                results = retriever.search(query, top_k=3)
                
                if results:
                    print(f"✅ 找到 {len(results)} 个相关结果:")
                    
                    for i, result in enumerate(results, 1):
                        print(f"\n[结果{i}] 相似度: {result.final_score:.3f}")
                        print(f"类型: {result.chunk_type} | 文档: {result.document_name}")
                        
                        # 智能内容显示
                        if len(result.text) <= 200:
                            print(f"内容: {result.text}")
                        else:
                            # 显示前后部分
                            start_part = result.text[:100]
                            end_part = result.text[-100:]
                            print(f"内容: {start_part}...{end_part}")
                        
                        if result.matched_keywords:
                            keywords_str = ', '.join(result.matched_keywords[:3])
                            print(f"匹配词: {keywords_str}")
                else:
                    print("❌ 未找到相关结果，请尝试其他关键词")
                    
            except KeyboardInterrupt:
                print("\n👋 再见！")
                break
            except Exception as e:
                print(f"❌ 查询出错: {e}")
    
    except Exception as e:
        print(f"❌ 系统初始化失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()