#!/usr/bin/env python3
"""
find-ebooks / 搜好书 — 安娜档案 + 中文图书平台搜索器

搜索安娜档案(Anna's Archive)获取电子书详细信息，同时查询以下中文图书平台：
- 豆瓣读书、掌阅 iReader、天猫图书、当当网、京东图书、机械工业出版社

为每本书提供对应平台搜索/商品页 URL。
"""

import cloudscraper
import json
import random
import re
import subprocess
import sys
import time
import os
import requests as http_requests
from urllib.parse import quote, unquote


class BookFinder:
    """安娜档案 + 中文平台图书搜索器"""

    def __init__(self, proxy_url=None):
        self.base_url = "https://annas-archive.gd"
        self.scraper = cloudscraper.create_scraper(
            browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True},
            delay=5, interpreter='nodejs'
        )
        # 代理配置：优先用参数，其次环境变量 HTTP_PROXY/HTTPS_PROXY
        resolved_proxy = proxy_url or os.environ.get('HTTP_PROXY') or os.environ.get('HTTPS_PROXY')
        if resolved_proxy:
            self.scraper.proxies = {'http': resolved_proxy, 'https': resolved_proxy}
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }

        # 中文平台搜索用的独立 Session（不带 cloudscraper 延迟）
        self.cn_session = http_requests.Session()
        self.cn_session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        })
        if resolved_proxy:
            self.cn_session.proxies = {'http': resolved_proxy, 'https': resolved_proxy}

    # ============================================================== #
    #  中文图书平台搜索配置
    # ============================================================== #
    CN_PLATFORMS = {
        'douban': {
            'name': '豆瓣读书',
            'search_url': lambda t: f'https://book.douban.com/subject_search?search_text={quote(t)}',
            # 搜索结果页，提取第一个 subject 链接
            'result_pattern': r'<a[^>]*href="(https://book\.douban\.com/subject/\d+/)"[^>]*class="[^"]*title[^"]*"',
            'fallback_pattern': r'<a[^>]*href="(https://book\.douban\.com/subject/\d+/)"[^>]*>',
        },
        'ireader': {
            'name': '掌阅 iReader',
            'search_url': lambda t: f'https://www.ireader.com/index.php?ca=search.keyword&keyword={quote(t)}',
            'result_pattern': r'<a[^>]*href="(/book/\d+\.html)"[^>]*class="[^"]*book_name[^"]*"',
            'fallback_pattern': r'<a[^>]*href="(/book/\d+\.html)"[^>]*>',
        },
        'tmall': {
            'name': '天猫图书',
            'search_url': lambda t: f'https://list.tmall.com/search_product.htm?q={quote(t)}',
            # 天猫反爬严格，直接给搜索页 URL
            'result_pattern': None,
        },
        'dangdang': {
            'name': '当当网',
            'search_url': lambda t: f'https://search.dangdang.com/?key={quote(t)}',
            'result_pattern': r'<a[^>]*href="(https?://product\.dangdang\.com/\d+\.html)"[^>]*class="pic"',
            'fallback_pattern': r'<a[^>]*href="(https?://product\.dangdang\.com/\d+\.html)"[^>]*>',
        },
        'jd': {
            'name': '京东图书',
            'search_url': lambda t: f'https://search.jd.com/Search?keyword={quote(t)}&enc=utf-8',
            'result_pattern': r'<a[^>]*href="(//item\.jd\.com/\d+\.html)"[^>]*class="[^"]*skname[^"]*"',
            'fallback_pattern': r'<a[^>]*href="(//item\.jd\.com/\d+\.html)"[^>]*>',
        },
        'cmpbook': {
            'name': '机械工业出版社',
            'search_url': lambda t: f'https://www.cmpbook.com/search.html?keyword={quote(t)}',
            'result_pattern': r'<a[^>]*href="(/book/\d+\.html)"[^>]*class="[^"]*book-name[^"]*"',
            'fallback_pattern': r'<a[^>]*href="(/book/\d+\.html)"[^>]*>',
        },
    }

    # ============================================================== #
    #  安娜档案搜索
    # ============================================================== #
    def search(self, query, max_results=10):
        """搜索安娜档案，返回 [{md5, title}] 列表"""
        url = f'{self.base_url}/search?q={quote(query)}'
        resp = self.scraper.get(url, headers=self.headers, timeout=60)
        text = resp.text

        seen_md5 = set()
        results = []

        for m in re.finditer(
            r'<a[^>]*href="/md5/([a-f0-9]{32})"[^>]*>(.*?)</a>',
            text, re.DOTALL
        ):
            md5 = m.group(1)
            raw_title = m.group(2)
            title = re.sub(r'<[^>]+>', '', raw_title).strip()
            title = re.sub(r'\s+', ' ', title)

            if md5 in seen_md5:
                for r in results:
                    if r['md5'] == md5:
                        r['title'] = title
                        break
            else:
                seen_md5.add(md5)
                results.append({'md5': md5, 'title': title})

        results = [r for r in results if r['title'] and len(r['title']) > 2]
        return results[:max_results]

    # ============================================================== #
    #  安娜档案详情页解析
    # ============================================================== #
    def get_details(self, md5, title_short=""):
        """从安娜档案详情页提取完整元数据"""
        url = f'{self.base_url}/md5/{md5}'
        try:
            resp = self.scraper.get(url, headers=self.headers, timeout=30)
            text = resp.text
        except Exception as e:
            return {'md5': md5, 'title': title_short, 'error': str(e)}

        info = {'md5': md5}

        # 完整标题
        m = re.search(r'<title>(.*?) - Anna', text)
        info['title'] = (
            m.group(1).replace('&#39;', "'").replace('&amp;', '&')
            if m else title_short
        )

        # 作者
        m = re.search(r'\(([A-Z][a-z][^)]{2,60})\)\.(?:epub|pdf|mobi|azw3|djvu)', text)
        author = m.group(1).strip() if m else ''
        if not author:
            m = re.search(r'filepath:zlib/[^/]+/[^/]+/([^/]+?)(?:/|__)', text)
            if m:
                author = m.group(1).strip()
        info['author'] = unquote(author).replace('+', ' ') if author else '—'

        # 语言
        m = re.search(r'prefix=lang:(\w+)', text)
        info['language'] = m.group(1) if m else '—'

        # 出版年份
        m = re.search(r'prefix=year:(\d{4})', text)
        info['year'] = m.group(1) if m else '—'

        # 文件大小
        m = re.search(r'prefix=filesize_bytes:(\d+)', text)
        if m:
            b = int(m.group(1))
            info['size'] = f'{b/1048576:.1f}MB' if b >= 1048576 else f'{b/1024:.1f}KB'
        else:
            info['size'] = '—'

        # 格式
        m = re.search(r'filepath:[^ ]*?\.(epub|pdf|mobi|azw3|djvu)', text)
        info['format'] = m.group(1).upper() if m else '—'

        # 慢速下载
        slow_links = sorted(set(re.findall(r'href="(/slow_download/[^"]+)"', text)))
        if slow_links:
            info['slow_download'] = f'https://annas-archive.gd{random.choice(slow_links)}'
            info['slow_servers'] = len(slow_links)
        else:
            info['slow_download'] = f'https://annas-archive.gd/slow_download/{md5}/0/0'
            info['slow_servers'] = 1

        # 快速下载
        fast_links = sorted(set(re.findall(r'href="(/fast_download/[^"]+)"', text)))
        if fast_links:
            info['fast_download'] = f'https://annas-archive.gd{fast_links[0]}'
            info['fast_servers'] = len(fast_links)
        else:
            info['fast_download'] = '—'

        # Amazon
        m = re.search(r'href="(https://www\.amazon\.com/(?!sendtokindle)[^"]+)"', text)
        info['amazon'] = m.group(1) if m else '—'

        # Google Books
        m = re.search(r'google\.com/books[^"]*id=([\w-]+)', text)
        info['google_books'] = f'https://books.google.com/books?id={m.group(1)}' if m else '—'

        # ISBN
        m = re.search(r'prefix=isbn:([\dX-]+)', text)
        info['isbn'] = m.group(1) if m else '—'

        info['detail_url'] = url
        return info

    # ============================================================== #
    #  中文图书平台搜索
    # ============================================================== #
    def search_cn_platform(self, title):
        """搜索所有中文图书平台，返回 {平台key: {name, url, search_url}}"""
        result = {}
        title_clean = re.sub(r'\s*[\(（].*?[\)）]', '', title).strip()

        for key, cfg in self.CN_PLATFORMS.items():
            search_url = cfg['search_url'](title_clean)

            # 尝试提取第一个搜索结果
            direct_url = None
            pattern = cfg.get('result_pattern')
            if pattern:
                try:
                    resp = self.cn_session.get(search_url, timeout=15)
                    resp.encoding = 'utf-8'
                    m = re.search(pattern, resp.text)
                    if not m:
                        # 尝试 fallback pattern
                        fb = cfg.get('fallback_pattern')
                        if fb:
                            m = re.search(fb, resp.text)
                    if m:
                        href = m.group(1)
                        if href.startswith('//'):
                            href = 'https:' + href
                        elif href.startswith('/'):
                            href = f'https://www.{key}.com{href}' if key != 'cmpbook' else f'https://www.cmpbook.com{href}'
                        direct_url = href
                except Exception:
                    pass

            result[key] = {
                'name': cfg['name'],
                'search_url': search_url,
                'url': direct_url or search_url,
                'found': direct_url is not None,
            }
            # 避免请求过快被 ban
            time.sleep(0.5)

        return result

    # ============================================================== #
    #  微信读书查询
    # ============================================================== #
    @staticmethod
    def check_weread(title, author=""):
        """查询微信读书上架情况"""
        api_key = os.environ.get('WEREAD_API_KEY', '')
        if not api_key:
            return None

        try:
            result = subprocess.run(
                [
                    'curl', '-s', '-X', 'POST',
                    'https://i.weread.qq.com/api/agent/gateway',
                    '-H', f'Authorization: Bearer {api_key}',
                    '-H', 'Content-Type: application/json',
                    '-d', json.dumps({
                        "api_name": "/store/search",
                        "keyword": title[:50],
                        "count": 3,
                        "skill_version": "1.0.4"
                    })
                ],
                capture_output=True, text=True, timeout=10
            )
            data = json.loads(result.stdout)
            books = data.get('results', [{}])[0].get('books', [])
            if books:
                b = books[0]['bookInfo']
                return {
                    'title': b.get('title', ''),
                    'author': b.get('author', ''),
                    'url': b.get('deepLink', ''),
                    'bookId': b.get('bookId', ''),
                }
        except Exception:
            pass
        return None

    # ============================================================== #
    #  主入口
    # ============================================================== #
    def search_and_report(self, query, max_results=10,
                          check_weread=True, check_cn=True):
        """搜索安娜档案 + 查询中文平台，返回完整结果列表"""
        books = self.search(query, max_results)
        if not books:
            return []

        results = []
        for i, b in enumerate(books):
            msg = f'[{i+1}/{len(books)}] {b["title"][:50]}'
            print(msg, file=sys.stderr)

            info = self.get_details(b['md5'], b['title'])

            # 微信读书
            if check_weread and info.get('title'):
                wr = self.check_weread(info['title'], info.get('author', ''))
                if wr:
                    info['weread'] = wr

            # 中文图书平台
            if check_cn and info.get('title'):
                cn = self.search_cn_platform(info['title'])
                if cn:
                    info['cn_platforms'] = cn

            results.append(info)
            if i < len(books) - 1:
                time.sleep(1.5)

        return results


# ================================================================== #
#  格式化输出
# ================================================================== #

def format_report(results, json_output=False):
    """格式化输出报告"""
    if json_output:
        return json.dumps(results, ensure_ascii=False, indent=2)

    lines = []
    lines.append(f'## 搜索结果：共找到 {len(results)} 本\n')

    # 表格头
    lines.append('| # | 书名 | 作者 | 格式 | 大小 | 语言 | 年份 |')
    lines.append('|---|------|------|------|------|------|------|')
    for i, r in enumerate(results, 1):
        lines.append(
            f'| {i} | **{r.get("title","?")[:45]}** '
            f'| {r.get("author","—")[:20]} '
            f'| {r.get("format","—")} '
            f'| {r.get("size","—")} '
            f'| {r.get("language","—")} '
            f'| {r.get("year","—")} |'
        )
    lines.append('')

    # 每本书的详情块
    for i, r in enumerate(results, 1):
        lines.append(f'### {i}. {r.get("title","?")}')
        lines.append('```')
        lines.append(f'安娜档案详情: {r.get("detail_url","—")}')
        lines.append(f'慢速下载:     {r.get("slow_download","—")}')
        if r.get('fast_download') and r['fast_download'] != '—':
            lines.append(f'快速下载:     {r["fast_download"]}')
        if r.get('amazon') and r['amazon'] != '—':
            lines.append(f'Amazon:       {r["amazon"]}')
        if r.get('google_books') and r['google_books'] != '—':
            lines.append(f'Google Books: {r["google_books"]}')
        if r.get('weread'):
            lines.append(f'微信读书:     {r["weread"]["url"]}')
        if r.get('isbn') and r['isbn'] != '—':
            lines.append(f'ISBN:         {r["isbn"]}')
        lines.append('```')

        # 中文图书平台
        cn = r.get('cn_platforms', {})
        if cn:
            lines.append('')
            lines.append('**中文图书平台：**')
            for key in ['douban', 'ireader', 'tmall', 'dangdang', 'jd', 'cmpbook']:
                p = cn.get(key)
                if p:
                    icon = '✅' if p.get('found') else '🔍'
                    lines.append(f'- {icon} **{p["name"]}**: {p["url"]}')
            lines.append('')

        lines.append(
            f'> 慢速下载可选服务器: {r.get("slow_servers",1)} 个'
            '（修改URL末尾 /0/0 可切换服务器）'
        )
        lines.append('')

    return '\n'.join(lines)


# ================================================================== #
#  命令行入口
# ================================================================== #

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description='find-ebooks / 搜好书 — 安娜档案 + 中文平台图书搜索'
    )
    parser.add_argument('query', help='搜索关键词')
    parser.add_argument('--max', type=int, default=10, help='最大结果数')
    parser.add_argument('--json', action='store_true', help='输出JSON格式')
    parser.add_argument('--no-weread', action='store_true', help='不查微信读书')
    parser.add_argument('--no-cn', action='store_true', help='不查中文图书平台')
    parser.add_argument('--proxy', help='代理服务器地址，如 http://127.0.0.1:7890（默认读取 HTTP_PROXY 环境变量）')
    args = parser.parse_args()

    finder = BookFinder(proxy_url=args.proxy)
    results = finder.search_and_report(
        args.query, args.max,
        check_weread=not args.no_weread,
        check_cn=not args.no_cn,
    )
    print(format_report(results, args.json))


if __name__ == '__main__':
    main()
