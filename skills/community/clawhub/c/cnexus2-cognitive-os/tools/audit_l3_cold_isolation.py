#!/usr/bin/env python3
"""Phase 3 Audit: L2+L3 Cold Isolation Check
Ensures L3 analysis files do not claim write access to live State/L1 runtime."""

import os, sys, re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L2_DIR = os.path.join(BASE, '02_stability_spec')
L3_DIRS = [
    os.path.join(BASE, '06_failure_runtime_analyzer'),
    os.path.join(BASE, '07_feedback_runtime_controller'),
]

# Comments or statements claiming write access to live state
LIVE_WRITE_CLAIMS = [
    r'modify\s+current\s+State',
    r'write\s+to\s+State',
    r'direct\s+update\s+State',
    r'set\s+Emotion',
    r'set\s+Relationship',
    r'set\s+Goal',
    r'set\s+Attention',
    r'overwrite\s+State',
    r'modify\s+L1',
    r'modify\s+reducer',
    r'interrupt\s+loop',
    r'change\s+current.*state',
]

# Patterns indicating code implementation leaks (same as L1 check)
IMPLEMENTATION_LEAK = [
    r'async\s+',
    r'await\s+',
    r'class\s+\w+',
    r'@dataclass',
    r'import\s+\w+',
    r':\s*=\s*',
    r'def\s+\w+\s*\(',
]

def check_file(filepath, strict_write_check=True):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    in_code_block = False
    violations = []

    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith('```'):
            in_code_block = not in_code_block
            continue
        if in_code_block or not stripped or stripped.startswith('#'):
            continue

        # Check implementation leaks
        for p in IMPLEMENTATION_LEAK:
            if re.search(p, stripped):
                violations.append((i, stripped[:60], f"code_leak: {p}"))

        # Check live write claims
        if strict_write_check:
            for p in LIVE_WRITE_CLAIMS:
                if re.search(p, stripped, re.IGNORECASE):
                    violations.append((i, stripped[:60], f"live_write_claim: {p}"))

    return violations

def main():
    all_violations = {}

    # Check L2
    if os.path.exists(L2_DIR):
        for fname in sorted(os.listdir(L2_DIR)):
            if not fname.endswith('.md'):
                continue
            fpath = os.path.join(L2_DIR, fname)
            v = check_file(fpath, strict_write_check=False)  # L2 can write state
            if v:
                all_violations[f"02_stability_spec/{fname}"] = v

    # Check L3
    for d in L3_DIRS:
        if not os.path.exists(d):
            continue
        for fname in sorted(os.listdir(d)):
            if not fname.endswith('.md'):
                continue
            fpath = os.path.join(d, fname)
            v = check_file(fpath, strict_write_check=True)  # L3 strict cold isolation
            if v:
                short_dir = os.path.basename(os.path.dirname(fpath))
                all_violations[f"{short_dir}/{fname}"] = v

    if all_violations:
        print('[AUDIT] FAILED - Violations found:')
        for rel, vlist in all_violations.items():
            print(f'  {rel}:')
            for lineno, line, pattern in vlist:
                print(f'    L{lineno}: "{line}" -> {pattern}')
        sys.exit(1)
    else:
        l2_count = len([f for f in os.listdir(L2_DIR) if f.endswith('.md')]) if os.path.exists(L2_DIR) else 0
        l3_count = sum(1 for d in L3_DIRS if os.path.exists(d) for f in os.listdir(d) if f.endswith('.md'))
        print(f'[AUDIT] PASSED - {l2_count} L2 + {l3_count} L3 files, zero live-write claims, zero code leaks.')

if __name__ == '__main__':
    main()
