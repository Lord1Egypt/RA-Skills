#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compare before/after transformation with side-by-side detection scores."""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.analyzer import AIDetector
from core.rewrite import AIRewriter
from core.utils import read_file, write_file


def main():
    parser = argparse.ArgumentParser(
        description="Compare AI detection before/after transformation"
    )
    parser.add_argument("input", nargs="?", help="Input file (or read from stdin)")
    parser.add_argument("-a", "--aggressive", action="store_true", help="Use aggressive rewriting mode")
    parser.add_argument("-o", "--output", help="Save transformed text to file")
    parser.add_argument("-r", "--rules", help="User-defined rules JSON file")
    parser.add_argument("-q", "--quiet", action="store_true", help="Suppress detailed output")
    
    args = parser.parse_args()
    
    if args.input:
        try:
            text = read_file(args.input)
        except FileNotFoundError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        text = sys.stdin.read()
    
    if not text:
        print("Error: No input text provided", file=sys.stderr)
        sys.exit(1)
    
    detector = AIDetector(user_rules_path=args.rules)
    rewriter = AIRewriter(user_rules_path=args.rules)
    
    before = detector.detect(text)
    transformed, changes = rewriter.rewrite(text, aggressive=args.aggressive)
    after = detector.detect(transformed)
    
    icons = {"very high": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}
    
    print(f"\n{'='*60}")
    print("BEFORE → AFTER COMPARISON")
    print(f"{'='*60}\n")
    
    print(f"{'Metric':<25} {'Before':<15} {'After':<15} {'Change':<10}")
    print(f"{'-'*60}")
    
    issue_diff = after.total_issues - before.total_issues
    issue_sign = "+" if issue_diff > 0 else ""
    print(f"{'Issues':<25} {before.total_issues:<15} {after.total_issues:<15} {issue_sign}{issue_diff}")
    
    prob_before = f"{before.ai_probability:.1f}%"
    prob_after = f"{after.ai_probability:.1f}%"
    print(f"{'AI Probability':<25} {before.ai_level} ({prob_before}) → {after.ai_level} ({prob_after})")
    print(f"{'Word Count':<25} {before.word_count:<15} {after.word_count:<15} {after.word_count - before.word_count:+}")
    
    if not args.quiet:
        print(f"\n{'Category Changes':<25} {'Before':<15} {'After':<15} {'Change':<10}")
        print(f"{'-'*60}")
        
        categories = [
            ("AI Jargon", "ai_jargon_count"),
            ("Puffery", "puffery_count"),
            ("Marketing Speak", "marketing_count"),
            ("Vague Attributions", "vague_count"),
            ("Hedging", "hedging_count"),
            ("Chatbot Artifacts", "chatbot_count"),
            ("Citation Bugs", "citation_count"),
            ("Knowledge Cutoff", "cutoff_count"),
            ("Markdown", "markdown_count"),
            ("Filler Phrases", "filler_count"),
        ]
        
        for name, attr in categories:
            before_val = getattr(before, attr)
            after_val = getattr(after, attr)
            diff = after_val - before_val
            diff_str = f"+{diff}" if diff > 0 else str(diff)
            print(f"{name:<25} {before_val:<15} {after_val:<15} {diff_str}")
    
    if changes and not args.quiet:
        print(f"\n{'='*60}")
        print(f"TRANSFORMATIONS ({len(changes)})")
        print(f"{'='*60}")
        for c in changes:
            print(f" • {c}")
    
    reduction = before.total_issues - after.total_issues
    if reduction > 0:
        pct = (reduction / before.total_issues * 100) if before.total_issues else 0
        print(f"\n✓ Reduced {reduction} issues ({pct:.0f}% improvement)")
    elif reduction < 0:
        print(f"\n⚠ Issues increased by {-reduction}")
    else:
        print(f"\n— No change in issue count")
    
    if args.output:
        write_file(args.output, transformed)
        print(f"\n→ Saved to {args.output}")


if __name__ == "__main__":
    main()
