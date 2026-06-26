#!/usr/bin/env python3
"""
设计师情报站 - RSS 抓取器

功能：
- 批量解析 RSS/Atom 源
- 提取标题、链接、摘要、发布时间
- 支持并发抓取
- 结果缓存

使用方式:
    python rss_fetcher.py fetch <source_id>     # 抓取单个源
    python rss_fetcher.py fetch-all             # 抓取所有启用的 RSS 源
    python rss_fetcher.py test <url>            # 测试 RSS 源
"""

import feedparser
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# 导入信息源管理
from sources_manager import get_enabled_sources, get_source

# 缓存目录
CACHE_DIR = Path(__file__).parent.parent / "data" / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)


class RSSItem:
    """RSS 条目数据结构"""
    
    def __init__(self, title: str, link: str, source: str, source_id: str,
                 published: Optional[datetime] = None, summary: Optional[str] = None,
                 author: Optional[str] = None, tags: Optional[list[str]] = None):
        self.title = title
        self.link = link
        self.source = source
        self.source_id = source_id
        self.published = published
        self.summary = summary
        self.author = author
        self.tags = tags or []
    
    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "link": self.link,
            "source": self.source,
            "source_id": self.source_id,
            "published": self.published.isoformat() if self.published else None,
            "summary": self.summary,
            "author": self.author,
            "tags": self.tags,
            "type": "rss",
        }


def parse_date(date_tuple) -> Optional[datetime]:
    """解析 feedparser 的日期格式"""
    if not date_tuple:
        return None
    try:
        # feedparser 返回 time.struct_time
        return datetime(*date_tuple[:6], tzinfo=timezone.utc)
    except (TypeError, ValueError):
        return None


def fetch_rss(url: str, source_id: str, source_name: str, timeout: int = 10) -> list[RSSItem]:
    """
    抓取单个 RSS 源
    
    Args:
        url: RSS 源 URL
        source_id: 信息源 ID
        source_name: 信息源名称
        timeout: 请求超时（秒）
    
    Returns:
        RSSItem 列表
    """
    try:
        # feedparser 不直接支持 timeout，需要通过 agent 设置
        import urllib.request
        opener = urllib.request.build_opener()
        response = opener.open(url, timeout=timeout)
        feed_content = response.read()
        feed = feedparser.parse(feed_content)
        
        if feed.bozo:
            print(f"警告：{source_name} RSS 解析警告：{feed.bozo_exception}")
        
        items = []
        for entry in feed.entries[:20]:  # 每个源最多取 20 条
            title = entry.get("title", "无标题")
            link = entry.get("link", "")
            
            if not link:
                continue  # 跳过无链接的条目
            
            # 提取摘要
            summary = ""
            if hasattr(entry, "summary"):
                summary = entry.summary[:500]  # 限制长度
            elif hasattr(entry, "description"):
                summary = entry.description[:500]
            
            # 提取发布时间
            published = None
            if hasattr(entry, "published_parsed"):
                published = parse_date(entry.published_parsed)
            elif hasattr(entry, "updated_parsed"):
                published = parse_date(entry.updated_parsed)
            
            # 提取标签
            tags = []
            if hasattr(entry, "tags"):
                tags = [tag.term for tag in entry.tags if hasattr(tag, "term")]
            
            # 提取作者
            author = entry.get("author", "")
            
            items.append(RSSItem(
                title=title,
                link=link,
                source=source_name,
                source_id=source_id,
                published=published,
                summary=summary,
                author=author,
                tags=tags,
            ))
        
        return items
    
    except Exception as e:
        print(f"错误：抓取 {source_name} 失败 - {e}")
        return []


def fetch_all_rss(max_workers: int = 5, limit_per_source: int = 10) -> list[RSSItem]:
    """
    并发抓取所有启用的 RSS 源
    
    Args:
        max_workers: 并发数
        limit_per_source: 每个源最多抓取的条目数
    
    Returns:
        RSSItem 列表（按发布时间排序）
    """
    # 获取所有 RSS 源
    sources = [s for s in get_enabled_sources() if s["type"] == "RSS 源"]
    
    if not sources:
        print("未找到启用的 RSS 源")
        return []
    
    print(f"开始抓取 {len(sources)} 个 RSS 源...")
    
    all_items = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 提交任务
        future_to_source = {
            executor.submit(
                fetch_rss,
                s["url"],
                s["id"],
                s["name"],
            ): s for s in sources
        }
        
        # 收集结果
        for future in as_completed(future_to_source):
            source = future_to_source[future]
            try:
                items = future.result()
                # 限制每个源的条目数
                items = items[:limit_per_source]
                all_items.extend(items)
                print(f"✅ {source['name']}: {len(items)} 条")
            except Exception as e:
                print(f"❌ {source['name']}: 抓取失败 - {e}")
    
    # 按发布时间排序（最新的在前）
    all_items.sort(key=lambda x: x.published or datetime.min.replace(tzinfo=timezone.utc), reverse=True)
    
    print(f"\n共抓取 {len(all_items)} 条 RSS 条目")
    return all_items


def save_to_cache(items: list[RSSItem], filename: Optional[str] = None):
    """缓存抓取结果"""
    if not filename:
        filename = f"rss_cache_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    cache_file = CACHE_DIR / filename
    
    data = [item.to_dict() for item in items]
    
    with open(cache_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"缓存已保存：{cache_file}")


def load_from_cache(filename: str) -> list[dict]:
    """从缓存加载"""
    cache_file = CACHE_DIR / filename
    
    if not cache_file.exists():
        return []
    
    with open(cache_file, "r", encoding="utf-8") as f:
        return json.load(f)


def test_rss(url: str) -> bool:
    """测试 RSS 源是否可用"""
    try:
        feed = feedparser.parse(url, request_timeout=10)
        
        if feed.bozo:
            print(f"⚠️  警告：RSS 解析警告 - {feed.bozo_exception}")
        
        if feed.entries:
            print(f"✅ RSS 源有效，共 {len(feed.entries)} 条")
            print(f"   标题：{feed.feed.get('title', '无')}")
            print(f"   最新：{feed.entries[0].get('title', '无')}")
            return True
        else:
            print("⚠️  RSS 源无内容")
            return False
    
    except Exception as e:
        print(f"❌ RSS 源无效 - {e}")
        return False


# CLI 入口
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "fetch":
        if len(sys.argv) < 3:
            print("用法：python rss_fetcher.py fetch <source_id>")
            sys.exit(1)
        
        source = get_source(sys.argv[2])
        if not source:
            print(f"未找到信息源：{sys.argv[2]}")
            sys.exit(1)
        
        items = fetch_rss(source["url"], source["id"], source["name"])
        print(f"\n抓取到 {len(items)} 条:")
        for item in items[:10]:
            print(f"  - {item.title[:50]}... ({item.source})")
    
    elif command == "fetch-all":
        items = fetch_all_rss()
        save_to_cache(items)
        
        # 输出为 JSON（供 Agent 使用）
        if len(sys.argv) > 2 and sys.argv[2] == "--json":
            print(json.dumps([item.to_dict() for item in items], ensure_ascii=False, indent=2))
    
    elif command == "test":
        if len(sys.argv) < 3:
            print("用法：python rss_fetcher.py test <url>")
            sys.exit(1)
        test_rss(sys.argv[2])
    
    elif command == "list-cache":
        cache_files = list(CACHE_DIR.glob("rss_cache_*.json"))
        if cache_files:
            print("缓存文件:")
            for f in cache_files[-10:]:
                print(f"  {f.name}")
        else:
            print("无缓存文件")
    
    else:
        print(f"未知命令：{command}")
        sys.exit(1)
