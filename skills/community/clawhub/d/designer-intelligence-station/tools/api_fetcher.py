#!/usr/bin/env python3
"""
设计师情报站 - API 集成模块

功能：
- Product Hunt API（新产品发现）
- GitHub Trending（开源项目趋势）
- 其他平台 API 集成

使用方式:
    python api_fetcher.py producthunt        # 抓取 Product Hunt 今日热门
    python api_fetcher.py github             # 抓取 GitHub Trending
"""

import json
import requests
from datetime import datetime, timezone
from bs4 import BeautifulSoup
from pathlib import Path
from typing import Optional

# 缓存目录
CACHE_DIR = Path(__file__).parent.parent / "data" / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)


class APIItem:
    """API 抓取条目数据结构"""
    
    def __init__(self, title: str, link: str, source: str, source_id: str,
                 summary: Optional[str] = None, author: Optional[str] = None,
                 tags: Optional[list[str]] = None, extra: Optional[dict] = None):
        self.title = title
        self.link = link
        self.source = source
        self.source_id = source_id
        self.summary = summary
        self.author = author
        self.tags = tags or []
        self.extra = extra or {}
        self.published = datetime.now(timezone.utc)
    
    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "link": self.link,
            "source": self.source,
            "source_id": self.source_id,
            "published": self.published.isoformat(),
            "summary": self.summary,
            "author": self.author,
            "tags": self.tags,
            "type": "api",
            "extra": self.extra,
        }


def fetch_producthunt(limit: int = 20) -> list[APIItem]:
    """
    抓取 Product Hunt 今日热门产品
    
    注意：Product Hunt 需要 API 认证，这里使用网页抓取作为替代
    """
    url = "https://www.producthunt.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        items = []
        
        # Product Hunt 页面结构复杂，这里尝试提取热门产品
        # 注意：实际使用时可能需要根据页面结构调整选择器
        product_cards = soup.select('div[class*="PostItem"]')[:limit]
        
        for card in product_cards:
            try:
                title_elem = card.select_one('a[href*="/posts/"]')
                if not title_elem:
                    continue
                
                title = title_elem.get_text(strip=True)
                link = "https://www.producthunt.com" + title_elem.get('href', '')
                
                # 提取描述
                summary_elem = card.select_one('div[class*="PostItem__summary"]')
                summary = summary_elem.get_text(strip=True)[:200] if summary_elem else ""
                
                # 提取标签
                tags = []
                for tag_elem in card.select('a[class*="Tag__Anchor"]')[:5]:
                    tag = tag_elem.get_text(strip=True)
                    if tag:
                        tags.append(tag)
                
                # 提取票数
                votes_elem = card.select_one('button[data-test="vote-button"]')
                votes = votes_elem.get_text(strip=True) if votes_elem else ""
                
                items.append(APIItem(
                    title=title,
                    link=link,
                    source="Product Hunt",
                    source_id="COM001",
                    summary=summary,
                    tags=tags,
                    extra={"votes": votes},
                ))
            except Exception as e:
                continue
        
        print(f"Product Hunt: 抓取到 {len(items)} 个产品")
        return items
    
    except Exception as e:
        print(f"Product Hunt 抓取失败：{e}")
        return []


def fetch_github_trending(since: str = "daily", language: Optional[str] = None) -> list[APIItem]:
    """
    抓取 GitHub Trending
    
    Args:
        since: daily/weekly/monthly
        language: 编程语言过滤（如 Python、JavaScript）
    """
    url = f"https://github.com/trending/{language}" if language else "https://github.com/trending"
    params = {"since": since}
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        items = []
        
        # GitHub Trending 文章卡片
        articles = soup.select('article.Box-row')[:20]
        
        for article in articles:
            try:
                # 提取标题（包含作者和仓库名）
                title_elem = article.select_one('h2 a')
                if not title_elem:
                    continue
                
                full_name = title_elem.get_text(strip=True)  # 如：owner/repo
                link = "https://github.com" + title_elem.get('href', '')
                
                # 提取描述
                summary_elem = article.select_one('p')
                summary = summary_elem.get_text(strip=True)[:200] if summary_elem else ""
                
                # 提取语言
                lang_elem = article.select_one('span[itemprop="programmingLanguage"]')
                language = lang_elem.get_text(strip=True) if lang_elem else ""
                
                # 提取星标数
                stars_elem = article.select_one('a[href$="/stargazers"]')
                stars = stars_elem.get_text(strip=True) if stars_elem else ""
                
                # 提取 fork 数
                forks_elem = article.select_one('a[href$="/forks"]')
                forks = forks_elem.get_text(strip=True) if forks_elem else ""
                
                items.append(APIItem(
                    title=full_name,
                    link=link,
                    source="GitHub Trending",
                    source_id="COM002",
                    summary=summary,
                    tags=[language] if language else [],
                    extra={"stars": stars, "forks": forks, "since": since},
                ))
            except Exception as e:
                continue
        
        print(f"GitHub Trending ({since}): 抓取到 {len(items)} 个项目")
        return items
    
    except Exception as e:
        print(f"GitHub Trending 抓取失败：{e}")
        return []


def fetch_all_api(limit_per_source: int = 20) -> list[APIItem]:
    """抓取所有 API 源"""
    all_items = []
    
    # Product Hunt
    ph_items = fetch_producthunt(limit=limit_per_source)
    all_items.extend(ph_items)
    
    # GitHub Trending
    gh_items = fetch_github_trending(since="daily")
    all_items.extend(gh_items)
    
    print(f"\nAPI 抓取完成：共 {len(all_items)} 条")
    return all_items


def save_to_cache(items: list[APIItem], prefix: str = "api"):
    """缓存抓取结果"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{prefix}_cache_{timestamp}.json"
    cache_file = CACHE_DIR / filename
    
    data = [item.to_dict() for item in items]
    
    with open(cache_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"缓存已保存：{cache_file}")
    return cache_file


# CLI 入口
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "producthunt":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 20
        items = fetch_producthunt(limit=limit)
        for item in items[:10]:
            print(f"  - {item.title} ({item.extra.get('votes', '?')} votes)")
        save_to_cache(items, "producthunt")
    
    elif command == "github":
        since = sys.argv[2] if len(sys.argv) > 2 else "daily"
        language = sys.argv[3] if len(sys.argv) > 3 else None
        items = fetch_github_trending(since=since, language=language)
        for item in items[:10]:
            print(f"  - {item.title} ⭐{item.extra.get('stars', '?')}")
        save_to_cache(items, "github")
    
    elif command == "fetch-all":
        items = fetch_all_api()
        save_to_cache(items, "api")
        
        # 输出 JSON（供 Agent 使用）
        if len(sys.argv) > 2 and sys.argv[2] == "--json":
            print(json.dumps([item.to_dict() for item in items], ensure_ascii=False, indent=2))
    
    else:
        print(f"未知命令：{command}")
        sys.exit(1)
