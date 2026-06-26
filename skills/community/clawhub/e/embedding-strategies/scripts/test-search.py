#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""向量搜索测试脚本"""

from langchain_chroma import Chroma

print("=" * 60)
print("Vector Search Test")
print("=" * 60)

# 加载向量库
db = Chroma(
    persist_directory="chroma_db",
    collection_name="openclaw_memory"
)

# 测试查询
test_queries = ["瀑布", "TTS", "记忆", "阿里云"]

for query in test_queries:
    print(f"\nQuery: '{query}'")
    results = db.similarity_search(query, k=3)
    print(f"Found {len(results)} results:")
    for i, doc in enumerate(results, 1):
        source = doc.metadata.get("source", "Unknown")
        preview = doc.page_content[:80].replace("\n", " ")
        print(f"  {i}. [{source}] {preview}...")

print("\n" + "=" * 60)
print("Test Complete!")
print("=" * 60)
