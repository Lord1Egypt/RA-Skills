"""Single-upload document regressions using synthetic career fixtures."""
import hashlib
import importlib.util
from pathlib import Path
import shutil
import subprocess
import unittest
from unittest.mock import patch

import test_documents as fixtures
import combine_documents
inspect, packet, renderer, W = fixtures.inspect, fixtures.packet, fixtures.renderer, fixtures.W


def fingerprint(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class CombinedDocuments(unittest.TestCase):
    setUp = fixtures.Documents.setUp

    def test_word_preserves_both_documents_links_and_section_break(self):
        source = packet()
        source['cover_letter_lines'][5] += ' See [Letter portfolio](https://example.org/letter).'
        out = self.directory / 'combined'
        renderer.render(source, out, combine=True)
        resume, first, resume_links = inspect(out / 'Resume.docx')
        letter, second, letter_links = inspect(out / 'Letter.docx')
        merged, actual, merged_links = inspect(out / 'Application.docx')
        self.assertEqual([''.join(p.itertext()) for p in actual],
                         [''.join(p.itertext()) for p in first + second])
        self.assertEqual(merged_links, resume_links | letter_links)
        boundary = actual[len(first) - 1].find(W + 'pPr/' + W + 'sectPr')
        self.assertIsNotNone(boundary)
        self.assertEqual(boundary.find(W + 'type').get(W + 'val'), 'nextPage')
        self.assertEqual([child.tag for child in boundary], [W + 'type', W + 'pgSz', W + 'pgMar'])
        self.assertEqual(boundary.find(W + 'pgMar').attrib,
                         resume.find(W + 'body/' + W + 'sectPr/' + W + 'pgMar').attrib)
        self.assertEqual(merged.find(W + 'body/' + W + 'sectPr/' + W + 'pgMar').attrib,
                         letter.find(W + 'body/' + W + 'sectPr/' + W + 'pgMar').attrib)
        # Compare each hyperlink's label and target, not only the set of URLs.
        def links(document, path):
            import xml.etree.ElementTree as ET
            import zipfile
            with zipfile.ZipFile(path) as archive:
                relationships = ET.fromstring(archive.read('word/_rels/document.xml.rels'))
            targets = {r.attrib['Id']: r.attrib['Target'] for r in relationships}
            return [(''.join(h.itertext()), targets[h.attrib[combine_documents.R + 'id']])
                    for h in document.iter(W + 'hyperlink')]
        self.assertEqual(links(merged, out / 'Application.docx'),
                         links(resume, out / 'Resume.docx') + links(letter, out / 'Letter.docx'))

    def test_regular_flow_stays_separate_and_combination_can_be_added(self):
        source = packet()
        out = self.directory / 'separate'
        renderer.render(source, out)
        self.assertFalse((out / 'Application.docx').exists())
        originals = {p.name: (fingerprint(p), p.stat().st_mtime_ns) for p in out.glob('*.docx')}
        with patch.object(renderer, 'build', side_effect=AssertionError('Reuse résumé')), \
                patch.object(renderer, 'make_letter', side_effect=AssertionError('Reuse letter')):
            renderer.render(source, out, resume=True, combine=True)
        self.assertTrue((out / 'Application.docx').is_file())
        for name, expected in originals.items():
            self.assertEqual((fingerprint(out / name), (out / name).stat().st_mtime_ns), expected)
        with patch.object(combine_documents, 'combine_word', side_effect=AssertionError('Reuse combined file')):
            renderer.render(source, out, resume=True, combine=True)

    def test_edited_combined_document_is_preserved(self):
        source = packet()
        out = self.directory / 'edited'
        renderer.render(source, out, combine=True)
        target = out / 'Application.docx'
        target.write_bytes(b'Synthetic user-edited application')
        before = {p.name: p.read_bytes() for p in out.iterdir() if p.is_file()}
        with self.assertRaisesRegex(ValueError, 'combined'):
            renderer.render(source, out, resume=True, combine=True)
        self.assertEqual({p.name: p.read_bytes() for p in out.iterdir() if p.is_file()}, before)

    def test_interrupted_combined_receipt_recovers_without_rebuilding(self):
        source = packet()
        out = self.directory / 'interrupted'
        publish = renderer.publish
        def interrupted(source_path, destination):
            if Path(destination).name == 'Application.docx.json':
                raise OSError('Synthetic receipt interruption')
            return publish(source_path, destination)
        with patch.object(renderer, 'publish', side_effect=interrupted):
            with self.assertRaisesRegex(OSError, 'Synthetic receipt'):
                renderer.render(source, out, combine=True)
        target = out / 'Application.docx'
        before = (fingerprint(target), target.stat().st_mtime_ns)
        self.assertTrue((out / '.Application.docx.pending.json').is_file())
        with patch.object(combine_documents, 'combine_word', side_effect=AssertionError('Reuse published file')):
            renderer.render(source, out, resume=True, combine=True)
        self.assertEqual((fingerprint(target), target.stat().st_mtime_ns), before)
        self.assertTrue((out / 'Application.docx.json').is_file())
        self.assertFalse((out / '.Application.docx.pending.json').exists())

    @unittest.skipUnless(importlib.util.find_spec('weasyprint') and shutil.which('pdftotext')
                         and shutil.which('pdfinfo'), 'PDF inspection tools required')
    def test_combined_pdf_has_every_page_in_order_and_working_links(self):
        source = packet()
        source['cover_letter_lines'][5] += ' See [Letter portfolio](https://example.org/letter).'
        # A long résumé exercises a cover letter beginning after multiple pages.
        source['resume_blocks'][6:6] = [
            {'kind': 'achievement', 'role_id': 'north',
             'text': f'Contribution {i}: documented customer workflows and practical delivery improvements.'}
            for i in range(60)
        ]
        out = self.directory / 'pdf'
        renderer.render(source, out, format='both', combine=True)
        texts = {}
        counts = {}
        for name in ['Resume', 'Letter', 'Application']:
            path = out / (name + '.pdf')
            texts[name] = subprocess.check_output(['pdftotext', str(path), '-'], text=True)
            info = subprocess.check_output(['pdfinfo', str(path)], text=True)
            counts[name] = int(next(line.split(':', 1)[1] for line in info.splitlines()
                                    if line.startswith('Pages:')))
        self.assertGreater(counts['Resume'], 1)
        self.assertEqual(counts['Application'], counts['Resume'] + counts['Letter'])
        self.assertEqual(' '.join(texts['Application'].split()),
                         ' '.join((texts['Resume'] + texts['Letter']).split()))
        pages = texts['Application'].split('\f')
        self.assertIn('Northwind team', pages[counts['Resume']])
        links = subprocess.check_output(['pdfinfo', '-url', str(out / 'Application.pdf')], text=True)
        self.assertIn('https://example.org/letter', links)
        self.assertIn('https://example.org/profile', links)
        before = {p.name: (fingerprint(p), p.stat().st_mtime_ns) for p in out.glob('*.pdf')}
        with patch.object(combine_documents, 'combine_pdf', side_effect=AssertionError('Reuse combined PDF')):
            renderer.render(source, out, resume=True, format='both', combine=True)
        self.assertEqual({p.name: (fingerprint(p), p.stat().st_mtime_ns) for p in out.glob('*.pdf')}, before)


if __name__ == '__main__':
    unittest.main()
