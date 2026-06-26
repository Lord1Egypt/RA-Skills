#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Debug Search Step by Step"""

import os
import sys
sys.path.insert(0, 'skills')

os.environ['ALIYUN_API_KEY'] = 'sk-1f3847debc3e492e81f64115b20c6d82'
os.environ['CHROMA_PERSIST_DIR'] = 'chroma_db'

from langchain_chroma import Chroma
from rag_search.src.search import AliyunEmbeddings

print("=" * 60)
print("Debug Search Step by Step")
print("=" * 60)

# Step 1: Generate query embedding
print("\n[Step 1] Generate query embedding...")
embeddings = AliyunEmbeddings(api_key='sk-1f3847debc3e492e81f64115b20c6d82')
query = "waterfall"
query_embedding = embeddings.embed_query(query)

print(f"  Query: '{query}'")
print(f"  Embedding length: {len(query_embedding)}")
print(f"  First 5 values: {query_embedding[:5]}")

if not query_embedding:
    print("  [ERROR] Embedding is empty!")
    sys.exit(1)

# Step 2: Load vector store WITH EMBEDDING FUNCTION
print("\n[Step 2] Load vector store...")
db = Chroma(
    persist_directory="chroma_db", 
    collection_name="openclaw_memory",
    embedding_function=embeddings  # MUST use same embedding as indexing!
)
print(f"  Collection loaded with Aliyun embeddings (1024 dim)")

# Step 3: Search
print("\n[Step 3] Search...")
try:
    results = db.similarity_search_with_score(query, k=3)
    print(f"  Found {len(results)} results")
    
    for i, (doc, score) in enumerate(results, 1):
        similarity = 1 - score
        print(f"  {i}. Score: {score:.4f}, Similarity: {similarity:.4f}")
        print(f"     Source: {doc.metadata.get('source', 'N/A')}")
        print(f"     Preview: {doc.page_content[:100]}...")
except Exception as e:
    print(f"  [ERROR] Search failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
