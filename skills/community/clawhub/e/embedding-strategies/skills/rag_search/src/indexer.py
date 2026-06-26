#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Memory Indexer for OpenClaw RAG Search
Indexes all memory files into Chroma vector database
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from search import AliyunEmbeddings, MemorySearcher

try:
    from langchain_chroma import Chroma
    from langchain_core.documents import Document
except ImportError as e:
    print(f"[ERROR] Missing package: {e}")
    print("Run: pip install langchain-chroma langchain-core")
    raise


def load_memory_files(workspace_dir: str) -> List[Document]:
    """
    Load all memory markdown files
    
    Args:
        workspace_dir: Path to OpenClaw workspace
    
    Returns:
        List of Document objects
    """
    memory_dir = Path(workspace_dir) / "memory"
    documents = []
    
    if not memory_dir.exists():
        print(f"[WARN] Memory directory not found: {memory_dir}")
        return documents
    
    # Load daily memory files
    for md_file in memory_dir.glob("*.md"):
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract date from filename (YYYY-MM-DD.md)
            date_str = md_file.stem
            
            # Create document with metadata
            doc = Document(
                page_content=content,
                metadata={
                    "source": str(md_file),
                    "type": "daily_memory",
                    "date": date_str,
                    "filename": md_file.name
                }
            )
            documents.append(doc)
            print(f"[INFO] Loaded: {md_file.name}")
            
        except Exception as e:
            print(f"[ERROR] Failed to load {md_file.name}: {e}")
    
    # Load MEMORY.md if exists
    memory_md = Path(workspace_dir) / "MEMORY.md"
    if memory_md.exists():
        try:
            with open(memory_md, 'r', encoding='utf-8') as f:
                content = f.read()
            
            doc = Document(
                page_content=content,
                metadata={
                    "source": str(memory_md),
                    "type": "long_term_memory",
                    "date": "ongoing",
                    "filename": "MEMORY.md"
                }
            )
            documents.append(doc)
            print(f"[INFO] Loaded: MEMORY.md")
            
        except Exception as e:
            print(f"[ERROR] Failed to load MEMORY.md: {e}")
    
    return documents


def chunk_document(content: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """
    Split document into overlapping chunks
    
    Args:
        content: Document content
        chunk_size: Characters per chunk
        overlap: Overlap between chunks
    
    Returns:
        List of text chunks
    """
    chunks = []
    start = 0
    
    while start < len(content):
        end = start + chunk_size
        chunk = content[start:end]
        
        # Try to break at sentence boundary
        if end < len(content):
            last_period = chunk.rfind('.')
            last_newline = chunk.rfind('\n')
            break_point = max(last_period, last_newline)
            
            if break_point > chunk_size // 2:
                chunk = chunk[:break_point + 1]
                end = start + break_point + 1
        
        chunks.append(chunk.strip())
        start = end - overlap
    
    return chunks


def index_memories(workspace_dir: str, 
                   chroma_dir: str,
                   collection_name: str = "openclaw_memory",
                   api_key: str = None):
    """
    Index all memories into Chroma
    
    Args:
        workspace_dir: OpenClaw workspace path
        chroma_dir: Chroma database directory
        collection_name: Collection name
        api_key: Aliyun API key
    """
    print("=" * 60)
    print("Memory Indexer for OpenClaw")
    print("=" * 60)
    
    # Get API key
    if api_key is None:
        api_key = os.getenv("ALIYUN_API_KEY")
    
    if not api_key:
        print("[ERROR] ALIYUN_API_KEY not found")
        print("Please set environment variable or pass as argument")
        sys.exit(1)
    
    print(f"[INFO] Workspace: {workspace_dir}")
    print(f"[INFO] Chroma DB: {chroma_dir}")
    print(f"[INFO] Collection: {collection_name}")
    
    # Load documents
    print("\n[INFO] Loading memory files...")
    documents = load_memory_files(workspace_dir)
    
    if not documents:
        print("[ERROR] No documents found to index")
        sys.exit(1)
    
    print(f"[INFO] Loaded {len(documents)} files")
    
    # Chunk documents
    print("\n[INFO] Chunking documents...")
    all_chunks = []
    chunk_metadata = []
    
    for doc in documents:
        chunks = chunk_document(doc.page_content)
        for chunk in chunks:
            if len(chunk.strip()) > 20:  # Skip very short chunks
                all_chunks.append(chunk)
                chunk_metadata.append(doc.metadata.copy())
    
    print(f"[INFO] Created {len(all_chunks)} chunks")
    
    # Initialize embeddings
    print("\n[INFO] Initializing embeddings...")
    embeddings = AliyunEmbeddings(api_key=api_key)
    
    # Create/load vector store
    print(f"\n[INFO] Creating vector store...")
    
    # Delete existing collection if it exists (to avoid dimension mismatch)
    import chromadb
    client = chromadb.PersistentClient(path=chroma_dir)
    try:
        client.delete_collection(name=collection_name)
        print(f"[INFO] Deleted existing collection: {collection_name}")
    except Exception as e:
        print(f"[INFO] No existing collection to delete: {e}")
    
    # Manually generate embeddings in batches (max 10 per batch per API limit)
    print(f"[INFO] Generating embeddings for {len(all_chunks)} chunks in batches...")
    all_embeddings = []
    batch_size = 10
    
    for i in range(0, len(all_chunks), batch_size):
        batch_texts = all_chunks[i:i+batch_size]
        try:
            batch_embeddings = embeddings.embed_documents(batch_texts)
            all_embeddings.extend(batch_embeddings)
            print(f"[INFO] Embedded {min(i+batch_size, len(all_chunks))}/{len(all_chunks)} chunks")
        except Exception as e:
            print(f"[ERROR] Failed to embed batch {i//batch_size}: {e}")
            # Add zero embeddings as fallback
            all_embeddings.extend([[0.0] * 1024] * len(batch_texts))
    
    # Create Chroma collection manually
    from chromadb.api.models.Collection import Collection as ChromaCollection
    
    # Create collection with explicit metadata
    collection = client.create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine", "embedding_dimension": 1024}
    )
    
    # Add documents in batches
    print(f"[INFO] Adding {len(all_chunks)} documents to collection...")
    ids = [f"doc_{i}" for i in range(len(all_chunks))]
    collection.add(
        ids=ids,
        embeddings=all_embeddings,
        documents=all_chunks,
        metadatas=chunk_metadata
    )
    
    print(f"[INFO] Collection created successfully")
    
    # Create vectorstore wrapper
    vectorstore = Chroma(
        client=client,
        collection_name=collection_name,
        embedding_function=embeddings
    )
    
    print(f"\n[INFO] Indexing complete!")
    print(f"   - Total chunks: {len(all_chunks)}")
    print(f"   - Collection: {collection_name}")
    print(f"   - Database: {chroma_dir}")
    
    # Test search
    print("\n[INFO] Testing search...")
    test_query = "瀑布"
    results = vectorstore.similarity_search_with_score(test_query, k=3)
    
    if results:
        print(f"[SUCCESS] Found {len(results)} results for '{test_query}'")
        for i, (doc, score) in enumerate(results, 1):
            similarity = 1 - score
            print(f"  {i}. [{doc.metadata.get('filename', 'Unknown')}] (similarity: {similarity:.3f})")
            print(f"     {doc.page_content[:100]}...")
    else:
        print(f"[WARN] No results found for test query")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    # Configuration - use absolute paths
    workspace_dir = r"C:\Users\Xiabi\.openclaw\workspace"
    chroma_dir = r"C:\Users\Xiabi\.openclaw\workspace\chroma_db"
    
    # Run indexer
    index_memories(workspace_dir, chroma_dir)
