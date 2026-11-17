"""Shared filesystem, manifest and repository helpers for ai-native-bootstrap.
Python 3.9+; standard library only. Never executes application commands.
"""
from __future__ import annotations
import hashlib
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path

VERSION = '1.0.0'
SKILL_NAME = 'ai-native-bootstrap'
MANIFEST_FILE = 'docs/ai-sdlc/bootstrap-manifest.json'
BAD_BRANCHES = {'main', 'master', 'trunk'}

class Blocked(Exception):
    pass

def stamp():
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def refuse_symlink_components(path: Path):
    """Reject a symlinked target, but tolerate OS-level symlink ancestors.

    macOS ships /var -> /private/var and /tmp -> /private/tmp as system links;
    tempfile workspaces and CI checkouts routinely live below them. Walking every
    ancestor rejected those legitimate roots and made bootstrap unusable on macOS.
    Escape protection for user-controlled paths is enforced by safe_destination()
    (checks every component from the destination up to the project root) together
    with exclusive 'xb' writes in write_new().
    """
    absolute = Path(os.path.abspath(os.path.expanduser(str(path))))
    if absolute.is_symlink():
        raise Blocked('symlink path component is not allowed: ' + str(absolute))
    return absolute

def safe_project(path: str):
    p = refuse_symlink_components(Path(path))
    if not p.exists() or not p.is_dir():
        raise Blocked('project directory does not exist: ' + str(p))
    return p

def safe_destination(base: Path, relative: str):
    rel = Path(relative)
    if rel.is_absolute() or not relative or '..' in rel.parts or '\x00' in relative:
        raise Blocked('unsafe destination path: ' + repr(relative))
    out = base / rel
    if not out.is_relative_to(base):
        raise Blocked('destination escapes project')
    for item in (out, *out.parents):
        if item == base.parent:
            break
        if item.is_symlink():
            raise Blocked('symlink in destination path: ' + str(item))
    if out.exists() and not out.is_file():
        raise Blocked('destination exists but is not a file: ' + str(out))
    return out

def git(root: Path, *args):
    try:
        p = subprocess.run(['git', '-C', str(root), *args], capture_output=True, text=True, timeout=10, check=False)
        return p.returncode, p.stdout.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return 127, ''

def repo_facts(root: Path):
    rc, reporoot = git(root, 'rev-parse', '--show-toplevel')
    if rc != 0:
        return {'git': False, 'branch': None, 'head': None, 'clean': None, 'repo_root': None, 'status': 'NO_GIT'}
    rc2, branch = git(root, 'symbolic-ref', '--quiet', '--short', 'HEAD')
    _, head = git(root, 'rev-parse', 'HEAD')
    rc3, status = git(root, 'status', '--porcelain', '--untracked-files=all')
    return {'git': True, 'branch': branch if rc2 == 0 else 'DETACHED', 'head': head,
            'clean': rc3 == 0 and status == '', 'repo_root': str(Path(reporoot).resolve()),
            'status': 'CLEAN' if rc3 == 0 and not status else 'DIRTY_OR_UNKNOWN'}

def existing_policy(root: Path):
    found = [x for x in ('AGENTS.md', 'CLAUDE.md', 'CONTRIBUTING.md', '.cursorrules', '.github/copilot-instructions.md') if (root / x).exists()]
    if (root/'.agents').is_dir(): found.append('.agents/')
    if (root/'.claude').is_dir(): found.append('.claude/')
    if (root/'.opencode').is_dir(): found.append('.opencode/')
    return found

def candidates(root: Path):
    """Report *untrusted* candidates. Read manifest only, never execute scripts."""
    out = []
    pkg = root / 'package.json'
    if pkg.is_file() and not pkg.is_symlink() and pkg.stat().st_size < 250_000:
        try:
            scripts = json.loads(pkg.read_text(encoding='utf-8')).get('scripts', {})
            if isinstance(scripts, dict):
                runner = 'npm'
                if (root/'pnpm-lock.yaml').is_file(): runner = 'pnpm'
                elif (root/'yarn.lock').is_file(): runner = 'yarn'
                elif (root/'bun.lockb').is_file() or (root/'bun.lock').is_file(): runner = 'bun'
                for name in ('lint','typecheck','test','check','build'):
                    if isinstance(scripts.get(name),str):
                        out.append({'name':name,'argv':[runner,'run',name],'enabled':False,'source':'package.json scripts (UNVERIFIED)'})
        except (ValueError,UnicodeError,OSError):
            pass
    if (root/'pyproject.toml').is_file() or (root/'pytest.ini').is_file():
        out.append({'name':'python-tests','argv':['python3','-m','pytest'],'enabled':False,'source':'Python config detected (UNVERIFIED)'})
    if (root/'go.mod').is_file():
        out.append({'name':'go-tests','argv':['go','test','./...'],'enabled':False,'source':'go.mod (UNVERIFIED)'})
    if (root/'Cargo.toml').is_file():
        out.append({'name':'cargo-tests','argv':['cargo','test'],'enabled':False,'source':'Cargo.toml (UNVERIFIED)'})
    return out

def evidence(root: Path):
    tech = [n for n in ('package.json','pnpm-lock.yaml','package-lock.json','yarn.lock','bun.lock','pyproject.toml','requirements.txt','go.mod','Cargo.toml','Gemfile','pom.xml','Dockerfile','docker-compose.yml') if (root/n).is_file()]
    ci = [x for x in ('.github/workflows','.gitlab-ci.yml','Jenkinsfile','azure-pipelines.yml','.circleci/config.yml') if (root/x).exists()]
    return {'root': str(root), 'git':repo_facts(root), 'indicators':tech, 'policy':existing_policy(root), 'ci':ci, 'candidates':candidates(root)}

def ensure_writable(root: Path):
    f = repo_facts(root)
    if f['git']:
        # git resolves OS-level symlinks (macOS: /var -> /private/var) while
        # safe_project keeps the user-supplied absolute path. Compare canonical
        # forms so a legitimate temp/CI workspace is not mistaken for a subdir.
        if Path(f['repo_root']).resolve() != root.resolve():
            raise Blocked('project is not the Git repository root; run against repository root')
        if not f['clean']:
            raise Blocked('dirty Git worktree: create a clean worktree/branch, preserving changes')
        if f['branch'] in BAD_BRANCHES or f['branch'] == 'DETACHED':
            raise Blocked('protected/default or detached Git branch: '+str(f['branch']))
    elif any(root.iterdir()):
        raise Blocked('existing non-Git project; establish version control/isolation before writing')
    return f

def write_new(base: Path, relative: str, contents: bytes, created_files: list, made_dirs: list):
    dest = safe_destination(base, relative)
    if dest.exists():
        raise Blocked('refusing to overwrite existing file: '+relative)
    missing = []
    p = dest.parent
    while not p.exists() and p != base:
        missing.append(p)
        p = p.parent
    for d in reversed(missing):
        d.mkdir(mode=0o755)
        made_dirs.append(d)
    with dest.open('xb') as w:
        w.write(contents)
    created_files.append(dest)


def rollback(created_files, made_dirs):
    for p in reversed(created_files):
        try: p.unlink()
        except OSError: pass
    for p in reversed(made_dirs):
        try: p.rmdir()
        except OSError: pass

def json_dump(obj):
    return (json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True)+'\n').encode('utf-8')
