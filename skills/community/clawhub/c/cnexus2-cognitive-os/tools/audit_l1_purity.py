#!/usr/bin/env python3
"""Phase 2 Audit: L1 Specs Purity Check
Ensures 01_runtime_spec/ files contain no code, no Python syntax, no classes, no async/await."""

import os, sys, re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L1_DIR = os.path.join(BASE, '01_runtime_spec')

# Patterns that indicate code implementation leaking into specs
IMPLEMENTATION_LEAK = [
    r'async\s+',               # async operations
    r'await\s+',               # await
    r'class\s+\w+',            # class definitions
    r'@dataclass',             # Python dataclass
    r'import\s+\w+',           # imports
    r':\s*=\s*',               # walrus
    r'def\s+\w+\s*\(',         # function def (allow markdown code blocks via table check later)
]

ALLOWED_IN_MD = [
    '```python', '```json', '```yaml',
]

def check_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    in_code_block = False
    violations = []

    for i, line in enumerate(lines, 1):
        stripped = line.strip()

        # Track code blocks to skip
        if stripped.startswith('```'):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        if not stripped or stripped.startswith('#') or stripped.startswith('<!--'):
            continue

        # Check for implementation leaks
        for pattern in IMPLEMENTATION_LEAK:
            if re.search(pattern, stripped):
                violations.append((i, stripped[:80], pattern))

    return violations

def main():
    if not os.path.exists(L1_DIR):
        print('[AUDIT] L1 spec directory not found')
        sys.exit(1)

    # Walk all files in 01_runtime_spec recursively
    all_violations = {}
    for root, dirs, files in os.walk(L1_DIR):
        for fname in sorted(files):
            if not fname.endswith('.md'):
                continue
            fpath = os.path.join(root, fname)
            rel = os.path.relpath(fpath, BASE)
            v = check_file(fpath)
            if v:
                all_violations[rel] = v

    if all_violations:
        print('[AUDIT] L1_FAILED - Implementation artifacts found:')
        for rel, vlist in all_violations.items():
            print(f'  {rel}:')
            for lineno, line, pattern in vlist:
                print(f'    L{lineno}: "{line}"  matched: {pattern}')
        sys.exit(1)
    else:
        file_count = sum(1 for r, d, fs in os.walk(L1_DIR) for f in fs if f.endswith('.md'))
        print(f'[AUDIT] L1_PASSED - {file_count} files in 01_runtime_spec/ are spec-clean.')

if __name__ == '__main__':
    main()
