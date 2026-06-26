"""
备份恢复工具包 - 单元测试
Backup Recovery Toolkit - Unit Tests
"""

import unittest
import sys
import os
import tempfile
import shutil

# 添加scripts目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from backup_toolkit import FileBackup, IncrementalBackup, RestoreManager, BackupResult


class TestFileBackup(unittest.TestCase):
    """文件备份测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.source_dir = tempfile.mkdtemp()
        self.dest_dir = tempfile.mkdtemp()
        
        # 创建测试文件
        for i in range(5):
            with open(os.path.join(self.source_dir, f"file{i}.txt"), 'w') as f:
                f.write(f"Test content {i}\n" * 100)
    
    def tearDown(self):
        """测试后清理"""
        if os.path.exists(self.source_dir):
            shutil.rmtree(self.source_dir)
        if os.path.exists(self.dest_dir):
            shutil.rmtree(self.dest_dir)
    
    def test_init(self):
        """测试初始化"""
        backup = FileBackup(self.source_dir, self.dest_dir)
        self.assertEqual(backup.source, os.path.abspath(self.source_dir))
        self.assertEqual(backup.destination, os.path.abspath(self.dest_dir))
        self.assertTrue(backup.compress)
    
    def test_run_compressed(self):
        """测试压缩备份"""
        backup = FileBackup(self.source_dir, self.dest_dir, compress=True)
        result = backup.run(name="test-compressed")
        
        self.assertTrue(result['success'])
        self.assertEqual(result['files_backed_up'], 5)
        self.assertTrue(os.path.exists(result['backup_path']))
        self.assertTrue(result['backup_path'].endswith('.tar.gz'))
    
    def test_run_uncompressed(self):
        """测试非压缩备份"""
        backup = FileBackup(self.source_dir, self.dest_dir, compress=False)
        result = backup.run(name="test-uncompressed")
        
        self.assertTrue(result['success'])
        self.assertEqual(result['files_backed_up'], 5)
        self.assertTrue(os.path.isdir(result['backup_path']))
    
    def test_run_default_name(self):
        """测试默认名称备份"""
        backup = FileBackup(self.source_dir, self.dest_dir)
        result = backup.run()
        
        self.assertTrue(result['success'])
        self.assertIn('backup_', result['backup_path'])


class TestIncrementalBackup(unittest.TestCase):
    """增量备份测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.source_dir = tempfile.mkdtemp()
        self.dest_dir = tempfile.mkdtemp()
        
        # 创建初始文件
        for i in range(3):
            with open(os.path.join(self.source_dir, f"file{i}.txt"), 'w') as f:
                f.write(f"Initial {i}\n")
    
    def tearDown(self):
        """测试后清理"""
        if os.path.exists(self.source_dir):
            shutil.rmtree(self.source_dir)
        if os.path.exists(self.dest_dir):
            shutil.rmtree(self.dest_dir)
    
    def test_init(self):
        """测试初始化"""
        backup = IncrementalBackup(self.source_dir, self.dest_dir)
        self.assertEqual(backup.source, os.path.abspath(self.source_dir))
        self.assertIsNone(backup.reference_backup)
    
    def test_incremental_backup(self):
        """测试增量备份流程"""
        # 先创建完整备份
        full_backup = FileBackup(self.source_dir, self.dest_dir)
        full_result = full_backup.run(name="full")
        
        # 添加新文件
        with open(os.path.join(self.source_dir, "new_file.txt"), 'w') as f:
            f.write("New content\n")
        
        # 执行增量备份
        incr_backup = IncrementalBackup(
            self.source_dir, 
            self.dest_dir, 
            full_result['backup_path']
        )
        incr_result = incr_backup.run(name="incremental")
        
        self.assertTrue(incr_result['success'])
        self.assertEqual(incr_result['files_backed_up'], 1)  # 只有新文件


class TestRestoreManager(unittest.TestCase):
    """恢复管理测试类"""
    
    def setUp(self):
        """测试前准备"""
        self.source_dir = tempfile.mkdtemp()
        self.dest_dir = tempfile.mkdtemp()
        self.restore_dir = tempfile.mkdtemp()
        
        # 创建测试文件
        for i in range(5):
            with open(os.path.join(self.source_dir, f"file{i}.txt"), 'w') as f:
                f.write(f"Content {i}\n")
    
    def tearDown(self):
        """测试后清理"""
        for d in [self.source_dir, self.dest_dir, self.restore_dir]:
            if os.path.exists(d):
                shutil.rmtree(d)
    
    def test_restore_compressed(self):
        """测试从压缩备份恢复"""
        # 创建压缩备份
        backup = FileBackup(self.source_dir, self.dest_dir, compress=True)
        result = backup.run(name="test")
        
        # 执行恢复
        restore_result = RestoreManager.restore_file_backup(
            result['backup_path'],
            self.restore_dir
        )
        
        self.assertTrue(restore_result['success'])
        self.assertGreater(restore_result['files_restored'], 0)
        
        # 验证文件存在
        restored_files = os.listdir(self.restore_dir)
        self.assertGreater(len(restored_files), 0)
    
    def test_restore_uncompressed(self):
        """测试从非压缩备份恢复"""
        # 创建非压缩备份
        backup = FileBackup(self.source_dir, self.dest_dir, compress=False)
        result = backup.run(name="test")
        
        # 执行恢复
        restore_result = RestoreManager.restore_file_backup(
            result['backup_path'],
            self.restore_dir
        )
        
        self.assertTrue(restore_result['success'])
        self.assertGreater(restore_result['files_restored'], 0)


class TestBackupResult(unittest.TestCase):
    """备份结果类测试"""
    
    def test_result_init(self):
        """测试结果初始化"""
        result = BackupResult()
        self.assertFalse(result.success)
        self.assertEqual(result.files_backed_up, 0)
        self.assertEqual(result.total_size, 0)
        self.assertEqual(result.errors, [])
    
    def test_result_to_dict(self):
        """测试结果转字典"""
        result = BackupResult()
        result.success = True
        result.files_backed_up = 10
        result.total_size = 1024
        result.backup_path = "/backup/test.tar.gz"
        
        data = result.to_dict()
        
        self.assertTrue(data['success'])
        self.assertEqual(data['files_backed_up'], 10)
        self.assertEqual(data['total_size'], 1024)
        self.assertEqual(data['backup_path'], "/backup/test.tar.gz")


class TestFileOperations(unittest.TestCase):
    """文件操作测试"""
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_create_and_read_file(self):
        """测试文件创建和读取"""
        test_file = os.path.join(self.test_dir, "test.txt")
        content = "Test content\n"
        
        with open(test_file, 'w') as f:
            f.write(content)
        
        with open(test_file, 'r') as f:
            read_content = f.read()
        
        self.assertEqual(read_content, content)
    
    def test_file_size(self):
        """测试文件大小"""
        test_file = os.path.join(self.test_dir, "test.txt")
        content = "x" * 1000
        
        with open(test_file, 'w') as f:
            f.write(content)
        
        size = os.path.getsize(test_file)
        self.assertEqual(size, 1000)


if __name__ == '__main__':
    unittest.main(verbosity=2)
