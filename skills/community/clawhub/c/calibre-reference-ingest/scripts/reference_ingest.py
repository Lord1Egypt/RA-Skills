#!/usr/bin/env python3
"""Prepare and import one reference. No downloader, crawler, server, or auto-update."""
import argparse
from contextlib import contextmanager
from datetime import date
import hashlib
import html
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit, unquote
import uuid
import xml.etree.ElementTree as ET
import zipfile
from ebook_archive import EBOOK_EXTENSIONS, safe_name

DC = 'http://purl.org/dc/elements/1.1/'
OPF = 'http://www.idpf.org/2007/opf'
NS = {'dc': DC, 'opf': OPF}
ET.register_namespace('dc', DC)
ET.register_namespace('opf', OPF)
MAX_BYTES = 200 * 1024 * 1024
TRACKING = {'fbclid', 'gclid', 'dclid', 'msclkid', 'mc_cid', 'mc_eid'}
SECRET_QUERY = re.compile(r'(^|[-_])(token|password|secret|signature|credential|key|auth|session)([-_]|$)', re.I)
FIELDS = {'file', 'source_url', 'canonical_url', 'title', 'authors',
          'tags', 'language', 'kind', 'coverage', 'capture_method', 'publisher',
          'published_date', 'version', 'summary', 'location', 'notes', 'doi', 'archive_member', 'archive_sha256'}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def clean(value, name, limit=2000):
    require(isinstance(value, str), name + ' must be a string')
    value = unicodedata.normalize('NFC', value.strip())
    require(value and len(value) <= limit, name + ' is empty or too long')
    require(not re.search(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', value), name + ' contains control characters')
    return value


def canonical_url(value):
    value = clean(value, 'URL', 8000)
    require(not re.search(r'\s', value), 'URL contains whitespace')
    u = urlsplit(value)
    require(u.scheme.lower() in ('http', 'https') and u.hostname, 'source must be an http(s) URL')
    require(not u.username and not u.password, 'source URL must not contain credentials')
    host = u.hostname.encode('idna').decode('ascii').lower()
    if ':' in host:
        host = '[' + host + ']'
    if u.port and not ((u.scheme.lower() == 'http' and u.port == 80) or (u.scheme.lower() == 'https' and u.port == 443)):
        host += ':' + str(u.port)
    pairs = parse_qsl(u.query, keep_blank_values=True)
    require(all(not SECRET_QUERY.search(k) for k, _ in pairs), 'source URL contains a sensitive query; use a clean landing URL')
    pairs = [(k, v) for k, v in pairs if not k.lower().startswith('utm_') and k.lower() not in TRACKING]
    # Keep functional parameters, order, scheme, path case, version, language and trailing slash.
    return urlunsplit((u.scheme.lower(), host, u.path or '/', urlencode(pairs), ''))


def normalize(raw):
    require(isinstance(raw, dict), 'input must be an object')
    require(not set(raw) - FIELDS, 'unknown input fields: ' + ', '.join(sorted(set(raw) - FIELDS)))
    m = dict(raw)
    for key in ('file', 'title', 'language', 'kind', 'coverage', 'capture_method'):
        m[key] = clean(m.get(key), key)
    m['source_url'] = canonical_url(m.get('source_url'))
    m['canonical_url'] = canonical_url(m.get('canonical_url', m['source_url']))
    require(m['coverage'] in ('full', 'partial'), 'coverage must be full or partial; synthesized summary books are excluded')
    require(re.fullmatch(r'[a-z]{3}', m['language']), 'language must be a three-letter ISO 639 code, e.g. jpn/eng')
    for key, count in (('authors', 30), ('tags', 12)):
        values = m.get(key)
        require(isinstance(values, list) and 1 <= len(values) <= count, key + ' must be a nonempty bounded array')
        values = [clean(v, key, 200) for v in values]
        require(len({v.casefold() for v in values}) == len(values), key + ' contains duplicates')
        require(all(not any(c in v for c in ('\n', '\r', '|', '&')) for v in values), key + ' contains unsupported delimiter')
        if key == 'tags':
            require(all(',' not in v for v in values), 'tag cannot contain a comma')
        m[key] = values
    if m['coverage'] != 'full':
        # Prefer the plain tag; retain legacy plans using the old dotted label.
        require(any(tag in m['tags'] for tag in ('抜粋', '状態.抜粋')),
                m['coverage'] + ' capture needs 抜粋 tag')
    for key in ('publisher', 'published_date', 'version', 'summary', 'location', 'notes', 'doi'):
        if key in m:
            m[key] = clean(m[key], key, 10000 if key in ('summary', 'notes') else 2000)
    if 'published_date' in m:
        require(re.fullmatch(r'\d{4}-\d{2}-\d{2}', m['published_date']), 'published_date must be YYYY-MM-DD')
        date.fromisoformat(m['published_date'])
    if 'doi' in m:
        m['doi'] = m['doi'].removeprefix('https://doi.org/').lower()
        require(re.fullmatch(r'10\.\d{4,9}/[^\s"\\]+', m['doi']), 'invalid DOI')
    require(('archive_member' in m) == ('archive_sha256' in m), 'archive_member and archive_sha256 must be supplied together')
    if 'archive_member' in m:
        m['archive_member'] = safe_name(m['archive_member'])
        require(isinstance(m['archive_sha256'], str) and re.fullmatch(r'[0-9a-f]{64}', m['archive_sha256']), 'invalid archive SHA256')
    return m


def digest_bytes(data):
    return hashlib.sha256(data).hexdigest()


def encoded(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')


def file_hash(path):
    with open(path, 'rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def save_new(path, data):
    with open(path, 'xb') as f:
        os.chmod(path, 0o600)
        f.write(data)
        f.flush()
        os.fsync(f.fileno())


def endpoint(value):
    require(bool(value), 'specify --with-library or CALIBRE_WITH_LIBRARY')
    if value.startswith(('http://', 'https://')):
        u = urlsplit(value)
        require(u.hostname and not u.username and not u.password and not u.query, 'invalid library URL')
        library = unquote(u.fragment)
        require(library and library != '-' and not library.startswith('library_id='), 'library URL needs CLI #LIBRARY_ID, not browser #library_id=')
        return urlunsplit((u.scheme, u.netloc, u.path, '', library))
    p = Path(value).expanduser().resolve()
    require((p / 'metadata.db').is_file(), 'local library must already contain metadata.db')
    return str(p)


class Calibre:
    def __init__(self, library, username=None, password_env='CALIBRE_PASSWORD'):
        self.library = endpoint(library)
        self.username = username or os.environ.get('CALIBRE_USERNAME', '')
        self.secret = os.environ.get(password_env, '')

    def run(self, *args):
        cmd = ['calibredb', *map(str, args), '--with-library', self.library, '--timeout', '120']
        if self.username:
            cmd += ['--username', self.username]
        if self.secret:
            cmd += ['--password', '<stdin>']
        env = {k: os.environ[k] for k in ('PATH', 'HOME', 'LANG', 'LC_ALL', 'SYSTEMROOT', 'WINDIR', 'CALIBRE_CONFIG_DIRECTORY', 'QT_QPA_PLATFORM') if k in os.environ}
        try:
            p = subprocess.run(cmd, input=self.secret, text=True, capture_output=True, timeout=150, env=env)
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise RuntimeError('calibredb could not complete; inspect any apply receipt before retrying') from exc
        if p.returncode:
            detail = (p.stderr or p.stdout)[-1200:]
            if self.secret:
                detail = detail.replace(self.secret, '[REDACTED]')
            raise RuntimeError('calibredb failed: ' + detail)
        return p.stdout

    def rows(self, query):
        data = json.loads(self.run('list', '--for-machine', '--fields', 'title,authors,tags,identifiers,formats', '--search', query, '--limit', '101'))
        require(isinstance(data, list) and len(data) < 101, 'candidate lookup incomplete; refine/review manually')
        return data


def quoted(value):
    return '"' + value.replace('\\', '\\\\').replace('"', '\\"') + '"'


def identifier_query(key, value):
    return 'identifiers:' + quoted('=' + key + ':' + value)


def candidates(db, plan):
    identifiers = {k: v for k, v in plan['identifiers'].items() if k != 'refimport' and not (k == 'url' and plan['metadata'].get('archive_member'))}
    query = ' or '.join([identifier_query(k, v) for k, v in identifiers.items() if k != 'refimport'] + ['title:' + quoted('=' + plan['metadata']['title'])])
    rows = db.rows(query)
    return [{'id': r['id'], 'title': r['title'], 'authors': r.get('authors'), 'tags': r.get('tags', []),
             'identifiers': r.get('identifiers', {}),
             'reason': 'source_or_content_match' if any(r.get('identifiers', {}).get(k) == v for k, v in identifiers.items() if k != 'refimport') else 'title_candidate'} for r in rows]


def comments(m):
    labels = [('source_url', '出典URL'), ('canonical_url', '正規URL'),
              ('archive_member', '圧縮ファイル内の書籍'), ('archive_sha256', '元圧縮ファイルSHA256'),
              ('kind', '資料種別'), ('version', '公開版'), ('coverage', '収録範囲'), ('capture_method', '取得方法'),
              ('location', '参照箇所'), ('notes', '保存上の注意'), ('summary', '要約 (AI作成・原文とは別)')]
    parts = ['<div><h2>参照資料の保存記録</h2>']
    for key, label in labels:
        if m.get(key):
            text = html.escape(m[key])
            if key.endswith('_url'):
                text = '<a href="' + html.escape(m[key], quote=True) + '">' + text + '</a>'
            parts.append('<p><strong>' + label + ':</strong> ' + text + '</p>')
    parts.append('</div>')
    return ''.join(parts)


def make_opf(m, identifiers, epub=False):
    root = ET.Element('{' + OPF + '}package', {'version': '2.0', 'unique-identifier': 'book-id'})
    meta = ET.SubElement(root, '{' + OPF + '}metadata')
    def dc(key, value, attrs=None):
        ET.SubElement(meta, '{' + DC + '}' + key, attrs or {}).text = value
    dc('title', m['title'])
    for author in m['authors']:
        dc('creator', author, {'{' + OPF + '}role': 'aut'})
    dc('language', m['language'])
    for tag in m['tags']:
        dc('subject', tag)
    dc('description', comments(m))
    if m.get('publisher'):
        dc('publisher', m['publisher'])
    if m.get('published_date'):
        dc('date', m['published_date'] + 'T00:00:00+00:00')
    for key, value in identifiers.items():
        attrs = {'{' + OPF + '}scheme': key}
        if key == 'refimport':
            attrs['id'] = 'book-id'
        dc('identifier', value, attrs)
    if epub:
        manifest = ET.SubElement(root, '{' + OPF + '}manifest')
        ET.SubElement(manifest, '{' + OPF + '}item', {'id': 'content', 'href': 'content.xhtml', 'media-type': 'application/xhtml+xml'})
        ET.SubElement(manifest, '{' + OPF + '}item', {'id': 'ncx', 'href': 'toc.ncx', 'media-type': 'application/x-dtbncx+xml'})
        spine = ET.SubElement(root, '{' + OPF + '}spine', {'toc': 'ncx'})
        ET.SubElement(spine, '{' + OPF + '}itemref', {'idref': 'content'})
    return ET.tostring(root, encoding='utf-8', xml_declaration=True)


def inspect_source(path):
    require(path.is_file() and 0 < path.stat().st_size <= MAX_BYTES, 'source missing, empty, or larger than 200 MiB')
    ext = path.suffix.lower()
    require(ext in EBOOK_EXTENSIONS, 'ebook originals only: ' + ', '.join(sorted(EBOOK_EXTENSIONS)) + '; no Web clips, HTML, TXT, MD or generated summaries')
    with path.open('rb') as f:
        head = f.read(65536)
    if ext == '.pdf':
        require(head.startswith(b'%PDF-'), 'not a PDF (possible HTML/login/error page)')
    elif ext in ('.epub', '.kepub'):
        with zipfile.ZipFile(path) as z:
            require(z.getinfo('mimetype').file_size < 100 and z.read('mimetype').strip() == b'application/epub+zip', 'not an EPUB')
            require('META-INF/container.xml' in z.namelist(), 'EPUB container missing')
    elif ext in ('.mobi', '.azw', '.azw3', '.azw4', '.prc'):
        require(head[60:68] in (b'BOOKMOBI', b'TEXtREAd'), 'not a recognized MOBI/Kindle/PRC header')
    elif ext == '.fb2':
        require(re.search(rb'<(?:[A-Za-z0-9_]+:)?FictionBook\b', head), 'not an FB2 document')
    elif ext == '.djvu':
        require(head.startswith(b'AT&TFORM') and head[12:16] in (b'DJVU', b'DJVM'), 'not a DjVu document')
    elif ext == '.cbz':
        with zipfile.ZipFile(path) as z:
            require(any(Path(n).suffix.lower() in ('.jpg', '.jpeg', '.png', '.webp', '.gif') for n in z.namelist()), 'CBZ contains no recognized image pages')
    elif ext == '.cbr':
        require(head.startswith(b'Rar!\x1a\x07'), 'not a RAR-based comic')
    elif ext == '.cb7':
        require(head.startswith(b'7z\xbc\xaf\x27\x1c'), 'not a 7z-based comic')
    return ext


def prepare(args):
    raw = json.loads(Path(args.input_json).read_text(encoding='utf-8'))
    m = normalize(raw)
    source = Path(m['file']).expanduser()
    require(source.is_absolute(), 'file must be an absolute path')
    source = source.resolve()
    ext = inspect_source(source)
    db = Calibre(args.with_library, args.username, args.password_env)
    run = Path(args.run_dir).expanduser().resolve()
    require(not run.exists(), 'run directory already exists; never overwrite a plan')
    run.mkdir(parents=True, mode=0o700)
    copied = run / ('source' + ext)
    # Stage the source first; identifiers bind these exact bytes, not the moving original.
    with source.open('rb') as src, copied.open('xb') as dst:
        os.chmod(copied, 0o600)
        shutil.copyfileobj(src, dst)
    inspect_source(copied)
    source_sha = file_hash(copied)
    identifiers = {'refsource': digest_bytes((m['canonical_url'] + ('\n' + m['archive_member'] if m.get('archive_member') else '')).encode()), 'refsha256': source_sha,
                   'refimport': uuid.uuid4().hex, 'url': m['canonical_url']}
    if m.get('doi'):
        identifiers['doi'] = m['doi']
    artifact = copied
    opf = run / 'metadata.opf'
    save_new(opf, make_opf(m, identifiers))
    plan = {'schema': 2, 'library': db.library, 'metadata': m, 'identifiers': identifiers,
            'source_file': copied.name, 'source_sha256': source_sha,
            'artifact_file': artifact.name, 'artifact_sha256': file_hash(artifact),
            'opf_file': opf.name, 'opf_sha256': file_hash(opf)}
    matches = candidates(db, plan)
    plan['candidates'] = matches
    plan['decision'] = 'review_existing' if matches else 'new'
    envelope = {'plan': plan, 'digest': digest_bytes(encoded(plan))}
    save_new(run / 'plan.json', encoded(envelope) + b'\n')
    return {'ok': True, 'status': 'prepared', 'decision': plan['decision'], 'plan_file': str(run / 'plan.json'),
            'plan_digest': envelope['digest'], 'metadata': m, 'candidates': matches}


def load_plan(path, require_staged=True):
    path = Path(path).expanduser().resolve()
    envelope = json.loads(path.read_text(encoding='utf-8'))
    p = envelope['plan']
    require(p.get('schema') == 2 and envelope['digest'] == digest_bytes(encoded(p)), 'plan changed or unsupported schema')
    for field in ('source', 'artifact', 'opf'):
        name = p[field + '_file']
        require(Path(name).name == name and name not in ('.', '..'), 'invalid staged path')
        f = path.parent / name
        if require_staged:
            require(not f.is_symlink() and f.is_file() and file_hash(f) == p[field + '_sha256'], 'staged ' + field + ' missing or changed')
    normalize(p['metadata'])
    require(p['source_file'] == p['artifact_file'], 'only original ebooks may be imported; legacy Web-clip plans are not supported')
    if require_staged:
        inspect_source(path.parent / p['source_file'])
    return path, p, envelope['digest']


def find_import(db, p):
    token = p['identifiers']['refimport']
    return [r for r in db.rows(identifier_query('refimport', token)) if r.get('identifiers', {}).get('refimport') == token]


def verify(db, p):
    rows = find_import(db, p)
    require(len(rows) == 1, 'expected exactly one imported record; inspect library and receipt')
    row = rows[0]
    root = ET.fromstring(db.run('show_metadata', row['id'], '--as-opf'))
    def values(key):
        return [e.text or '' for e in root.findall('.//dc:' + key, NS)]
    m = p['metadata']
    ids = {e.get('{' + OPF + '}scheme', '').lower(): e.text for e in root.findall('.//dc:identifier', NS)}
    require(values('title') == [m['title']], 'title readback mismatch')
    require(values('creator') == m['authors'], 'authors readback mismatch')
    require(set(values('subject')) == set(m['tags']), 'tags readback mismatch')
    require(values('language') == [m['language']], 'language readback mismatch')
    require(all(ids.get(k) == v for k, v in p['identifiers'].items()), 'identifier readback mismatch')
    require(values('description') == [comments(m)], 'comments readback mismatch')
    if m.get('publisher'):
        require(values('publisher') == [m['publisher']], 'publisher readback mismatch')
    if m.get('published_date'):
        require(any(v[:10] == m['published_date'] for v in values('date')), 'publication date readback mismatch')
    expected_format = Path(p['artifact_file']).suffix.upper().lstrip('.')
    require(any(str(f).upper().endswith('.' + expected_format) or str(f).upper() == expected_format for f in row.get('formats', [])), 'format missing from library')
    return {'id': row['id'], 'title': m['title'], 'tags': m['tags'], 'format': expected_format}


@contextmanager
def library_lock(root, library):
    root.mkdir(parents=True, exist_ok=True, mode=0o700)
    lock = root / (digest_bytes(library.encode()) + '.lock')
    save_new(lock, encoded({'pid': os.getpid(), 'library': library}))
    try:
        yield
    finally:
        lock.unlink()


def receipt_event(f, event):
    f.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + '\n')
    f.flush()
    os.fsync(f.fileno())


def apply_plan(args):
    path, p, digest = load_plan(args.plan_file)
    require(p['decision'] == 'new' and not p['candidates'], 'existing candidate needs review; this plan cannot import')
    if args.with_library:
        require(endpoint(args.with_library) == p['library'], 'plan targets a different library')
    db = Calibre(p['library'], args.username, args.password_env)
    receipt = path.parent / 'apply-receipt.jsonl'
    state = Path(args.state_dir).expanduser().resolve()
    with library_lock(state, db.library):
        require(not receipt.exists(), 'an attempt already exists; inspect receipt and use verify, never blindly retry')
        require(not candidates(db, p), 'new duplicate/title candidate appeared since preparation; no writes performed')
        with receipt.open('x', encoding='utf-8') as log:
            os.chmod(receipt, 0o600)
            receipt_event(log, {'event': 'intent', 'digest': digest, 'library': db.library, 'refimport': p['identifiers']['refimport']})
            try:
                m = p['metadata']
                argv = ['add', '--title', m['title'], '--authors', ' & '.join(m['authors']), '--tags', ','.join(m['tags']), '--languages', m['language']]
                for key, value in p['identifiers'].items():
                    argv += ['--identifier', key + ':' + value]
                argv += [str(path.parent / p['artifact_file'])]
                db.run(*argv)  # Never --duplicates, --automerge or an overwrite option.
                rows = find_import(db, p)
                require(len(rows) == 1, 'add outcome ambiguous or refused; inspect receipt/library before any new attempt')
                book_id = rows[0]['id']
                receipt_event(log, {'event': 'added', 'id': book_id})
                # Only this newly imported, token-identified book may receive our OPF.
                db.run('set_metadata', book_id, str(path.parent / p['opf_file']))
                actual = verify(db, p)
                receipt_event(log, {'event': 'verified', **actual})
                return {'ok': True, 'status': 'imported_verified', 'library': db.library, 'receipt_file': str(receipt), **actual}
            except Exception as exc:
                receipt_event(log, {'event': 'failed_or_unverified', 'error': str(exc)})
                raise


def cleanup_plan(args):
    path, p, digest = load_plan(args.plan_file, require_staged=False)
    if args.with_library:
        require(endpoint(args.with_library) == p['library'], 'plan targets a different library')
    db = Calibre(p['library'], args.username, args.password_env)
    receipt = path.parent / 'apply-receipt.jsonl'
    require(receipt.is_file() and not receipt.is_symlink(), 'verified apply receipt required before cleanup')
    events = [json.loads(line) for line in receipt.read_text(encoding='utf-8').splitlines() if line.strip()]
    require(events and events[0].get('event') == 'intent' and events[0].get('digest') == digest, 'receipt does not match this plan')
    with library_lock(Path(args.state_dir).expanduser().resolve(), db.library):
        actual = verify(db, p)
        require(any(e.get('event') == 'verified' and e.get('id') == actual['id'] for e in events), 'import has not been verified; keep files for recovery')
        source = path.parent / p['source_file']
        if source.exists() or source.is_symlink():
            require(not source.is_symlink() and source.is_file() and file_hash(source) == p['source_sha256'], 'staged source changed; do not clean it up')
        # Verify the library's actual stored bytes, not just a format/identifier label.
        # This export is an owned temporary verification copy, never a new backup.
        with tempfile.TemporaryDirectory(prefix='calibre-copy-check-') as tmp:
            db.run('export', actual['id'], '--to-dir', tmp, '--single-dir',
                   '--formats', actual['format'], '--dont-update-metadata',
                   '--dont-save-cover', '--dont-write-opf', '--dont-save-extra-files')
            exported = [f for f in Path(tmp).iterdir() if f.is_file() and not f.is_symlink() and f.suffix.upper() == '.' + actual['format']]
            require(len(exported) == 1 and file_hash(exported[0]) == p['artifact_sha256'], 'library file missing or byte mismatch; retain local files')
        targets = [source] if source.exists() else []
        if not args.apply:
            return {'ok': True, 'status': 'cleanup_ready', 'id': actual['id'], 'files': list(map(str, targets)), 'library_bytes_verified': True}
        if targets:
            require(not source.is_symlink() and source.is_file() and file_hash(source) == p['source_sha256'], 'staged source changed during verification; do not clean it up')
            require(shutil.which('trash'), 'trash is required for reversible cleanup; never fall back to permanent deletion')
            try:
                cp = subprocess.run(['trash', '--', *map(str, targets)], capture_output=True, text=True, timeout=60)
            except (OSError, subprocess.TimeoutExpired) as exc:
                raise RuntimeError('cleanup could not complete; inspect source/trash state before retrying') from exc
            require(cp.returncode == 0 and all(not f.exists() for f in targets), 'trash cleanup failed; inspect local state')
        with receipt.open('a', encoding='utf-8') as log:
            receipt_event(log, {'event': 'staged_copy_cleaned', 'id': actual['id'], 'source_sha256': p['source_sha256'], 'library_bytes_verified': True})
        return {'ok': True, 'status': 'staged_copy_cleaned', 'id': actual['id'],
                'library_bytes_verified': True, 'trashed_files': list(map(str, targets)),
                'receipt_file': str(receipt), 'input_file_untouched': p['metadata']['file']}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest='command', required=True)
    for name in ('prepare', 'apply', 'verify', 'cleanup'):
        sub = subs.add_parser(name)
        sub.add_argument('--with-library', default=os.environ.get('CALIBRE_WITH_LIBRARY') if name == 'prepare' else None)
        sub.add_argument('--username')
        sub.add_argument('--password-env', default='CALIBRE_PASSWORD')
        if name == 'prepare':
            sub.add_argument('--input-json', required=True)
            sub.add_argument('--run-dir', required=True)
        else:
            sub.add_argument('--plan-file', required=True)
        if name in ('apply', 'cleanup'):
            sub.add_argument('--apply', action='store_true', required=name == 'apply')
            sub.add_argument('--state-dir', default=os.path.join(os.environ.get('XDG_STATE_HOME', os.path.expanduser('~/.local/state')), 'calibre-reference-ingest', 'locks'))
    args = parser.parse_args(argv)
    try:
        if args.command == 'prepare':
            result = prepare(args)
        elif args.command == 'apply':
            result = apply_plan(args)
        elif args.command == 'cleanup':
            result = cleanup_plan(args)
        else:
            _, p, _ = load_plan(args.plan_file, require_staged=False)
            if args.with_library:
                require(endpoint(args.with_library) == p['library'], 'plan targets a different library')
            result = {'ok': True, 'status': 'verified', **verify(Calibre(p['library'], args.username, args.password_env), p)}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:
        print(json.dumps({'ok': False, 'error': str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
