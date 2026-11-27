"""Real render evidence; external observations never substitute for missing evidence."""
from __future__ import annotations
import io
import json
import os
import re
import tempfile
from pathlib import Path
from pptx import Presentation
from .safety import require, fields, strict_json, encode, sha, read_file, atomic, locked, safe_path
from .runtime import load, current_candidate, state_hash
from .package import slide_inventory, package
from engine.visual_review import _template_page_review

CRITERIA = ('hierarchy', 'reading_order', 'template_match', 'readability', 'content', 'editability')
PLACEHOLDER_REVIEWERS = {'REPLACE_WITH_REVIEWER_PROVIDER', 'REPLACE_WITH_INDEPENDENT_REVIEWER'}
SHA_RE = re.compile(r'^sha256:[0-9a-f]{64}$')


def _page_evidence(state, candidate, rendered):
    """Per-page cryptographic digest binding template, render engine, position, edits, images and fidelity."""
    pages_by_id = {p['id']: p for p in state['pages']}
    fidelity_by_id = {p['pageId']: p for p in candidate.get('templateFidelity', {}).get('pages', [])}
    render_engine = rendered.get('candidateRender', {}).get('engine')
    result = {}
    for slide in rendered.get('slides', []):
        pid = slide['pageId']
        page_state = pages_by_id.get(pid)
        if page_state is None:
            continue
        record = {
            'templateHash': state['templateHash'],
            'renderEngine': render_engine,
            'slide_index': slide['slide_index'],
            'pageId': pid,
            'sourceSlideId': slide['sourceSlideId'],
            'pageState': page_state,
            'preview_sha256': slide['sha256'],
            'reference_sha256': slide['referenceHash'],
            'fidelity': fidelity_by_id.get(pid),
        }
        result[pid] = sha(encode(record))
    return result


def _history_entry(root, review_hash):
    require(isinstance(review_hash, str) and SHA_RE.fullmatch(review_hash), 'INVALID_INHERIT_REVIEW_HASH')
    path = safe_path(root / 'review-history' / (review_hash.split(':', 1)[1] + '.json'))
    require(path.is_relative_to(root) and path.is_file(), 'INHERIT_SOURCE_NOT_RECORDED_IN_WORKSPACE')
    entry = strict_json(read_file(path))
    require(entry.get('reviewHash') == review_hash and sha(encode(entry.get('review'))) == review_hash,
            'INHERIT_ARCHIVE_HASH_MISMATCH')
    return entry


def _images(root, report):
    for page in report.get('slides', []):
        path = safe_path(page['image'])
        require(path.is_relative_to(root), 'PREVIEW_OUTSIDE_WORKSPACE')
        page['sha256'] = sha(read_file(path))
    return report


def _load_cached_source_render(root, template_hash, engine, expected_slides):
    cache_path = root / 'source-render-cache.json'
    if not cache_path.is_file():
        return None
    try:
        cached = strict_json(read_file(cache_path))
        if (cached.get('templateHash') != template_hash or cached.get('engine') != engine
                or cached.get('slideCount') != expected_slides):
            return None
        source = cached.get('sourceRender')
        if not isinstance(source, dict) or source.get('status') != 'passed':
            return None
        slides = source.get('slides', [])
        if len(slides) != expected_slides:
            return None
        for page in slides:
            path = safe_path(page['image'])
            require(path.is_relative_to(root), 'PREVIEW_OUTSIDE_WORKSPACE')
            require(sha(read_file(path)) == page['sha256'], 'STALE_PREVIEW_HASH')
        return source
    except (OSError, ValueError, KeyError, TypeError):
        return None


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
        source_cache_hit = False
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
            cached_source = _load_cached_source_render(root, state['templateHash'], engine, len(pres.slides))
            if cached_source is not None:
                source = cached_source
                source_cache_hit = True
            else:
                source = run_render_report(root / 'template.pptx', run_dir / 'source', engine=engine,
                                           expected_slides=len(pres.slides), expected_aspect=aspect)
        finally:
            tempfile.tempdir = previous_tmp
            for key, value in old_env.items():
                if value is None: os.environ.pop(key, None)
                else: os.environ[key] = value
        _images(root, actual)
        if not source_cache_hit:
            _images(root, source)
            if source.get('status') == 'passed':
                atomic(root / 'source-render-cache.json', encode({
                    'templateHash': state['templateHash'], 'engine': engine,
                    'slideCount': len(pres.slides), 'sourceRender': source,
                }))
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
                  'sourceRenderCacheHit': source_cache_hit,
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
    require(all(isinstance(v, str) and v.strip() and v.strip() not in PLACEHOLDER_REVIEWERS
                for v in review['reviewer'].values()), 'REVIEWER_REQUIRED')
    require(isinstance(review['pages'], list), 'REVIEW_PAGES_REQUIRED')
    by_index = {p['slide_index']: p for p in rendered['slides']}
    current_ev = _page_evidence(state, candidate, rendered)
    archive_cache = {}
    for p in review['pages']:
        fields(p, {'slide_index', 'pageId', 'sourceSlideId', 'preview_sha256', 'reference_sha256', 'inherited_from', *CRITERIA},
               {'slide_index', 'pageId', 'sourceSlideId', 'preview_sha256', 'reference_sha256', *CRITERIA})
        require(type(p['slide_index']) is int and p['slide_index'] in by_index, 'INVALID_REVIEW_PAGE')
        actual = by_index[p['slide_index']]
        require(p['pageId'] == actual['pageId'] and p['sourceSlideId'] == actual['sourceSlideId'] and p['reference_sha256'] == actual['referenceHash'], 'REVIEW_SOURCE_BINDING_MISMATCH')
        for key in CRITERIA: fields(p[key], {'status', 'observation'}, {'status', 'observation'})
        if 'inherited_from' in p:
            ref = p['inherited_from']
            fields(ref, {'candidateHash', 'renderReportHash', 'reviewHash'},
                   {'candidateHash', 'renderReportHash', 'reviewHash'})
            rhash = ref['reviewHash']
            if rhash not in archive_cache:
                archive_cache[rhash] = _history_entry(root, rhash)
            archived = archive_cache[rhash]
            require(archived.get('templateHash') == state['templateHash']
                    and archived.get('candidateHash') == ref['candidateHash']
                    and archived.get('renderReportHash') == ref['renderReportHash']
                    and archived.get('candidateHash') != candidate['candidateHash'],
                    'INHERITED_REVIEW_BINDING_MISMATCH')
            pid = p['pageId']
            require(pid in current_ev and current_ev[pid] == archived.get('pageEvidence', {}).get(pid),
                    'INHERITED_PAGE_CHANGED: ' + pid)
            old_page = next((op for op in archived['review'].get('pages', []) if op.get('pageId') == pid), None)
            require(old_page is not None
                    and old_page.get('sourceSlideId') == actual['sourceSlideId']
                    and old_page.get('preview_sha256') == actual['sha256']
                    and old_page.get('reference_sha256') == actual['referenceHash'],
                    'INHERITED_PAGE_CHANGED: ' + pid)
            require(all(old_page[k]['status'] == 'pass' for k in CRITERIA), 'INHERITED_PAGE_NOT_PASSED: ' + pid)
            require({k: p[k] for k in CRITERIA} == {k: old_page[k] for k in CRITERIA},
                    'INHERITED_OBSERVATION_TAMPERED: ' + pid)
    # Reuse the existing strict six-observation gate; do not fabricate its visual floors.
    rejected = _template_page_review(rendered, review)
    require(rejected is None, (rejected or {}).get('code', 'REVIEW_REJECTED'))
    return review['status'] == 'approved'


def review_template(workspace, output=None, inherit_from=None):
    """Generate a hash-bound, failing-by-default review skeleton for the current rendered candidate.

    When ``inherit_from`` points to a previously recorded raw review JSON in this workspace,
    unchanged passing pages inherit their original observations with cryptographic provenance
    while ``status`` stays ``revise`` and ``deck_rhythm`` stays empty for fresh whole-deck review.
    """
    with locked(workspace) as root:
        state, _ = load(root)
        candidate, rendered = evidence(root, state)
        draft = {
            'schema_version': '1.0.0',
            'status': 'revise',
            'candidateHash': candidate['candidateHash'],
            'templateHash': state['templateHash'],
            'renderReportHash': sha(read_file(root / 'render-report.json')),
            'reviewer': {
                'provider': 'REPLACE_WITH_REVIEWER_PROVIDER',
                'model': 'REPLACE_WITH_INDEPENDENT_REVIEWER',
                'method': 'external visual comparison',
            },
            'pages': [
                {
                    'slide_index': p['slide_index'],
                    'pageId': p['pageId'],
                    'sourceSlideId': p['sourceSlideId'],
                    'preview_sha256': p['sha256'],
                    'reference_sha256': p['referenceHash'],
                    **{k: {'status': 'fail', 'observation': ''} for k in CRITERIA},
                }
                for p in rendered['slides']
            ],
            'deck_rhythm': '',
        }
        inherited_pages = []
        if inherit_from:
            previous = strict_json(read_file(inherit_from))
            if isinstance(previous, dict) and 'review' in previous and 'pages' not in previous:
                require(False, 'INHERIT_INPUT_MUST_BE_RAW: pass the original external review JSON, not workspace/review.json')
            prev_hash = sha(encode(previous))
            archived = _history_entry(root, prev_hash)
            require(archived.get('templateHash') == state['templateHash'], 'INHERIT_TEMPLATE_MISMATCH')
            require(archived.get('candidateHash') != candidate['candidateHash'], 'INHERIT_SAME_CANDIDATE')
            current_ev = _page_evidence(state, candidate, rendered)
            prev_pages = {p['pageId']: p for p in previous.get('pages', [])}
            for row in draft['pages']:
                pid = row['pageId']
                old_row = prev_pages.get(pid)
                if (old_row is None or pid not in current_ev
                        or current_ev[pid] != archived.get('pageEvidence', {}).get(pid)
                        or old_row.get('sourceSlideId') != row['sourceSlideId']
                        or old_row.get('preview_sha256') != row['preview_sha256']
                        or old_row.get('reference_sha256') != row['reference_sha256']
                        or not all(old_row.get(k, {}).get('status') == 'pass'
                                   and str(old_row.get(k, {}).get('observation', '')).strip() for k in CRITERIA)):
                    continue
                for key in CRITERIA:
                    row[key] = {'status': old_row[key]['status'], 'observation': old_row[key]['observation']}
                row['inherited_from'] = {
                    'candidateHash': archived['candidateHash'],
                    'renderReportHash': archived['renderReportHash'],
                    'reviewHash': prev_hash,
                }
                inherited_pages.append(pid)
        pages_requiring_review = [p['pageId'] for p in draft['pages'] if p['pageId'] not in inherited_pages]
        if output:
            target = safe_path(output)
            require(not target.exists(), 'OUTPUT_ALREADY_EXISTS')
            require(target.parent.is_dir(), 'OUTPUT_PARENT_REQUIRED')
            payload = (json.dumps(draft, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode('utf-8')
            atomic(target, payload)
            return {'ok': True, 'status': 'independent_review_required', 'file': str(target),
                    'pages': len(draft['pages']), 'candidateHash': draft['candidateHash'],
                    'renderReportHash': draft['renderReportHash'],
                    'inheritedPageCount': len(inherited_pages), 'inheritedPages': inherited_pages,
                    'pagesRequiringReview': pages_requiring_review}
        return {'ok': True, 'status': 'independent_review_required', 'review': draft,
                'inheritedPageCount': len(inherited_pages), 'inheritedPages': inherited_pages,
                'pagesRequiringReview': pages_requiring_review}


def review(workspace, document):
    strict_json(encode(document))
    with locked(workspace) as root:
        state, _ = load(root)
        approved = validate_review(root, state, document)
        candidate, rendered = evidence(root, state)
        doc_hash = sha(encode(document))
        history_dir = root / 'review-history'
        history_dir.mkdir(exist_ok=True)
        archive = {
            'reviewHash': doc_hash,
            'revision': state['revision'],
            'stateHash': state_hash(state),
            'candidateHash': candidate['candidateHash'],
            'templateHash': state['templateHash'],
            'renderReportHash': sha(read_file(root / 'render-report.json')),
            'pageEvidence': _page_evidence(state, candidate, rendered),
            'review': document,
        }
        atomic(history_dir / (doc_hash.split(':', 1)[1] + '.json'), encode(archive))
        inherited_ids = [p['pageId'] for p in document['pages'] if 'inherited_from' in p]
        record = {'review': document, 'revision': state['revision'], 'stateHash': state_hash(state),
                  'reviewerIdentityAuthenticated': False, 'automaticFactChecking': False,
                  'reviewReuse': bool(inherited_ids), 'inheritedPageIds': inherited_ids}
        atomic(root / 'review.json', encode(record))
        return {'ok': approved, 'status': 'external_review_recorded' if approved else 'refinement_required',
                'reviewerIdentityAuthenticated': False, 'next': 'verify', 'reviewHash': sha(encode(record)),
                'inheritedPageCount': len(inherited_ids)}


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
