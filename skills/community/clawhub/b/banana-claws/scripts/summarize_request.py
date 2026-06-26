#!/usr/bin/env python3
import argparse
import json
import pathlib


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument('--queue-dir', default='generated/imagegen-queue')
    p.add_argument('--request-id', required=True)
    args = p.parse_args()

    queue_dir = pathlib.Path(args.queue_dir)
    results = sorted((queue_dir / 'results').glob('*.json'))
    failed = sorted((queue_dir / 'failed').glob('*.json'))

    ok = []
    bad = []
    for path in results:
        j = json.loads(path.read_text())
        if j.get('request_id') == args.request_id:
            ok.append(j)
    for path in failed:
        j = json.loads(path.read_text())
        if j.get('request_id') == args.request_id:
            bad.append(j)

    files = [j.get('out') for j in ok if j.get('out')]
    out = {
        'request_id': args.request_id,
        'succeeded': len(ok),
        'failed': len(bad),
        'attachments': files,
        'handoff_mode_values': sorted({(j.get('handoff_mode') or '') for j in (ok + bad)}),
        'same_turn_drain_detected_any': any(bool(j.get('same_turn_drain_detected')) for j in (ok + bad)),
    }
    print(json.dumps(out, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
