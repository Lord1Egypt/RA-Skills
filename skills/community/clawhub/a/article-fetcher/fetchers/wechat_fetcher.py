"""
微信公众号文章抓取器 — v1.3.0
HTTP (Cookies) → Playwright 浏览器 → 失败放弃
"""
from bs4 import BeautifulSoup
from fetchers.base_fetcher import BaseFetcher
from utils.logger import logger
import re
import requests
from datetime import datetime


class WechatFetcher(BaseFetcher):
    """微信公众号文章抓取器（二级回退）"""

    def fetch_article(self, url: str) -> dict:
        """抓取文章：HTTP → Playwright → 失败"""
        logger.info(f"开始抓取微信公众号文章：{url}")
        self._apply_cookies_for_url(url)

        # ① HTTP 请求
        try:
            html = self._fetch_html(url, headers=self.headers, timeout=30)
            result = self._parse(html, url)
            if self._is_valid(result):
                return result
            logger.warning("HTTP 抓取到空内容或反爬页面，尝试 Playwright 回退...")
        except requests.HTTPError as e:
            logger.warning(f"HTTP 错误 {e.response.status_code if e.response else e}，尝试 Playwright 回退...")
        except Exception as e:
            logger.warning(f"HTTP 异常: {e}，尝试 Playwright 回退...")

        # ② Playwright 浏览器回退
        try:
            html = self._fetch_with_playwright(url)
            if html:
                result = self._parse(html, url)
                if self._is_valid(result):
                    return result
                logger.warning("Playwright 抓取到空内容")
        except Exception as e:
            logger.error(f"Playwright 回退失败: {e}")

        # ③ 失败放弃
        logger.warning("微信抓取完全失败")
        return self._empty_result(url)

    # ========== Playwright 回退 ==========

    def _fetch_with_playwright(self, url: str) -> str | None:
        """Playwright headless Chromium 抓取微信文章"""
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            logger.warning("playwright 未安装，跳过浏览器回退")
            return None

        logger.info("启动 Playwright headless Chromium...")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent=(
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/120.0.0.0 Safari/537.36'
                ),
            )

            if self.cookies_list:
                cookies_to_add = [
                    {'name': c['name'], 'value': c['value'], 'domain': c['domain'], 'path': '/'}
                    for c in self.cookies_list
                ]
                context.add_cookies(cookies_to_add)
                logger.debug(f"Playwright 注入 {len(cookies_to_add)} 个 Cookies")

            page = context.new_page()
            try:
                page.goto(url, wait_until='networkidle', timeout=30000)
                page.wait_for_timeout(3000)
                html = page.content()
                logger.info("Playwright 抓取成功")
                return html
            finally:
                browser.close()

    # ========== HTML 解析 ==========

    def _parse(self, html: str, url: str) -> dict:
        """统一解析入口"""
        soup = BeautifulSoup(html, 'html.parser')
        return {
            'title': self._extract_title(soup),
            'author': self._extract_author(soup),
            'pub_date': self._extract_pub_date(soup, html),
            'content': self._extract_content(soup),
            'images': self._extract_images(soup),
            'original_url': url,
        }

    def _is_valid(self, data: dict) -> bool:
        """检测抓取结果是否有效：标题不为空且不为占位值，正文不为空"""
        title = data.get('title', '')
        content = data.get('content', '')
        if not title or title == '未知标题':
            return False
        if not content or len(content.strip()) < 100:
            return False
        # 反爬页面包含「环境异常」「验证」等关键词
        anti_crawl = ['环境异常', '请在微信客户端打开', '验证']
        if any(kw in content for kw in anti_crawl):
            return False
        return True

    def _empty_result(self, url: str) -> dict:
        return {'title': '', 'author': '', 'pub_date': '', 'content': '', 'images': [], 'original_url': url}

    def _extract_title(self, soup: BeautifulSoup) -> str:
        tag = soup.find('h1', id='activity-name')
        if tag:
            return tag.get_text().strip()
        meta = soup.find('meta', property='og:title')
        if meta and meta.get('content'):
            return meta['content']
        logger.warning("未找到文章标题")
        return "未知标题"

    def _extract_author(self, soup: BeautifulSoup) -> str:
        tag = soup.find(id='js_author_name')
        if tag:
            return tag.get_text().strip()
        for m in soup.find_all('span', class_='rich_media_meta'):
            text = m.get_text().strip()
            if text and '原创' not in text:
                return text
        logger.warning("未找到作者信息")
        return '未知作者'

    def _extract_pub_date(self, soup: BeautifulSoup, html: str) -> str:
        for script in soup.find_all('script'):
            if script.string and 'publish_time' in script.string:
                match = re.search(r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2})', script.string)
                if match:
                    return match.group(1)
        ts_match = re.search(r'"ct":\s*(\d+)', html)
        if ts_match:
            return datetime.fromtimestamp(int(ts_match.group(1))).strftime('%Y-%m-%d %H:%M:%S')
        logger.warning("未找到发布时间")
        return ''

    def _extract_content(self, soup: BeautifulSoup) -> str:
        div = soup.find('div', id='js_content') or soup.find('div', class_='rich_media_content')
        if div:
            return str(div)
        logger.warning("未找到正文内容")
        return ''

    def _extract_images(self, soup: BeautifulSoup) -> list:
        content = soup.find('div', id='js_content') or soup.find('div', class_='rich_media_content')
        if not content:
            return []
        images = []
        for img in content.find_all('img'):
            src = img.get('data-src') or img.get('src')
            if src:
                images.append(src.split('?')[0])
        logger.debug(f"提取到 {len(images)} 张图片")
        return images
