"""
知乎文章抓取器 — v1.2.0
HTTP (Cookies) → Playwright 浏览器 → 失败放弃
"""
from bs4 import BeautifulSoup
from fetchers.base_fetcher import BaseFetcher
from utils.logger import logger
import re
import requests
from datetime import datetime


class ZhihuFetcher(BaseFetcher):
    """知乎文章抓取器（二级回退）"""

    def fetch_article(self, url: str) -> dict:
        """抓取文章：HTTP → Playwright → 失败"""
        self.headers['Referer'] = 'https://www.zhihu.com/'
        self._apply_cookies_for_url(url)

        # ① HTTP 请求
        try:
            html = self._fetch_html(url, headers=self.headers, timeout=30)
            return self._parse(html, url)
        except requests.HTTPError as e:
            if e.response is not None and e.response.status_code == 403:
                logger.warning("知乎返回 403 (Cookies 可能过期)，尝试 Playwright 回退...")
            else:
                logger.error(f"知乎 HTTP 错误: {e.response.status_code if e.response else e}")
                return self._empty_result(url)
        except Exception as e:
            logger.error(f"知乎抓取异常: {e}")
            return self._empty_result(url)

        # ② Playwright 浏览器回退
        try:
            html = self._fetch_with_playwright(url)
            if html:
                return self._parse(html, url)
        except Exception as e:
            logger.error(f"Playwright 回退失败: {e}")

        # ③ 失败放弃
        logger.warning("知乎抓取完全失败（HTTP 403 + Playwright 不可用）")
        return self._empty_result(url)

    # ========== Playwright 回退 ==========

    def _fetch_with_playwright(self, url: str) -> str | None:
        """
        使用 Playwright headless Chromium 抓取知乎页面。
        自动加载 self.cookies_list 中的 Cookies 到浏览器上下文。
        """
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            logger.warning("playwright 未安装，跳过浏览器回退。请参阅 requirements.txt 安装依赖")
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

            # 注入 Cookies（从 Netscape 文件加载）
            if self.cookies_list:
                cookies_to_add = []
                for c in self.cookies_list:
                    cookies_to_add.append({
                        'name': c['name'],
                        'value': c['value'],
                        'domain': c['domain'],
                        'path': '/',
                    })
                context.add_cookies(cookies_to_add)
                logger.debug(f"Playwright 注入 {len(cookies_to_add)} 个 Cookies")

            page = context.new_page()
            try:
                page.goto(url, wait_until='networkidle', timeout=30000)
                page.wait_for_timeout(3000)  # 等待 JS 渲染完成
                html = page.content()
                logger.info("Playwright 抓取成功")
                return html
            finally:
                browser.close()

    # ========== HTML 解析 ==========

    def _parse(self, html: str, url: str) -> dict:
        """统一解析入口：HTML → article_data dict"""
        soup = BeautifulSoup(html, 'html.parser')
        if 'answer' in url:
            return self._extract_answer(soup, url, html)
        if '/pin/' in url:
            return self._extract_pin(soup, url, html)
        return self._extract_article(soup, url, html)

    def _empty_result(self, url: str) -> dict:
        return {'title': '', 'author': '', 'pub_date': '', 'content': '', 'images': [], 'original_url': url}

    def _extract_pin(self, soup, url, html):
        """知乎想法（Pin）"""
        # 标题：从 meta description 取
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            desc = meta_desc['content']
            title = desc.split('|')[0].strip() if '|' in desc else desc[:50]
        else:
            title = '未知标题'

        # 作者
        author_meta = soup.find('meta', itemprop='author')
        author = author_meta['content'] if author_meta and author_meta.get('content') else '未知作者'

        pub_date = self._extract_date(html)

        # 正文：优先 RichContent/RichText
        content_div = soup.find('div', class_='RichContent') or soup.find('div', class_='RichText')
        if content_div:
            # 图片懒加载修复：data-original/data-actualsrc → src
            for img in content_div.find_all('img'):
                real = img.get('data-original') or img.get('data-actualsrc')
                if real and not real.startswith('data:'):
                    img['src'] = real
            images = self._extract_images(content_div)
            content = str(self._clean_zhihu_html(content_div))
        else:
            # fallback：取 body 可见文本
            for tag in soup.find_all(['header', 'nav', 'footer', 'script', 'style']):
                tag.decompose()
            body = soup.find('body')
            text = body.get_text(separator='\n', strip=True) if body else ''
            lines = [l for l in text.split('\n') if len(l) > 10 and '知乎' not in l][:50]
            content = '<p>' + '</p><p>'.join(lines) + '</p>'
            images = self._extract_images(soup)

        return {
            'title': title, 'author': author, 'pub_date': pub_date,
            'content': content, 'images': images, 'original_url': url,
        }

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

        images = self._extract_images(content_div)
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

        images = self._extract_images(content_div)
        content = str(self._clean_zhihu_html(content_div))
        return {'title': title, 'author': author, 'pub_date': pub_date, 'content': content, 'images': images, 'original_url': url}

    def _clean_zhihu_html(self, element):
        """清理知乎 HTML 中的无用元素，保留正文内容"""
        if not element:
            return element

        for tag in element.find_all('style'):
            tag.decompose()

        for tag_name in ['script', 'noscript', 'meta', 'link']:
            for tag in element.find_all(tag_name):
                tag.decompose()

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

        for tag in element.find_all(True):
            if tag.name == 'img':
                keep_attrs = {'data-original', 'data-actualsrc'}
                attrs_to_remove = [
                    k for k in tag.attrs
                    if k.startswith('data-') and k.lower() not in keep_attrs
                ]
                for k in attrs_to_remove:
                    del tag[k]
            else:
                attrs_to_remove = [k for k in tag.attrs if k.startswith('data-')]
                for k in attrs_to_remove:
                    del tag[k]

            js_attrs = [k for k in tag.attrs if k in ('options', 'data-zop')]
            for k in js_attrs:
                del tag[k]

            if tag.get('class'):
                tag['class'] = [
                    c for c in tag['class']
                    if not re.match(r'^css-[a-z0-9]{2,}$', c)
                ]
                if not tag['class']:
                    del tag['class']

        for tag in element.find_all(True):
            if tag.name in ('style', 'script'):
                tag.decompose()

        return element

    def _extract_date(self, html):
        match = re.search(r'"created":\s*(\d+)', html) or re.search(r'"updatedTime":\s*(\d+)', html)
        if match:
            return datetime.fromtimestamp(int(match.group(1))).strftime('%Y-%m-%d %H:%M:%S')
        return ''

    def _extract_images(self, content_div) -> list:
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
