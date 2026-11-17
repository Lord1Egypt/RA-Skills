import argparse
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET
import zipfile

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/reference_ingest.py'
sys.path.insert(0, str(SCRIPT.parent))
spec = importlib.util.spec_from_file_location('reference_ingest', SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def manifest(file='/tmp/source.txt', **kwargs):
    result = dict(file=str(file), source_url='https://example.org/docs?v=2', title='合成資料',
                  authors=['Doe, Jane', '試験著者'], tags=['資料', '種別.公式ドキュメント', 'Calibre'],
                  language='jpn', kind='公式ドキュメント', coverage='full', capture_method='本文抽出',
                  summary='Test <unsafe> & summary', publisher='試験出版', published_date='2024-02-29')
    result.update(kwargs)
    return result


def write_epub(path, body='Synthetic original ebook. 日本語の合成資料。'):
    import html
    m = mod.normalize(manifest(path))
    with zipfile.ZipFile(path, 'w') as z:
        z.writestr('mimetype', 'application/epub+zip', compress_type=zipfile.ZIP_STORED)
        z.writestr('META-INF/container.xml', '<?xml version="1.0"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="content.opf" media-type="application/oebps-package+xml"/></rootfiles></container>')
        z.writestr('content.opf', mod.make_opf(m, {'refimport': 'synthetic-fixture'}, True))
        z.writestr('content.xhtml', '<html xmlns="http://www.w3.org/1999/xhtml"><head><title>Test</title></head><body><p>' + html.escape(body) + '</p></body></html>')
        z.writestr('toc.ncx', '<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1"><head/><docTitle><text>Test</text></docTitle><navMap><navPoint id="one" playOrder="1"><navLabel><text>Test</text></navLabel><content src="content.xhtml"/></navPoint></navMap></ncx>')


class Helpers(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='reference-unit-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / 'article.epub'
        write_epub(self.source)
        self.input = self.root / 'input.json'
        self.input.write_text(json.dumps(manifest(self.source), ensure_ascii=False), encoding='utf-8')
        self.args = argparse.Namespace(input_json=str(self.input), run_dir=str(self.root / 'run'), with_library='https://library.example/#test', username=None, password_env='CALIBRE_PASSWORD')

    def prepared(self):
        with patch.object(mod.Calibre, 'rows', return_value=[]):
            result = mod.prepare(self.args)
        return Path(result['plan_file'])

    def test_canonical_preserves_functional_query(self):
        self.assertEqual(mod.canonical_url('HTTPS://Example.org:443/docs/?v=2&utm_source=x&lang=ja#part'), 'https://example.org/docs/?v=2&lang=ja')
        self.assertNotEqual(mod.canonical_url('http://example.org/docs'), mod.canonical_url('https://example.org/docs'))
        self.assertNotEqual(mod.canonical_url('https://example.org/docs/'), mod.canonical_url('https://example.org/docs'))

    def test_rejects_credential_urls(self):
        for url in ('https://a:b@example.org/doc', 'file:///etc/passwd', 'https://example.org/doc?access_token=x', 'https://example.org/doc?X-Amz-Signature=x', 'https://example.org/a b'):
            with self.subTest(url=url), self.assertRaises(ValueError):
                mod.canonical_url(url)

    def test_no_retrieval_timestamp_contract(self):
        self.assertNotIn('取得日時', mod.comments(mod.normalize(manifest())))
        for key in ('retrieved_at', 'acquired_at', 'timestamp'):
            with self.subTest(key=key), self.assertRaises(ValueError):
                mod.normalize(manifest(**{key: '2026-01-01'}))

    def test_valid_date_doi_and_author_comma(self):
        m = mod.normalize(manifest(doi='10.12345/ABC.123'))
        self.assertEqual(m['doi'], '10.12345/abc.123')
        self.assertEqual(m['authors'][0], 'Doe, Jane')
        for change in (dict(published_date='2025-02-29'), dict(doi='bad'), dict(authors=['A & B']), dict(tags=['資料', '資料']), dict(tags=['a,b'])):
            with self.subTest(change=change), self.assertRaises(ValueError):
                mod.normalize(manifest(**change))

    def test_partial_requires_label(self):
        with self.assertRaises(ValueError):
            mod.normalize(manifest(coverage='partial'))
        self.assertEqual(mod.normalize(manifest(coverage='partial', tags=['資料', '状態.抜粋']))['coverage'], 'partial')

    def test_summary_capture_is_excluded(self):
        with self.assertRaisesRegex(ValueError, 'summary books are excluded'):
            mod.normalize(manifest(coverage='summary', tags=['資料', '状態.要約']))

    def test_web_clip_inputs_are_excluded(self):
        for suffix in ('.html', '.md', '.txt', '.mhtml', '.htmlz'):
            f = self.root / ('web' + suffix)
            f.write_text('Captured webpage body')
            with self.subTest(suffix=suffix), self.assertRaisesRegex(ValueError, 'ebook originals only'):
                mod.inspect_source(f)

    def test_query_escapes_quotes(self):
        self.assertEqual(mod.quoted('a"b\\c'), '"a\\"b\\\\c"')

    def test_pdf_and_html_sanity_checks(self):
        bad = self.root / 'bad.pdf'; bad.write_text('<html>login</html>')
        with self.assertRaises(ValueError):
            mod.inspect_source(bad)
        bad = self.root / 'bad.txt'; bad.write_text('<!doctype html><html>error</html>')
        with self.assertRaises(ValueError):
            mod.inspect_source(bad)
        bad.write_text('x\x00y')
        with self.assertRaises(ValueError):
            mod.inspect_source(bad)

    def test_prepare_only_reads_calibre_and_epub_is_xml(self):
        with patch.object(mod.Calibre, 'rows', return_value=[]) as rows, patch.object(mod.Calibre, 'run', side_effect=AssertionError('unexpected mutation')):
            result = mod.prepare(self.args)
        self.assertEqual(result['decision'], 'new')
        rows.assert_called_once()
        p = Path(result['plan_file'])
        _, plan, _ = mod.load_plan(p)
        self.assertEqual(plan['source_sha256'], mod.file_hash(self.source))
        self.assertEqual((p.parent / 'source.epub').read_bytes(), self.source.read_bytes())
        with zipfile.ZipFile(p.parent / 'source.epub') as z:
            self.assertEqual(z.infolist()[0].filename, 'mimetype')
            self.assertEqual(z.infolist()[0].compress_type, zipfile.ZIP_STORED)
            for name in ('META-INF/container.xml', 'content.opf', 'content.xhtml', 'toc.ncx'):
                ET.fromstring(z.read(name))
            body = z.read('content.xhtml').decode()
            self.assertNotIn('取得日時', body)
        self.assertEqual(p.stat().st_mode & 0o777, 0o600)

    def test_legacy_web_plan_schema_is_rejected(self):
        plan_file = self.prepared()
        value = json.loads(plan_file.read_text())
        value['plan']['schema'] = 1
        value['digest'] = mod.digest_bytes(mod.encoded(value['plan']))
        plan_file.write_text(json.dumps(value))
        with self.assertRaisesRegex(ValueError, 'unsupported schema'):
            mod.load_plan(plan_file)

    def test_archive_provenance_fields_validate_together(self):
        with self.assertRaisesRegex(ValueError, 'supplied together'):
            mod.normalize(manifest(archive_member='book.epub'))
        with self.assertRaises(ValueError):
            mod.normalize(manifest(archive_member='../book.epub', archive_sha256='a' * 64))

    def test_additional_ebook_headers(self):
        cases = {'.mobi': b'x' * 60 + b'BOOKMOBI', '.azw3': b'x' * 60 + b'BOOKMOBI',
                 '.fb2': b'<?xml version="1.0"?><FictionBook></FictionBook>',
                 '.djvu': b'AT&TFORM' + b'\x00' * 4 + b'DJVU',
                 '.cbr': b'Rar!\x1a\x07\x00', '.cb7': b'7z\xbc\xaf\x27\x1c'}
        for ext, content in cases.items():
            path = self.root / ('book' + ext); path.write_bytes(content)
            self.assertEqual(mod.inspect_source(path), ext)
        fake = self.root / 'fake.mobi'; fake.write_text('<html>not a book</html>')
        with self.assertRaises(ValueError):
            mod.inspect_source(fake)

    def test_stage_changes_are_rejected(self):
        plan = self.prepared()
        (plan.parent / 'source.epub').write_text('tampered')
        with self.assertRaisesRegex(ValueError, 'changed'):
            mod.load_plan(plan)

    def test_modified_plan_is_rejected(self):
        plan = self.prepared()
        p = json.loads(plan.read_text()); p['plan']['metadata']['title'] = 'tampered'
        plan.write_text(json.dumps(p))
        with self.assertRaisesRegex(ValueError, 'plan changed'):
            mod.load_plan(plan)

    def test_existing_candidate_is_not_writable(self):
        with patch.object(mod.Calibre, 'rows', return_value=[{'id': 1, 'title': '合成資料'}]):
            result = mod.prepare(self.args)
        self.assertEqual(result['decision'], 'review_existing')
        args = argparse.Namespace(plan_file=result['plan_file'], with_library=None, username=None, password_env='CALIBRE_PASSWORD', state_dir=str(self.root / 'locks'))
        with self.assertRaisesRegex(ValueError, 'existing candidate'), patch.object(mod.Calibre, 'run', side_effect=AssertionError('write')):
            mod.apply_plan(args)

    def test_failed_add_receipt_blocks_retry(self):
        plan = self.prepared()
        args = argparse.Namespace(plan_file=str(plan), with_library=None, username=None, password_env='CALIBRE_PASSWORD', state_dir=str(self.root / 'locks'))
        with patch.object(mod.Calibre, 'rows', return_value=[]), patch.object(mod.Calibre, 'run', side_effect=RuntimeError('synthetic timeout')):
            with self.assertRaisesRegex(RuntimeError, 'synthetic timeout'):
                mod.apply_plan(args)
        events = [json.loads(line) for line in (plan.parent / 'apply-receipt.jsonl').read_text().splitlines()]
        self.assertEqual([e['event'] for e in events], ['intent', 'failed_or_unverified'])
        with patch.object(mod.Calibre, 'run', side_effect=AssertionError('write')), self.assertRaisesRegex(ValueError, 'attempt already exists'):
            mod.apply_plan(args)

    def test_new_candidate_since_prepare_stops_apply(self):
        plan = self.prepared()
        args = argparse.Namespace(plan_file=str(plan), with_library=None, username=None, password_env='CALIBRE_PASSWORD', state_dir=str(self.root / 'locks'))
        with patch.object(mod.Calibre, 'rows', return_value=[{'id': 3, 'title': '合成資料'}]), patch.object(mod.Calibre, 'run', side_effect=AssertionError('write')), self.assertRaisesRegex(ValueError, 'appeared'):
            mod.apply_plan(args)
        self.assertFalse((plan.parent / 'apply-receipt.jsonl').exists())

    def test_readback_failure_is_not_success(self):
        plan_file = self.prepared()
        _, plan, _ = mod.load_plan(plan_file)
        row = {'id': 7, 'identifiers': plan['identifiers'], 'formats': ['EPUB']}
        args = argparse.Namespace(plan_file=str(plan_file), with_library=None, username=None, password_env='CALIBRE_PASSWORD', state_dir=str(self.root / 'locks'))
        bad_opf = mod.make_opf(dict(plan['metadata'], title='Wrong title'), plan['identifiers']).decode()
        with patch.object(mod.Calibre, 'rows', side_effect=[[], [row], [row]]), patch.object(mod.Calibre, 'run', side_effect=['', '', bad_opf]), self.assertRaisesRegex(ValueError, 'title readback mismatch'):
            mod.apply_plan(args)
        events = [json.loads(line) for line in (plan_file.parent / 'apply-receipt.jsonl').read_text().splitlines()]
        self.assertEqual([e['event'] for e in events], ['intent', 'added', 'failed_or_unverified'])

    def test_wrong_destination_is_rejected(self):
        plan_file = self.prepared()
        args = argparse.Namespace(plan_file=str(plan_file), with_library='https://other-library.example/#other', username=None, password_env='CALIBRE_PASSWORD', state_dir=str(self.root / 'locks'))
        with patch.object(mod.Calibre, 'run', side_effect=AssertionError('write')), self.assertRaisesRegex(ValueError, 'different library'):
            mod.apply_plan(args)

    def test_cleanup_requires_verified_receipt(self):
        plan = self.prepared()
        args = argparse.Namespace(plan_file=str(plan), with_library=None, username=None, password_env='CALIBRE_PASSWORD', state_dir=str(self.root / 'locks'), apply=True)
        with self.assertRaisesRegex(ValueError, 'verified apply receipt required'):
            mod.cleanup_plan(args)
        self.assertTrue((plan.parent / 'source.epub').exists())

    def test_cleanup_stops_on_library_byte_mismatch(self):
        plan_file = self.prepared()
        _, plan, digest = mod.load_plan(plan_file)
        events = [{'event': 'intent', 'digest': digest}, {'event': 'verified', 'id': 7}]
        (plan_file.parent / 'apply-receipt.jsonl').write_text('\n'.join(json.dumps(e) for e in events) + '\n')
        args = argparse.Namespace(plan_file=str(plan_file), with_library=None, username=None, password_env='CALIBRE_PASSWORD', state_dir=str(self.root / 'locks'), apply=True)
        def export(db, *argv):
            self.assertEqual(argv[0], 'export')
            (Path(argv[argv.index('--to-dir') + 1]) / 'book.epub').write_bytes(b'corrupt library bytes')
            return ''
        with patch.object(mod, 'verify', return_value={'id': 7, 'format': 'EPUB'}), patch.object(mod.Calibre, 'run', export), patch.object(mod.subprocess, 'run', side_effect=AssertionError('must not trash')), self.assertRaisesRegex(ValueError, 'byte mismatch'):
            mod.cleanup_plan(args)
        self.assertTrue((plan_file.parent / 'source.epub').exists())
        self.assertTrue(self.source.exists())

    def test_cleanup_stops_when_staged_file_changed(self):
        plan_file = self.prepared()
        _, plan, digest = mod.load_plan(plan_file)
        events = [{'event': 'intent', 'digest': digest}, {'event': 'verified', 'id': 7}]
        (plan_file.parent / 'apply-receipt.jsonl').write_text('\n'.join(json.dumps(e) for e in events) + '\n')
        (plan_file.parent / 'source.epub').write_bytes(b'different local file')
        args = argparse.Namespace(plan_file=str(plan_file), with_library=None, username=None, password_env='CALIBRE_PASSWORD', state_dir=str(self.root / 'locks'), apply=True)
        with patch.object(mod, 'verify', return_value={'id': 7, 'format': 'EPUB'}), patch.object(mod.Calibre, 'run', side_effect=AssertionError('no export')), self.assertRaisesRegex(ValueError, 'staged source changed'):
            mod.cleanup_plan(args)
        self.assertEqual((plan_file.parent / 'source.epub').read_bytes(), b'different local file')

    def test_password_stdin_not_argv_or_environment(self):
        completed = subprocess.CompletedProcess([], 0, '[]', '')
        with patch.dict(os.environ, {'TEST_PASSWORD': 'synthetic-secret', 'OTHER_SECRET': 'unrelated'}), patch.object(mod.subprocess, 'run', return_value=completed) as run:
            db = mod.Calibre('https://library.example/#test', username='test-user', password_env='TEST_PASSWORD')
            db.run('list')
        args, kwargs = run.call_args
        self.assertNotIn('synthetic-secret', ' '.join(args[0]))
        self.assertEqual(kwargs['input'], 'synthetic-secret')
        self.assertNotIn('OTHER_SECRET', kwargs['env'])
        self.assertNotIn('TEST_PASSWORD', kwargs['env'])
        self.assertIn('<stdin>', args[0])

    def test_lock_is_exclusive(self):
        with mod.library_lock(self.root / 'locks', 'library'):
            with self.assertRaises(FileExistsError), mod.library_lock(self.root / 'locks', 'library'):
                self.fail('second lock acquired')
        self.assertEqual(list((self.root / 'locks').iterdir()), [])


@unittest.skipUnless(os.environ.get('CALIBRE_NATIVE_TESTS') == '1', 'set CALIBRE_NATIVE_TESTS=1 for isolated native Calibre tests')
class Native(unittest.TestCase):
    def setUp(self):
        if not shutil.which('calibredb'):
            self.skipTest('calibredb missing')
        self.temp = tempfile.TemporaryDirectory(prefix='reference-native-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.library = self.root / '試験 library'
        self.env = {k: os.environ[k] for k in ('PATH', 'SYSTEMROOT', 'WINDIR') if k in os.environ}
        self.env.update(HOME=str(self.root), LANG='C.UTF-8', QT_QPA_PLATFORM='offscreen', CALIBRE_CONFIG_DIRECTORY=str(self.root / 'config'))
        self.calibre('add', '--empty', '--title', 'Unrelated fixture', '--authors', 'Unrelated')
        self.source = self.root / 'original.epub'
        write_epub(self.source)

    def execute(self, *args, ok=True):
        p = subprocess.run(list(map(str, args)), env=self.env, capture_output=True, text=True, timeout=160)
        if ok and p.returncode:
            self.fail(str(args) + '\n' + p.stdout + '\n' + p.stderr)
        if not ok:
            self.assertNotEqual(p.returncode, 0, p.stdout)
        return p

    def calibre(self, *args):
        return self.execute('calibredb', *args, '--with-library', self.library)

    def cli(self, *args, ok=True):
        return self.execute(sys.executable, SCRIPT, *args, ok=ok)

    def prepare(self, name='run', **changes):
        input_file = self.root / (name + '-input.json')
        input_file.write_text(json.dumps(manifest(self.source, **changes), ensure_ascii=False))
        p = self.cli('prepare', '--input-json', input_file, '--run-dir', self.root / name, '--with-library', self.library)
        return json.loads(p.stdout)

    def apply(self, prepared, ok=True):
        return self.cli('apply', '--apply', '--plan-file', prepared['plan_file'], '--state-dir', self.root / 'locks', ok=ok)

    def snapshot(self):
        return json.loads(self.calibre('list', '--for-machine', '--fields', 'all').stdout)

    def test_import_verify_export_duplicates_and_native_date(self):
        before = self.snapshot()
        prepared = self.prepare()
        self.assertEqual(self.snapshot(), before, 'prepare must be read-only')
        self.assertEqual(prepared['decision'], 'new')
        applied = json.loads(self.apply(prepared).stdout)
        self.assertEqual(applied['status'], 'imported_verified')
        verified = json.loads(self.cli('verify', '--plan-file', prepared['plan_file']).stdout)
        self.assertEqual(verified['id'], applied['id'])
        after = self.snapshot()
        self.assertEqual(len(after), len(before) + 1)
        self.assertEqual(after[0], before[0], 'existing book must remain unchanged')
        row = next(r for r in after if r['id'] == applied['id'])
        self.assertTrue(row['timestamp'])
        self.assertNotIn('取得日時', row['comments'])
        self.assertEqual(row['pubdate'][:10], '2024-02-29')
        export = self.root / 'export'
        self.calibre('export', applied['id'], '--to-dir', export, '--single-dir', '--dont-update-metadata', '--dont-save-cover', '--dont-write-opf', '--dont-save-extra-files', '--formats', 'EPUB')
        files = list(export.glob('*.epub'))
        self.assertEqual(len(files), 1)
        self.assertEqual(mod.file_hash(files[0]), mod.file_hash(Path(prepared['plan_file']).parent / 'source.epub'))
        with zipfile.ZipFile(files[0]) as z:
            ET.fromstring(z.read('content.xhtml'))
        duplicate = self.prepare('duplicate', title='Different title')
        self.assertEqual(duplicate['decision'], 'review_existing')
        self.apply(duplicate, ok=False)
        self.apply(prepared, ok=False)
        self.assertEqual(self.snapshot(), after)
        # Different URL and title but identical bytes must also be detected.
        same_bytes = self.prepare('same-bytes', source_url='https://example.net/other', title='Another title')
        self.assertEqual(same_bytes['decision'], 'review_existing')
        write_epub(self.source, 'Different body for legacy-title matching.')
        title_only = self.prepare('title-only', source_url='https://example.net/new')
        self.assertEqual(title_only['decision'], 'review_existing')

    def test_doi_duplicate_with_distinct_url_title_and_bytes(self):
        first = self.prepare(doi='10.1234/testdoc')
        self.apply(first)
        write_epub(self.source, 'Other bytes')
        other = self.prepare('other-doi', doi='10.1234/testdoc', source_url='https://example.net/doi-copy', title='Other title')
        self.assertEqual(other['decision'], 'review_existing')

    def test_cleanup_preserves_library_and_input(self):
        if not shutil.which('trash'):
            self.skipTest('trash is required for reversible cleanup')
        prepared = self.prepare()
        applied = json.loads(self.apply(prepared).stdout)
        before = self.snapshot()
        plan_file = Path(prepared['plan_file'])
        source = plan_file.parent / 'source.epub'
        dry = json.loads(self.cli('cleanup', '--plan-file', plan_file, '--state-dir', self.root / 'locks').stdout)
        self.assertEqual(dry['status'], 'cleanup_ready')
        self.assertTrue(source.exists())
        cleaned = json.loads(self.cli('cleanup', '--apply', '--plan-file', plan_file, '--state-dir', self.root / 'locks').stdout)
        self.assertEqual(cleaned['status'], 'staged_copy_cleaned')
        self.assertTrue(cleaned['library_bytes_verified'])
        self.assertFalse(source.exists())
        self.assertTrue(self.source.exists(), 'never delete a user-supplied input by path alone')
        self.assertTrue(plan_file.exists())
        self.assertEqual(self.snapshot(), before)
        verified = json.loads(self.cli('verify', '--plan-file', plan_file).stdout)
        self.assertEqual(verified['id'], applied['id'], 'read-only verification works after local bytes are cleaned')
        again = json.loads(self.cli('cleanup', '--apply', '--plan-file', plan_file, '--state-dir', self.root / 'locks').stdout)
        self.assertEqual(again['trashed_files'], [])
        trashed = list((self.root / '.local/share/Trash/files').glob('*'))
        self.assertTrue(trashed, 'cleanup should be reversible, not permanent deletion')

    def test_cleanup_rejects_corrupt_library_file(self):
        prepared = self.prepare()
        applied = json.loads(self.apply(prepared).stdout)
        row = next(r for r in self.snapshot() if r['id'] == applied['id'])
        stored = Path(row['formats'][0])
        stored.write_bytes(b'synthetic corruption')
        result = self.cli('cleanup', '--apply', '--plan-file', prepared['plan_file'], '--state-dir', self.root / 'locks', ok=False)
        self.assertIn('byte mismatch', result.stderr)
        self.assertTrue((Path(prepared['plan_file']).parent / 'source.epub').exists())

    def test_two_books_in_same_archive_are_distinct(self):
        import ebook_archive as arc
        one = self.root / 'first.epub'; two = self.root / 'second.epub'
        write_epub(one, 'Archive first ebook'); write_epub(two, 'Archive second ebook')
        archive = self.root / 'bundle.zip'
        with zipfile.ZipFile(archive, 'w') as z:
            z.write(one, 'books/first.epub'); z.write(two, 'books/second.epub'); z.writestr('web.html', '<html>excluded</html>')
        index = arc.inventory(archive)
        ids = []
        for member in index['members']:
            extracted = arc.extract(archive, index['archive_sha256'], member['id'], self.root / ('extracted-' + str(member['id'])))
            self.source = Path(extracted['file'])
            prepared = self.prepare('import-' + str(member['id']), title=member['name'], source_url='https://example.org/bundle.zip', archive_member=extracted['archive_member'], archive_sha256=extracted['archive_sha256'])
            self.assertEqual(prepared['decision'], 'new', prepared)
            ids.append(json.loads(self.apply(prepared).stdout)['id'])
        self.assertEqual(len(set(ids)), 2)
        duplicate = self.prepare('again', title='Different title', source_url='https://example.org/bundle.zip', archive_member=extracted['archive_member'], archive_sha256=extracted['archive_sha256'])
        self.assertEqual(duplicate['decision'], 'review_existing')

    def test_legacy_url_identifier(self):
        self.calibre('add', '--empty', '--title', 'Legacy record', '--authors', 'Legacy author', '--identifier', 'url:https://example.org/docs?v=2')
        prepared = self.prepare()
        self.assertEqual(prepared['decision'], 'review_existing')
        self.assertEqual(prepared['candidates'][0]['title'], 'Legacy record')

    def test_original_pdf_and_epub_bytes_are_preserved(self):
        # Minimal valid single-page synthetic PDF, no external fixtures/services.
        objects = [b'<< /Type /Catalog /Pages 2 0 R >>',
                   b'<< /Type /Pages /Kids [3 0 R] /Count 1 >>',
                   b'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 300 300] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>',
                   b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>']
        stream = b'BT /F1 12 Tf 20 270 Td (Synthetic test document) Tj ET'
        objects.append(b'<< /Length ' + str(len(stream)).encode() + b' >>\nstream\n' + stream + b'\nendstream')
        data = bytearray(b'%PDF-1.4\n'); offsets = []
        for num, value in enumerate(objects, 1):
            offsets.append(len(data)); data.extend(str(num).encode() + b' 0 obj\n' + value + b'\nendobj\n')
        xref = len(data); data.extend(b'xref\n0 6\n0000000000 65535 f \n')
        for offset in offsets:
            data.extend(('%010d 00000 n \n' % offset).encode())
        data.extend(b'trailer\n<< /Size 6 /Root 1 0 R >>\nstartxref\n' + str(xref).encode() + b'\n%%EOF\n')
        pdf = self.root / 'original.pdf'; pdf.write_bytes(data)
        epub = self.root / 'original.epub'
        write_epub(epub, 'Synthetic original EPUB')
        for original in (pdf, epub):
            with self.subTest(format=original.suffix):
                self.source = original
                prepared = self.prepare('original-' + original.suffix[1:], title='Original ' + original.suffix, source_url='https://example.org/original' + original.suffix)
                applied = json.loads(self.apply(prepared).stdout)
                export = self.root / ('export-' + original.suffix[1:])
                self.calibre('export', applied['id'], '--to-dir', export, '--single-dir', '--dont-update-metadata', '--dont-save-cover', '--dont-write-opf', '--dont-save-extra-files', '--formats', original.suffix[1:])
                files = list(export.glob('*' + original.suffix))
                self.assertEqual(len(files), 1)
                self.assertEqual(mod.file_hash(files[0]), mod.file_hash(original))

    def test_quoted_title_and_stale_plan(self):
        prepared = self.prepare(title='A "quoted" guide')
        self.calibre('add', '--empty', '--title', 'A "quoted" guide', '--authors', 'Someone else')
        count = len(self.snapshot())
        result = self.apply(prepared, ok=False)
        self.assertIn('appeared', result.stderr)
        self.assertEqual(len(self.snapshot()), count)
        self.assertFalse((Path(prepared['plan_file']).parent / 'apply-receipt.jsonl').exists())


if __name__ == '__main__':
    unittest.main()
