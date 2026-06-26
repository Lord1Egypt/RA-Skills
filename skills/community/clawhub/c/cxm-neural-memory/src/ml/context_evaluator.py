# src/ml/context_evaluator.py

from typing import Dict, Any, List
from src.core.interfaces import BaseContextEvaluator

class ContextEvaluator(BaseContextEvaluator):
    """
    Evaluates individual RAG hits against user intent and deduplicates context.
    Acts as a 'gatekeeper' and 'judge' to categorize and filter context.
    """
    
    RELEVANCE_TYPES = {
        'direct_code': ['def ', 'class ', 'import ', 'async ', 'return '],
        'architecture': ['design', 'structure', 'flow', 'component', 'system', 'module'],
        'pattern': ['standard', 'best practice', 'convention', 'naming', 'style'],
        'logic': ['calculation', 'math', 'decimal', 'ratio', 'formula']
    }

    def __init__(self):
        # Local import to avoid circular dependencies
        from src.ml.intent_analyzer import IntentAnalyzer
        self.analyzer = IntentAnalyzer()
        
    def evaluate(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deeper evaluation of context relevance.
        Categorizes hits into types: direct_code, architecture, pattern, or general.
        """
        query_analysis = self.analyzer.analyze(query)
        content = context.get('full_content', context.get('content_preview', '')).lower()
        file_name = context.get('name', '').lower()
        
        relevance_score = 0.0
        reasons = []
        rel_type = "general"
        
        # 1. Determine Relevance Type
        for rtype, keywords in self.RELEVANCE_TYPES.items():
            if any(kw in content for kw in keywords) or any(kw in file_name for kw in keywords):
                rel_type = rtype
                break

        # 2. Entity Match (High weight)
        matched_entities = [e for e in query_analysis['entities'] if e.lower() in content or e.lower() in file_name]
        if matched_entities:
            relevance_score += 0.5 * min(len(matched_entities) / 2, 1.0)
            reasons.append(f"Matches query entities: {', '.join(matched_entities)}")
            
        # 3. Intent-specific check
        intent = query_analysis['intent']
        if intent == 'bug_fixing' and ('error' in content or 'exception' in content):
            relevance_score += 0.3
            reasons.append("Contains error/exception handling logic")
        elif intent == 'code_optimization' and any(kw in content for kw in ['loop', 'performance', 'async']):
            relevance_score += 0.3
            reasons.append("Target for optimization found")
        elif intent == 'testing' and ('test' in file_name or 'assert' in content):
            relevance_score += 0.4
            reasons.append("Direct testing context")

        # 4. Keyword Overlap
        matched_keywords = [kw for kw in query_analysis['keywords'] if kw in content]
        if matched_keywords:
            relevance_score += 0.2 * (len(matched_keywords) / max(len(query_analysis['keywords']), 1))
            
        # 5. Baseline for high RAG similarity
        if relevance_score == 0.0 and context.get('similarity', 0) > 0.6:
            relevance_score = 0.3
            reasons.append("High semantic similarity")

        # Final decision
        is_relevant = relevance_score >= 0.25 
        
        reason = " | ".join(reasons) if reasons else "Semantic match"
        return {
            'relevant': is_relevant,
            'reason': reason,
            'score': relevance_score,
            'type': rel_type
        }

    def _calculate_overlap(self, text1: str, text2: str) -> float:
        """Calculate character tri-gram Jaccard similarity for robust code deduplication."""
        
        def get_trigrams(text: str) -> set:
            # Remove excessive whitespace but keep structure
            clean_text = " ".join(text.split())
            return set(clean_text[i:i+3] for i in range(len(clean_text) - 2))
            
        set1 = get_trigrams(text1)
        set2 = get_trigrams(text2)
        
        if not set1 or not set2: 
            return 0.0
            
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return intersection / union

    def evaluate_batch(self, query: str, candidates: List[Dict[str, Any]], max_overlap: float = 0.4) -> List[Dict[str, Any]]:
        """
        Selection Layer: Filters for relevance and removes redundancy.
        """
        selected = []
        selected_texts = []
        
        for cand in candidates:
            eval_res = self.evaluate(query, cand)
            if not eval_res['relevant']: continue
                
            content = cand.get('full_content', cand.get('content_preview', ''))
            is_redundant = False
            
            for prev_text in selected_texts:
                if self._calculate_overlap(content, prev_text) > max_overlap:
                    is_redundant = True
                    break
                    
            if not is_redundant:
                cand['_evaluation_reason'] = eval_res['reason']
                cand['_relevance_type'] = eval_res['type']
                cand['_relevance_score'] = eval_res['score']
                selected.append(cand)
                selected_texts.append(content)
                
        return selected
