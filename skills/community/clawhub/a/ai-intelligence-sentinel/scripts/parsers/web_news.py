#!/usr/bin/env python3
"""
网页新闻解析器
用于解析中国AI公司官网的新闻页面（无RSS的情况）
支持：智谱AI、MiniMax、扣子Coze等
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass
import logging
import time
import re

logger = logging.getLogger(__name__)


@dataclass
class WebNewsItem:
    """网页新闻条目"""
    title: str
    url: str
    source: str
    company: str
    summary: str = ""
    published_date: Optional[datetime] = None
    category: str = ""
    
    def to_dict(self) -> Dict:
        """转换为字典格式"""
        return {
            'title': self.title,
            'url': self.url,
            'source': self.source,
            'company': self.company,
            'summary': self.summary,
            'published_date': self.published_date.isoformat() if self.published_date else None,
            'category': self.category,
            'source_type': 'web_news'
        }


class WebNewsParser:
    """网页新闻解析器"""
    
    # 请求配置
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    TIMEOUT = 15
    RETRY_COUNT = 2
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)
    
    def fetch_page(self, url: str) -> Optional[str]:
        """获取网页内容"""
        for attempt in range(self.RETRY_COUNT):
            try:
                response = self.session.get(url, timeout=self.TIMEOUT)
                response.raise_for_status()
                response.encoding = response.apparent_encoding or 'utf-8'
                return response.text
            except Exception as e:
                logger.warning(f"获取页面失败 (尝试 {attempt+1}/{self.RETRY_COUNT}): {url}, 错误: {e}")
                if attempt < self.RETRY_COUNT - 1:
                    time.sleep(2)
        return None
    
    def parse_zhipu(self, html: str, base_url: str) -> List[WebNewsItem]:
        """解析智谱AI新品发布页面"""
        items = []
        soup = BeautifulSoup(html, 'html.parser')
        
        # 智谱文档页面结构：查找文章列表
        # 通常包含标题、日期等信息
        articles = soup.find_all(['article', 'div'], class_=re.compile(r'(article|post|news|item|release)', re.I))
        
        for article in articles[:10]:  # 限制10条
            try:
                # 尝试提取标题
                title_elem = article.find(['h1', 'h2', 'h3', 'h4', 'a'], class_=re.compile(r'(title|heading)', re.I))
                if not title_elem:
                    title_elem = article.find(['h1', 'h2', 'h3', 'h4'])
                
                if not title_elem:
                    continue
                    
                title = title_elem.get_text(strip=True)
                if not title or len(title) < 5:
                    continue
                
                # 提取链接
                link = article.find('a', href=True)
                url = link['href'] if link else ''
                if url and not url.startswith('http'):
                    url = base_url.rstrip('/') + '/' + url.lstrip('/')
                
                # 提取日期
                date_elem = article.find(['time', 'span', 'div'], class_=re.compile(r'(date|time)', re.I))
                published_date = None
                if date_elem:
                    date_str = date_elem.get_text(strip=True)
                    published_date = self._parse_date(date_str)
                
                # 提取摘要
                summary_elem = article.find(['p', 'div'], class_=re.compile(r'(summary|description|excerpt)', re.I))
                summary = summary_elem.get_text(strip=True)[:200] if summary_elem else ""
                
                items.append(WebNewsItem(
                    title=title,
                    url=url,
                    source="智谱AI新品发布",
                    company="ZhipuAI (智谱)",
                    summary=summary,
                    published_date=published_date,
                    category="AI Company"
                ))
                
            except Exception as e:
                logger.debug(f"解析智谱文章失败: {e}")
                continue
        
        # 如果没找到标准结构，尝试通用解析
        if not items:
            items = self._generic_parse(html, base_url, "智谱AI新品发布", "ZhipuAI (智谱)")
        
        return items
    
    def parse_minimax(self, html: str, base_url: str) -> List[WebNewsItem]:
        """解析MiniMax新闻页面"""
        items = []
        soup = BeautifulSoup(html, 'html.parser')
        
        # MiniMax新闻页面可能是动态渲染的，这里尝试解析HTML结构
        # 查找新闻卡片或列表项
        news_cards = soup.find_all(['div', 'article', 'li'], 
                                    class_=re.compile(r'(news|article|card|item|post)', re.I))
        
        for card in news_cards[:10]:
            try:
                # 提取标题
                title_elem = card.find(['h1', 'h2', 'h3', 'h4', 'a', 'span'])
                if not title_elem:
                    continue
                    
                title = title_elem.get_text(strip=True)
                if not title or len(title) < 5:
                    continue
                
                # 提取链接
                link = card.find('a', href=True)
                url = link['href'] if link else ''
                if url and not url.startswith('http'):
                    url = base_url.rstrip('/') + '/' + url.lstrip('/')
                
                # 提取日期
                date_elem = card.find(['time', 'span'], class_=re.compile(r'(date|time)', re.I))
                published_date = None
                if date_elem:
                    date_str = date_elem.get_text(strip=True)
                    published_date = self._parse_date(date_str)
                
                items.append(WebNewsItem(
                    title=title,
                    url=url or base_url,
                    source="MiniMax新闻动态",
                    company="MiniMax",
                    summary="",
                    published_date=published_date,
                    category="AI Company"
                ))
                
            except Exception as e:
                logger.debug(f"解析MiniMax文章失败: {e}")
                continue
        
        # 如果没找到标准结构，尝试通用解析
        if not items:
            items = self._generic_parse(html, base_url, "MiniMax新闻动态", "MiniMax")
        
        return items
    
    def parse_coze(self, html: str, base_url: str) -> List[WebNewsItem]:
        """解析扣子Coze文档页面"""
        items = []
        soup = BeautifulSoup(html, 'html.parser')
        
        # Coze文档页面结构
        # 查找更新日志、公告等
        updates = soup.find_all(['div', 'section', 'article'], 
                                class_=re.compile(r'(update|release|changelog|announcement)', re.I))
        
        for update in updates[:10]:
            try:
                # 提取标题
                title_elem = update.find(['h1', 'h2', 'h3', 'h4', 'strong', 'a'])
                if not title_elem:
                    continue
                    
                title = title_elem.get_text(strip=True)
                if not title or len(title) < 5:
                    continue
                
                # 提取链接
                link = update.find('a', href=True)
                url = link['href'] if link else ''
                if url and not url.startswith('http'):
                    url = base_url.rstrip('/') + '/' + url.lstrip('/')
                
                # 提取日期
                date_elem = update.find(['time', 'span'], class_=re.compile(r'(date|time)', re.I))
                published_date = None
                if date_elem:
                    date_str = date_elem.get_text(strip=True)
                    published_date = self._parse_date(date_str)
                
                # 提取摘要
                summary_elem = update.find(['p', 'div'], class_=re.compile(r'(summary|description|content)', re.I))
                summary = summary_elem.get_text(strip=True)[:200] if summary_elem else ""
                
                items.append(WebNewsItem(
                    title=title,
                    url=url or base_url,
                    source="扣子Coze文档更新",
                    company="Coze (扣子)",
                    summary=summary,
                    published_date=published_date,
                    category="AI Tool"
                ))
                
            except Exception as e:
                logger.debug(f"解析Coze文章失败: {e}")
                continue
        
        # 如果没找到标准结构，尝试通用解析
        if not items:
            items = self._generic_parse(html, base_url, "扣子Coze文档更新", "Coze (扣子)")
        
        return items
    
    def _generic_parse(self, html: str, base_url: str, source_name: str, company: str) -> List[WebNewsItem]:
        """通用HTML解析"""
        items = []
        soup = BeautifulSoup(html, 'html.parser')
        
        # 移除脚本和样式
        for tag in soup(['script', 'style', 'nav', 'footer', 'header']):
            tag.decompose()
        
        # 查找所有链接
        links = soup.find_all('a', href=True)
        
        seen_urls = set()
        for link in links[:30]:  # 限制处理数量
            url = link['href']
            if url in seen_urls:
                continue
            seen_urls.add(url)
            
            # 跳过导航链接、空链接等
            if url in ['#', '/', ''] or url.startswith('javascript:'):
                continue
            
            title = link.get_text(strip=True)
            
            # 过滤掉太短或太长的标题
            if not title or len(title) < 10 or len(title) > 200:
                continue
            
            # 过滤掉导航类标题
            nav_keywords = ['登录', '注册', '首页', '关于', '联系', '帮助', 'login', 'home', 'about']
            if any(kw in title.lower() for kw in nav_keywords):
                continue
            
            # 补全URL
            if not url.startswith('http'):
                url = base_url.rstrip('/') + '/' + url.lstrip('/')
            
            items.append(WebNewsItem(
                title=title,
                url=url,
                source=source_name,
                company=company,
                summary="",
                published_date=datetime.now(),
                category="AI Company" if "AI" in company or "智谱" in company else "AI Tool"
            ))
        
        return items[:10]  # 最多返回10条
    
    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """解析日期字符串"""
        # 常见日期格式
        patterns = [
            r'(\d{4})[/-](\d{1,2})[/-](\d{1,2})',  # 2024-01-15, 2024/01/15
            r'(\d{1,2})[/-](\d{1,2})[/-](\d{4})',  # 01-15-2024
            r'(\d{4})年(\d{1,2})月(\d{1,2})日',    # 2024年1月15日
        ]
        
        for pattern in patterns:
            match = re.search(pattern, date_str)
            if match:
                groups = match.groups()
                try:
                    if len(groups[0]) == 4:  # 年份在前
                        year, month, day = int(groups[0]), int(groups[1]), int(groups[2])
                    else:  # 年份在后
                        month, day, year = int(groups[0]), int(groups[1]), int(groups[2])
                    return datetime(year, month, day)
                except:
                    pass
        
        return None
    
    def parse(self, url: str, source_type: str) -> List[Dict]:
        """
        主解析入口
        
        Args:
            url: 页面URL
            source_type: 源类型 ('zhipu', 'minimax', 'coze')
        
        Returns:
            新闻列表（字典格式）
        """
        logger.info(f"正在解析: {url} ({source_type})")
        
        html = self.fetch_page(url)
        if not html:
            logger.error(f"无法获取页面: {url}")
            return []
        
        # 根据源类型选择解析方法
        if 'bigmodel' in url or 'zhipu' in url:
            items = self.parse_zhipu(html, url)
        elif 'minimax' in url:
            items = self.parse_minimax(html, url)
        elif 'coze' in url:
            items = self.parse_coze(html, url)
        else:
            # 通用解析
            items = self._generic_parse(html, url, "网页新闻", "未知")
        
        logger.info(f"解析完成: 获得 {len(items)} 条新闻")
        return [item.to_dict() for item in items]


# 便捷函数
def parse_web_news(config: Dict) -> List[Dict]:
    """
    解析网页新闻配置
    
    Args:
        config: sources.yaml中的chinese_ai_companies配置
    
    Returns:
        所有新闻列表
    """
    parser = WebNewsParser()
    all_items = []
    
    sources = config.get('chinese_ai_companies', [])
    if isinstance(sources, dict):
        # 处理enabled字段
        sources = [s for s in sources.values() if isinstance(s, dict)]
    
    for source in sources:
        if not source.get('enabled', True):
            continue
            
        url = source.get('url')
        if not url:
            continue
        
        items = parser.parse(url, source.get('name', ''))
        for item in items:
            item['source_config'] = source
        all_items.extend(items)
    
    return all_items


if __name__ == '__main__':
    # 测试
    logging.basicConfig(level=logging.INFO)
    
    test_sources = [
        ('https://docs.bigmodel.cn/cn/update/new-releases', 'zhipu'),
        ('https://www.minimaxi.com/news', 'minimax'),
        ('https://docs.coze.cn', 'coze'),
    ]
    
    parser = WebNewsParser()
    for url, source_type in test_sources:
        print(f"\n{'='*60}")
        print(f"测试: {url}")
        print('='*60)
        items = parser.parse(url, source_type)
        for item in items[:5]:
            print(f"\n标题: {item['title']}")
            print(f"链接: {item['url']}")
            print(f"来源: {item['source']}")
            if item.get('published_date'):
                print(f"日期: {item['published_date']}")
