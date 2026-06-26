#!/usr/bin/env python3
from pathlib import Path
import json
import sys

BASE = Path('/root/.openclaw/workspace/skills/eda-spec2gds/eda-runs').resolve()


def load_json(path: Path, default=None):
    if default is None:
        default = {}
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception:
        return default


def summarize_run(run_dir: Path):
    final_dir = run_dir / 'final'
    metrics = load_json(final_dir / 'metrics.json', {})
    has_gds = any((final_dir / 'gds').glob('*.gds')) if (final_dir / 'gds').exists() else False
    return {
        'run': run_dir.name,
        'path': str(run_dir),
        'has_gds': has_gds,
        'die_area': metrics.get('design__die__area'),
        'utilization': metrics.get('design__instance__utilization'),
        'setup_wns': metrics.get('timing__setup__wns'),
        'hold_wns': metrics.get('timing__hold__wns'),
        'power_total': metrics.get('power__total'),
        'route_drc_errors': metrics.get('route__drc_errors'),
        'lvs_errors': metrics.get('design__lvs_error__count'),
        'magic_drc_errors': metrics.get('magic__drc_error__count'),
        'max_slew_violations': metrics.get('design__max_slew_violation__count'),
        'status': 'pass' if has_gds else 'unknown',
    }


def main():
    if len(sys.argv) < 3:
        print('usage: build_run_history.py <project-root> <output.json>', file=sys.stderr)
        sys.exit(1)
    project = Path(sys.argv[1])
    out = Path(sys.argv[2])
    runs_root = project / 'constraints' / 'runs'
    history = {'runs': []}
    if runs_root.exists():
        # Only include runs with actual results (have 'final' directory)
        for run_dir in sorted([p for p in runs_root.iterdir() if p.is_dir() and (p / 'final').exists()]):
            history['runs'].append(summarize_run(run_dir))
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(history, indent=2, ensure_ascii=False), encoding='utf-8')
    print(out)


if __name__ == '__main__':
    main()
