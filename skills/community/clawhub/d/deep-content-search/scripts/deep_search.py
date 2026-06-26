#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
深度内容搜索工具 v1.0
整合微信公众号和知乎内容抓取，支持多平台搜索

使用方法:
    # 综合搜索（微信+知乎），默认3条
    python3 deep_search.py "OpenClaw教程"
    
    # 指定结果数量
    python3 deep_search.py "AI人工智能" --limit 5
    
    # 只搜微信公众号
    python3 deep_search.py "大龙虾" --source wechat
    
    # 只搜知乎
    python3 deep_search.py "如何学习编程" --source zhihu
"""

import argparse
import json
import re
import sys
import time
from dataclasses import dataclass, asdict, field
from typing import Optional, List, Dict
from html.parser import HTMLParser

try:
    import requests
    from bs4 import BeautifulSoup
    from fake_useragent import UserAgent
except ImportError:
    print("请安装依赖: pip install requests beautifulsoup4 lxml fake-useragent")
    sys.exit(1)


class MLStripper(HTMLParser):
    """HTML标签清理器"""
    def __init__(self):
        super().__init__()
        self.reset()
        self.fed = []
    
    def handle_data(self, d):
        self.fed.append(d)
    
    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html: str) -> str:
    """移除HTML标签"""
    s = MLStripper()
    s.feed(html)
    return s.get_data()


# ============================================================================
# 数据结构
# ============================================================================

@dataclass
class WechatArticle:
    """微信公众号文章"""
    platform: str = "wechat"
    title: str = ""
    author: str = ""  # 公众号名称
    content: str = ""
    url: str = ""
    publish_time: Optional[str] = None


@dataclass
class ZhihuResult:
    """知乎搜索结果"""
    platform: str = "zhihu"
    title: str = ""
    source: str = ""
    abstract: str = ""
    content: str = ""  # 完整正文（如果获取成功）
    engine: str = ""
    link: Optional[str] = None
    stats: Optional[str] = None
    type: Optional[str] = None  # question/article


@dataclass
class DoubanResult:
    """豆瓣搜索结果"""
    platform: str = "douban"
    title: str = ""
    type: str = ""  # movie/book/review
    rating: Optional[float] = None
    abstract: str = ""
    content: str = ""
    link: Optional[str] = None
    author: Optional[str] = None


@dataclass
class ToutiaoResult:
    """今日头条搜索结果"""
    platform: str = "toutiao"
    title: str = ""
    source: str = ""
    abstract: str = ""
    content: str = ""
    link: Optional[str] = None
    publish_time: Optional[str] = None


@dataclass
class BaijiahaoResult:
    """百家号搜索结果"""
    platform: str = "baijiahao"
    title: str = ""
    author: str = ""
    abstract: str = ""
    content: str = ""
    link: Optional[str] = None


@dataclass
class WeiboResult:
    """微博搜索结果"""
    platform: str = "weibo"
    title: str = ""
    user: str = ""
    content: str = ""
    link: Optional[str] = None
    stats: Optional[str] = None  # 转发/评论/点赞


@dataclass
class BilibiliResult:
    """B站专栏搜索结果"""
    platform: str = "bilibili"
    title: str = ""
    author: str = ""
    abstract: str = ""
    content: str = ""
    link: Optional[str] = None
    video_id: Optional[str] = None


# ============================================================================
# 微信公众号抓取器
# ============================================================================

class WechatFetcher:
    """微信公众号文章抓取器"""
    
    def __init__(self):
        self.ua = UserAgent()
        self.session = requests.Session()
        self._setup_session()
    
    def _setup_session(self):
        """设置请求头"""
        headers = {
            "User-Agent": self.ua.chrome,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }
        self.session.headers.update(headers)
        
        try:
            self.session.get("https://weixin.sogou.com/", timeout=30)
        except Exception:
            pass
    
    def search(self, keyword: str, account: Optional[str] = None) -> List[Dict]:
        """搜索微信公众号文章"""
        search_query = f"{keyword} {account}" if account else keyword
        
        url = "https://weixin.sogou.com/weixin"
        params = {"type": 2, "query": search_query}
        
        resp = self.session.get(url, params=params, timeout=30)
        soup = BeautifulSoup(resp.text, 'lxml')
        
        results = []
        articles = soup.select('.news-list li')
        
        for article in articles:
            try:
                title_elem = article.select_one('h3 a')
                summary_elem = article.select_one('p')
                account_elem = article.select_one('.account')
                link_elem = article.select_one('h3 a')
                
                if title_elem:
                    link = link_elem.get('href', '') if link_elem else ""
                    if link.startswith('/'):
                        link = "https://weixin.sogou.com" + link
                    
                    results.append({
                        "title": title_elem.text.strip(),
                        "summary": summary_elem.text.strip() if summary_elem else "",
                        "account": account_elem.text.strip() if account_elem else "",
                        "link": link
                    })
            except Exception:
                continue
        
        return results
    
    def _extract_wechat_url_from_js(self, sogou_url: str) -> Optional[str]:
        """从搜狗链接的JavaScript重定向中提取真实的微信文章链接"""
        resp = self.session.get(sogou_url, timeout=30, allow_redirects=True)
        
        if 'antispider' in resp.url:
            return None
        
        # 匹配所有 url += '内容' 并拼接
        pattern = r"url \+= '([^']+)'"
        matches = re.findall(pattern, resp.text)
        
        if matches:
            wechat_url = ''.join(matches)
            if 'mp.weixin.qq.com' in wechat_url:
                return wechat_url
        
        # 备用方案
        pattern2 = r"(https://mp\.weixin\.qq\.com/s\?[^'\"<>\s]+)"
        matches2 = re.findall(pattern2, resp.text)
        if matches2:
            return matches2[0]
        
        return None
    
    def fetch_article(self, url: str) -> Optional[WechatArticle]:
        """获取微信公众号文章内容"""
        wechat_url = url
        
        if 'weixin.sogou.com' in url:
            wechat_url = self._extract_wechat_url_from_js(url)
            if not wechat_url:
                return None
        
        resp = self.session.get(wechat_url, timeout=30)
        
        if resp.status_code != 200:
            return None
        
        soup = BeautifulSoup(resp.text, 'lxml')
        
        title_elem = soup.select_one('#activity-name')
        title = title_elem.text.strip() if title_elem else "未知标题"
        
        author_elem = soup.select_one('#js_name')
        author = author_elem.text.strip() if author_elem else "未知公众号"
        
        time_elem = soup.select_one('#publish_time')
        publish_time = time_elem.text.strip() if time_elem else None
        
        content_elem = soup.select_one('#js_content')
        if not content_elem:
            return None
        
        paragraphs = content_elem.find_all(['p', 'section'])
        content_lines = []
        for p in paragraphs:
            text = p.get_text(strip=True)
            if len(text) > 3:
                content_lines.append(text)
        
        content = '\n\n'.join(content_lines)
        
        return WechatArticle(
            title=title,
            author=author,
            content=content,
            url=wechat_url,
            publish_time=publish_time
        )
    
    def fetch(self, keyword: str, account: Optional[str] = None, limit: int = 3, retry: bool = True) -> List[WechatArticle]:
        """搜索并获取多篇文章
        
        Args:
            keyword: 搜索关键词
            account: 公众号名称（可选）
            limit: 结果数量限制
            retry: 是否在失败时自动重试（默认True）
        """
        print(f"  正在搜索微信公众号: {keyword}")
        results = self.search(keyword, account)
        
        if not results:
            if retry:
                print("  未找到微信文章，10秒后自动重试...")
                time.sleep(10)
                print(f"  重试搜索微信公众号: {keyword}")
                results = self.search(keyword, account)
                if not results:
                    print("  重试后仍未找到微信文章")
                    return []
            else:
                print("  未找到微信文章")
                return []
        
        articles = []
        for i, r in enumerate(results[:limit]):
            print(f"  [{i+1}/{min(limit, len(results))}] 获取: {r['title'][:30]}...")
            article = self.fetch_article(r['link'])
            if article:
                articles.append(article)
            time.sleep(1)  # 避免频繁请求
        
        return articles


# ============================================================================
# 知乎内容抓取器
# ============================================================================

class ZhihuFetcher:
    """知乎内容抓取器 - 支持获取完整内容"""
    
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }
        self._last_request_time = 0
    
    def _request(self, url: str, params: dict = None, delay: float = 1.0, 
                 headers: dict = None) -> Optional[requests.Response]:
        """带延迟的请求"""
        elapsed = time.time() - self._last_request_time
        if elapsed < delay:
            time.sleep(delay - elapsed)
        
        try:
            h = headers or self.headers
            resp = self.session.get(url, params=params, headers=h, timeout=15)
            resp.encoding = 'utf-8'
            self._last_request_time = time.time()
            return resp
        except Exception as e:
            print(f"  请求失败: {e}", file=sys.stderr)
            return None
    
    def _extract_stats(self, text: str) -> str:
        """提取统计数据"""
        patterns = [
            r'(\d+)\s*个回答',
            r'(\d+)\s*人关注',
            r'(\d+(?:\.\d+)?[万亿]?)\s*次浏览',
        ]
        stats = []
        for p in patterns:
            match = re.search(p, text)
            if match:
                stats.append(match.group(0))
        return ' | '.join(stats) if stats else ''
    
    def _get_real_zhihu_url(self, sogou_link: str) -> Optional[str]:
        """从搜狗链接获取真实知乎 URL"""
        if not sogou_link.startswith('https://www.sogou.com/link'):
            sogou_link = 'https://www.sogou.com' + sogou_link if sogou_link.startswith('/') else sogou_link
        
        resp = self._request(sogou_link, delay=0.5)
        if not resp or resp.status_code != 200:
            return None
        
        # 从 JavaScript 重定向提取真实 URL
        match = re.search(r'window\.location\.replace\("([^"]+)"\)', resp.text)
        if match:
            return match.group(1)
        
        return None
    
    # ========================================
    # 知乎日报获取（完整正文）
    # ========================================
    
    def _search_daily_history(self, keyword: str, days: int = 30) -> List[Dict]:
        """搜索知乎日报历史内容"""
        from datetime import datetime, timedelta
        
        results = []
        
        for i in range(days):
            date = (datetime.now() - timedelta(days=i)).strftime("%Y%m%d")
            
            if i == 0:
                api = "https://news-at.zhihu.com/api/4/news/latest"
            else:
                api = f"https://news-at.zhihu.com/api/4/news/before/{date}"
            
            try:
                resp = self._request(api, delay=0.3)
                if resp and resp.status_code == 200:
                    data = resp.json()
                    stories = data.get('stories', [])
                    
                    for s in stories:
                        title = s.get('title', '')
                        # 关键词匹配
                        if keyword.lower() in title.lower():
                            story_id = s.get('url', '').split('/')[-1] or str(s.get('id', ''))
                            results.append({
                                'daily_id': story_id,
                                'title': title,
                                'hint': s.get('hint', ''),
                                'date': date,
                            })
                
                if len(results) >= 5:
                    break
            except Exception:
                continue
        
        return results
    
    def _fetch_daily_content(self, daily_id: str) -> Optional[Dict]:
        """获取知乎日报文章详情（包含完整正文）"""
        api = f"https://news-at.zhihu.com/api/4/news/{daily_id}"
        
        resp = self._request(api, delay=0.5)
        if not resp or resp.status_code != 200:
            return None
        
        try:
            data = resp.json()
            body = data.get('body', '')
            
            if not body:
                return None
            
            # 提取完整正文
            soup = BeautifulSoup(body, 'lxml')
            text = soup.get_text(strip=True)
            
            # 提取知乎原文链接
            zhihu_url = ''
            zhihu_question_id = ''
            zhihu_answer_id = ''
            
            for a in soup.find_all('a', href=True):
                href = a.get('href', '')
                if 'zhihu.com' in href:
                    q_match = re.search(r'question/(\d+)', href)
                    a_match = re.search(r'answer/(\d+)', href)
                    
                    if q_match:
                        zhihu_question_id = q_match.group(1)
                        zhihu_url = href
                    if a_match:
                        zhihu_answer_id = a_match.group(1)
            
            return {
                'title': data.get('title', ''),
                'content': text,
                'zhihu_url': zhihu_url,
                'zhihu_question_id': zhihu_question_id,
                'zhihu_answer_id': zhihu_answer_id,
                'daily_url': f"https://daily.zhihu.com/story/{daily_id}",
            }
        except Exception:
            return None
    
    def fetch_via_daily(self, keyword: str, limit: int) -> List[ZhihuResult]:
        """通过知乎日报获取完整内容"""
        print("    尝试知乎日报获取...")
        
        results = []
        
        # 搜索日报历史
        daily_stories = self._search_daily_history(keyword, days=30)
        
        if not daily_stories:
            print("    日报中未找到相关内容")
            return []
        
        print(f"    日报找到 {len(daily_stories)} 条")
        
        for story in daily_stories[:limit]:
            daily_id = story['daily_id']
            
            # 获取完整内容
            content_data = self._fetch_daily_content(daily_id)
            
            if content_data and content_data.get('content'):
                print(f"    ✓ 日报获取成功: {len(content_data['content'])}字")
                
                results.append(ZhihuResult(
                    platform='zhihu',
                    title=content_data['title'] or story['title'],
                    source='知乎日报',
                    abstract='',
                    content=content_data['content'],
                    engine='daily',
                    link=content_data['zhihu_url'] or content_data['daily_url'],
                    stats=story.get('hint', ''),
                    type='daily',
                ))
        
        return results
    
    def fetch_sogou(self, keyword: str, limit: int) -> List[ZhihuResult]:
        """搜狗搜索知乎"""
        url = "https://www.sogou.com/web"
        params = {'query': f"{keyword} site:zhihu.com"}
        
        resp = self._request(url, params)
        if not resp:
            return []
        
        soup = BeautifulSoup(resp.text, 'lxml')
        results = []
        
        for div in soup.find_all(['div', 'li'], class_=re.compile(r'vrwrap|rb|result|res-list')):
            result = self._parse_sogou_result(div)
            if result:
                results.append(result)
                if len(results) >= limit:
                    break
        
        return results
    
    def _parse_sogou_result(self, div) -> Optional[ZhihuResult]:
        """解析搜狗结果"""
        title_tag = div.find('h3') or div.find('a', class_=re.compile(r'vr-title'))
        if not title_tag:
            return None
        
        title = title_tag.get_text(strip=True)
        
        if title.startswith('找到') and '条结果' in title:
            return None
        
        link = title_tag.find('a') if title_tag.name != 'a' else title_tag
        href = link.get('href', '') if link else ''
        
        abstract = ''
        p_tags = div.find_all('p')
        for p in p_tags:
            text = p.get_text(strip=True)
            if len(text) > 30 and 'function' not in text[:20]:
                abstract = text
                break
        
        stats = self._extract_stats(abstract or title)
        source = '知乎' if 'zhihu' in title.lower() or '知乎' in title else '未知'
        
        if title and len(title) > 5:
            return ZhihuResult(
                title=title[:100],
                source=source,
                abstract=abstract[:500] if abstract else stats,
                engine='sogou',
                link=href,
                stats=stats
            )
        
        return None
    
    def fetch_360(self, keyword: str, limit: int) -> List[ZhihuResult]:
        """360搜索知乎"""
        url = "https://www.so.com/s"
        params = {'q': f"{keyword} site:zhihu.com"}
        
        resp = self._request(url, params)
        if not resp:
            return []
        
        soup = BeautifulSoup(resp.text, 'lxml')
        results = []
        
        for li in soup.find_all('li', class_='res-list'):
            h3 = li.find('h3')
            if not h3:
                continue
            
            title = h3.get_text(strip=True)
            abstract = ''
            p = li.find('p', class_='res-desc')
            if p:
                abstract = p.get_text(strip=True)
            
            stats = self._extract_stats(abstract or title)
            
            results.append(ZhihuResult(
                title=title[:100],
                source='知乎' if 'zhihu' in title.lower() else '未知',
                abstract=abstract[:500] if abstract else stats,
                engine='360',
                stats=stats
            ))
            
            if len(results) >= limit:
                break
        
        return results
    
    def fetch_bing(self, keyword: str, limit: int) -> List[ZhihuResult]:
        """Bing搜索知乎"""
        url = "https://cn.bing.com/search"
        params = {'q': f"{keyword} site:zhihu.com"}
        
        resp = self._request(url, params)
        if not resp:
            return []
        
        soup = BeautifulSoup(resp.text, 'lxml')
        results = []
        
        for li in soup.find_all('li', class_='b_algo'):
            h2 = li.find('h2')
            if not h2:
                continue
            
            title = h2.get_text(strip=True)
            abstract = ''
            p = li.find('p')
            if p:
                abstract = p.get_text(strip=True)
            
            if not abstract:
                caption = li.find('div', class_='b_caption')
                if caption:
                    abstract = caption.get_text(strip=True)
            
            stats = self._extract_stats(abstract or title)
            
            results.append(ZhihuResult(
                title=title[:100],
                source='知乎' if 'zhihu' in title.lower() else '未知',
                abstract=abstract[:500] if abstract else stats,
                engine='bing',
                stats=stats
            ))
            
            if len(results) >= limit:
                break
        
        return results
    
    def fetch_sogou_with_full_link(self, keyword: str, limit: int) -> List[ZhihuResult]:
        """搜狗搜索知乎并获取真实链接"""
        url = "https://www.sogou.com/web"
        params = {'query': f"{keyword} site:zhihu.com"}
        
        resp = self._request(url, params, delay=1.0)
        if not resp:
            return []
        
        soup = BeautifulSoup(resp.text, 'lxml')
        results = []
        seen = set()
        
        # 提取搜狗结果
        for vrwrap in soup.find_all('div', class_='vrwrap'):
            title_elem = vrwrap.find('h3')
            if not title_elem:
                continue
            
            title = title_elem.get_text(strip=True)
            
            # 只处理知乎相关
            if '知乎' not in title and 'zhihu' not in title.lower():
                continue
            
            # 去重
            key = title[:40]
            if key in seen:
                continue
            seen.add(key)
            
            # 提取摘要 - 找最长段落
            abstracts = []
            for p in vrwrap.find_all(['p', 'div']):
                text = p.get_text(strip=True)
                if len(text) > 20 and text != title:
                    abstracts.append(text)
            
            abstract = max(abstracts, key=len) if abstracts else ''
            
            # 提取搜狗链接
            a_tag = title_elem.find('a') if title_elem.name != 'a' else title_elem
            sogou_link = a_tag.get('href', '') if a_tag else ''
            
            if not sogou_link:
                continue
            
            print(f"    找到: {title[:40]}...")
            
            # 获取真实知乎 URL
            real_url = self._get_real_zhihu_url(sogou_link)
            
            if real_url:
                print(f"    真实链接: {real_url}")
                link = real_url
                engine = 'sogou'
            else:
                link = sogou_link
                engine = 'sogou'
            
            # 提取统计数据
            stats = self._extract_stats(abstract or title)
            
            results.append(ZhihuResult(
                title=title,
                source='知乎',
                abstract=abstract[:500] if abstract else '',
                content='',  # 知乎无法获取完整正文
                engine=engine,
                link=link,
                stats=stats,
                type='unknown'
            ))
            
            if len(results) >= limit:
                break
        
        return results
    
    def fetch(self, keyword: str, limit: int = 3) -> List[ZhihuResult]:
        """搜索知乎内容（优先获取完整正文）"""
        print(f"  正在搜索知乎: {keyword}")
        
        results = []
        
        # 1. 优先尝试知乎日报获取完整内容
        daily_results = self.fetch_via_daily(keyword, limit)
        
        if daily_results:
            results.extend(daily_results)
            
            if len(results) >= limit:
                return results[:limit]
        
        # 2. 补充搜狗搜索摘要
        print("    补充搜狗搜索...")
        sogou_results = self.fetch_sogou_with_full_link(keyword, limit - len(results))
        
        seen_titles = set(r.title[:30] for r in results)
        
        for r in sogou_results:
            key = r.title[:30]
            if key not in seen_titles:
                seen_titles.add(key)
                results.append(r)
                if len(results) >= limit:
                    return results[:limit]
        
        # 3. 如果仍然不足，补充其他搜索引擎
        for fetcher in [self.fetch_360, self.fetch_bing]:
            try:
                for r in fetcher(keyword, limit - len(results)):
                    key = r.title[:30]
                    if key not in seen_titles:
                        seen_titles.add(key)
                        results.append(r)
                        if len(results) >= limit:
                            return results[:limit]
            except Exception as e:
                print(f"    补充搜索失败: {e}", file=sys.stderr)
        
        return results[:limit]


# ============================================================================
# 豆瓣内容抓取器
# ============================================================================

class DoubanFetcher:
    """豆瓣内容抓取器 - 影评/书评（使用官方API）"""
    
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Cookie': 'll="118281"; bid=test',
        }
        self._last_request_time = 0
    
    def _request(self, url: str, params: dict = None, delay: float = 1.0) -> Optional[requests.Response]:
        elapsed = time.time() - self._last_request_time
        if elapsed < delay:
            time.sleep(delay - elapsed)
        
        try:
            resp = self.session.get(url, params=params, headers=self.headers, timeout=15)
            self._last_request_time = time.time()
            return resp
        except:
            return None
    
    def search_movie(self, keyword: str, limit: int) -> List[DoubanResult]:
        """搜索豆瓣电影"""
        url = "https://movie.douban.com/j/search_subjects"
        params = {
            'type': 'movie',
            'tag': keyword,
            'sort': 'recommend',
            'page_limit': limit,
            'page_start': 0
        }
        
        resp = self._request(url, params)
        if not resp:
            return []
        
        try:
            data = resp.json()
            subjects = data.get('subjects', [])
            results = []
            
            for s in subjects:
                results.append(DoubanResult(
                    platform='douban',
                    title=s.get('title', ''),
                    type='movie',
                    rating=float(s.get('rate', 0)) if s.get('rate') else None,
                    abstract='',
                    content='',
                    link=s.get('url', ''),
                ))
            
            return results
        except:
            return []
    
    def fetch(self, keyword: str, limit: int = 3) -> List[DoubanResult]:
        """搜索豆瓣内容"""
        print(f"  正在搜索豆瓣: {keyword}")
        
        results = self.search_movie(keyword, limit)
        
        print(f"    找到 {len(results)} 条")
        
        return results[:limit]


# ============================================================================
# 今日头条抓取器
# ============================================================================

class ToutiaoFetcher:
    """今日头条内容抓取器 - 通过搜索引擎获取摘要"""
    
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        }
        self._last_request_time = 0
    
    def _request(self, url: str, params: dict = None, delay: float = 1.0) -> Optional[requests.Response]:
        elapsed = time.time() - self._last_request_time
        if elapsed < delay:
            time.sleep(delay - elapsed)
        
        try:
            resp = self.session.get(url, params=params, headers=self.headers, timeout=15)
            resp.encoding = 'utf-8'
            self._last_request_time = time.time()
            return resp
        except:
            return None
    
    def search_360(self, keyword: str, limit: int) -> List[ToutiaoResult]:
        """通过360搜索今日头条"""
        url = "https://www.so.com/s"
        params = {'q': f"{keyword} site:toutiao.com"}
        
        resp = self._request(url, params)
        if not resp:
            return []
        
        soup = BeautifulSoup(resp.text, 'lxml')
        results = []
        
        for li in soup.find_all('li', class_='res-list')[:limit]:
            h3 = li.find('h3')
            if not h3:
                continue
            
            title = h3.get_text(strip=True)
            
            if '头条' not in title and 'toutiao' not in title.lower():
                continue
            
            # 提取摘要
            p = li.find('p', class_='res-desc')
            abstract = p.get_text(strip=True)[:200] if p else ''
            
            # 提取链接
            a = h3.find('a')
            link = a.get('href', '') if a else ''
            
            results.append(ToutiaoResult(
                platform='toutiao',
                title=title[:100],
                source='今日头条',
                abstract=abstract,
                content='',
                link=link,
            ))
        
        return results
    
    def fetch(self, keyword: str, limit: int = 3) -> List[ToutiaoResult]:
        """搜索今日头条内容"""
        print(f"  正在搜索今日头条: {keyword}")
        
        results = self.search_360(keyword, limit)
        
        print(f"    找到 {len(results)} 条")
        
        return results[:limit]


# ============================================================================
# 百家号抓取器
# ============================================================================

class BaijiahaoFetcher:
    """百家号内容抓取器 - 通过360搜索获取摘要"""
    
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        }
        self._last_request_time = 0
    
    def _request(self, url: str, params: dict = None, delay: float = 1.0) -> Optional[requests.Response]:
        elapsed = time.time() - self._last_request_time
        if elapsed < delay:
            time.sleep(delay - elapsed)
        
        try:
            resp = self.session.get(url, params=params, headers=self.headers, timeout=15)
            resp.encoding = 'utf-8'
            self._last_request_time = time.time()
            return resp
        except:
            return None
    
    def search_360(self, keyword: str, limit: int) -> List[BaijiahaoResult]:
        """通过360搜索百家号"""
        url = "https://www.so.com/s"
        params = {'q': f"{keyword}百家号"}
        
        resp = self._request(url, params)
        if not resp:
            return []
        
        soup = BeautifulSoup(resp.text, 'lxml')
        results = []
        
        for li in soup.find_all('li', class_='res-list')[:limit]:
            h3 = li.find('h3')
            if not h3:
                continue
            
            title = h3.get_text(strip=True)
            
            # 提取摘要
            p = li.find('p', class_='res-desc')
            abstract = p.get_text(strip=True)[:200] if p else ''
            
            # 提取链接
            a = h3.find('a')
            link = a.get('href', '') if a else ''
            
            # 提取作者
            cite = li.find('cite')
            author = cite.get_text(strip=True) if cite else ''
            
            results.append(BaijiahaoResult(
                platform='baijiahao',
                title=title[:100],
                author=author,
                abstract=abstract,
                content='',
                link=link,
            ))
        
        return results
    
    def fetch(self, keyword: str, limit: int = 3) -> List[BaijiahaoResult]:
        """搜索百家号内容"""
        print(f"  正在搜索百家号: {keyword}")
        
        results = self.search_360(keyword, limit)
        
        print(f"    找到 {len(results)} 条")
        
        return results[:limit]


# ============================================================================
# 微博抓取器
# ============================================================================

class WeiboFetcher:
    """微博内容抓取器 - 通过360搜索获取摘要"""
    
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        }
        self._last_request_time = 0
    
    def _request(self, url: str, params: dict = None, delay: float = 1.0) -> Optional[requests.Response]:
        elapsed = time.time() - self._last_request_time
        if elapsed < delay:
            time.sleep(delay - elapsed)
        
        try:
            resp = self.session.get(url, params=params, headers=self.headers, timeout=15)
            resp.encoding = 'utf-8'
            self._last_request_time = time.time()
            return resp
        except:
            return None
    
    def search_360(self, keyword: str, limit: int) -> List[WeiboResult]:
        """通过360搜索微博"""
        url = "https://www.so.com/s"
        params = {'q': f"{keyword}微博"}
        
        resp = self._request(url, params)
        if not resp:
            return []
        
        soup = BeautifulSoup(resp.text, 'lxml')
        results = []
        
        for li in soup.find_all('li', class_='res-list')[:limit]:
            h3 = li.find('h3')
            if not h3:
                continue
            
            title = h3.get_text(strip=True)
            
            if '微博' not in title and 'weibo' not in title.lower():
                continue
            
            # 提取摘要
            p = li.find('p', class_='res-desc')
            content = p.get_text(strip=True)[:200] if p else ''
            
            # 提取用户名
            user_match = re.search(r'来自\s*(\S+)', title) or re.search(r'@(\w+)', content)
            user = user_match.group(1) if user_match else ''
            
            # 提取链接
            a = h3.find('a')
            link = a.get('href', '') if a else ''
            
            results.append(WeiboResult(
                platform='weibo',
                title=title[:100],
                user=user,
                content=content,
                link=link,
            ))
        
        return results
    
    def fetch(self, keyword: str, limit: int = 3) -> List[WeiboResult]:
        """搜索微博内容"""
        print(f"  正在搜索微博: {keyword}")
        
        results = self.search_360(keyword, limit)
        
        print(f"    找到 {len(results)} 条")
        
        return results[:limit]


# ============================================================================
# B站专栏抓取器
# ============================================================================

class BilibiliFetcher:
    """B站专栏内容抓取器 - 通过360搜索获取摘要"""
    
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        }
        self._last_request_time = 0
    
    def _request(self, url: str, params: dict = None, delay: float = 1.0) -> Optional[requests.Response]:
        elapsed = time.time() - self._last_request_time
        if elapsed < delay:
            time.sleep(delay - elapsed)
        
        try:
            resp = self.session.get(url, params=params, headers=self.headers, timeout=15)
            resp.encoding = 'utf-8'
            self._last_request_time = time.time()
            return resp
        except:
            return None
    
    def search_360(self, keyword: str, limit: int) -> List[BilibiliResult]:
        """通过360搜索B站专栏"""
        url = "https://www.so.com/s"
        params = {'q': f"{keyword}哔哩哔哩bilibili"}
        
        resp = self._request(url, params)
        if not resp:
            return []
        
        soup = BeautifulSoup(resp.text, 'lxml')
        results = []
        
        for li in soup.find_all('li', class_='res-list')[:limit]:
            h3 = li.find('h3')
            if not h3:
                continue
            
            title = h3.get_text(strip=True)
            
            # 提取摘要
            p = li.find('p', class_='res-desc')
            abstract = p.get_text(strip=True)[:200] if p else ''
            
            # 提取链接
            a = h3.find('a')
            link = a.get('href', '') if a else ''
            
            # 提取作者
            cite = li.find('cite')
            author = cite.get_text(strip=True) if cite else ''
            
            results.append(BilibiliResult(
                platform='bilibili',
                title=title[:100],
                author=author,
                abstract=abstract,
                content='',
                link=link,
                video_id='',
            ))
        
        return results
    
    def fetch(self, keyword: str, limit: int = 3) -> List[BilibiliResult]:
        """搜索B站专栏内容"""
        print(f"  正在搜索B站专栏: {keyword}")
        
        results = self.search_360(keyword, limit)
        
        print(f"    找到 {len(results)} 条")
        
        return results[:limit]


# ============================================================================
# 综合搜索器
# ============================================================================

class DeepSearcher:
    """深度内容搜索器"""
    
    def __init__(self):
        self.wechat = WechatFetcher()
        self.zhihu = ZhihuFetcher()
        self.douban = DoubanFetcher()
        self.toutiao = ToutiaoFetcher()
        self.baijiahao = BaijiahaoFetcher()
        self.weibo = WeiboFetcher()
        self.bilibili = BilibiliFetcher()
    
    def search(self, keyword: str, source: str = "all", limit: int = 3, 
               account: Optional[str] = None) -> Dict:
        """
        综合搜索
        
        Args:
            keyword: 搜索关键词
            source: 平台选择 (wechat/zhihu/douban/toutiao/baijiahao/weibo/bilibili/all)
            limit: 每平台结果数量
            account: 微信公众号名称
        
        Returns:
            {
                "keyword": str,
                "total": int,
                "results": [...]
            }
        """
        results = []
        
        # 支持的平台列表
        platforms = {
            'wechat': self.wechat,
            'zhihu': self.zhihu,
            'douban': self.douban,
            'toutiao': self.toutiao,
            'baijiahao': self.baijiahao,
            'weibo': self.weibo,
            'bilibili': self.bilibili,
        }
        
        if source == "all":
            # 综合搜索所有平台
            for platform_name, fetcher in platforms.items():
                try:
                    platform_results = fetcher.fetch(keyword, limit)
                    results.extend(platform_results)
                except Exception as e:
                    print(f"  {platform_name}搜索失败: {e}")
        elif source in platforms:
            # 单平台搜索
            fetcher = platforms[source]
            try:
                if source == 'wechat' and account:
                    platform_results = fetcher.fetch(keyword, account, limit)
                else:
                    platform_results = fetcher.fetch(keyword, limit)
                results.extend(platform_results)
            except Exception as e:
                print(f"  {source}搜索失败: {e}")
        
        return {
            "keyword": keyword,
            "total": len(results),
            "results": results
        }


# ============================================================================
# 输出格式化
# ============================================================================

def format_output(data: Dict, json_output: bool = False) -> str:
    """格式化输出"""
    if json_output:
        # 转换为可序列化格式
        results = []
        for r in data["results"]:
            if hasattr(r, '__dataclass_fields__'):
                results.append(asdict(r))
            else:
                results.append(r)
        
        output = {
            "keyword": data["keyword"],
            "total": data["total"],
            "results": results
        }
        return json.dumps(output, ensure_ascii=False, indent=2)
    
    # 文本格式
    lines = []
    lines.append(f"\n{'='*70}")
    lines.append(f"搜索关键词: {data['keyword']}")
    lines.append(f"共找到 {data['total']} 条内容")
    lines.append(f"{'='*70}")
    
    platform_icons = {
        'wechat': '📱',
        'zhihu': '📘',
        'douban': '🎬',
        'toutiao': '📰',
        'baijiahao': '📝',
        'weibo': '💬',
        'bilibili': '📺',
    }
    
    platform_names = {
        'wechat': '微信公众号',
        'zhihu': '知乎',
        'douban': '豆瓣',
        'toutiao': '今日头条',
        'baijiahao': '百家号',
        'weibo': '微博',
        'bilibili': 'B站专栏',
    }
    
    # 各渠道条数汇总表
    lines.append("\n📊 各渠道检索结果:")
    lines.append("-" * 50)
    for platform in ['wechat', 'zhihu', 'douban', 'toutiao', 'baijiahao', 'weibo', 'bilibili']:
        platform_results = [r for r in data["results"] if getattr(r, 'platform', None) == platform]
        icon = platform_icons.get(platform, '📄')
        name = platform_names.get(platform, platform)
        count = len(platform_results)
        status = f"✅ {count}条" if count > 0 else "❌ 0条"
        lines.append(f"  {icon} {name}: {status}")
    lines.append("-" * 50)
    
    # 按平台分组
    for platform in ['wechat', 'zhihu', 'douban', 'toutiao', 'baijiahao', 'weibo', 'bilibili']:
        platform_results = [r for r in data["results"] if getattr(r, 'platform', None) == platform]
        
        if platform_results:
            icon = platform_icons.get(platform, '📄')
            name = platform_names.get(platform, platform)
            lines.append(f"\n{icon}【{name}】({len(platform_results)}条)")
            lines.append("-" * 70)
            
            for i, r in enumerate(platform_results, 1):
                lines.append(f"\n[{i}] {r.title[:60]}")
                
                # 根据平台类型提取不同字段
                if platform == 'wechat':
                    lines.append(f"    公众号: {getattr(r, 'author', 'N/A')}")
                    if getattr(r, 'content', ''):
                        content_preview = r.content[:150] + "..." if len(r.content) > 150 else r.content
                        lines.append(f"    正文: {content_preview}")
                    lines.append(f"    链接: {getattr(r, 'url', 'N/A')}")
                
                elif platform == 'zhihu':
                    if getattr(r, 'stats', ''):
                        lines.append(f"    统计: {r.stats}")
                    lines.append(f"    来源: {getattr(r, 'source', 'N/A')} | {getattr(r, 'engine', 'N/A')}")
                    if getattr(r, 'abstract', ''):
                        lines.append(f"    摘要: {r.abstract[:100]}...")
                
                elif platform == 'douban':
                    if getattr(r, 'rating', None):
                        lines.append(f"    评分: {r.rating}")
                    lines.append(f"    类型: {getattr(r, 'type', 'N/A')}")
                    lines.append(f"    链接: {getattr(r, 'link', 'N/A')}")
                
                elif platform == 'toutiao':
                    if getattr(r, 'abstract', ''):
                        lines.append(f"    摘要: {r.abstract[:100]}...")
                    lines.append(f"    链接: {getattr(r, 'link', 'N/A')}")
                
                elif platform == 'baijiahao':
                    if getattr(r, 'author', ''):
                        lines.append(f"    作者: {r.author}")
                    if getattr(r, 'abstract', ''):
                        lines.append(f"    摘要: {r.abstract[:100]}...")
                
                elif platform == 'weibo':
                    if getattr(r, 'user', ''):
                        lines.append(f"    用户: @{r.user}")
                    if getattr(r, 'content', ''):
                        lines.append(f"    内容: {r.content[:100]}...")
                
                elif platform == 'bilibili':
                    if getattr(r, 'abstract', ''):
                        lines.append(f"    摘要: {r.abstract[:100]}...")
                    lines.append(f"    链接: {getattr(r, 'link', 'N/A')}")
    
    lines.append(f"\n{'='*70}")
    lines.append(f"✅ 搜索完成")
    
    return '\n'.join(lines)


# ============================================================================
# 主程序
# ============================================================================

def is_wechat_url(text: str) -> bool:
    """检测是否为微信公众号链接"""
    return 'mp.weixin.qq.com' in text and ('/s' in text or '/s?' in text)


def fetch_wechat_url(url: str, json_output: bool = False) -> str:
    """直接获取微信公众号文章内容"""
    print(f"📱 直接解析微信链接: {url}")
    
    fetcher = WechatFetcher()
    article = fetcher.fetch_article(url)
    
    if not article:
        return "❌ 获取失败，可能链接已失效或被限制访问"
    
    if json_output:
        result = asdict(article)
        result['word_count'] = len(article.content)
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    # 文本格式
    lines = []
    lines.append(f"\n{'='*70}")
    lines.append(f"📱 微信公众号文章")
    lines.append(f"{'='*70}")
    lines.append(f"标题: {article.title}")
    lines.append(f"公众号: {article.author}")
    if article.publish_time:
        lines.append(f"发布时间: {article.publish_time}")
    lines.append(f"字数: {len(article.content)}")
    lines.append(f"链接: {article.url}")
    lines.append(f"\n{'-'*70}")
    lines.append(f"正文内容:")
    lines.append(f"{'-'*70}")
    lines.append(article.content)
    lines.append(f"\n{'='*70}")
    lines.append(f"✅ 获取完成")
    
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='深度内容搜索工具 - 整合微信公众号和知乎内容抓取',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 综合搜索（所有平台），默认3条
  python3 deep_search.py "OpenClaw教程"
  
  # 指定结果数量
  python3 deep_search.py "AI人工智能" --limit 5
  
  # 只搜微信公众号
  python3 deep_search.py "大龙虾" --source wechat
  
  # 只搜知乎
  python3 deep_search.py "如何学习编程" --source zhihu
  
  # 只搜豆瓣
  python3 deep_search.py "人工智能电影" --source douban
  
  # 只搜今日头条
  python3 deep_search.py "大模型" --source toutiao
  
  # 只搜百家号
  python3 deep_search.py "OpenClaw" --source baijiahao
  
  # 只搜微博
  python3 deep_search.py "大模型" --source weibo
  
  # 只搜B站专栏
  python3 deep_search.py "AI教程" --source bilibili
  
  # 输出JSON格式
  python3 deep_search.py "OpenClaw" --json
  
  # 指定公众号
  python3 deep_search.py "OpenClaw教程" --source wechat --account "软件小技"
  
  # 直接解析微信链接（自动检测）
  python3 deep_search.py "https://mp.weixin.qq.com/s/xxx"
"""
    )
    
    parser.add_argument('keyword', help='搜索关键词或微信链接')
    parser.add_argument('-s', '--source', 
                        choices=['wechat', 'zhihu', 'douban', 'toutiao', 'baijiahao', 'weibo', 'bilibili', 'all'], 
                        default='all', 
                        help='搜索平台: wechat/zhihu/douban/toutiao/baijiahao/weibo/bilibili/all (默认: all)')
    parser.add_argument('-l', '--limit', type=int, default=3, 
                        help='每平台结果数量 (默认: 3)')
    parser.add_argument('-a', '--account', help='微信公众号名称')
    parser.add_argument('-j', '--json', action='store_true', help='输出JSON格式')
    parser.add_argument('-o', '--output', help='输出文件路径')
    
    args = parser.parse_args()
    
    # 检测是否为微信链接
    if is_wechat_url(args.keyword):
        output = fetch_wechat_url(args.keyword, json_output=args.json)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"\n✅ 已保存到: {args.output}")
        else:
            print(output)
        return
    
    # 正常搜索流程
    print(f"🔍 深度搜索: {args.keyword}")
    print(f"   来源: {args.source} | 每平台条数: {args.limit}")
    
    searcher = DeepSearcher()
    data = searcher.search(
        keyword=args.keyword,
        source=args.source,
        limit=args.limit,
        account=args.account
    )
    
    output = format_output(data, json_output=args.json)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"\n✅ 已保存到: {args.output}")
    else:
        print(output)


if __name__ == '__main__':
    main()