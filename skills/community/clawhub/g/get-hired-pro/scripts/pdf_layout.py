"""Export the bundled DOCX layouts to PDF using WeasyPrint, or save printable HTML."""
from html import escape
import hashlib
import json
from pathlib import Path
import tempfile
import xml.etree.ElementTree as ET
import zipfile

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
R = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}'


def printable_html(document):
    """Translate the paragraph formatting emitted by the bundled Word builders."""
    with zipfile.ZipFile(document) as archive:
        root = ET.fromstring(archive.read('word/document.xml'))
        relationships = ET.fromstring(archive.read('word/_rels/document.xml.rels'))
    links = {r.attrib['Id']: r.attrib['Target'] for r in relationships}
    body = root.find(W + 'body')
    section = body.find(W + 'sectPr')
    size, margins = section.find(W + 'pgSz'), section.find(W + 'pgMar')
    page = 'size: {}pt {}pt; margin: {}pt {}pt {}pt {}pt;'.format(
        float(size.get(W + 'w')) / 20, float(size.get(W + 'h')) / 20,
        *(float(margins.get(W + key)) / 20 for key in ('top', 'right', 'bottom', 'left')))
    paragraphs = []
    for paragraph in body.findall(W + 'p'):
        styles, runs = [], []
        properties = paragraph.find(W + 'pPr')
        if properties is not None:
            spacing = properties.find(W + 'spacing')
            if spacing is not None:
                styles += ['margin-top: {}pt'.format(float(spacing.get(W + 'before', 0)) / 20),
                           'margin-bottom: {}pt'.format(float(spacing.get(W + 'after', 0)) / 20),
                           'line-height: {}'.format(float(spacing.get(W + 'line', 240)) / 240)]
            if properties.find(W + 'keepLines') is not None:
                styles.append('break-inside: avoid')
            if properties.find(W + 'keepNext') is not None:
                styles.append('break-after: avoid')
            indent = properties.find(W + 'ind')
            if indent is not None:
                styles += ['padding-left: {}pt'.format(float(indent.get(W + 'left', 0)) / 20),
                           'text-indent: {}pt'.format(-float(indent.get(W + 'hanging', 0)) / 20)]
        for container in paragraph:
            if container.tag == W + 'pPr':
                continue
            contents = []
            for run in ([container] if container.tag == W + 'r' else container.findall(W + 'r')):
                text = ''.join(t.text or '' for t in run.findall(W + 't'))
                formatting = run.find(W + 'rPr')
                style = []
                if formatting is not None:
                    font_size = formatting.find(W + 'sz')
                    if font_size is not None:
                        style.append('font-size: {}pt'.format(float(font_size.get(W + 'val')) / 2))
                    if formatting.find(W + 'b') is not None:
                        style.append('font-weight: bold')
                contents.append('<span style="{}">{}</span>'.format(';'.join(style), escape(text)))
            content = ''.join(contents)
            if container.tag == W + 'hyperlink':
                content = '<a href="{}">{}</a>'.format(escape(links[container.get(R + 'id')], quote=True), content)
            runs.append(content)
        paragraphs.append('<p style="{}">{}</p>'.format(';'.join(styles), ''.join(runs)))
    return ('<!doctype html><html><head><meta charset="utf-8"><style>'
            '@page {' + page + '} '
            'body {font-family: Calibri, Carlito, "Liberation Sans", "DejaVu Sans", sans-serif; '
            'font-size:12pt;} p {margin:0; white-space:pre-wrap; overflow-wrap:anywhere;}'
            'a {color:inherit; text-decoration:none;}'
            '</style></head><body>' + ''.join(paragraphs) + '</body></html>')


def export_pdfs(directory, *, resume, publish, verify):
    out = Path(directory)
    documents = []
    for name in ('Resume', 'Letter'):
        source = out / (name + '.docx')
        pdf = out / (name + '.pdf')
        receipt = out / (name + '.pdf.json')
        pending = out / ('.' + name + '.pdf.pending.json')
        expected = {'format': 'pdf', 'source_docx_sha256': hashlib.sha256(source.read_bytes()).hexdigest()}
        if pending.exists():
            verify(pending, expected, name + ' PDF', pdf if pdf.exists() else None, hash_field='pdf_sha256')
        if pdf.exists():
            saved = receipt if receipt.is_file() else pending
            if not resume or not saved.is_file():
                raise ValueError('Preserve the existing PDF and choose a new revision directory')
            verify(saved, expected, name + ' PDF', pdf, hash_field='pdf_sha256')
        elif receipt.exists():
            raise ValueError('An existing PDF receipt needs a new revision directory')
        documents.append((source, pdf, receipt, pending, expected))
    # Import only when an actual conversion is needed; completed PDFs can be reused.
    if any(not pdf.exists() for _, pdf, _, _, _ in documents):
        try:
            from weasyprint import HTML
        except (ImportError, OSError) as exc:
            raise RuntimeError('PDF export needs WeasyPrint. Install requirements-pdf.txt in the '
                               'document environment, then rerun with --resume. Completed Word '
                               'files are saved. Existing PDF tools can also export them.') from exc
    with tempfile.TemporaryDirectory(prefix='.get-hired-pro-pdf-', dir=out) as temporary:
        for source, pdf, receipt, pending, expected in documents:
            if not pdf.exists():
                staged = Path(temporary) / pdf.name
                HTML(string=printable_html(source)).write_pdf(staged)
                pending.write_text(json.dumps({**expected, 'pdf_sha256': hashlib.sha256(staged.read_bytes()).hexdigest()},
                                              indent=2) + '\n', encoding='utf-8')
                publish(staged, pdf)
            if not receipt.exists():
                publish(pending, receipt)
            if pending.exists():
                pending.unlink()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('docx')
    parser.add_argument('html', help='Printable HTML for an existing browser PDF tool')
    args = parser.parse_args()
    with Path(args.html).open('x', encoding='utf-8') as output:
        output.write(printable_html(args.docx))
