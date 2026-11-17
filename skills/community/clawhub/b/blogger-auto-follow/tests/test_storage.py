# -*- coding: utf-8 -*-
"""
单元测试: 本地博主资产库 (BloggerDB & Industry Inference)
"""

import os
import sys
import shutil
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from storage import BloggerDB, infer_industry, get_all_industries


class TestBloggerDB(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="test_blogger_db_")
        self.db = BloggerDB(data_dir=self.test_dir)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_initial_state(self):
        """测试初始状态为空，并在保存后生成数据文件"""
        self.assertEqual(len(self.db.get_all()), 0)
        self.db.save()
        self.assertTrue(os.path.exists(self.db.json_file))
        self.assertTrue(os.path.exists(self.db.md_file))

    def test_upsert_single_blogger(self):
        """测试单条博主增量录入与自动推断行业"""
        record = {
            "name": "极客湾Geekerwan",
            "category": "数码评测",
            "platform": "bilibili",
            "profile_url": "https://space.bilibili.com/25876945",
            "unique_id": "25876945",
            "fans": "350万",
            "bio": "科技数码硬件深度评测",
            "status": "SUCCESS"
        }
        saved = self.db.upsert_blogger(record)
        self.assertEqual(saved["name"], "极客湾Geekerwan")
        self.assertEqual(saved["primary_platform"], "bilibili")
        self.assertEqual(saved["industry"], "科技 · 数码 · 编程")
        self.assertEqual(len(self.db.get_all()), 1)

    def test_upsert_update_existing_blogger(self):
        """测试同名博主增量更新属性，不重复创建记录"""
        rec1 = {
            "name": "李开复",
            "category": "默认",
            "platform": "douyin",
            "bio": "零一万物CEO"
        }
        self.db.upsert_blogger(rec1)
        self.assertEqual(len(self.db.get_all()), 1)

        # 更新更丰富的信息
        rec2 = {
            "name": "李开复",
            "category": "AI认知",
            "platform": "douyin",
            "profile_url": "https://www.douyin.com/user/MS4wLjABAAAA...",
            "fans": "500万"
        }
        updated = self.db.upsert_blogger(rec2)
        self.assertEqual(len(self.db.get_all()), 1)
        self.assertEqual(updated["category"], "AI认知")
        self.assertEqual(updated["fans"], "500万")
        self.assertTrue(updated["profile_url"].startswith("https://www.douyin.com"))

    def test_delete_blogger_by_name_and_id(self):
        """测试按名称和 ID 删除博主"""
        self.db.upsert_blogger({"name": "博主A", "platform": "douyin"})
        self.db.upsert_blogger({"name": "博主B", "platform": "bilibili"})
        self.assertEqual(len(self.db.get_all()), 2)

        # 按名称删除
        deleted_a = self.db.delete_blogger("博主A")
        self.assertIsNotNone(deleted_a)
        self.assertEqual(deleted_a["name"], "博主A")
        self.assertEqual(len(self.db.get_all()), 1)

        # 按 ID 删除
        deleted_b = self.db.delete_blogger(1)
        self.assertIsNotNone(deleted_b)
        self.assertEqual(len(self.db.get_all()), 0)

        # 删除不存在的博主返回 None
        self.assertIsNone(self.db.delete_blogger("不存在的博主"))

    def test_industry_inference(self):
        """测试各领域关键字的智能行业分类推断"""
        self.assertEqual(infer_industry("Python编程教室", "", ""), "科技 · 数码 · 编程")
        self.assertEqual(infer_industry("商业小纸条", "创业思维", ""), "商业 · 财经 · 创业")
        self.assertEqual(infer_industry("设计师阿文", "UI视觉", ""), "设计 · 视觉 · 创意")
        self.assertEqual(infer_industry("木鱼水心", "影视解说", ""), "影视 · 摄影 · 剪辑")
        self.assertEqual(infer_industry("秋叶Excel", "PPT教程", ""), "职场 · 效率 · 成长")
        self.assertEqual(infer_industry("回形针PaperClip", "硬核科普", ""), "知识 · 人文 · 科普")
        self.assertEqual(infer_industry("李子柒", "美食生活", ""), "泛生活 · 娱乐 · 兴趣")

    def test_export_markdown_content(self):
        """测试生成的 Markdown 导航手册格式规范"""
        self.db.upsert_blogger({
            "name": "GitHub星选",
            "category": "开源项目",
            "platform": "douyin",
            "profile_url": "https://www.douyin.com/user/github_star",
            "fans": "20万",
            "bio": "每日推荐优质开源项目"
        })

        with open(self.db.md_file, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("全行业已关注博主资产库与主页直达导航", content)
        self.assertIn("GitHub星选", content)
        self.assertIn("https://www.douyin.com/user/github_star", content)
        self.assertIn("科技 · 数码 · 编程", content)


if __name__ == "__main__":
    unittest.main()
