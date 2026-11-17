"""Offline regressions for Get Hired PRO document delivery; synthetic career data only."""
import copy
import errno
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import shutil
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as E
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import render_documents as renderer
from letter_layout import roles

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'


def packet(contacts=1):
    return {
        'resume_blocks': [
            {'kind': 'name', 'text': 'José Chen'},
            {'kind': 'contact', 'text': 'jose@example.org | https://example.org/profile'},
            {'kind': 'section', 'text': 'Experience'},
            {'kind': 'role_header', 'role_id': 'north', 'text': 'North Studio | Developer | 2024–present'},
            {'kind': 'context', 'role_id': 'north', 'text': 'Customer delivery tools.'},
            {'kind': 'achievement', 'role_id': 'north', 'text': 'Built a reporting tool used by the customer team.'},
            {'kind': 'achievement', 'role_id': 'north', 'text': 'Documented integration handoffs for support.'},
            {'kind': 'section', 'text': 'Publications'},
            {'kind': 'publication', 'text': '[Workflow paper](https://example.org/a(b(c)d)e?x=1&y=2)'},
        ],
        'cover_letter_lines': ['José Chen'] + ['jose@example.org'] * contacts + [
            'October 20, 2026', 'Northwind team', 'Dear Northwind team,',
            'Your new service interests me. I can build useful customer delivery tools.',
            'At North Studio, I built a reporting tool used by the customer team.',
            'I would welcome a conversation.', 'Sincerely,', 'José Chen'],
        'contact_lines_count': contacts,
        'application_answers': {'availability': 'Two weeks'},
    }


def inspect(path):
    with zipfile.ZipFile(path) as z:
        for name in z.namelist():
            E.fromstring(z.read(name))
        doc = E.fromstring(z.read('word/document.xml'))
        relationships = E.fromstring(z.read('word/_rels/document.xml.rels'))
    paragraphs = doc.findall('./' + W + 'body/' + W + 'p')
    return doc, paragraphs, {r.attrib['Target'] for r in relationships}


class Documents(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='get-hired-pro-documents-')
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)

    def test_contact_counts_preserve_content_and_structural_roles(self):
        for count in (0, 1, 2, 4):
            with self.subTest(count=count):
                source = packet(count)
                out = self.directory / str(count)
                renderer.render(source, out)
                _, paragraphs, _ = inspect(out / 'Letter.docx')
                self.assertEqual([''.join(p.itertext()) for p in paragraphs], source['cover_letter_lines'])
                self.assertEqual(roles(source['cover_letter_lines'], count)[count + 1:count + 4],
                                 ['date', 'recipient', 'salutation'])
                self.assertEqual(json.loads((out / 'packet.json').read_text(encoding='utf-8')), source)

    def test_missing_contact_count_fails_before_writing(self):
        source = packet()
        del source['contact_lines_count']
        out = self.directory / 'missing'
        with self.assertRaisesRegex(ValueError, 'contact_lines_count'):
            renderer.render(source, out)
        self.assertFalse(out.exists())

    def test_visible_spacing_in_both_letter_profiles_and_resume_sections(self):
        for profile, minimum in [('standard', 200), ('compact', 120)]:
            with self.subTest(profile=profile):
                source = packet()
                source['letter_spacing'] = profile
                out = self.directory / profile
                renderer.render(source, out)
                _, paragraphs, _ = inspect(out / 'Letter.docx')
                for p, role in zip(paragraphs, roles(source['cover_letter_lines'], 1)):
                    if role == 'body':
                        spacing = p.find('./' + W + 'pPr/' + W + 'spacing')
                        self.assertGreaterEqual(int(spacing.attrib[W + 'after']), minimum)
                        self.assertGreaterEqual(int(spacing.attrib[W + 'line']), 264)
                _, paragraphs, _ = inspect(out / 'Resume.docx')
                for b, p in zip(source['resume_blocks'], paragraphs):
                    if b['kind'] == 'section':
                        self.assertGreaterEqual(int(p.find('./' + W + 'pPr/' + W + 'spacing').attrib[W + 'before']), 240)

    def test_role_heading_is_kept_with_opening_but_bullets_can_flow(self):
        out = self.directory / 'flow'
        source = packet()
        renderer.render(source, out)
        _, paragraphs, _ = inspect(out / 'Resume.docx')
        for b, p in zip(source['resume_blocks'], paragraphs):
            keep_next = p.find('./' + W + 'pPr/' + W + 'keepNext') is not None
            if b['kind'] in ['role_header', 'context']:
                self.assertTrue(keep_next)
            if b['kind'] == 'achievement':
                self.assertFalse(keep_next)
                self.assertIsNotNone(p.find('./' + W + 'pPr/' + W + 'keepLines'))

    def test_nested_markdown_url_preserves_label_and_target(self):
        out = self.directory / 'links'
        renderer.render(packet(), out)
        _, paragraphs, links = inspect(out / 'Resume.docx')
        self.assertEqual(''.join(paragraphs[-1].itertext()), 'Workflow paper')
        self.assertIn('https://example.org/a(b(c)d)e?x=1&y=2', links)

    def test_quoted_urls_keep_visible_punctuation_and_correct_targets(self):
        cases = [
            ('"https://example.org/work"', 'https://example.org/work'),
            ("'https://example.org/work'", 'https://example.org/work'),
            ('“https://example.org/work”', 'https://example.org/work'),
            ('‘https://example.org/work’', 'https://example.org/work'),
            ("https://example.org/O'Neil", "https://example.org/O'Neil"),
            ("'https://example.org/O'Neil'", "https://example.org/O'Neil"),
            ('"https://example.org/find?q=why?"', 'https://example.org/find?q=why?'),
            ('https://example.org/work.', 'https://example.org/work'),
        ]
        for index, (visible, target) in enumerate(cases):
            with self.subTest(visible=visible):
                source = packet()
                text = 'Portfolio: ' + visible
                source['resume_blocks'][-1]['text'] = text
                source['cover_letter_lines'][5] = text
                out = self.directory / ('quoted-' + str(index))
                renderer.render(source, out)
                for filename in ['Resume.docx', 'Letter.docx']:
                    _, paragraphs, links = inspect(out / filename)
                    self.assertIn(target, links)
                    self.assertIn(text, [''.join(p.itertext()) for p in paragraphs])

    def test_invalid_xml_in_either_document_fails_before_any_output(self):
        for location in ['resume', 'letter']:
            with self.subTest(location=location):
                source = packet()
                if location == 'resume':
                    source['resume_blocks'][0]['text'] += '\x00'
                else:
                    source['cover_letter_lines'][4] += '\x00'
                out = self.directory / location
                with self.assertRaisesRegex(ValueError, 'XML-invalid'):
                    renderer.render(source, out)
                self.assertFalse(out.exists())

    def test_failed_letter_can_resume_without_rebuilding_good_resume(self):
        out = self.directory / 'interrupted'
        source = packet()
        def interrupted(lines, path, **kwargs):
            Path(path).write_bytes(b'incomplete temporary document')
            raise OSError('Synthetic file failure')
        with patch.object(renderer, 'make_letter', side_effect=interrupted):
            with self.assertRaises(OSError):
                renderer.render(source, out)
        self.assertFalse((out / 'Letter.docx').exists())
        self.assertFalse(any(p.name.startswith('.get-hired-pro-build-') for p in out.iterdir()))
        resume_bytes = (out / 'Resume.docx').read_bytes()
        resume_mtime = (out / 'Resume.docx').stat().st_mtime_ns
        self.assertEqual(json.loads((out / 'packet.json').read_text(encoding='utf-8')), source)
        with patch.object(renderer, 'build', side_effect=AssertionError('Successful resume must be reused')):
            renderer.render(source, out, resume=True)
        inspect(out / 'Letter.docx')
        self.assertEqual((out / 'Resume.docx').read_bytes(), resume_bytes)
        self.assertEqual((out / 'Resume.docx').stat().st_mtime_ns, resume_mtime)

    def test_existing_documents_and_changed_packets_remain_protected(self):
        source = packet()
        out = self.directory / 'protected'
        renderer.render(source, out)
        original = {name: (out / name).read_bytes() for name in ['Resume.docx', 'Letter.docx', 'packet.json']}
        with self.assertRaises(ValueError):
            renderer.render(source, out)
        changed = copy.deepcopy(source)
        changed['cover_letter_lines'][5] += ' Another sentence.'
        with self.assertRaises(ValueError):
            renderer.render(changed, out, resume=True)
        renderer.render(source, out, resume=True)
        self.assertEqual(original, {name: (out / name).read_bytes() for name in original})

    def interrupt_publication(self, source, out, call_number):
        original_link = os.link
        count = 0
        def interrupted(*args, **kwargs):
            nonlocal count
            count += 1
            if count == call_number:
                raise OSError(errno.EIO, 'Interrupted before publishing receipt')
            return original_link(*args, **kwargs)
        with patch.object(renderer.os, 'link', side_effect=interrupted):
            with self.assertRaises(OSError):
                renderer.render(source, out)

    def test_resume_recovers_either_published_document_without_rebuilding_it(self):
        for name, call_number in [('Resume', 2), ('Letter', 4)]:
            with self.subTest(name=name):
                out = self.directory / ('publication-' + name)
                source = packet()
                self.interrupt_publication(source, out, call_number)
                self.assertTrue((out / ('.' + name + '.pending.json')).is_file())
                self.assertFalse((out / (name + '.layout.json')).exists())
                saved = {p.name: (p.read_bytes(), p.stat().st_mtime_ns)
                         for p in out.glob('*.docx')}
                sentinel = out / 'owner-note.txt'
                sentinel.write_text('Keep this unrelated note.')
                with patch.object(renderer, 'build', side_effect=AssertionError('Reuse published resume')):
                    if name == 'Letter':
                        with patch.object(renderer, 'make_letter', side_effect=AssertionError('Reuse published letter')):
                            renderer.render(source, out, resume=True)
                    else:
                        renderer.render(source, out, resume=True)
                for filename, (content, modified) in saved.items():
                    self.assertEqual((out / filename).read_bytes(), content)
                    self.assertEqual((out / filename).stat().st_mtime_ns, modified)
                for filename in ['Resume.docx', 'Letter.docx']:
                    inspect(out / filename)
                self.assertFalse(list(out.glob('.*.pending.json')))
                self.assertFalse(any(p.name.startswith('.get-hired-pro-build-') for p in out.iterdir()))
                self.assertEqual(sentinel.read_text(), 'Keep this unrelated note.')

    def test_resume_refuses_mismatched_pending_evidence_or_changed_work(self):
        for fault in ['document', 'metadata', 'hash', 'packet']:
            with self.subTest(fault=fault):
                out = self.directory / ('recovery-' + fault)
                source = packet()
                self.interrupt_publication(source, out, 2)
                pending = out / '.Resume.pending.json'
                if fault == 'document':
                    with (out / 'Resume.docx').open('ab') as f:
                        f.write(b'User changed this document')
                elif fault in ['metadata', 'hash']:
                    receipt = json.loads(pending.read_text())
                    if fault == 'metadata':
                        receipt['source_blocks'] = []
                    else:
                        receipt['docx_sha256'] = '0' * 64
                    pending.write_text(json.dumps(receipt))
                else:
                    source['cover_letter_lines'][5] = 'Changed packet wording.'
                originals = {p.name: p.read_bytes() for p in out.iterdir() if p.is_file()}
                with self.assertRaises(ValueError):
                    renderer.render(source, out, resume=True)
                self.assertEqual(originals, {p.name: p.read_bytes() for p in out.iterdir() if p.is_file()})

    def test_unsupported_hard_links_preserve_packet_and_recovery_evidence(self):
        out = self.directory / 'unsupported-links'
        source = packet()
        with patch.object(renderer.os, 'link', side_effect=OSError(errno.EOPNOTSUPP, 'Unsupported storage')):
            with self.assertRaisesRegex(OSError, 'filesystem hard-link support'):
                renderer.render(source, out)
        self.assertEqual(json.loads((out / 'packet.json').read_text()), source)
        self.assertTrue((out / '.Resume.pending.json').is_file())
        self.assertFalse((out / 'Resume.docx').exists())
        renderer.render(source, out, resume=True)
        inspect(out / 'Resume.docx')
        inspect(out / 'Letter.docx')
        self.assertFalse(list(out.glob('.*.pending.json')))

    def test_resume_rejects_edited_letter_without_changing_either_document(self):
        source = packet()
        out = self.directory / 'edited-letter'
        renderer.render(source, out)
        letter = out / 'Letter.docx'
        with zipfile.ZipFile(letter) as archive:
            parts = {name: archive.read(name) for name in archive.namelist()}
        parts['word/document.xml'] = parts['word/document.xml'].replace(
            b'Northwind team', b'Unrelated employer')
        with zipfile.ZipFile(letter, 'w', zipfile.ZIP_DEFLATED) as archive:
            for name, content in parts.items():
                archive.writestr(name, content)
        originals = {name: (out / name).read_bytes() for name in ['Resume.docx', 'Letter.docx']}
        with self.assertRaisesRegex(ValueError, 'Existing letter'):
            renderer.render(source, out, resume=True)
        for name, content in originals.items():
            self.assertEqual((out / name).read_bytes(), content)

    def test_resume_preserves_verified_letter_and_rejects_missing_receipt(self):
        source = packet()
        out = self.directory / 'verified-letter'
        renderer.render(source, out)
        letter = out / 'Letter.docx'
        original = letter.read_bytes()
        original_mtime = letter.stat().st_mtime_ns
        with patch.object(renderer, 'make_letter', side_effect=AssertionError('Verified letter must be reused')):
            renderer.render(source, out, resume=True)
        self.assertEqual(letter.read_bytes(), original)
        self.assertEqual(letter.stat().st_mtime_ns, original_mtime)
        (out / 'Letter.layout.json').unlink()
        with self.assertRaisesRegex(ValueError, 'Existing letter has no receipt'):
            renderer.render(source, out, resume=True)
        self.assertEqual(letter.read_bytes(), original)

    def test_utf8_packet_works_with_non_utf8_locale(self):
        path = self.directory / 'input.json'
        path.write_text(json.dumps(packet(), ensure_ascii=False), encoding='utf-8')
        env = os.environ.copy()
        env.update(LC_ALL='C', LANG='C', PYTHONUTF8='0', PYTHONCOERCECLOCALE='0', PYTHONDONTWRITEBYTECODE='1')
        out = self.directory / 'unicode'
        result = subprocess.run([sys.executable, str(ROOT / 'scripts/render_documents.py'), str(path), str(out)],
                                env=env, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads((out / 'packet.json').read_text(encoding='utf-8'))['resume_blocks'][0]['text'], 'José Chen')
        _, paragraphs, _ = inspect(out / 'Resume.docx')
        self.assertEqual(''.join(paragraphs[0].itertext()), 'José Chen')


@unittest.skipUnless(importlib.util.find_spec('weasyprint'), 'PDF tests use requirements-pdf.txt')
class PDFDocuments(unittest.TestCase):
    setUp = Documents.setUp
    def test_pdf_and_word_preserve_text_unicode_and_links(self):
        out = self.directory / 'both'
        source = packet()
        source['cover_letter_lines'][5] += ' Portfolio: [Work](https://example.org/work).'
        renderer.render(source, out, format='both')
        for name in ('Resume', 'Letter'):
            self.assertTrue((out / (name + '.pdf')).read_bytes().startswith(b'%PDF-'))
            _, paragraphs, expected_urls = inspect(out / (name + '.docx'))
            if shutil.which('pdftotext'):
                extracted = subprocess.check_output(['pdftotext', str(out / (name + '.pdf')), '-'], text=True)
                normalized = ' '.join(extracted.split())
                for paragraph in paragraphs:
                    self.assertIn(' '.join(''.join(paragraph.itertext()).split()), normalized)
            if shutil.which('pdfinfo'):
                urls = subprocess.check_output(['pdfinfo', '-url', str(out / (name + '.pdf'))], text=True)
                for url in expected_urls:
                    self.assertIn(url, urls)

    def test_pdf_can_be_added_without_rebuilding_word_files(self):
        source = packet()
        out = self.directory / 'add-pdf'
        renderer.render(source, out)
        originals = {p.name: (p.read_bytes(), p.stat().st_mtime_ns) for p in out.glob('*.docx')}
        with patch.object(renderer, 'build', side_effect=AssertionError('Reuse Word resume')), \
                patch.object(renderer, 'make_letter', side_effect=AssertionError('Reuse Word letter')):
            renderer.render(source, out, resume=True, format='pdf')
        self.assertTrue((out / 'Resume.pdf').is_file())
        self.assertTrue((out / 'Letter.pdf').is_file())
        for name, saved in originals.items():
            self.assertEqual((out / name).read_bytes(), saved[0])
            self.assertEqual((out / name).stat().st_mtime_ns, saved[1])

    def test_missing_pdf_dependency_preserves_word_and_can_resume(self):
        source = packet()
        out = self.directory / 'missing-pdf-tool'
        with patch.dict(sys.modules, {'weasyprint': None}):
            with self.assertRaisesRegex(RuntimeError, 'WeasyPrint'):
                renderer.render(source, out, format='pdf')
        originals = {p.name: p.read_bytes() for p in out.glob('*.docx')}
        self.assertEqual(len(originals), 2)
        renderer.render(source, out, resume=True, format='pdf')
        for name, content in originals.items():
            self.assertEqual((out / name).read_bytes(), content)

    def test_interrupted_pdf_receipt_recovers_without_rebuilding_finished_pdf(self):
        source = packet()
        out = self.directory / 'pdf-interrupted'
        original_link = renderer.os.link
        def interrupted(src, dst):
            if Path(dst).name == 'Resume.pdf.json':
                raise OSError(errno.EIO, 'Interrupted PDF receipt')
            return original_link(src, dst)
        with patch.object(renderer.os, 'link', side_effect=interrupted):
            with self.assertRaises(OSError):
                renderer.render(source, out, format='both')
        saved = (out / 'Resume.pdf').read_bytes()
        modified = (out / 'Resume.pdf').stat().st_mtime_ns
        import pdf_layout
        original_html = pdf_layout.printable_html
        def only_missing(path):
            self.assertEqual(Path(path).name, 'Letter.docx')
            return original_html(path)
        with patch.object(pdf_layout, 'printable_html', side_effect=only_missing):
            renderer.render(source, out, resume=True, format='both')
        self.assertEqual((out / 'Resume.pdf').read_bytes(), saved)
        self.assertEqual((out / 'Resume.pdf').stat().st_mtime_ns, modified)
        self.assertTrue((out / 'Letter.pdf').exists())
        self.assertFalse(list(out.glob('.*.pdf.pending.json')))

    def test_edited_pdf_is_preserved_on_resume(self):
        source = packet()
        out = self.directory / 'edited-pdf'
        renderer.render(source, out, format='both')
        with (out / 'Letter.pdf').open('ab') as f:
            f.write(b'User revision')
        originals = {p.name: p.read_bytes() for p in out.iterdir() if p.is_file()}
        with self.assertRaisesRegex(ValueError, 'Existing Letter PDF'):
            renderer.render(source, out, resume=True, format='both')
        self.assertEqual(originals, {p.name: p.read_bytes() for p in out.iterdir() if p.is_file()})

    def test_pdf_export_uses_escaped_printable_html(self):
        import pdf_layout
        source = packet()
        source['resume_blocks'][1]['text'] = 'Research & development <team> | https://example.org/profile'
        out = self.directory / 'html'
        renderer.render(source, out)
        html = pdf_layout.printable_html(out / 'Resume.docx')
        self.assertIn('Research &amp; development &lt;team&gt;', html)
        self.assertIn('href="https://example.org/profile"', html)


if __name__ == '__main__':
    unittest.main()
