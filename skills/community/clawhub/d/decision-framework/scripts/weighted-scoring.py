#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Weighted Scoring Calculator - 加权打分计算器

Usage:
    python weighted-scoring.py --dimensions "薪资:30,成长:25,强度:20,地点:15,团队:10" \
                               --options "Offer A:8,7,6,9,8;Offer B:9,6,7,8,7;Offer C:7,9,8,7,9"

Output: Markdown table with scores and rankings
"""

import argparse
import sys
from typing import Dict, List, Tuple

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


def parse_dimensions(dim_str: str) -> List[Tuple[str, float]]:
    """Parse dimension string like '薪资:30,成长:25' into list of (name, weight) tuples"""
    dimensions = []
    for item in dim_str.split(','):
        if ':' not in item:
            continue
        name, weight = item.split(':')
        dimensions.append((name.strip(), float(weight)))
    
    # Validate weights sum to ~100
    total = sum(w for _, w in dimensions)
    if abs(total - 100) > 1:
        print(f"⚠️  Warning: weights sum to {total}, not 100", file=sys.stderr)
    
    return dimensions


def parse_options(opt_str: str, num_dimensions: int) -> List[Tuple[str, List[float]]]:
    """Parse options string like 'Offer A:8,7,6;Offer B:9,6,7' into list of (name, scores) tuples"""
    options = []
    for item in opt_str.split(';'):
        if ':' not in item:
            continue
        parts = item.split(':')
        name = parts[0].strip()
        scores = [float(x) for x in parts[1].split(',')]
        if len(scores) != num_dimensions:
            print(f"⚠️  Warning: {name} has {len(scores)} scores, expected {num_dimensions}", file=sys.stderr)
        options.append((name, scores))
    return options


def calculate_weighted_score(scores: List[float], weights: List[float]) -> float:
    """Calculate weighted score"""
    return sum(s * w / 100 for s, w in zip(scores, weights))


def generate_markdown_table(dimensions: List[Tuple[str, float]], 
                           options: List[Tuple[str, List[float]]]) -> str:
    """Generate markdown table with weighted scores"""
    lines = []
    
    # Header
    header = "| 维度 | 权重 | " + " | ".join(name for name, _ in options) + " |"
    lines.append(header)
    
    # Separator
    sep = "|------|------|" + "------|" * len(options)
    lines.append(sep)
    
    # Dimension rows
    for i, (dim_name, weight) in enumerate(dimensions):
        row = f"| {dim_name} | {weight}% |"
        for _, scores in options:
            score = scores[i] if i < len(scores) else 0
            weighted = score * weight / 100
            row += f" {score} ({weighted:.1f}) |"
        lines.append(row)
    
    # Total row
    total_row = "| **总分** | 100% |"
    for name, scores in options:
        total = calculate_weighted_score(scores, [w for _, w in dimensions])
        total_row += f" **{total:.1f}** |"
    lines.append(total_row)
    
    return '\n'.join(lines)


def generate_ranking(options: List[Tuple[str, List[float]]], 
                    dimensions: List[Tuple[str, float]]) -> str:
    """Generate ranking summary"""
    weights = [w for _, w in dimensions]
    scored = [(name, calculate_weighted_score(scores, weights)) for name, scores in options]
    scored.sort(key=lambda x: x[1], reverse=True)
    
    lines = ["\n## 排名"]
    for i, (name, score) in enumerate(scored, 1):
        # Use text medals for better compatibility
        if i == 1:
            medal = "1."
        elif i == 2:
            medal = "2."
        elif i == 3:
            medal = "3."
        else:
            medal = f"{i}."
        lines.append(f"{medal} {name}: {score:.1f} 分")
    
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Weighted Scoring Calculator')
    parser.add_argument('--dimensions', required=True, help='Dimensions with weights (e.g., "薪资:30,成长:25")')
    parser.add_argument('--options', required=True, help='Options with scores (e.g., "A:8,7,6;B:9,6,7")')
    args = parser.parse_args()
    
    dimensions = parse_dimensions(args.dimensions)
    options = parse_options(args.options, len(dimensions))
    
    if not dimensions or not options:
        print("Error: Invalid input", file=sys.stderr)
        sys.exit(1)
    
    print("# 加权打分结果\n")
    print(generate_markdown_table(dimensions, options))
    print(generate_ranking(options, dimensions))


if __name__ == '__main__':
    main()
