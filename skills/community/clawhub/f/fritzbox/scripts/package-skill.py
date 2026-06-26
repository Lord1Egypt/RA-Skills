#!/usr/bin/env python3
"""
Package the FRITZ!Box skill into a .skill file (zip archive) for ClawHub publication.
Usage: python3 scripts/package-skill.py [skill-path] [output-file]
"""

import os
import sys
import zipfile
import json
from pathlib import Path

skill_path = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path('.').resolve()
output_file = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else Path('fritzbox.skill').resolve()
skill_name = skill_path.name

print(f"Packaging skill: {skill_name}")
print(f"Output: {output_file}")

# Validate SKILL.md
skill_md = skill_path / 'SKILL.md'
if not skill_md.exists():
    print('❌ SKILL.md not found')
    sys.exit(1)

content = skill_md.read_text()
if not content.startswith('---'):
    print('❌ SKILL.md missing YAML frontmatter')
    sys.exit(1)

# Validate _meta.json
meta_file = skill_path / '_meta.json'
if not meta_file.exists():
    print('❌ _meta.json not found')
    sys.exit(1)

meta = json.loads(meta_file.read_text())
for key in ('slug', 'version', 'source'):
    if key not in meta:
        print(f'❌ _meta.json missing "{key}" field')
        sys.exit(1)

# Files to include (whitelist)
include_files = [
    'SKILL.md',
    'README.md',
    'fritzbox.py',
    'requirements.txt',
    '_meta.json',
    '.env.example',
    'CHANGELOG.md',
    'CONTRIBUTING.md',
    'INSTALL.md',
    'LICENSE',
    'test.sh',
]

# Directories to include recursively
include_dirs = [
    'scripts',
    'examples',
    'references',
]

# Paths to always exclude
exclude = {
    'node_modules', '.git', '__pycache__', '.DS_Store',
    'coverage', '.vscode', '.idea', '*.pyc', '*.skill',
    '.env',
}

def should_exclude(rel_path: str) -> bool:
    parts = Path(rel_path).parts
    name = parts[-1] if parts else rel_path
    for pattern in exclude:
        if pattern.startswith('*'):
            ext = pattern[1:]
            if name.endswith(ext):
                return True
        elif name == pattern or parts[0] == pattern:
            return True
    return False


output_file.parent.mkdir(parents=True, exist_ok=True)

with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zf:
    # Add whitelisted individual files
    for fname in include_files:
        src = skill_path / fname
        if src.exists():
            arcname = f'{skill_name}/{fname}'
            zf.write(src, arcname)
            print(f'  + {fname}')
        else:
            print(f'  - skipped (not found): {fname}')

    # Add whitelisted directories recursively
    for dname in include_dirs:
        src_dir = skill_path / dname
        if src_dir.exists():
            for item in src_dir.rglob('*'):
                rel = item.relative_to(skill_path)
                if should_exclude(str(rel)):
                    continue
                if item.is_file():
                    arcname = f'{skill_name}/{rel}'
                    zf.write(item, arcname)
                    print(f'  + {rel}')

size_kb = output_file.stat().st_size / 1024
print(f'\n✅ Packaged {skill_name} v{meta["version"]} → {output_file.name} ({size_kb:.1f} KB)')
