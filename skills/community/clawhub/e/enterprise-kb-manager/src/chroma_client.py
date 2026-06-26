"""
ChromaDB client for Enterprise Knowledge Base

Handles connection to ChromaDB and all vector operations.
Uses shared configuration for multi-agent deployment.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings
import os
from .system_config import load_system_config


@dataclass
class SearchResult:
    """Search result from ChromaDB"""
    id: str
    text: str
    metadata: Dict[str, Any]
    distance: float
    score: float  # 1 - distance


class CustomEmbeddingFunction(EmbeddingFunction):
    """Custom embedding function that uses pre-computed embeddings"""
    
    def __call__(self, input: Documents) -> Embeddings:
        # This won't be called since we provide embeddings directly
        return [[0.0] * 1536] * len(input)


class ChromaVectorDB:
    """ChromaDB client for local vector storage"""
    
    def __init__(self, db_path: str = None, 
                 collection_name: str = "enterprise_kb"):
        """
        Initialize ChromaDB client
        
        Args:
            db_path: Path to ChromaDB database directory (optional, uses shared config)
            collection_name: Name of the collection
        """
        # 使用系统配置
        if db_path is None:
            system_config = load_system_config()
            db_path = system_config.data_path
            print(f"✓ 使用系统数据路径: {db_path}")
        
        self.db_path = db_path
        self.collection_name = collection_name
        
        # Ensure data directory exists
        os.makedirs(db_path, exist_ok=True)
        
        # Initialize client
        self.client = chromadb.PersistentClient(path=db_path)
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=CustomEmbeddingFunction()
        )
        
        print(f"✓ ChromaDB collection '{collection_name}' ready")
    
    def add_chunks(self, chunks: List[Dict[str, Any]]) -> int:
        """
        Add document chunks to collection
        
        Args:
            chunks: List of chunk dictionaries
        
        Returns:
            int: Number of chunks inserted
        """
        if not chunks:
            return 0
        
        # Prepare data
        ids = []
        documents = []
        embeddings = []
        metadatas = []
        
        for chunk in chunks:
            ids.append(chunk["id"])
            documents.append(chunk["text"])
            embeddings.append(chunk["vector"])
            
            # Prepare metadata
            metadata = {
                "document_id": chunk["document_id"],
                "document_name": chunk["document_name"],
                "chunk_index": chunk["chunk_index"]
            }
            
            # Add additional metadata
            if "metadata" in chunk and chunk["metadata"]:
                for key, value in chunk["metadata"].items():
                    metadata[key] = str(value)  # ChromaDB requires string values
            
            metadatas.append(metadata)
        
        # Insert
        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )
        
        return len(chunks)
    
    def search(self, query_vector: List[float], top_k: int = 5,
               filter_expr: Optional[Dict] = None) -> List[SearchResult]:
        """
        Search for similar vectors
        
        Args:
            query_vector: Query embedding vector
            top_k: Number of results to return
            filter_expr: Optional filter (e.g., {"document_id": "doc123"})
        
        Returns:
            List[SearchResult]: Search results sorted by similarity
        """
        results = self.collection.query(
            query_embeddings=[query_vector],
            n_results=top_k,
            where=filter_expr,
            include=["documents", "metadatas", "distances"]
        )
        
        # Convert to SearchResult objects
        search_results = []
        
        if results["ids"] and results["ids"][0]:
            for i, doc_id in enumerate(results["ids"][0]):
                distance = results["distances"][0][i]
                
                # ChromaDB uses cosine distance by default
                # For cosine distance: similarity = 1 - distance
                # But we need to handle the range properly
                if distance <= 2.0:  # Valid cosine distance range [0, 2]
                    similarity_score = 1 - (distance / 2.0)  # Normalize to [0, 1]
                else:
                    similarity_score = max(0, 1 - distance)  # Fallback
                
                search_results.append(SearchResult(
                    id=doc_id,
                    text=results["documents"][0][i],
                    metadata=results["metadatas"][0][i],
                    distance=distance,
                    score=similarity_score
                ))
        
        return search_results
    
    def delete_by_document(self, document_id: str) -> int:
        """
        Delete all chunks belonging to a document
        
        Args:
            document_id: Document ID to delete
        
        Returns:
            int: Number of chunks deleted
        """
        # Query to get IDs
        results = self.collection.get(
            where={"document_id": document_id},
            include=["metadatas"]
        )
        
        if not results["ids"]:
            return 0
        
        # Delete by IDs
        self.collection.delete(ids=results["ids"])
        
        return len(results["ids"])
    
    def count_by_document(self, document_id: str) -> int:
        """
        Count chunks for a document
        
        Args:
            document_id: Document ID
        
        Returns:
            int: Number of chunks
        """
        results = self.collection.get(
            where={"document_id": document_id},
            include=["metadatas"]
        )
        
        return len(results["ids"])
    
    def get_all_documents(self) -> List[Dict[str, Any]]:
        """
        Get list of all unique documents
        
        Returns:
            List of document info dictionaries
        """
        try:
            # Get all chunks
            results = self.collection.get(include=["metadatas"])
            
            # Group by document_id
            docs = {}
            for metadata in results["metadatas"]:
                if metadata and 'document_id' in metadata:
                    doc_id = metadata["document_id"]
                    if doc_id not in docs:
                        docs[doc_id] = {
                            "document_id": doc_id,
                            "document_name": metadata.get("document_name", "Unknown"),
                            "chunk_count": 0
                        }
                    docs[doc_id]["chunk_count"] += 1
            
            return list(docs.values())
        except Exception as e:
            print(f"⚠️ get_all_documents 错误: {e}")
            return []
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get collection statistics
        
        Returns:
            Dictionary with stats
        """
        total_chunks = self.collection.count()
        documents = self.get_all_documents()
        
        return {
            "collection_name": self.collection_name,
            "chunk_count": total_chunks,
            "document_count": len(documents),
            "vector_dimension": 1536,  # Assuming OpenAI embeddings
            "metric_type": "COSINE"
        }
    
    def close(self):
        """Close connection"""
        pass


if __name__ == "__main__":
    # Test ChromaDB client
    print("Testing ChromaDB client...")
    
    # Initialize
    client = ChromaVectorDB(
        db_path="./data/chroma_test",
        collection_name="test_collection"
    )
    
    # Add test data
    test_chunks = [
        {
            "id": "chunk_1",
            "vector": [0.1] * 1536,
            "text": "This is a test chunk",
            "document_id": "doc_1",
            "document_name": "test.txt",
            "chunk_index": 0
        }
    ]
    
    count = client.add_chunks(test_chunks)
    print(f"✓ Inserted {count} chunks")
    
    # Search
    results = client.search([0.15] * 1536, top_k=1)
    print(f"✓ Found {len(results)} results")
    
    # Stats
    stats = client.get_stats()
    print(f"✓ Stats: {stats}")
    
    # Cleanup
    import shutil
    if os.path.exists("./data/chroma_test"):
        shutil.rmtree("./data/chroma_test")
        print("✓ Cleaned up")