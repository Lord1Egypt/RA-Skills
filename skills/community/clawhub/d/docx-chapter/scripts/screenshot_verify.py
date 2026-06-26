#!/usr/bin/env python3
"""
Screenshot verification for docx-chapter pipeline.
Reads chapter JSON + research results, extracts keywords from source excerpts,
skips broken URLs, runs purple highlight screenshots for each URL.

Usage:
    python3 screenshot_verify.py <chapter.json> <output_dir> [--research <path>] [--url-status <path>]

Expects chapter.json to have:
  - footnotes: [{ id, text, url }]
  - md_content: "..."

Optional:
  --research: research_results.json from Phase 2 (URL→excerpt mapping for keywords)
  --url-status: url_status.json from Phase 5b (curl results for broken URL detection)

Outputs:
  - output_dir/screenshots/fn<N>_<domain>.png
  - output_dir/screenshots/summary.json
"""

import sys
import os
import json
import re
import signal
import subprocess
import argparse
from pathlib import Path
from urllib.parse import urlparse


SCRIPT_DIR = Path(__file__).parent
PURPLE_SCRIPT = SCRIPT_DIR / "purple_highlight_screenshot.py"
PLAYWRIGHT_PYTHON = "python3"

# Stop words for keyword extraction
STOP_WORDS = {
    'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
    'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
    'should', 'may', 'might', 'can', 'shall', 'to', 'of', 'in', 'for',
    'on', 'with', 'at', 'by', 'from', 'as', 'into', 'through', 'during',
    'before', 'after', 'above', 'below', 'between', 'out', 'off', 'over',
    'under', 'again', 'further', 'then', 'once', 'and', 'but', 'or', 'nor',
    'not', 'so', 'very', 'just', 'than', 'too', 'also', 'about', 'up',
    'its', 'it', 'this', 'that', 'these', 'those', 'they', 'them', 'their',
    'he', 'she', 'his', 'her', 'him', 'who', 'which', 'what', 'where',
    'when', 'how', 'all', 'each', 'every', 'both', 'few', 'more', 'most',
    'other', 'some', 'such', 'no', 'only', 'own', 'same', 'that', 'there',
    'here', 'been', 'would', 'could', 'should', 'may', 'might', 'must',
    'also', 'into', 'been', 'have', 'has', 'had', 'did', 'does', 'doing',
    'used', 'using', 'use', 'one', 'two', 'three', 'new', 'first', 'last',
    'long', 'great', 'little', 'own', 'old', 'right', 'big', 'high',
    'different', 'small', 'large', 'next', 'early', 'young', 'important',
    'few', 'public', 'bad', 'same', 'able',
}


def build_url_to_excerpt(research_results: list) -> dict:
    """Flatten research results into URL→excerpt mapping.

    research_results is an array of { topic, sources: [{url, title, excerpt, ...}], ... }
    Returns dict mapping URL → { title, excerpt, topic }
    """
    url_map = {}
    for result in research_results:
        topic = result.get("topic", "")
        sources = result.get("sources", [])
        for src in sources:
            url = src.get("url", "")
            if url:
                url_map[url] = {
                    "title": src.get("title", ""),
                    "excerpt": src.get("excerpt", "") or src.get("snippet", "") or src.get("summary", ""),
                    "topic": topic,
                }
    return url_map


def load_broken_urls(url_status_data: list, footnotes: list) -> set:
    """Determine which URLs are broken from curl results.

    url_status_data is an array of curl output strings (one per footnote, same order).
    Returns set of broken URLs.
    """
    broken = set()
    for i, fn in enumerate(footnotes):
        url = fn.get("url", "")
        if not url:
            continue
        if i < len(url_status_data):
            curl_output = str(url_status_data[i]).strip()
            # Parse HTTP status from curl output
            # Looks like "HTTP/2 200" or "HTTP/1.1 404 Not Found"
            match = re.search(r'HTTP/[\d.]+\s+(\d+)', curl_output)
            if match:
                status_code = int(match.group(1))
                if status_code >= 400:
                    broken.add(url)
            elif not curl_output:
                # Empty output = connection failure/timeout
                broken.add(url)
            # Redirects (3xx) are OK since curl -L follows them
    return broken


# Preposition words - phrases containing these tend to be abstract descriptions,
# not concrete searchable terms.
PREPOSITIONS = {'of', 'for', 'to', 'in', 'and', 'with', 'from', 'that', 'this',
                'into', 'through', 'during', 'before', 'after', 'between'}

# Well-known technical domains - boost phrases containing these words
DOMAIN_WORDS = {
    'testing', 'software', 'release', 'development', 'deployment', 'product',
    'alpha', 'beta', 'user', 'acceptance', 'integration', 'performance',
    'security', 'design', 'system', 'quality', 'analysis', 'data', 'code',
    'test', 'life', 'cycle', 'management', 'process', 'requirements',
    'validation', 'verification', 'automation', 'continuous', 'delivery',
    'agile', 'scrum', 'devops', 'feedback', 'iteration', 'pipeline',
}


def _is_concrete(keyword: str) -> bool:
    """Check if a keyword is a concrete searchable term (vs abstract description)."""
    kw_words = keyword.lower().split()
    words = set(kw_words)
    # Reject if contains prepositions (abstract: "adherence to product requirements")
    if words & PREPOSITIONS:
        return False
    # Reject common English filler that snuck through
    common_filler = {'generally', 'include', 'completed', 'critical', 'catch',
                     'entry', 'exit', 'criteria', 'required', 'needs', 'need',
                     'functions', 'understanding', 'differences'}
    if words.issubset(common_filler):
        return False
    # Multi-word: require >= half content words to be domain-relevant
    domain_count = len(words & DOMAIN_WORDS)
    if len(kw_words) >= 3 and domain_count < len(kw_words) / 2:
        return False
    # Accept if contains domain words or is capitalized
    if words & DOMAIN_WORDS:
        return True
    if keyword[0].isupper():
        return True
    # Single domain word
    return len(kw_words) == 1 and (domain_count > 0 or len(keyword) > 5)


def _needs_llm_fallback(keywords: list[str]) -> bool:
    """Check if regex-extracted keywords are poor quality and need LLM fallback."""
    if len(keywords) < 2:
        return True
    concrete_count = sum(1 for kw in keywords if _is_concrete(kw))
    # Require ALL keywords to be concrete; otherwise fall back to LLM
    return concrete_count < len(keywords)


def extract_keywords_with_llm(excerpt: str, title: str = "") -> list[str]:
    """Extract keywords using LLM when regex yields poor results.

    Calls openclaw infer model run with a targeted prompt.
    Returns list of keyword strings.
    """
    text_sample = excerpt[:600]  # Avoid huge prompts
    prompt = (
        'Extract 3-5 short, concrete terms (1-2 words each) that are MOST LIKELY '
        'to appear VERBATIM on the target web page described below. '
        'CRITICAL RULES:\n'
        '1. PREFER 1-2 word generic domain terms (e.g. "beta testing", "QA", "usability").\n'
        '2. NEVER copy multi-word descriptive phrases from the excerpt '
        '   (e.g. do NOT output "recruit external testers" or "uncontrolled environments").\n'
        '3. Split concepts into individual short keywords.\n'
        '4. Think: what words would a glossary/definition page ACTUALLY contain?\n'
        'Return ONLY a JSON array of strings, nothing else.\n\n'
        f'Title: {title}\n'
        f'Excerpt: {text_sample}'
    )

    try:
        proc = subprocess.run(
            ['openclaw', 'infer', 'model', 'run', '--prompt', prompt, '--json'],
            capture_output=True, text=True, timeout=30
        )
        if proc.returncode == 0:
            result = json.loads(proc.stdout)
            outputs = result.get('outputs', [])
            if outputs:
                text = outputs[0].get('text', '')
                # Strip markdown fences if present
                text = re.sub(r'^```(?:json)?\s*\n?', '', text.strip())
                text = re.sub(r'\n?```\s*$', '', text)
                keywords = json.loads(text)
                if isinstance(keywords, list):
                    return [str(k) for k in keywords[:5]]
    except Exception:
        pass

    return []


def extract_keywords_from_excerpt(excerpt: str, title: str = "", use_llm: bool = True) -> list[str]:
    """Extract meaningful keywords from source excerpt text.

    Strategy:
    1. Extract capitalized phrases (proper nouns, technical terms)
    2. Extract hyphenated compound terms
    3. Extract ALL CAPS acronyms
    4. Extract domain-specific noun phrases (avoiding abstract prepositional chains)
    5. [LLM fallback] If regex results are poor, call LLM for better keywords
    """
    if not excerpt and not title:
        return []

    text = f"{title} {excerpt}".strip()
    candidates = []

    # 1. Extract capitalized phrases (proper nouns, product names, technical concepts)
    cap_phrases = re.findall(r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,3})\b', text)
    for phrase in cap_phrases:
        words = phrase.split()
        if not all(w.lower() in STOP_WORDS for w in words):
            candidates.append(phrase)

    # 2. Extract hyphenated compound terms (e.g., "top-down", "real-world")
    hyphenated = re.findall(r'\b([a-zA-Z]+-[a-zA-Z]+(?:-[a-zA-Z]+)*)\b', text)
    for term in hyphenated:
        if len(term) > 4:
            candidates.append(term)

    # 3. Extract ALL CAPS terms (acronyms, abbreviations)
    acronyms = re.findall(r'\b([A-Z]{2,})\b', text)
    for acr in acronyms:
        if acr not in ('HTTP', 'HTTPS', 'URL', 'HTML', 'CSS', 'API', 'PDF'):
            candidates.append(acr)

    # 4. Extract 2-3 word lowercase domain phrases WITHOUT prepositions
    #    Avoids abstract prepositional chains like "adherence to product requirements"
    domain_phrases = re.findall(
        r'\b([a-z]{3,}(?:\s+[a-z]{3,}){1,2})\b',
        text.lower()
    )
    for phrase in domain_phrases:
        words = set(phrase.split())
        # Skip if contains prepositions (abstract) or too many stop words
        if words & PREPOSITIONS:
            continue
        content_words = [w for w in phrase.split() if w not in STOP_WORDS]
        if len(content_words) >= 1:
            candidates.append(phrase)

    # Deduplicate and score (prefer concrete terms)
    seen = set()
    scored = []
    for kw in candidates:
        low = kw.lower().strip()
        if low in seen or len(low) < 3:
            continue
        seen.add(low)

        score = len(kw)
        if re.match(r'^[A-Z]', kw):
            score += 5  # Capitalized bonus
        if '-' in kw:
            score += 3  # Hyphenated bonus
        if len(kw.split()) >= 2:
            score += 2  # Multi-word bonus
        # Boost domain-relevant terms
        if set(kw.lower().split()) & DOMAIN_WORDS:
            score += 4  # Domain bonus
        # Penalize abstract prepositional phrases
        if set(kw.lower().split()) & PREPOSITIONS:
            score -= 6  # Preposition penalty

        scored.append((score, kw))

    scored.sort(key=lambda x: -x[0])
    result = [kw for _, kw in scored[:3]]

    # LLM fallback: if regex results are poor, use LLM
    if use_llm and _needs_llm_fallback(result):
        llm_keywords = extract_keywords_with_llm(excerpt, title)
        if llm_keywords:
            return llm_keywords[:3]

    return result


def enrich_keywords_with_llm(keywords: list[str], excerpt: str = "", title: str = "", body_context: str = "") -> list[str]:
    """Use LLM to generate semantically equivalent keyword variants.

    For each keyword, generates 2-3 variants (synonyms, rewordings, different formats)
    that are more likely to appear verbatim on a target web page.
    If body_context is provided, uses the chapter sentence citing this source
    to guide keyword generation toward specific supporting content.
    Returns original keywords + variants combined (deduplicated, max 10).
    """
    if not keywords:
        return keywords

    source_context = f"{title} {excerpt}".strip()[:400]

    if body_context:
        # Body-context mode: generate specific keywords from chapter claims,
        # not generic variants of the input keywords.
        prompt = (
            f'Source: {source_context}\n\n'
            f'Chapter context (the sentence citing this source): {body_context}\n\n'
            'TASK: Extract 8-12 SPECIFIC phrases from the CHAPTER CONTEXT '
            'that would appear verbatim or nearly-verbatim on the target web page.\n\n'
            'RULES:\n'
            '1. Read the chapter context carefully - it makes specific claims about this source\n'
            '2. Pull out the key nouns, concepts, and domain phrases from those claims\n'
            '3. Return 2-4 word English phrases that are DISTINCTIVE on the page\n'
            '4. Translate any Chinese concepts to their most common English equivalents\n'
            '5. If the source is cited for a specific definition or concept, include that phrase\n\n'
            'DO NOT include generic single words like "alpha", "testing", or "definition".\n'
            'Focus on phrases that someone would Ctrl+F to find the relevant section.\n\n'
        )
    else:
        # Variant mode: generate semantic equivalents of existing keywords
        prompt = (
            'For each keyword below, generate 2-3 semantically equivalent phrases '
            'that could appear VERBATIM on a web page. Think about:\n'
            '1. Synonyms (e.g. "improved" → "enhanced", "boosted", "increased")\n'
            '2. Different word orders (e.g. "pass rate 95%" → "95% pass rate")\n'
            '3. Common rewordings that web pages actually use\n'
            '4. If keyword is in one language, also consider the other language equivalent\n'
            '5. Numeric variants (e.g. "50%" → "50 percent")\n\n'
            f'Source description: {source_context}\n\n'
        )

    prompt += (
        f'Keywords: {json.dumps(keywords)}\n\n'
        'Return ONLY a JSON array of all keywords+variants combined (no duplicates), nothing else.'
    )

    try:
        proc = subprocess.Popen(
            ['openclaw', 'infer', 'model', 'run', '--prompt', prompt, '--json'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            start_new_session=True
        )
        try:
            stdout, stderr = proc.communicate(timeout=120)
            if proc.returncode == 0:
                result = json.loads(stdout)
                outputs = result.get('outputs', [])
                if outputs:
                    text = outputs[0].get('text', '')
                    text = re.sub(r'^```(?:json)?\s*\n?', '', text.strip())
                    text = re.sub(r'\n?```\s*$', '', text)
                    variants = json.loads(text)
                    if isinstance(variants, list) and len(variants) > 0:
                        if body_context:
                            # When body context is available: LLM output takes priority.
                            # Place originals AFTER LLM results so specific keywords come first.
                            all_kw = list(dict.fromkeys(
                                [str(v) for v in variants] +
                                [str(k) for k in keywords]
                            ))
                            return all_kw[:15]
                        else:
                            # No body context: originals first, variants appended
                            all_kw = list(dict.fromkeys(
                                [str(k) for k in keywords] +
                                [str(v) for v in variants if str(v) not in set(str(k) for k in keywords)]
                            ))
                            return all_kw[:10]
        except subprocess.TimeoutExpired:
            print(f"  [LLM timeout for {title[:40]}...]", file=sys.stderr)
            pgid = os.getpgid(proc.pid)
            os.killpg(pgid, signal.SIGKILL)
            proc.wait()
    except Exception:
        pass

    return keywords


def extract_keywords_from_footnote(footnote_text: str) -> list[str]:
    """Fallback: extract keywords from footnote text (legacy behavior)."""
    keywords = []

    # Try to extract title from footnote
    title_match = re.search(r'[""\"](.*?)[""\"]|《(.*?)》', footnote_text)
    if title_match:
        title = title_match.group(1) or title_match.group(2)
        words = re.findall(r'[a-zA-Z]+', title)
        meaningful = [w for w in words if w.lower() not in STOP_WORDS and len(w) > 2]
        keywords.extend(meaningful[:3])

    if not keywords:
        author_match = re.match(r'^([^.]+)\.', footnote_text)
        if author_match:
            author = author_match.group(1).strip()
            words = re.findall(r'[a-zA-Z]+', author)
            meaningful = [w for w in words if len(w) > 2]
            keywords.extend(meaningful[:2])

    if not keywords:
        words = re.findall(r'[a-zA-Z]{3,}', footnote_text)
        keywords = words[:3]

    # Deduplicate
    seen = set()
    result = []
    for kw in keywords:
        low = kw.lower()
        if low not in seen:
            seen.add(low)
            result.append(kw)

    return result[:3]


def extract_domain(url: str) -> str:
    """Extract a clean domain name for filename."""
    match = re.search(r'https?://(?:www\.)?([^/]+)', url)
    if match:
        domain = match.group(1)
        domain = re.sub(r'[^a-zA-Z0-9]', '_', domain)
        return domain[:30]
    return "unknown"


def extract_footnote_body_contexts(md_content: str) -> dict:
    """Extract body sentence context for each footnote marker from chapter.md.

    Parses chapter markdown to find sentences containing [^N] markers
    (before the footnote definitions section), returns mapping of
    footnote_id (str) -> body sentence text (without [^N] markers).
    """
    contexts = {}
    if not md_content:
        return contexts

    # Split off the footnote definitions section (## 脚注)
    parts = re.split(r'\n##\s*脚注\s*\n', md_content, maxsplit=1)
    body = parts[0]

    # Split body into sentences (Chinese + English sentence boundaries)
    sentences = re.split(r'(?<=[。！？])\s*', body)

    for sent in sentences:
        markers = re.findall(r'\[\^(\d+)\]', sent)
        if markers:
            clean = sent.replace('\n', ' ').strip()
            # Strip leading [^N] markers for cleaner context
            clean = re.sub(r'(?:\[\^\d+\]\s*)+', '', clean).strip()
            for m in markers:
                if m not in contexts:
                    contexts[m] = clean

    return contexts


def calculate_grade(status: str, highlighted_count: int, body_text_length: int) -> str:
    """Assign a quality grade to a screenshot result.

    Grades:
      A = screenshot OK, highlighted_count > 0, body text >= 100 chars
      B = screenshot OK, highlighted_count == 0, body text >= 100 chars
      C = screenshot OK, body text < 100 chars (page loaded but empty/near-empty)
      F = screenshot failed (error/timeout)
      N/A = skipped (no URL, PDF source, broken URL, etc.)
    """
    if status in ("error", "timeout"):
        return "F"
    if status == "skipped":
        return "N/A"
    # status == "ok"
    if highlighted_count > 0 and body_text_length >= 100:
        return "A"
    if body_text_length < 100:
        return "C"
    # highlighted_count == 0 with sufficient body text
    return "B"


def check_claim_alignment(body_text: str, claims_for_fn: list) -> list[dict]:
    """Search page body text for claim text keywords.

    For each claim associated with this footnote, search the extracted page
    body text for evidence that the claim's content appears on the source page.

    Returns list of { claim_id, matched_text, match_type }
    where match_type is one of: "exact", "paraphrase", "not_found".
    """
    if not body_text or not claims_for_fn:
        return []

    body_lower = body_text.lower()
    alignments = []

    for claim in claims_for_fn:
        claim_text = claim.get("text", "")
        claim_id = claim.get("claim_id", "")
        if not claim_text:
            continue

        # 1) Full claim text verbatim on page
        if claim_text.lower() in body_lower:
            alignments.append({
                "claim_id": claim_id,
                "matched_text": claim_text[:200],
                "match_type": "exact",
            })
            continue

        # 2) Extract key phrases for approximate matching
        eng_words = re.findall(r'[a-zA-Z]+', claim_text)
        meaningful_eng = [w for w in eng_words if w.lower() not in STOP_WORDS and len(w) > 2]
        chn_phrases = re.findall(r'[一-鿿]{2,}', claim_text)

        # Try 2-word English phrases
        found_phrase = ""
        for i in range(len(meaningful_eng) - 1):
            phrase = f"{meaningful_eng[i]} {meaningful_eng[i + 1]}"
            if phrase.lower() in body_lower:
                found_phrase = phrase
                break

        if found_phrase:
            alignments.append({
                "claim_id": claim_id,
                "matched_text": found_phrase[:200],
                "match_type": "paraphrase",
            })
            continue

        # Try Chinese phrases
        for phrase in chn_phrases:
            if phrase in body_text:
                alignments.append({
                    "claim_id": claim_id,
                    "matched_text": phrase[:200],
                    "match_type": "paraphrase",
                })
                found_phrase = phrase
                break

        if found_phrase:
            continue

        # 3) Fall back to individual keywords
        matched_kw = ""
        for w in meaningful_eng:
            if w.lower() in body_lower:
                matched_kw = w
                break
        if not matched_kw:
            for phrase in chn_phrases:
                if phrase in body_text:
                    matched_kw = phrase
                    break

        if matched_kw:
            alignments.append({
                "claim_id": claim_id,
                "matched_text": matched_kw[:200],
                "match_type": "paraphrase",
            })
        else:
            alignments.append({
                "claim_id": claim_id,
                "matched_text": "",
                "match_type": "not_found",
            })

    return alignments


def load_claim_keywords(keywords_file_path: str) -> dict:
    """Load verification_keywords.json and build fn_id → keywords mapping.

    Returns dict of fn_id (str) → list of keyword strings.
    Only includes entries that have both an id and keywords.
    """
    with open(keywords_file_path) as f:
        data = json.load(f)
    fn_keywords = {}
    for entry in data.get("footnotes", []):
        fn_id = str(entry.get("id", ""))
        if fn_id:
            keywords = entry.get("keywords", [])
            if keywords:
                fn_keywords[fn_id] = keywords
    return fn_keywords


def main():
    parser = argparse.ArgumentParser(description="Screenshot verification for docx-chapter pipeline")
    parser.add_argument("chapter_json", help="Path to chapter.json")
    parser.add_argument("output_dir", help="Output directory")
    parser.add_argument("--research", help="Path to research_results.json from Phase 2")
    parser.add_argument("--url-status", help="Path to url_status.json from Phase 5b")
    parser.add_argument("--keywords-file", help="Path to verification_keywords.json for claim-driven keywords")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)

    # Load chapter data
    with open(args.chapter_json) as f:
        chapter = json.load(f)

    footnotes = chapter.get("footnotes", [])
    md_content = chapter.get("md_content", "")

    # Load Pass 1 claims for claim-alignment detection
    pass1 = chapter.get("pass1_extraction", {})
    claims = pass1.get("claims", [])
    # Build footnote_id → claims mapping
    fn_id_to_claims: dict[str, list] = {}
    for c in claims:
        for fid in c.get("footnote_ids", []):
            fn_id_to_claims.setdefault(str(fid), []).append(c)

    # Extract footnote body contexts from chapter markdown
    body_contexts = extract_footnote_body_contexts(md_content)

    if not footnotes:
        print(json.dumps({"ok": True, "message": "No footnotes found", "screenshots": []}))
        return

    # Load research results (URL→excerpt mapping)
    url_to_source = {}
    if args.research and os.path.exists(args.research):
        with open(args.research) as f:
            research_data = json.load(f)
        # Handle both dict (with 'topics' key) and list formats
        if isinstance(research_data, dict) and 'topics' in research_data:
            research_data = research_data['topics']
        url_to_source = build_url_to_excerpt(research_data)

    # Load URL status (broken URL detection)
    broken_urls = set()
    if args.url_status and os.path.exists(args.url_status):
        with open(args.url_status) as f:
            url_status_data = json.load(f)
        broken_urls = load_broken_urls(url_status_data, footnotes)

    # Load claim-driven keywords from verification_keywords.json if provided
    fn_id_to_claim_keywords = {}
    if args.keywords_file and os.path.exists(args.keywords_file):
        fn_id_to_claim_keywords = load_claim_keywords(args.keywords_file)

    # Create screenshots directory
    screenshots_dir = output_dir / "screenshots"
    screenshots_dir.mkdir(parents=True, exist_ok=True)

    results = []
    for fn in footnotes:
        fn_id = fn.get("id", "?")
        fn_text = fn.get("text", "")
        fn_url = fn.get("url", "")

        print(f"[{fn_id}] Processing: {fn_url[:80]}...", file=sys.stderr, flush=True)

        if not fn_url:
            results.append({"id": fn_id, "status": "skipped", "reason": "no URL", "grade": "N/A", "claim_alignments": []})
            continue

        # Check if PDF
        if fn_url.lower().endswith(".pdf"):
            results.append({"id": fn_id, "status": "skipped", "reason": "PDF source", "url": fn_url, "grade": "N/A", "claim_alignments": []})
            continue

        # Check if URL is broken (from url_check)
        if fn_url in broken_urls:
            results.append({"id": fn_id, "status": "skipped", "reason": "URL unreachable (404/timeout)", "url": fn_url, "grade": "N/A", "claim_alignments": []})
            continue

        # Check for claim-driven keywords from verification_keywords.json
        claim_keywords = fn_id_to_claim_keywords.get(str(fn_id))

        if claim_keywords:
            keywords = claim_keywords
            keyword_source = "claim_keywords"
        else:
            # Extract keywords: prefer source excerpt, fall back to footnote text
            # Try exact match first, then fuzzy prefix match
            source_info = url_to_source.get(fn_url)
            if source_info is None:
                # Find the longest key that is a prefix of fn_url
                best_match = None
                best_len = 0
                for key in url_to_source:
                    if fn_url.startswith(key) and len(key) > best_len:
                        best_match = key
                        best_len = len(key)
                if best_match:
                    source_info = url_to_source[best_match]
                else:
                    source_info = {}
            excerpt = source_info.get("excerpt", "")
            title = source_info.get("title", "")

            if excerpt:
                keywords = extract_keywords_from_excerpt(excerpt, title)
                keyword_source = "excerpt"
            else:
                keywords = extract_keywords_from_footnote(fn_text)
                keyword_source = "footnote_fallback"

            if not keywords:
                keywords = ["test"]
                keyword_source = "fallback"

            # Step 1: Enrich keywords with LLM using body context from chapter
            body_ctx = body_contexts.get(str(fn_id), "")
            has_meaningful_kw = len(keywords) > 0 and keywords != ["test"]
            has_context = bool(excerpt or body_ctx)

            if has_meaningful_kw and has_context:
                enriched = enrich_keywords_with_llm(keywords, excerpt, title, body_ctx)
                if len(enriched) > len(keywords):
                    keywords = enriched
                    if excerpt:
                        keyword_source = "excerpt+llm_variants"
                    else:
                        keyword_source = "footnote+body_llm_variants"

        # Generate output filename
        domain = extract_domain(fn_url)
        output_file = screenshots_dir / f"fn{fn_id}_{domain}.png"

        # Run purple highlight script
        try:
            if claim_keywords:
                cmd = [PLAYWRIGHT_PYTHON, str(PURPLE_SCRIPT), fn_url, str(output_file), '--smart', '--keywords-file', args.keywords_file]
            else:
                cmd = [PLAYWRIGHT_PYTHON, str(PURPLE_SCRIPT), fn_url, str(output_file), '--smart'] + keywords
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, start_new_session=True)
            try:
                stdout, stderr = proc.communicate(timeout=300)
                if proc.returncode == 0:
                    result = json.loads(stdout)
                    results.append({
                        "id": fn_id,
                        "status": "ok",
                        "url": fn_url,
                        "output": str(output_file),
                        "keywords": keywords,
                        "keyword_source": keyword_source,
                        "highlighted_count": result.get("highlighted_count", 0),
                    })
                else:
                    results.append({
                        "id": fn_id,
                        "status": "error",
                        "url": fn_url,
                        "error": stderr[:200] if stderr else "unknown",
                    })
            except subprocess.TimeoutExpired:
                pgid = os.getpgid(proc.pid)
                os.killpg(pgid, signal.SIGKILL)
                proc.wait()
                results.append({
                    "id": fn_id,
                    "status": "timeout",
                    "url": fn_url,
                })
        except subprocess.TimeoutExpired:
            results.append({
                "id": fn_id,
                "status": "timeout",
                "url": fn_url,
            })
        except Exception as e:
            results.append({
                "id": fn_id,
                "status": "error",
                "url": fn_url,
                "error": str(e)[:200],
            })

    # Save summary
    summary = {
        "ok": True,
        "total": len(footnotes),
        "screenshots": len([r for r in results if r["status"] == "ok"]),
        "skipped": len([r for r in results if r["status"] == "skipped"]),
        "errors": len([r for r in results if r["status"] in ("error", "timeout")]),
        "broken_urls_skipped": len([r for r in results if r.get("reason") == "URL unreachable (404/timeout)"]),
        "keyword_sources": {
            "from_excerpt": len([r for r in results if r.get("keyword_source") == "excerpt"]),
            "from_footnote_fallback": len([r for r in results if r.get("keyword_source") == "footnote_fallback"]),
        },
        "results": results,
    }

    summary_path = screenshots_dir / "summary.json"
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)

    print(json.dumps(summary))


if __name__ == "__main__":
    main()
