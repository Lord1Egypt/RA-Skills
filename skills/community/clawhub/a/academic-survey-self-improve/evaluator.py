#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LLM-Based Survey Evaluator
Uses LLM to evaluate academic survey quality across 5 dimensions
"""

import json
from pathlib import Path

class LLMEvaluator:
    """LLM-based quality evaluator for academic surveys"""
    
    def __init__(self):
        self.dimensions = [
            'structure',
            'references', 
            'content',
            'tables_figures',
            'writing'
        ]
        
        self.weights = {
            'structure': 0.15,
            'references': 0.20,
            'content': 0.25,
            'tables_figures': 0.20,
            'writing': 0.20
        }
    
    def evaluate(self, tex_path):
        """
        Evaluate survey quality using LLM
        
        Args:
            tex_path: Path to .tex file
            
        Returns:
            dict with overall_score, dimension_scores, and feedback
        """
        # Read LaTeX content
        with open(tex_path, 'r', encoding='utf-8') as f:
            tex_content = f.read()
        
        # Extract metrics
        metrics = self._extract_metrics(tex_content)
        
        # Use LLM to evaluate (simulated for now)
        evaluation = self._llm_evaluate(tex_content, metrics)
        
        return evaluation
    
    def _extract_metrics(self, tex_content):
        """Extract quantitative metrics from LaTeX"""
        import re
        
        metrics = {
            'references': len(re.findall(r'\\bibitem\{', tex_content)),
            'figures': len(re.findall(r'\\begin\{figure\}', tex_content)),
            'tables': len(re.findall(r'\\begin\{table', tex_content)),
            'equations': len(re.findall(r'\\begin\{equation', tex_content)),
            'sections': len(re.findall(r'\\section\{', tex_content)),
            'word_count': len(tex_content.split()),
            'has_abstract': 1 if '\\begin{abstract}' in tex_content else 0,
            'has_keywords': 1 if '\\begin{keywords}' in tex_content else 0,
        }
        
        return metrics
    
    def _llm_evaluate(self, tex_content, metrics):
        """
        Evaluate using LLM analysis
        
        In production, this would call an actual LLM API.
        For now, uses rule-based simulation with LLM-like reasoning.
        """
        
        # Structure evaluation (15%)
        structure_score = self._evaluate_structure(metrics)
        
        # References evaluation (20%)
        references_score = self._evaluate_references(metrics)
        
        # Content evaluation (25%)
        content_score = self._evaluate_content(metrics, tex_content)
        
        # Tables/Figures evaluation (20%)
        visuals_score = self._evaluate_visuals(metrics)
        
        # Writing evaluation (20%)
        writing_score = self._evaluate_writing(tex_content)
        
        # Calculate weighted average
        scores = {
            'structure': structure_score,
            'references': references_score,
            'content': content_score,
            'tables_figures': visuals_score,
            'writing': writing_score
        }
        
        overall = sum(scores[k] * self.weights[k] for k in scores)
        
        # Generate feedback
        feedback = self._generate_feedback(scores, metrics)
        
        return {
            'overall_score': round(overall, 2),
            'dimension_scores': scores,
            'metrics': metrics,
            'feedback': feedback
        }
    
    def _evaluate_structure(self, metrics):
        """Evaluate structure quality"""
        score = 0
        
        # Required sections
        if metrics['sections'] >= 6:
            score += 4
        elif metrics['sections'] >= 4:
            score += 2
        
        # Abstract
        score += metrics['has_abstract'] * 2
        
        # Completeness
        if metrics['sections'] >= 8:
            score += 4
        
        return min(score, 10)
    
    def _evaluate_references(self, metrics):
        """Evaluate reference quality"""
        ref_count = metrics['references']
        
        if ref_count >= 50:
            return 10.0
        elif ref_count >= 30:
            return 8.0
        elif ref_count >= 20:
            return 6.0
        elif ref_count >= 10:
            return 4.0
        else:
            return 2.0
    
    def _evaluate_content(self, metrics, tex_content):
        """Evaluate content depth"""
        score = 0
        
        # Word count
        if metrics['word_count'] >= 8000:
            score += 4
        elif metrics['word_count'] >= 5000:
            score += 3
        elif metrics['word_count'] >= 3000:
            score += 2
        
        # Equations (technical depth)
        if metrics['equations'] >= 4:
            score += 3
        elif metrics['equations'] >= 2:
            score += 2
        
        # Section depth
        if metrics['sections'] >= 8:
            score += 3
        
        return min(score, 10)
    
    def _evaluate_visuals(self, metrics):
        """Evaluate tables and figures"""
        score = 0
        
        # Figures
        if metrics['figures'] >= 3:
            score += 5
        elif metrics['figures'] >= 2:
            score += 3
        elif metrics['figures'] >= 1:
            score += 1
        
        # Tables
        if metrics['tables'] >= 2:
            score += 5
        elif metrics['tables'] >= 1:
            score += 3
        
        return min(score, 10)
    
    def _evaluate_writing(self, tex_content):
        """Evaluate writing quality"""
        import re
        
        score = 0
        
        # Academic transitions
        transitions = ['furthermore', 'moreover', 'consequently', 'however', 
                      'therefore', 'in contrast', 'in summary', 'notably',
                      'specifically', 'building upon', 'to establish']
        
        transition_count = sum(1 for t in transitions if t.lower() in tex_content.lower())
        
        if transition_count >= 10:
            score += 4
        elif transition_count >= 5:
            score += 2
        
        # Formal language indicators
        formal_patterns = [r'\\textbf', r'\\textit', r'\\section', r'\\subsection']
        formal_count = sum(len(re.findall(p, tex_content)) for p in formal_patterns)
        
        if formal_count >= 20:
            score += 3
        elif formal_count >= 10:
            score += 2
        
        # LaTeX quality
        if '\\cite' in tex_content:
            score += 3
        
        return min(score, 10)
    
    def _generate_feedback(self, scores, metrics):
        """Generate actionable feedback"""
        feedback = []
        
        if scores['references'] < 8:
            feedback.append(f"📚 Add more references (current: {metrics['references']}, target: 50+)")
        
        if scores['content'] < 8:
            feedback.append(f"📝 Expand content depth (current: ~{metrics['word_count']} words, target: 8000+)")
        
        if scores['tables_figures'] < 8:
            feedback.append(f"📊 Add more visuals (figures: {metrics['figures']}, tables: {metrics['tables']}, target: 3+ figures, 2+ tables)")
        
        if scores['writing'] < 8:
            feedback.append("✍️ Enhance academic writing with more transitions and formal language")
        
        if scores['structure'] < 10:
            feedback.append(f"📑 Ensure all 8 standard sections are present (current: {metrics['sections']})")
        
        return feedback
