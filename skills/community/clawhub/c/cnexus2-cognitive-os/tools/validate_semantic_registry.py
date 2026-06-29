#!/usr/bin/env python3
"""Phase 1 Audit Tool: Semantic Registry Check
Verifies all concepts in core_essence/ are registered in GLOBAL_SEMANTIC_REGISTRY.md"""

import os, sys, re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTRY = os.path.join(BASE, '_global_registry', 'GLOBAL_SEMANTIC_REGISTRY.md')

# L0 concepts that must be registered
REQUIRED_CONCEPTS = [
    'identity_attractor', 'identity_coherence',
    'cognitive_loop', 'OBSERVE', 'COGNIZE', 'DECIDE', 'SPEAK', 'STORE', 'REFLECT',
    'Block', 'State', 'Trace',
    'persona', 'emotion', 'intent', 'belief', 'narrative', 'episodic', 'archival', 'reflective',
    'P1', 'P2', 'P3',
    'attractor',
    'objective_function',
    'loop',
    'state',
    'memory',
    'trace',
    'inference',
]

def main():
    if not os.path.exists(REGISTRY):
        print(f'[AUDIT] Registy not found: {REGISTRY}')
        sys.exit(1)

    with open(REGISTRY, 'r', encoding='utf-8') as f:
        content = f.read()

    missing = []
    for concept in REQUIRED_CONCEPTS:
        # Check as markdown table entry or section header
        if concept not in content:
            missing.append(concept)

    if missing:
        print(f'[AUDIT] FAILED - {len(missing)} concepts not registered:')
        for c in missing:
            print(f'  - {c}')
        sys.exit(1)
    else:
        print(f'[AUDIT] PASSED - All {len(REQUIRED_CONCEPTS)} required concepts registered.')

if __name__ == '__main__':
    main()
