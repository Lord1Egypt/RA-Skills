"""Real render evidence; external observations never substitute for missing evidence."""
from __future__ import annotations
import io
import os
import tempfile
from pathlib import Path
from pptx import Presentation
from .safety import require, fields, strict_json, encode, sha, read_file, atomic, locked, safe_path
from .runtime import load, current_candidate, state_hash
from .package import slide_inventory, package
from engine.visual_review import _template_page_review

CRITERIA = ('hierarchy', 'reading_order', 'template_match', 'readability', 'content', 'editability')


def _images(root, report):
    for page in report.get('slides', []):
        path = safe_path(page['image'])
        require(path.is_relative_to(root), 'PREVIEW_OUTSIDE_WORKSPACE')
        page['sha256'] = sha(read_file(path))
    return report


def render(workspace, engine='auto'):
    require(engine in {'auto', 'libreoffice'}, 'UNSUPPORTED_RENDER_ENGINE')
    from .rendering import run_render_report
    with locked(workspace) as root:
        state, template = load(root); candidate = current_candidate(root, state)
        # Use a fresh directory so no stale renderer output can be accepted.
        run_dir = Path(tempfile.mkdtemp(prefix='render-', dir=root))
        tempdir = run_dir / 'tmp'; tempdir.mkdir()
        previous_tmp = tempfile.tempdir
        old_env = {k: os.environ.get(k) for k in ('TMPDIR', 'TMP', 'TEMP')}
        try:
            tempfile.tempdir = str(tempdir)
            for key in old_env: os.environ[key] = str(tempdir)
            pres = Presentation(io.BytesIO(template))
            aspect = pres.slide_width / pres.slide_height
            pixels_per_page = pres.slide_width / 914400 * pres.slide_height / 914400 * 144 * 144
            require(pixels_per_page * max(len(pres.slides), len(state['pages'])) <= 200000000, 'RENDER_PIXEL_BUDGET_EXCEEDED')
            # The same exact candidate bytes exported above are supplied to renderer.
            actual = run_render_report(root / 'candidate.pptx', run_dir / 'candidate', engine=engine,
                                       expected_slides=len(state['pages']), expected_aspect=aspect)
            source = run_render_report(root / 'template.pptx', run_dir / 'source', engine=engine,
                                       expected_slides=len(pres.slides), expected_aspect=aspect)
        finally:
            tempfile.tempdir = previous_tmp
            for key, value in old_env.items():
                if value is None: os.environ.pop(key, None)
                else: os.environ[key] = value
        _images(root, actual); _images(root, source)
        current_candidate(root, state)
        require(sha(read_file(root / 'template.pptx')) == state['templateHash'], 'TEMPLATE_CHANGED_DURING_RENDER')
        status = 'passed' if actual.get('status') == source.get('status') == 'passed' else 'unavailable' if 'unavailable' in {actual.get('status'), source.get('status')} else 'failed'
        sources = {sid: i + 1 for i, (sid, _) in enumerate(slide_inventory(package(template)))}
        references = {p['slide_index']: p for p in source.get('slides', [])}
        slides = []
        for i, p in enumerate(actual.get('slides', [])):
            if i >= len(state['pages']): break
            page = state['pages'][i]; ref = references.get(sources[page['sourceSlideId']], {})
            slides.append({**p, 'pageId': page['id'], 'sourceSlideId': page['sourceSlideId'],
                           'referenceImage': ref.get('image'), 'referenceHash': ref.get('sha256')})
        result = {'ok': status == 'passed', 'status': status, 'revision': state['revision'],
                  'stateHash': state_hash(state), 'candidateHash': candidate['candidateHash'], 'templateHash': state['templateHash'],
                  'slides': slides, 'candidateRender': actual, 'sourceRender': source}
        atomic(root / 'render-report.json', encode(result))
        return result


def evidence(root, state):
    candidate = current_candidate(root, state)
    report = strict_json(read_file(root / 'render-report.json'))
    require(report.get('status') == 'passed' and report.get('ok') is True, 'REAL_RENDER_REQUIRED')
    require(report.get('revision') == state['revision'] and report.get('stateHash') == state_hash(state), 'STALE_RENDER')
    require(report.get('candidateHash') == candidate['candidateHash'] and report.get('templateHash') == state['templateHash'], 'RENDER_HASH_MISMATCH')
    slides = report.get('slides', [])
    require(len(slides) == len(state['pages']), 'RENDER_PAGE_COVERAGE')
    for i, (p, s) in enumerate(zip(slides, state['pages']), 1):
        require(p.get('slide_index') == i and p.get('pageId') == s['id'] and p.get('sourceSlideId') == s['sourceSlideId'], 'RENDER_PAGE_BINDING_MISMATCH')
        for path_key, hash_key in [('image', 'sha256'), ('referenceImage', 'referenceHash')]:
            path = safe_path(p[path_key]); require(path.is_relative_to(root), 'PREVIEW_OUTSIDE_WORKSPACE')
            require(sha(read_file(path)) == p[hash_key], 'STALE_PREVIEW_HASH')
    # Check every source/candidate image, including non-selected source previews.
    for key in ('candidateRender', 'sourceRender'):
        require(report.get(key, {}).get('status') == 'passed', 'REAL_RENDER_REQUIRED')
        for p in report[key].get('slides', []):
            path = safe_path(p['image']); require(path.is_relative_to(root), 'PREVIEW_OUTSIDE_WORKSPACE')
            require(sha(read_file(path)) == p['sha256'], 'STALE_PREVIEW_HASH')
    return candidate, report


def validate_review(root, state, review):
    fields(review, {'schema_version', 'status', 'candidateHash', 'templateHash', 'renderReportHash', 'reviewer', 'pages', 'deck_rhythm'},
           {'schema_version', 'status', 'candidateHash', 'templateHash', 'renderReportHash', 'reviewer', 'pages', 'deck_rhythm'})
    candidate, rendered = evidence(root, state)
    require(review['schema_version'] == '1.0.0' and review['status'] in {'approved', 'revise', 'rejected'}, 'INVALID_REVIEW')
    require(review['candidateHash'] == candidate['candidateHash'] and review['templateHash'] == state['templateHash'], 'REVIEW_HASH_MISMATCH')
    require(review['renderReportHash'] == sha(read_file(root / 'render-report.json')), 'STALE_REVIEW_RENDER_HASH')
    fields(review['reviewer'], {'provider', 'model', 'method'}, {'provider', 'model', 'method'})
    require(all(isinstance(v, str) and v.strip() for v in review['reviewer'].values()), 'REVIEWER_REQUIRED')
    require(isinstance(review['pages'], list), 'REVIEW_PAGES_REQUIRED')
    by_index = {p['slide_index']: p for p in rendered['slides']}
    for p in review['pages']:
        fields(p, {'slide_index', 'pageId', 'sourceSlideId', 'preview_sha256', 'reference_sha256', *CRITERIA},
               {'slide_index', 'pageId', 'sourceSlideId', 'preview_sha256', 'reference_sha256', *CRITERIA})
        require(type(p['slide_index']) is int and p['slide_index'] in by_index, 'INVALID_REVIEW_PAGE')
        actual = by_index[p['slide_index']]
        require(p['pageId'] == actual['pageId'] and p['sourceSlideId'] == actual['sourceSlideId'] and p['reference_sha256'] == actual['referenceHash'], 'REVIEW_SOURCE_BINDING_MISMATCH')
        for key in CRITERIA: fields(p[key], {'status', 'observation'}, {'status', 'observation'})
    # Reuse the existing strict six-observation gate; do not fabricate its visual floors.
    rejected = _template_page_review(rendered, review)
    require(rejected is None, (rejected or {}).get('code', 'REVIEW_REJECTED'))
    return review['status'] == 'approved'


def review(workspace, document):
    strict_json(encode(document))
    with locked(workspace) as root:
        state, _ = load(root)
        approved = validate_review(root, state, document)
        record = {'review': document, 'revision': state['revision'], 'stateHash': state_hash(state),
                  'reviewerIdentityAuthenticated': False, 'automaticFactChecking': False,
                  'reviewReuse': False}
        atomic(root / 'review.json', encode(record))
        return {'ok': approved, 'status': 'external_review_recorded' if approved else 'refinement_required',
                'reviewerIdentityAuthenticated': False, 'next': 'verify', 'reviewHash': sha(encode(record))}


def verify(workspace):
    with locked(workspace) as root:
        state, template = load(root)
        candidate = current_candidate(root, state)
        from .floor import check
        floor = check(template, read_file(root / 'candidate.pptx'), state)
        require(floor['status'] == 'passed', 'PRESERVATION_FLOOR_BLOCKED: ' + ','.join(sorted({i['code'] for i in floor['issues']})))
        fidelity = candidate['templateFidelity']
        require(fidelity['status'] == 'passed', 'TEMPLATE_FIDELITY_BLOCKED: ' + ','.join(sorted({i['code'] for i in fidelity['findings']})))
        record = strict_json(read_file(root / 'review.json'))
        require(record.get('revision') == state['revision'] and record.get('stateHash') == state_hash(state), 'STALE_REVIEW')
        require(validate_review(root, state, record['review']), 'EXTERNAL_REVIEW_NOT_APPROVED')
        return {'ok': True, 'status': 'final_delivery_ready', 'candidate': str(root / 'candidate.pptx'),
                'candidateHash': sha(read_file(root / 'candidate.pptx')), 'reviewHash': sha(read_file(root / 'review.json')),
                'reviewerIdentityAuthenticated': False, 'automaticFactChecking': False,
                'officeWpsCompatibilityActuallyVerified': False,
                'compatibility': {'powerpoint': 'not_tested', 'wps': 'not_tested'},
                'qualityFloor': 'source_preservation_fidelity_and_external_observations', 'templateFidelity': fidelity,
                'preservationFloor': floor, 'scope': 'native_template_toolchain_only',
                'skillBusinessAcceptance': 'not_assessed'}
