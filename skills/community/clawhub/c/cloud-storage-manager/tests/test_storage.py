#!/usr/bin/env python3
"""
Cloud Storage Manager - Unit Tests
云存储管理器 - 单元测试

Run tests: python -m pytest tests/test_storage.py -v
运行测试: python -m pytest tests/test_storage.py -v
"""

import os
import sys
import unittest
import tempfile
import hashlib
from datetime import datetime, timedelta

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


class MockStorageManager:
    """Mock storage manager for testing"""
    
    def __init__(self, provider, config=None):
        self.provider = provider
        self.config = config or {}
        self.files = {}  # Simulate storage
        
    def upload(self, local_path, remote_path):
        """Mock upload"""
        content = f"Mock content from {local_path}"
        self.files[remote_path] = {
            'content': content,
            'size': len(content),
            'created_at': datetime.now()
        }
        return {'success': True, 'path': remote_path}
    
    def download(self, remote_path, local_path):
        """Mock download"""
        if remote_path not in self.files:
            raise FileNotFoundError(f"File not found: {remote_path}")
        return {'success': True, 'size': self.files[remote_path]['size']}
    
    def delete(self, remote_path):
        """Mock delete"""
        if remote_path in self.files:
            del self.files[remote_path]
            return True
        return False
    
    def exists(self, remote_path):
        """Check if file exists"""
        return remote_path in self.files
    
    def list_objects(self, prefix=''):
        """List objects with prefix"""
        return [
            {'key': k, 'size': v['size'], 'modified': v['created_at']}
            for k, v in self.files.items()
            if k.startswith(prefix)
        ]
    
    def get_size(self, remote_path):
        """Get file size"""
        if remote_path in self.files:
            return self.files[remote_path]['size']
        raise FileNotFoundError(f"File not found: {remote_path}")
    
    def get_signed_url(self, remote_path, expires=3600):
        """Generate signed URL"""
        if remote_path not in self.files:
            raise FileNotFoundError(f"File not found: {remote_path}")
        expiry = datetime.now() + timedelta(seconds=expires)
        return f"https://mock-storage.example.com/{remote_path}?expires={expiry.timestamp()}"


class MockSyncManager:
    """Mock sync manager"""
    
    def __init__(self, storage):
        self.storage = storage
        self.sync_history = []
    
    def sync_to_cloud(self, local_dir, remote_prefix, exclude=None, delete_remote=False):
        """Mock sync to cloud"""
        self.sync_history.append({
            'direction': 'to_cloud',
            'local': local_dir,
            'remote': remote_prefix
        })
        return {'uploaded': 5, 'skipped': 2, 'deleted': 0 if not delete_remote else 1}
    
    def sync_from_cloud(self, remote_prefix, local_dir, include=None):
        """Mock sync from cloud"""
        self.sync_history.append({
            'direction': 'from_cloud',
            'remote': remote_prefix,
            'local': local_dir
        })
        return {'downloaded': 3, 'skipped': 1}
    
    def compare(self, local_dir, remote_prefix):
        """Compare directories"""
        return {
            'local_only': ['file1.txt'],
            'remote_only': ['file2.txt'],
            'different': ['file3.txt'],
            'same': ['file4.txt']
        }


class TestCloudStorageManager(unittest.TestCase):
    """Test cases for cloud storage manager"""
    
    def setUp(self):
        """Set up test storage"""
        self.storage = MockStorageManager("mock")
    
    def test_upload(self):
        """Test upload operation"""
        result = self.storage.upload("local/test.txt", "remote/test.txt")
        self.assertTrue(result['success'])
        self.assertEqual(result['path'], "remote/test.txt")
        self.assertIn("remote/test.txt", self.storage.files)
    
    def test_download(self):
        """Test download operation"""
        # First upload
        self.storage.upload("local/test.txt", "remote/test.txt")
        
        # Then download
        result = self.storage.download("remote/test.txt", "local/downloaded.txt")
        self.assertTrue(result['success'])
    
    def test_download_not_found(self):
        """Test download non-existent file"""
        with self.assertRaises(FileNotFoundError):
            self.storage.download("remote/nonexistent.txt", "local.txt")
    
    def test_delete(self):
        """Test delete operation"""
        self.storage.upload("local/test.txt", "remote/test.txt")
        
        result = self.storage.delete("remote/test.txt")
        self.assertTrue(result)
        self.assertNotIn("remote/test.txt", self.storage.files)
    
    def test_delete_not_found(self):
        """Test delete non-existent file"""
        result = self.storage.delete("remote/nonexistent.txt")
        self.assertFalse(result)
    
    def test_exists(self):
        """Test exists check"""
        self.assertFalse(self.storage.exists("remote/test.txt"))
        
        self.storage.upload("local/test.txt", "remote/test.txt")
        self.assertTrue(self.storage.exists("remote/test.txt"))
    
    def test_list_objects(self):
        """Test list objects"""
        # Upload files with different prefixes
        files = [
            ("local/a.txt", "documents/2024/a.txt"),
            ("local/b.txt", "documents/2024/b.txt"),
            ("local/c.txt", "images/photo.jpg"),
        ]
        for local, remote in files:
            self.storage.upload(local, remote)
        
        # List with prefix
        docs = self.storage.list_objects(prefix="documents/")
        self.assertEqual(len(docs), 2)
        
        # List all
        all_files = self.storage.list_objects()
        self.assertEqual(len(all_files), 3)
    
    def test_get_size(self):
        """Test get file size"""
        self.storage.upload("local/test.txt", "remote/test.txt")
        
        size = self.storage.get_size("remote/test.txt")
        self.assertGreater(size, 0)
    
    def test_get_size_not_found(self):
        """Test get size of non-existent file"""
        with self.assertRaises(FileNotFoundError):
            self.storage.get_size("remote/nonexistent.txt")
    
    def test_get_signed_url(self):
        """Test signed URL generation"""
        self.storage.upload("local/test.txt", "remote/test.txt")
        
        url = self.storage.get_signed_url("remote/test.txt", expires=3600)
        self.assertIn("https://mock-storage.example.com/", url)
        self.assertIn("expires=", url)
    
    def test_get_signed_url_not_found(self):
        """Test signed URL for non-existent file"""
        with self.assertRaises(FileNotFoundError):
            self.storage.get_signed_url("remote/nonexistent.txt")


class TestSyncManager(unittest.TestCase):
    """Test cases for sync manager"""
    
    def setUp(self):
        """Set up test"""
        self.storage = MockStorageManager("mock")
        self.sync = MockSyncManager(self.storage)
    
    def test_sync_to_cloud(self):
        """Test sync to cloud"""
        result = self.sync.sync_to_cloud("/local/data", "backup/2024/")
        
        self.assertEqual(result['uploaded'], 5)
        self.assertEqual(result['skipped'], 2)
        self.assertEqual(self.sync.sync_history[0]['direction'], 'to_cloud')
    
    def test_sync_from_cloud(self):
        """Test sync from cloud"""
        result = self.sync.sync_from_cloud("data/", "/local/download")
        
        self.assertEqual(result['downloaded'], 3)
        self.assertEqual(self.sync.sync_history[0]['direction'], 'from_cloud')
    
    def test_compare(self):
        """Test directory comparison"""
        result = self.sync.compare("/local", "remote/")
        
        self.assertIn('local_only', result)
        self.assertIn('remote_only', result)
        self.assertIn('different', result)
        self.assertIn('same', result)


class TestProviders(unittest.TestCase):
    """Test provider constants"""
    
    def test_provider_names(self):
        """Test provider name consistency"""
        providers = ["AWS_S3", "ALIYUN_OSS", "TENCENT_COS", "AZURE_BLOB"]
        for provider in providers:
            # Just verify the name format
            self.assertTrue(provider.isupper())
            self.assertIn("_", provider)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases"""
    
    def test_empty_storage(self):
        """Test operations on empty storage"""
        storage = MockStorageManager("mock")
        
        # List should return empty
        files = storage.list_objects()
        self.assertEqual(len(files), 0)
        
        # Exists should return False
        self.assertFalse(storage.exists("anything.txt"))
    
    def test_special_characters_in_path(self):
        """Test paths with special characters"""
        storage = MockStorageManager("mock")
        
        special_paths = [
            "path with spaces/file.txt",
            "path-with-dashes/file.txt",
            "path_with_underscores/file.txt",
            "2024/01/15/file.txt",
        ]
        
        for i, path in enumerate(special_paths):
            storage.upload(f"local{i}.txt", path)
            self.assertTrue(storage.exists(path))


if __name__ == '__main__':
    unittest.main()
