import ctypes as C
import ctypes.util
import importlib.util
import io
import json
from pathlib import Path
import stat
import sys
import tarfile
import tempfile
import unittest
from unittest.mock import patch
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import ebook_archive as arc


@unittest.skipUnless(ctypes.util.find_library('archive'), 'libarchive required')
class Archives(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='ebook-archive-test-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def zip(self, pairs, name='books.zip'):
        f = self.root / name
        with zipfile.ZipFile(f, 'w', compression=zipfile.ZIP_DEFLATED) as z:
            for path, value in pairs:
                z.writestr(path, value)
        return f

    def test_only_books_selected_and_bytes_preserved(self):
        archive = self.zip([('books/日本語.pdf', b'%PDF-synthetic'), ('web.html', b'<html>no</html>'), ('notes.md', b'# no'), ('nested.zip', b'not-recursed')])
        index = arc.inventory(archive)
        self.assertEqual([m['name'] for m in index['members']], ['books/日本語.pdf'])
        self.assertEqual(index['ignored_non_ebook'], 3)
        out = arc.extract(archive, index['archive_sha256'], index['members'][0]['id'], self.root / 'out')
        self.assertEqual(Path(out['file']).read_bytes(), b'%PDF-synthetic')
        self.assertEqual(Path(out['file']).name, 'ebook.pdf')
        self.assertEqual(out['archive_member'], 'books/日本語.pdf')
        self.assertTrue(archive.exists())
        self.assertTrue((self.root / 'out/extraction.json').is_file())

    def test_path_traversal_absolute_and_windows_names_rejected(self):
        for num, name in enumerate(('../evil.pdf', '/tmp/evil.pdf', 'C:/evil.pdf', '..\\evil.pdf')):
            with self.subTest(name=name):
                path = self.zip([(name, b'%PDF-synthetic')], str(num) + '.zip')
                with self.assertRaises(ValueError):
                    arc.inventory(path)

    def test_links_rejected_even_when_unselected(self):
        for linktype in (tarfile.SYMTYPE, tarfile.LNKTYPE):
            f = self.root / (str(linktype) + '.tar')
            with tarfile.open(f, 'w') as t:
                e = tarfile.TarInfo('escape.pdf'); e.type = linktype; e.linkname = '/etc/passwd'; t.addfile(e)
            with self.subTest(linktype=linktype), self.assertRaisesRegex(ValueError, 'links'):
                arc.inventory(f)

    def test_zip_symlink_rejected(self):
        f = self.root / 'symlink.zip'
        with zipfile.ZipFile(f, 'w') as z:
            entry = zipfile.ZipInfo('link.pdf'); entry.create_system = 3; entry.external_attr = (stat.S_IFLNK | 0o777) << 16
            z.writestr(entry, '../outside')
        with self.assertRaisesRegex(ValueError, 'links'):
            arc.inventory(f)

    def test_case_collisions_rejected(self):
        f = self.zip([('Book.pdf', b'x'), ('book.pdf', b'y')])
        with self.assertRaisesRegex(ValueError, 'colliding'):
            arc.inventory(f)

    def test_encryption_flag_rejected(self):
        f = self.zip([('book.pdf', b'%PDF-synthetic')])
        data = bytearray(f.read_bytes()); data[6] |= 1
        central = data.index(b'PK\x01\x02'); data[central + 8] |= 1
        f.write_bytes(data)
        with self.assertRaisesRegex(ValueError, 'encrypt'):
            arc.inventory(f)

    def test_bounded_entries_and_expanded_sizes(self):
        f = self.zip([('one.pdf', b'abc'), ('two.pdf', b'def')])
        with patch.object(arc, 'MAX_ENTRIES', 1), self.assertRaisesRegex(ValueError, 'entry limit'):
            arc.inventory(f)
        with patch.object(arc, 'MAX_MEMBER', 2), self.assertRaisesRegex(ValueError, 'member size limit'):
            arc.inventory(f)
        with patch.object(arc, 'MAX_TOTAL', 5), self.assertRaisesRegex(ValueError, 'expanded size limit'):
            arc.inventory(f)

    def test_tar_gzip_bzip2_xz(self):
        for mode, suffix in (('w', '.tar'), ('w:gz', '.tar.gz'), ('w:bz2', '.tar.bz2'), ('w:xz', '.tar.xz')):
            f = self.root / ('books' + suffix)
            with tarfile.open(f, mode) as t:
                b = b'%PDF-synthetic'; e = tarfile.TarInfo('./book.pdf'); e.size = len(b); t.addfile(e, io.BytesIO(b))
            with self.subTest(suffix=suffix):
                index = arc.inventory(f)
                out = arc.extract(f, index['archive_sha256'], index['members'][0]['id'], self.root / ('out' + suffix))
                self.assertEqual(Path(out['file']).read_bytes(), b)

    def test_7zip_native_reader(self):
        lib = C.CDLL(ctypes.util.find_library('archive'))
        p, i, s = C.c_void_p, C.c_int, C.c_char_p
        specs = {'archive_write_new': (p, []), 'archive_write_set_format_7zip': (i, [p]),
                 'archive_write_open_filename': (i, [p, s]), 'archive_write_header': (i, [p, p]),
                 'archive_write_data': (C.c_ssize_t, [p, p, C.c_size_t]), 'archive_write_close': (i, [p]),
                 'archive_write_free': (i, [p]), 'archive_entry_new': (p, []), 'archive_entry_free': (None, [p]),
                 'archive_entry_set_pathname': (None, [p, s]), 'archive_entry_set_size': (None, [p, C.c_int64]),
                 'archive_entry_set_filetype': (None, [p, C.c_uint]), 'archive_entry_set_perm': (None, [p, C.c_uint])}
        for name, (result, args) in specs.items():
            arc.bind(lib, name, result, args)
        path = self.root / 'books.7z'
        handle = lib.archive_write_new(); entry = lib.archive_entry_new()
        body = b'%PDF-synthetic 7zip'; buffer = C.create_string_buffer(body)
        try:
            self.assertEqual(lib.archive_write_set_format_7zip(handle), 0)
            self.assertEqual(lib.archive_write_open_filename(handle, str(path).encode()), 0)
            lib.archive_entry_set_pathname(entry, b'book.pdf'); lib.archive_entry_set_size(entry, len(body))
            lib.archive_entry_set_filetype(entry, stat.S_IFREG); lib.archive_entry_set_perm(entry, 0o600)
            self.assertEqual(lib.archive_write_header(handle, entry), 0)
            self.assertEqual(lib.archive_write_data(handle, buffer, len(body)), len(body))
            self.assertEqual(lib.archive_write_close(handle), 0)
        finally:
            lib.archive_entry_free(entry); lib.archive_write_free(handle)
        index = arc.inventory(path)
        result = arc.extract(path, index['archive_sha256'], index['members'][0]['id'], self.root / '7z-out')
        self.assertEqual(Path(result['file']).read_bytes(), body)

    def test_archive_change_and_clobber_rejected(self):
        f = self.zip([('book.pdf', b'%PDF-first')]); index = arc.inventory(f)
        self.zip([('book.pdf', b'%PDF-second')])
        with self.assertRaisesRegex(ValueError, 'changed since'):
            arc.extract(f, index['archive_sha256'], 1, self.root / 'out')
        self.assertFalse((self.root / 'out').exists())
        index = arc.inventory(f); (self.root / 'out').mkdir()
        with self.assertRaisesRegex(ValueError, 'output directory exists'):
            arc.extract(f, index['archive_sha256'], 1, self.root / 'out')

    def test_epub_comic_archives_are_not_unpacked(self):
        for ext in ('.epub', '.cbz', '.cbr', '.cb7'):
            f = self.root / ('book' + ext); f.write_bytes(b'book')
            with self.subTest(ext=ext), self.assertRaisesRegex(ValueError, 'import intact'):
                arc.inventory(f)

    def test_empty_ebook_set_is_explicit(self):
        f = self.zip([('web.html', b'web'), ('notes.txt', b'text')])
        index = arc.inventory(f)
        self.assertEqual(index['members'], [])
        with self.assertRaisesRegex(ValueError, 'not an eligible ebook'):
            arc.extract(f, index['archive_sha256'], 1, self.root / 'out')


if __name__ == '__main__':
    unittest.main()
