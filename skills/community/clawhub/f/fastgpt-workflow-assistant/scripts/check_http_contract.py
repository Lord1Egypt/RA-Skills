#!/usr/bin/env python3
"""Check explicit HTTP URL/config/catch contracts offline; never resolves or requests URLs."""
import argparse
import hashlib
import ipaddress
import json
from pathlib import Path
import re
from urllib.parse import urlsplit


def validate_url(value):
    if not isinstance(value, str) or not value:
        return {'valid': False, 'reason': 'empty'}
    if value != value.strip() or re.search(r'[\s\x00-\x1f\x7f\\]', value):
        return {'valid': False, 'reason': 'whitespace_or_backslash'}
    try:
        parsed = urlsplit(value)
        if parsed.scheme.lower() not in ('http', 'https') or not parsed.netloc or not parsed.hostname:
            return {'valid': False, 'reason': 'scheme_or_host_missing'}
        if parsed.username is not None or parsed.password is not None:
            return {'valid': False, 'reason': 'credentials_in_url'}
        host = parsed.hostname
        if parsed.port is not None and not 1 <= parsed.port <= 65535:
            return {'valid': False, 'reason': 'invalid_port'}
        if parsed.netloc.endswith(':'):
            return {'valid': False, 'reason': 'empty_port'}
        try:
            ipaddress.ip_address(host)
        except ValueError:
            ascii_host = host.encode('idna').decode('ascii').rstrip('.')
            if re.fullmatch(r'[\d.]+', host):
                return {'valid': False, 'reason': 'invalid_ip_host'}
            if len(ascii_host) > 253 or not all(re.fullmatch(r'[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?', label) for label in ascii_host.split('.')):
                return {'valid': False, 'reason': 'invalid_host'}
        if parsed.fragment:
            return {'valid': False, 'reason': 'fragment_not_request_target'}
    except (ValueError, UnicodeError):
        return {'valid': False, 'reason': 'invalid_url'}
    return {'valid': True, 'reason': 'syntax_only_not_reachability_or_api_readiness'}


def check(workflow, contract):
    nodes = {n['nodeId']: n for n in workflow.get('nodes', [])}
    edges = workflow.get('edges', [])
    cases = contract.get('cases')
    if not isinstance(cases, list) or not cases:
        raise ValueError('nonempty cases required')
    results = []
    for case in cases:
        errors = []
        http = nodes.get(case['http_node'])
        gate = nodes.get(case['gate_node'])
        source = case.get('source')
        if not http or http.get('flowNodeType') != 'httpRequest468' or not gate:
            raise ValueError('HTTP/gate node missing')
        if not isinstance(source, dict) or set(source) not in ({'reference'}, {'literal'}):
            raise ValueError('source must contain exactly reference or literal')
        def input_at(node, key):
            return next((i for i in node.get('inputs', []) if i.get('key') == key), None)
        gate_url = input_at(gate, case['gate_url_input'])
        http_url = input_at(http, 'system_httpReqUrl')
        def matches(item):
            if not item or 'value' not in item:
                return False
            value = item['value']
            if 'literal' in source:
                return value == source['literal']
            ref = source['reference']
            if not isinstance(ref, list) or len(ref) != 2 or not all(isinstance(x, str) and x for x in ref):
                raise ValueError('invalid source reference')
            return value == ref or value == '{{$' + ref[0] + '.' + ref[1] + '$}}'
        if not matches(gate_url) or not matches(http_url):
            errors.append('HC001_gate_and_http_source_mismatch_or_missing')
        # Equality of export values is not proof that the platform interpolates URL references.
        if 'reference' in source:
            ref = source['reference']
            if ref[0] == 'VARIABLE_NODE_ID':
                if not any(v.get('key') == ref[1] for v in workflow.get('chatConfig', {}).get('variables', [])):
                    errors.append('HC002_source_variable_not_declared')
            elif ref[0] not in nodes or not any(o.get('id') == ref[1] for o in nodes[ref[0]].get('outputs', [])):
                errors.append('HC002_source_output_not_declared')
        elif not validate_url(source['literal'])['valid']:
            errors.append('HC003_invalid_literal_url')
        if case.get('require_catch', True):
            catch_edges = [e for e in edges if e.get('source') == http['nodeId'] and 'source_catch' in e.get('sourceHandle', '')]
            if not http.get('catchError') or not catch_edges:
                errors.append('HC004_http_catch_missing')
            if not any(o.get('key') == 'error' for o in http.get('outputs', [])):
                errors.append('HC004_error_output_missing')
            expected = set(case.get('error_targets', []))
            if not expected or not expected <= set(nodes):
                raise ValueError('known error_targets required')
            if not any(e.get('target') in expected for e in catch_edges):
                errors.append('HC005_error_target_not_connected')
            for nid in expected:
                for required in case.get('error_required_references', []):
                    needle = '{{$' + required[0] + '.' + required[1] + '$}}'
                    if not any(i.get('value') == required or needle in str(i.get('value', '')) for i in nodes[nid].get('inputs', [])):
                        errors.append('HC006_error_reference_missing')
        results.append({'name': case.get('name', http['nodeId']), 'passed': not errors, 'errors': sorted(set(errors))})
    return {'passed': all(r['passed'] for r in results), 'cases': results,
            'scope': 'explicit export source equality and direct catch wiring only; no interpolation, condition evaluation, error semantics, network or platform runtime verified'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('workflow', type=Path)
    parser.add_argument('contract', type=Path)
    args = parser.parse_args()
    try:
        raw = args.workflow.read_bytes()
        report = check(json.loads(raw.decode('utf-8-sig')), json.loads(args.contract.read_text(encoding='utf-8-sig')))
        report['workflow_sha256'] = hashlib.sha256(raw).hexdigest()
        report['contract_sha256'] = hashlib.sha256(args.contract.read_bytes()).hexdigest()
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0 if report['passed'] else 1
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print(json.dumps({'passed': False, 'error_type': type(exc).__name__}))
        return 2

if __name__ == '__main__':
    raise SystemExit(main())
