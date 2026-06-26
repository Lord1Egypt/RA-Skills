#!/usr/bin/env python3
import argparse
import hashlib
import json
from pathlib import Path

IGNORED_DIRS = {'.git', '__pycache__', '.DS_Store'}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def collect_skill(skill_dir: Path) -> dict:
    files = []
    for file_path in sorted(p for p in skill_dir.rglob('*') if p.is_file()):
        rel_parts = file_path.relative_to(skill_dir).parts
        if any(part in IGNORED_DIRS for part in rel_parts):
            continue
        files.append({
            'relative_path': str(file_path.relative_to(skill_dir)),
            'sha256': sha256_file(file_path),
        })
    return {
        'skill_name': skill_dir.name,
        'files': files,
    }


def discover_skills(root: Path) -> list:
    if not root.exists() or not root.is_dir():
        return []
    skills = []
    for entry in sorted(root.iterdir()):
        if entry.is_dir() and not entry.name.startswith('.'):
            skill_md = entry / 'SKILL.md'
            if skill_md.exists():
                skills.append(collect_skill(entry))
    return skills


def main() -> None:
    parser = argparse.ArgumentParser(description='Collect SHA-256 hashes for installed skills.')
    parser.add_argument('roots', nargs='+', help='Skill roots to inspect, e.g. ~/.openclaw/skills ./skills')
    args = parser.parse_args()

    payload = {'skills': []}
    for raw_root in args.roots:
        root = Path(raw_root).expanduser().resolve()
        payload['skills'].extend(discover_skills(root))

    print(json.dumps(payload, indent=2))


if __name__ == '__main__':
    main()
