#!/usr/bin/env python3
"""
测试分类链接采集功能
"""

import unittest
import tempfile
import os
from pathlib import Path
import pandas as pd

# 添加父目录到路径
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.collect_categories import (
    extract_domain,
    extract_category_path,
    parse_category_info,
    collect_category_links
)


class TestCategoryCollector(unittest.TestCase):
    
    def test_extract_domain(self):
        """测试域名提取"""
        url = "https://lulumonclick-eu.shop/collections/women-women-clothes-tank-tops"
        self.assertEqual(extract_domain(url), "lulumonclick-eu.shop")
        
        url2 = "http://example.com/path/to/page"
        self.assertEqual(extract_domain(url2), "example.com")
    
    def test_extract_category_path(self):
        """测试分类路径提取"""
        url = "https://lulumonclick-eu.shop/collections/women-women-clothes-tank-tops"
        self.assertEqual(extract_category_path(url), "women-women-clothes-tank-tops")
        
        url2 = "https://example.com/collections/men-clothes"
        self.assertEqual(extract_category_path(url2), "men-clothes")
        
        # 测试没有分类路径的情况
        url3 = "https://example.com/"
        self.assertEqual(extract_category_path(url3), "")
    
    def test_parse_category_info(self):
        """测试分类信息解析"""
        # 测试标准格式
        path = "women-women-clothes-tank-tops"
        first, second = parse_category_info(path)
        self.assertEqual(first, "Women")
        self.assertEqual(second, "Tank Tops")
        
        # 测试多单词二级分类
        path2 = "women-women-clothes-bras-underwear"
        first2, second2 = parse_category_info(path2)
        self.assertEqual(first2, "Women")
        self.assertEqual(second2, "Bras Underwear")
        
        # 测试单级分类
        path3 = "accessories"
        first3, second3 = parse_category_info(path3)
        self.assertEqual(first3, "Accessories")
        self.assertEqual(second3, "")
        
        # 测试空路径
        first4, second4 = parse_category_info("")
        self.assertEqual(first4, "")
        self.assertEqual(second4, "")
    
    def test_collect_category_links(self):
        """测试完整的链接采集流程"""
        # 创建临时目录
        with tempfile.TemporaryDirectory() as tmpdir:
            # 测试数据
            test_links = [
                "https://lulumonclick-eu.shop/collections/women-women-clothes-tank-tops",
                "https://lulumonclick-eu.shop/collections/women-women-clothes-bras-underwear"
            ]
            
            # 采集数据
            csv_path = collect_category_links(test_links, output_dir=tmpdir)
            
            # 验证文件存在
            self.assertTrue(os.path.exists(csv_path))
            
            # 验证文件内容
            df = pd.read_csv(csv_path)
            
            # 验证行数
            self.assertEqual(len(df), 2)
            
            # 验证列名
            expected_columns = ["完整链接", "分类路径", "一级分类", "二级分类", "域名"]
            self.assertListEqual(list(df.columns), expected_columns)
            
            # 验证数据
            first_row = df.iloc[0]
            self.assertEqual(first_row["完整链接"], test_links[0])
            self.assertEqual(first_row["分类路径"], "women-women-clothes-tank-tops")
            self.assertEqual(first_row["一级分类"], "Women")
            self.assertEqual(first_row["二级分类"], "Tank Tops")
            self.assertEqual(first_row["域名"], "lulumonclick-eu.shop")
    
    def test_output_filename(self):
        """测试输出文件名生成"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # 单域名测试
            links1 = ["https://example.com/collections/test"]
            csv_path1 = collect_category_links(links1, output_dir=tmpdir)
            self.assertIn("example_com.csv", csv_path1)
            
            # 多域名测试（应该使用第一个链接的域名）
            links2 = [
                "https://site1.com/collections/cat1",
                "https://site2.com/collections/cat2"
            ]
            csv_path2 = collect_category_links(links2, output_dir=tmpdir)
            self.assertIn("site1_com.csv", csv_path2)
    
    def test_directory_creation(self):
        """测试目录自动创建"""
        # 测试不存在的目录
        test_dir = "/tmp/test_category_collector/nested/dir"
        
        # 确保目录不存在
        if os.path.exists(test_dir):
            import shutil
            shutil.rmtree("/tmp/test_category_collector")
        
        test_links = ["https://example.com/collections/test"]
        
        # 应该自动创建目录
        csv_path = collect_category_links(test_links, output_dir=test_dir)
        
        # 验证目录已创建
        self.assertTrue(os.path.exists(test_dir))
        
        # 清理
        import shutil
        shutil.rmtree("/tmp/test_category_collector")


if __name__ == "__main__":
    unittest.main()