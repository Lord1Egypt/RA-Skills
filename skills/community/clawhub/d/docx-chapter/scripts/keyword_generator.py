#!/usr/bin/env python3
"""
keyword_generator.py — Orchestrator for claim-driven keyword generation (Stage 2).

Reads chapter.json + research_results.json, maps claims to footnotes,
calls claim_keyword_extractor.py for each footnote, and outputs verification_keywords.json.

Usage:
    python3 keyword_generator.py <chapter.json> <research_results.json> <output.json> [--research-dir <path>]

Inputs:
  chapter.json        — md_content (Markdown body with [^N] footnote markers)
                        and footnotes array [{id, text, url}]
  research_results.json — research data per section, each source has {url, quotes}

Output (verification_keywords.json):
  {
    "footnotes": [
      {
        "id": "2",
        "url": "https://...",
        "claim": "CLSC 的关键特征包括：...",
        "keywords": ["design for recyclability", "re-use and recycling", ...],
        "keyword_sources": {
          "design for recyclability": "claim",
          "re-use and recycling": "research"
        }
      }
    ]
  }

Exit codes:
  0  — Success (some footnotes may lack keywords)
  1  — Fatal error (input files missing/corrupt)
"""

import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

# Subprocess binary path
PYTHON = 'python3'
SCRIPT_DIR = Path(__file__).parent
EXTRACTOR = SCRIPT_DIR / 'claim_keyword_extractor.py'

# Regex for footnote markers in body text
FOOTNOTE_MARKER_RE = re.compile(r'\[\^(\d+)\]')

# Regex for splitting sentences (Chinese + English punctuation)
SENTENCE_SPLIT_RE = re.compile(r'(?<=[。！？.!?])\s*')

# Section header marking footnote definitions
FOOTNOTE_SECTION_RE = re.compile(r'\n##\s*脚注\s*\n')


# ── URL normalisation ─────────────────────────────────────────────────────────


def normalize_url(url: str) -> str:
    """Normalise URL for matching: strip trailing slash, lowercase scheme+host."""
    parsed = urlparse(url)
    path = parsed.path.rstrip('/') or '/'
    return f'{parsed.scheme}://{parsed.netloc}{path}'


# ── research_results.json parsing ─────────────────────────────────────────────


def _extract_sources_from_node(node) -> list[dict]:
    """Recursively find source arrays from an arbitrary research-results node."""
    sources = []
    if isinstance(node, dict):
        if 'url' in node and 'quotes' in node:
            # Leaf source object
            return [node]
        for val in node.values():
            sources.extend(_extract_sources_from_node(val))
    elif isinstance(node, list):
        for item in node:
            sources.extend(_extract_sources_from_node(item))
    return sources


def build_url_to_quotes(research_data) -> dict[str, dict]:
    """Flatten research data into {normalised_url: {url, quotes: [str]}}.

    Handles both section-dict and flat-array formats.
    """
    # Collect all source objects
    all_sources = _extract_sources_from_node(research_data)

    url_map: dict[str, dict] = {}
    for src in all_sources:
        url = (src.get('url') or '').strip()
        if not url:
            continue

        quotes = src.get('quotes')
        if not quotes or not isinstance(quotes, list):
            # Fall back to other text fields
            fallback = (
                src.get('excerpt') or src.get('snippet')
                or src.get('summary') or ''
            )
            if fallback:
                quotes = [fallback]
        if not quotes:
            continue

        norm = normalize_url(url)
        # Merge quotes if same URL appears under multiple topics
        if norm not in url_map:
            url_map[norm] = {'url': url, 'quotes': []}
        url_map[norm]['quotes'].extend(quotes)

    return url_map


def find_quote_for_url(url: str, url_quotes: dict[str, dict]) -> str:
    """Return concatenated quotes for *url*, or empty string."""
    norm = normalize_url(url)
    entry = url_quotes.get(norm)
    if entry:
        return ' '.join(entry['quotes'])
    # Lenient: strip www differences
    for key, val in url_quotes.items():
        if key.rstrip('/') == norm.rstrip('/'):
            return ' '.join(val['quotes'])
    return ''


# ── Claim extraction from md_content ─────────────────────────────────────────


def split_footnotes_section(md: str) -> str:
    """Return only the body (before 脚注 definitions)."""
    parts = FOOTNOTE_SECTION_RE.split(md, maxsplit=1)
    return parts[0]


def extract_all_footnote_claims(body: str) -> dict[str, str]:
    """Return {footnote_id: surrounding_sentence} for every [^N] in *body*."""
    results: dict[str, str] = {}
    sentences = SENTENCE_SPLIT_RE.split(body)
    for sent in sentences:
        sent = sent.strip()
        if not sent:
            continue
        markers = FOOTNOTE_MARKER_RE.findall(sent)
        for fn_id in markers:
            if fn_id not in results:
                results[fn_id] = sent
    return results


# ── Main pipeline ─────────────────────────────────────────────────────────────


def main() -> None:
    if len(sys.argv) < 4:
        print(
            'Usage: keyword_generator.py <chapter.json> <research_results.json> '
            '<output.json> [--research-dir <path>]',
            file=sys.stderr,
        )
        sys.exit(1)

    chapter_path = Path(sys.argv[1])
    research_path = Path(sys.argv[2])
    output_path = Path(sys.argv[3])

    # Optional --research-dir flag
    if '--research-dir' in sys.argv:
        idx = sys.argv.index('--research-dir')
        if idx + 1 < len(sys.argv):
            _research_dir = Path(sys.argv[idx + 1])  # noqa: F841

    # ── Validate inputs ───────────────────────────────────────────────────────
    if not chapter_path.exists():
        print(f'Error: chapter.json not found at {chapter_path}', file=sys.stderr)
        sys.exit(1)
    if not research_path.exists():
        print(f'Error: research_results.json not found at {research_path}', file=sys.stderr)
        sys.exit(1)

    with open(chapter_path, 'r', encoding='utf-8') as f:
        chapter = json.load(f)
    with open(research_path, 'r', encoding='utf-8') as f:
        research = json.load(f)

    footnotes = chapter.get('footnotes', [])
    md_content = chapter.get('md_content', '')

    if not footnotes:
        print('Error: chapter.json has no footnotes array', file=sys.stderr)
        sys.exit(1)
    if not md_content:
        print('Error: chapter.json has no md_content', file=sys.stderr)
        sys.exit(1)

    # ── Build lookup maps ─────────────────────────────────────────────────────
    url_quotes = build_url_to_quotes(research)
    body = split_footnotes_section(md_content)
    footnote_claims = extract_all_footnote_claims(body)

    print(f'Found {len(footnotes)} footnotes in chapter.json', file=sys.stderr)
    print(f'Found {len(url_quotes)} unique URLs in research_results.json', file=sys.stderr)
    print(f'Found claims for {len(footnote_claims)} footnote markers', file=sys.stderr)

    # ── Process each footnote ─────────────────────────────────────────────────
    output_footnotes: list[dict] = []
    extractor_errors = 0

    for fn in footnotes:
        fn_id = str(fn.get('id', ''))
        fn_url = fn.get('url', '')

        claim = footnote_claims.get(fn_id, '')
        if not claim:
            print(f'  [^{fn_id}] No claim sentence found in body', file=sys.stderr)

        research_quote = find_quote_for_url(fn_url, url_quotes) if fn_url else ''
        if not research_quote:
            print(f'  [^{fn_id}] No research quote found for {fn_url or "(empty url)"}',
                  file=sys.stderr)

        if not claim or not research_quote:
            # Cannot generate keywords without both inputs
            output_footnotes.append({
                'id': fn_id,
                'url': fn_url,
                'claim': claim,
                'keywords': [],
                'keyword_sources': {},
            })
            continue

        # ── Call claim_keyword_extractor.py ───────────────────────────────────
        try:
            proc = subprocess.run(
                [PYTHON, str(EXTRACTOR), claim, research_quote],
                capture_output=True, text=True, timeout=90,
            )
            if proc.returncode != 0:
                print(f'  [^{fn_id}] Extractor failed (exit {proc.returncode}): '
                      f'{proc.stderr.strip()}', file=sys.stderr)
                extractor_errors += 1
                keywords: list[str] = []
                keyword_sources: dict[str, str] = {}
            else:
                kw_list = json.loads(proc.stdout)
                keywords = [
                    kw['text'] for kw in kw_list
                    if isinstance(kw, dict) and kw.get('text')
                ]
                keyword_sources = {
                    kw['text']: kw['source'] for kw in kw_list
                    if isinstance(kw, dict) and kw.get('text') and kw.get('source')
                }
        except subprocess.TimeoutExpired:
            print(f'  [^{fn_id}] Extractor timed out after 90s', file=sys.stderr)
            extractor_errors += 1
            keywords, keyword_sources = [], {}
        except json.JSONDecodeError as e:
            print(f'  [^{fn_id}] Extractor returned invalid JSON: {e}',
                  file=sys.stderr)
            extractor_errors += 1
            keywords, keyword_sources = [], {}
        except Exception as e:
            print(f'  [^{fn_id}] Extractor error: {e}', file=sys.stderr)
            extractor_errors += 1
            keywords, keyword_sources = [], {}

        output_footnotes.append({
            'id': fn_id,
            'url': fn_url,
            'claim': claim,
            'keywords': keywords,
            'keyword_sources': keyword_sources,
        })

    # ── Write output ──────────────────────────────────────────────────────────
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({'footnotes': output_footnotes}, f, ensure_ascii=False, indent=2)

    total = len(output_footnotes)
    with_kw = sum(1 for f in output_footnotes if f['keywords'])
    print(f'\nOutput written to {output_path}', file=sys.stderr)
    print(f'  Total footnotes:  {total}', file=sys.stderr)
    print(f'  With keywords:    {with_kw}', file=sys.stderr)
    print(f'  Without keywords: {total - with_kw}', file=sys.stderr)
    if extractor_errors:
        print(f'  Extractor errors: {extractor_errors}', file=sys.stderr)


if __name__ == '__main__':
    main()
