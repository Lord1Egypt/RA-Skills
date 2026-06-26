"""
Retrieval engine for Enterprise Knowledge Base

Searches vector database and formats results for LLM.
"""

from typing import List
from dataclasses import dataclass

from .chroma_client import ChromaVectorDB, SearchResult
from .embedder import Embedder


@dataclass
class RetrievalResult:
    """Enhanced search result with formatting"""
    chunk_id: str
    text: str
    document_name: str
    document_id: str
    chunk_index: int
    score: float
    
    def format_with_source(self, index: int) -> str:
        """Format chunk with source citation"""
        return f"[来源{index + 1}: {self.document_name}]\n{self.text}"


class Retriever:
    """Retrieve relevant chunks for queries"""
    
    def __init__(self, db: ChromaVectorDB, embedder: Embedder, top_k: int = 5, 
                 similarity_threshold: float = 0.3):
        """
        Initialize retriever
        
        Args:
            db: ChromaDB database client
            embedder: Embedding generator
            top_k: Number of results to retrieve
            similarity_threshold: Minimum similarity score to include results
        """
        self.db = db
        self.embedder = embedder
        self.top_k = top_k
        self.similarity_threshold = similarity_threshold
    
    def retrieve(self, query: str, top_k: int = None, 
                 similarity_threshold: float = None) -> List[RetrievalResult]:
        """
        Retrieve relevant chunks for a query
        
        Args:
            query: User query
            top_k: Override default top_k
            similarity_threshold: Override default similarity threshold
        
        Returns:
            List of retrieval results sorted by relevance (filtered by threshold)
        """
        if top_k is None:
            top_k = self.top_k
        if similarity_threshold is None:
            similarity_threshold = self.similarity_threshold
        
        # Generate query embedding
        query_vector = self.embedder.embed_query(query)
        
        # Search in ChromaDB (get more results to allow for filtering)
        search_results = self.db.search(query_vector, top_k=top_k * 2)
        
        # Convert to RetrievalResult and filter by similarity threshold
        results = []
        for sr in search_results:
            # ChromaDB client already converted distance to similarity score
            similarity_score = sr.score
            
            # Only include results above threshold
            if similarity_score >= similarity_threshold:
                results.append(RetrievalResult(
                    chunk_id=sr.id,
                    text=sr.text,
                    document_name=sr.metadata["document_name"],
                    document_id=sr.metadata["document_id"],
                    chunk_index=sr.metadata["chunk_index"],
                    score=similarity_score
                ))
        
        # Sort by similarity score (descending) and limit to top_k
        results.sort(key=lambda x: x.score, reverse=True)
        return results[:top_k]
    
    def format_context(self, results: List[RetrievalResult]) -> str:
        """
        Format retrieval results as context for LLM
        
        Args:
            results: List of retrieval results
        
        Returns:
            Formatted context string
        """
        if not results:
            return "知识库中没有找到相关信息。"
        
        context_parts = ["以下是从知识库中检索到的相关内容：\n"]
        
        for i, result in enumerate(results):
            context_parts.append(result.format_with_source(i))
            context_parts.append("")  # Empty line between chunks
        
        context_parts.append("\n请基于以上内容回答用户的问题。如果以上内容不足以回答问题，请明确说明。")
        
        return "\n".join(context_parts)


if __name__ == "__main__":
    # Test retriever
    from .config_loader import load_config
    
    print("Testing retriever...")
    
    config = load_config()
    
    # Initialize components
    db = ChromaVectorDB(
        collection_name=config.collection_name
    )
    
    embedder = Embedder(
        model=config.embedding_model,
        api_key=config.embedding_api_key
    )
    
    retriever = Retriever(db, embedder, top_k=3)
    
    # Test retrieval
    query = "test query"
    results = retriever.retrieve(query)
    
    print(f"✓ Retrieved {len(results)} results")
    
    if results:
        context = retriever.format_context(results)
        print(f"✓ Formatted context ({len(context)} chars)")
        print(f"\n{context[:200]}...")
    else:
        print("  No results found (database may be empty)")
