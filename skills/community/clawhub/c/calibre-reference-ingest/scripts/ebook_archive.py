#!/usr/bin/env python3
"""Inventory or extract one ebook member. Never writes archive paths or runs contents."""
import argparse
import ctypes as C
import ctypes.util
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import signal
import stat
import sys
import time
import unicodedata

EBOOK_EXTENSIONS = {'.pdf', '.epub', '.kepub', '.mobi', '.azw', '.azw3', '.azw4', '.prc', '.fb2', '.djvu', '.cbz', '.cbr', '.cb7'}
MAX_ARCHIVE = 1024 * 1024 * 1024
MAX_MEMBER = 200 * 1024 * 1024
MAX_TOTAL = 512 * 1024 * 1024
MAX_ENTRIES = 2000


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha256(path):
    with open(path, 'rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def safe_name(name):
    require(isinstance(name, str) and name, 'archive member has no name')
    require(not re.search(r'[\x00-\x1f\x7f]', name), 'control character in archive member name')
    require('\\' not in name and ':' not in name and not name.startswith('/'), 'unsafe archive member path')
    require('..' not in PurePosixPath(name).parts, 'parent traversal in archive member path')
    name.encode('utf-8', 'strict')
    normalized = unicodedata.normalize('NFC', str(PurePosixPath(name)))
    require(normalized not in ('', '.'), 'empty archive member path')
    return normalized


def archive_kind(path):
    name = path.name.lower()
    require(path.suffix.lower() not in EBOOK_EXTENSIONS, 'EPUB/CBZ/CBR/CB7 are books; import intact, do not unpack them')
    if name.endswith('.zip'):
        return 'zip'
    if name.endswith('.7z'):
        return '7zip'
    if name.endswith('.rar'):
        return 'rar'
    if name.endswith(('.tar', '.tar.gz', '.tgz', '.tar.bz2', '.tbz2', '.tar.xz', '.txz')):
        return 'tar'
    raise ValueError('supported containers: ZIP, 7z, RAR, TAR, TAR.GZ/BZ2/XZ; no nested or raw compressed streams')


def bind(lib, name, result, args):
    fn = getattr(lib, name)
    fn.restype = result
    fn.argtypes = args
    return fn


class Reader:
    def __init__(self, path):
        library = ctypes.util.find_library('archive')
        require(library, 'libarchive shared library is required for archive files; do not silently skip them')
        self.lib = C.CDLL(library)
        p, i, s = C.c_void_p, C.c_int, C.c_char_p
        specs = {
            'archive_read_new': (p, []), 'archive_read_free': (i, [p]),
            'archive_error_string': (s, [p]),
            'archive_read_open_filename': (i, [p, s, C.c_size_t]),
            'archive_read_next_header': (i, [p, C.POINTER(p)]),
            'archive_read_data': (C.c_ssize_t, [p, p, C.c_size_t]),
            'archive_read_data_skip': (i, [p]),
            'archive_entry_pathname_utf8': (s, [p]), 'archive_entry_pathname': (s, [p]),
            'archive_entry_size': (C.c_int64, [p]), 'archive_entry_filetype': (C.c_uint, [p]),
            'archive_entry_symlink': (s, [p]), 'archive_entry_hardlink': (s, [p]),
            'archive_entry_is_encrypted': (i, [p]),
        }
        for name, (result, args) in specs.items():
            bind(self.lib, name, result, args)
        self.handle = self.lib.archive_read_new()
        require(self.handle, 'cannot allocate archive reader')
        try:
            # Only built-in, known filters/formats. Never external decompressor commands.
            for name in ('none', 'gzip', 'bzip2', 'xz'):
                self.check(bind(self.lib, 'archive_read_support_filter_' + name, i, [p])(self.handle))
            kind = archive_kind(path)
            for name in (('rar', 'rar5') if kind == 'rar' else (kind,)):
                self.check(bind(self.lib, 'archive_read_support_format_' + name, i, [p])(self.handle))
            self.check(self.lib.archive_read_open_filename(self.handle, os.fsencode(path), 65536))
        except BaseException:
            self.close()
            raise

    def check(self, code):
        if code != 0:
            msg = self.lib.archive_error_string(self.handle)
            raise ValueError('archive read failed: ' + (msg.decode('utf-8', 'replace') if msg else str(code)))

    def close(self):
        if self.handle:
            self.lib.archive_read_free(self.handle)
            self.handle = None

    def entries(self):
        started = time.monotonic()
        count, total = 0, 0
        seen = set()
        while True:
            require(time.monotonic() - started < 60, 'archive time budget exceeded')
            entry = C.c_void_p()
            result = self.lib.archive_read_next_header(self.handle, C.byref(entry))
            if result == 1:
                return
            self.check(result)
            count += 1
            require(count <= MAX_ENTRIES, 'archive entry limit exceeded')
            raw = self.lib.archive_entry_pathname_utf8(entry) or self.lib.archive_entry_pathname(entry)
            require(raw, 'missing archive member name')
            name = raw.decode('utf-8', 'strict')
            kind = self.lib.archive_entry_filetype(entry)
            require(not self.lib.archive_entry_is_encrypted(entry), 'encrypted archive member is unsupported; never guess passwords')
            require(not self.lib.archive_entry_symlink(entry) and not self.lib.archive_entry_hardlink(entry), 'archive links are forbidden')
            require(kind in (stat.S_IFREG, stat.S_IFDIR), 'special archive entry is forbidden')
            if kind == stat.S_IFDIR and name in ('.', './'):
                continue
            name = safe_name(name)
            folded = name.casefold()
            require(folded not in seen, 'duplicate/colliding archive member path')
            seen.add(folded)
            size = self.lib.archive_entry_size(entry)
            require(0 <= size <= MAX_MEMBER, 'archive member size limit exceeded')
            total += size
            require(total <= MAX_TOTAL, 'archive expanded size limit exceeded')
            if kind == stat.S_IFREG:
                yield {'id': count, 'name': name, 'size': size, 'format': Path(name).suffix.lower(), 'ebook': Path(name).suffix.lower() in EBOOK_EXTENSIONS}
            self.check(self.lib.archive_read_data_skip(self.handle))

    def copy_current(self, output, declared_size):
        buf = C.create_string_buffer(65536)
        count = 0
        started = time.monotonic()
        with output.open('xb') as f:
            os.chmod(output, 0o600)
            while True:
                require(time.monotonic() - started < 60, 'archive extraction time budget exceeded')
                n = self.lib.archive_read_data(self.handle, buf, len(buf))
                if n == 0:
                    break
                if n < 0:
                    self.check(n)
                count += n
                require(count <= declared_size and count <= MAX_MEMBER, 'archive exceeded declared size')
                f.write(buf.raw[:n])
            f.flush()
            os.fsync(f.fileno())
        require(count == declared_size, 'archive member was truncated')


def inventory(path):
    path = Path(path).expanduser().resolve()
    require(path.is_file() and 0 < path.stat().st_size <= MAX_ARCHIVE, 'archive missing, empty, or larger than 1 GiB')
    kind = archive_kind(path)
    before = sha256(path)
    reader = Reader(path)
    try:
        all_members = list(reader.entries())
    finally:
        reader.close()
    require(before == sha256(path), 'archive changed during inventory')
    members = [m for m in all_members if m['ebook']]
    return {'ok': True, 'status': 'inventoried', 'archive': str(path), 'archive_sha256': before,
            'kind': kind, 'members': members, 'ignored_non_ebook': len(all_members) - len(members)}


def extract(path, expected_sha256, member_id, output_dir):
    index = inventory(path)  # Validate every entry before writing anything.
    require(index['archive_sha256'] == expected_sha256, 'archive changed since the reviewed inventory')
    selected = [m for m in index['members'] if m['id'] == member_id]
    require(len(selected) == 1, 'selected member is not an eligible ebook')
    member = selected[0]
    require(member['size'] > 0, 'empty ebook member')
    out = Path(output_dir).expanduser().resolve()
    require(not out.exists(), 'output directory exists; never overwrite extracted files')
    out.mkdir(parents=True, mode=0o700)
    partial = out / 'ebook.partial'
    final = out / ('ebook' + member['format'])
    reader = Reader(Path(index['archive']))
    copied = False
    try:
        for row in reader.entries():
            if row['id'] == member_id:
                require(row == member, 'archive member changed')
                reader.copy_current(partial, member['size'])
                copied = True
        require(copied, 'archive member disappeared')
    finally:
        reader.close()
    require(sha256(index['archive']) == expected_sha256, 'archive changed during extraction; partial output is not ready')
    partial.rename(final)
    result = {'ok': True, 'status': 'extracted', 'file': str(final), 'source_sha256': sha256(final),
              'archive': index['archive'], 'archive_sha256': expected_sha256, 'archive_member': member['name']}
    receipt = out / 'extraction.json'
    with receipt.open('x', encoding='utf-8') as f:
        os.chmod(receipt, 0o600)
        json.dump(result, f, ensure_ascii=False, indent=2)
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    subs = p.add_subparsers(dest='command', required=True)
    for name in ('list', 'extract'):
        sub = subs.add_parser(name)
        sub.add_argument('--archive', required=True)
        if name == 'extract':
            sub.add_argument('--sha256', required=True)
            sub.add_argument('--member-id', type=int, required=True)
            sub.add_argument('--output-dir', required=True)
    args = p.parse_args()
    try:
        if hasattr(signal, 'SIGALRM'):
            def deadline(signum, frame):
                raise TimeoutError('archive time budget exceeded')
            signal.signal(signal.SIGALRM, deadline)
            signal.alarm(120)
        result = inventory(args.archive) if args.command == 'list' else extract(args.archive, args.sha256, args.member_id, args.output_dir)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:
        print(json.dumps({'ok': False, 'error': str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1
    finally:
        if hasattr(signal, 'SIGALRM'):
            signal.alarm(0)


if __name__ == '__main__':
    sys.exit(main())
