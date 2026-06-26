#!/usr/bin/env python3
import json
import sys
from pathlib import Path


def check(path_str):
    p = Path(path_str)
    return {"path": str(p), "exists": p.exists(), "non_empty": p.exists() and p.stat().st_size > 0}


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: verify_outputs.py <manifest.json>", file=sys.stderr)
        return 2
    manifest = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
    result = {
        "raw": [check(p) for p in manifest.get('raw_files', [])],
        "synthesized": check(manifest['synthesized_file']) if manifest.get('synthesized_file') else None,
        "boss_summary": check(manifest['boss_summary_file']) if manifest.get('boss_summary_file') else None,
        "index": check(manifest['index_file']) if manifest.get('index_file') else None,
    }
    ok = True
    for item in result['raw']:
        ok &= item['exists'] and item['non_empty']
    for key in ('synthesized', 'boss_summary', 'index'):
        item = result.get(key)
        if item is not None:
            ok &= item['exists'] and item['non_empty']
    result['ok'] = bool(ok)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if ok else 1


if __name__ == '__main__':
    raise SystemExit(main())
