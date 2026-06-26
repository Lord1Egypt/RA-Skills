#!/usr/bin/env python3
import sys, os
os.environ['ALIYUN_API_KEY'] = 'sk-1f3847debc3e492e81f64115b20c6d82'
os.environ['CHROMA_PERSIST_DIR'] = 'chroma_db'
sys.path.insert(0, 'skills')
from rag_search.src.search import search_memories

print("Quick Test Results:")
print("=" * 50)

tests = [
    ("waterfall", 3),
    ("TTS", 3),
    ("embedding", 3),
]

for query, k in tests:
    results = search_memories(query, k=k)
    status = "OK" if results else "FAIL"
    print(f"{status}: '{query}' -> {len(results)} results")

print("=" * 50)
print("All tests passed!" if all(search_memories(q, 3) for q, _ in tests) else "Some tests failed")
