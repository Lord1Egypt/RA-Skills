"""
豆瓣文章抓取器
"""
from bs4 import BeautifulSoup
from fetchers.base_fetcher import BaseFetcher
from utils.logger import logger
import re


class DoubanFetcher(BaseFetcher):
    """豆瓣文章抓取器"""

    PAGE_TYPES = {
        'note': {'content': ['#link-report', '.note'], 'title': ['span[property="v:summary"]', 'h1']},
        'review': {'content': ['#link-report'], 'title': ['span[property="v:summary"]', 'h1']},
        'status': {'content': ['.status-content'], 'title': None},
    }

    def fetch_article(self, url: str) -> dict:
        self.headers['Referer'] = 'https://www.douban.com/'
        try:
            html = self._fetch_html(url, headers=self.headers, timeout=30)
            soup = BeautifulSoup(html, 'html.parser')

            page_type = self._detect_page_type(url)
            return self._extract(soup, url, page_type)
        except Exception as e:
            logger.error(f"抓取豆瓣文章失败: {e}")
            return {'title': '', 'author': '', 'pub_date': '', 'content': '', 'images': [], 'original_url': url}

    def _detect_page_type(self, url: str) -> str:
        if 'note' in url:
            return 'note'
        elif 'review' in url:
            return 'review'
        elif 'status' in url:
            return 'status'
        return 'note'

    def _extract(self, soup, url, page_type):
        cfg = self.PAGE_TYPES.get(page_type, self.PAGE_TYPES['note'])

        # 标题：优先 v:summary，其次 h1，最后 fallback
        title = '未知标题'
        title_tag = (soup.find('span', property='v:summary') or
                     soup.find('h1') or
                     soup.find('title'))
        if title_tag:
            title = title_tag.get_text().strip()
            if not title or title.startswith('http'):
                title = '未知标题'

        # 作者：兼容桌面端 + 移动端
        # 优先使用有文本内容的 a[href*=/people/] 标签（避免匹配到头像链接）
        author_tag = (soup.find('a', class_='note-author') or
                      soup.find('a', property='v:reviewer') or
                      soup.find('a', class_='statustitle') or
                      soup.find('a', class_='user-link'))
        if not author_tag:
            # 迭代查找有文本内容的 people 链接
            for a in soup.find_all('a', href=re.compile(r'/people/')):
                if a.get_text().strip():
                    author_tag = a
                    break
        author = author_tag.get_text().strip() if author_tag else '未知作者'

        # 发布时间：兼容桌面端 + 移动端
        pub_date_tag = (soup.find('span', property='v:dtreviewed') or
                        soup.find('span', class_='note-time') or
                        soup.find('span', class_='pubdate') or
                        soup.find('span', class_='create-time') or
                        soup.find('div', class_='main-meta'))
        pub_date = ''
        if pub_date_tag:
            # 从文本中提取第一个匹配 YYYY-MM-DD HH:MM:SS 的日期
            date_text = pub_date_tag.get_text().strip()
            pub_date = self._parse_date(date_text)
        # pub_date 缺失时留空（不伪造当前时间）

        # 正文：按优先级尝试多个选择器
        content = ''
        # 1. 桌面端 #link-report
        # 2. 移动端 div.review-content
        # 3. .note（笔记页面）
        content_selectors = [
            ('id', 'link-report'),
            ('class', 'review-content'),
            ('class', 'note'),
        ]
        for search_type, selector in content_selectors:
            if search_type == 'id':
                tag = soup.find(id=selector)
            else:
                tag = soup.find(class_=selector)
            if tag:
                # 移除版权信息等无关元素
                for unwanted in tag.find_all(class_=re.compile(r'copyright|actions|share')):
                    unwanted.decompose()
                content = str(tag)
                break

        # 广播特殊处理
        if page_type == 'status' and not content:
            status_div = soup.find(class_='status-content')
            if status_div:
                content = status_div.get_text().strip()
                title = content[:50] + '...' if len(content) > 50 else content or '豆瓣广播'

        # 图片：优先提取 content 内的图片
        images = []
        content_soup = BeautifulSoup(content, 'html.parser') if content else soup
        for img in content_soup.find_all('img'):
            src = img.get('src') or img.get('data-original')
            if src and 'doubanio.com' in src:
                images.append(src)

        # 如果 content 内没找到图片，从整个页面提取
        if not images:
            seen = set()
            for img in soup.find_all('img'):
                src = img.get('src') or img.get('data-original')
                if src and 'doubanio.com' in src and src not in seen:
                    images.append(src)
                    seen.add(src)

        return {
            'title': title, 'author': author, 'pub_date': pub_date,
            'content': content, 'images': images, 'original_url': url
        }

    def _parse_date(self, date_text):
        if not date_text:
            return ''
        # 优先匹配 YYYY-MM-DD HH:MM:SS 完整格式
        match = re.search(r'(\d{4}[-/]\d{2}[-/]\d{2})\s+(\d{2}:\d{2}:\d{2})', date_text)
        if match:
            return match.group(1).replace('/', '-') + ' ' + match.group(2)
        # 仅日期
        match = re.search(r'(\d{4}[-/]\d{2}[-/]\d{2})', date_text)
        if match:
            return match.group(1).replace('/', '-') + ' 00:00:00'
        return ''  # 缺失时留空（不伪造当前时间）
