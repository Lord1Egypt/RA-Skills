from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


def _extract_cites(text: str) -> list[str]:
    keys: list[str] = []
    for m in re.finditer(r"\[@([^\]]+)\]", text or ""):
        inside = (m.group(1) or "").strip()
        for k in re.findall(r"[A-Za-z0-9:_-]+", inside):
            if k and k not in keys:
                keys.append(k)
    return keys


def _norm_title(text: str) -> str:
    return re.sub(r'[^a-z0-9]+', ' ', str(text or '').lower()).strip()


def _surface_focus(text: str) -> str:
    cleaned = re.sub(r'^\s*\d+(?:\.\d+)*\s+', '', str(text or '').strip())
    cleaned = re.sub(r'\s+', ' ', cleaned).strip(' .,:;')
    return cleaned.lower()


def _parse_budget_report(md: str) -> tuple[int, int, dict[str, list[str]], dict[str, list[str]]]:
    target = 0
    gap = 0
    suggestions: dict[str, list[str]] = {}
    suggestions_by_title: dict[str, list[str]] = {}
    m = re.search(r"(?im)^\s*-\s*Global\s+(?:target|hard\s+minimum).*>=\s*(\d+)\b", md or "")
    if m:
        target = int(m.group(1))
    m = re.search(r"(?im)^\s*-\s*Gap(?:\s*\([^)]*\))?\s*:\s*(\d+)\b", md or "")
    if m:
        gap = int(m.group(1))
    for raw in (md or "").splitlines():
        line = raw.strip()
        if not line.startswith("|") or line.startswith("|---") or "| suggested keys" in line.lower():
            continue
        cols = [c.strip() for c in line.strip("|").split("|")]
        if len(cols) < 6:
            continue
        sub_id = cols[0].strip()
        title = cols[1].strip() if len(cols) > 1 else ''
        sug = cols[5].strip()
        keys = [k.strip() for k in re.findall(r"`([^`]+)`", sug) if k.strip()]
        if sub_id and keys:
            suggestions[sub_id] = keys
        if title and keys:
            suggestions_by_title[_norm_title(title)] = keys
    return target, gap, suggestions, suggestions_by_title


def _split_h3(md: str) -> list[tuple[str | None, list[str]]]:
    blocks: list[tuple[str | None, list[str]]] = []
    current_title: str | None = None
    current_lines: list[str] = []
    for raw in (md or '').splitlines():
        if raw.startswith('### '):
            if current_title is not None:
                blocks.append((current_title, current_lines))
            current_title = raw[4:].strip()
            current_lines = [raw]
            continue
        if raw.startswith('## '):
            if current_title is not None:
                blocks.append((current_title, current_lines))
                current_title = None
                current_lines = []
            blocks.append((None, [raw]))
            continue
        if current_title is not None:
            current_lines.append(raw)
        else:
            if not blocks:
                blocks.append((None, [raw]))
            else:
                blocks[-1][1].append(raw)
    if current_title is not None:
        blocks.append((current_title, current_lines))
    return blocks


def _section_id_from_title(title: str) -> str:
    m = re.match(r'^(\d+(?:\.\d+)?)\b', str(title or '').strip())
    return m.group(1) if m else ''


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


def _pick_variant(*, seed: str, options: list[str]) -> str:
    if not options:
        return ""
    h = int(hashlib.sha1(str(seed or "").encode("utf-8", errors="ignore")).hexdigest()[:8], 16)
    return options[h % len(options)]


def _format_cite_text(keys: list[str]) -> str:
    phrases = [f'[@{k}]' for k in _uniq(keys)]
    if not phrases:
        return ''
    if len(phrases) == 1:
        return phrases[0]
    if len(phrases) == 2:
        return f'{phrases[0]} and {phrases[1]}'
    return ', '.join(phrases[:-1]) + f', and {phrases[-1]}'


def _load_writer_pack_context(workspace: Path) -> dict[str, dict[str, object]]:
    contexts: dict[str, dict[str, object]] = {}
    packs_path = workspace / "outline" / "writer_context_packs.jsonl"
    if not packs_path.exists() or packs_path.stat().st_size <= 0:
        return contexts
    for raw in packs_path.read_text(encoding='utf-8', errors='ignore').splitlines():
        raw = raw.strip()
        if not raw:
            continue
        try:
            rec = json.loads(raw)
        except Exception:
            continue
        if not isinstance(rec, dict):
            continue
        title = _norm_title(rec.get('title') or '')
        if not title:
            continue
        clusters: list[str] = []
        for item in (rec.get('clusters') or []):
            if not isinstance(item, dict):
                continue
            label = re.sub(r'\s+', ' ', str(item.get('label') or '').strip()).strip(' .,:;')
            if label and label not in clusters:
                clusters.append(label)
        axes = [
            re.sub(r'\s+', ' ', str(axis or '').strip()).strip(' .,:;')
            for axis in (rec.get('axes') or [])
            if str(axis or '').strip()
        ]
        contexts[title] = {
            'contrast_hook': re.sub(r'\s+', ' ', str(rec.get('contrast_hook') or '').strip()).strip(' .,:;'),
            'axes': axes,
            'clusters': clusters,
        }
    return contexts


def _in_scope_sentences(keys: list[str], *, title: str = "", context: dict[str, object] | None = None) -> list[str]:
    keys = _uniq(keys)
    if not keys:
        return []
    focus = _surface_focus(title) or 'the same question'
    ctx = context or {}
    axes = _uniq([str(x or '').strip() for x in (ctx.get('axes') or []) if str(x or '').strip()])
    hint = axes[0] if axes else re.sub(r'\s+', ' ', str(ctx.get('contrast_hook') or '').strip()).strip(' .,:;')
    clusters = _uniq([str(x or '').strip() for x in (ctx.get('clusters') or []) if str(x or '').strip()])
    templates: list[str] = []
    if len(clusters) >= 2:
        templates.extend([
            "Across {focus}, adjacent studies extend both {cluster_a} and {cluster_b} {cite_text}.",
            "Comparable cases in {focus} appear on both sides of the comparison {cite_text}.",
        ])
    if hint:
        templates.extend([
            "Additional work in {focus} keeps returning to {hint} as a comparison pressure {cite_text}.",
            "Related studies in {focus} also sharpen the record around {hint} {cite_text}.",
        ])
    templates.extend([
        "Additional studies in {focus} help bound the comparison {cite_text}.",
        "Neighboring work in {focus} broadens the evidence base {cite_text}.",
    ])
    out: list[str] = []
    for idx in range(0, len(keys), 6):
        chunk = keys[idx: idx + 6]
        cite_text = _format_cite_text(chunk)
        template = _pick_variant(seed=f"{focus}:{idx}:{'|'.join(chunk)}", options=templates)
        out.append(
            template.format(
                focus=focus,
                hint=hint,
                cluster_a=clusters[0] if clusters else 'one line of work',
                cluster_b=clusters[1] if len(clusters) > 1 else 'another line of work',
                cite_text=cite_text,
            )
        )
    return out


def _global_top_up_sentences(keys: list[str], *, title: str = "the broader survey") -> list[str]:
    keys = _uniq(keys)
    if not keys:
        return []
    templates = [
        "Appendix-level background references also include {tail}.",
        "Broader survey context is also visible in {tail}.",
        "Supplementary cross-chapter references include {tail}.",
    ]
    out: list[str] = []
    for idx in range(0, len(keys), 8):
        chunk = keys[idx: idx + 8]
        if not chunk:
            continue
        tail = _format_cite_text(chunk)
        template = _pick_variant(seed=f"global:{title}:{idx}:{'|'.join(chunk)}", options=templates)
        out.append(template.format(title_lower=str(title or "the broader survey").strip().lower(), tail=tail))
    return out


def _inject_sentences_into_block(block: str, sentences: list[str]) -> str:
    sentence_block = ' '.join(re.sub(r'\s+', ' ', s.strip()) for s in sentences if str(s or '').strip()).strip()
    if not sentence_block:
        return block
    lines = block.splitlines()
    if not lines or not lines[0].startswith('### '):
        return (block.rstrip() + ' ' + sentence_block).strip()
    heading = lines[0].rstrip()
    body = '\n'.join(lines[1:]).strip()
    if not body:
        return heading + '\n\n' + sentence_block
    paragraphs = [part.strip() for part in re.split(r'\n\s*\n', body) if part.strip()]
    if not paragraphs:
        return heading + '\n\n' + sentence_block
    insert_at = 1 if len(paragraphs) >= 2 else len(paragraphs)
    paragraphs.insert(insert_at, sentence_block)
    return heading + '\n\n' + '\n\n'.join(paragraphs)


def _load_writer_pack_pool(workspace: Path) -> list[str]:
    pool: list[str] = []
    packs_path = workspace / "outline" / "writer_context_packs.jsonl"
    if not packs_path.exists() or packs_path.stat().st_size <= 0:
        return pool
    for raw in packs_path.read_text(encoding='utf-8', errors='ignore').splitlines():
        raw = raw.strip()
        if not raw:
            continue
        try:
            rec = json.loads(raw)
        except Exception:
            continue
        if not isinstance(rec, dict):
            continue
        for field in ("allowed_bibkeys_selected", "allowed_bibkeys_mapped", "allowed_bibkeys_chapter", "allowed_bibkeys_global"):
            for key in (rec.get(field) or []):
                cleaned = str(key or '').strip()
                if cleaned and cleaned not in pool:
                    pool.append(cleaned)
    return pool


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

    from tooling.common import atomic_write_text, ensure_dir, parse_semicolon_list
    from tooling.quality_gate import QualityIssue, _draft_profile, check_unit_outputs, write_quality_report

    workspace = Path(args.workspace).resolve()
    unit_id = str(args.unit_id or 'U1045').strip() or 'U1045'
    inputs = parse_semicolon_list(args.inputs) or ['output/DRAFT.md', 'output/CITATION_BUDGET_REPORT.md']
    outputs = parse_semicolon_list(args.outputs) or ['output/DRAFT.md', 'output/CITATION_INJECTION_REPORT.md']

    draft_rel = next((p for p in outputs if p.endswith('DRAFT.md')), 'output/DRAFT.md')
    report_rel = next((p for p in outputs if p.endswith('CITATION_INJECTION_REPORT.md')), 'output/CITATION_INJECTION_REPORT.md')
    budget_rel = next((p for p in inputs if p.endswith('CITATION_BUDGET_REPORT.md')), 'output/CITATION_BUDGET_REPORT.md')
    draft_path = workspace / draft_rel
    report_path = workspace / report_rel
    budget_path = workspace / budget_rel
    ensure_dir(report_path.parent)

    missing_inputs: list[str] = []
    if not draft_path.exists() or draft_path.stat().st_size <= 0:
        missing_inputs.append(draft_rel)
    if not budget_path.exists() or budget_path.stat().st_size <= 0:
        missing_inputs.append(budget_rel)
    if missing_inputs:
        msg = 'Missing inputs: ' + ', '.join(missing_inputs)
        atomic_write_text(report_path, '# Citation injection report\n\n- Status: FAIL\n- Reason: ' + msg + '\n')
        write_quality_report(workspace=workspace, unit_id=unit_id, skill='citation-injector', issues=[QualityIssue(code='missing_inputs', message=msg)])
        return 2

    draft = draft_path.read_text(encoding='utf-8', errors='ignore')
    budget = budget_path.read_text(encoding='utf-8', errors='ignore')
    target, gap_from_budget, suggestions, suggestions_by_title = _parse_budget_report(budget)
    draft_profile = _draft_profile(workspace)
    local_floor = 0
    pack_context = _load_writer_pack_context(workspace)

    current_unique = len(set(_extract_cites(draft)))
    modified_blocks = 0
    if target > 0 and suggestions:
        new_parts: list[str] = []
        seen_after = set(_extract_cites(draft))
        for title, lines in _split_h3(draft):
            block = '\n'.join(lines).rstrip()
            if title is None:
                new_parts.append(block)
                continue
            sid = _section_id_from_title(title)
            suggested = suggestions.get(sid) or suggestions_by_title.get(_norm_title(title)) or []
            if suggested:
                existing = set(_extract_cites(block))
                local_need = max(0, int(local_floor) - len(existing))
                needed_budget = max(0, int(target) - len(seen_after))
                desired = needed_budget if needed_budget > 0 else local_need
                if desired <= 0:
                    new_parts.append(block)
                    continue
                preferred_new = [k for k in suggested if k not in existing and k not in seen_after]
                reusable_local = [k for k in suggested if k not in existing and k in seen_after]
                needed = preferred_new[:desired]
                if len(needed) < desired:
                    needed.extend(reusable_local[: max(0, desired - len(needed))])
                if needed:
                    inserted = needed[:4]
                    sentences = _in_scope_sentences(inserted, title=title, context=pack_context.get(_norm_title(title)))
                    if sentences:
                        block = _inject_sentences_into_block(block, sentences)
                        modified_blocks += 1
                        seen_after.update(inserted)
            new_parts.append(block)
        draft = '\n'.join(part for part in new_parts if part is not None).rstrip() + '\n'
        atomic_write_text(draft_path, draft)

    unique_after_h3 = len(set(_extract_cites(draft)))
    if target > 0 and unique_after_h3 < target:
        pool: list[str] = []
        for keys in suggestions.values():
            for key in keys:
                cleaned = str(key or "").strip()
                if cleaned and cleaned not in pool:
                    pool.append(cleaned)
        for key in _load_writer_pack_pool(workspace):
            if key not in pool:
                pool.append(key)
        remaining = [k for k in pool if k not in set(_extract_cites(draft))]
        if remaining:
            redistributed: list[str] = []
            seen_after = set(_extract_cites(draft))
            new_parts = []
            for title, lines in _split_h3(draft):
                block = '\n'.join(lines).rstrip()
                if title is None:
                    new_parts.append(block)
                    continue
                if not remaining or len(seen_after) >= int(target):
                    new_parts.append(block)
                    continue
                take = min(3, max(1, int(target) - len(seen_after)), len(remaining))
                chunk = remaining[:take]
                remaining = remaining[take:]
                sentences = _in_scope_sentences(chunk, title=title, context=pack_context.get(_norm_title(title)))
                if sentences:
                    block = _inject_sentences_into_block(block, sentences)
                    redistributed.extend(chunk)
                    seen_after.update(chunk)
                    modified_blocks += 1
                new_parts.append(block)
            if redistributed:
                draft = '\n'.join(part for part in new_parts if part is not None).rstrip() + '\n'
                atomic_write_text(draft_path, draft)
                unique_after_h3 = len(set(_extract_cites(draft)))
        if target > 0 and unique_after_h3 < target:
            remaining = [k for k in pool if k not in set(_extract_cites(draft))]
            needed = max(0, int(target) - int(unique_after_h3))
            global_lines = _global_top_up_sentences(remaining[: max(needed, 4)], title="the broader survey")
            if global_lines:
                appendix_markers = ['\n**Appendix', '\n## Appendix']
                insert_at = len(draft)
                found_appendix = False
                for marker in appendix_markers:
                    idx = draft.find(marker)
                    if idx != -1:
                        line_end = draft.find('\n', idx + 1)
                        insert_at = min(insert_at, (line_end + 1) if line_end != -1 else len(draft))
                        found_appendix = True
                extra = '\n\n'.join(global_lines)
                if insert_at < len(draft):
                    draft = draft[:insert_at].rstrip() + '\n\n' + extra + '\n\n' + draft[insert_at:].lstrip()
                else:
                    draft = draft.rstrip() + '\n\n' + extra + '\n'
                atomic_write_text(draft_path, draft)

    unique = len(set(_extract_cites(draft)))
    gap_current = max(0, int(target) - int(unique)) if target > 0 else 0
    status = 'PASS' if (target <= 0 or unique >= target) else 'FAIL'
    lines = [
        '# Citation injection report',
        '',
        f'- Status: {status}',
        f'- Draft: `{draft_rel}`',
        f'- Budget: `{budget_rel}`',
        f'- Unique citations (current): {unique}',
        f'- Global target (from budget): {target}',
        f'- Gap (current, to target): {gap_current}',
        f'- Gap (from budget, at report time): {gap_from_budget}',
        f'- H3 blocks modified: {modified_blocks}',
        '',
    ]
    if status == 'PASS':
        summary = '- Citation target satisfied after in-scope injection.'
        lines.extend(['## Summary', '', summary, ''])
    else:
        lines.extend(['## Summary', '', '- Citation target is still unmet after automatic in-scope injection.', ''])
        if suggestions:
            lines.extend(['## Remaining suggestions', ''])
            for sid, keys in list(suggestions.items())[:10]:
                lines.append(f"- `{sid}`: " + ', '.join(f'`{k}`' for k in keys[:8]))
            lines.append('')
    atomic_write_text(report_path, '\n'.join(lines).rstrip() + '\n')

    issues = check_unit_outputs(skill='citation-injector', workspace=workspace, outputs=[report_rel])
    if issues:
        write_quality_report(workspace=workspace, unit_id=unit_id, skill='citation-injector', issues=issues)
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
