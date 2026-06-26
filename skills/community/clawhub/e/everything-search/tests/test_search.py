"""
Tests for Everything Search module.
"""

import unittest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from everything_search import EverythingSearch, SearchItem, SearchResult
from utils import format_size, encode_keyword, check_connection


class TestSearchItem(unittest.TestCase):
    """Test SearchItem class."""
    
    def test_format_size_bytes(self):
        item = SearchItem(
            name="test.txt",
            path="",
            full_path="test.txt",
            item_type="file",
            size=512
        )
        self.assertEqual(item.format_size(), "512 B")
    
    def test_format_size_kb(self):
        item = SearchItem(
            name="test.txt",
            path="",
            full_path="test.txt",
            item_type="file",
            size=2048
        )
        self.assertEqual(item.format_size(), "2.0 KB")
    
    def test_format_size_mb(self):
        item = SearchItem(
            name="test.zip",
            path="",
            full_path="test.zip",
            item_type="file",
            size=1572864  # 1.5 MB
        )
        self.assertEqual(item.format_size(), "1.5 MB")
    
    def test_format_size_zero(self):
        item = SearchItem(
            name="folder",
            path="",
            full_path="folder",
            item_type="folder",
            size=0
        )
        self.assertEqual(item.format_size(), "0 B")


class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions."""
    
    def test_format_size(self):
        self.assertEqual(format_size(0), "0 B")
        self.assertEqual(format_size(512), "512 B")
        self.assertEqual(format_size(2048), "2.0 KB")
        self.assertEqual(format_size(1048576), "1.0 MB")
    
    def test_encode_keyword(self):
        # English
        self.assertEqual(encode_keyword("test"), "test")
        
        # Chinese
        self.assertEqual(encode_keyword("数据"), "%E6%95%B0%E6%8D%AE")
        
        # Mixed
        encoded = encode_keyword("测试 test")
        self.assertIn("%E6%B5%8B%E8%AF%95", encoded)


class TestEverythingSearch(unittest.TestCase):
    """Test EverythingSearch class."""
    
    def setUp(self):
        self.search = EverythingSearch(port=2853)
    
    def test_init(self):
        self.assertEqual(self.search.port, 2853)
        self.assertEqual(self.search.host, "127.0.0.1")
        self.assertEqual(self.search.timeout, 10)
    
    def test_build_url(self):
        url = self.search._build_url("test")
        self.assertIn("search=test", url)
        self.assertIn("json=1", url)
    
    def test_build_url_chinese(self):
        url = self.search._build_url("数据")
        self.assertIn("search=%E6%95%B0%E6%8D%AE", url)
    
    def test_check_connection(self):
        # This will fail if Everything is not running
        # which is expected in test environment
        result = self.search.check_connection()
        # Just verify it returns a boolean
        self.assertIsInstance(result, bool)


if __name__ == "__main__":
    unittest.main()
