# -*- coding: utf-8 -*-
"""
单元测试: 多平台适配层 (Platform Adapters & URL Generation & Selectors)
"""

import os
import sys
import unittest
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from platforms import get_platform, supported_platform_names, PLATFORMS
from platforms.base import BasePlatform


class TestPlatforms(unittest.TestCase):
    def test_platform_registry_and_aliases(self):
        """测试各平台及其常见中英文别名的工厂解析"""
        cases = {
            "douyin": "douyin",
            "tiktok": "douyin",
            "bilibili": "bilibili",
            "b站": "bilibili",
            "xiaohongshu": "xiaohongshu",
            "red": "xiaohongshu",
            "小红书": "xiaohongshu",
            "x": "x",
            "twitter": "x",
            "推特": "x",
            "youtube": "youtube",
            "油管": "youtube",
        }
        for alias, expected_name in cases.items():
            adapter = get_platform(alias)
            self.assertIsNotNone(adapter, f"别名 '{alias}' 未能解析到有效适配器")
            self.assertEqual(adapter.name, expected_name)

        # 未知平台返回 None
        self.assertIsNone(get_platform("unknown_platform_123"))

    def test_supported_platform_names(self):
        """测试支持的平台清单列表"""
        names = supported_platform_names()
        self.assertTrue(len(names) >= 5)
        self.assertTrue(any("抖音" in n for n in names))
        self.assertTrue(any("小红书" in n for n in names))
        self.assertTrue(any("哔哩哔哩" in n for n in names))
        self.assertTrue(any("Twitter" in n for n in names))
        self.assertTrue(any("YouTube" in n for n in names))

    def test_search_url_generation(self):
        """测试各平台搜索 URL 构造及 URL 编码有效性"""
        test_blogger = "AI 研习社 & Geek"
        encoded_name = urllib.parse.quote(test_blogger)

        dy = get_platform("douyin")
        dy_url = dy.get_search_url(test_blogger)
        self.assertTrue(dy_url.startswith("https://www.douyin.com/search/"))
        self.assertIn(encoded_name, dy_url)
        self.assertIn("type=user", dy_url)

        xhs = get_platform("xiaohongshu")
        xhs_url = xhs.get_search_url(test_blogger)
        self.assertTrue(xhs_url.startswith("https://www.xiaohongshu.com/search_result"))
        self.assertIn(encoded_name, xhs_url)

        bili = get_platform("bilibili")
        bili_url = bili.get_search_url(test_blogger)
        self.assertTrue(bili_url.startswith("https://search.bilibili.com/upuser"))
        self.assertIn(encoded_name, bili_url)

        x_plat = get_platform("x")
        x_url = x_plat.get_search_url(test_blogger)
        self.assertTrue(x_url.startswith("https://x.com/search"))
        self.assertIn("f=user", x_url)

        yt = get_platform("youtube")
        yt_url = yt.get_search_url(test_blogger)
        self.assertTrue(yt_url.startswith("https://www.youtube.com/results"))
        self.assertIn(encoded_name, yt_url)

    def test_platform_interface_integrity(self):
        """测试所有适配器均完整实现了 BasePlatform 所需的接口与属性"""
        for key, adapter in PLATFORMS.items():
            self.assertIsInstance(adapter, BasePlatform)
            self.assertTrue(bool(adapter.name))
            self.assertTrue(bool(adapter.display_name))
            self.assertTrue(adapter.home_url.startswith("http"))
            self.assertTrue(callable(getattr(adapter, "get_search_url", None)))
            self.assertTrue(callable(getattr(adapter, "dismiss_popups", None)))
            self.assertTrue(callable(getattr(adapter, "check_captcha", None)))
            self.assertTrue(callable(getattr(adapter, "handle_follow", None)))

    def test_xiaohongshu_uses_result_card_profile_link_selector(self):
        """小红书只查询结果卡片，避免侧边栏“我”的资料链接触发渲染竞态。"""
        xhs = get_platform("xiaohongshu")
        self.assertEqual(
            xhs.profile_link_selector,
            'div.onebox a[href*="/user/profile/"]',
        )
        self.assertNotIn("user-item", xhs.profile_link_selector)
        self.assertEqual(xhs.result_wait_seconds, 17.5)
        self.assertEqual(xhs.result_poll_seconds, 0.5)

    def test_douyin_waits_for_scoped_spa_result_cards(self):
        """抖音精选重定向后，不能把侧边栏“我的”当作搜索结果。"""
        dy = get_platform("douyin")
        self.assertEqual(dy.result_wait_seconds, 22)
        self.assertEqual(dy.result_poll_seconds, 0.5)
        self.assertIn('div[data-e2e="search-user-item"]', dy.result_card_selectors)
        self.assertTrue(all(
            s == 'div[data-e2e="search-user-item"]' or "[data-e2e*=" in s or s.startswith("main ")
            for s in dy.result_card_selectors
        ))


if __name__ == "__main__":
    unittest.main()
