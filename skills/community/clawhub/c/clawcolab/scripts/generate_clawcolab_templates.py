#!/usr/bin/env python3
import argparse
import shutil
from pathlib import Path

FILES = {
    'assets/task-template.yaml': 'workspace/tasks/TASK-001.yaml',
    'assets/proposal-template.md': 'workspace/proposals/PROPOSAL-001.md',
    'assets/decision-template.md': 'workspace/decisions/DECISION-001.md',
    'assets/handoff-template.md': 'workspace/handoffs/HANDOFF-001.md',
    'assets/risk-template.md': 'workspace/risks/RISK-001.md',
    'assets/claim-template.yaml': 'workspace/claims/CLAIM-001.yaml',
    'assets/visibility-policy-template.yaml': 'workspace/policy/visibility-policy.yaml',
    'assets/role-policy-template.yaml': 'workspace/policy/role-policy.yaml',
    'assets/approval-policy-template.yaml': 'workspace/policy/approval-policy.yaml',
}


def main():
    parser = argparse.ArgumentParser(description='Generate a sample ClawColab repository structure from bundled templates.')
    parser.add_argument('destination', help='Destination directory')
    args = parser.parse_args()

    skill_dir = Path(__file__).resolve().parent.parent
    dest = Path(args.destination).resolve()
    dest.mkdir(parents=True, exist_ok=True)
    (dest / 'sealed').mkdir(exist_ok=True)

    for src_rel, dest_rel in FILES.items():
        src = skill_dir / src_rel
        out = dest / dest_rel
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, out)
        print(f'WROTE {out}')

    index = dest / 'sealed' / 'INDEX.md'
    if not index.exists():
        index.write_text('- id: sealed-001\n  title: Example sealed reference\n  owner: replace-me\n  summary: Replace with a summary-only sealed note.\n  status: exists\n', encoding='utf-8')
        print(f'WROTE {index}')


if __name__ == '__main__':
    main()
