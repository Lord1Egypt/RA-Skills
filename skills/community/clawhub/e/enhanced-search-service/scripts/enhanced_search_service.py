#!/usr/bin/env python3
"""
Enhanced Search Service - Core implementation

Provides enhanced memory search by combining co-occurrence graph analysis
and semantic vector similarity.
"""

import logging
from typing import Dict, List, Any, Optional
import sys
import os

logger = logging.getLogger(__name__)

class EnhancedSearchService:
    """Enhanced search service combining co-occurrence and semantic similarity"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.co_occurrence_adapter = None
        self.semantic_vector_adapter = None
        self._initialize()
    
    def _initialize(self):
        """Initialize adapters for dependencies"""
        try:
            # Try to import co-occurrence adapter
            sys.path.insert(0, '/root/.openclaw/workspace/integration/adapter')
            from co_occurrence_adapter import CoOccurrenceAdapter
            self.co_occurrence_adapter = CoOccurrenceAdapter()
            logger.info("Co-occurrence adapter initialized")
        except ImportError as e:
            logger.warning(f"Could not import co-occurrence adapter: {e}")
        
        try:
            # Try to import semantic vector adapter
            from semantic_vector_adapter import SemanticVectorAdapter
            self.semantic_vector_adapter = SemanticVectorAdapter()
            logger.info("Semantic vector adapter initialized")
        except ImportError as e:
            logger.warning(f"Could not import semantic vector adapter: {e}")
        
        # Check if at least one adapter is available
        if not self.co_occurrence_adapter and not self.semantic_vector_adapter:
            logger.error("No search adapters available - service will be limited")
    
    def is_available(self) -> bool:
        """Check if service has at least one functional adapter"""
        return bool(self.co_occurrence_adapter or self.semantic_vector_adapter)
    
    def enhance_search(self, query: str, search_results: List[Dict], 
                       max_expansion: int = 5) -> List[Dict]:
        """
        Enhance search results using co-occurrence and semantic similarity
        
        Args:
            query: Search query string
            search_results: Raw search results list, each dict containing at least:
                          - 'content' or 'text'
                          - 'path' or 'file'
                          - 'lines' or line range
                          - Optional 'score' (relevance score)
            max_expansion: Maximum number of related results to add
        
        Returns:
            Enhanced results list with additional fields:
            - enhanced_score: Combined relevance score
            - co_occurrence_score: Co-occurrence enhancement score
            - semantic_score: Semantic similarity score
            - explanation: Brief explanation of enhancements
        """
        if not search_results:
            return []
        
        # Step 1: Extract memory IDs for co-occurrence tracking
        mem_ids = []
        for result in search_results:
            content = result.get('content', '') or result.get('text', '')
            path = result.get('path', '') or result.get('file', '')
            lines = result.get('lines', (0, 0))
            
            if content and path:
                # Generate a consistent memory ID
                import hashlib
                hash_input = f"{path}:{lines[0]}:{content[:100]}"
                mem_id = f"mem_{hashlib.md5(hash_input.encode()).hexdigest()[:10]}"
                mem_ids.append(mem_id)
                result['memory_id'] = mem_id
        
        # Step 2: Record co-occurrence of this search
        if self.co_occurrence_adapter and len(mem_ids) > 1:
            try:
                self.co_occurrence_adapter.record_cooccurrence(mem_ids, f"search:{query[:50]}")
            except Exception as e:
                logger.warning(f"Failed to record co-occurrence: {e}")
        
        # Step 3: Calculate enhancement scores for each result
        enhanced_results = []
        for result in search_results:
            enhanced = result.copy()
            base_score = enhanced.get('score', 0.5)
            co_score = 0.0
            semantic_score = 0.0
            
            # Co-occurrence enhancement
            if self.co_occurrence_adapter and 'memory_id' in enhanced:
                mem_id = enhanced['memory_id']
                related_ids = [id for id in mem_ids if id != mem_id]
                if related_ids:
                    try:
                        co_score = self.co_occurrence_adapter.get_co_occurrence_score(
                            mem_id, related_ids
                        )
                    except Exception as e:
                        logger.debug(f"Could not get co-occurrence score: {e}")
            
            # Semantic similarity enhancement
            if self.semantic_vector_adapter:
                content = enhanced.get('content', '') or enhanced.get('text', '')
                if content:
                    try:
                        # Get semantic similarity between query and content
                        semantic_score = self.semantic_vector_adapter.similarity(
                            query, content
                        )
                    except Exception as e:
                        logger.debug(f"Could not get semantic similarity: {e}")
            
            # Combine scores (configurable weights)
            co_weight = self.config.get('co_occurrence_weight', 0.3)
            semantic_weight = self.config.get('semantic_weight', 0.5)
            text_weight = self.config.get('text_match_weight', 0.2)
            
            # Normalize weights
            total_weight = co_weight + semantic_weight + text_weight
            if total_weight > 0:
                co_weight /= total_weight
                semantic_weight /= total_weight
                text_weight /= total_weight
            
            enhanced_score = (
                base_score * text_weight +
                co_score * co_weight +
                semantic_score * semantic_weight
            )
            
            enhanced['enhanced_score'] = enhanced_score
            enhanced['co_occurrence_score'] = co_score
            enhanced['semantic_score'] = semantic_score
            enhanced['base_score'] = base_score
            
            # Add explanation
            explanations = []
            if co_score > 0.1:
                explanations.append(f"co-occurrence +{co_score:.2f}")
            if semantic_score > 0.1:
                explanations.append(f"semantic +{semantic_score:.2f}")
            enhanced['explanation'] = ', '.join(explanations) if explanations else "base score only"
            
            enhanced_results.append(enhanced)
        
        # Step 4: Sort by enhanced score
        enhanced_results.sort(key=lambda x: x.get('enhanced_score', 0), reverse=True)
        
        # Step 5: Limit to max_expansion if needed (not implemented yet)
        
        return enhanced_results
    
    def health_check(self) -> Dict[str, Any]:
        """Return health status of the service"""
        status = {
            "service": "enhanced-search-service",
            "healthy": self.is_available(),
            "dependencies": {
                "co_occurrence_adapter": bool(self.co_occurrence_adapter),
                "semantic_vector_adapter": bool(self.semantic_vector_adapter)
            },
            "config": self.config
        }
        
        # Test functionality if adapters are available
        if self.co_occurrence_adapter:
            try:
                co_health = self.co_occurrence_adapter.health_check()
                status["co_occurrence_health"] = co_health.get("healthy", False)
            except Exception as e:
                status["co_occurrence_health"] = False
                status["co_occurrence_error"] = str(e)
        
        if self.semantic_vector_adapter:
            try:
                sem_health = self.semantic_vector_adapter.health_check()
                status["semantic_vector_health"] = sem_health.get("healthy", False)
            except Exception as e:
                status["semantic_vector_health"] = False
                status["semantic_vector_error"] = str(e)
        
        return status