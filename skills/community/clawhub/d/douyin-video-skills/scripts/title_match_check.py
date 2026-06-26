#!/usr/bin/env python3
import argparse
import json
import re
import sys
from difflib import SequenceMatcher


PUNCT_RE = re.compile(r'[\-—_~·•|,，。！？!?:：;；()（）\[\]【】"“”‘’`…]')


def normalize_title(text: str) -> str:
    text = text.strip()
    text = re.sub(r'[#＃].*$', '', text)  # drop trailing hashtags
    text = PUNCT_RE.sub('', text)
    text = re.sub(r'\s+', '', text)
    return text.lower()


def title_similarity(expected: str, actual: str) -> float:
    return SequenceMatcher(None, expected, actual).ratio()


def is_match(expected: str, actual: str, mode: str, min_similarity: float) -> tuple[bool, str, float]:
    expected_n = normalize_title(expected)
    actual_n = normalize_title(actual)
    similarity = title_similarity(expected_n, actual_n)

    if expected_n == actual_n:
        return True, 'exact-match', similarity
    if expected_n and actual_n and (expected_n in actual_n or actual_n in expected_n):
        return True, 'contain-match', similarity

    threshold = min_similarity
    if mode == 'loose':
        threshold = min(min_similarity, 0.72)
    elif mode == 'strict':
        threshold = max(min_similarity, 0.9)

    if similarity >= threshold:
        return True, 'similarity-match', similarity
    return False, 'title-mismatch', similarity


def main():
    parser = argparse.ArgumentParser(description='校验当前弹层标题是否与目标搜索结果标题一致')
    parser.add_argument('--expected', required=True, help='目标搜索结果标题')
    parser.add_argument('--actual', required=True, help='当前弹层标题')
    parser.add_argument('--mode', choices=['strict', 'default', 'loose'], default='default', help='匹配模式')
    parser.add_argument('--min-similarity', type=float, default=0.82, help='最小标题相似度阈值，默认 0.82')
    args = parser.parse_args()

    matched, reason, similarity = is_match(args.expected, args.actual, args.mode, args.min_similarity)
    expected_n = normalize_title(args.expected)
    actual_n = normalize_title(args.actual)

    result = {
        'matched': matched,
        'expected': args.expected,
        'actual': args.actual,
        'expected_normalized': expected_n,
        'actual_normalized': actual_n,
        'mode': args.mode,
        'similarity': round(similarity, 4),
        'min_similarity': args.min_similarity,
        'reason': reason,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not matched:
        sys.exit(2)


if __name__ == '__main__':
    main()
