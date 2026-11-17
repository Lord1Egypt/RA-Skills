"""Pure résumé production; explicit layout roles, unchanged prose, no packet side effects.

CLI: python3 resume_layout.py layout.json OUTPUT.docx
Input: {"blocks": [{"kind": "name|contact|headline|summary|section|role_header|
context|achievement|publication|skills|education", "text": "...", "role_id": "..."}]}
Assign semantic kinds in the existing production job, not in another writing call.
Achievement bullets are layout, not a requirement to turn all body prose into lists.
"""
import hashlib
import json
from pathlib import Path
import re
import sys
import zipfile
import xml.etree.ElementTree as E

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
E.register_namespace('w', W)
E.register_namespace('r', R)
KINDS = {'name', 'contact', 'headline', 'summary', 'section', 'role_header',
         'context', 'achievement', 'publication', 'skills', 'education'}
BOLD = {'name', 'headline', 'section', 'role_header'}


def q(s):
    return '{' + W + '}' + s



MARKDOWN_START = re.compile(r'\[([^\]\n]+)\]\((https?://)')
BARE_LINK = re.compile(r'https?://[^\s<>]+')


def bare_link_runs(text):
    cursor = 0
    for match in BARE_LINK.finditer(text):
        if match.start() > cursor:
            yield text[cursor:match.start()], None
        visible = match.group()
        if visible.startswith(('http://', 'https://')):
            tail = ''
            quote = {'"': '"', "'": "'", '“': '”', '‘': '’'}.get(
                text[match.start() - 1] if match.start() else '')
            closing = visible.rfind(quote) if quote else -1
            quoted = closing >= len('https://')
            if quoted:
                visible, tail = visible[:closing], visible[closing:]
            while visible and not quoted:
                last = visible[-1]
                unmatched = any(last == close and visible.count(close) > visible.count(opened)
                                for opened, close in [('(', ')'), ('[', ']'), ('{', '}')])
                if last in '.,;:!?' or unmatched:
                    tail = last + tail
                    visible = visible[:-1]
                else:
                    break
            yield visible, visible
            if tail:
                yield tail, None
        cursor = match.end()
    if cursor < len(text):
        yield text[cursor:], None


def inline_link_runs(text):
    cursor = 0
    for match in MARKDOWN_START.finditer(text):
        if match.start() < cursor:
            continue
        end, depth = match.end(), 1
        while end < len(text) and not text[end].isspace():
            if text[end] == '(':
                depth += 1
            elif text[end] == ')':
                depth -= 1
                if not depth:
                    break
            end += 1
        if depth:
            continue
        yield from bare_link_runs(text[cursor:match.start()])
        yield match.group(1), text[match.start(2):end]
        cursor = end + 1
    yield from bare_link_runs(text[cursor:])


def rendered_text(text):
    return ''.join(part for part, target in inline_link_runs(text))


def validate_xml_text(text):
    if not isinstance(text, str) or not text.strip():
        raise ValueError('Document paragraphs must contain nonempty text')
    if any(not (ord(c) in (9, 10, 13) or 0x20 <= ord(c) <= 0xD7FF
                    or 0xE000 <= ord(c) <= 0xFFFD or 0x10000 <= ord(c) <= 0x10FFFF)
           for c in text):
        raise ValueError('Document text contains an XML-invalid character; correct the source text before export')


def validate_blocks(blocks):
    if not isinstance(blocks, list) or not blocks or not isinstance(blocks[0], dict) or blocks[0].get('kind') != 'name':
        raise ValueError('first block must identify the name')
    for b in blocks:
        if not isinstance(b, dict):
            raise ValueError('each block must be a layout object')
        if set(b) - {'kind', 'text', 'role_id'}:
            raise ValueError('unknown layout option; no ad-hoc breaks/style overrides')
        if b.get('kind') not in KINDS:
            raise ValueError('every block needs an explicit kind and nonempty exact text')
        validate_xml_text(b.get('text'))
        if '\n' in b['text'] or '\r' in b['text']:
            raise ValueError('one source paragraph per block')
        if 'role_id' in b and (not isinstance(b['role_id'], str) or not b['role_id'].strip()):
            raise ValueError('role_id must be a nonempty string')
        if b['kind'] in {'role_header', 'achievement', 'context'} and not b.get('role_id'):
            raise ValueError('role content must identify its role')
    role_ids = [b['role_id'] for b in blocks if b['kind'] == 'role_header']
    if len(set(role_ids)) != len(role_ids):
        raise ValueError('duplicate role header identity')
    for b in blocks:
        if b.get('role_id') and b['role_id'] not in role_ids:
            raise ValueError('role content without a header')
    for ident in role_ids:
        indices = [i for i, b in enumerate(blocks) if b.get('role_id') == ident]
        if indices != list(range(min(indices), max(indices) + 1)):
            raise ValueError('role content must remain contiguous')
    return blocks


def build(spec, destination):
    blocks = validate_blocks(spec['blocks'])
    root = E.Element(q('document'))
    body = E.SubElement(root, q('body'))
    rels = E.Element('Relationships', xmlns='http://schemas.openxmlformats.org/package/2006/relationships')
    rendered = []
    for i, b in enumerate(blocks):
        kind, text = b['kind'], b['text']
        if kind == 'achievement' and not text.startswith('• '):
            text = '• ' + text
        rendered.append(rendered_text(text))
        p = E.SubElement(body, q('p'))
        pp = E.SubElement(p, q('pPr'))
        # Readable list separation/leading from the approved spacing calibration;
        # pagination follows role grouping, never a page-fill percentage target.
        before = '240' if kind == 'section' else ('160' if kind in BOLD and i > 2 else '0')
        after = '100' if kind in {'role_header', 'achievement'} else '140'
        E.SubElement(pp, q('spacing'), {q('before'): before,
                                      q('after'): after, q('line'): '264', q('lineRule'): 'auto'})
        E.SubElement(pp, q('keepLines'))
        same_role = bool(b.get('role_id')) and i + 1 < len(blocks) and b['role_id'] == blocks[i+1].get('role_id')
        if kind in {'headline', 'section', 'role_header'} or (kind == 'context' and same_role):
            E.SubElement(pp, q('keepNext'))
        if kind == 'achievement':
            E.SubElement(pp, q('ind'), {q('left'): '160', q('hanging'): '160'})
        for part, target in inline_link_runs(text):
            if not part:
                continue
            container = p
            if target:
                rid = 'rId' + str(len(rels) + 1)
                E.SubElement(rels, 'Relationship', Id=rid, Type=R + '/hyperlink', Target=target, TargetMode='External')
                container = E.SubElement(p, q('hyperlink'), {'{' + R + '}id': rid})
            run = E.SubElement(container, q('r'))
            rp = E.SubElement(run, q('rPr'))
            E.SubElement(rp, q('rFonts'), {q('ascii'): 'Calibri', q('hAnsi'): 'Calibri'})
            # Approved baseline uses 12pt body / 16pt name.
            E.SubElement(rp, q('sz'), {q('val'): '32' if kind == 'name' else '24'})
            if kind in BOLD:
                E.SubElement(rp, q('b'))
            E.SubElement(run, q('t'), {'{http://www.w3.org/XML/1998/namespace}space': 'preserve'}).text = part
    sect = E.SubElement(body, q('sectPr'))
    E.SubElement(sect, q('pgSz'), {q('w'): '12240', q('h'): '15840'})
    E.SubElement(sect, q('pgMar'), {q('top'): '800', q('bottom'): '800', q('left'): '850', q('right'): '850', q('header'): '0', q('footer'): '0', q('gutter'): '0'})
    content_types = '<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/></Types>'
    package = '<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>'
    destination = Path(destination)
    with zipfile.ZipFile(destination, 'w', zipfile.ZIP_DEFLATED) as z:
        for name, value in {'[Content_Types].xml': content_types, '_rels/.rels': package,
                            'word/document.xml': E.tostring(root, encoding='utf-8', xml_declaration=True),
                            'word/_rels/document.xml.rels': E.tostring(rels, encoding='utf-8', xml_declaration=True)}.items():
            z.writestr(name, value)
    receipt = {'renderer': str(Path(__file__).resolve()), 'renderer_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               'source_blocks': blocks, 'rendered_paragraphs': rendered, 'source_wording_preserved': True,
               'text_representation': 'inline-links-v1',
               'docx_sha256': hashlib.sha256(destination.read_bytes()).hexdigest(),
               'status': 'BUILT_ONLY: export and inspect pages with available document tools before calling layout verified'}
    destination.with_suffix('.layout.json').write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    return receipt


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit('Usage: python3 resume_layout.py layout.json OUTPUT.docx')
    try:
        receipt = build(json.loads(Path(sys.argv[1]).read_text(encoding='utf-8')), sys.argv[2])
        print(receipt['status'])
    except (OSError, ValueError, KeyError, TypeError) as exc:
        sys.exit('FAIL: ' + str(exc))
