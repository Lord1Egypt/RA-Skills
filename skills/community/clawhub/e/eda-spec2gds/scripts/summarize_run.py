#!/usr/bin/env python3
from pathlib import Path
import json
import sys


def tail(path: Path, n: int = 20):
    if not path.exists():
        return None
    lines = path.read_text(encoding='utf-8', errors='ignore').splitlines()
    return lines[-n:]


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
    summary = {
        'status': 'PARTIAL',
        'artifacts': {},
        'hints': []
    }

    for rel in ['lint/lint.log', 'sim/sim.log', 'synth/synth.log']:
        p = root / rel
        if p.exists():
            summary['artifacts'][rel] = str(p)
            summary[f'{rel}_tail'] = tail(p)

    if (root / 'synth' / 'synth_output.v').exists():
        summary['status'] = 'PASS'
    elif (root / 'sim' / 'sim.log').exists():
        summary['hints'].append('simulation exists but synthesis netlist missing')

    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
