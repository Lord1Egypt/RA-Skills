#!/usr/bin/env python3
"""Run *explicitly approved* project checks, fail closed on missing checks.

No third-party libraries. The runner is NOT a sandbox; only enable scripts reviewed
for safety in an environment without production credentials.
"""
from __future__ import annotations
import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path


def fail(message, code=2):
    print(f'{"BLOCKED" if code == 2 else "FAIL"}: {message}',file=sys.stderr)
    return code

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', help='Path to checks.json (default: next to this file)')
    parser.add_argument('--dry-run',action='store_true',help='Show enabled commands; never run them')
    parser.add_argument('--timeout',type=int,default=180,help='Max seconds per command (1..900)')
    args=parser.parse_args(argv)
    if not 1<=args.timeout<=900: return fail('timeout must be within 1..900')
    base=Path(__file__).resolve().parent
    config=Path(args.config) if args.config else base/'checks.json'
    if config.is_symlink():return fail('symlinked config is not permitted')
    try:
        data=json.loads(config.read_text(encoding='utf-8'))
    except (OSError,ValueError) as e:
        return fail('cannot load checks.json: '+str(e))
    if data.get('schema')!=1 or not isinstance(data.get('checks'),list):
        return fail('invalid checks.json schema')
    if config.parent.name=='ai-sdlc' and config.parent.parent.name=='scripts':
        root=config.parent.parent.parent
    else:
        root=Path.cwd()
    enabled=[]
    for c in data['checks']:
        if not isinstance(c,dict) or type(c.get('enabled')) is not bool:
            return fail('each check needs a boolean enabled field')
        if not c['enabled']: continue
        argv=c.get('argv')
        if not isinstance(argv,list) or not argv or any(not isinstance(x,str) or not x.strip() or '\x00' in x for x in argv):
            return fail('enabled check requires a nonempty argv list')
        # Explicit argv with shell=False prevents the implicit shell from handling pipes/redirections.
        # This intentionally does NOT prove scripts are safe; inspect package scripts first.
        if argv[0] in {'sh','bash','zsh','fish','curl','wget','rm','sudo','ssh','scp','docker','kubectl'}:
            return fail('unsafe launcher refused: '+argv[0])
        enabled.append((str(c.get('name','unnamed')),argv))
    if not enabled:
        return fail('no verified enabled project checks; refusing false-green')
    if args.dry_run:
        print(json.dumps({'status':'NOT RUN','commands':[{'name':n,'argv':a} for n,a in enabled]},ensure_ascii=False,indent=2))
        return 0
    failures=[]
    for name,argv in enabled:
        start=time.monotonic()
        try:
            # Output captured, never replayed automatically; may contain credentials.
            proc=subprocess.run(argv,cwd=str(root),stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=args.timeout,check=False)
            status='PASS' if proc.returncode==0 else 'FAIL'
            rc=proc.returncode
            if rc: failures.append(name)
        except (FileNotFoundError,PermissionError) as exc:
            status='BLOCKED';rc=127;failures.append(name)
        except subprocess.TimeoutExpired:
            status='FAIL';rc=124;failures.append(name)
        print(json.dumps({'check':name,'command':argv,'status':status,'exit_code':rc,
                          'elapsed_s':round(time.monotonic()-start,3),
                          'note':'stdout/stderr intentionally suppressed to avoid leaking secrets'},ensure_ascii=False))
    return 1 if failures else 0
if __name__=='__main__':sys.exit(main())
