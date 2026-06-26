#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
向量化现有内容并存入 ChromaDB
使用阿里云 Embedding-v3
"""

import os
import sys
import dashscope
from dashscope import TextEmbedding
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from pathlib import Path
import json

# 配置
DASHSCOPE_API_KEY = "sk-1f3847debc3e492e81f64115b20c6d82"
CHROMA_PERSIST_DIR = "C:/Users/Xiabi/.openclaw/workspace/chroma_db"
WORKSPACE_DIR = "C:/Users/Xiabi/.openclaw/workspace"

dashscope.api_key = DASHSCOPE_API_KEY

# 文件列表
files_to_vectorize = [
    ("USER.md", "user_preference"),
    ("MEMORY.md", "longterm_memory"),
    ("best_practices.jsonl", "best_practice"),
]

# 添加 memory/*.md 文件
memory_dir = Path(WORKSPACE_DIR) / "memory"
if memory_dir.exists():
    for md_file in memory_dir.glob("*.md"):
        files_to_vectorize.append((f"memory/{md_file.name}", "daily_memory"))

# 添加 knowledge/**/*.md 文件
knowledge_dir = Path(WORKSPACE_DIR) / "knowledge"
if knowledge_dir.exists():
    for md_file in knowledge_dir.rglob("*.md"):
        files_to_vectorize.append((f"knowledge/{md_file.relative_to(knowledge_dir).as_posix()}", "knowledge"))

print(f"📊 待向量化文件：{len(files_to_vectorize)} 个")

# 文本分块
splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=50,
    separators=["\n\n", "\n", ". ", " ", ""]
)

# 读取文件并分块
documents = []
for file_path, doc_type in files_to_vectorize:
    full_path = Path(WORKSPACE_DIR) / file_path
    if not full_path.exists():
        print(f"⚠️  文件不存在：{file_path}")
        continue
    
    try:
        content = full_path.read_text(encoding='utf-8')
        chunks = splitter.split_text(content)
        
        for i, chunk in enumerate(chunks):
            documents.append(Document(
                page_content=chunk,
                metadata={
                    "source": file_path,
                    "type": doc_type,
                    "chunk": i
                }
            ))
        
        print(f"✅ {file_path}: {len(chunks)} 个块")
    except Exception as e:
        print(f"❌ {file_path} 读取失败：{e}")

print(f"\n📊 总文档块数：{len(documents)}")

# 批量生成向量（阿里云 API 每次最多 10 个）
print("\n🧠 开始生成向量...")
all_texts = [doc.page_content for doc in documents]
all_embeddings = []

for i in range(0, len(all_texts), 10):
    batch = all_texts[i:i+10]
    try:
        response = TextEmbedding.call(
            model="text-embedding-v3",
            input=batch
        )
        
        if response.status_code == 200:
            embeddings = [item["embedding"] for item in response.output["embeddings"]]
            all_embeddings.extend(embeddings)
            print(f"  进度：{min(i+10, len(all_texts))}/{len(all_texts)} ({len(all_embeddings)} 个向量)")
        else:
            print(f"  ❌ API 错误：{response.code} - {response.message}")
    except Exception as e:
        print(f"  ❌ 错误：{e}")

print(f"\n✅ 向量生成完成：{len(all_embeddings)} 个向量")

# 存入 ChromaDB
print(f"\n💾 存入 ChromaDB: {CHROMA_PERSIST_DIR}")

# 删除旧集合（避免维度不匹配）
import chromadb
client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
try:
    client.delete_collection("user_preferences")
    print("  ✅ 已删除旧集合")
except:
    print("  ℹ️  旧集合不存在")

# 创建新集合并添加数据
db = Chroma(
    persist_directory=CHROMA_PERSIST_DIR,
    collection_name="user_preferences"
)

# 添加文档和向量
db.add_documents(documents=documents, embeddings=all_embeddings)

print(f"\n✅ ChromaDB 存储完成！")
print(f"   向量数量：{db._collection.count()}")
print(f"   向量维度：{len(all_embeddings[0]) if all_embeddings else 0}")

# 测试搜索
print(f"\n🧪 测试语义搜索...")
test_queries = ["瀑布", "TTS", "供应商", "表情图片", "向量数据库"]

for query in test_queries:
    try:
        # 生成查询向量
        query_response = TextEmbedding.call(model="text-embedding-v3", input=query)
        query_embedding = query_response.output["embeddings"][0]["embedding"]
        
        # 搜索
        results = db.similarity_search_by_vector(query_embedding, k=2)
        
        print(f"\n  查询：'{query}'")
        for i, doc in enumerate(results, 1):
            source = doc.metadata.get("source", "Unknown")
            preview = doc.page_content[:80].replace("\n", " ")
            print(f"    {i}. [{source}] {preview}...")
    except Exception as e:
        print(f"  ❌ '{query}' 搜索失败：{e}")

print(f"\n🎉 向量化完成！")
