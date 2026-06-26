#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path


def load_manifest(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def tokenize(text: str):
    text = (text or '').lower()
    text = re.sub(r'[^a-z0-9\u4e00-\u9fff]+', ' ', text)
    return [t for t in text.split() if t]


def score_entry(entry: dict, query_tokens: list[str]):
    title = (entry.get('title') or '').lower()
    tags = [t.lower() for t in (entry.get('tags') or [])]
    preview = (entry.get('body_preview') or '').lower()
    source = (entry.get('source') or '').lower()

    score = 0
    matched = []

    for q in query_tokens:
        if q in title:
            score += 5
            matched.append(f'title:{q}')
        if any(q in tag for tag in tags):
            score += 4
            matched.append(f'tag:{q}')
        if q in preview:
            score += 2
            matched.append(f'preview:{q}')
        if q in source:
            score += 1
            matched.append(f'source:{q}')

    # Bonus for exact phrase in title
    query_phrase = ' '.join(query_tokens)
    if query_phrase and query_phrase in title:
        score += 6
        matched.append('title_phrase')

    return score, matched


def snippet(text: str, query_tokens: list[str], width=220):
    if not text:
        return ''
    lower = text.lower()
    pos = -1
    for q in query_tokens:
        p = lower.find(q)
        if p != -1:
            pos = p
            break
    if pos == -1:
        return text[:width]
    start = max(0, pos - width // 3)
    end = min(len(text), start + width)
    return text[start:end].replace('\n', ' ')


def main():
    parser = argparse.ArgumentParser(description='Search KB manifest/wiki sources with lightweight ranking')
    parser.add_argument('--root', required=True, help='KB root path')
    parser.add_argument('--query', required=True, help='Search query')
    parser.add_argument('--top-k', type=int, default=8)
    parser.add_argument('--include-wiki', action='store_true', help='Also scan wiki/sources markdown content')
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    manifest_path = root / 'manifest.json'
    if not manifest_path.exists():
        raise SystemExit(f'manifest.json not found under {root}')

    manifest = load_manifest(manifest_path)
    entries = manifest.get('entries', [])
    query_tokens = tokenize(args.query)
    if not query_tokens:
        raise SystemExit('query has no valid tokens')

    results = []
    for entry in entries:
        score, matched = score_entry(entry, query_tokens)
        if score <= 0:
            continue

        snip = snippet(entry.get('body_preview') or '', query_tokens)

        wiki_path = root / 'wiki' / 'sources' / f"{entry.get('slug','')}.md"
        wiki_bonus = 0
        if args.include_wiki and wiki_path.exists():
            try:
                content = wiki_path.read_text(encoding='utf-8', errors='replace').lower()
                hit = sum(1 for q in query_tokens if q in content)
                wiki_bonus = min(5, hit)
                score += wiki_bonus
            except Exception:
                pass

        results.append({
            'slug': entry.get('slug'),
            'title': entry.get('title'),
            'source_type': entry.get('source_type'),
            'source': entry.get('source'),
            'score': score,
            'matched': matched,
            'snippet': snip,
            'wiki_path': str(wiki_path.relative_to(root)) if wiki_path.exists() else None,
            'raw_path': entry.get('raw_path'),
            'ingested_at': entry.get('ingested_at'),
            'status': entry.get('status'),
            'wiki_bonus': wiki_bonus,
        })

    results.sort(key=lambda x: (-x['score'], x.get('ingested_at') or ''))
    results = results[:max(1, args.top_k)]

    print(json.dumps({
        'ok': True,
        'query': args.query,
        'root': str(root),
        'total_hits': len(results),
        'results': results,
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
