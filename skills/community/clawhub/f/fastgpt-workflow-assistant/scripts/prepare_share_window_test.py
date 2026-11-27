#!/usr/bin/env python3
"""Prepare local evidence metadata for a user-authorized share-window test. No network or execution."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
from urllib.parse import parse_qs, urlsplit


def select_test_method(testing_requested, api_contract_confirmed=False, http_discovery_blocked=False, browser_available=False):
    """Plan from observed capabilities/evidence, not a permission grant or actual test."""
    if not testing_requested:
        return {'method': 'clarify_test_scope', 'needs_chat_api_from_user': False}
    if api_contract_confirmed:
        return {'method': 'direct_share_api_regression', 'needs_chat_api_from_user': False}
    if not http_discovery_blocked:
        return {'method': 'http_read_page_and_public_api_evidence', 'needs_chat_api_from_user': False}
    if browser_available:
        return {'method': 'browser_network_discovery_fallback', 'needs_chat_api_from_user': False}
    return {'method': 'report_specific_discovery_block_and_request_minimum_evidence', 'needs_chat_api_from_user': 'only_if_not_obtainable_with_available_tools'}


def inspect_target(page_url, workflow=None):
    if not isinstance(page_url, str) or page_url != page_url.strip() or any(c.isspace() for c in page_url) or '\\' in page_url:
        raise ValueError('Invalid page URL')
    parsed = urlsplit(page_url)
    if parsed.scheme not in ('http', 'https') or not parsed.hostname or parsed.username is not None or parsed.password is not None or parsed.fragment:
        raise ValueError('Expected HTTP(S) share page without credentials or fragment')
    if parsed.port is not None and not 1 <= parsed.port <= 65535:
        raise ValueError('Invalid port')
    query = parse_qs(parsed.query, keep_blank_values=True)
    ids = query.get('shareId')
    if not ids or len(ids) != 1 or not ids[0].strip():
        raise ValueError('Exactly one nonempty shareId required; other channel formats need target-instance evidence')
    if set(query) - {'shareId'}:
        raise ValueError('Additional URL parameters require manual review; do not copy passwords or tokens into test manifests')
    report = {'artifact_role': 'share-test-target-report', 'importable_workflow': False,
              'page_url': page_url, 'origin': parsed.scheme + '://' + parsed.netloc,
              'share_id': ids[0], 'endpoint': None, 'endpoint_status': 'not_observed_do_not_guess',
              'app_id': None, 'app_id_status': 'not_inferred_from_share_id',
              'workflow': None, 'scope': 'offline URL/JSON inspection only; no browser, HTTP, login or conversation executed',
              'page_access': 'not_tested', 'platform_runtime': 'not_tested',
              'flow_details_visibility': 'unknown', 'zero_tool_requests': 'not_verified',
              'preferred_test_method': 'api-first',
              'browser_role': 'fallback_protocol_discovery_or_optional_visual_check',
              'next_step': 'resolve_evidenced_instance_profile_then_smoke_before_any_new_discovery'}
    if workflow is not None:
        file = Path(workflow)
        raw = file.read_bytes()
        data = json.loads(raw.decode('utf-8-sig'))
        if not isinstance(data, dict) or not isinstance(data.get('nodes'), list) or not data['nodes'] or not isinstance(data.get('edges'), list) or not isinstance(data.get('chatConfig'), dict):
            raise ValueError('Expected workflow export nodes/edges/chatConfig, not a validation report or contract')
        report['workflow'] = {'file': str(file.resolve()), 'sha256': hashlib.sha256(raw).hexdigest(),
                              'nodes': len(data['nodes']), 'edges': len(data['edges']),
                              'published_version_alignment': 'not_verified_against_shared_channel'}
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--page-url', required=True)
    parser.add_argument('--workflow', type=Path)
    parser.add_argument('--output', required=True, type=Path, help='Local target report; not an importable workflow')
    args = parser.parse_args()
    try:
        report = inspect_target(args.page_url, args.workflow)
        report['created_at'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open('x', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
            f.write('\n')
        print(json.dumps({'status': 'prepared_not_executed', 'file': str(args.output), 'importable_workflow': False}))
        return 0
    except (ValueError, OSError, TypeError) as exc:
        print(json.dumps({'status': 'error', 'error_type': type(exc).__name__}))
        return 1

if __name__ == '__main__':
    raise SystemExit(main())
