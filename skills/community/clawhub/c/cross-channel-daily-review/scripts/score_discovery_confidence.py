#!/usr/bin/env python3
import json
import sys
from pathlib import Path


def score(item):
    score = 0
    reasons = []
    status = item.get('status')
    scopes = 0
    for note in item.get('notes', []):
        if str(note).startswith('scopes='):
            try:
                scopes = int(str(note).split('=', 1)[1])
            except Exception:
                scopes = 0
    if status == 'active':
        score += 60
        reasons.append('sessions metadata confirmed')
    elif status == 'configured':
        score += 30
        reasons.append('structured transcript candidate only')
    if item.get('scope_type') and item.get('scope_type') != 'unknown':
        score += 15
        reasons.append('scope type inferred')
    if scopes > 0:
        score += min(scopes * 5, 15)
        reasons.append(f'{scopes} scope(s) detected')
    if item.get('session_count', 0) > 0:
        score += min(item.get('session_count', 0) * 2, 10)
        reasons.append(f"{item.get('session_count')} session(s) linked")
    return min(score, 100), reasons


def main() -> int:
    if len(sys.argv) != 3:
        print('usage: score_discovery_confidence.py <normalized.json> <output.json>', file=sys.stderr)
        return 2
    data = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
    for item in data:
        sc, reasons = score(item)
        item['confidence_score'] = sc
        item['confidence_reasons'] = reasons
    Path(sys.argv[2]).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'channels': len(data), 'scored': True}, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
