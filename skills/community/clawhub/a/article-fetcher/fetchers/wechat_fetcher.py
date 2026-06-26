"""
微信公众号文章抓取器
"""
from bs4 import BeautifulSoup
from fetchers.base_fetcher import BaseFetcher
from utils.logger import logger
import re
from datetime import datetime


class WechatFetcher(BaseFetcher):
    """微信公众号文章抓取器"""

    def fetch_article(self, url: str) -> dict:
        logger.info(f"开始抓取微信公众号文章：{url}")
        self._apply_cookies_for_url(url)

        try:
            html = self._fetch_html(url, headers=self.headers, timeout=30)
            soup = BeautifulSoup(html, 'html.parser')

            article_data = {
                'title': self._extract_title(soup),
                'author': self._extract_author(soup),
                'pub_date': self._extract_pub_date(soup, html),
                'content': self._extract_content(soup),
                'images': self._extract_images(soup),
                'original_url': url
            }

            logger.info(
                f"抓取成功 | 标题：{article_data['title']} | "
                f"作者：{article_data['author']} | 图片：{len(article_data['images'])} 张"
            )
            return article_data

        except Exception as e:
            logger.error(f"抓取微信公众号文章失败：{e}")
            return {'title': '', 'author': '', 'pub_date': '', 'content': '', 'images': [], 'original_url': url}

    def _extract_title(self, soup: BeautifulSoup) -> str:
        # id=activity-name
        tag = soup.find('h1', id='activity-name')
        if tag:
            return tag.get_text().strip()
        # meta og:title
        meta = soup.find('meta', property='og:title')
        if meta and meta.get('content'):
            return meta['content']
        logger.warning("未找到文章标题")
        return "未知标题"

    def _extract_author(self, soup: BeautifulSoup) -> str:
        # id=js_author_name（<a> 或 <span>）
        tag = soup.find(id='js_author_name')
        if tag:
            return tag.get_text().strip()
        # class=rich_media_meta 中非"原创"的文本
        for m in soup.find_all('span', class_='rich_media_meta'):
            text = m.get_text().strip()
            if text and '原创' not in text:
                return text
        logger.warning("未找到作者信息")
        return '未知作者'

    def _extract_pub_date(self, soup: BeautifulSoup, html: str) -> str:
        # 从 script 标签查找 publish_time
        for script in soup.find_all('script'):
            if script.string and 'publish_time' in script.string:
                match = re.search(r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2})', script.string)
                if match:
                    return match.group(1)
        # 查找时间戳
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
                images.append(src.split('?')[0])  # 去除微信图片参数
        logger.debug(f"提取到 {len(images)} 张图片")
        return images
