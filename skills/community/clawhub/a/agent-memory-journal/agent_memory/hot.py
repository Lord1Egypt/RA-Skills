from __future__ import annotations

from pathlib import Path

from .storage import init_memory_root, extract_state, split_claim_and_metadata

HOT_LIMIT_CHARS = 2048
HOT_MIN_CHARS = 256
HOT_MAX_CHARS_CEILING = 10000


def _has_metadata_flag(line: str, flag: str) -> bool:
    if '[' not in line or ']' not in line:
        return False
    meta = line.rsplit('[', 1)[-1].rstrip(']')
    return flag in meta.split()


def effective_hot_budget(config: dict, override: int | None = None) -> int:
    if override is not None:
        return max(0, int(override))
    raw = config.get('hot_max_chars', HOT_LIMIT_CHARS)
    return min(max(HOT_MIN_CHARS, int(raw)), HOT_MAX_CHARS_CEILING)


def rebuild_agent_md(root: str | Path, max_chars: int | None = None) -> dict[str, object]:
    paths = init_memory_root(root)
    selected: list[str] = []
    budget = effective_hot_budget(paths.config, override=max_chars)
    header = paths.config.get('hot_header', '# AGENT.md')

    for core_file in sorted(paths.core_dir.glob('*.md')):
        for line in core_file.read_text(encoding='utf-8', errors='ignore').splitlines():
            stripped = line.strip()
            if not stripped.startswith('- '):
                continue
            if not _has_metadata_flag(stripped, 'pinned:true'):
                continue
            if extract_state(stripped) == 'superseded':
                continue
            claim, _meta = split_claim_and_metadata(stripped)
            selected.append(f'- {claim}')

    content_lines = [header, '']
    used = len('\n'.join(content_lines))
    kept: list[str] = []
    skipped: list[str] = []
    for item in selected:
        addition = len(item) + 1
        if used + addition > budget:
            skipped.append(item)
            continue
        kept.append(item)
        used += addition

    if kept:
        content_lines.extend(kept)
    else:
        content_lines.append('')

    paths.hot_file.write_text('\n'.join(content_lines).rstrip() + '\n', encoding='utf-8')
    return {
        'written': len(kept),
        'skipped': len(skipped),
        'max_chars': budget,
        'path': str(paths.hot_file),
    }
