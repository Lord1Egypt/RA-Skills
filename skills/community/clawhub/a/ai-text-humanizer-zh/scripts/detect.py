#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Command-line interface for AI text detection."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.analyzer import AIDetector
from core.utils import read_file


def print_report(report):
    """打印格式化检测报告"""
    icons = {"very high": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}
    
    print(f"\n{'='*60}")
    print(f"AI DETECTION REPORT")
    print(f"{'='*60}\n")
    
    print(f"Word Count: {report.word_count}")
    print(f"Character Count: {report.char_count}")
    print(f"Total Issues: {report.total_issues}")
    print(f"AI Probability: {icons.get(report.ai_level, '')} {report.ai_probability:.1f}% (Level: {report.ai_level.upper()})")
    
    print(f"\n{'-'*60}")
    print("Category Breakdown:")
    print(f"{'-'*60}")
    
    categories = [
        ("AI Jargon", report.ai_jargon_count),
        ("Puffery (夸大)", report.puffery_count),
        ("Marketing Speak", report.marketing_count),
        ("Vague Attributions", report.vague_count),
        ("Hedging", report.hedging_count),
        ("Chatbot Artifacts", report.chatbot_count),
        ("Citation Bugs", report.citation_count),
        ("Knowledge Cutoff", report.cutoff_count),
        ("Markdown", report.markdown_count),
        ("Negative Parallelisms", report.negative_parallel_count),
        ("Superficial Verbs", report.superficial_verb_count),
        ("Filler Phrases", report.filler_count),
        ("Rule of Three", report.rule_of_three_count),
        ("Sentence Starters", report.sentence_starter_count),
        ("Rhetorical Patterns", report.rhetorical_count),
        ("List Markers", report.list_marker_count),
    ]
    
    for name, count in categories:
        if count > 0:
            print(f"  {name:<25} {count}")
    
    punct = [
        ("Em dashes (——)", report.em_dash_count),
        ("Curly quotes", report.curly_quote_count),
        ("Exclamation marks", report.exclamation_count),
        ("Question marks", report.question_count),
    ]
    
    print(f"\n{'-'*60}")
    print("Punctuation:")
    print(f"{'-'*60}")
    for name, count in punct:
        if count > 0:
            print(f"  {name:<25} {count}")
    
    if report.sentence_reports:
        high_risk_sentences = [s for s in report.sentence_reports if s.score > 0]
        if high_risk_sentences:
            print(f"\n{'='*60}")
            print("Suspicious Sentences (with issues):")
            print(f"{'='*60}")
            for i, s in enumerate(high_risk_sentences[:10], 1):
                print(f"\n{i}. [Score: {s.score}] {s.sentence[:100]}...")
                if s.reasons:
                    print(f"   Reasons: {', '.join(s.reasons[:3])}")
            if len(high_risk_sentences) > 10:
                print(f"\n... and {len(high_risk_sentences) - 10} more suspicious sentences.")


def main():
    parser = argparse.ArgumentParser(
        description="Detect AI patterns in text (no rewriting)"
    )
    parser.add_argument("input", nargs="?", help="Input file (or read from stdin)")
    parser.add_argument("-j", "--json", action="store_true", help="Output results in JSON format")
    parser.add_argument("-s", "--score-only", action="store_true", help="Print only score and probability")
    parser.add_argument("-r", "--rules", help="User-defined rules JSON file")
    parser.add_argument("--no-sentences", action="store_true", help="Skip displaying suspicious sentences")
    
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
    report = detector.detect(text)
    
    if args.json:
        output = {
            "word_count": report.word_count,
            "char_count": report.char_count,
            "total_issues": report.total_issues,
            "ai_probability": report.ai_probability,
            "ai_level": report.ai_level,
            "categories": {
                "ai_jargon": report.ai_jargon_count,
                "puffery": report.puffery_count,
                "marketing": report.marketing_count,
                "vague": report.vague_count,
                "hedging": report.hedging_count,
                "chatbot": report.chatbot_count,
                "citation": report.citation_count,
                "cutoff": report.cutoff_count,
                "markdown": report.markdown_count,
                "negative_parallel": report.negative_parallel_count,
                "superficial_verb": report.superficial_verb_count,
                "filler": report.filler_count,
                "rule_of_three": report.rule_of_three_count,
                "sentence_starter": report.sentence_starter_count,
                "rhetorical": report.rhetorical_count,
                "list_marker": report.list_marker_count,
            },
            "punctuation": {
                "em_dash": report.em_dash_count,
                "curly_quote": report.curly_quote_count,
                "exclamation": report.exclamation_count,
                "question": report.question_count,
            },
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    elif args.score_only:
        print(f"Issues: {report.total_issues} | Words: {report.word_count} | AI: {report.ai_probability:.1f}% ({report.ai_level})")
    else:
        print_report(report)


if __name__ == "__main__":
    main()
