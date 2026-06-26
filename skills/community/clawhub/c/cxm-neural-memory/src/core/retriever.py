# src/cxm/core/retriever.py

from typing import List, Dict
from datetime import datetime

import numpy as np

# We try to import BM25, but if it's missing, we fall back to Semantic only
try:
    from rank_bm25 import BM25Okapi
except ImportError:
    BM25Okapi = None

from src.core.rag import RAGEngine


class HybridRetriever:
    """
    Combines:
    1. Semantic search (embeddings via RAGEngine)
    2. Keyword search (BM25)
    3. Recency weighting
    4. Context-need filtering
    """
    
    def __init__(
        self,
        rag: RAGEngine,
        semantic_weight: float = 0.7,
        keyword_weight: float = 0.3
    ):
        self.rag = rag
        self.semantic_weight = semantic_weight
        self.keyword_weight = keyword_weight
        
        # Build BM25 index
        self.bm25 = self._build_bm25()
    
    def _build_bm25(self):
        """Build keyword index from metadata"""
        if BM25Okapi is None:
            return None
            
        docs = self.rag.metadata
        if not docs:
            return None
        
        tokenized = [
            doc.get('full_content', doc.get('content_preview', '')).lower().split()
            for doc in docs
        ]
        
        return BM25Okapi(tokenized)
    
    def retrieve(
        self,
        query: str,
        context_needs: List[str] = None,
        k: int = 10,
        min_similarity: float = 0.0
    ) -> List[Dict]:
        """
        Hybrid retrieval
        
        Args:
            query: Search query
            context_needs: From intent analyzer (filters by type)
            k: Number of results
            min_similarity: Minimum threshold
        
        Returns:
            Ranked list of documents
        """
        
        if not self.rag.metadata:
            return []
        
        # 1. Semantic search
        semantic_results = self.rag.search(query, k=k * 3)
        
        # 2. Keyword search
        keyword_results = self._keyword_search(query, k=k * 3)
        
        # 3. Merge scores
        merged = self._merge_results(semantic_results, keyword_results)
        
        # 4. Apply boosts
        for doc in merged.values():
            # Recency boost
            doc['final_score'] = doc['hybrid_score'] * self._recency_boost(doc)
            
            # Context-need boost
            if context_needs:
                doc['final_score'] *= self._context_need_boost(doc, context_needs)
        
        # 5. Sort and return top-k
        ranked = sorted(merged.values(), key=lambda x: x['final_score'], reverse=True)
        
        return [r for r in ranked[:k] if r['final_score'] >= min_similarity]
    
    def _keyword_search(self, query: str, k: int) -> List[Dict]:
        """BM25 keyword search"""
        
        if not self.bm25:
            return []
        
        tokens = query.lower().split()
        scores = self.bm25.get_scores(tokens)
        
        top_indices = np.argsort(scores)[-k:][::-1]
        
        results = []
        for idx in top_indices:
            if idx < len(self.rag.metadata) and scores[idx] > 0:
                doc = self.rag.metadata[idx].copy()
                doc['bm25_score'] = float(scores[idx])
                results.append(doc)
        
        return results
    
    def _merge_results(
        self,
        semantic: List[Dict],
        keyword: List[Dict]
    ) -> Dict[int, Dict]:
        """Merge semantic and keyword results using Reciprocal Rank Fusion (RRF)"""
        
        merged = {}
        k = 60 # Standard RRF constant
        
        # Rank Semantic
        for rank, r in enumerate(semantic):
            doc_id = r['id']
            merged[doc_id] = r.copy()
            # RRF Score for Semantic
            merged[doc_id]['semantic_rrf'] = 1.0 / (k + rank + 1)
            merged[doc_id]['keyword_rrf'] = 0.0
        
        # Rank Keyword
        for rank, r in enumerate(keyword):
            doc_id = r['id']
            kw_rrf = 1.0 / (k + rank + 1)
            
            if doc_id in merged:
                merged[doc_id]['keyword_rrf'] = kw_rrf
            else:
                merged[doc_id] = r.copy()
                merged[doc_id]['semantic_rrf'] = 0.0
                merged[doc_id]['keyword_rrf'] = kw_rrf
        
        # Calculate hybrid RRF score
        for doc in merged.values():
            if not self.bm25:
                doc['hybrid_score'] = doc.get('semantic_rrf', 0)
            else:
                # Weighted RRF
                doc['hybrid_score'] = (
                    self.semantic_weight * doc.get('semantic_rrf', 0) +
                    self.keyword_weight * doc.get('keyword_rrf', 0)
                )
        
        return merged
    
    def _recency_boost(self, doc: Dict) -> float:
        """Newer documents get slight boost"""
        try:
            indexed = datetime.fromisoformat(doc.get('indexed_at', ''))
            age_days = (datetime.now() - indexed).days
            return max(0.5, 1.0 / (1.0 + age_days / 30.0))
        except Exception:
            return 1.0
    
    def _context_need_boost(self, doc: Dict, context_needs: List[str]) -> float:
        """Boost based on context needs matching doc type"""
        
        ext = doc.get('extension', '')
        
        type_map = {
            'similar_code': ['.py', '.js', '.ts', '.rs', '.go', '.java', '.c', '.cpp'],
            'documentation': ['.md', '.txt', '.rst'],
            'tests': ['.py', '.js', '.ts'],
            'error_logs': ['.log', '.txt'],
        }
        
        boost = 1.0
        for need in context_needs:
            if ext in type_map.get(need, []):
                boost += 0.2
        
        return min(boost, 2.0)
    
    def rebuild_keyword_index(self):
        """Rebuild BM25 after new documents indexed"""
        self.bm25 = self._build_bm25()