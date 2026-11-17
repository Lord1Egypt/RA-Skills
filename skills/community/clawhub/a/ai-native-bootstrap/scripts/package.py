#!/usr/bin/env python3
"""Reproducibly archive the curated Skill directory, excluding caches and local data."""
from __future__ import annotations
import argparse
import hashlib
import sys
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
TOP={'SKILL.md','README.md','ACCEPTANCE.md'}
FOLDERS={'agents','references','scripts','templates','tests'}
BAN={'__pycache__','.DS_Store','.pytest_cache','.git'}

def contents():
    out=[]
    for p in ROOT.rglob('*'):
        r=p.relative_to(ROOT)
        if any(x in BAN or x.startswith('.') for x in r.parts):continue
        if len(r.parts)==1 and p.name not in TOP:continue
        if len(r.parts)>1 and r.parts[0] not in FOLDERS:continue
        if p.is_symlink():raise ValueError('symlink refused: '+str(r))
        if p.is_file() and p.suffix!='.pyc':out.append((p,r))
    return sorted(out,key=lambda p:str(p[1]))

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('output',help='Output .zip path')
    a=ap.parse_args()
    out=Path(a.output).absolute()
    if out.suffix!='.zip':raise SystemExit('Output must be .zip')
    members=contents()
    if not any(str(r)=='SKILL.md' for _,r in members):raise SystemExit('No SKILL.md')
    out.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for src,rel in members:
            dest='ai-native-bootstrap/'+rel.as_posix()
            info=zipfile.ZipInfo(dest,(2026,11,13,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=(0o100644 << 16)
            z.writestr(info,src.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
    sha=hashlib.sha256(out.read_bytes()).hexdigest()
    print(f'CREATED {out} files={len(members)} bytes={out.stat().st_size} sha256={sha}')
    return 0
if __name__=='__main__':sys.exit(main())
