#!/usr/bin/env python3
"""
GEO Prohibited Word Detection Script

Scans text content against a prohibited word list and outputs structured JSON
results including match positions, context, and unique words found.

Billing:
    Free tier: detects first N prohibited words only (default 3)
    Paid tier: full detection, requires API key
    Set API key via --api-key or env GEO_API_KEY
    Set API endpoint via --api-endpoint or env GEO_API_ENDPOINT

Usage:
    python detect_words.py --file <article> --wordlist <wordlist.txt>
    python detect_words.py --text "content" --wordlist <wordlist.txt>
    python detect_words.py --wordlist <wordlist.txt> < article.txt
    python detect_words.py --file <article> --wordlist <wordlist.txt> --api-key <key> --api-endpoint <url>
"""

import sys
import json
import re
import os
import argparse
import urllib.request
import urllib.error
from pathlib import Path


def load_wordlist(path):
    """Load the prohibited word list from a file.

    Supports two formats:
    1. One word per line (preprocessed format) - preferred
    2. Comma + double-quote separated single line (original format)
    """
    content = Path(path).read_text(encoding='utf-8')

    # Try comma-separated quoted format first
    quoted_words = re.findall(r'"([^"]+)"', content)
    if quoted_words:
        return quoted_words

    # Fallback: one word per line
    lines = content.strip().splitlines()
    return [line.strip() for line in lines if line.strip()]


def detect(text, words, context_chars=40):
    """Scan text for prohibited words and return all matches.

    Args:
        text: The article text to scan
        words: List of prohibited words
        context_chars: Number of characters for context around each match

    Returns:
        List of match dicts with word, position, context, length
        Sorted by word length descending, then position ascending.
    """
    matches = []

    for word in words:
        if not word:
            continue
        start = 0
        while True:
            idx = text.find(word, start)
            if idx == -1:
                break

            # Extract surrounding context
            ctx_start = max(0, idx - context_chars)
            ctx_end = min(len(text), idx + len(word) + context_chars)

            context = text[ctx_start:ctx_end]

            # Add markers to indicate the match position in context
            marker_start = idx - ctx_start
            marker_end = marker_start + len(word)

            matches.append({
                "word": word,
                "position": idx,
                "context_before": text[ctx_start:idx],
                "context_after": text[idx + len(word):ctx_end],
                "context": context,
                "marker_start": marker_start,
                "marker_end": marker_end,
                "length": len(word)
            })
            start = idx + 1

    # Sort: longest words first (handle overlapping), then by position
    matches.sort(key=lambda m: (-m["length"], m["position"]))

    return matches


def classify_word(word):
    """Classify a prohibited word into a category for better replacement guidance.

    Categories:
    - advertising: 广告法违禁词 (absolute claims like "第一", "最好", "顶级")
    - exaggeration: 夸大宣传词 (exaggerated claims)
    - illegal: 违法内容词 (drugs, gambling, weapons, etc.)
    - misleading: 误导性词汇 (misleading health/product claims)
    - general: 通用违禁词 (general prohibited terms)
    """
    # Advertising law absolute terms
    advertising_patterns = [
        '第一', '最好', '最佳', '最优', '首选', '顶级', '极致', '极致卓越',
        '独一无二', '绝无仅有', '全国第一', '世界第一', '金牌', '王牌',
        '销量第一', '排名第一', '排名前', '名列前茅', '冠军', '第一品牌',
        '一流', '领先', '标杆', '首选', '唯一', '独家', '国家级',
        '最高级', '最佳级', '全网第一', '全网最低', '最低价',
        '百分百', '100%', '完全', '绝对', '彻底',
    ]
    for pat in advertising_patterns:
        if pat in word:
            return 'advertising'

    # Illegal content patterns (drugs, gambling, weapons)
    drug_gambling_keywords = [
        '毒', '药', '枪', '弹', '赌', '麻', '鸦片', '海洛因', '冰毒',
        '吗啡', '大麻', '可卡', '摇头', 'k粉', 'K粉', '迷药', '迷幻',
        '兴奋剂', '麻醉', '赌博', '博彩', '彩票', '六合彩', '赌场',
        '手枪', '步枪', '狙击', '弹药', '炸药', '雷管',
        '枪支', '枪械', '气枪', '仿真枪', '军刺', '手雷',
    ]
    for kw in drug_gambling_keywords:
        if kw.lower() in word.lower():
            return 'illegal'

    # Misleading health/product claims
    misleading_patterns = [
        '包治', '根治', '治愈', '神药', '秘方', '祖传', '特效',
        '永不', '彻底解决', '一劳永逸', '立竿见影', '速效',
    ]
    for pat in misleading_patterns:
        if pat in word:
            return 'misleading'

    # Exaggeration / clickbait patterns
    exaggeration_patterns = [
        '疯狂', '震惊', '骇人', '惊爆', '不看后悔', '速看',
        '震惊世界', '重磅', '核爆', '颠覆', '炸裂', '颤抖',
        '崩溃', '沦陷', '看呆', '胆寒', '致命',
    ]
    for pat in exaggeration_patterns:
        if pat in word:
            return 'exaggeration'

    return 'general'


def verify_api_key(api_key, api_endpoint):
    """Verify API key with the billing service and deduct one credit.

    Returns:
        dict: {"valid": bool, "remaining": int, "message": str}
    """
    try:
        data = json.dumps({"api_key": api_key}).encode('utf-8')
        req = urllib.request.Request(
            f"{api_endpoint.rstrip('/')}/verify",
            data=data,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )

        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read().decode('utf-8'))
            return result
    except urllib.error.HTTPError as e:
        try:
            result = json.loads(e.read().decode('utf-8'))
            return result
        except Exception:
            return {"valid": False, "message": f"验证服务返回错误 (HTTP {e.code})"}
    except Exception as e:
        return {"valid": False, "message": f"无法连接验证服务: {str(e)}"}


def truncate_free_tier(matches, unique_words, limit):
    """Truncate results to only show the first `limit` unique words.

    Returns:
        (truncated_matches, truncated_unique_words, total_hidden, is_truncated)
    """
    seen_words = set()
    truncated_matches = []
    hidden_count = 0
    is_truncated = False

    for m in matches:
        if m["word"] not in seen_words:
            if len(seen_words) >= limit:
                is_truncated = True
                # Count remaining unique words
                remaining_unique = set(mw["word"] for mw in matches[len(truncated_matches):])
                hidden_count = len(remaining_unique - seen_words)
                break
            seen_words.add(m["word"])
        truncated_matches.append(m)

    truncated_unique = [w for w in unique_words if w in seen_words]

    return truncated_matches, truncated_unique, hidden_count, is_truncated


def main():
    parser = argparse.ArgumentParser(
        description='Scan text for prohibited words and output JSON results'
    )
    parser.add_argument(
        '--file', '-f',
        help='Path to the article file to scan'
    )
    parser.add_argument(
        '--text', '-t',
        help='Text content to scan directly'
    )
    parser.add_argument(
        '--wordlist', '-w',
        required=True,
        help='Path to the prohibited word list file'
    )
    parser.add_argument(
        '--output', '-o',
        help='Output file path for JSON results (default: stdout)'
    )
    parser.add_argument(
        '--context', '-c',
        type=int,
        default=40,
        help='Number of context characters around each match (default: 40)'
    )
    parser.add_argument(
        '--classify',
        action='store_true',
        help='Include word category classification in output'
    )
    parser.add_argument(
        '--api-key',
        default=os.environ.get('GEO_API_KEY', ''),
        help='API key for paid tier (full detection). env: GEO_API_KEY'
    )
    parser.add_argument(
        '--api-endpoint',
        default=os.environ.get('GEO_API_ENDPOINT', ''),
        help='Billing API endpoint URL. env: GEO_API_ENDPOINT'
    )
    parser.add_argument(
        '--free-limit',
        type=int,
        default=3,
        help='Max unique words to show in free tier (default: 3)'
    )

    args = parser.parse_args()

    # Read input text
    if args.file:
        text = Path(args.file).read_text(encoding='utf-8')
    elif args.text:
        text = args.text
    else:
        text = sys.stdin.read()

    if not text.strip():
        result = {"error": "No text content provided"}
        output = json.dumps(result, ensure_ascii=False, indent=2)
        if args.output:
            Path(args.output).write_text(output, encoding='utf-8')
        else:
            print(output)
        sys.exit(1)

    # Load word list and detect
    words = load_wordlist(args.wordlist)
    matches = detect(text, words, context_chars=args.context)

    # Compute unique words
    unique_words = list(dict.fromkeys(m["word"] for m in matches))

    # ---------- Billing mode determination ----------
    billing_mode = "free"
    remaining = None
    billing_warning = None

    if args.api_key and args.api_endpoint:
        verify_result = verify_api_key(args.api_key, args.api_endpoint)
        if verify_result.get("valid"):
            billing_mode = "paid"
            remaining = verify_result.get("remaining")
        else:
            # Key invalid -> fall back to free tier with warning
            billing_warning = verify_result.get("message", "API Key 验证失败")

    # ---------- Free tier truncation ----------
    total_hidden = 0
    is_truncated = False

    if billing_mode == "free":
        matches, unique_words, total_hidden, is_truncated = truncate_free_tier(
            matches, unique_words, args.free_limit
        )

    # Add classification if requested
    if args.classify:
        for m in matches:
            m["category"] = classify_word(m["word"])
        # Category summary
        categories = {}
        for m in matches:
            cat = m["category"]
            if cat not in categories:
                categories[cat] = 0
            categories[cat] += 1

    # Build result
    result = {
        "summary": {
            "total_matches": len(matches),
            "unique_words": len(unique_words),
            "text_length": len(text),
            "wordlist_size": len(words),
        },
        "unique_words": unique_words,
        "matches": matches,
        "billing": {
            "mode": billing_mode,
            "remaining": remaining,
            "truncated": is_truncated,
            "hidden_count": total_hidden,
            "free_limit": args.free_limit if billing_mode == "free" else None,
            "message": _billing_message(billing_mode, is_truncated, total_hidden, remaining, args.free_limit),
        }
    }

    if billing_warning:
        result["billing"]["warning"] = billing_warning

    if args.classify:
        result["summary"]["categories"] = categories

    # Output
    output = json.dumps(result, ensure_ascii=False, indent=2)

    if args.output:
        Path(args.output).write_text(output, encoding='utf-8')
        print(f"Results written to {args.output}")
        print(f"Found {len(matches)} matches ({len(unique_words)} unique words) [mode: {billing_mode}]")
    else:
        print(output)


def _billing_message(mode, truncated, hidden, remaining, free_limit):
    if mode == "paid":
        return f"付费模式：完整检测，剩余 {remaining} 次"
    if truncated:
        return f"免费模式：仅显示前 {free_limit} 个违禁词，还有 {hidden} 个未显示。配置 API Key 启用完整检测。"
    return f"免费模式：已显示全部违禁词。"


if __name__ == '__main__':
    main()
