#!/usr/bin/env python3
"""
ContextSlim - Compression Suggestion Engine
Analyzes text and provides actionable compression recommendations.

Author: Shadow Rose
License: MIT
"""

import re
from typing import List, Dict, Tuple
from dataclasses import dataclass
from context_slim import TokenEstimator


@dataclass
class CompressionSuggestion:
    """A single compression suggestion with before/after comparison."""
    category: str  # 'redundancy', 'verbosity', 'formatting', 'examples'
    description: str
    original: str
    suggested: str
    tokens_saved: int
    confidence: str  # 'high', 'medium', 'low'


class CompressionAnalyzer:
    """Analyzes text and generates compression suggestions."""
    
    def __init__(self, provider: str = 'generic'):
        """
        Initialize compression analyzer.
        
        Args:
            provider: Provider type for token estimation
        """
        self.provider = provider
    
    def analyze(self, text: str) -> List[CompressionSuggestion]:
        """
        Analyze text and generate compression suggestions.
        
        Args:
            text: Input text to analyze
        
        Returns:
            List of compression suggestions
        """
        suggestions = []
        
        # Check for redundant phrases
        suggestions.extend(self._find_redundant_phrases(text))
        
        # Check for verbose language
        suggestions.extend(self._find_verbose_patterns(text))
        
        # Check for excessive examples
        suggestions.extend(self._find_excessive_examples(text))
        
        # Check for formatting inefficiencies
        suggestions.extend(self._find_formatting_issues(text))
        
        # Check for repetitive instructions
        suggestions.extend(self._find_repetitive_instructions(text))
        
        return suggestions
    
    def _find_redundant_phrases(self, text: str) -> List[CompressionSuggestion]:
        """Find redundant phrases that can be simplified."""
        suggestions = []
        
        # Common redundant patterns
        redundancies = [
            (r'in order to', 'to'),
            (r'at this point in time', 'now'),
            (r'due to the fact that', 'because'),
            (r'in the event that', 'if'),
            (r'for the purpose of', 'to'),
            (r'with the exception of', 'except'),
            (r'in spite of the fact that', 'although'),
            (r'until such time as', 'until'),
            (r'in the process of', 'while'),
            (r'in a timely manner', 'promptly'),
        ]
        
        for pattern, replacement in redundancies:
            matches = list(re.finditer(pattern, text, re.IGNORECASE))
            
            for match in matches:
                original = match.group(0)
                # Find surrounding context (20 chars each side)
                start = max(0, match.start() - 20)
                end = min(len(text), match.end() + 20)
                context = text[start:end]
                
                suggested_context = context.replace(original, replacement)
                
                tokens_saved = TokenEstimator.estimate(original, self.provider) - \
                              TokenEstimator.estimate(replacement, self.provider)
                
                suggestions.append(CompressionSuggestion(
                    category='redundancy',
                    description=f'Replace "{original}" with "{replacement}"',
                    original=context,
                    suggested=suggested_context,
                    tokens_saved=tokens_saved,
                    confidence='high'
                ))
        
        return suggestions
    
    def _find_verbose_patterns(self, text: str) -> List[CompressionSuggestion]:
        """Find verbose language patterns that can be tightened."""
        suggestions = []
        
        # Verbose patterns
        patterns = [
            (r'it is important to note that', 'note:'),
            (r'please be aware that', ''),
            (r'as a matter of fact', 'in fact'),
            (r'the fact that', 'that'),
            (r'is able to', 'can'),
            (r'has the ability to', 'can'),
            (r'in a situation where', 'when'),
            (r'a large number of', 'many'),
            (r'a small number of', 'few'),
        ]
        
        for pattern, replacement in patterns:
            matches = list(re.finditer(pattern, text, re.IGNORECASE))
            
            for match in matches[:3]:  # Limit to 3 suggestions per pattern
                original = match.group(0)
                start = max(0, match.start() - 30)
                end = min(len(text), match.end() + 30)
                context = text[start:end]
                
                suggested_context = context.replace(original, replacement).strip()
                
                tokens_saved = TokenEstimator.estimate(original, self.provider) - \
                              TokenEstimator.estimate(replacement, self.provider)
                
                if tokens_saved > 0:
                    suggestions.append(CompressionSuggestion(
                        category='verbosity',
                        description=f'Simplify verbose phrase',
                        original=context,
                        suggested=suggested_context,
                        tokens_saved=tokens_saved,
                        confidence='medium'
                    ))
        
        return suggestions
    
    def _find_excessive_examples(self, text: str) -> List[CompressionSuggestion]:
        """Find excessive examples that could be condensed."""
        suggestions = []
        
        # Look for example patterns
        example_markers = [
            r'for example:',
            r'e\.g\.',
            r'such as',
            r'like:',
        ]
        
        for marker in example_markers:
            matches = list(re.finditer(marker, text, re.IGNORECASE))
            
            for match in matches:
                # Find the example section (next 200 chars)
                start = match.start()
                end = min(len(text), match.end() + 200)
                example_section = text[start:end]
                
                # Count items in the example (commas, "and", "or")
                item_count = example_section.count(',') + \
                            example_section.count(' and ') + \
                            example_section.count(' or ')
                
                # If more than 3 items, suggest condensing
                if item_count > 3:
                    original_tokens = TokenEstimator.estimate(example_section, self.provider)
                    
                    suggestions.append(CompressionSuggestion(
                        category='examples',
                        description=f'Consider condensing {item_count} examples to 2-3 key ones',
                        original=example_section[:100] + '...',
                        suggested='[Condense to 2-3 most relevant examples]',
                        tokens_saved=int(original_tokens * 0.4),  # Estimate 40% savings
                        confidence='medium'
                    ))
        
        return suggestions[:3]  # Limit total example suggestions
    
    def _find_formatting_issues(self, text: str) -> List[CompressionSuggestion]:
        """Find formatting inefficiencies."""
        suggestions = []
        
        # Check for excessive newlines
        excessive_newlines = re.finditer(r'\n{4,}', text)
        for match in excessive_newlines:
            original = match.group(0)
            tokens_saved = TokenEstimator.estimate(original, self.provider) - \
                          TokenEstimator.estimate('\n\n', self.provider)
            
            if tokens_saved > 0:
                suggestions.append(CompressionSuggestion(
                    category='formatting',
                    description='Reduce excessive blank lines',
                    original=f'{len(original)} newlines',
                    suggested='2 newlines',
                    tokens_saved=tokens_saved,
                    confidence='high'
                ))
        
        # Check for long separator lines
        separators = re.finditer(r'[-=*]{10,}', text)
        for match in separators[:3]:
            original = match.group(0)
            suggested = original[:5]
            tokens_saved = TokenEstimator.estimate(original, self.provider) - \
                          TokenEstimator.estimate(suggested, self.provider)
            
            if tokens_saved > 0:
                suggestions.append(CompressionSuggestion(
                    category='formatting',
                    description='Shorten separator line',
                    original=original,
                    suggested=suggested,
                    tokens_saved=tokens_saved,
                    confidence='medium'
                ))
        
        return suggestions
    
    def _find_repetitive_instructions(self, text: str) -> List[CompressionSuggestion]:
        """Find repetitive instructions or phrases."""
        suggestions = []
        
        # Split into sentences
        sentences = re.split(r'[.!?]+', text)
        
        # Look for similar sentences (simple word overlap check)
        seen = {}
        for idx, sentence in enumerate(sentences):
            if len(sentence.strip()) < 20:
                continue
            
            words = set(sentence.lower().split())
            
            for prev_idx, prev_words in seen.items():
                # Calculate overlap
                overlap = len(words & prev_words) / len(words | prev_words) if words | prev_words else 0
                
                if overlap > 0.6:  # 60% similar
                    original = sentences[prev_idx].strip() + '. ' + sentence.strip() + '.'
                    suggested = '[Consider consolidating these similar instructions]'
                    tokens_saved = TokenEstimator.estimate(sentence, self.provider)
                    
                    suggestions.append(CompressionSuggestion(
                        category='redundancy',
                        description='Possible repetitive instruction',
                        original=original[:150],
                        suggested=suggested,
                        tokens_saved=tokens_saved,
                        confidence='low'
                    ))
            
            seen[idx] = words
        
        return suggestions[:2]  # Limit to 2 repetition suggestions
    
    def estimate_total_savings(self, suggestions: List[CompressionSuggestion]) -> int:
        """
        Estimate total tokens that could be saved.
        
        Args:
            suggestions: List of compression suggestions
        
        Returns:
            Estimated total tokens saved
        """
        return sum(s.tokens_saved for s in suggestions)
    
    def filter_by_confidence(self, suggestions: List[CompressionSuggestion], 
                            min_confidence: str = 'low') -> List[CompressionSuggestion]:
        """
        Filter suggestions by confidence level.
        
        Args:
            suggestions: List of suggestions to filter
            min_confidence: Minimum confidence level ('high', 'medium', 'low')
        
        Returns:
            Filtered list of suggestions
        """
        confidence_order = ['low', 'medium', 'high']
        min_level = confidence_order.index(min_confidence)
        
        return [s for s in suggestions 
                if confidence_order.index(s.confidence) >= min_level]


def main():
    """CLI interface for compression analyzer."""
    import argparse
    import sys
    import json
    
    parser = argparse.ArgumentParser(
        description='ContextSlim Compression Analyzer'
    )
    parser.add_argument(
        'input',
        nargs='?',
        help='Input file path or text (reads from stdin if not provided)'
    )
    parser.add_argument(
        '--provider',
        default='generic',
        help='AI provider type for token estimation'
    )
    parser.add_argument(
        '--min-confidence',
        default='low',
        choices=['high', 'medium', 'low'],
        help='Minimum confidence level for suggestions'
    )
    parser.add_argument(
        '--output',
        default='text',
        choices=['text', 'json'],
        help='Output format'
    )
    
    args = parser.parse_args()
    
    # Get input
    if args.input:
        try:
            with open(args.input, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception as e:
            print(f"Error reading file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        text = sys.stdin.read()
    
    # Analyze
    analyzer = CompressionAnalyzer(provider=args.provider)
    suggestions = analyzer.analyze(text)
    
    # Filter by confidence
    suggestions = analyzer.filter_by_confidence(suggestions, args.min_confidence)
    
    # Output
    if args.output == 'json':
        output = {
            'total_suggestions': len(suggestions),
            'total_tokens_saved': analyzer.estimate_total_savings(suggestions),
            'suggestions': [
                {
                    'category': s.category,
                    'description': s.description,
                    'original': s.original,
                    'suggested': s.suggested,
                    'tokens_saved': s.tokens_saved,
                    'confidence': s.confidence
                }
                for s in suggestions
            ]
        }
        print(json.dumps(output, indent=2))
    else:
        print(f"\n=== ContextSlim Compression Analysis ===")
        print(f"Found {len(suggestions)} suggestions")
        print(f"Potential savings: {analyzer.estimate_total_savings(suggestions)} tokens\n")
        
        for idx, s in enumerate(suggestions, 1):
            print(f"{idx}. [{s.category.upper()}] {s.description}")
            print(f"   Confidence: {s.confidence} | Saves: ~{s.tokens_saved} tokens")
            print(f"   Original: {s.original[:80]}")
            print(f"   Suggested: {s.suggested[:80]}")
            print()


if __name__ == '__main__':
    main()
