#!/usr/bin/env python3
"""
Phase 3.x — Mandatory cross-agent URL deduplication.
Runs AFTER research_results.json + chapter.md + verification_keywords.json are produced.

Input:
  research_results.json  — flat list of sources with footnote_id
  chapter.md             — contains [^N] inline references
  verification_keywords.json — contains footnote_id → keywords

Output:
  research_results.json  — dedup'd, renumbered
  chapter.md             — [^N] references remapped
  verification_keywords.json — footnote_ids remapped
  dedup_report.json      — what was merged/removed
"""

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path


def load_json(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  ✓ {path}")


def dedup_sources(workdir: str):
    """Main deduplication routine."""
    research_path = Path(workdir) / 'research_results.json'
    chapter_path = Path(workdir) / 'chapter.md'
    keywords_path = Path(workdir) / 'verification_keywords.json'

    # ── 1. Load ──
    sources = load_json(research_path)
    chapter = chapter_path.read_text(encoding='utf-8')
    kw_data = load_json(keywords_path) if keywords_path.exists() else {}

    print(f'Sources loaded: {len(sources)}')
    print(f'Chapter size: {len(chapter)} chars')

    # ── 2. Find duplicates by URL ──
    url_to_fids = defaultdict(list)
    for s in sources:
        url = (s.get('url') or '').strip().rstrip('/')
        if url:
            url_to_fids[url].append(s['footnote_id'])

    # Build merge map: duplicate_id → canonical_id (smallest footnote_id)
    merge_map = {}
    removed_ids = set()
    dup_groups = []

    for url, fids in url_to_fids.items():
        if len(fids) > 1:
            canonical = min(fids)
            group = {'url': url, 'canonical': canonical, 'duplicates': []}
            for fid in sorted(fids):
                if fid != canonical:
                    merge_map[fid] = canonical
                    removed_ids.add(fid)
                    # find source info
                    src = next(s for s in sources if s['footnote_id'] == fid)
                    group['duplicates'].append({
                        'footnote_id': fid,
                        'title': src.get('title', '?')[:80],
                        'section': src.get('section', '?')[:30],
                        'source_channel': src.get('source_channel', '?'),
                    })
            dup_groups.append(group)

    if dup_groups:
        print(f'\nFound {len(dup_groups)} URL-exact duplicate groups ({len(removed_ids)} entries to remove):')
        for g in dup_groups:
            print(f"  Keep [^{g['canonical']}], remove {[d['footnote_id'] for d in g['duplicates']]} — {g['url'][:70]}")
    else:
        print('No exact-URL duplicates found.')

    # ── 2b. DOI-based dedup (same paper, different mirrors) ──
    def extract_doi(url):
        """Extract DOI from URL if present. Handles doi.org, dx.doi.org, and publisher URLs."""
        url = url.strip().rstrip('/')
        # Direct DOI resolver: doi.org/10.xxx/yyy, dx.doi.org/10.xxx/yyy
        m = re.search(r'(?:doi\.org/|dx\.doi\.org/)(10\.\d{4,}/.+)', url)
        if m:
            return m.group(1).rstrip('/')
        # Publisher URLs often contain DOIs: /article/10.xxx/yyy
        m = re.search(r'(?:/article/|/abs/)(10\.\d{4,}/[^?#]+)', url)
        if m:
            return m.group(1).rstrip('/')
        return None

    # DOI → list of (footnote_id, url, title)
    doi_map = defaultdict(list)
    for s in sources:
        url = s.get('url', '')
        doi = extract_doi(url)
        if doi:
            doi_map[doi].append({
                'footnote_id': s['footnote_id'],
                'url': url,
                'title': s.get('title', '?')[:80]
            })

    doi_dup_groups = []
    for doi, entries in doi_map.items():
        if len(entries) > 1:
            fids = [e['footnote_id'] for e in entries]
            canonical = min(fids)
            group = {'doi': doi, 'canonical': canonical, 'entries': entries}
            for e in entries:
                if e['footnote_id'] != canonical:
                    merge_map[e['footnote_id']] = canonical
                    removed_ids.add(e['footnote_id'])
            doi_dup_groups.append(group)

    if doi_dup_groups:
        print(f'\nFound {len(doi_dup_groups)} DOI-based cross-domain duplicate groups:')
        for g in doi_dup_groups:
            print(f"  DOI: {g['doi'][:50]}")
            for e in g['entries']:
                mark = ' ← KEEP' if e['footnote_id'] == g['canonical'] else ' ✗ REMOVE'
                print(f"    [^{e['footnote_id']}] {e['url'][:70]}...{mark}")

    # ── 2c. Title-based near-duplicate detection (flag only, no auto-remove) ──
    def normalize_title(title):
        """Strip parentheticals, lowercase, collapse whitespace."""
        t = re.sub(r'\([^)]*\)', '', title.lower())
        t = re.sub(r'[^a-z0-9\s]', '', t)
        t = re.sub(r'\s+', ' ', t).strip()
        return t

    title_map = defaultdict(list)
    for s in sources:
        if s['footnote_id'] in removed_ids:
            continue
        tkey = normalize_title(s.get('title', ''))
        if len(tkey) > 20:
            title_map[tkey].append(s)

    title_merged = 0
    title_warnings = []
    for tkey, group in title_map.items():
        if len(group) > 1:
            urls = set(s['url'].rstrip('/') for s in group if s.get('url'))
            if len(urls) > 1:
                # Auto-merge if title > 40 chars (essentially zero false-positive risk)
                if len(tkey) > 40:
                    # Prefer DOI URL as canonical; fallback to smallest footnote_id
                    doi_srcs = [s for s in group if 'doi.org/' in s.get('url','')]
                    if doi_srcs:
                        canonical = min(s['footnote_id'] for s in doi_srcs)
                    else:
                        canonical = min(s['footnote_id'] for s in group)
                    for s in group:
                        if s['footnote_id'] != canonical:
                            merge_map[s['footnote_id']] = canonical
                            removed_ids.add(s['footnote_id'])
                            title_merged += 1
                    print(f"  Title-merge: '{tkey[:60]}...' → keep [^{canonical}], remove {[s['footnote_id'] for s in group if s['footnote_id']!=canonical]}")
                else:
                    title_warnings.append({'title_key': tkey, 'sources': group})
    if title_merged:
        print(f'\nAuto-merged {title_merged} entries from {title_merged} title-based cross-domain duplicate groups.')

    if title_warnings:
        print(f'\n⚠️  {len(title_warnings)} short-title near-duplicates detected (NOT auto-removed — review manually):')
        for tw in title_warnings:
            print(f"  Title: {tw['title_key'][:80]}")
            for s in tw['sources']:
                print(f"    [^{s['footnote_id']}] {s.get('url','')[:80]}...")

    # ── 3. Remove duplicates, renumber ──
    original_count = len(sources)
    sources = [s for s in sources if s['footnote_id'] not in removed_ids]
    sources.sort(key=lambda s: s['footnote_id'])

    # Renumber
    renumber_map = {}
    for new_id, s in enumerate(sources):
        old_id = s['footnote_id']
        renumber_map[old_id] = new_id
        s['footnote_id'] = new_id

    new_count = len(sources)

    # ── 4. Build final remapping ──
    all_old_ids = set(range(original_count))  # footnote_ids are 0..original_count-1
    final_map = {}
    merged_count = 0

    for old_id in sorted(all_old_ids):
        if old_id in merge_map:
            canon = merge_map[old_id]
            final_map[old_id] = renumber_map[canon]
            merged_count += 1
        elif old_id in renumber_map:
            final_map[old_id] = renumber_map[old_id]
        # else: shouldn't happen

    # ── 5. Save dedup'd research_results.json ──
    save_json(research_path, sources)

    # ── 6. Remap chapter.md ──
    # Match [^N] where N is 0-121 (or whatever max was)
    max_id = max(final_map.keys())
    pattern = re.compile(r'\[\^(\d+)\]')

    def replace_fn(m):
        fid = int(m.group(1))
        if fid <= max_id and fid in final_map:
            return f'[^{final_map[fid]}]'
        return m.group(0)  # unchanged (e.g., IDs beyond range)

    new_chapter = pattern.sub(replace_fn, chapter)

    # Also remap footnote definitions: [^N]: text
    new_chapter = pattern.sub(replace_fn, new_chapter)

    # ── 6b. Remove duplicate footnote definitions ──
    # After remapping, multiple lines may define the same [^N]. Keep first only.
    lines = new_chapter.split('\n')
    seen_defs = set()
    cleaned_lines = []
    def_start_re = re.compile(r'^\[\^(\d+)\]:')
    removed_defs = 0
    for line in lines:
        m = def_start_re.match(line)
        if m:
            fid = int(m.group(1))
            if fid in seen_defs:
                removed_defs += 1
                continue  # skip duplicate definition
            seen_defs.add(fid)
        cleaned_lines.append(line)
    new_chapter = '\n'.join(cleaned_lines)
    if removed_defs:
        print(f"  Removed {removed_defs} duplicate footnote definitions (same ID, different lines)")

    chapter_path.write_text(new_chapter, encoding='utf-8')
    print(f"  ✓ {chapter_path} ({len(new_chapter)} chars, {len(pattern.findall(new_chapter))} refs)")

    # ── 7. Remap verification_keywords.json ──
    if isinstance(kw_data, list):
        # List of {id: "...", url: "...", keywords: [...]}
        new_kw = []
        for entry in kw_data:
            fid = entry.get('id') or entry.get('footnote_id')
            if fid is not None:
                fid = int(fid)
                if fid in final_map:
                    entry = dict(entry)
                    entry['id'] = str(final_map[fid])
                    entry['footnote_id'] = final_map[fid]
            new_kw.append(entry)
    elif isinstance(kw_data, dict) and 'footnotes' in kw_data:
        for fn in kw_data['footnotes']:
            fid = int(fn.get('id', fn.get('footnote_id', -1)))
            if fid in final_map:
                fn['id'] = str(final_map[fid])
                fn['footnote_id'] = final_map[fid]

    save_json(keywords_path, kw_data)

    # ── 8. Report ──
    report = {
        'original_count': original_count,
        'new_count': new_count,
        'removed': len(removed_ids),
        'duplicate_groups': len(dup_groups),
        'remapping_summary': {str(k): v for k, v in sorted(final_map.items()) if k != v},
        'groups': dup_groups,
    }
    report_path = Path(workdir) / 'dedup_report.json'
    save_json(report_path, report)

    print(f'\n✅ Dedup complete: {original_count} → {new_count} sources ({len(removed_ids)} removed)')
    print(f'   Remapped {merged_count} references in chapter.md')
    print(f'   Report: {report_path}')


if __name__ == '__main__':
    workdir = sys.argv[1] if len(sys.argv) > 1 else '.'
    dedup_sources(workdir)
