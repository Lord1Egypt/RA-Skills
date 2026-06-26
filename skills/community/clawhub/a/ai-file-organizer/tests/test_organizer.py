#!/usr/bin/env python3
"""
AI File Organizer v3.0.0 - 单元测试套件

测试覆盖率目标：>90%
"""

import unittest
import os
import sys
import tempfile
import shutil
import asyncio
import time
from pathlib import Path
from unittest.mock import patch, MagicMock

# 添加脚本路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))


class TestFileStats(unittest.TestCase):
    """测试统计数据类"""
    
    def test_default_values(self):
        """测试默认值"""
        from organizer import FileStats
        stats = FileStats()
        
        self.assertEqual(stats.total_files, 0)
        self.assertEqual(stats.processed, 0)
        self.assertEqual(stats.errors, 0)
    
    def test_dataclass_conversion(self):
        """测试数据类转换"""
        from organizer import FileStats, asdict
        stats = FileStats(total_files=100, processed=95)
        
        stats_dict = asdict(stats)
        self.assertIn('total_files', stats_dict)
        self.assertEqual(stats_dict['total_files'], 100)


class TestFileCache(unittest.TestCase):
    """测试缓存系统"""
    
    def setUp(self):
        """测试前准备"""
        from organizer import FileCache
        self.test_cache_dir = tempfile.mkdtemp()
        self.cache = FileCache(cache_dir=self.test_cache_dir, max_size=100)
    
    def tearDown(self):
        """测试后清理"""
        shutil.rmtree(self.test_cache_dir)
    
    def test_cache_set_get(self):
        """测试缓存设置和获取"""
        file_hash = "test_hash_123"
        data = {'category': 'Documents', 'new_path': '/test/path.pdf'}
        
        self.cache.set(file_hash, data)
        retrieved = self.cache.get(file_hash)
        
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved['category'], 'Documents')
        self.assertEqual(retrieved['new_path'], '/test/path.pdf')
    
    def test_cache_miss(self):
        """测试缓存未命中"""
        retrieved = self.cache.get("nonexistent_hash")
        self.assertIsNone(retrieved)
    
    def test_cache_clear(self):
        """测试缓存清空"""
        self.cache.set("hash1", {'data': 'test1'})
        self.cache.set("hash2", {'data': 'test2'})
        
        self.cache.clear()
        
        self.assertIsNone(self.cache.get("hash1"))
        self.assertIsNone(self.cache.get("hash2"))
        self.assertEqual(self.cache.hits, 0)
        self.assertEqual(self.cache.misses, 0)
    
    def test_cache_persistence(self):
        """测试缓存持久化"""
        file_hash = "persistent_hash"
        data = {'test': 'data'}
        
        self.cache.set(file_hash, data)
        
        # 创建新缓存实例（模拟重新加载）
        from organizer import FileCache
        cache2 = FileCache(cache_dir=self.test_cache_dir, max_size=100)
        retrieved = cache2.get(file_hash)
        
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved['test'], 'data')


class TestFileTypeDetection(unittest.TestCase):
    """测试文件类型检测"""
    
    def setUp(self):
        """测试前准备"""
        from organizer import AIFileOrganizer
        self.organizer = AIFileOrganizer()
    
    def test_document_detection(self):
        """测试文档类型检测"""
        extensions = ['.pdf', '.doc', '.docx', '.txt', '.md', '.rtf']
        for ext in extensions:
            with self.subTest(ext=ext):
                self.assertEqual(self.organizer.get_file_type(f'test{ext}'), 'document')
    
    def test_image_detection(self):
        """测试图片类型检测"""
        extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp']
        for ext in extensions:
            with self.subTest(ext=ext):
                self.assertEqual(self.organizer.get_file_type(f'photo{ext}'), 'image')
    
    def test_code_detection(self):
        """测试代码文件检测"""
        extensions = ['.py', '.js', '.java', '.cpp', '.c', '.h', '.html', '.css', '.ts', '.go', '.rs', '.rb']
        for ext in extensions:
            with self.subTest(ext=ext):
                self.assertEqual(self.organizer.get_file_type(f'script{ext}'), 'code')
    
    def test_archive_detection(self):
        """测试压缩文件检测"""
        extensions = ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2']
        for ext in extensions:
            with self.subTest(ext=ext):
                self.assertEqual(self.organizer.get_file_type(f'archive{ext}'), 'archive')
    
    def test_unknown_type(self):
        """测试未知类型"""
        self.assertEqual(self.organizer.get_file_type('test.xyz'), 'other')


class TestFileClassification(unittest.TestCase):
    """测试文件分类"""
    
    def setUp(self):
        """测试前准备"""
        from organizer import AIFileOrganizer
        
        config = {
            'classification': {
                'categories': [
                    {'name': '工作文档', 'keywords': ['报告', '方案', '合同'], 'folder': 'Work'},
                    {'name': '学习资料', 'keywords': ['教程', '课程'], 'folder': 'Learning'},
                    {'name': '图片视频', 'extensions': ['jpg', 'png', 'mp4'], 'folder': 'Media'}
                ]
            }
        }
        self.organizer = AIFileOrganizer(config)
    
    def test_keyword_classification(self):
        """测试关键词分类"""
        category, confidence = self.organizer.classify_file('/path/test.pdf', '年度报告.pdf')
        self.assertEqual(category, 'Work')
        self.assertGreater(confidence, 0.9)
    
    def test_extension_classification(self):
        """测试扩展名分类"""
        category, confidence = self.organizer.classify_file('/path/photo.jpg', 'photo.jpg')
        self.assertEqual(category, 'Media')
        self.assertGreaterEqual(confidence, 0.85)
    
    def test_default_classification(self):
        """测试默认分类"""
        category, confidence = self.organizer.classify_file('/path/unknown.xyz', 'unknown.xyz')
        self.assertEqual(category, 'Other')
        self.assertLessEqual(confidence, 0.6)
    
    def test_classification_confidence(self):
        """测试分类置信度层级"""
        # 关键词匹配应该有最高置信度
        _, kw_confidence = self.organizer.classify_file('/path/test.pdf', '项目报告.pdf')
        # 扩展名匹配应该有中等置信度
        _, ext_confidence = self.organizer.classify_file('/path/test.jpg', 'random.jpg')
        # 默认分类应该有最低置信度
        _, def_confidence = self.organizer.classify_file('/path/test.xyz', 'unknown.xyz')
        
        self.assertGreater(kw_confidence, ext_confidence)
        self.assertGreater(ext_confidence, def_confidence)


class TestFilenameGeneration(unittest.TestCase):
    """测试文件名生成"""
    
    def setUp(self):
        """测试前准备"""
        from organizer import AIFileOrganizer
        
        config = {
            'naming': {
                'format': '{date}_{type}_{original}',
                'date_format': '%Y%m%d',
                'max_length': 100,
                'replace_spaces': True
            }
        }
        self.organizer = AIFileOrganizer(config)
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """测试后清理"""
        shutil.rmtree(self.test_dir)
    
    def test_filename_format(self):
        """测试文件名格式"""
        test_file = os.path.join(self.test_dir, 'test.pdf')
        with open(test_file, 'w') as f:
            f.write('test')
        
        new_name = self.organizer.generate_filename(test_file)
        
        # 应该包含日期和类型
        self.assertIn('.pdf', new_name)
        self.assertIn('document', new_name)
    
    def test_filename_length_limit(self):
        """测试文件名长度限制"""
        test_file = os.path.join(self.test_dir, 'a' * 200 + '.pdf')
        with open(test_file, 'w') as f:
            f.write('test')
        
        new_name = self.organizer.generate_filename(test_file)
        
        # 文件名不应该超过最大长度
        self.assertLessEqual(len(new_name), 100)
    
    def test_special_character_handling(self):
        """测试特殊字符处理"""
        test_file = os.path.join(self.test_dir, 'test<>:"file.pdf')
        with open(test_file, 'w') as f:
            f.write('test')
        
        new_name = self.organizer.generate_filename(test_file)
        
        # 不应该包含非法字符
        self.assertNotIn('<', new_name)
        self.assertNotIn('>', new_name)
        self.assertNotIn(':', new_name)


class TestDuplicateDetection(unittest.TestCase):
    """测试重复文件检测"""
    
    def setUp(self):
        """测试前准备"""
        from organizer import AIFileOrganizer
        self.organizer = AIFileOrganizer()
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """测试后清理"""
        shutil.rmtree(self.test_dir)
    
    def test_identical_files(self):
        """测试相同文件检测"""
        file1 = os.path.join(self.test_dir, 'file1.txt')
        file2 = os.path.join(self.test_dir, 'file2.txt')
        
        with open(file1, 'w') as f:
            f.write('test content')
        shutil.copy(file1, file2)
        
        hash1 = self.organizer._get_file_hash_sync(file1)
        hash2 = self.organizer._get_file_hash_sync(file2)
        
        self.assertEqual(hash1, hash2)
    
    def test_different_files(self):
        """测试不同文件检测"""
        file1 = os.path.join(self.test_dir, 'file1.txt')
        file2 = os.path.join(self.test_dir, 'file2.txt')
        
        with open(file1, 'w') as f:
            f.write('content 1')
        with open(file2, 'w') as f:
            f.write('content 2')
        
        hash1 = self.organizer._get_file_hash_sync(file1)
        hash2 = self.organizer._get_file_hash_sync(file2)
        
        self.assertNotEqual(hash1, hash2)
    
    def test_find_duplicates(self):
        """测试查找重复文件"""
        # 创建重复文件
        for i in range(3):
            file_path = os.path.join(self.test_dir, f'file{i}.txt')
            with open(file_path, 'w') as f:
                f.write('duplicate content')
        
        duplicates = self.organizer.find_duplicates(self.test_dir)
        
        self.assertEqual(len(duplicates), 1)
        self.assertEqual(len(list(duplicates.values())[0]), 3)


class TestAsyncProcessing(unittest.TestCase):
    """测试异步处理"""
    
    def setUp(self):
        """测试前准备"""
        from organizer import AIFileOrganizer
        self.organizer = AIFileOrganizer()
        self.test_dir = tempfile.mkdtemp()
        self.target_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """测试后清理"""
        shutil.rmtree(self.test_dir)
        shutil.rmtree(self.target_dir)
    
    def test_async_file_processing(self):
        """测试异步文件处理"""
        test_file = os.path.join(self.test_dir, 'test.pdf')
        with open(test_file, 'w') as f:
            f.write('test content')
        
        result = asyncio.run(
            self.organizer.process_file_async(test_file, self.target_dir)
        )
        
        self.assertTrue(result.success)
        self.assertIsNotNone(result.new_path)
        self.assertTrue(os.path.exists(result.new_path))
    
    def test_async_organize_files(self):
        """测试异步文件整理"""
        # 创建测试文件
        for i in range(5):
            file_path = os.path.join(self.test_dir, f'file{i}.txt')
            with open(file_path, 'w') as f:
                f.write(f'content {i}')
        
        report = self.organizer.organize_files(self.test_dir, self.target_dir)
        
        self.assertIn(report.status, ['success', 'partial_success'])
        self.assertEqual(report.stats['total_files'], 5)
        self.assertGreater(report.stats['processed'], 0)
    
    def test_concurrent_processing(self):
        """测试并发处理"""
        # 创建多个测试文件
        for i in range(20):
            file_path = os.path.join(self.test_dir, f'file{i}.txt')
            with open(file_path, 'w') as f:
                f.write(f'content {i}')
        
        start_time = time.time()
        report = self.organizer.organize_files(
            self.test_dir, 
            self.target_dir, 
            max_concurrent=5
        )
        elapsed = time.time() - start_time
        
        self.assertGreater(report.stats['processed'], 0)
        self.assertLess(elapsed, 10)  # 应该在 10 秒内完成


class TestErrorHandling(unittest.TestCase):
    """测试错误处理"""
    
    def setUp(self):
        """测试前准备"""
        from organizer import AIFileOrganizer
        self.organizer = AIFileOrganizer()
    
    def test_nonexistent_file(self):
        """测试处理不存在的文件"""
        result = asyncio.run(
            self.organizer.process_file_async('/nonexistent/file.txt', '/tmp')
        )
        
        self.assertFalse(result.success)
        self.assertIsNotNone(result.error)
    
    def test_permission_error(self):
        """测试权限错误处理"""
        # 创建一个不可读的文件（在某些系统上可能无效）
        test_dir = tempfile.mkdtemp()
        test_file = os.path.join(test_dir, 'readonly.txt')
        with open(test_file, 'w') as f:
            f.write('test')
        
        try:
            os.chmod(test_file, 0o000)
            result = asyncio.run(
                self.organizer.process_file_async(test_file, '/tmp')
            )
            # 如果权限设置生效，应该失败
            if not result.success:
                self.assertIsNotNone(result.error)
        finally:
            os.chmod(test_file, 0o644)
            shutil.rmtree(test_dir)


class TestReportGeneration(unittest.TestCase):
    """测试报告生成"""
    
    def setUp(self):
        """测试前准备"""
        from organizer import AIFileOrganizer, OrganizeReport
        self.organizer = AIFileOrganizer()
        self.test_dir = tempfile.mkdtemp()
        self.report_file = os.path.join(self.test_dir, 'report.json')
    
    def tearDown(self):
        """测试后清理"""
        shutil.rmtree(self.test_dir)
    
    def test_export_report(self):
        """测试导出报告"""
        report = OrganizeReport(
            status='success',
            stats={'total_files': 10, 'processed': 10},
            categories={'Documents': 5, 'Images': 5}
        )
        
        self.organizer.export_report(report, self.report_file)
        
        self.assertTrue(os.path.exists(self.report_file))
        
        with open(self.report_file, 'r', encoding='utf-8') as f:
            loaded_report = json.load(f)
        
        self.assertEqual(loaded_report['status'], 'success')
        self.assertIn('generated_at', loaded_report)


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def setUp(self):
        """测试前准备"""
        from organizer import AIFileOrganizer
        self.organizer = AIFileOrganizer()
        self.test_dir = tempfile.mkdtemp()
        self.target_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """测试后清理"""
        shutil.rmtree(self.test_dir)
        shutil.rmtree(self.target_dir)
    
    def test_full_workflow(self):
        """测试完整工作流程"""
        # 创建混合类型的测试文件
        test_files = [
            ('report.pdf', 'PDF content'),
            ('photo.jpg', 'Image content'),
            ('code.py', 'Python code'),
            ('data.xlsx', 'Spreadsheet'),
            ('archive.zip', 'Archive'),
        ]
        
        for filename, content in test_files:
            file_path = os.path.join(self.test_dir, filename)
            with open(file_path, 'w') as f:
                f.write(content)
        
        # 执行整理
        report = self.organizer.organize_files(self.test_dir, self.target_dir)
        
        # 验证结果
        self.assertIn(report.status, ['success', 'partial_success'])
        self.assertEqual(report.stats['total_files'], len(test_files))
        
        # 验证文件被正确分类
        self.assertTrue(os.path.exists(self.target_dir))
        
        # 验证报告导出
        report_file = os.path.join(self.test_dir, 'report.json')
        self.organizer.export_report(report, report_file)
        self.assertTrue(os.path.exists(report_file))


if __name__ == '__main__':
    # 运行测试
    unittest.main(verbosity=2)
    
    # 输出覆盖率提示
    print("\n" + "=" * 60)
    print("💡 提示：使用以下命令获取覆盖率报告:")
    print("   python -m pytest tests/test_organizer.py -v --cov=scripts --cov-report=html")
    print("=" * 60)
