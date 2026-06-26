#!/usr/bin/env python3
import sys
sys.path.insert(0, r"C:\Users\Xiabi\.openclaw\workspace\skills\rag_search\src")

from search import MemorySearcher

# Create searcher
searcher = MemorySearcher()

print(f"Collection: {searcher.vectorstore._collection.name}")
print(f"Count: {searcher.vectorstore._collection.count()}")

# Test search
results = searcher.search("瀑布", k=3, score_threshold=0.0)
print(f"Search results: {len(results)}")
for r in results:
    source = r['source'].split('\\')[-1]
    print(f"  - {source}: {r['preview'][:50]}")
