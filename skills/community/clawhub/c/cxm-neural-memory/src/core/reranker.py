# src/cxm/core/reranker.py

from typing import List, Dict, Optional


class Reranker:
    """
    Re-ranks retrieved documents for precision
    
    Two modes:
    1. Cross-encoder (if available) - more accurate, slower
    2. Heuristic (always available) - fast, good enough
    """
    
    def __init__(self, use_cross_encoder: bool = False):
        self.cross_encoder = None
        
        if use_cross_encoder:
            try:
                from sentence_transformers import CrossEncoder
                import os
                # Suppress output for cross encoder too
                os.environ['TRANSFORMERS_VERBOSITY'] = 'error'
                os.environ['HF_HUB_DISABLE_PROGRESS_BARS'] = '1'
                self.cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
            except Exception:
                pass  # Fall back to heuristic
    
    def rerank(
        self,
        query: str,
        candidates: List[Dict],
        top_k: int = 5,
        token_budget: int = 4000
    ) -> List[Dict]:
        """
        Re-rank and select best candidates within token budget
        
        Args:
            query: User query
            candidates: Retrieved documents
            top_k: Max results
            token_budget: Max total tokens for context
        """
        
        if not candidates:
            return []
        
        # Score candidates
        if self.cross_encoder:
            candidates = self._neural_rerank(query, candidates)
        else:
            candidates = self._heuristic_rerank(query, candidates)
        
        # Select within token budget
        return self._select_within_budget(candidates, top_k, token_budget)
    
    def _neural_rerank(self, query: str, candidates: List[Dict]) -> List[Dict]:
        """Cross-encoder reranking"""
        
        pairs = [
            (query, c.get('full_content', c.get('content_preview', '')))
            for c in candidates
        ]
        
        scores = self.cross_encoder.predict(pairs)
        
        for cand, score in zip(candidates, scores):
            cand['rerank_score'] = float(score)
        
        return sorted(candidates, key=lambda x: x['rerank_score'], reverse=True)
    
    def _heuristic_rerank(self, query: str, candidates: List[Dict]) -> List[Dict]:
        """
        Heuristic reranking using multiple signals:
        - Existing similarity score
        - Query term overlap
        - Document length (prefer concise)
        - Diversity (penalize similar documents)
        """
        
        query_terms = set(query.lower().split())
        
        for cand in candidates:
            content = cand.get('full_content', cand.get('content_preview', '')).lower()
            content_terms = set(content.split())
            
            # Term overlap
            overlap = len(query_terms & content_terms) / max(len(query_terms), 1)
            
            # Length penalty (prefer 100-2000 chars)
            length = len(content)
            if length < 50:
                length_score = 0.3
            elif length < 100:
                length_score = 0.7
            elif length < 2000:
                length_score = 1.0
            else:
                length_score = 0.8
            
            # Combined score
            base_score = cand.get('final_score', cand.get('similarity', 0))
            cand['rerank_score'] = base_score * 0.5 + overlap * 0.3 + length_score * 0.2
        
        return sorted(candidates, key=lambda x: x['rerank_score'], reverse=True)
    
    def _select_within_budget(
        self,
        ranked: List[Dict],
        top_k: int,
        token_budget: int
    ) -> List[Dict]:
        """Select top documents within token budget"""
        
        selected = []
        total_tokens = 0
        seen_hashes = set()
        
        for doc in ranked:
            content = doc.get('full_content', doc.get('content_preview', ''))
            estimated_tokens = len(content) // 4
            
            # Budget check
            if total_tokens + estimated_tokens > token_budget:
                # Try truncated version
                remaining = token_budget - total_tokens
                if remaining > 100:  # At least 100 tokens worth
                    doc = doc.copy()
                    doc['full_content'] = content[:remaining * 4]
                    doc['content_preview'] = content[:min(500, remaining * 4)]
                    doc['_truncated'] = True
                    selected.append(doc)
                break
            
            # Diversity check (skip near-duplicates)
            content_hash = hash(content[:200])
            if content_hash in seen_hashes:
                continue
            seen_hashes.add(content_hash)
            
            selected.append(doc)
            total_tokens += estimated_tokens
            
            if len(selected) >= top_k:
                break
        
        return selected