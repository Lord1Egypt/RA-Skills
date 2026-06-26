#!/usr/bin/env python3
import argparse
from pathlib import Path

ALLOWED_STATUS = {'open','pending_approval','approved','in_progress','blocked','handoff_needed','done','cancelled'}
ALLOWED_MODE = {'proposal-approval','claimable'}
ALLOWED_RISK = {'low','medium','high'}
REQUIRED_KEYS = ['id','title','visibility','status','mode','approval_required','risk_level']


def parse_simple_yaml(text):
    data = {}
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        if line.startswith(' ') or line.startswith('\t'):
            continue
        if ':' not in line:
            continue
        k, v = line.split(':', 1)
        data[k.strip()] = v.strip()
    return data


def validate(path: Path):
    data = parse_simple_yaml(path.read_text(encoding='utf-8', errors='ignore'))
    errors = []
    warnings = []
    for key in REQUIRED_KEYS:
        if key not in data:
            errors.append(f'missing key: {key}')
    status = data.get('status')
    mode = data.get('mode')
    risk = data.get('risk_level')
    if status and status not in ALLOWED_STATUS:
        errors.append(f'invalid status: {status}')
    if mode and mode not in ALLOWED_MODE:
        errors.append(f'invalid mode: {mode}')
    if risk and risk not in ALLOWED_RISK:
        errors.append(f'invalid risk_level: {risk}')
    if data.get('approval_required') not in {'true','false'}:
        errors.append('approval_required must be true or false')
    if data.get('mode') == 'claimable' and data.get('risk_level') != 'low':
        errors.append('claimable tasks must have risk_level: low')
    if data.get('mode') == 'claimable' and data.get('approval_required') == 'true':
        errors.append('claimable tasks should not require approval; use proposal-approval instead')
    outputs = data.get('outputs', '')
    if 'policy/' in outputs:
        errors.append('tasks that change policy outputs must not be treated as ordinary task outputs')
    if 'demo_space' not in data:
        warnings.append('missing demo_space (recommended for project scoping)')
    if 'priority' not in data:
        warnings.append('missing priority')
    return errors, warnings


def main():
    parser = argparse.ArgumentParser(description='Validate basic ClawColab task file state.')
    parser.add_argument('paths', nargs='+')
    args = parser.parse_args()
    failed = False
    for raw in args.paths:
        path = Path(raw)
        errs, warns = validate(path)
        if errs:
            failed = True
            print(f'FAIL {path}')
            for err in errs:
                print(f'  - {err}')
        else:
            print(f'OK   {path}')
        for warn in warns:
            print(f'WARN {path}: {warn}')
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
