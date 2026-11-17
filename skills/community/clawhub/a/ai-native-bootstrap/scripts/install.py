#!/usr/bin/env python3
"""Install ai-native-bootstrap skill with preview, collision checks and safe backup."""
from __future__ import annotations
import argparse
import json
import os
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from _core import (SKILL_NAME,VERSION,Blocked, safe_project,refuse_symlink_components,
    digest,json_dump,ensure_writable)

SOURCE=Path(__file__).resolve().parent.parent
# Keep the install payload lean; never bundle caches, arbitrary local data, or credentials.
TOP={'SKILL.md','README.md','ACCEPTANCE.md'}
DIRS={'agents','references','scripts','templates','tests'}
EXCLUDE={'__pycache__','.DS_Store'}

def payload():
    files={}
    for f in sorted(SOURCE.rglob('*')):
        rel=f.relative_to(SOURCE)
        if any(x in EXCLUDE or x.startswith('.') for x in rel.parts): continue
        if len(rel.parts)==1 and f.name not in TOP:continue
        if len(rel.parts)>1 and rel.parts[0] not in DIRS:continue
        if f.is_symlink():raise Blocked('source skill contains symlink: '+str(rel))
        if f.is_file():
            if f.stat().st_size>1_000_000:raise Blocked('oversize source file: '+str(rel))
            files[str(rel)]=f.read_bytes()
    if 'SKILL.md' not in files:raise Blocked('missing SKILL.md')
    return files

def destination(agent,scope,project,home):
    if scope=='user':
        root=refuse_symlink_components(Path(home or Path.home()))
        return root / {'codex':'.agents/skills','claude':'.claude/skills','opencode':'.config/opencode/skills'}[agent] / SKILL_NAME
    if not project:raise Blocked('--project is required for project scope')
    root=safe_project(project)
    return root / {'codex':'.agents/skills','claude':'.claude/skills','opencode':'.opencode/skills'}[agent] / SKILL_NAME

def check_install_manifest(target):
    manifest=target/'install-manifest.json'
    if not manifest.is_file() or manifest.is_symlink(): raise Blocked('existing install has no valid install manifest; refuse upgrade')
    try: data=json.loads(manifest.read_text('utf-8'))
    except (ValueError,OSError):raise Blocked('cannot parse install manifest')
    if data.get('tool')!=SKILL_NAME or not isinstance(data.get('files'),dict):raise Blocked('invalid install manifest')
    for relative, sha in data['files'].items():
        p=target/relative
        if not p.is_file() or p.is_symlink() or digest(p.read_bytes())!=sha:
            raise Blocked('installed file has local modifications; refuse overwrite: '+relative)
    extra=[]
    known=set(data['files'])|{'install-manifest.json'}
    for p in target.rglob('*'):
        if p.is_symlink():raise Blocked('installed folder contains symlink')
        if p.is_file() and not ('__pycache__' in p.parts or p.suffix=='.pyc') and str(p.relative_to(target)) not in known:extra.append(str(p.relative_to(target)))
    if extra:raise Blocked('installed folder has untracked files; refuse upgrade: '+', '.join(extra[:5]))

def install(target, upgrade, files):
    target=refuse_symlink_components(target)
    parent=target.parent
    if target.exists() and not upgrade:raise Blocked('already installed; use --upgrade only if replacement is intended')
    if target.exists() and not target.is_dir():raise Blocked('target is not a directory')
    if upgrade and target.exists():check_install_manifest(target)
    parent.mkdir(parents=True, exist_ok=True)
    stage=Path(tempfile.mkdtemp(prefix='.ai-native-bootstrap-stage-',dir=parent))
    backup=None
    try:
        for name,body in files.items():
            dest=stage/name; dest.parent.mkdir(parents=True, exist_ok=True);dest.write_bytes(body)
        (stage/'install-manifest.json').write_bytes(json_dump({'tool':SKILL_NAME,'version':VERSION,
             'files':{n:digest(d) for n,d in files.items()}}))
        if target.exists():
            serial=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
            backup=parent/(SKILL_NAME+'.backup-'+serial)
            if backup.exists():raise Blocked('backup folder collision: '+str(backup))
            target.rename(backup)
        try:
            stage.rename(target)
        except Exception:
            if backup is not None and backup.exists():backup.rename(target)
            raise
    finally:
        if stage.exists():shutil.rmtree(stage)
    return backup

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--agent',choices=['codex','claude','opencode'],required=True)
    p.add_argument('--scope',choices=['user','project'],default='user')
    p.add_argument('--project')
    p.add_argument('--home',help='Optional alternate home for reproducible tests')
    p.add_argument('--apply',action='store_true')
    p.add_argument('--upgrade',action='store_true')
    a=p.parse_args(argv)
    try:
        target=destination(a.agent,a.scope,a.project,a.home)
        files=payload()
        info={'agent':a.agent,'scope':a.scope,'target':str(target),'files':sorted(files),
              'existing':target.exists(),'mode':'APPLY' if a.apply else 'PREVIEW'}
        if not a.apply:
            print(json.dumps(info,ensure_ascii=False,indent=2));return 0
        if a.scope=='project':ensure_writable(safe_project(a.project))
        backup=install(target,a.upgrade,files)
        print(json.dumps({'status':'INSTALLED','path':str(target),'previous_backup':str(backup) if backup else None,
                         'next':'Restart your agent session and check actual skill discovery; no project bootstrapping was performed.'},indent=2))
        return 0
    except Blocked as ex:
        print('BLOCKED: '+str(ex),file=sys.stderr);return 2
    except OSError as ex:
        print('FAIL: '+str(ex),file=sys.stderr);return 1
if __name__=='__main__':sys.exit(main())
