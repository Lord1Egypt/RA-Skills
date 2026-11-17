"""Check supplied rewrites against narrow, case-specific offline constraints.

This is NOT a converter, semantic-equivalence model, or dialect-fluency judge.
Exit 0: surface checks passed; 1: a check failed; 2: invalid/incomplete input.
"""
import argparse
import json
import re
import sys
from pathlib import Path

DEFAULT_CASES = Path(__file__).resolve().parents[1] / 'tests/fixtures/abu_dhabi_cases.json'


def evaluate(cases, responses):
    """Require exactly one nonempty response per case; never fill in answers."""
    if not isinstance(cases, list) or not cases:
        raise ValueError('Cases must be a nonempty list')
    expected = {}
    for case in cases:
        if not isinstance(case, dict) or not isinstance(case.get('id'), str) or not case['id'].strip():
            raise ValueError('Every case needs a nonempty string id')
        if case['id'] in expected:
            raise ValueError('Duplicate case id: ' + case['id'])
        for field in ('required_literals', 'forbidden_patterns'):
            items = case.get(field, [])
            if not isinstance(items, list) or any(not isinstance(s, str) or not s for s in items):
                raise ValueError('Invalid ' + field + ': ' + case['id'])
        groups = case.get('required_any', [])
        if not isinstance(groups, list) or any(not isinstance(g, list) or not g or any(not isinstance(s, str) or not s for s in g) for g in groups):
            raise ValueError('Invalid required_any: ' + case['id'])
        if not (case.get('required_literals') or groups or case.get('forbidden_patterns')):
            raise ValueError('Case has no automated constraints: ' + case['id'])
        for pattern in case.get('forbidden_patterns', []) + [p for g in groups for p in g]:
            try:
                re.compile(pattern)
            except re.error as exc:
                raise ValueError('Invalid regex in case: ' + case['id']) from exc
        expected[case['id']] = case
    if not isinstance(responses, list):
        raise ValueError('Responses must be a JSON list')
    supplied = {}
    for response in responses:
        if not isinstance(response, dict) or set(response) != {'id', 'output'}:
            raise ValueError('Each response must contain exactly id and output')
        ident = response['id']
        output = response['output']
        if not isinstance(ident, str) or ident not in expected:
            raise ValueError('Unknown response id')
        if ident in supplied:
            raise ValueError('Duplicate response id: ' + ident)
        if not isinstance(output, str) or not output.strip():
            raise ValueError('Output must be a nonempty string: ' + ident)
        supplied[ident] = output
    missing = sorted(set(expected) - set(supplied))
    if missing:
        raise ValueError('Missing response ids: ' + ', '.join(missing))
    results = []
    for ident, case in expected.items():
        output = supplied[ident]
        failures = []
        for literal in case.get('required_literals', []):
            if literal not in output:
                failures.append('Missing protected literal: ' + literal)
        for choices in case.get('required_any', []):
            if not any(re.search(pattern, output) for pattern in choices):
                failures.append('No match in required group: ' + ' | '.join(choices))
        for pattern in case.get('forbidden_patterns', []):
            if re.search(pattern, output):
                failures.append('Forbidden pattern matched: ' + pattern)
        results.append({'id': ident, 'passed': not failures, 'failures': failures})
    return {'passed': all(r['passed'] for r in results), 'evaluated': len(results),
            'total': len(expected), 'human_review_required': True,
            'check_scope': 'case-specific surface constraints only; not semantic or native fluency certification',
            'results': results}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--responses', required=True, type=Path, help='JSON list of {id, output}; must cover every case')
    parser.add_argument('--cases', type=Path, default=DEFAULT_CASES, help='Trusted local case file; regexes are not sandboxed')
    args = parser.parse_args(argv)
    try:
        payload = json.loads(args.cases.read_text(encoding='utf-8'))
        if not isinstance(payload, dict) or 'cases' not in payload:
            raise ValueError('Case file must be an object containing cases')
        responses = json.loads(args.responses.read_text(encoding='utf-8'))
        report = evaluate(payload['cases'], responses)
    except (OSError, UnicodeError, ValueError) as exc:
        print(json.dumps({'error': str(exc), 'passed': False}, ensure_ascii=False))
        return 2
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    reconfigure = getattr(sys.stdout, 'reconfigure', None)
    if reconfigure is not None:
        reconfigure(encoding='utf-8')
    raise SystemExit(main())
