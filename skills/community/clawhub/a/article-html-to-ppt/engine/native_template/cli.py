"""One local template workflow; the host Agent owns narration and orchestration."""
from __future__ import annotations
import argparse
import json
import sys
from . import runtime
from . import review as review_module
from .safety import strict_json, read_file, workspace_supported
from .package import SOURCE_PAGE_LIMIT
from .fidelity import RETENTION_MIN, HEADING_SIZE_MIN, SMALLEST_SIZE_MIN, BOX_TOLERANCE_PT


def capabilities():
    return {'ok': True, 'workflow': 'template', 'version': 1,
            'platform': {'supported': 'POSIX with fcntl and O_NOFOLLOW', 'windows': 'unsupported', 'tested': ['macOS']},
            'workspaceSupported': workspace_supported(),
            'limits': {'maxSourcePages': SOURCE_PAGE_LIMIT, 'maxOutputPages': runtime.OUTPUT_PAGE_LIMIT},
            'scope': 'native_template_toolchain_only',
            'templateFidelityThresholds': {'retentionMinimum': RETENTION_MIN, 'headingSizeMinimumRatio': HEADING_SIZE_MIN, 'smallestSizeMinimumRatio': SMALLEST_SIZE_MIN, 'geometryTolerancePt': BOX_TOLERANCE_PT},
            'finalRequirements': ['current real renders and external observations', 'source preservation floor passed', 'recomputed source-retention/type-scale fidelity floor passed', 'explicit nonblank output-page notes (presence only; truth not verified)'],
            'commands': ['capabilities', 'init', 'inspect', 'status', 'apply', 'export', 'render', 'review', 'verify'],
            'operations': {k: sorted(v) for k, v in runtime.OPERATIONS.items()},
            'objectIds': 'string cNvPr@id on the permanently bound source slide; new IDs positive numeric strings',
            'sourceSlideIds': 'string presentation sldId@id, in real presentation order',
            'geometryUnits': 'inches', 'initialRevision': 0, 'initialPages': [],
            'nativeChartData': {'categories': ['Test A', 'Test B'], 'series': [{'name': 'Test values', 'values': [1, 2]}]},
            'requestExample': {'expectedRevision': 0, 'operations': [{'op': 'add_page', 'id': 'cover', 'sourceSlideId': '256'}, {'op': 'edit_native', 'pageId': 'cover', 'objectId': '2', 'text': '新标题'}]},
            'reviewContract': {'schema_version': '1.0.0', 'status': 'approved|revise|rejected',
                               'candidateHash': 'sha256:...', 'templateHash': 'sha256:...', 'renderReportHash': 'sha256:...',
                               'reviewer': {'provider': 'human|provider', 'model': 'reviewer/model label', 'method': 'external visual comparison'},
                               'pages': [{'slide_index': 1, 'pageId': 'cover', 'sourceSlideId': '256', 'preview_sha256': 'sha256:...', 'reference_sha256': 'sha256:...',
                                          **{k: {'status': 'pass|fail', 'observation': '具体的外部视觉观察'} for k in review_module.CRITERIA}}],
                               'deck_rhythm': '全稿节奏与一致性观察'},
            'limitations': ['No scripts, network, macros, external relationships, font/color guesses or model calls',
                            'No arbitrary image input: picture additions clone an embedded same-source picture only',
                            'No cross-source slide jump links; notes back-links to the bound source remain supported',
                            'No group creation or geometry edit of group children', 'Text replacement retains paragraph/first-run native style, not mixed-run semantic mapping',
                            'Chart edits: single-plot category charts only; table edits: unchanged unmerged rectangular structure',
                            'No automatic review reuse; reviewer identity declared, not authenticated',
                            'No automatic factual review or tested Office/WPS compatibility',
                            'Not the complete Web visual floor or whole-Skill business acceptance',
                            'Strict source decoration/image and font-size retention; unresolved evidence blocks verify',
                            'Auto renderer uses workspace-isolated LibreOffice only; no GUI Office automation',
                            'Render unavailable/failure or missing/stale external review blocks final delivery']}


def main(argv=None):
    parser = argparse.ArgumentParser(prog='python3 -m engine template', description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('capabilities', help='accurate capabilities, operation keys and review JSON contract')
    init = sub.add_parser('init', help='freeze template bytes/hash; empty deck revision 0')
    init.add_argument('--template', required=True); init.add_argument('--workspace', required=True)
    init.add_argument('--page-constraints', help='inline JSON: {"mode":"exact","count":5}; also auto/target/maximum')
    for name in ('inspect', 'status', 'apply', 'export', 'render', 'review', 'verify'):
        p = sub.add_parser(name); p.add_argument('--workspace', required=True)
        if name == 'inspect':
            p.add_argument('--offset', type=int, default=0); p.add_argument('--limit', type=int, default=20)
            p.add_argument('--details', action='store_true', help='include raw OOXML inheritance evidence and per-run records')
        if name == 'apply': p.add_argument('--request', required=True)
        if name == 'review': p.add_argument('--review', required=True)
        if name == 'render': p.add_argument('--render-engine', choices=['auto', 'libreoffice'], default='auto')
    args = parser.parse_args(argv)
    try:
        name = args.command
        if name == 'capabilities': result = capabilities()
        elif name == 'init': result = runtime.init(args.template, args.workspace, strict_json(args.page_constraints.encode()) if args.page_constraints else None)
        elif name == 'inspect': result = runtime.inspect(args.workspace, args.offset, args.limit, details=args.details)
        elif name == 'apply': result = runtime.apply(args.workspace, strict_json(read_file(args.request)))
        elif name == 'review': result = review_module.review(args.workspace, strict_json(read_file(args.review)))
        elif name == 'render': result = review_module.render(args.workspace, args.render_engine)
        elif name == 'verify': result = review_module.verify(args.workspace)
        else: result = getattr(runtime, name)(args.workspace)
        print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
        return 0 if result.get('ok') else 1
    except Exception as exc:
        # Inputs are untrusted. Return machine-readable rejection, never partial success.
        print(json.dumps({'ok': False, 'status': 'rejected', 'code': type(exc).__name__, 'error': str(exc)}, ensure_ascii=False))
        return 1
