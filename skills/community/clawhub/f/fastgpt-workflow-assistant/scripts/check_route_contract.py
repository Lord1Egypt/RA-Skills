#!/usr/bin/env python3
"""Check explicit branch graph contracts without evaluating conditions, executing code or accessing URLs."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path


def check(workflow: dict, contract: dict) -> dict:
    nodes, edges = workflow.get('nodes', []), workflow.get('edges', [])
    ids = [n['nodeId'] for n in nodes]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate node IDs')
    ids = set(ids)
    terminals = contract.get('terminal_nodes', [])
    cases = contract.get('cases')
    if not isinstance(cases, list) or not cases:
        raise ValueError('Nonempty cases required')
    if not set(terminals) <= ids:
        raise ValueError('Unknown terminal node')
    dangling = any(e.get('source') not in ids or e.get('target') not in ids for e in edges)
    quads = [(e.get('source'), e.get('target'), e.get('sourceHandle'), e.get('targetHandle')) for e in edges]
    duplicates = len(quads) != len(set(quads))
    results = []
    for case in cases:
        source, handle = case['source'], case['source_handle']
        required, forbidden = set(case.get('required_nodes', [])), set(case.get('forbidden_nodes', []))
        if source not in ids or not handle or not required or not (required | forbidden) <= ids or required & forbidden:
            raise ValueError('Invalid source/handle or required/forbidden node contract')
        entry = [e for e in edges if e.get('source') == source and e.get('sourceHandle') == handle]
        errors = []
        if len(entry) != 1:
            errors.append('selected_branch_must_have_exactly_one_edge')
        if dangling:
            errors.append('dangling_edge')
        if duplicates:
            errors.append('duplicate_edge')
        visited, active, done = set(), set(), set()

        def walk(node):
            if node in active:
                errors.append('cycle_requires_runtime_state')
                return
            if node in done:
                return
            visited.add(node)
            active.add(node)
            outgoing = [e for e in edges if e.get('source') == node]
            if node in terminals and outgoing:
                errors.append('terminal_has_outgoing_edges')
            # Explore ALL edges, even unexpected branches or edges leaving a reply.
            for e in outgoing:
                if e.get('target') in ids:
                    walk(e['target'])
            active.remove(node)
            done.add(node)

        for e in entry:
            if e.get('target') in ids:
                walk(e['target'])
        if not required <= visited:
            errors.append('required_nodes_not_reachable')
        if forbidden & visited:
            errors.append('forbidden_nodes_reachable')
        results.append({'name': case.get('name', handle), 'passed': not errors,
                        'reachable_nodes': sorted(visited), 'errors': sorted(set(errors))})
    return {'scope': 'conservative static graph only; required nodes are reachable, not proven executed on every runtime path',
            'conditions_evaluated': False, 'code_executed': False, 'network_access': False,
            'platform_runtime': 'not_verified', 'passed': all(r['passed'] for r in results), 'cases': results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('workflow', type=Path)
    parser.add_argument('contract', type=Path)
    args = parser.parse_args()
    try:
        raw = args.workflow.read_bytes()
        result = check(json.loads(raw.decode('utf-8-sig')), json.loads(args.contract.read_text(encoding='utf-8-sig')))
        result['workflow_sha256'] = hashlib.sha256(raw).hexdigest()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result['passed'] else 1
    except (OSError, ValueError, KeyError, TypeError, RecursionError) as exc:
        print(json.dumps({'passed': False, 'error_type': type(exc).__name__, 'scope': 'static contract inspection'}))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
