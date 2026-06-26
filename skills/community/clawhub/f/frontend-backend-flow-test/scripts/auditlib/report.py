from __future__ import annotations

from typing import Dict, List

from .ir import EndpointIR, Finding


def format_hint_summary(hints: Dict[str, object]) -> str:
    parts = []
    if hints.get('path_params'):
        parts.append(f"path={','.join(hints['path_params'])}")
    if hints.get('query_params'):
        parts.append(f"query={','.join(hints['query_params'])}")
    if hints.get('body_kind'):
        body_text = str(hints['body_kind'])
        if hints.get('body_keys'):
            body_text += f"({','.join(hints['body_keys'])})"
        parts.append(f'body={body_text}')
    if hints.get('response_keys'):
        parts.append(f"response={','.join(hints['response_keys'])}")
    if hints.get('auth'):
        parts.append(f"auth={','.join(hints['auth'])}")
    if hints.get('consumes'):
        parts.append(f"consumes={hints['consumes']}")
    return '; '.join(parts) if parts else 'none'


def summarize_findings(findings: List[Finding]) -> Dict[str, object]:
    by_severity = {'high': 0, 'medium': 0, 'low': 0}
    by_category: Dict[str, int] = {}
    for f in findings:
        by_severity[f.severity] = by_severity.get(f.severity, 0) + 1
        by_category[f.category] = by_category.get(f.category, 0) + 1
    top_categories = sorted(by_category.items(), key=lambda x: (-x[1], x[0]))[:5]
    return {'by_severity': by_severity, 'top_categories': top_categories}


def render_markdown(frontend: List[EndpointIR], backend: List[EndpointIR], findings: List[Finding], unknowns: List[str], next_actions: List[str], risk_level: str, stats: Dict[str, int]) -> str:
    lines = []
    summary = summarize_findings(findings)
    hi = summary['by_severity']['high']
    med = summary['by_severity']['medium']
    low = summary['by_severity']['low']
    lines += ['# Frontend-Backend Audit Report', '', '## TL;DR', '']
    lines.append(f'- 위험도: **{risk_level.upper()}**')
    lines.append(f'- 프론트 호출 {len(frontend)}건 / 백엔드 엔드포인트 {len(backend)}건 분석')
    lines.append(f'- 주요 이슈 {len(findings)}건 (high {hi} / medium {med} / low {low})')
    lines.append(f'- 매칭 성공: exact {stats["frontend_exact_matches"]}건, dynamic {stats["frontend_dynamic_matches"]}건')
    lines.append(f'- 즉시 확인할 항목: missing {stats["frontend_missing"]} / method {stats["frontend_method_mismatches"]} / path {stats["frontend_path_mismatches"]} / hint {stats["hint_mismatches"]}')
    if summary['top_categories']:
        lines.append('- 많이 나온 유형: ' + ', '.join(f'{name} {count}건' for name, count in summary['top_categories']))
    lines += ['', '## Summary', '', '| Metric | Count |', '| --- | ---: |']
    for label, value in [('Frontend endpoints found', len(frontend)), ('Backend endpoints found', len(backend)), ('Exact matches', stats['frontend_exact_matches']), ('Dynamic-path matches', stats['frontend_dynamic_matches']), ('Missing backend endpoints', stats['frontend_missing']), ('Method mismatches', stats['frontend_method_mismatches']), ('Path mismatches', stats['frontend_path_mismatches']), ('Hint mismatches', stats['hint_mismatches']), ('Ambiguous unmatched frontend calls', stats['frontend_ambiguous_unmatched']), ('Backend-only endpoints', stats['backend_only']), ('Findings', len(findings)), ('Risk level', risk_level)]:
        lines.append(f'| {label} | {value} |')
    lines += ['', '## Priority Actions', '']
    for item in next_actions[:10]:
        lines.append(f'- {item}')
    if len(next_actions) > 10:
        lines.append(f'- ... 외 {len(next_actions) - 10}건')
    lines += ['', '## Findings', '']
    if findings:
        for f in findings:
            lines.append(f'### {f.id} [{f.severity}] {f.category}')
            lines.append(f'- 요약: {f.summary}')
            if f.frontend_source:
                lines.append(f"- Frontend: `{f.frontend_source['file']}:{f.frontend_source['line']}` ({f.frontend_source['symbol']})")
            if f.backend_source:
                lines.append(f"- Backend: `{f.backend_source['file']}:{f.backend_source['line']}` ({f.backend_source['symbol']})")
            if f.evidence.get('frontend'):
                lines.append(f"- Frontend call: `{f.evidence['frontend']['call']}`")
                lines.append(f"- Frontend confidence: {f.evidence['frontend'].get('confidence', 'unknown')}")
                lines.append(f"- Frontend hints: {format_hint_summary(f.evidence['frontend']['hints'])}")
            if f.evidence.get('backend'):
                lines.append(f"- Backend mapping: `{f.evidence['backend']['mapping']}`")
                lines.append(f"- Backend confidence: {f.evidence['backend'].get('confidence', 'unknown')}")
                lines.append(f"- Backend hints: {format_hint_summary(f.evidence['backend']['hints'])}")
            if f.evidence.get('hint_diff'):
                diff = f.evidence['hint_diff']
                lines.append(f"- Hint diff(path): shared={','.join(diff['path_params']['shared']) or '-'} | fe-only={','.join(diff['path_params']['frontend_only']) or '-'} | be-only={','.join(diff['path_params']['backend_only']) or '-'}")
                lines.append(f"- Hint diff(query): shared={','.join(diff['query_params']['shared']) or '-'} | fe-only={','.join(diff['query_params']['frontend_only']) or '-'} | be-only={','.join(diff['query_params']['backend_only']) or '-'}")
                lines.append(f"- Hint diff(body): shared={','.join(diff['body_keys']['shared']) or '-'} | fe-only={','.join(diff['body_keys']['frontend_only']) or '-'} | be-only={','.join(diff['body_keys']['backend_only']) or '-'}")
                lines.append(f"- Hint diff(response): shared={','.join(diff['response_keys']['shared']) or '-'} | fe-only={','.join(diff['response_keys']['frontend_only']) or '-'} | be-only={','.join(diff['response_keys']['backend_only']) or '-'}")
                lines.append(f"- Hint diff(auth): shared={','.join(diff['auth']['shared']) or '-'} | fe-only={','.join(diff['auth']['frontend_only']) or '-'} | be-only={','.join(diff['auth']['backend_only']) or '-'}")
            lines.append(f'- Recommendation: {f.recommendation}')
            lines.append('')
    else:
        lines += ['- No mismatches found by current heuristics.', '']
    lines += ['## Unknowns', '']
    for item in unknowns or ['없음']:
        lines.append(f'- {item}')
    lines.append('')
    return '\n'.join(lines)
