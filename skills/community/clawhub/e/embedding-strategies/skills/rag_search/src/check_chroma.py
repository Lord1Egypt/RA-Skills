#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')

import chromadb

# Connect to Chroma
client = chromadb.PersistentClient(path="C:/Users/Xiabi/.openclaw/workspace/chroma_db")

# List collections
collections = client.list_collections()
print(f"Collections: {len(collections)}")
for coll in collections:
    print(f"  - {coll.name}")
    
    # Get collection stats
    try:
        count = coll.count()
        print(f"    Document count: {count}")
        
        # Peek at first few documents
        if count > 0:
            peek = coll.peek(limit=3)
            print(f"    First 3 IDs: {peek['ids'][:3]}")
    except Exception as e:
        print(f"    Error: {e}")

# Try to get the collection we created
try:
    collection = client.get_collection("openclaw_memory")
    count = collection.count()
    print(f"\nopenclaw_memory collection: {count} documents")
    
    # Try a query
    from search import AliyunEmbeddings
    import os
    embeddings = AliyunEmbeddings(api_key=os.getenv("ALIYUN_API_KEY"))
    query_emb = embeddings.embed_query("瀑布")
    
    result = collection.query(query_embeddings=[query_emb], n_results=5)
    print(f"Query results: {len(result['ids'][0])}")
    if result['documents'] and result['documents'][0]:
        for i, doc in enumerate(result['documents'][0]):
            print(f"  {i+1}. {doc[:100]}")
    
except Exception as e:
    print(f"Error accessing collection: {e}")
    import traceback
    traceback.print_exc()
