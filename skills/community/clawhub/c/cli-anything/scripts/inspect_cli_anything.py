#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path('/root/.openclaw/workspace/CLI-Anything')


def detect_harnesses(root: Path):
    items = []
    if not root.exists():
        return items
    for setup_py in sorted(root.glob('*/agent-harness/setup.py')):
        harness_dir = setup_py.parent
        software_dir = harness_dir.parent
        name = software_dir.name
        pkg_root = harness_dir / 'cli_anything'
        readmes = list(harness_dir.glob('*.md')) + list((pkg_root / name).glob('README.md')) if (pkg_root / name).exists() else list(harness_dir.glob('*.md'))
        tests = list(harness_dir.glob('cli_anything/**/tests/test_full_e2e.py'))
        items.append({
            'name': name,
            'path': str(harness_dir),
            'has_setup_py': setup_py.exists(),
            'has_pkg_dir': (pkg_root / name).exists(),
            'has_readme': any(p.name.lower() == 'readme.md' for p in readmes),
            'has_e2e_tests': bool(tests),
        })
    return items


def main():
    data = {
        'repo_exists': ROOT.exists(),
        'repo_path': str(ROOT),
        'harnesses': detect_harnesses(ROOT),
    }
    data['harness_count'] = len(data['harnesses'])
    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
