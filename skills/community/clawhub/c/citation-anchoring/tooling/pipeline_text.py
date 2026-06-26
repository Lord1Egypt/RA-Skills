from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from tooling.common import load_yaml, read_jsonl


def slug_unit_id(unit_id: str) -> str:
    raw = str(unit_id or '').strip()
    out: list[str] = []
    for ch in raw:
        out.append(ch if ch.isalnum() else '_')
    safe = ''.join(out).strip('_')
    return f'S{safe}' if safe else 'S'


def load_outline_sections(path: Path) -> list[dict[str, Any]]:
    outline = load_yaml(path) if path.exists() else []
    if not isinstance(outline, list):
        return []
    out: list[dict[str, Any]] = []
    for sec in outline:
        if not isinstance(sec, dict):
            continue
        sec_id = str(sec.get('id') or '').strip()
        sec_title = str(sec.get('title') or '').strip()
        subsections: list[dict[str, str]] = []
        for sub in sec.get('subsections') or []:
            if not isinstance(sub, dict):
                continue
            sub_id = str(sub.get('id') or '').strip()
            sub_title = str(sub.get('title') or '').strip()
            if sub_id and sub_title:
                subsections.append({'id': sub_id, 'title': sub_title})
        if sec_id and sec_title:
            out.append({'id': sec_id, 'title': sec_title, 'subsections': subsections})
    return out


def iter_h3_units(path: Path) -> list[dict[str, str]]:
    units: list[dict[str, str]] = []
    for sec in load_outline_sections(path):
        sec_id = str(sec.get('id') or '').strip()
        sec_title = str(sec.get('title') or '').strip()
        for sub in sec.get('subsections') or []:
            sub_id = str(sub.get('id') or '').strip()
            sub_title = str(sub.get('title') or '').strip()
            if sub_id and sub_title:
                units.append(
                    {
                        'section_id': sec_id,
                        'section_title': sec_title,
                        'sub_id': sub_id,
                        'title': sub_title,
                    }
                )
    return units


def read_jsonl_map(path: Path, key: str) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for rec in read_jsonl(path):
        if not isinstance(rec, dict):
            continue
        val = str(rec.get(key) or '').strip()
        if val:
            out[val] = rec
    return out


def read_bib_keys(path: Path) -> set[str]:
    if not path.exists() or path.stat().st_size <= 0:
        return set()
    text = path.read_text(encoding='utf-8', errors='ignore')
    return set(re.findall(r'(?im)^@\w+\s*\{\s*([^,\s]+)\s*,', text))


def uniq_keep_order(items: list[str]) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for item in items:
        value = str(item or '').strip()
        if not value or value in seen:
            continue
        seen.add(value)
        out.append(value)
    return out


def clean_excerpt(text: str, *, limit: int = 220) -> str:
    s = str(text or '').strip()
    s = s.replace('\n', ' ')
    s = re.sub(r'\s+', ' ', s)
    s = s.strip(' "\'`')
    s = s.replace('|', ', ')
    if len(s) <= limit:
        return s
    clipped = s[:limit].rsplit(' ', 1)[0].strip()
    return clipped if clipped else s[:limit].strip()


def citation_list(keys: list[str], *, max_keys: int = 3) -> str:
    items = uniq_keep_order(keys)[:max_keys]
    if not items:
        return ''
    cites = [f'[@{k}]' for k in items]
    if len(cites) == 1:
        return cites[0]
    if len(cites) == 2:
        return f'{cites[0]} and {cites[1]}'
    return ', '.join(cites[:-1]) + f', and {cites[-1]}'


def inline_evidence_phrase(keys: list[str], *, max_keys: int = 3) -> str:
    items = uniq_keep_order(keys)[:max_keys]
    if not items:
        return ''
    cites = [f'in [@{k}]' for k in items]
    if len(cites) == 1:
        return cites[0]
    if len(cites) == 2:
        return f'{cites[0]} and {cites[1]}'
    return ', '.join(cites[:-1]) + f', and {cites[-1]}'


def heading_blocks(md: str) -> list[tuple[str, str]]:
    blocks: list[tuple[str, str]] = []
    current = ''
    lines: list[str] = []
    for raw in (md or '').splitlines():
        if raw.startswith('### '):
            if current:
                blocks.append((current, '\n'.join(lines).strip()))
            current = raw[4:].strip()
            lines = []
            continue
        if raw.startswith('## '):
            if current:
                blocks.append((current, '\n'.join(lines).strip()))
            current = ''
            lines = []
            continue
        if current:
            lines.append(raw)
    if current:
        blocks.append((current, '\n'.join(lines).strip()))
    return blocks


def dump_jsonl_lines(records: list[dict[str, Any]]) -> str:
    return '\n'.join(json.dumps(r, ensure_ascii=False) for r in records).rstrip() + ('\n' if records else '')
