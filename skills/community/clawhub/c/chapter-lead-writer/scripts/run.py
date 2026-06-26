from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    if not path.exists() or path.stat().st_size <= 0:
        return out
    import json

    for raw in path.read_text(encoding='utf-8', errors='ignore').splitlines():
        raw = raw.strip()
        if not raw:
            continue
        try:
            rec = json.loads(raw)
        except Exception:
            continue
        if isinstance(rec, dict):
            out.append(rec)
    return out


def _load_json_asset(path: Path) -> dict[str, Any]:
    if not path.exists() or path.stat().st_size <= 0:
        return {}
    try:
        data = json.loads(path.read_text(encoding='utf-8', errors='ignore'))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def _uniq(items: list[str]) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for item in items:
        v = str(item or '').strip()
        if not v or v in seen:
            continue
        seen.add(v)
        out.append(v)
    return out


def _cite(keys: list[str], n: int = 3) -> str:
    vals = _uniq(keys)[:n]
    return f"[@{'; '.join(vals)}]" if vals else ""


def _clean_phrase(text: str) -> str:
    s = str(text or '').strip().replace('/', ' and ')
    s = ' '.join(s.split())
    return s.rstrip(' .;:，；。')


def _natural_phrase(text: str) -> str:
    s = _clean_phrase(text).replace('&', 'and')
    s = re.sub(r'\([^)]*\)', '', s)
    s = re.sub(r'\s+', ' ', s).strip(' ,;:')
    low = s.lower()
    blocked = (
        'core mechanism and architecture',
        'evaluation protocol',
        'datasets, metrics, human eval',
    )
    if any(token in low for token in blocked):
        return ''
    return low if low else ''


def _content_phrase(text: str) -> str:
    s = _clean_phrase(text)
    low = s.lower()
    prefixes = [
        'pin scope to goal:',
        'compare approaches along:',
        'para 1:',
        'para 2:',
        'para 3:',
        'para 3 (optional):',
    ]
    for prefix in prefixes:
        if low.startswith(prefix):
            s = s.split(':', 1)[1].strip() if ':' in s else ''
            low = s.lower()
    meta_starts = (
        'state the chapter',
        'preview the h3',
        'highlight evaluation anchors',
    )
    if any(low.startswith(prefix) for prefix in meta_starts):
        return ''
    return s


def _skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _compatibility_defaults() -> dict[str, Any]:
    asset_path = _skill_root() / 'assets' / 'lead_block_compatibility_defaults.json'
    return _load_json_asset(asset_path)


def _limit(value: Any, *, fallback: int) -> int:
    try:
        num = int(value)
    except Exception:
        return fallback
    return num if num > 0 else fallback


def _series(items: list[str], *, limit: int, fallback: str) -> str:
    vals = [str(item).strip() for item in items if str(item).strip()][:limit]
    if not vals:
        return fallback
    if len(vals) == 1:
        return vals[0]
    if len(vals) == 2:
        return f'{vals[0]} and {vals[1]}'
    return f"{', '.join(vals[:-1])}, and {vals[-1]}"


def _citation_suffix(keys: list[str], n: int = 3) -> str:
    cite = _cite(keys, n)
    return f' {cite}' if cite else ''


def _render(template: str, **kwargs: str) -> str:
    text = template.format(**kwargs)
    text = ' '.join(text.split())
    text = text.replace(' .', '.').replace(' ,', ',').replace(' ;', ';').replace(' :', ':')
    return text


def _ordered_options(seed: str, value: Any) -> list[str]:
    if not isinstance(value, list):
        single = str(value or '').strip()
        return [single] if single else []
    options = [str(item or '').strip() for item in value if str(item or '').strip()]
    if not options:
        return []
    digest = hashlib.sha1(str(seed or '').encode('utf-8', errors='ignore')).hexdigest()
    idx = int(digest[:12], 16) % len(options)
    return options[idx:] + options[:idx]


def _pick_template(seed: str, value: Any, fallback: str) -> str:
    options = _ordered_options(seed, value)
    return options[0] if options else fallback


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--workspace', required=True)
    parser.add_argument('--unit-id', default='')
    parser.add_argument('--inputs', default='')
    parser.add_argument('--outputs', default='')
    parser.add_argument('--checkpoint', default='')
    args = parser.parse_args()

    repo_root = Path(__file__).resolve()
    for _ in range(10):
        if (repo_root / "AGENTS.md").exists():
            break
        parent = repo_root.parent
        if parent == repo_root:
            break
        repo_root = parent
    sys.path.insert(0, str(repo_root))

    from tooling.common import atomic_write_text, ensure_dir, load_yaml, now_iso_seconds
    from tooling.pipeline_text import slug_unit_id

    workspace = Path(args.workspace).resolve()
    compat = _compatibility_defaults()
    limits = compat.get('limits') if isinstance(compat.get('limits'), dict) else {}
    fallbacks = compat.get('fallbacks') if isinstance(compat.get('fallbacks'), dict) else {}
    templates = compat.get('templates') if isinstance(compat.get('templates'), dict) else {}
    archetype = str(compat.get('default_archetype') or 'lens-first').strip() or 'lens-first'
    template_pack = templates.get(archetype) if isinstance(templates.get(archetype), dict) else {}
    sections_dir = workspace / 'sections'
    ensure_dir(sections_dir)
    report_path = workspace / 'output' / 'CHAPTER_LEADS_REPORT.md'
    ensure_dir(report_path.parent)

    outline = load_yaml(workspace / 'outline' / 'outline.yml') if (workspace / 'outline' / 'outline.yml').exists() else []
    briefs = {str(r.get('section_id') or '').strip(): r for r in _load_jsonl(workspace / 'outline' / 'chapter_briefs.jsonl') if str(r.get('section_id') or '').strip()}
    packs = _load_jsonl(workspace / 'outline' / 'writer_context_packs.jsonl')
    cites_by_sec: dict[str, list[str]] = {}
    for rec in packs:
        sec_id = str(rec.get('section_id') or '').strip()
        if not sec_id:
            continue
        bucket = cites_by_sec.setdefault(sec_id, [])
        for field in ['allowed_bibkeys_selected', 'allowed_bibkeys_chapter']:
            for key in rec.get(field) or []:
                bucket.append(str(key).strip())

    written: list[str] = []
    if isinstance(outline, list):
        for sec in outline:
            if not isinstance(sec, dict):
                continue
            subs = [x for x in (sec.get('subsections') or []) if isinstance(x, dict)]
            if not subs:
                continue
            sec_id = str(sec.get('id') or '').strip()
            sec_title = str(sec.get('title') or '').strip() or str(fallbacks.get('section_title') or 'chapter {section_id}').format(section_id=sec_id)
            if not sec_id:
                continue
            brief = briefs.get(sec_id) or {}
            throughline = [_natural_phrase(_content_phrase(x)) for x in (brief.get('throughline') or []) if _natural_phrase(_content_phrase(x))]
            contrasts = [_natural_phrase(x) for x in (brief.get('key_contrasts') or []) if _natural_phrase(x)]
            sub_titles = [str(x.get('title') or '').strip() for x in subs if str(x.get('title') or '').strip()]
            cites = cites_by_sec.get(sec_id) or []
            comparison_problem = _series(
                contrasts or throughline,
                limit=_limit(limits.get('throughline_items'), fallback=2),
                fallback=str(fallbacks.get('comparison_problem') or 'the comparison pressure that the subsections keep reopening'),
            )
            recurring_contrasts = _series(
                contrasts,
                limit=_limit(limits.get('contrast_items'), fallback=3),
                fallback=str(fallbacks.get('recurring_contrasts') or 'protocol assumptions, resource constraints, and evaluation scope'),
            )
            subsection_preview = _series(
                sub_titles,
                limit=_limit(limits.get('subsection_preview_items'), fallback=3),
                fallback=str(fallbacks.get('subsection_preview') or 'the chapter subsections'),
            )
            paragraph_1 = _render(
                _pick_template(
                    f'lead:p1:{sec_id}:{sec_title}',
                    template_pack.get('paragraph_1'),
                    'What binds {section_title} together is a shared comparison problem: {comparison_problem}{citation}.',
                ),
                section_title=sec_title,
                comparison_problem=comparison_problem,
                citation=_citation_suffix(cites, 4),
            )
            paragraph_2 = _render(
                _pick_template(
                    f'lead:p2:{sec_id}:{subsection_preview}',
                    template_pack.get('paragraph_2'),
                    'Taken together, {subsection_preview} show why {recurring_contrasts} cannot be treated as background implementation detail{citation}.',
                ),
                subsection_preview=subsection_preview,
                recurring_contrasts=recurring_contrasts,
                citation=_citation_suffix(cites[4:], 4) or _citation_suffix(cites, 4),
            )
            paragraphs = [paragraph_1, paragraph_2]
            path = sections_dir / f"{slug_unit_id(sec_id)}_lead.md"
            atomic_write_text(path, '\n\n'.join(paragraphs).rstrip() + '\n')
            written.append(str(path.relative_to(workspace)))

    report = '\n'.join([
        '# Chapter leads report',
        '',
        '- Status: PASS',
        f'- Generated at: `{now_iso_seconds()}`',
    ] + [f'- `{p}`' for p in written]) + '\n'
    atomic_write_text(report_path, report)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
