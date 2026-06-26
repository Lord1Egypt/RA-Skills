#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from common import INDEX_FILE, LEARNINGS_MD, MEMORY_MD, META_FILE, WORKSPACE, list_daily_memory_files
from retrieve import ensure_index_ready, summarize_index_state


def main() -> int:
    state = ensure_index_ready()
    files = []
    if MEMORY_MD.exists():
        files.append(str(MEMORY_MD.relative_to(WORKSPACE)))
    if LEARNINGS_MD.exists():
        files.append(str(LEARNINGS_MD.relative_to(WORKSPACE)))
    files.extend(str(p.relative_to(WORKSPACE)) for p in list_daily_memory_files()[:20])
    payload = {
        'workspace': str(WORKSPACE),
        'index_file': str(INDEX_FILE),
        'meta_file': str(META_FILE),
        'index_exists': INDEX_FILE.exists(),
        'meta_exists': META_FILE.exists(),
        'index_status': summarize_index_state(state),
        'source_files_preview': files,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
