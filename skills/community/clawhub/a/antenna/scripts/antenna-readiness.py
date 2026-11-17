#!/usr/bin/env python3
"""Read-only native readiness; the same static checks as Doctor, no repairs."""
import argparse, json, os, subprocess, sys
from pathlib import Path
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--json',action='store_true');p.add_argument('--gateway')
    a=p.parse_args();root=Path(__file__).resolve().parents[1]
    host=a.gateway or os.environ.get('OPENCLAW_CONFIG_PATH') or str(Path.home()/'.openclaw/openclaw.json')
    r=subprocess.run(['node',str(root/'plugin/doctor.mjs'),'doctor',host,str(root)],capture_output=True,text=True)
    if a.json: print(r.stdout or r.stderr,end='')
    else:
        try:
            v=json.loads(r.stdout or r.stderr)
            print('Native static checks: '+('passed' if v.get('staticChecksPassed') else 'not passed'))
            print('Live ingress and remote-peer readiness: not verified.')
            for item in v.get('problems',[])+v.get('warnings',[]): print(json.dumps(item))
            if v.get('reason'): print(json.dumps(v['reason']))
        except ValueError: print('Cannot complete native readiness checks.',file=sys.stderr)
    return r.returncode

if __name__=="__main__": sys.exit(main())
