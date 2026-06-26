#!/usr/bin/env python3
import argparse
import hashlib
import os
import re
import subprocess
import sys
from pathlib import Path

IGNORE = {'.DS_Store'}
SKIP_PARTS = {'.git', '.clawhub', '__pycache__'}


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, (p.stdout + p.stderr).strip()


def local_files(skill_dir: Path):
    out = {}
    for path in skill_dir.rglob('*'):
        if not path.is_file() or path.name in IGNORE or any(part in SKIP_PARTS for part in path.parts):
            continue
        rel = str(path.relative_to(skill_dir))
        data = path.read_bytes()
        out[rel] = hashlib.sha256(data).hexdigest()
    return out


def published_files(slug: str):
    rc, out = run(['clawhub', 'inspect', slug, '--files'])
    if rc != 0:
        raise RuntimeError(out)
    files = {}
    in_files = False
    for line in out.splitlines():
        if line.strip() == 'Files:':
            in_files = True
            continue
        if not in_files or not line.strip():
            continue
        m = re.match(r'^(\S+)\s+\S+\s+([0-9a-f]{64})\s+', line.strip())
        if m:
            files[m.group(1)] = m.group(2)
    return files


def main():
    ap = argparse.ArgumentParser(description='Compare local skill contents to latest published version')
    ap.add_argument('skill_dir')
    ap.add_argument('slug')
    args = ap.parse_args()

    skill_dir = Path(os.path.expanduser(args.skill_dir)).resolve()
    local = local_files(skill_dir)
    remote = published_files(args.slug)

    only_local = sorted(set(local) - set(remote))
    only_remote = sorted(set(remote) - set(local))
    changed = sorted(p for p in set(local) & set(remote) if local[p] != remote[p])

    print(f'Local files: {len(local)}')
    print(f'Published files: {len(remote)}')
    if not only_local and not only_remote and not changed:
        print('Verdict: no-material-diff')
        print('Meaning: local skill matches latest published contents exactly; publishing again is probably unnecessary.')
    else:
        print('Verdict: changed')
        if changed:
            print('Changed files:')
            for p in changed:
                print(f'- {p}')
        if only_local:
            print('New local files:')
            for p in only_local:
                print(f'- {p}')
        if only_remote:
            print('Published-only files:')
            for p in only_remote:
                print(f'- {p}')


if __name__ == '__main__':
    main()
