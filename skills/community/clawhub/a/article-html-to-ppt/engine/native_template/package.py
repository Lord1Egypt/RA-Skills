"""Clone selected slide relationship closures; preserve immutable template styles."""
from __future__ import annotations
from copy import deepcopy
import io
import posixpath
import zipfile
from lxml import etree
from .safety import package, xml, require, MAX_EXPANDED

P = 'http://schemas.openxmlformats.org/presentationml/2006/main'
R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
PR = 'http://schemas.openxmlformats.org/package/2006/relationships'
CT = 'http://schemas.openxmlformats.org/package/2006/content-types'
A = 'http://schemas.openxmlformats.org/drawingml/2006/main'
NS = {'p': P, 'a': A, 'r': R}


def dump(tree):
    return etree.tostring(tree, encoding='UTF-8', xml_declaration=True, standalone=True)


def relname(part):
    return posixpath.join(posixpath.dirname(part), '_rels', posixpath.basename(part) + '.rels') if part else '_rels/.rels'


def target(part, value):
    require(isinstance(value, str) and value and '\\' not in value and ':' not in value and '\x00' not in value, 'INVALID_RELATIONSHIP_TARGET')
    result = posixpath.normpath(value.lstrip('/') if value.startswith('/') else posixpath.join(posixpath.dirname(part), value))
    require(not result.startswith('../') and result != '..', 'RELATIONSHIP_ESCAPE')
    return result


SOURCE_PAGE_LIMIT = 100


def slide_inventory(parts):
    pres = xml(parts['ppt/presentation.xml'])
    rels = {r.get('Id'): target('ppt/presentation.xml', r.get('Target')) for r in xml(parts[relname('ppt/presentation.xml')])}
    ids = pres.find('{%s}sldIdLst' % P)
    result = [(s.get('id'), rels[s.get('{%s}id' % R)]) for s in ids] if ids is not None else []
    require(len(result) <= SOURCE_PAGE_LIMIT and len({s[0] for s in result}) == len(result), 'SOURCE_PAGE_LIMIT_OR_DUPLICATE_ID')
    return result


def pack(parts):
    out = io.BytesIO()
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
        for name, data in sorted(parts.items()):
            info = zipfile.ZipInfo(name, (2020, 1, 1, 0, 0, 0)); info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, data)
    return out.getvalue()


def prune(parts):
    seen = set()
    def walk(part):
        if part in seen: return
        require(part in parts, 'MISSING_RELATIONSHIP_PART: ' + part)
        seen.add(part)
        rn = relname(part)
        if rn in parts:
            seen.add(rn)
            for r in xml(parts[rn]): walk(target(part, r.get('Target')))
    seen.add('_rels/.rels')
    for r in xml(parts['_rels/.rels']): walk(target('', r.get('Target')))
    types = xml(parts['[Content_Types].xml'])
    selected_slides = {part for _, part in slide_inventory(parts)}
    typed_slides = {n.get('PartName', '').lstrip('/') for n in types if n.get('ContentType', '').casefold().endswith('presentationml.slide+xml')}
    reachable_slides = {name for name in seen if name in typed_slides or (name.casefold().startswith('ppt/slides/') and name.casefold().endswith('.xml'))}
    require(reachable_slides == selected_slides, 'UNSELECTED_SLIDE_RELATIONSHIP_REFUSED')
    for node in list(types):
        if node.tag == '{%s}Override' % CT and node.get('PartName', '').lstrip('/') not in seen: types.remove(node)
    kept = {k: v for k, v in parts.items() if k in seen}
    kept['[Content_Types].xml'] = dump(types)
    return kept


def clone_pages(template, pages):
    original = package(template)
    sources = dict(slide_inventory(original))
    parts = dict(original)
    types = xml(original['[Content_Types].xml'])
    overrides = {n.get('PartName', '').lstrip('/'): n.get('ContentType') for n in types if n.tag == '{%s}Override' % CT}
    pres = xml(parts['ppt/presentation.xml'])
    ids = pres.find('{%s}sldIdLst' % P)
    if ids is None: ids = etree.SubElement(pres, '{%s}sldIdLst' % P)
    ids.clear()
    # Custom shows / sections reference old physical slide IDs and may leak titles.
    for node in list(pres):
        if etree.QName(node).localname in {'custShowLst', 'extLst', 'tagsLst', 'custDataLst'}: pres.remove(node)
    rels = xml(parts[relname('ppt/presentation.xml')])
    for rel in list(rels):
        if not rel.get('Type', '').endswith(('/slideMaster', '/notesMaster', '/handoutMaster', '/theme', '/presProps', '/viewProps', '/tableStyles')): rels.remove(rel)
    counter = [0]
    expansion = [sum(len(v) for v in original.values())]
    def copy_part(old, mapping):
        if old in mapping: return mapping[old]
        require(not old.startswith('ppt/slides/') or not mapping, 'UNSUPPORTED_CROSS_SLIDE_LINK_RELATIONSHIP')
        # Layout/master/theme are immutable and must retain their exact bytes.
        if old.startswith(('ppt/slideLayouts/', 'ppt/slideMasters/', 'ppt/theme/', 'ppt/notesMasters/')):
            return old
        require(old in original, 'MISSING_SOURCE_PART')
        counter[0] += 1
        folder, filename = posixpath.split(old)
        new = posixpath.join(folder, 'native-%d-%s' % (counter[0], filename))
        while new in parts:
            counter[0] += 1; new = posixpath.join(folder, 'native-%d-%s' % (counter[0], filename))
        expansion[0] += len(original[old])
        require(expansion[0] <= MAX_EXPANDED, 'CLONED_PACKAGE_EXPANSION_LIMIT')
        mapping[old] = new
        parts[new] = original[old]
        if old in overrides:
            etree.SubElement(types, '{%s}Override' % CT, PartName='/' + new, ContentType=overrides[old])
        rn = relname(old)
        if rn in original:
            rr = xml(original[rn])
            for rel in rr:
                dest = copy_part(target(old, rel.get('Target')), mapping)
                rel.set('Target', posixpath.relpath(dest, posixpath.dirname(new)))
            parts[relname(new)] = dump(rr)
        return new
    for index, page in enumerate(pages):
        require(page['sourceSlideId'] in sources, 'UNKNOWN_SOURCE_SLIDE_ID')
        dest = copy_part(sources[page['sourceSlideId']], {})
        rid = 'nativePage%d' % index
        etree.SubElement(rels, '{%s}Relationship' % PR, Id=rid, Type=R + '/slide', Target=posixpath.relpath(dest, 'ppt'))
        s = etree.SubElement(ids, '{%s}sldId' % P, id=str(256 + index)); s.set('{%s}id' % R, rid)
    parts['ppt/presentation.xml'] = dump(pres)
    parts[relname('ppt/presentation.xml')] = dump(rels)
    parts['[Content_Types].xml'] = dump(types)
    return pack(prune(parts))


def canonical_workbooks(parts):
    """xlsxwriter timestamps must not change a candidate merely on re-export."""
    for name, data in list(parts.items()):
        if name.lower().endswith('.xlsx'):
            workbook = package(data, nested=True)
            if 'docProps/core.xml' in workbook:
                core = xml(workbook['docProps/core.xml'])
                for node in core:
                    if etree.QName(node).localname in {'created', 'modified'}:
                        node.text = '2020-01-01T00:00:00Z'
                workbook['docProps/core.xml'] = dump(core)
            parts[name] = pack(workbook)
    return parts


def strip_metadata(parts):
    """Do not carry a template's cached thumbnail, title list, or custom properties."""
    root = xml(parts['_rels/.rels'])
    for rel in list(root):
        if not rel.get('Type', '').endswith('/officeDocument'):
            root.remove(rel)
    parts['_rels/.rels'] = dump(root)
    return parts
