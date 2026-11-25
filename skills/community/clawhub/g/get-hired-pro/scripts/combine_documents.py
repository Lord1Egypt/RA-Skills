"""Combine the bundled résumé and cover letter without changing their prose."""
import copy
import hashlib
import json
from pathlib import Path
import tempfile
import xml.etree.ElementTree as ET
import zipfile

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
R = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}'


def combine_word(resume, letter, destination):
    """Join the bundled builders' DOCX files, retaining sections and hyperlink IDs."""
    with zipfile.ZipFile(resume) as archive:
        parts = {name: archive.read(name) for name in archive.namelist()}
    with zipfile.ZipFile(letter) as archive:
        second = ET.fromstring(archive.read('word/document.xml'))
        second_links = ET.fromstring(archive.read('word/_rels/document.xml.rels'))
    document = ET.fromstring(parts['word/document.xml'])
    body, next_body = document.find(W + 'body'), second.find(W + 'body')
    links = ET.fromstring(parts['word/_rels/document.xml.rels'])
    # The final résumé paragraph terminates its own section; the letter starts
    # on the next page with its original margins.
    section = body.find(W + 'sectPr')
    body.remove(section)
    section = copy.deepcopy(section)
    transition = ET.Element(W + 'type')
    transition.set(W + 'val', 'nextPage')
    section.insert(0, transition)
    properties = body[-1].find(W + 'pPr')
    if properties is None:
        properties = ET.SubElement(body[-1], W + 'pPr')
    properties.append(section)
    used = {link.attrib['Id'] for link in links}
    remap = {}
    for link in second_links:
        number = len(used) + 1
        while 'rId' + str(number) in used:
            number += 1
        ident = 'rId' + str(number)
        remap[link.attrib['Id']] = ident
        link.set('Id', ident)
        used.add(ident)
        links.append(link)
    for hyperlink in next_body.iter(W + 'hyperlink'):
        hyperlink.set(R + 'id', remap[hyperlink.attrib[R + 'id']])
    body.extend(list(next_body))
    parts['word/document.xml'] = ET.tostring(document, encoding='utf-8', xml_declaration=True)
    parts['word/_rels/document.xml.rels'] = ET.tostring(links, encoding='utf-8', xml_declaration=True)
    with zipfile.ZipFile(destination, 'x', zipfile.ZIP_DEFLATED) as archive:
        for name, data in parts.items():
            archive.writestr(name, data)


def combine_pdf(resume, letter, destination):
    from pdf_layout import printable_html
    try:
        from weasyprint import HTML
    except (ImportError, OSError) as exc:
        raise RuntimeError('Combined PDF export needs requirements-pdf.txt or an existing PDF tool. '
                           'The separate documents and combined Word file are preserved.') from exc
    documents = [HTML(string=printable_html(path)).render() for path in (resume, letter)]
    documents[0].copy([page for document in documents for page in document.pages]).write_pdf(destination)


def combine(directory, *, resume, format, publish, verify):
    out = Path(directory)
    inputs = [out / 'Resume.docx', out / 'Letter.docx']
    sources = {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in inputs}
    formats = ['docx', 'pdf'] if format in ('pdf', 'both') else ['docx']
    outputs = []
    # Check every existing combined output before changing any of them.
    for extension in formats:
        target = out / ('Application.' + extension)
        receipt = out / ('Application.' + extension + '.json')
        pending = out / ('.Application.' + extension + '.pending.json')
        expected = {'sources': sources, 'format': extension, 'order': ['resume', 'cover-letter']}
        if pending.exists():
            verify(pending, expected, 'combined ' + extension,
                   target if target.exists() else None, hash_field='sha256')
        if target.exists():
            saved = receipt if receipt.is_file() else pending
            if not resume or not saved.is_file():
                raise ValueError('Preserve the existing combined application and use --resume or a new revision directory')
            verify(saved, expected, 'combined ' + extension, target, hash_field='sha256')
        elif receipt.exists():
            raise ValueError('An existing combined receipt needs a new revision directory')
        outputs.append((extension, target, receipt, pending, expected))
    with tempfile.TemporaryDirectory(prefix='.get-hired-pro-combine-', dir=out) as temporary:
        for extension, target, receipt, pending, expected in outputs:
            if not target.exists():
                staged = Path(temporary) / target.name
                (combine_word if extension == 'docx' else combine_pdf)(*inputs, staged)
                pending.write_text(json.dumps({
                    **expected, 'sha256': hashlib.sha256(staged.read_bytes()).hexdigest()
                }, indent=2) + '\n', encoding='utf-8')
                publish(staged, target)
            if not receipt.exists():
                publish(pending, receipt)
            pending.unlink(missing_ok=True)
