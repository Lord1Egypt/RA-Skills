#!/usr/bin/env python3
from pathlib import Path
import json
import sys


def find_runs_root(project_dir: Path):
    candidates = [
        project_dir / 'runs',
        project_dir / 'constraints' / 'runs',
        project_dir / 'backend' / 'runs',
    ]
    for c in candidates:
        if c.exists() and c.is_dir():
            return c
    return None


def latest_run_dir(project_dir: Path):
    runs_root = find_runs_root(project_dir)
    if runs_root is None:
        return None
    runs = [p for p in runs_root.iterdir() if p.is_dir()]
    if not runs:
        return None
    return sorted(runs)[-1]


def main():
    if len(sys.argv) < 2:
        print('usage: collect_openlane_results.py <openlane-project-dir>', file=sys.stderr)
        sys.exit(1)

    project_dir = Path(sys.argv[1])
    result = {
        'project_dir': str(project_dir.resolve()),
        'latest_run': None,
        'gds': None,
        'reports': {},
    }

    run_dir = latest_run_dir(project_dir)
    if run_dir is None:
        print(json.dumps(result, indent=2))
        return

    result['latest_run'] = str(run_dir)

    final_gds_dir = run_dir / 'final' / 'gds'
    if final_gds_dir.exists():
      gds_files = sorted(final_gds_dir.glob('*.gds'))
      if gds_files:
          result['gds'] = str(gds_files[0])

    summary_candidates = [
        run_dir / 'final' / 'summary.rpt',
        run_dir / 'final' / 'final.summary.rpt',
        run_dir / 'openlane.log',
        run_dir / 'flow.log',
        run_dir / 'warning.log',
        run_dir / 'error.log',
    ]
    for p in summary_candidates:
        if p.exists():
            result['reports'][p.name] = str(p)

    final_dir = run_dir / 'final'
    if final_dir.exists():
        result['reports']['final_dir'] = str(final_dir)
    else:
        result['reports']['final_dir'] = None

    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
