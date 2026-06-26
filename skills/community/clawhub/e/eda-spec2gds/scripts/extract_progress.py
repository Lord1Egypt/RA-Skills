#!/usr/bin/env python3
from pathlib import Path
import json
import sys


def latest_run(project_root: Path):
    candidates = sorted(project_root.glob('constraints/runs/*'))
    candidates = [p for p in candidates if p.is_dir()]
    # Prefer runs with actual results (have 'final' directory or stage directories)
    for r in reversed(candidates):
        if (r / 'final').exists() or any(p.is_dir() and p.name[:2].isdigit() for p in r.iterdir()):
            return r
    return candidates[-1] if candidates else None


def stage_status(stage_dir: Path):
    name = stage_dir.name
    has_state_out = (stage_dir / 'state_out.json').exists()
    has_state_in = (stage_dir / 'state_in.json').exists()
    has_runtime = (stage_dir / 'runtime.txt').exists()
    status = 'done' if has_state_out else ('started' if has_state_in or has_runtime else 'unknown')
    return {'name': name, 'status': status}


def tail(path: Path, n: int = 20):
    if not path.exists():
        return []
    return path.read_text(encoding='utf-8', errors='ignore').splitlines()[-n:]


def main():
    if len(sys.argv) < 3:
        print('usage: extract_progress.py <project-root> <output.json>', file=sys.stderr)
        sys.exit(1)

    project_root = Path(sys.argv[1])
    out_path = Path(sys.argv[2])
    run = latest_run(project_root)
    result = {'latest_run': None, 'stages': [], 'tails': {}}
    if run is not None:
        result['latest_run'] = str(run)
        stages = [p for p in sorted(run.iterdir()) if p.is_dir() and p.name[:2].isdigit()]
        result['stages'] = [stage_status(s) for s in stages]
        for log_name in ['flow.log', 'warning.log', 'error.log']:
            result['tails'][log_name] = tail(run / log_name, 30)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')
    print(out_path)


if __name__ == '__main__':
    main()
