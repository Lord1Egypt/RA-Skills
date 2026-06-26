from __future__ import annotations

from typing import Dict, List, Tuple

from .common import compare_hint_lists, path_similarity, uniq
from .ir import EndpointIR, Finding, hints_to_dict


def canonicalize_auth_hints(values: List[str]) -> List[str]:
    out = []
    for value in values:
        normalized = value
        if value in {'authorization-helper', 'authorization-default-header', 'token-ref', 'authentication-principal', 'request-header', 'authenticated-route'}:
            normalized = 'authorization-header'
        out.append(normalized)
    return uniq(out)


def compare_surfaces(frontend: List[EndpointIR], backend: List[EndpointIR]):
    findings: List[Finding] = []
    unknowns: List[str] = []
    next_actions: List[str] = []
    idx = 1
    stats = {'frontend_total': len(frontend), 'backend_total': len(backend), 'frontend_exact_matches': 0, 'frontend_dynamic_matches': 0, 'frontend_missing': 0, 'frontend_method_mismatches': 0, 'frontend_path_mismatches': 0, 'frontend_ambiguous_unmatched': 0, 'backend_only': 0, 'hint_mismatches': 0}

    def add_finding(category: str, severity: str, summary: str, fe: EndpointIR | None, be: EndpointIR | None, recommendation: str):
        nonlocal idx
        findings.append(Finding(
            id=f'FB-{idx:03d}', category=category, severity=severity, summary=summary,
            frontend_source=None if fe is None else {'file': fe.file, 'line': fe.line, 'symbol': fe.locator},
            backend_source=None if be is None else {'file': be.file, 'line': be.line, 'symbol': be.locator},
            evidence={
                'frontend': None if fe is None else {'call': fe.source, 'path': fe.path, 'raw_path': fe.raw_path, 'framework': fe.framework, 'confidence': fe.confidence, 'hints': hints_to_dict(fe.hints)},
                'backend': None if be is None else {'mapping': be.source, 'path': be.path, 'raw_path': be.raw_path, 'framework': be.framework, 'confidence': be.confidence, 'hints': hints_to_dict(be.hints)},
                'hint_diff': None if fe is None or be is None else {
                    'path_params': compare_hint_lists(fe.hints.path_params, be.hints.path_params),
                    'query_params': compare_hint_lists(fe.hints.query_params, be.hints.query_params),
                    'body_keys': compare_hint_lists(fe.hints.body_keys, be.hints.body_keys),
                    'response_keys': compare_hint_lists(fe.hints.response_keys, be.hints.response_keys),
                    'auth': compare_hint_lists(fe.hints.auth, be.hints.auth, canonicalize_auth_hints),
                },
            },
            recommendation=recommendation,
        ))
        idx += 1

    def add_hint_findings(fe: EndpointIR, be: EndpointIR):
        diff_query = compare_hint_lists(fe.hints.query_params, be.hints.query_params)
        diff_body = compare_hint_lists(fe.hints.body_keys, be.hints.body_keys)
        diff_auth = compare_hint_lists(fe.hints.auth, be.hints.auth, canonicalize_auth_hints)
        diff_response = compare_hint_lists(fe.hints.response_keys, be.hints.response_keys)
        if diff_query['frontend_only'] or diff_query['backend_only']:
            stats['hint_mismatches'] += 1
            add_finding('query-hint-mismatch', 'medium', f'프론트/백엔드 query 파라미터 힌트가 어긋남: {fe.method} {fe.path}', fe, be, 'params 구성과 @RequestParam/Pageable 계약을 맞춰라.')
        body_presence_diff = bool(fe.hints.body_kind) != bool(be.hints.body_kind)
        consumes_diff = fe.hints.consumes != be.hints.consumes and (fe.hints.consumes or be.hints.consumes)
        if (fe.hints.body_kind or be.hints.body_kind) and (diff_body['frontend_only'] or diff_body['backend_only'] or body_presence_diff or consumes_diff):
            stats['hint_mismatches'] += 1
            add_finding('body-hint-mismatch', 'medium', f'프론트/백엔드 request body 힌트가 어긋남: {fe.method} {fe.path}', fe, be, 'payload 필드, multipart 여부, DTO 계약을 맞춰라.')
        if fe.hints.response_keys and be.hints.response_keys and (diff_response['frontend_only'] or diff_response['backend_only']):
            stats['hint_mismatches'] += 1
            add_finding('response-hint-mismatch', 'medium', f'프론트/백엔드 response 필드 힌트가 어긋남: {fe.method} {fe.path}', fe, be, '프론트가 읽는 응답 필드와 백엔드 응답 DTO/랩퍼 구조를 함께 점검해라.')
        if diff_auth['frontend_only'] or diff_auth['backend_only']:
            stats['hint_mismatches'] += 1
            add_finding('auth-hint-mismatch', 'low', f'프론트/백엔드 auth 힌트가 어긋남: {fe.method} {fe.path}', fe, be, 'Authorization 헤더/인증 가드/쿠키 사용 여부를 점검해라.')

    matched_backend = set()
    for fe in frontend:
        exact = [be for be in backend if be.method == fe.method and path_similarity(be.path, fe.path)]
        if exact:
            for be in exact:
                matched_backend.add((be.method, be.path, be.file, be.line))
                add_hint_findings(fe, be)
            stats['frontend_dynamic_matches' if fe.ambiguous else 'frontend_exact_matches'] += 1
            continue
        same_path = [be for be in backend if path_similarity(be.path, fe.path)]
        if same_path:
            be = same_path[0]
            stats['frontend_method_mismatches'] += 1
            add_finding('method-mismatch', 'high', f'프론트는 {fe.method} {fe.path} 를 호출하지만 백엔드는 같은 경로에 {be.method} 만 노출함', fe, be, '프론트 HTTP 메서드 또는 백엔드 매핑을 맞춰라.')
            matched_backend.add((be.method, be.path, be.file, be.line))
            next_actions.append(f'{fe.path} 메서드 정의 정합성 수정')
            continue
        same_method = [be for be in backend if be.method == fe.method]
        fe_last = fe.path.split('/')[-1]
        likely = next((be for be in same_method if fe_last == be.path.split('/')[-1] and fe_last != '{}' and len(fe.path.split('/')) == len(be.path.split('/'))), None)
        if fe.ambiguous:
            stats['frontend_ambiguous_unmatched'] += 1
        dynamic_prefix_candidates = []
        if '{}' in fe.path:
            fe_prefix = fe.path.rsplit('/', 1)[0]
            dynamic_prefix_candidates = [be for be in same_method if be.path.startswith(fe_prefix + '/')]
        if likely is None and dynamic_prefix_candidates:
            if fe.ambiguous:
                stats['frontend_ambiguous_unmatched'] += 1
            unknowns.append(f'동적 경로 추론 한계: {fe.method} {fe.path} 는 동일 prefix 백엔드 후보 {len(dynamic_prefix_candidates)}건과 수동 확인 필요')
        elif likely is None:
            stats['frontend_missing'] += 1
            add_finding('missing-backend-endpoint', 'high', f'프론트 {fe.method} {fe.path} 와 일치하는 백엔드 엔드포인트를 찾지 못함', fe, None, '프론트 경로 문자열, base path 결합, 또는 백엔드 매핑 누락 여부를 점검해라.')
        else:
            stats['frontend_path_mismatches'] += 1
            add_finding('path-mismatch', 'medium', f'프론트 {fe.method} {fe.path} 와 백엔드 {likely.method} {likely.path} 경로가 어긋남', fe, likely, '프론트 경로 문자열, base path 결합, 또는 백엔드 @RequestMapping prefix 를 점검해라.')
        next_actions.append(f'{fe.method} {fe.path} 경로 매핑 확인')
    for be in backend:
        key = (be.method, be.path, be.file, be.line)
        if key not in matched_backend:
            stats['backend_only'] += 1
            add_finding('backend-only-endpoint', 'low', f'백엔드 {be.method} {be.path} 엔드포인트가 현재 추출된 프론트 호출과 연결되지 않음', None, be, '미사용 엔드포인트인지, 다른 클라이언트 전용인지, 동적 호출이라 추출 실패한 것인지 확인해라.')
    dynamic_total = sum(1 for fe in frontend if fe.ambiguous)
    if dynamic_total:
        unknowns.append(f'동적 경로 호출 {dynamic_total}건 중 {stats["frontend_dynamic_matches"]}건은 정상 매칭됐고 {stats["frontend_ambiguous_unmatched"]}건만 여전히 미해결')
    if not frontend:
        unknowns.append('프론트 API 호출 패턴을 찾지 못함: axios/fetch/Dio 및 일부 wrapper alias 패턴만 현재 지원')
    if not backend:
        unknowns.append('백엔드 Spring 매핑을 찾지 못함: @GetMapping/@PostMapping/@RequestMapping 패턴만 현재 지원')
    if not next_actions:
        next_actions.append('정적 추출 범위를 넓혀 response 필드 비교를 추가')
    severity_rank = {'high': 3, 'medium': 2, 'low': 1}
    max_sev = max((severity_rank[f.severity] for f in findings), default=0)
    risk_level = {0: 'low', 1: 'low', 2: 'medium', 3: 'high'}[max_sev]
    return findings, unknowns, sorted(set(next_actions)), risk_level, stats
