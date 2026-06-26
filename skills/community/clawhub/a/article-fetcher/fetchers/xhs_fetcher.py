"""
小红书文章抓取器
"""
from bs4 import BeautifulSoup
from fetchers.base_fetcher import BaseFetcher
from utils.logger import logger
import json
from datetime import datetime


class XHSFetcher(BaseFetcher):
    """小红书文章抓取器"""

    def fetch_article(self, url: str) -> dict:
        self.headers['Referer'] = 'https://www.xiaohongshu.com/'
        try:
            html = self._fetch_html(url, headers=self.headers, timeout=30)
            soup = BeautifulSoup(html, 'html.parser')

            # 尝试从 window.__INITIAL_STATE__ 提取 JSON
            note_data = self._extract_json_state(soup)
            if note_data:
                return self._build_from_json(note_data, url)

            # 降级：从 HTML 元素提取
            return self._build_from_html(soup, url)
        except Exception as e:
            logger.error(f"抓取小红书文章失败: {e}")
            return {'title': '', 'author': '', 'pub_date': '', 'content': '', 'images': [], 'original_url': url}

    def _extract_json_state(self, soup):
        """从 script 标签提取 __INITIAL_STATE__ JSON 数据"""
        for script in soup.find_all('script'):
            if script.string and 'window.__INITIAL_STATE__=' in script.string:
                json_str = script.string.replace('window.__INITIAL_STATE__=', '').strip().rstrip(';')
                try:
                    state = json.loads(json_str)
                    return self._traverse(state)
                except json.JSONDecodeError:
                    continue
        return None

    def _traverse(self, obj):
        """递归查找 note 数据"""
        if isinstance(obj, dict):
            if 'note' in obj and isinstance(obj['note'], dict) and 'title' in obj['note']:
                return obj['note']
            for v in obj.values():
                result = self._traverse(v)
                if result:
                    return result
        elif isinstance(obj, list):
            for item in obj:
                result = self._traverse(item)
                if result:
                    return result
        return None

    def _build_from_json(self, note, url):
        user = note.get('user', {})
        pub_ts = note.get('time')
        if pub_ts and isinstance(pub_ts, (int, float)) and pub_ts > 0:
            pub_date = datetime.fromtimestamp(pub_ts / 1000).strftime('%Y-%m-%d %H:%M:%S')
        else:
            pub_date = ''

        images = []
        for img_item in note.get('imageList', []):
            if 'url' in img_item:
                images.append(img_item['url'])
        if not images and 'video' in note and 'cover' in note['video']:
            images.append(note['video']['cover'])

        return {
            'title': note.get('title', '未知标题'),
            'author': user.get('nickName', '未知作者'),
            'pub_date': pub_date,
            'content': note.get('desc', ''),
            'images': images,
            'original_url': url
        }

    def _build_from_html(self, soup, url):
        title = (soup.find('h1') or soup.find(class_='title'))
        title = title.get_text().strip() if title else '未知标题'

        author = (soup.find(class_='user-name') or soup.find(class_='author'))
        author = author.get_text().strip() if author else '未知作者'

        desc = (soup.find(class_='desc') or soup.find(class_='note-content'))
        content = desc.get_text().strip() if desc else ''

        images = []
        for img in soup.find_all('img'):
            src = img.get('src') or img.get('data-src')
            if src and ('xhscdn.com' in src):
                images.append(src)

        return {
            'title': title,
            'author': author,
            'pub_date': '',
            'content': content,
            'images': images,
            'original_url': url
        }
