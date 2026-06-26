#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
360 搜索客户端
360 Search Client

使用 360 搜索引擎进行网页搜索
"""

import os
import time
import json
from typing import Optional, Dict, Any, List
from playwright.sync_api import sync_playwright, Page, Browser


class Search360Client:
    """360 搜索客户端"""

    def __init__(
        self,
        headless: bool = True,
        timeout: int = 30000,
    ):
        """
        初始化 360 搜索客户端

        Args:
            headless: 是否无头模式
            timeout: 超时时间（毫秒）
        """
        self.headless = headless
        self.timeout = timeout
        self.base_url = "https://www.so.com"

        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None

    def start(self):
        """启动浏览器"""
        playwright = sync_playwright().start()
        self.browser = playwright.chromium.launch(headless=self.headless)
        context = self.browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        )
        self.page = context.new_page()
        return self

    def stop(self):
        """关闭浏览器"""
        if self.browser:
            self.browser.close()
            self.browser = None
            self.page = None

    def search(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        执行搜索

        Args:
            query: 搜索关键词
            max_results: 最大结果数

        Returns:
            搜索结果列表
        """
        if not self.page:
            self.start()

        results = []
        try:
            url = f"{self.base_url}/s?q={query}"
            self.page.goto(url, timeout=self.timeout)
            time.sleep(2)

            result_elements = self.page.query_selector_all(".res-list")[:max_results]

            for elem in result_elements:
                try:
                    title_elem = elem.query_selector(".res-title")
                    link_elem = elem.query_selector(".res-url")
                    desc_elem = elem.query_selector(".res-desc")

                    title = title_elem.inner_text() if title_elem else ""
                    link = link_elem.get_attribute("href") if link_elem else ""
                    desc = desc_elem.inner_text() if desc_elem else ""

                    results.append(
                        {
                            "title": title,
                            "link": link,
                            "snippet": desc,
                            "source": "360 搜索",
                        }
                    )
                except Exception:
                    continue

        except Exception as e:
            print(f"搜索失败：{e}")

        return results

    def search_news(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        搜索新闻

        Args:
            query: 搜索关键词
            max_results: 最大结果数

        Returns:
            新闻结果列表
        """
        if not self.page:
            self.start()

        results = []
        try:
            url = f"{self.base_url}/s?q={query}&tn=news"
            self.page.goto(url, timeout=self.timeout)
            time.sleep(2)

            result_elements = self.page.query_selector_all(".res-list")[:max_results]

            for elem in result_elements:
                try:
                    title_elem = elem.query_selector(".res-title")
                    link_elem = elem.query_selector(".res-url")
                    source_elem = elem.query_selector(".res-source")
                    time_elem = elem.query_selector(".res-time")

                    results.append(
                        {
                            "title": title_elem.inner_text() if title_elem else "",
                            "link": link_elem.get_attribute("href")
                            if link_elem
                            else "",
                            "source": source_elem.inner_text() if source_elem else "",
                            "time": time_elem.inner_text() if time_elem else "",
                            "type": "news",
                        }
                    )
                except Exception:
                    continue

        except Exception as e:
            print(f"新闻搜索失败：{e}")

        return results

    def search_image(self, query: str, max_results: int = 20) -> List[Dict[str, Any]]:
        """
        搜索图片

        Args:
            query: 搜索关键词
            max_results: 最大结果数

        Returns:
            图片结果列表
        """
        if not self.page:
            self.start()

        results = []
        try:
            url = f"{self.base_url}/s?q={query}&tn=pic"
            self.page.goto(url, timeout=self.timeout)
            time.sleep(3)

            img_elements = self.page.query_selector_all(".pic-list img")[:max_results]

            for img in img_elements:
                try:
                    src = img.get_attribute("src")
                    alt = img.get_attribute("alt")
                    if src:
                        results.append(
                            {"image_url": src, "alt": alt or "", "source": "360 图片"}
                        )
                except Exception:
                    continue

        except Exception as e:
            print(f"图片搜索失败：{e}")

        return results


def main():
    """主函数 - 测试用"""
    client = Search360Client(headless=False)
    try:
        client.start()
        results = client.search("Python 编程", max_results=5)
        print(f"找到 {len(results)} 条结果")
        for r in results:
            print(f"- {r['title']}")
    finally:
        client.stop()


if __name__ == "__main__":
    main()
