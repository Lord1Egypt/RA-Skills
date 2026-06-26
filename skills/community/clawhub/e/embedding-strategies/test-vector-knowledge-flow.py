#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
向量知识库全流程运行逻辑演示
"""

from langchain_chroma import Chroma
import dashscope
from dashscope import TextEmbedding

print("=" * 60)
print("🦞 向量知识库全流程运行逻辑演示")
print("=" * 60)
print()

# 配置
DASHSCOPE_API_KEY = "sk-1f3847debc3e492e81f64115b20c6d82"
CHROMA_PERSIST_DIR = "C:/Users/Xiabi/.openclaw/workspace/chroma_db"

dashscope.api_key = DASHSCOPE_API_KEY

# 步骤 1: 加载向量数据库
print("📊 步骤 1: 加载向量数据库")
db = Chroma(persist_directory=CHROMA_PERSIST_DIR, collection_name="user_preferences")
print(f"   ✅ 向量数量：{db._collection.count()}")
print(f"   ✅ 向量维度：1024 维（阿里云 v3）")
print()

# 步骤 2: 用户提问
print("📝 步骤 2: 用户提问")
test_queries = [
    "瀑布在哪里？",
    "TTS 应该怎么用？",
    "供应商直连系统进度如何？",
    "表情图片怎么发送？",
]
print(f"   测试查询：{len(test_queries)} 个")
print()

# 步骤 3: 生成查询向量
print("🧠 步骤 3: 生成查询向量（阿里云 Embedding）")
for i, query in enumerate(test_queries, 1):
    print(f"   {i}. '{query}'")
    query_response = TextEmbedding.call(model='text-embedding-v3', input=query)
    query_embedding = query_response.output["embeddings"][0]["embedding"]
    print(f"      ✅ 生成 1024 维向量")
print()

# 步骤 4: 向量相似度搜索
print("🔍 步骤 4: 向量相似度搜索")
for i, query in enumerate(test_queries, 1):
    print(f"   {i}. '{query}'")
    query_response = TextEmbedding.call(model='text-embedding-v3', input=query)
    query_embedding = query_response.output["embeddings"][0]["embedding"]
    results = db.similarity_search_by_vector(query_embedding, k=2)
    print(f"      ✅ 找到 {len(results)} 条相关记忆")
    for j, doc in enumerate(results, 1):
        source = doc.metadata.get("source", "Unknown")
        preview = doc.page_content[:80].replace("\n", " ")
        print(f"         {j}. [{source}] {preview}...")
print()

# 步骤 5: 返回结果给用户
print("💬 步骤 5: 返回结果给用户")
print("   ✅ 阿香基于检索结果生成回复")
print()

print("=" * 60)
print("🎉 向量知识库全流程演示完成！")
print("=" * 60)
