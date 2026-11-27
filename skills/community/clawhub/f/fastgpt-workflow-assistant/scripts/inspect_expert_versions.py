#!/usr/bin/env python3
"""Read expert/embedded skill version evidence, including hidden plugin metadata; never execute input code."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import zipfile


def inspect(path: Path) -> dict:
    if path.is_dir():
        # Only metadata is read; listing includes dot-directories on all platforms.
        files = {}
        for p in path.rglob('*'):
            if p.is_file() and not p.is_symlink() and p.name in ('plugin.json', 'skill-version.json', 'SKILL.md'):
                resolved = p.resolve()
                if resolved.is_relative_to(path.resolve()):
                    files[p.relative_to(path).as_posix()] = p.read_bytes()
        archive_sha = None
    else:
        with zipfile.ZipFile(path) as z:
            files = {}
            for item in z.infolist():
                name = item.filename
                if item.is_dir():
                    continue
                if name.startswith('/') or '\\' in name or ':' in name or '..' in name.split('/'):
                    raise ValueError('Unsafe archive path')
                if name in files:
                    raise ValueError('Duplicate archive metadata')
                if PurePosixPath(name).name in ('plugin.json', 'skill-version.json', 'SKILL.md'):
                    if item.file_size > 2_000_000 or len(files) >= 500:
                        raise ValueError('Metadata inspection size limit exceeded')
                    files[name] = z.read(item)
        archive_sha = hashlib.sha256(path.read_bytes()).hexdigest()
    plugins, skills = [], []
    for name, data in sorted(files.items()):
        if name.endswith('/.codebuddy-plugin/plugin.json') or name == '.codebuddy-plugin/plugin.json':
            c = json.loads(data.decode('utf-8-sig'))
            plugins.append({'file': name, 'name': c.get('name'), 'expert_version': c.get('version'),
                            'declared_skills': c.get('skills', []), 'sha256': hashlib.sha256(data).hexdigest()})
        if name.endswith('assets/skill-version.json'):
            c = json.loads(data.decode('utf-8-sig'))
            prefix = name[:-len('assets/skill-version.json')]
            skills.append({'file': name, 'name': c.get('skill_name', c.get('name')),
                           'skill_version': c.get('version'), 'local_revision': c.get('local_revision'), 'build_id': c.get('build_id'), 'skill_entry_present': prefix + 'SKILL.md' in files,
                           'sha256': hashlib.sha256(data).hexdigest()})
    warnings = []
    for p in plugins:
        base = p['file'][:-len('.codebuddy-plugin/plugin.json')]
        for declared in p['declared_skills']:
            if not isinstance(declared, str):
                warnings.append('Invalid declared skill path')
                continue
            clean = declared[2:] if declared.startswith('./') else declared
            if clean.startswith('/') or '..' in clean.split('/') or '\\' in clean or ':' in clean:
                warnings.append('Unsafe declared skill path')
                continue
            expected = base + clean.rstrip('/') + '/assets/skill-version.json'
            if expected not in {s['file'] for s in skills}:
                warnings.append('Declared skill version evidence missing: ' + clean)
    if not plugins:
        warnings.append('No expert plugin metadata found; expert version unknown, not proven absent')
    if not skills:
        warnings.append('No skill-version manifest found; skill version unknown')
    return {'experts': plugins, 'skills': skills, 'warnings': warnings, 'archive_sha256': archive_sha,
            'platform_version': 'unknown', 'marketplace_effective_version': 'not_checked',
            'scope': 'local metadata only; node version and download time do not establish platform or publication version'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path', type=Path)
    args = parser.parse_args()
    try:
        if not args.path.exists():
            raise ValueError('Input does not exist')
        result = inspect(args.path)
    except (OSError, ValueError, zipfile.BadZipFile) as exc:
        print(json.dumps({'status': 'error', 'error_type': type(exc).__name__}))
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
