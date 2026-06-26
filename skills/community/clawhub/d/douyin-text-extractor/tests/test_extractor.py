#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
抖音文案提取工具 - 单元测试
"""

import os
import sys
import unittest
from pathlib import Path

# 添加 src 目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from douyin_extractor import DouyinExtractor


class TestDouyinExtractor(unittest.TestCase):
    """抖音文案提取器测试"""
    
    def setUp(self):
        """测试前准备"""
        self.extractor = DouyinExtractor()
        self.test_video_url = "https://v.douyin.com/example/"  # 测试用链接
    
    def test_init(self):
        """测试初始化"""
        # 无 API Key 初始化
        extractor = DouyinExtractor()
        self.assertEqual(extractor.api_key, "")
        
        # 有 API Key 初始化
        extractor = DouyinExtractor(api_key="sk-test")
        self.assertEqual(extractor.api_key, "sk-test")
    
    def test_invite_code(self):
        """测试邀请码配置"""
        self.assertEqual(self.extractor.INVITE_CODE, "84kySW0S")
        self.assertIn("84kySW0S", self.extractor.REGISTER_URL)
    
    def test_api_key_from_env(self):
        """测试从环境变量获取 API Key"""
        os.environ["API_KEY"] = "sk-env-test"
        extractor = DouyinExtractor()
        self.assertEqual(extractor.api_key, "sk-env-test")
        del os.environ["API_KEY"]
    
    def test_siliconflow_config(self):
        """测试硅基流动 API 配置"""
        self.assertEqual(
            self.extractor.SILICONFLOW_MODEL,
            "FunAudioLLM/SenseVoiceSmall"
        )
        self.assertIn("siliconflow.cn", self.extractor.SILICONFLOW_API_URL)


class TestHelperFunctions(unittest.TestCase):
    """辅助函数测试"""
    
    def test_print_help(self):
        """测试帮助信息输出"""
        from douyin_extractor import print_help
        # 应该不抛出异常
        try:
            print_help()
        except Exception as e:
            self.fail(f"print_help() raised {e}")


if __name__ == "__main__":
    unittest.main()
