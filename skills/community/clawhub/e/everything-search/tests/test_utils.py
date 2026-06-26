"""
Tests for utility functions.
"""

import unittest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils import (
    format_size,
    encode_keyword,
    get_file_extension,
    is_image_file,
    is_document_file,
    is_archive_file
)


class TestFormatSize(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(format_size(0), "0 B")
    
    def test_bytes(self):
        self.assertEqual(format_size(512), "512 B")
        self.assertEqual(format_size(1023), "1023 B")
    
    def test_kilobytes(self):
        self.assertEqual(format_size(1024), "1.0 KB")
        self.assertEqual(format_size(2048), "2.0 KB")
        self.assertEqual(format_size(1536), "1.5 KB")
    
    def test_megabytes(self):
        self.assertEqual(format_size(1048576), "1.0 MB")
        self.assertEqual(format_size(2097152), "2.0 MB")
    
    def test_gigabytes(self):
        self.assertEqual(format_size(1073741824), "1.0 GB")


class TestEncodeKeyword(unittest.TestCase):
    def test_english(self):
        self.assertEqual(encode_keyword("test"), "test")
        self.assertEqual(encode_keyword("hello world"), "hello%20world")
    
    def test_chinese(self):
        # 数据 should be encoded
        encoded = encode_keyword("数据")
        self.assertEqual(encoded, "%E6%95%B0%E6%8D%AE")
    
    def test_mixed(self):
        encoded = encode_keyword("测试 test")
        self.assertIn("test", encoded)


class TestFileExtension(unittest.TestCase):
    def test_get_extension(self):
        self.assertEqual(get_file_extension("file.txt"), "txt")
        self.assertEqual(get_file_extension("file.JPG"), "jpg")
        self.assertEqual(get_file_extension("archive.tar.gz"), "gz")
        self.assertEqual(get_file_extension("noextension"), "")
    
    def test_is_image(self):
        self.assertTrue(is_image_file("photo.jpg"))
        self.assertTrue(is_image_file("image.PNG"))
        self.assertFalse(is_image_file("document.pdf"))
    
    def test_is_document(self):
        self.assertTrue(is_document_file("report.pdf"))
        self.assertTrue(is_document_file("data.xlsx"))
        self.assertTrue(is_document_file("notes.md"))
        self.assertFalse(is_document_file("photo.jpg"))
    
    def test_is_archive(self):
        self.assertTrue(is_archive_file("backup.zip"))
        self.assertTrue(is_archive_file("archive.tar.gz"))
        self.assertFalse(is_archive_file("document.pdf"))


if __name__ == "__main__":
    unittest.main()
