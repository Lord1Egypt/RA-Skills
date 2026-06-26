# src/cxm/core/enhancer.py

from typing import Dict, List, Optional
from pathlib import Path

from src.core.rag import RAGEngine
from src.core.retriever import HybridRetriever
from src.core.reranker import Reranker
from src.ml.intent_analyzer import IntentAnalyzer
from src.ml.prompt_assembler import PromptAssembler
from src.ml.prompt_refiner import PromptRefiner
from src.ml.context_evaluator import ContextEvaluator
from src.tools.context_gatherer import gather_all


class PromptEnhancer:
    """
    Main orchestrator pipeline:
    
    User Prompt
      → Intent Analysis
      → System Context Gathering
      → Prompt Refinement (Gap Analysis)
      → Hybrid Retrieval (semantic + keyword)
      → Neural Reranking
      → Context Evaluation & Deduplication
      → Prompt Assembly with Citations
      → Enhanced Prompt
    """
    
    def __init__(
        self,
        rag: RAGEngine,
        use_cross_encoder: bool = False
    ):
        self.rag = rag
        self.intent_analyzer = IntentAnalyzer()
        self.retriever = HybridRetriever(rag)
        self.reranker = Reranker(use_cross_encoder=use_cross_encoder)
        self.assembler = PromptAssembler()
        self.refiner = PromptRefiner(rag=rag)
        self.evaluator = ContextEvaluator()
    
    def run_evaluation_pipeline(
        self,
        query: str,
        analysis: Dict,
        system_context: Dict = None,
        max_contexts: int = 5,
        token_budget: int = 4000
    ) -> Dict:
        """
        Stage 2 & 3: Multi-query Retrieval & Selection.
        Runs multiple searches based on Goal Analysis and aggregates unique hits.
        """
        all_candidates = []
        seen_paths = set()
        
        # 1. Multi-Query Retrieval (Stage 2)
        queries = analysis.get('search_queries', [query])
        for q in queries:
            candidates = self.retriever.retrieve(
                query=q,
                context_needs=analysis.get('context_needs', []),
                k=max_contexts * 2,
            )
            for cand in candidates:
                if cand['path'] not in seen_paths:
                    all_candidates.append(cand)
                    seen_paths.add(cand['path'])
        
        # 2. Rerank the aggregated set
        ranked = self.reranker.rerank(
            query=query,
            candidates=all_candidates,
            top_k=max_contexts * 3,
            token_budget=token_budget * 2
        )
        
        # 3. Evaluate & Deduplicate (Stage 3: Selection Layer)
        evaluated_selection = self.evaluator.evaluate_batch(query, ranked)
        
        # Final limit
        final_selection = evaluated_selection[:max_contexts]
        
        # 4. Assemble & Synthesize (Stage 4)
        result = self.assembler.assemble(
            user_prompt=query,
            intent=analysis['intent'],
            contexts=final_selection,
            system_context=system_context,
            max_tokens=token_budget,
        )
        
        result['evaluation_log'] = [
            {
                'name': cand['name'], 
                'relevant': '_evaluation_reason' in cand and not cand['_evaluation_reason'].startswith('Discarded'),
                'reason': cand.get('_evaluation_reason', 'No evaluation')
            } 
            for cand in ranked
        ]
        result['selected_contexts'] = final_selection
        
        return result

    
    def enhance(
        self,
        prompt: str,
        max_contexts: int = 5,
        token_budget: int = 4000,
        include_system_context: bool = True,
        min_similarity: float = 0.0,
    ) -> Dict:
        """
        Full enhancement pipeline
        
        Args:
            prompt: User's original prompt
            max_contexts: Maximum contexts to include
            token_budget: Token limit for enhanced prompt
            include_system_context: Gather git/file/shell context
            min_similarity: Minimum relevance threshold
        
        Returns:
            {
                'original': str,
                'refined': str,
                'enhanced': str,
                'refinement': Dict,
                'analysis': Dict,
                'contexts': List[Dict],
                'citations': List[Dict],
                'system_context': Dict,
                'metadata': Dict
            }
        """
        
        # 1. Analyze intent
        analysis = self.intent_analyzer.analyze(prompt)
        
        # 2. Gather system context
        system_context = {}
        if include_system_context:
            system_context = gather_all()
            
        # 3. Prompt Refinement (Auto)
        refinement = self.refiner.auto_refine(
            prompt=prompt,
            intent=analysis['intent'],
            auto_context=system_context,
        )
        
        search_prompt = refinement['refined_prompt']
        
        # 4. Use unified pipeline for retrieval, reranking, evaluation, and assembly
        pipeline_result = self.run_evaluation_pipeline(
            query=search_prompt,
            intent=analysis['intent'],
            context_needs=analysis['context_needs'],
            system_context=system_context,
            max_contexts=max_contexts,
            token_budget=token_budget
        )
        
        # 5. Return complete result
        return {
            'original': prompt,
            'refined': search_prompt,
            'enhanced': pipeline_result['enhanced_prompt'],
            'refinement': refinement,
            'analysis': analysis,
            'contexts': pipeline_result['selected_contexts'],
            'citations': pipeline_result['citations'],
            'evaluation_log': pipeline_result['evaluation_log'],
            'system_context': system_context,
            'metadata': {
                **pipeline_result['metadata'],
                'intent': analysis['intent'],
                'confidence': analysis['confidence'],
                'context_needs': analysis['context_needs'],
                'keywords': analysis['keywords'],
                'entities': analysis['entities'],
            }
        }
    
    def enhance_for_agent(
        self,
        prompt: str,
        agent_type: str = 'general',
        **kwargs
    ) -> str:
        """
        Simplified: returns only the enhanced prompt string
        Useful for piping into other tools/agents
        """
        result = self.enhance(prompt, **kwargs)
        return result['enhanced']
    
    def index_conversation(
        self,
        messages: List[Dict],
        session_name: str = "conversation"
    ) -> int:
        """
        Index a conversation for future retrieval
        """
        
        text = "\n\n".join([
            f"{m.get('role', 'unknown')}: {m.get('content', '')}"
            for m in messages
        ])
        
        return self.rag.index_text(
            content=text,
            source=f"conversation:{session_name}",
            metadata={
                'type': 'conversation',
                'session': session_name,
                'num_messages': len(messages),
            }
        )

    def interactive_enhance(self, prompt: str):
        """
        Interactive version: Asks user for missing info
        
        Returns:
            Generator that asks questions and finally
            provides the finished prompt
        """
        
        # 1. Analysis
        analysis = self.intent_analyzer.analyze(prompt)
        system_context = gather_all()
        
        # 2. Find gaps
        gaps = self.refiner.analyze_gaps(
            prompt=prompt,
            intent=analysis['intent'],
            auto_context=system_context,
        )
        
        # 3. Result object to fill
        answers = {}
        
        # 4. Yield questions
        if gaps['missing_critical'] or gaps['missing_optional']:
            questions = self.refiner.generate_clarifying_questions(gaps)
            yield {
                'type': 'questions',
                'questions': questions,
                'completeness': gaps['completeness'],
                'inferred': gaps['inferred'],
                'gaps': gaps
            }
            # The user interacts and the wrapper passes the answers back.
        
        # We need a way to receive the answers in the real implementation,
        # but for the CLI loop, it is easier to implement the CLI layer directly.
        # This generator approach is a placeholder. The CLI will drive the questions.
        pass
