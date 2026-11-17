#!/usr/bin/env python3
"""Safe opt-in AI-native SDLC repository bootstrap (Python 3.9+, stdlib)."""
from __future__ import annotations
import argparse
import json
import os
import tempfile
import sys
from pathlib import Path
from _core import (VERSION, MANIFEST_FILE, Blocked, safe_project, safe_destination, repo_facts,
                   evidence, ensure_writable, candidates, stamp, digest, json_dump, write_new, rollback)

BASE = Path(__file__).resolve().parent.parent
TEMPLATES = BASE / 'templates'
ALL = {'codex','claude','opencode'}

def audit_text(f):
    git = f['git']
    fmt=lambda x: ', '.join(x) if x else 'NONE OBSERVED'
    cases=f['candidates']
    return (f'# AI-Native SDLC read-only repository audit\n\n'
        f'- Generated (UTC): {stamp()}\n- Target: `{f["root"]}`\n'
        f'- Git state: {git["status"]}; branch: `{git["branch"] or "NONE"}`; HEAD: `{git["head"] or "NONE"}`\n'
        f'- Git repository root: `{git["repo_root"] or "NONE"}`\n'
        f'- Stack indicators (filenames only): {fmt(f["indicators"])}\n'
        f'- Existing policies (filenames only): {fmt(f["policy"])}\n'
        f'- CI indicator paths: {fmt(f["ci"])}\n'
        f'- Detected candidate check names: {fmt([c["name"] for c in cases])}\n'
        '- Check commands: **UNVERIFIED** (manifest or file existence does not prove safety or success).\n'
        '- Remote branch protection/release gate: **UNVERIFIED**; not inspected.\n'
        '- Secrets: **NOT READ**; no .env/private key/credential contents accessed.\n\n'
        '## Required follow-through\n\n'
        '- [ ] Inspect repository-specific policy and resolve authority conflicts.\n'
        '- [ ] Review candidate script bodies, network and production dependencies before enabling checks.\n'
        '- [ ] Run real tests and capture return codes; add at least one authentic regression.\n'
        '- [ ] Verify actual CI runs and remote/production permissions separately.\n'
        '- [ ] Obtain separate human approvals for R2/R3 actions.\n\n'
        'Bootstrap alone is CONDITIONAL, not proof of production readiness.\n')

def checks_data(f):
    return {'schema':1, 'notes':'Candidates are unverified and disabled. Inspect actual scripts, dependencies, credentials and environment before enabling. Never infer PASS from this file.', 'checks':f['candidates']}

def target_files(root, adapter, facts):
    policies = set(facts['policy'])
    policy = 'AGENTS.md' if 'AGENTS.md' in policies else ('CLAUDE.md' if 'CLAUDE.md' in policies else 'AGENTS.md')
    templates = {
      'docs/ai-sdlc/README.md': 'README.md',
      'docs/ai-sdlc/templates/intent.md':'intent.md',
      'docs/ai-sdlc/templates/spec.md':'spec.md',
      'docs/ai-sdlc/templates/plan.md':'plan.md',
      'docs/ai-sdlc/templates/acceptance.md':'acceptance.md',
      'docs/ai-sdlc/eval-plan.md':'eval-plan.md',
      'evals/cases.json':'eval-cases.json',
      'docs/ai-sdlc/acceptance-report.md':'acceptance-report.md',
    }
    out={x:(TEMPLATES/y).read_bytes() for x,y in templates.items()}
    out['docs/ai-sdlc/audit.md']=audit_text(facts).encode('utf-8')
    out['scripts/ai-sdlc/checks.json']=json_dump(checks_data(facts))
    out['scripts/ai-sdlc/check.py']=(BASE/'scripts/check_runner.py').read_bytes()
    out['scripts/ai-sdlc/eval.py']=(BASE/'scripts/eval_runner.py').read_bytes()
    if policy == 'AGENTS.md':
        if 'AGENTS.md' not in policies:
            out['AGENTS.md']=(TEMPLATES/'AGENTS.md').read_bytes()
        if ('claude' in adapter or 'all' in adapter) and 'CLAUDE.md' not in policies:
            out['CLAUDE.md']=(TEMPLATES/'CLAUDE.md').read_bytes()
    else:
        # Existing CLAUDE.md remains authoritative; Codex/OpenCode point to it, no duplicated rules.
        if 'AGENTS.md' not in policies and any(x in adapter for x in ('codex','opencode','all')):
            out['AGENTS.md']=('# Repository agent policy adapter\n\nRead `CLAUDE.md` as the existing canonical project policy, and `docs/ai-sdlc/README.md` for the SDLC record formats. Do not duplicate or override those rules here.\n').encode('utf-8')
    out['docs/ai-sdlc/README.md']=out['docs/ai-sdlc/README.md'].replace(b'`AGENTS.md` if created by bootstrap',f'`{policy}` (existing or bootstrap-created)'.encode())
    return out

def manifest(root, files, facts):
    return json_dump({'schema':1, 'tool':'ai-native-bootstrap', 'version':VERSION,
           'created_utc':stamp(),'source_git_head':facts['git']['head'],
           'created_files':{r:digest(d) for r,d in sorted(files.items())},
           'warnings':['Bootstrapping is CONDITIONAL until real checks, regression cases, CI and server-side permissions are verified.']})

def command_plan(root, adapter, upgrade=False):
    f=evidence(root)
    desired=target_files(root, adapter, f)
    blocked=[]; preserved=[]; writable=[]
    for rel,content in sorted(desired.items()):
        try:
            p=safe_destination(root,rel)
            if p.exists(): preserved.append(rel)
            else: writable.append(rel)
        except Blocked as exc: blocked.append(str(exc))
    try: safe_destination(root,MANIFEST_FILE)
    except Blocked as exc: blocked.append(str(exc))
    if (root/MANIFEST_FILE).exists():
        if not upgrade:
            blocked.append('existing bootstrap manifest; use verify or explicit --upgrade')
        else:
            try:
                prior=do_verify(root)
                if prior['drift']: blocked.append('existing managed-file drift: '+', '.join(prior['drift']))
            except Blocked as exc: blocked.append('invalid prior manifest: '+str(exc))
    state=f['git']
    return f,desired,{'root':str(root),'adapter':adapter,'upgrade':upgrade,'git':state,'create':writable+[MANIFEST_FILE], 'preserve':preserved,'blockers':blocked,
        'note':'DRY RUN: no files written; check candidates unverified and disabled. R2/R3 not authorized.'}

def do_init(root, adapter, upgrade=False):
    ensure_writable(root)
    f,desired,p=command_plan(root,adapter,upgrade)
    if p['blockers']:
        raise Blocked('; '.join(p['blockers']))
    files={k:v for k,v in desired.items() if not (root/k).exists()}
    existing_manifest=(root/MANIFEST_FILE).exists()
    prior={}
    if existing_manifest:
        prior=json.loads((root/MANIFEST_FILE).read_text(encoding='utf-8'))['created_files']
    new_entries={**prior,**{r:digest(data) for r,data in files.items()}}
    content=json_dump({'schema':1,'tool':'ai-native-bootstrap','version':VERSION,
          'created_utc':stamp(),'source_git_head':f['git']['head'],
          'created_files':dict(sorted(new_entries.items())),
          'warnings':['Only structural presence and integrity are verified; project acceptance requires real checks and external controls.']})
    created=[];dirs=[]
    try:
        for k,v in sorted(files.items()):
            write_new(root,k,v,created,dirs)
        if existing_manifest:
            if files:
                # Replace only our own verified manifest atomically. Existing policies remain untouched.
                parent=(root/MANIFEST_FILE).parent
                fd,tmp=tempfile.mkstemp(prefix='.ai-native-manifest-',suffix='.tmp',dir=str(parent))
                try:
                    with os.fdopen(fd,'wb') as w:w.write(content)
                    os.replace(tmp,str(root/MANIFEST_FILE))
                finally:
                    if os.path.exists(tmp):os.unlink(tmp)
        else:
            write_new(root,MANIFEST_FILE,content,created,dirs)
    except Exception:
        rollback(created,dirs)
        raise
    return {'status':'CONDITIONAL','mode':'UPGRADE' if existing_manifest else 'INITIALIZED',
            'created':sorted(files) + ([] if existing_manifest else [MANIFEST_FILE]),'preserved':p['preserve'],
            'next':['Review checks.json command candidates and their safety',
                    'Enable verified real checks and execute check.py',
                    'Add a genuine historical regression and verify CI/release permissions',
                    'Run bootstrap.py verify (structural only)'],
            'note':'No business code, dependency, production, network, CI or remote operations were performed.'}

def do_verify(root):
    p=safe_destination(root,MANIFEST_FILE)
    if not p.is_file(): raise Blocked('no bootstrap manifest found')
    try: m=json.loads(p.read_text(encoding='utf-8'))
    except (OSError,ValueError) as exc: raise Blocked('bad bootstrap manifest: '+str(exc))
    if m.get('schema')!=1 or m.get('tool')!='ai-native-bootstrap' or not isinstance(m.get('created_files'),dict):
        raise Blocked('unrecognized manifest schema')
    drift=[]
    for r,d in m['created_files'].items():
        t=safe_destination(root,r)
        if not t.is_file() or digest(t.read_bytes())!=d:
            drift.append(r)
    return {'manifest_version':m['version'],'files_checked':len(m['created_files']),
            'drift':drift,'structural':'PASS' if not drift else 'FAIL',
            'project_acceptance':'CONDITIONAL: structural hashes do not establish real tests/CI/production safety'}

def main(argv=None):
    pa=argparse.ArgumentParser(description=__doc__)
    pa.add_argument('command',choices=['audit','plan','init','verify'])
    pa.add_argument('--project',required=True)
    pa.add_argument('--adapter', choices=['all','codex','claude','opencode'],default='all')
    pa.add_argument('--apply', action='store_true',help='Required to write; no writes by default')
    pa.add_argument('--upgrade',action='store_true',help='On init: add missing files only after prior manifest verifies; never overwrite project files')
    ns=pa.parse_args(argv)
    try:
        root=safe_project(ns.project)
        if ns.command=='audit':
            print(audit_text(evidence(root)),end='')
        elif ns.command=='plan' or (ns.command=='init' and not ns.apply):
            print(json.dumps(command_plan(root,ns.adapter,ns.upgrade)[2],indent=2,ensure_ascii=False))
        elif ns.command=='init':
            print(json.dumps(do_init(root,ns.adapter,ns.upgrade),indent=2,ensure_ascii=False))
        else:
            result=do_verify(root); print(json.dumps(result,indent=2,ensure_ascii=False))
            if result['drift']:return 1
        return 0
    except Blocked as exc:
        print('BLOCKED: '+str(exc), file=sys.stderr)
        return 2
    except (OSError,ValueError) as exc:
        print('FAIL: '+str(exc), file=sys.stderr)
        return 1
if __name__=='__main__': sys.exit(main())
