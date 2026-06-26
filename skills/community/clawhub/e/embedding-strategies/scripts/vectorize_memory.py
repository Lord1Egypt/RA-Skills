#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw Memory Vectorization Script
Convert memory/*.md files to vectors and store in Chroma DB
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# Import dependencies
try:
    from langchain_chroma import Chroma
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_core.documents import Document
    import dashscope
    from dashscope import TextEmbedding
except ImportError as e:
    print(f"[ERROR] Missing package: {e}")
    print("Run: pip install langchain langchain-chroma dashscope langchain-text-splitters")
    sys.exit(1)


class AliyunEmbeddings:
    """Aliyun Embedding Wrapper"""
    
    def __init__(self, api_key: str, model: str = "text-embedding-v3"):
        dashscope.api_key = api_key
        self.model = model
    
    def embed_documents(self, texts: list) -> list:
        """Batch generate embeddings (max 10 per batch)"""
        all_embeddings = []
        batch_size = 10
        
        # Process in batches of 10
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i+batch_size]
            try:
                response = TextEmbedding.call(
                    model=self.model,
                    input=batch
                )
                if response.status_code == 200:
                    embeddings = [item["embedding"] for item in response.output["embeddings"]]
                    all_embeddings.extend(embeddings)
                    print(f"  Progress: {min(i+batch_size, len(texts))}/{len(texts)}")
                else:
                    print(f"[WARN] API Error: {response.code} - {response.message}")
            except Exception as e:
                print(f"[WARN] Embedding Error: {e}")
        
        return all_embeddings
    
    def embed_query(self, query: str) -> list:
        """Generate query embedding"""
        result = self.embed_documents([query])
        return result[0] if result else []


def load_memory_files(workspace: str) -> list:
    """Load OpenClaw memory files"""
    memory_dir = Path(workspace) / "memory"
    documents = []
    
    print(f"[INFO] Scanning memory directory: {memory_dir}")
    
    # Read daily notes
    md_files = list(memory_dir.glob("*.md"))
    print(f"[INFO] Found {len(md_files)} memory files")
    
    for file in md_files:
        try:
            content = file.read_text(encoding="utf-8")
            if len(content.strip()) > 0:  # Skip empty files
                documents.append(Document(
                    page_content=content,
                    metadata={
                        "source": f"memory/{file.name}",
                        "type": "daily",
                        "date": file.stem,
                        "loaded_at": datetime.now().isoformat()
                    }
                ))
        except Exception as e:
            print(f"[WARN] Failed to read {file.name}: {e}")
    
    # Read MEMORY.md (long-term memory)
    memory_file = Path(workspace) / "MEMORY.md"
    if memory_file.exists():
        try:
            content = memory_file.read_text(encoding="utf-8")
            documents.append(Document(
                page_content=content,
                metadata={
                    "source": "MEMORY.md",
                    "type": "longterm",
                    "loaded_at": datetime.now().isoformat()
                }
            ))
            print("[INFO] Found MEMORY.md")
        except Exception as e:
            print(f"[WARN] Failed to read MEMORY.md: {e}")
    
    return documents


def split_documents(documents: list, chunk_size: int = 512, chunk_overlap: int = 50) -> list:
    """Split text into chunks"""
    print(f"[INFO] Splitting text (chunk_size={chunk_size}, overlap={chunk_overlap})")
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    
    chunks = splitter.split_documents(documents)
    print(f"[OK] Split complete: {len(documents)} docs -> {len(chunks)} chunks")
    
    return chunks


def create_vectorstore(chunks: list, embeddings, persist_dir: str, collection_name: str = "openclaw_memory"):
    """Create vector database"""
    print(f"[INFO] Creating vector database: {persist_dir}")
    
    # Delete existing collection to avoid dimension mismatch
    import chromadb
    client = chromadb.PersistentClient(path=persist_dir)
    try:
        client.delete_collection(collection_name)
        print(f"[INFO] Deleted existing collection: {collection_name}")
    except:
        pass
    
    # Create or load vector store
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_dir,
        collection_name=collection_name
    )
    
    print(f"[OK] Vector database created!")
    print(f"   - Location: {persist_dir}")
    print(f"   - Collection: {collection_name}")
    print(f"   - Documents: {len(chunks)}")
    
    return vectorstore


def main():
    """Main function"""
    print("=" * 60)
    print("OpenClaw Memory Vectorization Script")
    print("=" * 60)
    print()
    
    # Configuration
    workspace = os.getenv("OPENCLAW_WORKSPACE", r"C:\Users\Xiabi\.openclaw\workspace")
    api_key = os.getenv("ALIYUN_API_KEY")
    chroma_dir = os.getenv("CHROMA_PERSIST_DIR", os.path.join(workspace, "chroma_db"))
    chunk_size = int(os.getenv("CHUNK_SIZE", "512"))
    chunk_overlap = int(os.getenv("CHUNK_OVERLAP", "50"))
    
    # Check API Key
    if not api_key:
        print("[ERROR] Missing ALIYUN_API_KEY environment variable")
        print("Set: $env:ALIYUN_API_KEY='sk-xxx'")
        return 1
    
    print(f"[CONFIG]")
    print(f"   - Workspace: {workspace}")
    print(f"   - Chroma DB: {chroma_dir}")
    print(f"   - Chunk Size: {chunk_size}")
    print()
    
    # 1. Load memory files
    print("[1/4] Loading memory files...")
    documents = load_memory_files(workspace)
    if not documents:
        print("[ERROR] No memory files found")
        return 1
    print(f"[OK] Loaded {len(documents)} documents")
    print()
    
    # 2. Split text
    print("[2/4] Splitting text...")
    chunks = split_documents(documents, chunk_size, chunk_overlap)
    print()
    
    # 3. Generate embeddings
    print("[3/4] Generating embeddings (calling Aliyun API)...")
    embeddings = AliyunEmbeddings(api_key=api_key)
    print()
    
    # 4. Create vector store
    print("[4/4] Creating vector database...")
    vectorstore = create_vectorstore(chunks, embeddings, chroma_dir)
    print()
    
    # Test search
    print("[TEST] Vector search test...")
    test_query = "waterfall"
    print(f"   Query: '{test_query}'")
    
    try:
        results = vectorstore.similarity_search(test_query, k=3)
        if results:
            print(f"   [OK] Found {len(results)} results:")
            for i, doc in enumerate(results, 1):
                source = doc.metadata.get("source", "Unknown")
                preview = doc.page_content[:100].replace("\n", " ")
                print(f"   {i}. [{source}] {preview}...")
        else:
            print("   [WARN] No results found")
    except Exception as e:
        print(f"   [WARN] Search test failed: {e}")
    
    print()
    print("=" * 60)
    print("Vectorization Complete!")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
