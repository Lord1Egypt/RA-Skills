"""
离线输入解析器：将 HTML 文本 / .mhtml 文件解析为标准 article_data

供 article-fetcher 后半段管线（OSS 上传 → 替换 URL → 打标 → 字数 → 归档）复用。
设计要点（源自 wechat-article-capture 技能沉淀的三陷阱）：
  1. 懒加载图片：data-src 搬家到 src 后必须 del data-src，否则 markdownify 仍读占位符
  2. MHTML 编码：get_payload(decode=True) 取 bytes → 按 charset 或 utf-8 解码，避免乱码
  3. 占位符过滤：images 列表排除 data:image/svg+xml 类占位符

版本：v1.3.5
"""
import email
import re
from typing import Dict, List
from bs4 import BeautifulSoup
from utils.logger import logger


# article_data 契约字段（与 fetchers/base_fetcher.py 注释一致）
_EMPTY_RESULT = lambda url: {
    'title': '', 'author': '', 'pub_date': '',
    'content': '', 'images': [], 'original_url': url,
}


def _extract_content_container(soup: BeautifulSoup, platform: str):
    """定位正文容器，返回 (容器节点, 是否微信)"""
    if platform == 'wechat':
        div = soup.find('div', id='js_content') or soup.find('div', class_='rich_media_content')
        if div:
            return div, True
    # 通用回退选择器
    for sel in ('article', 'main', 'body'):
        node = soup.find(sel)
        if node:
            return node, False
    return soup, False


def _extract_title(soup: BeautifulSoup, is_wechat: bool) -> str:
    if is_wechat:
        tag = soup.find('h1', id='activity-name')
        if tag and tag.get_text(strip=True):
            return tag.get_text(strip=True)
    meta = soup.find('meta', property='og:title')
    if meta and meta.get('content'):
        return meta['content'].strip()
    if is_wechat:
        h1 = soup.find('h1')
        if h1 and h1.get_text(strip=True):
            return h1.get_text(strip=True)
    title_tag = soup.find('title')
    if title_tag and title_tag.get_text(strip=True):
        return title_tag.get_text(strip=True)
    return ''


def _extract_author(soup: BeautifulSoup, is_wechat: bool) -> str:
    if is_wechat:
        tag = soup.find(id='js_author_name')
        if tag and tag.get_text(strip=True):
            return tag.get_text(strip=True)
        for m in soup.find_all('span', class_='rich_media_meta'):
            text = m.get_text(strip=True)
            if text and '原创' not in text:
                return text
    meta = soup.find('meta', attrs={'name': 'author'})
    if meta and meta.get('content'):
        return meta['content'].strip()
    return ''


def _extract_pub_date(soup: BeautifulSoup, html: str, is_wechat: bool) -> str:
    if is_wechat:
        for script in soup.find_all('script'):
            if script.string and 'publish_time' in script.string:
                m = re.search(r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2})', script.string)
                if m:
                    return m.group(1)
        ts = re.search(r'"ct":\s*(\d+)', html)
        if ts:
            from datetime import datetime
            return datetime.fromtimestamp(int(ts.group(1))).strftime('%Y-%m-%d %H:%M:%S')
    meta = soup.find('meta', property='article:published_time')
    if meta and meta.get('content'):
        return meta['content'].strip()
    return ''


def _fix_and_collect_images(container: BeautifulSoup) -> List[str]:
    """
    修复懒加载（data-src → src 并删除 data-src），返回去重真实图片 URL 列表。
    关键：src 最终值与 images 列表保持一致（均去除 query 参数），确保下游 URL 替换可命中。
    """
    images: List[str] = []
    seen = set()
    for img in container.find_all('img'):
        ds = (img.get('data-src') or '').strip()
        src = (img.get('src') or '').strip()
        real = ds or src
        if not real or real.startswith('data:image'):
            continue
        real = real.split('?')[0]
        img['src'] = real  # 归一化 src，确保与 images 列表一致
        if 'data-src' in img.attrs:
            del img['data-src']  # 陷阱①：搬完即删，根治占位符
        if real in seen:
            continue
        seen.add(real)
        images.append(real)
    logger.debug(f"提取到 {len(images)} 张图片（已过滤占位符/去重）")
    return images


def parse_html_to_article(html: str, platform: str = 'wechat', article_url: str = '') -> Dict:
    """将 HTML 文本解析为 article_data（标准契约）"""
    soup = BeautifulSoup(html, 'html.parser')
    container, is_wechat = _extract_content_container(soup, platform)

    # 空校验：基于正文纯文本长度，避免被下方图片属性改写（del data-src）影响 HTML 长度判定
    if not container or len(container.get_text(strip=True)) < 10:
        logger.warning("解析结果无效：正文文本过短")
        return _EMPTY_RESULT(article_url)

    title = _extract_title(soup, is_wechat)
    author = _extract_author(soup, is_wechat)
    pub_date = _extract_pub_date(soup, html, is_wechat)
    images = _fix_and_collect_images(container)
    content = str(container)  # 在图片属性改写（data-src→src 并删除）之后取值，内容更干净

    if not title:
        logger.warning("解析结果无效：未提取到标题")
        return _EMPTY_RESULT(article_url)

    return {
        'title': title,
        'author': author,
        'pub_date': pub_date,
        'content': content,
        'images': images,
        'original_url': article_url,
    }


def parse_mhtml_to_article(path: str, platform: str = 'wechat', article_url: str = '') -> Dict:
    """解析 .mhtml 文件为 article_data（陷阱②：编码修复）"""
    with open(path, 'rb') as f:
        msg = email.message_from_binary_file(f)

    html = None
    for part in msg.walk():
        if part.get_content_type() == 'text/html':
            payload = part.get_payload(decode=True)
            if payload is None:
                continue
            charset = part.get_content_charset() or 'utf-8'  # 陷阱②：探测 charset
            try:
                html = payload.decode(charset, errors='replace')
            except (LookupError, UnicodeDecodeError):
                html = payload.decode('utf-8', errors='replace')
            break

    if not html:
        logger.warning("MHTML 中未找到 text/html 部分")
        return _EMPTY_RESULT(article_url)

    return parse_html_to_article(html, platform, article_url)
