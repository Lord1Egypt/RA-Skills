#!/usr/bin/env python3
from pathlib import Path
import json
import sys


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
    report = {
        'root': str(root.resolve()),
        'artifacts': {}
    }

    candidates = {
        'lint_log': root / 'lint' / 'lint.log',
        'sim_log': root / 'sim' / 'sim.log',
        'vcd': root / 'sim' / 'output.vcd',
        'synth_log': root / 'synth' / 'synth.log',
        'synth_netlist': root / 'synth' / 'synth_output.v',
    }

    for name, path in candidates.items():
        if path.exists():
            report['artifacts'][name] = str(path)

    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
