#!/usr/bin/env python3
"""Static bundle validation; checks structure, Python syntax, source and templates."""
from __future__ import annotations
import hashlib
import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
REQUIRED=[
 'SKILL.md','README.md','ACCEPTANCE.md','agents/openai.yaml',
 'references/implementation-standard.md','references/adapters-and-safety.md',
 'scripts/_core.py','scripts/bootstrap.py','scripts/check_runner.py','scripts/eval_runner.py','scripts/install.py','scripts/validate_bundle.py','scripts/package.py',
 'templates/AGENTS.md','templates/CLAUDE.md','templates/audit.md','templates/README.md',
 'templates/intent.md','templates/spec.md','templates/plan.md','templates/acceptance.md',
 'templates/acceptance-report.md','templates/eval-plan.md','templates/checks.json','templates/eval-cases.json',
 'tests/test_bootstrap.py',
]

def main():
    problems=[]
    for name in REQUIRED:
        p=ROOT/name
        if not p.is_file() or p.is_symlink():problems.append(f'missing/unsafe: {name}')
        elif p.stat().st_size==0:problems.append(f'empty: {name}')
    for p in ROOT.rglob('*'):
        if p.is_symlink():problems.append('symlink: '+str(p.relative_to(ROOT)))
    for p in (ROOT/'scripts').glob('*.py'):
        try:compile(p.read_bytes(),str(p),'exec')
        except (SyntaxError,UnicodeError) as e:problems.append(f'Python syntax: {p.name}: {e}')
    try:
        skill=(ROOT/'SKILL.md').read_text(encoding='utf-8')
        if not skill.startswith('---\n') or 'name: ai-native-bootstrap' not in skill or 'description:' not in skill:
            problems.append('SKILL.md requires name and trigger description')
        checks=json.loads((ROOT/'templates/checks.json').read_text(encoding='utf-8'))
        if checks.get('schema')!=1 or checks.get('checks')!=[]:
            problems.append('checks template must be empty, never pre-enabled')
    except (OSError,ValueError) as e:
        problems.append(str(e))
    result={'status':'PASS' if not problems else 'FAIL','required_files':len(REQUIRED),'problems':problems,
            'note':'Static bundle integrity only; does not assert real project CI, model Evals or release permissions.'}
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 1 if problems else 0
if __name__=='__main__':sys.exit(main())
