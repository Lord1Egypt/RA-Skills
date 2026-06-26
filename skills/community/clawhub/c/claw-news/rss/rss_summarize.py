#!/usr/bin/env python3
"""
News Summarizer - Generate AI-powered summaries for news articles.

This script can work in two modes:
1. Local mode: Uses simple extractive summarization (no external API)
2. API mode: Calls OpenClaw or external LLM for abstractive summaries

Usage:
    python summarize.py [options]

Options:
    --input FILE        Input JSON file from fetch_news.py
    --output FILE       Output JSON file (default: stdout)
    --max-length N      Max summary length in words (default: 150)
    --method METHOD     Summarization method: extractive|api (default: extractive)
    --fields FIELDS     Comma-separated fields to summarize (default: title,summary)
    --verbose, -v       Verbose output
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List

# Import Kimi API client
try:
    from kimi_client import load_config, batch_summarize_with_kimi
    HAS_KIMI_CLIENT = True
except ImportError:
    HAS_KIMI_CLIENT = False


def clean_text(text: str) -> str:
    """Clean and normalize text."""
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', ' ', text)
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    # Decode HTML entities
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&amp;', '&')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&quot;', '"')
    return text.strip()


def sentence_tokenize(text: str) -> List[str]:
    """Simple sentence tokenization."""
    # Split on sentence endings
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]


def word_tokenize(text: str) -> List[str]:
    """Simple word tokenization."""
    return text.split()


def calculate_sentence_scores(sentences: List[str]) -> Dict[int, float]:
    """Calculate importance scores for sentences using simple heuristics."""
    scores = {}
    
    # Word frequency
    word_freq = {}
    for sentence in sentences:
        words = word_tokenize(sentence.lower())
        for word in words:
            if len(word) > 3:  # Ignore short words
                word_freq[word] = word_freq.get(word, 0) + 1
    
    # Score each sentence
    for i, sentence in enumerate(sentences):
        score = 0
        words = word_tokenize(sentence.lower())
        
        # Frequency score
        for word in words:
            if word in word_freq:
                score += word_freq[word]
        
        # Position bonus (earlier sentences often more important)
        if i < 3:
            score *= 1.5
        
        # Length penalty (avoid very short/long sentences)
        word_count = len(words)
        if word_count < 5:
            score *= 0.5
        elif word_count > 50:
            score *= 0.8
        
        scores[i] = score / max(len(words), 1)
    
    return scores


def extractive_summarize(text: str, max_words: int = 150) -> str:
    """Generate extractive summary using sentence scoring."""
    text = clean_text(text)
    
    if not text:
        return ""
    
    sentences = sentence_tokenize(text)
    
    if len(sentences) <= 2:
        return text
    
    # Calculate scores
    scores = calculate_sentence_scores(sentences)
    
    # Sort by score, keep original order
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    # Select top sentences until max_words
    selected_indices = []
    total_words = 0
    
    for idx, score in ranked:
        sentence_words = len(word_tokenize(sentences[idx]))
        if total_words + sentence_words <= max_words:
            selected_indices.append(idx)
            total_words += sentence_words
        else:
            break
    
    # Sort by original position
    selected_indices.sort()
    
    # Reconstruct summary
    summary = ' '.join(sentences[i] for i in selected_indices)
    return summary


def summarize_item(item: Dict, max_words: int = 150, fields: List[str] = None) -> Dict:
    """Summarize a single news item."""
    if fields is None:
        fields = ['title', 'summary']
    
    # Combine fields to summarize
    text_parts = []
    for field in fields:
        if field in item and item[field]:
            text_parts.append(item[field])
    
    text = ' '.join(text_parts)
    
    if not text:
        return item
    
    # Generate summary
    summary = extractive_summarize(text, max_words)
    
    # Create result
    result = item.copy()
    result['ai_summary'] = summary
    result['summary_length'] = len(word_tokenize(summary))
    result['original_length'] = len(word_tokenize(text))
    result['compression_ratio'] = round(result['summary_length'] / max(result['original_length'], 1), 2)
    
    return result


def batch_summarize(items: List[Dict], max_words: int = 150, fields: List[str] = None) -> List[Dict]:
    """Summarize multiple news items."""
    results = []
    for i, item in enumerate(items):
        result = summarize_item(item, max_words, fields)
        results.append(result)
    return results


def format_summary_output(items: List[Dict]) -> Dict:
    """Format output with summary statistics."""
    total_original = sum(item.get('original_length', 0) for item in items)
    total_summary = sum(item.get('summary_length', 0) for item in items)
    
    return {
        'summarized_at': __import__('datetime').datetime.now().isoformat(),
        'total_items': len(items),
        'total_original_words': total_original,
        'total_summary_words': total_summary,
        'overall_compression': round(total_summary / max(total_original, 1), 2),
        'items': items
    }


def main():
    parser = argparse.ArgumentParser(description='Summarize news articles')
    parser.add_argument('--input', '-i', help='Input JSON file')
    parser.add_argument('--output', '-o', help='Output JSON file (default: stdout)')
    parser.add_argument('--max-length', '-l', type=int, default=150, help='Max summary length in words')
    parser.add_argument('--method', '-m', default='extractive', choices=['extractive', 'api'],
                        help='Summarization method')
    parser.add_argument('--fields', '-f', default='title,summary',
                        help='Comma-separated fields to summarize')
    parser.add_argument('--limit', '-n', type=int, help='Limit number of items to process')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    # Read input
    if args.input:
        with open(args.input, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = json.load(sys.stdin)
    
    # Extract items
    if 'items' in data:
        items = data['items']
    else:
        items = data if isinstance(data, list) else [data]
    
    if args.limit:
        items = items[:args.limit]
    
    if args.verbose:
        print(f"Processing {len(items)} items...", file=sys.stderr)
    
    # Parse fields
    fields = [f.strip() for f in args.fields.split(',')]
    
    # Summarize
    if args.method == 'extractive':
        results = batch_summarize(items, args.max_length, fields)
    else:
        # API method using Kimi
        if not HAS_KIMI_CLIENT:
            print("Kimi client not available, falling back to extractive", file=sys.stderr)
            results = batch_summarize(items, args.max_length, fields)
        else:
            try:
                config = load_config()
                if not config.get('kimi', {}).get('api_key'):
                    print("Kimi API key not configured, falling back to extractive", file=sys.stderr)
                    results = batch_summarize(items, args.max_length, fields)
                else:
                    if args.verbose:
                        print(f"Using Kimi API for summarization (model: {config['kimi']['model']})...", file=sys.stderr)
                    results = batch_summarize_with_kimi(items, config)
            except Exception as e:
                print(f"Kimi API error: {e}, falling back to extractive", file=sys.stderr)
                results = batch_summarize(items, args.max_length, fields)
    
    # Format output
    output = format_summary_output(results)
    
    # Write output
    json_output = json.dumps(output, ensure_ascii=False, indent=2)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(json_output)
        if args.verbose:
            print(f"Output written to: {args.output}", file=sys.stderr)
            print(f"Summary: {output['total_original_words']} -> {output['total_summary_words']} words", file=sys.stderr)
    else:
        print(json_output)


if __name__ == '__main__':
    main()
