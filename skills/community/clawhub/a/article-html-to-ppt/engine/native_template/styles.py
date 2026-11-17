"""Inspectable OOXML font/color inheritance, without invented typography defaults."""
from __future__ import annotations
from lxml import etree
from .package import A, P
from .safety import sha


def q(name): return '{%s}%s' % (A, name)


def theme_context(slide):
    master = slide.slide_layout.slide_master
    theme = None
    for rel in master.part.rels.values():
        if rel.reltype.endswith('/theme'): theme = etree.fromstring(rel.target_part.blob)
    palette = {}
    if theme is not None:
        scheme = theme.find('.//' + q('clrScheme'))
        if scheme is not None:
            for slot in scheme:
                c = next(iter(slot), None)
                if c is not None:
                    palette[etree.QName(slot).localname] = c.get('val') if etree.QName(c).localname == 'srgbClr' else c.get('lastClr')
    color_map = master._element.find('{%s}clrMap' % P)
    mapping = dict(color_map.attrib) if color_map is not None else {}
    for owner in (slide.slide_layout, slide):
        override = owner._element.find('.//' + q('overrideClrMapping'))
        if override is not None: mapping = dict(override.attrib)
    return theme, palette, mapping


def _layers(shape, slide, paragraph, run):
    level = paragraph.level + 1
    result = []
    if run is not None:
        n = run._r.find(q('rPr'))
        if n is not None: result.append(('run', n))
    n = paragraph._p.find(q('pPr'))
    if n is not None:
        n = n.find(q('defRPr'))
        if n is not None: result.append(('paragraph', n))
    owners = [('object', shape)]
    if shape.is_placeholder:
        for origin, owner in [('layout', slide.slide_layout), ('master', slide.slide_layout.slide_master)]:
            same = [s for s in owner.placeholders if (s.placeholder_format.idx == shape.placeholder_format.idx if origin == 'layout' else s.placeholder_format.type == shape.placeholder_format.type)]
            if same: owners.append((origin, same[0]))
    for origin, owner in owners:
        if not owner.has_text_frame: continue
        body = owner.text_frame._txBody
        if origin != 'object':
            # Placeholder's own paragraph defaults precede its list style.
            for p in body.findall(q('p')):
                properties = p.find(q('pPr'))
                inherited_level = int(properties.get('lvl', '0')) + 1 if properties is not None else 1
                if inherited_level != level: continue
                n = properties.find(q('defRPr')) if properties is not None else None
                if n is not None: result.append((origin + 'Paragraph.level' + str(level), n))
                break
        ls = body.find(q('lstStyle'))
        if ls is not None:
            for tag in ('lvl%dpPr' % level, 'defPPr'):
                n = ls.find(q(tag) + '/' + q('defRPr'))
                if n is not None: result.append((origin + 'ListStyle', n))
    master = slide.slide_layout.slide_master._element
    style_type = 'otherStyle'
    if shape.is_placeholder:
        t = str(shape.placeholder_format.type)
        style_type = 'titleStyle' if 'TITLE' in t and 'SUBTITLE' not in t else 'bodyStyle' if 'BODY' in t or 'OBJECT' in t else 'otherStyle'
    tx = master.find('{%s}txStyles/{%s}%s' % (P, P, style_type))
    if tx is not None:
        n = tx.find(q('lvl%dpPr' % level) + '/' + q('defRPr'))
        if n is not None: result.append(('master.' + style_type, n))
    pres = slide.part.package.presentation_part._element
    ds = pres.find('{%s}defaultTextStyle' % P)
    if ds is not None:
        n = ds.find(q('lvl%dpPr' % level) + '/' + q('defRPr'))
        if n is not None: result.append(('presentation.defaultTextStyle', n))
    return result


def resolved_text(shape, slide):
    if not shape.has_text_frame: return []
    theme, palette, mapping = theme_context(slide)
    result = []
    for pi, paragraph in enumerate(shape.text_frame.paragraphs):
        runs = list(paragraph.runs) or [None]
        for ri, run in enumerate(runs):
            layers = _layers(shape, slide, paragraph, run)
            values = {'paragraph': pi, 'run': ri, 'text': run.text if run is not None else paragraph.text}
            for attr, key, scale in [('sz', 'fontSizePt', 100), ('b', 'bold', 1), ('i', 'italic', 1)]:
                found = next(((origin, n.get(attr)) for origin, n in layers if n.get(attr) is not None), None)
                if found: values[key] = {'value': int(found[1]) / scale if attr == 'sz' else found[1] in {'1', 'true'}, 'origin': found[0]}
            for tag, key in [('latin', 'latinFont'), ('ea', 'eastAsianFont'), ('cs', 'complexScriptFont')]:
                found = next(((origin, n.find(q(tag))) for origin, n in layers if n.find(q(tag)) is not None), None)
                if found:
                    face = found[1].get('typeface'); resolved = face
                    if face and face.startswith(('+mj-', '+mn-')) and theme is not None:
                        family = 'majorFont' if face.startswith('+mj-') else 'minorFont'
                        font = theme.find('.//' + q(family) + '/' + q(tag))
                        resolved = font.get('typeface') if font is not None else None
                    values[key] = {'token': face, 'value': resolved or None, 'origin': found[0]}
            found = next(((origin, n.find(q('solidFill'))) for origin, n in layers if n.find(q('solidFill')) is not None), None)
            if found and len(found[1]):
                color = found[1][0]; local = etree.QName(color).localname
                token = color.get('val')
                rgb = token if local == 'srgbClr' else color.get('lastClr') if local == 'sysClr' else palette.get(mapping.get(token, token)) if local == 'schemeClr' else None
                transforms = [{'kind': etree.QName(c).localname, **dict(c.attrib)} for c in color]
                values['color'] = {'kind': local, 'token': token, 'baseRgb': rgb, 'resolvedRgb': rgb if not transforms else None,
                                   'transforms': transforms, 'origin': found[0]}
            values['unresolved'] = [k for k in ('fontSizePt', 'latinFont', 'color') if k not in values or (values[k].get('resolvedRgb') if k == 'color' else values[k].get('value')) is None]
            result.append(values)
    return result
