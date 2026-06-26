# Simple Vectorization Test
import os
import sys
from pathlib import Path

# Set environment variables directly
os.environ['ALIYUN_API_KEY'] = 'sk-1f3847debc3e492e81f64115b20c6d82'
os.environ['CHROMA_PERSIST_DIR'] = './chroma_db'
os.environ['OPENCLAW_WORKSPACE'] = './workspace'

workspace = Path(__file__).parent

print("=" * 60)
print("MEMORY.md Vectorization Test")
print("=" * 60)

# Step 1: Check API Key
print("\n[Step 1] Check API Key...")
api_key = os.environ.get('ALIYUN_API_KEY')
if api_key and api_key.startswith('sk-'):
    print(f"[OK] ALIYUN_API_KEY configured: {api_key[:10]}...{api_key[-4:]}")
else:
    print("[ERROR] ALIYUN_API_KEY not configured")
    sys.exit(1)

# Step 2: Test Aliyun Embedding API
print("\n[Step 2] Test Aliyun Embedding API...")
try:
    import dashscope
    from dashscope import TextEmbedding
    
    response = TextEmbedding.call(
        model="text-embedding-v2",
        input="test embedding",
        api_key=api_key
    )
    
    if response.status_code == 200:
        embedding = response.output['embeddings'][0]['embedding']
        print(f"[OK] Embedding API success")
        print(f"   Model: text_embedding_v2")
        print(f"   Dimensions: {len(embedding)}")
    else:
        print(f"[ERROR] API failed: {response.code} - {response.message}")
        sys.exit(1)
        
except Exception as e:
    print(f"[ERROR] Import or call failed: {e}")
    print("   Install: pip install dashscope")
    sys.exit(1)

# Step 3: Check Chroma DB
print("\n[Step 3] Check Chroma Database...")
try:
    import chromadb
    from chromadb.config import Settings
    
    chroma_path = workspace / 'chroma_db'
    print(f"   Expected path: {chroma_path}")
    
    # Use actual chroma_db location
    actual_chroma = workspace / 'chroma_db'
    if not actual_chroma.exists():
        print(f"   Creating chroma_db directory...")
        actual_chroma.mkdir(exist_ok=True)
    
    client = chromadb.PersistentClient(path=str(actual_chroma))
    print(f"[OK] Chroma connected")
    
    collections = client.list_collections()
    print(f"   Collections: {len(collections)}")
    for col in collections:
        print(f"   - {col.name}: {col.count()} records")
    
except Exception as e:
    print(f"[ERROR] Chroma check failed: {e}")
    print("   Install: pip install langchain-chroma")
    sys.exit(1)

# Step 4: Check MEMORY.md
print("\n[Step 4] Check MEMORY.md...")
memory_path = Path.cwd() / 'MEMORY.md'
print(f"   Checking: {memory_path}")
if memory_path.exists():
    content = memory_path.read_text(encoding='utf-8')
    print(f"[OK] MEMORY.md exists")
    print(f"   Size: {len(content)} chars")
    print(f"   Path: {memory_path}")
else:
    print(f"[ERROR] MEMORY.md not found")
    sys.exit(1)

# Step 5: Vectorize
print("\n[Step 5] Vectorize MEMORY.md...")
try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_community.embeddings import DashScopeEmbeddings
    from langchain_chroma import Chroma
    
    print("   Reading MEMORY.md...")
    text = memory_path.read_text(encoding='utf-8')
    
    print("   Splitting text...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", "!", "?", " ", ""]
    )
    chunks = splitter.split_text(text)
    print(f"   Chunks: {len(chunks)}")
    
    print("   Creating embeddings...")
    embeddings = DashScopeEmbeddings(
        model="text-embedding-v2",
        dashscope_api_key=api_key
    )
    
    print("   Storing to Chroma...")
    collection_name = "openclaw_memory"
    try:
        client.delete_collection(collection_name)
        print("   Deleted old collection...")
    except:
        pass
    
    vectorstore = Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        collection_name=collection_name,
        persist_directory=str(chroma_path),
        metadatas=[{"source": "MEMORY.md", "chunk_id": i} for i in range(len(chunks))]
    )
    
    print(f"[OK] Vectorization complete")
    print(f"   Collection: {collection_name}")
    print(f"   Vectors: {vectorstore._collection.count()}")
    
except Exception as e:
    print(f"[ERROR] Vectorization failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Step 6: Test Search
print("\n[Step 6] Test Vector Search...")
try:
    query = "memory"
    print(f"   Query: \"{query}\"")
    
    results = vectorstore.similarity_search(query, k=3)
    
    print(f"[OK] Search success, found {len(results)} results")
    for i, doc in enumerate(results, 1):
        print(f"\n   Result {i}:")
        print(f"   Source: {doc.metadata.get('source', 'unknown')}")
        content = doc.page_content[:100].encode('gbk', errors='ignore').decode('gbk')
        print(f"   Content: {content}...")
        
except Exception as e:
    print(f"[ERROR] Search test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Complete
print("\n" + "=" * 60)
print("[SUCCESS] All tests passed!")
print("=" * 60)
print("\nSummary:")
print("1. [OK] Environment configured")
print("2. [OK] MEMORY.md exists")
print("3. [OK] Aliyun Embedding API works")
print("4. [OK] Chroma DB connected")
print("5. [OK] Vectorization successful")
print("6. [OK] Vector search works")
print("\nNext steps:")
print("- Run vectorize_memory.py for full vectorization")
print("- Or let agent auto-call vector search")
