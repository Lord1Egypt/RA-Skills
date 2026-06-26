#!/usr/bin/env python3
from pathlib import Path
import json
import sys


def tail(path: Path, n: int = 30):
    if not path.exists():
        return []
    return path.read_text(encoding='utf-8', errors='ignore').splitlines()[-n:]


def main():
    if len(sys.argv) < 3:
        print('usage: write_success_summary.py <openlane-results.json> <output.md>', file=sys.stderr)
        sys.exit(1)

    results_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2])
    results = json.loads(results_path.read_text(encoding='utf-8'))

    flow_log = Path(results['reports'].get('flow.log', '')) if results.get('reports') else None
    warning_log = Path(results['reports'].get('warning.log', '')) if results.get('reports') else None
    error_log = Path(results['reports'].get('error.log', '')) if results.get('reports') else None

    lines = []
    lines.append('# EDA Run Summary')
    lines.append('')
    lines.append(f"- Project: `{results.get('project_dir')}`")
    lines.append(f"- Latest run: `{results.get('latest_run')}`")
    lines.append(f"- Final GDS: `{results.get('gds')}`")
    lines.append(f"- Final dir: `{results.get('reports', {}).get('final_dir')}`")
    lines.append('')
    lines.append('## Status')
    lines.append('')
    lines.append('- OpenLane flow completed and final GDS was generated.')
    lines.append('')

    if warning_log and warning_log.exists():
        warnings = tail(warning_log, 20)
        if warnings:
            lines.append('## Warning tail')
            lines.append('')
            lines.extend([f'- {w}' for w in warnings if w.strip()])
            lines.append('')

    if error_log and error_log.exists():
        errors = [e for e in tail(error_log, 20) if e.strip()]
        if errors:
            lines.append('## Error tail')
            lines.append('')
            lines.extend([f'- {e}' for e in errors])
            lines.append('')

    if flow_log and flow_log.exists():
        flow_tail = tail(flow_log, 20)
        if flow_tail:
            lines.append('## Flow tail')
            lines.append('')
            lines.extend([f'- {x}' for x in flow_tail if x.strip()])
            lines.append('')

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(out_path)


if __name__ == '__main__':
    main()
