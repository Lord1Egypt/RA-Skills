#!/usr/bin/env python3
"""Phase 1 Audit Tool: L0 Purity Check"""

import os, re, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE_DIR = os.path.join(BASE, 'core_essence')

EXEC_SEMANTICS = [
    r'def\s+\w+\s*\(',
    r'class\s+\w+\s*[:\\(]',
    r'@dataclass',
    r'import\s+\w+',
    r'->\s*\w+',
    r':\s*=\s*',
    r'for\s+\w+\s+in\s+',
    r'if\s+.*:',
    r'else\s*:',
    r'while\s+',
    r'try\s*:',
]

def check_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    violations = []
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue
        if stripped.startswith('|') or stripped.startswith('-') or stripped.startswith('```'):
            continue
        for pattern in EXEC_SEMANTICS:
            if re.search(pattern, stripped):
                violations.append((i, stripped, pattern))
    return violations

def main():
    if not os.path.exists(CORE_DIR):
        print('[AUDIT] L0 directory not found')
        sys.exit(1)

    files = sorted(os.listdir(CORE_DIR))
    errors = {}

    for fname in files:
        if not fname.endswith('.md'):
            continue
        v = check_file(os.path.join(CORE_DIR, fname))
        if v:
            errors[fname] = v

    if errors:
        print('[AUDIT] FAILED - Executable semantics found:')
        for fname, vlist in errors.items():
            print(f'  {fname}:')
            for lineno, line, pattern in vlist:
                print(f'    L{lineno}: {line[:60]} -> matched: {pattern}')
        sys.exit(1)
    else:
        print(f'[AUDIT] PASSED - {len(files)} files in core_essence/ are clean.')

if __name__ == '__main__':
    main()
