#!/usr/bin/env python3
"""Heuristic linter for ontology-aware academic abstracts."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]
RULES_PATH = ROOT / 'assets' / 'discourse_rules.json'
LEXICON_PATH = ROOT / 'assets' / 'lexeme_types.json'


def load_json(path: Path) -> Dict:
    return json.loads(path.read_text(encoding='utf-8'))


def split_sentences(text: str) -> List[str]:
    text = text.strip()
    if not text:
        return []
    text = re.sub(r'\s+', ' ', text)
    pieces = re.split(r'(?<=[.!?])\s+', text)
    return [p.strip() for p in pieces if p.strip()]


def classify_role(sentence: str, role_cues: Dict[str, List[str]], order: List[str]) -> Optional[str]:
    s = sentence.lower()
    scores: Dict[str, int] = {}
    for role, cues in role_cues.items():
        score = 0
        for cue in cues:
            if cue.lower() in s:
                score += 1
        if score:
            scores[role] = score
    if not scores:
        return None
    ranked = sorted(scores.items(), key=lambda x: (-x[1], order.index(x[0]) if x[0] in order else 999))
    return ranked[0][0]


def find_forbidden(sentence: str, banned_patterns: List[str]) -> List[str]:
    found: List[str] = []
    for pattern in banned_patterns:
        token = pattern.encode('utf-8').decode('unicode_escape')
        if token.lower() in sentence.lower():
            found.append(token)
    return found


def find_summary_only(sentence: str, regexes: List[str]) -> List[str]:
    s = sentence.lower()
    hits: List[str] = []
    for expr in regexes:
        if re.search(expr, s):
            hits.append(expr)
    return hits


def noun_type(noun: str, noun_types: Dict[str, List[str]]) -> List[str]:
    noun = noun.strip().lower()
    return noun_types.get(noun, [])


def check_selection_mismatch(sentence: str, lexicon: Dict) -> List[Tuple[str, str, str]]:
    noun_types = lexicon['noun_types']
    verb_selection = lexicon['verb_selection']
    issues: List[Tuple[str, str, str]] = []
    low = sentence.lower()

    patterns = [
        ('growth of', r'growth of ([a-z][a-z\- ]{0,40})'),
        ('development of', r'development of ([a-z][a-z\- ]{0,40})'),
    ]

    for surface, expr in patterns:
        for match in re.finditer(expr, low):
            phrase = match.group(1).strip()
            head = phrase.split()[-1]
            types = noun_type(head, noun_types)
            if not types:
                continue
            if surface == 'growth of':
                allowed = set(verb_selection['grow']['allows'])
                if not allowed.intersection(types):
                    repair = 'development of ' + phrase
                    issues.append((surface, phrase, repair))
            if surface == 'development of':
                allowed = set(verb_selection['develop']['allows'])
                if not allowed.intersection(types):
                    repair = 'increase in ' + phrase
                    issues.append((surface, phrase, repair))

    for match in re.finditer(r'\b([a-z][a-z\-]+)\s+grows\b', low):
        noun = match.group(1)
        types = noun_type(noun, noun_types)
        if not types:
            continue
        allowed = set(verb_selection['grow']['allows'])
        if not allowed.intersection(types):
            repair = lexicon['default_repairs'].get(noun, 'develops')
            issues.append(('grows', noun, repair))

    return issues


def lint_text(text: str) -> Dict:
    rules = load_json(RULES_PATH)
    lexicon = load_json(LEXICON_PATH)
    sentences = split_sentences(text)

    issues = []
    role_trace: List[Optional[str]] = []

    for idx, sentence in enumerate(sentences, start=1):
        role = classify_role(sentence, rules['role_cues'], rules['order'])
        role_trace.append(role)

        for token in find_forbidden(sentence, rules['banned_patterns']):
            issues.append({'sentence': idx, 'rule': 'forbidden_marker', 'detail': token})

        for expr in find_summary_only(sentence, rules['summary_only_regexes']):
            issues.append({'sentence': idx, 'rule': 'summary_only', 'detail': expr})

        for surface, phrase, repair in check_selection_mismatch(sentence, lexicon):
            issues.append({
                'sentence': idx,
                'rule': 'selection_mismatch',
                'detail': f'{surface} {phrase}',
                'repair': repair,
            })

    present_roles = {r for r in role_trace if r}
    missing_core = [r for r in rules['required_roles'] if r not in present_roles]
    for role in missing_core:
        issues.append({'sentence': None, 'rule': 'missing_core_role', 'detail': role})

    last_index = -1
    order_violations = 0
    for role in role_trace:
        if role is None:
            continue
        current = rules['order'].index(role)
        if current < last_index:
            order_violations += 1
        last_index = max(last_index, current)
    for _ in range(order_violations):
        issues.append({'sentence': None, 'rule': 'role_order_violation', 'detail': 'nonmonotone role sequence'})

    if sentences:
        final_role = role_trace[-1]
        if final_role not in rules['final_roles']:
            issues.append({'sentence': len(sentences), 'rule': 'terminal_load', 'detail': str(final_role)})

    penalties = rules.get('score_weights', {}).get('penalties', {
        'missing_core_role': 20,
        'role_order_violation': 10,
        'summary_only': 8,
        'forbidden_marker': 6,
        'selection_mismatch': 4,
        'terminal_load': 4,
    })
    score = 100
    for issue in issues:
        score -= penalties.get(issue['rule'], 0)
    score = max(score, 0)

    return {
        'sentences': sentences,
        'role_trace': role_trace,
        'issues': issues,
        'score': score,
    }


def format_report(report: Dict) -> str:
    lines: List[str] = []
    lines.append(f"Score: {report['score']}")
    lines.append('Role trace: ' + ' | '.join(r if r else '?' for r in report['role_trace']))
    lines.append('Sentences:')
    for idx, sentence in enumerate(report['sentences'], start=1):
        role = report['role_trace'][idx - 1] or '?'
        lines.append(f'  {idx}. [{role}] {sentence}')
    lines.append('Issues:')
    if not report['issues']:
        lines.append('  none')
    else:
        for issue in report['issues']:
            prefix = f"sentence {issue['sentence']}" if issue['sentence'] is not None else 'global'
            detail = issue.get('detail', '')
            repair = issue.get('repair')
            if repair:
                lines.append(f"  - {prefix}: {issue['rule']} -> {detail}; suggested repair: {repair}")
            else:
                lines.append(f"  - {prefix}: {issue['rule']} -> {detail}")
    return '\n'.join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description='Lint an academic abstract with discourse and ontology checks.')
    parser.add_argument('input_file', help='Path to a plain text file containing the abstract.')
    parser.add_argument('--json', action='store_true', dest='as_json', help='Print machine-readable JSON report.')
    args = parser.parse_args()

    text = Path(args.input_file).read_text(encoding='utf-8')
    report = lint_text(text)
    if args.as_json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(format_report(report))


if __name__ == '__main__':
    main()
