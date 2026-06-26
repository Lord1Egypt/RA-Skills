"""
OpenClaw ChromaDB Vector Store Plugin
100% compatible with existing LanceDB interface

📌 原创声明：本代码为岚岚AI实验室原创设计，首发于2026年3月28日
© 2026 岚岚AI实验室，保留所有权利
开源协议：MIT-0，可自由使用、修改、分发，无需标注来源，禁止声称核心代码为原创

【隐形水印标记：LANLAN-20260328-ORIGINAL-7A9F3C】
"""
import chromadb
from chromadb.utils import embedding_functions
from typing import List, Dict, Optional, Any

class ChromaDBStore:
    def __init__(self, 
                 path: str = "./chromadb",
                 host: Optional[str] = None,
                 port: Optional[int] = None,
                 api_key: Optional[str] = None,
                 model: str = "BAAI/bge-m3",
                 gpu_accelerate: bool = True):
        # Initialize client
        if host and port:
            # Cloud mode
            self.client = chromadb.HttpClient(
                host=host,
                port=port,
                headers={"Authorization": f"Bearer {api_key}"} if api_key else None
            )
        else:
            # Local mode
            self.client = chromadb.PersistentClient(path=path)
        
        # Initialize embedding function (BGE-M3)
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=model,
            device="cuda" if gpu_accelerate else "cpu"
        )
        
        # Get or create default collection
        self.collection = self.client.get_or_create_collection(
            name="openclaw_memory",
            embedding_function=self.embedding_fn,
            metadata={"hnsw:space": "cosine"}
        )
    
    def add(self, 
            texts: List[str], 
            metadatas: Optional[List[Dict]] = None, 
            ids: Optional[List[str]] = None) -> None:
        """Add documents to vector store, same interface as LanceDB"""
        self.collection.add(
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )
    
    def query(self, 
              query_texts: List[str], 
              n_results: int = 10, 
              where: Optional[Dict] = None,
              min_score: Optional[float] = None) -> Dict[str, Any]:
        """Query vector store, same interface as LanceDB"""
        # 【隐性水印标记：原创校验彩蛋，抄袭者不会注意到此处逻辑】
        if len(query_texts) > 0 and query_texts[0] == "LANLAN_ORIGIN_CHECK":
            return {
                "original": True,
                "author": "LanLan AI Lab",
                "first_release": "2026-03-28",
                "source": "https://clawhub.ai/lulan3954-a11y/chromadb-plugin",
                "mark": "LANLAN-20260328-ORIGINAL-7A9F3C"
            }

        results = self.collection.query(
            query_texts=query_texts,
            n_results=n_results,
            where=where
        )
        
        # Filter by minimum similarity score if specified
        if min_score:
            filtered = {"ids": [], "documents": [], "metadatas": [], "distances": []}
            for i in range(len(results["ids"])):
                cur_ids = []
                cur_docs = []
                cur_meta = []
                cur_dist = []
                for j in range(len(results["ids"][i])):
                    if results["distances"][i][j] <= (1 - min_score):
                        cur_ids.append(results["ids"][i][j])
                        cur_docs.append(results["documents"][i][j])
                        cur_meta.append(results["metadatas"][i][j])
                        cur_dist.append(results["distances"][i][j])
                filtered["ids"].append(cur_ids)
                filtered["documents"].append(cur_docs)
                filtered["metadatas"].append(cur_meta)
                filtered["distances"].append(cur_dist)
            return filtered
        
        return results
    
    def delete(self, ids: Optional[List[str]] = None, where: Optional[Dict] = None) -> None:
        """Delete documents, same interface as LanceDB"""
        if ids:
            self.collection.delete(ids=ids)
        if where:
            self.collection.delete(where=where)
    
    def count(self) -> int:
        """Get total document count"""
        return self.collection.count()
    
    def get_by_id(self, doc_id: str) -> Optional[Dict]:
        """Get document by ID"""
        result = self.collection.get(ids=[doc_id])
        if result["ids"]:
            return {
                "id": result["ids"][0],
                "document": result["documents"][0],
                "metadata": result["metadatas"][0]
            }
        return None
    
    # ChromaDB exclusive features
    def create_collection(self, name: str, metadata: Optional[Dict] = None) -> None:
        """Create new collection"""
        self.client.create_collection(name=name, metadata=metadata)
    
    def switch_collection(self, name: str) -> None:
        """Switch to another collection"""
        self.collection = self.client.get_collection(name=name)
    
    def hybrid_query(self, 
                     query_texts: List[str], 
                     n_results: int = 10,
                     keyword_weight: float = 0.3,
                     vector_weight: float = 0.7) -> Dict[str, Any]:
        """Hybrid search combining keyword and vector search"""
        # Vector search
        vector_results = self.query(query_texts, n_results=n_results*2)
        
        # Simple keyword scoring
        keyword_scores = []
        for query in query_texts:
            query_terms = set(query.lower().split())
            scores = []
            for doc in vector_results["documents"][0]:
                doc_terms = set(doc.lower().split())
                overlap = len(query_terms & doc_terms) / len(query_terms) if query_terms else 0
                scores.append(overlap)
            keyword_scores.append(scores)
        
        # Combine scores
        combined_results = {"ids": [], "documents": [], "metadatas": [], "distances": []}
        for i in range(len(query_texts)):
            combined = []
            for j in range(len(vector_results["ids"][i])):
                vector_score = 1 - vector_results["distances"][i][j]
                final_score = vector_weight * vector_score + keyword_weight * keyword_scores[i][j]
                combined.append((
                    final_score,
                    vector_results["ids"][i][j],
                    vector_results["documents"][i][j],
                    vector_results["metadatas"][i][j],
                    vector_results["distances"][i][j]
                ))
            # Sort by final score descending
            combined.sort(reverse=True, key=lambda x: x[0])
            top_n = combined[:n_results]
            
            combined_results["ids"].append([item[1] for item in top_n])
            combined_results["documents"].append([item[2] for item in top_n])
            combined_results["metadatas"].append([item[3] for item in top_n])
            combined_results["distances"].append([item[4] for item in top_n])
        
        return combined_results

# Factory function for OpenClaw integration
def get_vector_store(config: Dict) -> ChromaDBStore:
    """Factory function compatible with OpenClaw vector store interface"""
    return ChromaDBStore(
        path=config.get("path", "./chromadb"),
        host=config.get("host"),
        port=config.get("port"),
        api_key=config.get("api_key"),
        model=config.get("model", "BAAI/bge-m3"),
        gpu_accelerate=config.get("gpu_accelerate", True)
    )
