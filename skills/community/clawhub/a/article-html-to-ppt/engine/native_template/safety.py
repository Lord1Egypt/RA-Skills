"""Bounded JSON/OOXML input and symlink-safe workspace transactions."""
from __future__ import annotations
import contextlib
try:
    import fcntl
except ImportError:  # Discovery remains available; workspace execution fails closed.
    fcntl = None
import hashlib
import io
import json
import math
import os
import posixpath
from pathlib import Path, PurePosixPath
import tempfile
import zipfile
from lxml import etree

MAX_BYTES = 64 * 1024 * 1024
MAX_EXPANDED = 256 * 1024 * 1024


def require(condition, message):
    if not condition:
        raise ValueError(message)


def workspace_supported():
    return fcntl is not None and callable(getattr(fcntl, 'flock', None)) and hasattr(os, 'O_NOFOLLOW')


def require_workspace_platform():
    require(workspace_supported(), 'PLATFORM_UNSUPPORTED_REQUIRES_POSIX_FCNTL_AND_O_NOFOLLOW')


def sha(data):
    return 'sha256:' + hashlib.sha256(data).hexdigest()


def encode(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def strict_json(data):
    require(len(data) <= 8 * 1024 * 1024, 'JSON_LIMIT')
    def pairs(items):
        result = {}
        for k, v in items:
            require(k not in result, 'DUPLICATE_JSON_KEY')
            require(k not in {'__proto__', 'constructor', 'prototype'}, 'UNSAFE_JSON_KEY')
            result[k] = v
        return result
    def constant(value):
        raise ValueError('NON_FINITE_NUMBER')
    value = json.loads(data, object_pairs_hook=pairs, parse_constant=constant)
    def visit(item, depth=0):
        require(depth < 40, 'JSON_DEPTH_LIMIT')
        if isinstance(item, float):
            require(math.isfinite(item), 'NON_FINITE_NUMBER')
        if isinstance(item, dict):
            for child in item.values(): visit(child, depth + 1)
        if isinstance(item, list):
            require(len(item) <= 10000, 'JSON_ARRAY_LIMIT')
            for child in item: visit(child, depth + 1)
    visit(value)
    return value


def fields(value, allowed, required=()):
    require(isinstance(value, dict), 'EXPECTED_OBJECT')
    require(not (set(value) - set(allowed)), 'UNKNOWN_FIELDS: ' + ','.join(sorted(set(value) - set(allowed))))
    require(set(required) <= set(value), 'MISSING_FIELDS: ' + ','.join(sorted(set(required) - set(value))))


def safe_path(value):
    path = Path(os.path.abspath(value))
    for part in [path, *path.parents]:
        require(not part.is_symlink(), 'SYMLINK_REFUSED: ' + str(part))
    return path


def read_file(value, limit=MAX_BYTES):
    require_workspace_platform()
    path = safe_path(value)
    require(path.is_file(), 'FILE_REQUIRED: ' + str(path))
    require(path.stat().st_size <= limit, 'FILE_SIZE_LIMIT')
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(fd, 'rb') as stream:
        data = stream.read(limit + 1)
    require(len(data) <= limit, 'FILE_SIZE_LIMIT')
    return data


def xml(data):
    # Reject declarations even for UTF-16 XML; disable every expansion/network path.
    probe = data.replace(b'\x00', b'').upper()
    require(b'<!DOCTYPE' not in probe and b'<!ENTITY' not in probe, 'XML_DTD_ENTITY_REFUSED')
    tree = etree.fromstring(data, etree.XMLParser(resolve_entities=False, no_network=True, load_dtd=False, huge_tree=False))
    _check_xml_objects(tree)
    return tree


def _active_type(value):
    lowered = value.casefold()
    return any(token in lowered for token in ('activex', 'oleobject', 'vba', 'macro', 'control',
                                               'ctrlprop', 'attachedtemplate', 'customui', 'webextension',
                                               'javascript', 'ecmascript', 'scripting'))


def _check_xml_objects(tree):
    banned = {'oleobj', 'oleobject', 'oleobjects', 'control', 'controls', 'controlpr',
              'controlproperties', 'ocx', 'ocxpr', 'script', 'scripts', 'scripting',
              'macro', 'fmlamacro', 'vbaproject', 'vbadata', 'vba', 'activex'}
    for node in tree.iter():
        if not isinstance(node.tag, str): continue
        tag = etree.QName(node)
        require(tag.localname.casefold() not in banned and not _active_type(tag.namespace or ''),
                'ACTIVE_OBJECT_XML_REFUSED')
        for key, value in node.attrib.items():
            local = etree.QName(key).localname.casefold()
            require(local not in {'macro', 'classid', 'onload', 'onclick', 'onaction'}, 'ACTIVE_OBJECT_XML_REFUSED')
            if local == 'action':
                require(not any(token in value.casefold() for token in ('ppaction://macro', 'ppaction://program', 'javascript:', 'vbscript:')),
                        'ACTIVE_OBJECT_ACTION_REFUSED')


def package(data, nested=False):
    require(len(data) <= MAX_BYTES, 'ZIP_SIZE_LIMIT')
    parts = {}
    folded_names = set()
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        infos = z.infolist()
        require(len(infos) <= 10000, 'ZIP_ENTRY_LIMIT')
        require(len({i.filename.casefold() for i in infos}) == len(infos), 'ZIP_DUPLICATE_ENTRY')
        require(sum(i.file_size for i in infos) <= MAX_EXPANDED, 'ZIP_EXPANSION_LIMIT')
        require('[Content_Types].xml' in z.namelist(), 'NOT_OPC_PACKAGE')
        ct_info = z.getinfo('[Content_Types].xml')
        require(ct_info.file_size <= MAX_BYTES and ct_info.file_size / max(ct_info.compress_size, 1) < 1000, 'ZIP_PART_LIMIT')
        content_types = xml(z.read(ct_info))
        require(not any(_active_type(n.get('ContentType', '')) for n in content_types), 'ACTIVE_CONTENT_TYPE_REFUSED')
        overrides = {n.get('PartName', '').lstrip('/'): n.get('ContentType', '').casefold() for n in content_types if n.get('PartName')}
        defaults = {n.get('Extension', '').casefold(): n.get('ContentType', '').casefold() for n in content_types if n.get('Extension')}
        for i in infos:
            name = i.filename
            require(name.casefold() not in folded_names, 'ZIP_DUPLICATE_ENTRY')
            folded_names.add(name.casefold())
            require(not i.is_dir() and not name.startswith('/') and '\\' not in name and ':' not in name and '%' not in name and all(p not in {'', '.', '..'} for p in name.split('/')), 'ZIP_UNSAFE_PATH')
            require((i.external_attr >> 16) & 0o170000 != 0o120000, 'ZIP_SYMLINK')
            require(not i.flag_bits & 1, 'ZIP_ENCRYPTION_REFUSED')
            require(i.file_size <= MAX_BYTES and (i.compress_size > 0 or i.file_size == 0), 'ZIP_PART_LIMIT')
            require(i.file_size / max(i.compress_size, 1) < 1000, 'ZIP_COMPRESSION_LIMIT')
            lower = name.lower()
            require(not any(t in lower for t in ('vbaproject', 'activex', 'oleobject', 'macros', '_xmlsignatures')), 'ACTIVE_CONTENT_REFUSED')
            content = z.read(i)
            declared_type = overrides.get(name, defaults.get(name.rsplit('.', 1)[-1].casefold(), ''))
            if lower.endswith(('.xml', '.rels')) or declared_type.endswith(('+xml', '/xml')) or name == '[Content_Types].xml':
                tree = xml(content)
                require(sum(1 for _ in tree.iter()) <= 200000, 'XML_NODE_LIMIT')
                if name == '[Content_Types].xml':
                    require(not any(_active_type(n.get('ContentType', '')) for n in tree), 'ACTIVE_CONTENT_TYPE_REFUSED')
                if name.lower().endswith('.rels'):
                    for rel in tree:
                        require(rel.get('TargetMode') in {None, 'Internal'}, 'EXTERNAL_RELATIONSHIP_REFUSED')
                        require(not _active_type(rel.get('Type', '')), 'ACTIVE_RELATIONSHIP_REFUSED')
            if lower.startswith('ppt/embeddings/'):
                require(lower.endswith('.xlsx'), 'UNSUPPORTED_EMBEDDED_OBJECT')
            if lower.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tif', '.tiff')):
                from PIL import Image
                with Image.open(io.BytesIO(content)) as image:
                    require(0 < image.width <= 16384 and 0 < image.height <= 16384 and image.width * image.height <= 20000000, 'IMAGE_PIXEL_LIMIT')
                    image.verify()
            if lower.endswith('.xlsx'):
                require(not nested, 'NESTED_ARCHIVE_LIMIT')
                package(content, nested=True)
            parts[name] = content
    require('[Content_Types].xml' in parts and '_rels/.rels' in parts, 'NOT_OPC_PACKAGE')
    for name, content in parts.items():
        if name.lower().endswith('.rels'):
            owner = '' if name == '_rels/.rels' else posixpath.join(posixpath.dirname(posixpath.dirname(name)), posixpath.basename(name)[:-5])
            seen_ids = set()
            for rel in xml(content):
                require(rel.get('Id') not in seen_ids, 'DUPLICATE_RELATIONSHIP_ID')
                seen_ids.add(rel.get('Id'))
                value = rel.get('Target', '')
                require(value and ':' not in value and '\\' not in value and not any(ord(c) < 32 for c in value), 'INVALID_RELATIONSHIP_TARGET')
                dest = posixpath.normpath(value.lstrip('/') if value.startswith('/') else posixpath.join(posixpath.dirname(owner), value))
                require(not dest.startswith('../') and dest != '..' and dest in parts, 'MISSING_OR_ESCAPED_RELATIONSHIP_TARGET')
    return parts


def atomic(path, data):
    path = safe_path(path)
    fd, name = tempfile.mkstemp(prefix='.atomic-', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(data); stream.flush(); os.fsync(stream.fileno())
        safe_path(path)
        os.replace(name, path)
    finally:
        if os.path.exists(name): os.unlink(name)


def scan_workspace(root):
    safe_path(root)
    for base, dirs, files in os.walk(root, followlinks=False):
        for name in dirs + files: safe_path(Path(base) / name)


@contextlib.contextmanager
def locked(workspace, create=False):
    require_workspace_platform()
    root = safe_path(workspace)
    if create: root.mkdir(parents=True, exist_ok=True)
    require(root.is_dir(), 'WORKSPACE_REQUIRED')
    scan_workspace(root)
    fd = os.open(root / '.native-template.lock', os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        scan_workspace(root)
        yield root
    finally:
        fcntl.flock(fd, fcntl.LOCK_UN); os.close(fd)
