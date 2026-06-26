#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Debug RAG Search"""

import sys
import os
sys.path.insert(0, 'skills')

os.environ['ALIYUN_API_KEY'] = 'sk-1f3847debc3e492e81f64115b20c6d82'
os.environ['CHROMA_PERSIST_DIR'] = 'chroma_db'

from rag_search.src.search import MemorySearcher

print("=" * 60)
print("Debug RAG Search")
print("=" * 60)

# Initialize searcher
searcher = MemorySearcher()

# Test with English queries first
test_queries = ["waterfall", "TTS", "memory", "embedding"]

for query in test_queries:
    print(f"\nQuery: '{query}'")
    results = searcher.search(query, k=3)
    
    if results:
        print(f"  Found {len(results)} results:")
        for i, r in enumerate(results, 1):
            print(f"  {i}. [{r['source']}] sim={r['similarity']}")
            print(f"     Preview: {r['preview'][:100]}...")
    else:
        print("  No results found")

print("\n" + "=" * 60)
