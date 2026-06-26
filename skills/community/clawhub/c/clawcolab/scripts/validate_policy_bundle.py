#!/usr/bin/env python3
import argparse
from pathlib import Path

REQUIRED_VISIBILITY = {'private', 'sealed', 'shared-team', 'public-repo'}
REQUIRED_ROLES = {'coordinator', 'architect', 'implementer', 'reviewer', 'security-reviewer', 'human-approver'}
REQUIRED_APPROVAL_KEYS = {'visibility_promotion', 'task_execution', 'ownership_changes', 'policy_changes'}


def parse_simple_yaml(text):
    data = {}
    stack = [(-1, data)]
    for raw_line in text.splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith('#'):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(' '))
        line = raw_line.strip()
        while stack and indent <= stack[-1][0]:
            stack.pop()
        if line.startswith('- '):
            continue
        if ':' not in line:
            continue
        key, value = line.split(':', 1)
        key = key.strip()
        value = value.strip()
        parent = stack[-1][1]
        if value == '':
            parent[key] = {}
            stack.append((indent, parent[key]))
        else:
            parent[key] = value
    return data


def validate_visibility(path: Path):
    data = parse_simple_yaml(path.read_text(encoding='utf-8', errors='ignore'))
    errs = []
    levels = set(data.get('levels', {}).keys())
    missing = REQUIRED_VISIBILITY - levels
    if missing:
        errs.append(f'missing visibility levels: {sorted(missing)}')
    if data.get('promotion_requires_decision_record') != 'true':
        errs.append('promotion_requires_decision_record should be true')
    return errs


def validate_roles(path: Path):
    data = parse_simple_yaml(path.read_text(encoding='utf-8', errors='ignore'))
    errs = []
    roles = set(data.get('roles', {}).keys())
    missing = REQUIRED_ROLES - roles
    if missing:
        errs.append(f'missing roles: {sorted(missing)}')
    human = data.get('roles', {}).get('human-approver', {})
    if human.get('can_approve') != 'true':
        errs.append('human-approver must have can_approve: true')
    constraints = data.get('constraints', {})
    if constraints.get('security_reviewer_required_for_high_risk') == 'true' and 'security-reviewer' not in roles:
        errs.append('security-reviewer role required for high risk but missing')
    return errs


def validate_approval(path: Path):
    data = parse_simple_yaml(path.read_text(encoding='utf-8', errors='ignore'))
    errs = []
    rules = set(data.get('approval_rules', {}).keys())
    missing = REQUIRED_APPROVAL_KEYS - rules
    if missing:
        errs.append(f'missing approval rule groups: {sorted(missing)}')
    task_exec = data.get('approval_rules', {}).get('task_execution', {})
    if task_exec.get('high_risk') != 'human-approval':
        errs.append('high_risk task execution must be human-approval')
    if task_exec.get('medium_risk') != 'human-approval':
        errs.append('medium_risk task execution should default to human-approval')
    req = data.get('claimable_requirements', {})
    if req.get('risk_level_must_be') != 'low':
        errs.append('claimable_requirements.risk_level_must_be should be low')
    if req.get('explicit_mode_required') != 'true':
        errs.append('claimable_requirements.explicit_mode_required should be true')
    return errs


def main():
    parser = argparse.ArgumentParser(description='Validate a ClawColab policy bundle.')
    parser.add_argument('visibility_policy')
    parser.add_argument('role_policy')
    parser.add_argument('approval_policy')
    args = parser.parse_args()
    checks = [
        (Path(args.visibility_policy), validate_visibility),
        (Path(args.role_policy), validate_roles),
        (Path(args.approval_policy), validate_approval),
    ]
    failed = False
    for path, func in checks:
        if not path.exists():
            print(f'FAIL {path}\n  - file does not exist')
            failed = True
            continue
        errs = func(path)
        if errs:
            failed = True
            print(f'FAIL {path}')
            for err in errs:
                print(f'  - {err}')
        else:
            print(f'OK   {path}')
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
