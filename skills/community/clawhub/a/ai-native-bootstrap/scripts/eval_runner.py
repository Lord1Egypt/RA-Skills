#!/usr/bin/env python3
"""Run approved deterministic regression cases (not an LLM judge).

Without authentic source cases the suite fails BLOCKED. Never fabricates results.
"""
from __future__ import annotations
import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--cases',help='JSON cases file; defaults to <project>/evals/cases.json')
    ap.add_argument('--project',help='Project root (defaults to parent of this script scripts/ai-sdlc/)')
    ap.add_argument('--timeout',type=int,default=180)
    a=ap.parse_args(argv)
    default_root=Path(__file__).resolve().parent.parent.parent
    root=Path(a.project).resolve() if a.project else default_root
    cases=Path(a.cases) if a.cases else root/'evals/cases.json'
    if not 1<=a.timeout<=900:print('BLOCKED: invalid timeout',file=sys.stderr);return 2
    if cases.is_symlink():print('BLOCKED: symlinked case file',file=sys.stderr);return 2
    try:d=json.loads(cases.read_text(encoding='utf-8'))
    except (OSError,ValueError) as e:
        print('BLOCKED: invalid case file: '+str(e),file=sys.stderr);return 2
    if d.get('schema')!=1 or not isinstance(d.get('cases'),list):
        print('BLOCKED: invalid case schema',file=sys.stderr);return 2
    enabled=[]
    for c in d['cases']:
        if not isinstance(c,dict) or type(c.get('enabled')) is not bool:
            print('BLOCKED: case needs enabled bool',file=sys.stderr);return 2
        if not c['enabled']:continue
        if c.get('kind')!='deterministic' or not isinstance(c.get('source'),str) or not c['source'].strip():
            print('BLOCKED: deterministic case requires a genuine source reference',file=sys.stderr);return 2
        cmd=c.get('argv')
        if not isinstance(cmd,list) or not cmd or not all(isinstance(x,str) and x.strip() for x in cmd):
            print('BLOCKED: deterministic case needs argv list',file=sys.stderr);return 2
        if cmd[0] in {'bash','sh','zsh','curl','wget','rm','sudo','ssh','scp','docker','kubectl'}:
            print('BLOCKED: untrusted launcher',file=sys.stderr);return 2
        if type(c.get('expected_exit_code')) is not int or not 0<=c['expected_exit_code']<=255:
            print('BLOCKED: explicit expected_exit_code required',file=sys.stderr);return 2
        enabled.append(c)
    if not enabled:
        print('BLOCKED: no enabled real evaluation cases; no synthetic PASS',file=sys.stderr);return 2
    errors=0
    for c in enabled:
        begin=time.monotonic()
        try:
            proc=subprocess.run(c['argv'],cwd=str(root),stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=a.timeout,check=False)
            actual=proc.returncode
        except subprocess.TimeoutExpired:actual=124
        except (FileNotFoundError,PermissionError):actual=127
        status='PASS' if actual==c['expected_exit_code'] else 'FAIL'
        errors+=status=='FAIL'
        print(json.dumps({'id':c.get('id','UNKNOWN'),'source':c['source'],'status':status,
             'expected_exit_code':c['expected_exit_code'],'actual_exit_code':actual,
             'elapsed_s':round(time.monotonic()-begin,3),
             'note':'stdout/stderr suppressed; deterministic check only, no LLM quality claim'},ensure_ascii=False))
    return 1 if errors else 0
if __name__=='__main__':sys.exit(main())
