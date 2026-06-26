#!/usr/bin/env python3
"""
Semantic Memory - Vector-based memory search
Indexes memory files and allows meaning-based search
"""

import os
import sys
import json
import hashlib
from pathlib import Path
from datetime import datetime

try:
    from chromadb import PersistentClient
    from chromadb.utils.embedding_functions import DefaultEmbeddingFunction
    CHROMA_AVAILABLE = True
except ImportError:
    CHROMA_AVAILABLE = False
    print("⚠️  ChromaDB not available, using simple text search")

TOOL_DIR = Path.home() / ".openclaw" / "semantic-memory"
MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"
DATA_DIR = TOOL_DIR / "data"
LOG_FILE = TOOL_DIR / "memory.log"
COLLECTION_NAME = "memories"

# Use ChromaDB's built-in embedding function (no API key needed)
EMBEDDING_FUNCTION = DefaultEmbeddingFunction()

def ensure_dirs():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(MEMORY_DIR, exist_ok=True)
    os.chmod(DATA_DIR, 0o755)

def log(msg):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] {msg}")
    ensure_dirs()
    with open(LOG_FILE, 'a') as f:
        f.write(f"[{timestamp}] {msg}\n")

def get_embedding(text):
    """Get embedding using ChromaDB's built-in model (no API key needed)"""
    try:
        return EMBEDDING_FUNCTION([text])[0]
    except Exception as e:
        log(f"Embedding error: {e}")
        return None

def init_chroma():
    """Initialize ChromaDB"""
    if not CHROMA_AVAILABLE:
        return None
    ensure_dirs()
    try:
        return PersistentClient(path=str(DATA_DIR))
    except Exception as e:
        log(f"ChromaDB init error: {e}")
        return None

def index_memories():
    """Index all memory files"""
    client = init_chroma()
    if client is None:
        log("No ChromaDB - skipping index")
        return 0
    
    collection = client.get_or_create_collection(COLLECTION_NAME)
    count = 0
    
    for mem_file in MEMORY_DIR.glob("*.md"):
        doc_id = f"{mem_file.stem}"
        
        with open(mem_file, 'r') as f:
            content = f.read()
        
        # Check if already indexed
        try:
            existing = collection.get(ids=[doc_id])
            if existing and existing.get('ids'):
                continue
        except:
            pass
        
        # Get embedding (or skip if no API key)
        embedding = get_embedding(content)
        if embedding is None:
            log(f"Skipping {mem_file.name} (no embedding)")
            continue
        
        try:
            collection.add(
                ids=[doc_id],
                embeddings=[embedding],
                documents=[content],
                metadatas=[{"file": mem_file.name, "path": str(mem_file)}]
            )
            count += 1
            log(f"Indexed: {mem_file.name}")
        except Exception as e:
            log(f"Failed to index {mem_file.name}: {e}")
    
    return count

def search_memories(query, n_results=5):
    """Search memories by meaning"""
    client = init_chroma()
    
    if client is None:
        return simple_search(query, n_results)
    
    try:
        collection = client.get_collection(COLLECTION_NAME)
    except:
        return simple_search(query, n_results)
    
    try:
        results = collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        matches = []
        if results and 'documents' in results and results['documents']:
            for i, doc in enumerate(results['documents'][0]):
                meta = {}
                if 'metadatas' in results and results['metadatas']:
                    meta = results['metadatas'][0][i] if i < len(results['metadatas'][0]) else {}
                
                matches.append({
                    'content': doc[:500] + "..." if len(doc) > 500 else doc,
                    'file': meta.get('file', 'unknown'),
                    'path': meta.get('path', '')
                })
        return matches
    except Exception as e:
        log(f"Search error: {e}")
        return simple_search(query, n_results)

def simple_search(query, n_results=5):
    """Simple keyword fallback search"""
    query_lower = query.lower()
    results = []
    
    for mem_file in MEMORY_DIR.glob("*.md"):
        with open(mem_file, 'r') as f:
            content = f.read()
        
        if query_lower in content.lower():
            idx = content.lower().index(query_lower)
            start = max(0, idx - 100)
            end = min(len(content), idx + len(query) + 200)
            snippet = content[start:end]
            
            results.append({
                'content': snippet,
                'file': mem_file.name,
                'path': str(mem_file)
            })
        
        if len(results) >= n_results:
            break
    
    return results

def add_memory(text, source="manual"):
    """Add a new memory"""
    today = datetime.now().strftime("%Y-%m-%d")
    mem_file = MEMORY_DIR / f"{today}.md"
    
    with open(mem_file, 'a') as f:
        f.write(f"\n## {datetime.now().strftime('%H:%M')} [{source}]\n")
        f.write(f"{text}\n")
    
    # Index in ChromaDB
    client = init_chroma()
    if client:
        try:
            collection = client.get_or_create_collection(COLLECTION_NAME)
            embedding = get_embedding(text)
            
            if embedding:
                file_hash = hashlib.md5(str(text).encode()).hexdigest()[:8]
                collection.add(
                    ids=[f"manual_{file_hash}"],
                    embeddings=[embedding],
                    documents=[text],
                    metadatas=[{"file": mem_file.name, "source": source}]
                )
                log(f"Added to vector DB: {mem_file.name}")
        except Exception as e:
            log(f"Index error: {e}")
    
    return mem_file.name

def show_stats():
    """Show memory stats"""
    files = list(MEMORY_DIR.glob("*.md"))
    total_size = sum(f.stat().st_size for f in files)
    
    print("\n🧠 Semantic Memory Stats")
    print("=" * 40)
    print(f"Memory files: {len(files)}")
    print(f"Total size: {total_size / 1024:.1f} KB")
    
    if CHROMA_AVAILABLE:
        client = init_chroma()
        if client:
            try:
                collection = client.get_collection(COLLECTION_NAME)
                print(f"Indexed entries: {collection.count()}")
            except:
                print("Indexed entries: 0")
        else:
            print("ChromaDB: not initialized")
    else:
        print("ChromaDB: not available")
    
    print(f"\n📁 Memory dir: {MEMORY_DIR}")
    print(f"💾 Data dir: {DATA_DIR}")

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    
    if cmd == "index":
        print("🔄 Indexing memories...")
        count = index_memories()
        print(f"✅ Indexed {count} new memories")
        
    elif cmd == "search":
        if len(sys.argv) < 3:
            print("Usage: semantic-memory search <query>")
        else:
            query = " ".join(sys.argv[2:])
            print(f"\n🔍 Searching for: {query}\n")
            results = search_memories(query)
            if results:
                for i, r in enumerate(results, 1):
                    print(f"{i}. {r['file']}")
                    print(f"   {r['content'][:200]}...")
                    print()
            else:
                print("No results found")
                
    elif cmd == "add":
        if len(sys.argv) < 3:
            print("Usage: semantic-memory add <text>")
        else:
            text = " ".join(sys.argv[2:])
            filename = add_memory(text)
            print(f"✅ Added to {filename}")
            
    elif cmd == "stats":
        show_stats()
        
    elif cmd == "status":
        show_stats()
        print("\n💡 Commands: index | search <query> | add <text> | stats")
        
    else:
        print("Usage: semantic-memory [index|search|add|stats]")
        print("  index  - Index all memory files")
        print("  search - Search memories by meaning")
        print("  add    - Add new memory")
        print("  stats  - Show memory statistics")