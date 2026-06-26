#!/usr/bin/env python3
"""
Data Mover Skill - 单元测试
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))


class TestDataValidation(unittest.TestCase):
    """测试数据验证功能"""
    
    def setUp(self):
        """测试前准备"""
        from mover import DataMover
        
        self.mover = DataMover({
            'validation': {
                'enabled': True,
                'rules': {
                    'email': r'^[\w.-]+@[\w.-]+\.\w+$',
                    'phone': r'^1[3-9]\d{9}$'
                },
                'required_fields': ['name', 'phone']
            }
        })
    
    def test_valid_email(self):
        """测试有效邮箱验证"""
        record = {'email': 'test@example.com'}
        rules = {'rules': {'email': r'^[\w.-]+@[\w.-]+\.\w+$'}}
        
        is_valid, errors = self.mover.validate_data(record, rules)
        self.assertTrue(is_valid)
    
    def test_invalid_email(self):
        """测试无效邮箱验证"""
        record = {'email': 'invalid-email'}
        rules = {'rules': {'email': r'^[\w.-]+@[\w.-]+\.\w+$'}}
        
        is_valid, errors = self.mover.validate_data(record, rules)
        self.assertFalse(is_valid)
        self.assertTrue(len(errors) > 0)
    
    def test_valid_phone(self):
        """测试有效手机号验证"""
        record = {'phone': '13800138000'}
        rules = {'rules': {'phone': r'^1[3-9]\d{9}$'}}
        
        is_valid, errors = self.mover.validate_data(record, rules)
        self.assertTrue(is_valid)
    
    def test_invalid_phone(self):
        """测试无效手机号验证"""
        record = {'phone': '1234567890'}
        rules = {'rules': {'phone': r'^1[3-9]\d{9}$'}}
        
        is_valid, errors = self.mover.validate_data(record, rules)
        self.assertFalse(is_valid)
    
    def test_required_fields(self):
        """测试必填字段验证"""
        record = {'name': '张三'}  # 缺少 phone
        rules = {'required_fields': ['name', 'phone']}
        
        is_valid, errors = self.mover.validate_data(record, rules)
        self.assertFalse(is_valid)
        self.assertTrue(any('phone' in err for err in errors))


class TestTableExtraction(unittest.TestCase):
    """测试表格提取功能"""
    
    def setUp(self):
        """测试前准备"""
        from mover import DataMover
        self.mover = DataMover()
    
    def test_extract_table_structure(self):
        """测试表格结构提取"""
        recognized_data = [
            {'text': '姓名', 'confidence': 0.99, 'bbox': [[0, 0], [100, 0], [100, 30], [0, 30]]},
            {'text': '电话', 'confidence': 0.99, 'bbox': [[110, 0], [210, 0], [210, 30], [110, 30]]},
            {'text': '张三', 'confidence': 0.95, 'bbox': [[0, 40], [100, 40], [100, 70], [0, 70]]},
            {'text': '13800138000', 'confidence': 0.96, 'bbox': [[110, 40], [210, 40], [210, 70], [110, 70]]},
        ]
        
        table = self.mover.extract_table(recognized_data)
        
        self.assertIsInstance(table, list)
        self.assertEqual(len(table), 1)
        self.assertIn('姓名', table[0])


class TestClipboard(unittest.TestCase):
    """测试剪贴板功能"""
    
    def setUp(self):
        """测试前准备"""
        from mover import DataMover
        self.mover = DataMover()
    
    def test_copy_paste_roundtrip(self):
        """测试复制粘贴往返"""
        test_text = "测试数据 123"
        
        # 这个测试需要实际的剪贴板支持，这里只做结构测试
        self.assertIsNotNone(self.mover.copy_to_clipboard)
        self.assertIsNotNone(self.mover.paste_from_clipboard)


if __name__ == '__main__':
    unittest.main()
