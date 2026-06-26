"""
网页爬虫抓取器
使用Playwright或BeautifulSoup抓取网页内容
"""
import asyncio
import logging
import time
from typing import List, Dict, Any
from datetime import datetime
import re

from .base_fetcher import BaseFetcher, NewsItem


class WebScraper(BaseFetcher):
    """网页爬虫抓取器"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.url = config.get("url", "")
        self.selector = config.get("selector", "")
        self.use_playwright = config.get("use_playwright", False)
        self.playwright_wait_seconds = config.get("playwright_wait_seconds", 2)
        self.logger = logging.getLogger(f"WebScraper.{self.name}")

    async def fetch(self) -> List[NewsItem]:
        """
        抓取网页内容

        Returns:
            新闻条目列表
        """
        if not self.enabled:
            self.logger.info(f"数据源已禁用: {self.name}")
            return []

        if not self.url:
            self.logger.error(f"URL为空: {self.name}")
            return []

        self.logger.info(f"开始抓取网页: {self.name} ({self.url})")
        start_time = time.time()

        try:
            if self.use_playwright:
                items = await self._fetch_with_playwright()
            else:
                items = await self._fetch_with_requests()

            # 应用过滤
            filtered_items = self.apply_filters(items)

            elapsed = time.time() - start_time
            self.logger.info(f"网页抓取完成: {self.name}, 获取 {len(filtered_items)} 个条目, 耗时 {elapsed:.2f}秒")
            return filtered_items

        except Exception as e:
            elapsed = time.time() - start_time
            self.logger.error(f"抓取网页失败 {self.name}, 耗时 {elapsed:.2f}秒: {e}")
            return []

    async def _fetch_with_requests(self) -> List[NewsItem]:
        """
        使用Requests和BeautifulSoup抓取网页

        Returns:
            新闻条目列表
        """
        try:
            import requests
            from bs4 import BeautifulSoup
        except ImportError:
            self.logger.error("需要安装requests和beautifulsoup4: pip install requests beautifulsoup4")
            return []

        try:
            # 获取fetch配置
            from .config import get_config_loader
            config_loader = get_config_loader()
            fetch_config = config_loader.get_fetch_config()

            headers = {
                "User-Agent": fetch_config.get("user_agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"),
            }

            # 发送请求
            response = requests.get(
                self.url,
                headers=headers,
                timeout=fetch_config.get("timeout_seconds", 30)
            )
            response.raise_for_status()

            # 解析HTML
            soup = BeautifulSoup(response.content, 'html.parser')

            # 根据选择器提取元素
            if self.selector:
                elements = soup.select(self.selector)
            else:
                # 如果没有选择器，尝试提取文章元素
                elements = soup.find_all(['article', 'div[class*="article"]', 'div[class*="post"]'])

            items = []
            for element in elements[:self.max_items]:
                try:
                    item = self._parse_html_element(element)
                    if item and self.validate_item(item):
                        items.append(item)
                except Exception as e:
                    self.logger.debug(f"解析HTML元素失败: {e}")

            return items

        except requests.RequestException as e:
            self.logger.error(f"请求失败: {e}")
            return []
        except Exception as e:
            self.logger.error(f"解析HTML失败: {e}")
            return []

    async def _fetch_with_playwright(self) -> List[NewsItem]:
        """
        使用Playwright抓取动态网页

        Returns:
            新闻条目列表
        """
        try:
            from playwright.async_api import async_playwright
        except ImportError:
            self.logger.error("需要安装Playwright: pip install playwright && playwright install")
            return []

        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                )
                page = await context.new_page()

                # 访问页面
                await page.goto(self.url, wait_until="networkidle")
                await page.wait_for_timeout(self.playwright_wait_seconds * 1000)

                # 根据选择器提取元素
                if self.selector:
                    elements = await page.query_selector_all(self.selector)
                else:
                    # 尝试常见文章选择器
                    selectors = ['article', 'div[class*="article"]', 'div[class*="post"]', 'div[class*="content"]']
                    elements = []
                    for selector in selectors:
                        found = await page.query_selector_all(selector)
                        if found:
                            elements.extend(found)
                            break

                items = []
                for element in elements[:self.max_items]:
                    try:
                        item = await self._parse_playwright_element(element)
                        if item and self.validate_item(item):
                            items.append(item)
                    except Exception as e:
                        self.logger.debug(f"解析Playwright元素失败: {e}")

                await browser.close()
                return items

        except Exception as e:
            self.logger.error(f"Playwright抓取失败: {e}")
            return []

    def _parse_html_element(self, element) -> NewsItem:
        """
        解析BeautifulSoup元素

        Args:
            element: BeautifulSoup元素

        Returns:
            新闻条目
        """
        # 提取标题
        title_elem = element.find(['h1', 'h2', 'h3', 'h4', 'h5'])
        title = title_elem.get_text(strip=True) if title_elem else "无标题"
        title = self.cleanup_content(title)

        # 提取链接
        link_elem = element.find('a', href=True)
        url = ""
        if link_elem:
            href = link_elem['href']
            if href.startswith('http'):
                url = href
            elif href.startswith('/'):
                # 转换为绝对URL
                from urllib.parse import urljoin
                url = urljoin(self.url, href)

        # 提取内容
        content_elem = element.find(['p', 'div[class*="content"]', 'div[class*="summary"]'])
        content = content_elem.get_text(strip=True) if content_elem else ""

        # 提取发布时间
        publish_date = None
        time_elem = element.find(['time', 'span[class*="date"]', 'div[class*="date"]'])
        if time_elem:
            time_text = time_elem.get_text(strip=True)
            # 尝试解析日期文本（简化处理）
            # 实际实现应使用dateparser库
            pass

        # 清理内容
        content = self.cleanup_content(content)

        item = NewsItem(
            title=title,
            url=url or self.url,  # 如果没有具体文章链接，使用页面URL
            content=content,
            summary=self.cleanup_content(content[:200]),
            source=self.name,
            source_type="web",
            publish_date=publish_date,
            metadata={
                "url": self.url,
                "selector": self.selector,
                "use_playwright": self.use_playwright,
            }
        )

        return item

    async def _parse_playwright_element(self, element) -> NewsItem:
        """
        解析Playwright元素

        Args:
            element: Playwright元素句柄

        Returns:
            新闻条目
        """
        # 提取标题
        title_elem = await element.query_selector('h1, h2, h3, h4, h5')
        title = await title_elem.inner_text() if title_elem else "无标题"
        title = title.strip()
        title = self.cleanup_content(title)

        # 提取链接
        link_elem = await element.query_selector('a[href]')
        url = ""
        if link_elem:
            href = await link_elem.get_attribute('href')
            if href:
                if href.startswith('http'):
                    url = href
                elif href.startswith('/'):
                    # 转换为绝对URL
                    from urllib.parse import urljoin
                    url = urljoin(self.url, href)

        # 提取内容
        content_elem = await element.query_selector('p, div[class*="content"], div[class*="summary"]')
        content = await content_elem.inner_text() if content_elem else ""
        content = content.strip()

        # 提取发布时间
        publish_date = None
        time_elem = await element.query_selector('time, span[class*="date"], div[class*="date"]')
        if time_elem:
            time_text = await time_elem.inner_text()
            time_text = time_text.strip()
            # 尝试解析日期
            datetime_attr = await time_elem.get_attribute('datetime')
            if datetime_attr:
                try:
                    publish_date = datetime.fromisoformat(datetime_attr.replace('Z', '+00:00'))
                except ValueError:
                    pass

        # 清理内容
        content = self.cleanup_content(content)

        item = NewsItem(
            title=title,
            url=url or self.url,
            content=content,
            summary=self.cleanup_content(content[:200]),
            source=self.name,
            source_type="web",
            publish_date=publish_date,
            metadata={
                "url": self.url,
                "selector": self.selector,
                "use_playwright": self.use_playwright,
            }
        )

        return item