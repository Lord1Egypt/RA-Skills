#!/usr/bin/env python3
"""Formal scoring and pairwise comparison for abstract fragments."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List

from abstract_lint import lint_text, split_sentences

ROOT = Path(__file__).resolve().parents[1]
RULES_PATH = ROOT / 'assets' / 'discourse_rules.json'


def load_rules() -> Dict:
    return json.loads(RULES_PATH.read_text(encoding='utf-8'))


def count_rule(report: Dict, rule_name: str) -> int:
    return sum(1 for issue in report['issues'] if issue['rule'] == rule_name)


def count_relation_bonus(text: str, rules: Dict) -> int:
    sentences = split_sentences(text)
    relation_verbs = rules.get('relation_verbs', [])
    artifact_heads = rules.get('artifact_heads', [])
    total = 0
    for sentence in sentences:
        low = sentence.lower()
        hits = 0
        if any(verb in low for verb in relation_verbs):
            hits += 1
        if ' for ' in f' {low} ' and any(head in low for head in artifact_heads):
            hits += 1
        if re.search(r'\bto\s+[a-z]+', low) and any(token in low for token in ['translate', 'align', 'reduce', 'maintain', 'decouple', 'ground', 'extract', 'support', 'enable']):
            hits += 1
        total += min(hits, 2)
    return total


def count_evidence_bonus(text: str, rules: Dict) -> int:
    sentences = split_sentences(text)
    evidence_tokens = rules.get('evidence_tokens', [])
    total = 0
    for sentence in sentences:
        low = sentence.lower()
        if any(token in low for token in evidence_tokens) or re.search(r'\b\d+(?:\.\d+)?\b', low):
            total += 1
    return total


def feature_vector(text: str) -> Dict[str, int]:
    rules = load_rules()
    report = lint_text(text)
    return {
        'missing_core_role': count_rule(report, 'missing_core_role'),
        'role_order_violation': count_rule(report, 'role_order_violation'),
        'summary_only': count_rule(report, 'summary_only'),
        'forbidden_marker': count_rule(report, 'forbidden_marker'),
        'selection_mismatch': count_rule(report, 'selection_mismatch'),
        'terminal_load': count_rule(report, 'terminal_load'),
        'relation_bonus': count_relation_bonus(text, rules),
        'evidence_bonus': count_evidence_bonus(text, rules),
    }


def score_from_features(features: Dict[str, int], rules: Dict) -> int:
    score = 100
    penalties = rules['score_weights']['penalties']
    bonuses = rules['score_weights']['bonuses']

    for key, weight in penalties.items():
        score -= weight * features.get(key, 0)
    for key, weight in bonuses.items():
        score += weight * features.get(key, 0)

    score = max(0, min(100, score))
    return int(score)


def analyze_text(text: str) -> Dict:
    rules = load_rules()
    features = feature_vector(text)
    score = score_from_features(features, rules)
    return {
        'score': score,
        'features': features,
    }


def compare_texts(text_a: str, text_b: str) -> Dict:
    ana_a = analyze_text(text_a)
    ana_b = analyze_text(text_b)
    delta = ana_b['score'] - ana_a['score']
    feature_delta = {key: ana_b['features'].get(key, 0) - ana_a['features'].get(key, 0) for key in sorted(set(ana_a['features']) | set(ana_b['features']))}
    winner = 'B' if delta > 0 else 'A' if delta < 0 else 'tie'
    return {
        'a': ana_a,
        'b': ana_b,
        'delta': delta,
        'winner': winner,
        'feature_delta': feature_delta,
    }


def format_single(label: str, result: Dict) -> str:
    lines: List[str] = []
    lines.append(f'{label} score: {result["score"]}/100')
    lines.append('Features:')
    for key, value in sorted(result['features'].items()):
        lines.append(f'  - {key}: {value}')
    return '\n'.join(lines)


def format_compare(result: Dict) -> str:
    lines: List[str] = []
    lines.append(f'A score: {result["a"]["score"]}/100')
    lines.append(f'B score: {result["b"]["score"]}/100')
    sign = '+' if result['delta'] > 0 else ''
    lines.append(f'Delta (B - A): {sign}{result["delta"]}')
    lines.append(f'Winner: {result["winner"]}')
    lines.append('Feature delta (B - A):')
    for key, value in sorted(result['feature_delta'].items()):
        sign = '+' if value > 0 else ''
        lines.append(f'  - {key}: {sign}{value}')
    return '\n'.join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description='Score one abstract fragment or compare two fragments.')
    parser.add_argument('input_file', help='Path to the first text file.')
    parser.add_argument('--compare', help='Optional second text file for pairwise comparison.')
    parser.add_argument('--json', action='store_true', dest='as_json', help='Print JSON output.')
    args = parser.parse_args()

    text_a = Path(args.input_file).read_text(encoding='utf-8')
    if args.compare:
        text_b = Path(args.compare).read_text(encoding='utf-8')
        result = compare_texts(text_a, text_b)
        if args.as_json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(format_compare(result))
    else:
        result = analyze_text(text_a)
        if args.as_json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(format_single('A', result))


if __name__ == '__main__':
    main()
