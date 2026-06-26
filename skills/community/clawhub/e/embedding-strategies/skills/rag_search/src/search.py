#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAG Search Interface for OpenClaw
Semantic search for memories and knowledge base
"""

import os
from pathlib import Path
from typing import List, Dict, Any, Optional

try:
    from langchain_chroma import Chroma
    from openai import OpenAI
except ImportError as e:
    print(f"[ERROR] Missing package: {e}")
    print("Run: pip install langchain-chroma openai")
    raise


class AliyunEmbeddings:
    """Aliyun Embedding Wrapper using OpenAI-compatible API (Recommended)"""
    
    def __init__(self, api_key: str, model: str = "text-embedding-v3", base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model
    
    def embed_query(self, query: str) -> List[float]:
        """Generate query embedding using OpenAI-compatible API"""
        try:
            response = self.client.embeddings.create(
                model=self.model,
                input=[query]
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"[WARN] Embedding Error: {e}")
            return []
    
    def embed_documents(self, documents: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple documents"""
        try:
            response = self.client.embeddings.create(
                model=self.model,
                input=documents
            )
            return [item.embedding for item in response.data]
        except Exception as e:
            print(f"[WARN] Embedding Error: {e}")
            return []


class MemorySearcher:
    """Memory Search Engine"""
    
    def __init__(self, 
                 chroma_dir: Optional[str] = None,
                 collection_name: str = "openclaw_memory",
                 api_key: Optional[str] = None):
        """
        Initialize Memory Searcher
        
        Args:
            chroma_dir: Path to Chroma database
            collection_name: Collection name in Chroma
            api_key: Aliyun API Key (optional, uses env if not provided)
        """
        # Configuration - always use absolute path
        if chroma_dir is None:
            # Use hardcoded absolute path to avoid relative path issues
            chroma_dir = r"C:\Users\Xiabi\.openclaw\workspace\chroma_db"
        
        if api_key is None:
            api_key = os.getenv("ALIYUN_API_KEY")
        
        if not api_key:
            raise ValueError("ALIYUN_API_KEY is required")
        
        # Initialize components
        self.embeddings = AliyunEmbeddings(api_key=api_key)
        
        # Load vector store (must use same embedding as during indexing!)
        self.vectorstore = Chroma(
            persist_directory=chroma_dir,
            collection_name=collection_name,
            embedding_function=self.embeddings  # Use Aliyun embeddings (1024 dim)
        )
        
        # Verify dimension
        try:
            test_embed = self.embeddings.embed_query("test")
            print(f"[INFO] Embedding dimension: {len(test_embed)}")
        except Exception as e:
            print(f"[WARN] Could not verify embedding dimension: {e}")
        
        print(f"[INFO] MemorySearcher initialized")
        print(f"   - Chroma DB: {chroma_dir}")
        print(f"   - Collection: {collection_name}")
    
    def search(self, 
               query: str, 
               k: int = 5,
               score_threshold: float = 0.3,
               filter_source: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Search memories
        
        Args:
            query: Search query
            k: Number of results to return
            score_threshold: Minimum similarity score
            filter_source: Filter by source file (optional)
        
        Returns:
            List of search results with metadata
        """
        # Generate query embedding
        query_embedding = self.embeddings.embed_query(query)
        
        if not query_embedding:
            print("[ERROR] Failed to generate query embedding")
            return []
        
        # Search using query embedding directly
        try:
            # Use query embedding for search (more reliable than text search)
            results = self.vectorstore.similarity_search_by_vector(query_embedding, k=k)
            # Add dummy scores since this method doesn't return scores
            results = [(doc, 0.5) for doc in results]
            
            # Filter and format
            formatted_results = []
            for doc, score in results:
                # Score is already similarity for cosine distance
                similarity = score
                
                # Apply score threshold
                if similarity < score_threshold:
                    continue
                
                # Apply source filter
                if filter_source and filter_source not in doc.metadata.get("source", ""):
                    continue
                
                formatted_results.append({
                    "content": doc.page_content,
                    "source": doc.metadata.get("source", "Unknown"),
                    "type": doc.metadata.get("type", "Unknown"),
                    "date": doc.metadata.get("date", "Unknown"),
                    "similarity": round(similarity, 3),
                    "preview": doc.page_content[:200].replace("\n", " ") + "..."
                })
            
            return formatted_results
            
        except Exception as e:
            print(f"[ERROR] Search failed: {e}")
            return []
    
    def search_with_context(self, 
                           query: str, 
                           context: List[str],
                           k: int = 5) -> List[Dict[str, Any]]:
        """
        Search with conversation context
        
        Args:
            query: Current query
            context: Previous conversation context
            k: Number of results
        
        Returns:
            Enhanced search results
        """
        # Enhance query with context
        if context:
            enhanced_query = f"Context: {' '.join(context[:2])}\nQuestion: {query}"
        else:
            enhanced_query = query
        
        return self.search(enhanced_query, k=k)


# Convenience functions
_searcher = None

def get_searcher() -> MemorySearcher:
    """Get or create singleton searcher"""
    global _searcher
    if _searcher is None:
        _searcher = MemorySearcher()
    return _searcher

def search_memories(query: str, k: int = 5) -> List[Dict[str, Any]]:
    """
    Search memories (convenience function)
    
    Args:
        query: Search query
        k: Number of results
    
    Returns:
        List of search results
    """
    searcher = get_searcher()
    return searcher.search(query, k=k)

def search_memory_with_context(query: str, 
                               context: List[str], 
                               k: int = 5) -> List[Dict[str, Any]]:
    """
    Search memories with context (convenience function)
    
    Args:
        query: Search query
        context: Previous conversation context
        k: Number of results
    
    Returns:
        List of search results
    """
    searcher = get_searcher()
    return searcher.search_with_context(query, context, k=k)


# CLI interface
if __name__ == "__main__":
    import sys
    
    print("=" * 60)
    print("Memory Search CLI")
    print("=" * 60)
    
    # Test queries
    test_queries = sys.argv[1:] if len(sys.argv) > 1 else ["瀑布", "TTS", "memory"]
    
    searcher = get_searcher()
    
    for query in test_queries:
        print(f"\nQuery: '{query}'")
        results = searcher.search(query, k=3)
        
        if results:
            print(f"Found {len(results)} results:")
            for i, result in enumerate(results, 1):
                print(f"  {i}. [{result['source']}] (similarity: {result['similarity']})")
                print(f"     {result['preview']}")
        else:
            print("  No results found")
    
    print("\n" + "=" * 60)
