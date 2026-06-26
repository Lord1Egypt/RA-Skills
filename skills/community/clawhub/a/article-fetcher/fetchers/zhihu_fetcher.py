"""
知乎文章抓取器
"""
from bs4 import BeautifulSoup
from fetchers.base_fetcher import BaseFetcher
from utils.logger import logger
import re
from datetime import datetime


class ZhihuFetcher(BaseFetcher):
    """知乎文章抓取器"""

    def fetch_article(self, url: str) -> dict:
        self.headers['Referer'] = 'https://www.zhihu.com/'
        self._apply_cookies_for_url(url)

        try:
            html = self._fetch_html(url, headers=self.headers, timeout=30)
            soup = BeautifulSoup(html, 'html.parser')

            if 'answer' in url:
                return self._extract_answer(soup, url, html)
            return self._extract_article(soup, url, html)
        except Exception as e:
            logger.error(f"抓取知乎内容失败: {e}")
            return {'title': '', 'author': '', 'pub_date': '', 'content': '', 'images': [], 'original_url': url}

    def _extract_article(self, soup, url, html):
        """专栏文章"""
        title_tag = soup.find('h1', class_='Post-Title') or soup.find('h1')
        title = title_tag.get_text().strip() if title_tag else '未知标题'

        author_tag = soup.find('meta', itemprop='author')
        author = author_tag['content'] if author_tag and author_tag.get('content') else '未知作者'

        pub_date = self._extract_date(html)
        content_div = soup.find('div', class_='RichText') or soup.find('div', itemprop='articleBody')
        if not content_div:
            return {'title': title, 'author': author, 'pub_date': pub_date, 'content': '', 'images': [], 'original_url': url}

        # 先提取图片（原始 HTML 包含完整 data-* 属性）
        images = self._extract_images(content_div)
        # 再清理 HTML（原地修改，移除噪音）
        content = str(self._clean_zhihu_html(content_div))
        return {'title': title, 'author': author, 'pub_date': pub_date, 'content': content, 'images': images, 'original_url': url}

    def _extract_answer(self, soup, url, html):
        """回答"""
        title_tag = soup.find('h1', class_='QuestionHeader-title') or soup.find('h1')
        title = title_tag.get_text().strip() if title_tag else '未知标题'

        author_tag = soup.find('span', class_='AuthorInfo-name') or soup.find('a', class_='UserLink-link')
        author = author_tag.get_text().strip() if author_tag else '未知作者'

        pub_date = self._extract_date(html)
        content_div = soup.find('div', class_='RichContent-inner') or soup.find('div', class_='Answer-richContent')
        if not content_div:
            return {'title': title, 'author': author, 'pub_date': pub_date, 'content': '', 'images': [], 'original_url': url}

        # 先提取图片（原始 HTML 包含完整 data-* 属性）
        images = self._extract_images(content_div)
        # 再清理 HTML（原地修改，移除噪音）
        content = str(self._clean_zhihu_html(content_div))
        return {'title': title, 'author': author, 'pub_date': pub_date, 'content': content, 'images': images, 'original_url': url}

    def _clean_zhihu_html(self, element):
        """清理知乎 HTML 中的无用元素，保留正文内容"""
        if not element:
            return element

        # 1. 移除所有 <style> 标签（知乎 emotion CSS 内嵌，64K+ 噪音来源）
        for tag in element.find_all('style'):
            tag.decompose()

        # 2. 移除脚本和元数据标签
        for tag_name in ['script', 'noscript', 'meta', 'link']:
            for tag in element.find_all(tag_name):
                tag.decompose()

        # 3. 移除知乎特有的无用容器（保留内含的图片）
        useless_classes = [
            'LinkCard', 'ExternalLinkCard', 'RichText-link',
            'RichText-actions', 'RichText-copyright', 'ContentItem-actions',
            'RichText-admin', 'vote-arrow', 'vote',
        ]
        for cls in useless_classes:
            for tag in element.find_all(class_=cls):
                imgs = tag.find_all('img')
                if imgs:
                    for img in imgs:
                        tag.insert_before(img)
                tag.decompose()

        # 4. 清理无用 data-* 属性，但保留图片的真实 URL
        for tag in element.find_all(True):
            if tag.name == 'img':
                # 图片标签：只保留 data-original / data-actualsrc（真实 URL）
                # 移除其他 data-* 属性（如 data-lazy-status, data-attachment 等）
                keep_attrs = {'data-original', 'data-actualsrc'}
                attrs_to_remove = [
                    k for k in tag.attrs
                    if k.startswith('data-') and k.lower() not in keep_attrs
                ]
                for k in attrs_to_remove:
                    del tag[k]
            else:
                # 非图片标签：移除所有 data-* 属性
                attrs_to_remove = [k for k in tag.attrs if k.startswith('data-')]
                for k in attrs_to_remove:
                    del tag[k]

            # 移除 JS 序列化残留属性（如 options="[object Object]"）
            js_attrs = [k for k in tag.attrs if k in ('options', 'data-zop')]
            for k in js_attrs:
                del tag[k]

            # 移除动态生成的 CSS class（css-xxxxxx 格式）
            if tag.get('class'):
                tag['class'] = [
                    c for c in tag['class']
                    if not re.match(r'^css-[a-z0-9]{2,}$', c)
                ]
                if not tag['class']:
                    del tag['class']

        # 5. 移除空的 style/script 残留（防御）
        for tag in element.find_all(True):
            if tag.name in ('style', 'script'):
                tag.decompose()

        return element

    def _extract_date(self, html):
        """从 script 标签提取时间"""
        match = re.search(r'"created":\s*(\d+)', html) or re.search(r'"updatedTime":\s*(\d+)', html)
        if match:
            return datetime.fromtimestamp(int(match.group(1))).strftime('%Y-%m-%d %H:%M:%S')
        return ''  # 缺失时留空（不伪造当前时间）

    def _extract_images(self, content_div) -> list:
        """提取图片 URL（知乎每种图有 _r.jpg 和 _720w.jpg 两个变体，全部提取用于替换）"""
        if not content_div:
            return []
        images = []
        seen = set()
        for img in content_div.find_all('img'):
            for attr in ['data-original', 'data-actualsrc', 'src']:
                src = img.get(attr)
                if src and not src.startswith('data:image/svg') and src not in seen:
                    images.append(src)
                    seen.add(src)
        return images
